# import the modules
import time
import threading
import board
import adafruit_bme280.advanced as adafruit_bme280
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db
from telegram.ext import Updater, CommandHandler

# ========== Firebase Initialization ==========
cred = credentials.Certificate("/home/pi/Project/serviceAccountKey.json") # load firebase credentials
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://smart-bakery-bc347-default-rtdb.asia-southeast1.firebasedatabase.app/"
}) # initialize firebase app with the URL

# ========== GPIO Setup ==========
FAN_RELAY_PIN = 18  # for fan
BUZZER_PIN = 17     # for buzzer
WHITE_LED_PIN = 27  # White LED for fan manual/auto status
RED_LED_PIN = 22    # Red LED for buzzer manual/auto status

GPIO.setmode(GPIO.BCM)

# configure pins as output
GPIO.setup(FAN_RELAY_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(WHITE_LED_PIN, GPIO.OUT)
GPIO.setup(RED_LED_PIN, GPIO.OUT)

# set all the outputs to low initially (off)
GPIO.output(FAN_RELAY_PIN, GPIO.LOW)
GPIO.output(BUZZER_PIN, GPIO.LOW)
GPIO.output(WHITE_LED_PIN, GPIO.LOW)
GPIO.output(RED_LED_PIN, GPIO.LOW)

# ========== Sensor Setup ==========
i2c = board.I2C()
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
bme280.sea_level_pressure = 1013.25

# ========== MQTT Setup ==========
BROKER = "localhost" # MQTT broker address
PORT = 1883 # MQTT broker port

# MQTT Topics to subscribe to
SENSOR_TOPIC = "sensor/bme280"
FAN_TOPIC = "control/fan"
BUZZER_TOPIC = "control/buzzer"
THRESHOLD_TOPIC = "config/threshold"
STATUS_FAN_TOPIC = "status/fan"
STATUS_BUZZER_TOPIC = "status/buzzer"
STATUS_THRESHOLD_TOPIC = "status/threshold"
UPTIME_TOPIC = "status/uptime"

# dictionary to store control states
control = {
    "manual_fan": None, # set to auto
    "manual_buzzer": None, # set to auto
    "temp_threshold": 27.5 # default threshold
}

# MQTT connection callback
def on_connect(client, userdata, flags, rc):
    print(f"MQTT Connected with result code {rc}")
    client.subscribe([
        (FAN_TOPIC, 0),
        (BUZZER_TOPIC, 0),
        (THRESHOLD_TOPIC, 0)
    ])

# MQTT message callback
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode().lower()
    print(f"MQTT message received on {topic}: {payload}")

    if topic == FAN_TOPIC:
        userdata["manual_fan"] = None if payload == "auto" else (payload == "on")
    elif topic == BUZZER_TOPIC:
        userdata["manual_buzzer"] = None if payload == "auto" else (payload == "on")
    elif topic == THRESHOLD_TOPIC:
        try:
            userdata["temp_threshold"] = float(payload)
            print(f"Threshold updated to {userdata['temp_threshold']}")
        except ValueError:
            print("Invalid threshold value")

# configure MQTT client
client = mqtt.Client(userdata=control)
client.on_connect = on_connect
client.on_message = on_message
client.will_set("status/availability", "offline", retain=True)
client.connect(BROKER, PORT, 60)
client.publish("status/availability", "online", retain=True)
client.loop_start()

# ========== Firebase Control Listener ==========
control_ref = db.reference("iot_data/control")

def firebase_control_listener(event):
    control_data = event.data

    if isinstance(control_data, str):
        key = event.path.lstrip('/')
        if key == "fan":
            fan_state = control_data.lower()
            control["manual_fan"] = None if fan_state == "auto" else (fan_state == "on")
            print(f"Firebase updated manual_fan to: {control['manual_fan']}")
        elif key == "buzzer":
            buzzer_state = control_data.lower()
            control["manual_buzzer"] = None if buzzer_state == "auto" else (buzzer_state == "on")
            print(f"Firebase updated manual_buzzer to: {control['manual_buzzer']}")
    elif isinstance(control_data, dict):
        fan_state = control_data.get("fan", "auto").lower()
        buzzer_state = control_data.get("buzzer", "auto").lower()
        control["manual_fan"] = None if fan_state == "auto" else (fan_state == "on")
        control["manual_buzzer"] = None if buzzer_state == "auto" else (buzzer_state == "on")
        print(f"Firebase updated manual_fan to: {control['manual_fan']}, manual_buzzer to: {control['manual_buzzer']}")

# listen for changes in firebase control
control_ref.listen(firebase_control_listener)

# ========== Telegram Bot ==========
TELEGRAM_TOKEN = "7755409480:AAEyfKkaHu8ax1tSW_74W3v9eoSjDPd01_A"

# command - /start
def start(update, context):
    update.message.reply_text("Use /status, /fan on|off|auto, /buzzer on|off|auto, /threshold <value>")

# command - /status
def status(update, context):
    temp = bme280.temperature
    humidity = bme280.humidity
    fan_state = "Manual ON" if control["manual_fan"] else "Manual OFF" if control["manual_fan"] is False else "Auto"
    buzzer_state = "Manual ON" if control["manual_buzzer"] else "Manual OFF" if control["manual_buzzer"] is False else "Auto"
    threshold = control["temp_threshold"]

    msg = (
        f"🌡 Temp: {temp:.2f} °C\n💧 Humidity: {humidity:.2f} %\n"
        f"🌀 Fan: {fan_state}\n🔔 Buzzer: {buzzer_state}\n"
        f"⚙️ Threshold: {threshold} °C"
    )
    update.message.reply_text(msg)

# command - /fan
def fan(update, context):
    arg = context.args[0].lower() if context.args else ""
    if arg == "on":
        control["manual_fan"] = True
        update.message.reply_text("Fan set to ON (Manual)")
    elif arg == "off":
        control["manual_fan"] = False
        update.message.reply_text("Fan set to OFF (Manual)")
    elif arg == "auto":
        control["manual_fan"] = None
        update.message.reply_text("Fan set to AUTO")
    else:
        update.message.reply_text("Usage: /fan on|off|auto")

# command - /buzzer
def buzzer(update, context):
    arg = context.args[0].lower() if context.args else ""
    if arg == "on":
        control["manual_buzzer"] = True
        update.message.reply_text("Buzzer set to ON (Manual)")
    elif arg == "off":
        control["manual_buzzer"] = False
        update.message.reply_text("Buzzer set to OFF (Manual)")
    elif arg == "auto":
        control["manual_buzzer"] = None
        update.message.reply_text("Buzzer set to AUTO")
    else:
        update.message.reply_text("Usage: /buzzer on|off|auto")

# command - /threshold
def threshold(update, context):
    try:
        value = float(context.args[0])
        control["temp_threshold"] = value
        update.message.reply_text(f"Threshold set to {value:.2f} °C")
    except (IndexError, ValueError):
        update.message.reply_text("Usage: /threshold <value>")

# Initialize Telegram bot
updater = Updater(TELEGRAM_TOKEN, request_kwargs={'read_timeout': 20, 'connect_timeout': 20})
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("status", status))
dp.add_handler(CommandHandler("fan", fan))
dp.add_handler(CommandHandler("buzzer", buzzer))
dp.add_handler(CommandHandler("threshold", threshold))
updater.start_polling()

# ========== LED Blinker Thread ==========
stop_threads = False

def led_blinker():
    white_led_state = False
    red_led_state = False

    while not stop_threads:
        # White LED for fan - blinking logic
        if control["manual_fan"] is None:  # Auto mode: blink
            white_led_state = not white_led_state
            GPIO.output(WHITE_LED_PIN, GPIO.HIGH if white_led_state else GPIO.LOW)
        else:  # Manual mode: steady ON or OFF
            GPIO.output(WHITE_LED_PIN, GPIO.HIGH if control["manual_fan"] else GPIO.LOW)

        # Red LED for buzzer - blinking logic
        if control["manual_buzzer"] is None:  # Auto mode: blink
            red_led_state = not red_led_state
            GPIO.output(RED_LED_PIN, GPIO.HIGH if red_led_state else GPIO.LOW)
        else:  # Manual mode: steady ON or OFF
            GPIO.output(RED_LED_PIN, GPIO.HIGH if control["manual_buzzer"] else GPIO.LOW)

        time.sleep(0.5) # blinking time

# start led blinking thread
blinker_thread = threading.Thread(target=led_blinker)
blinker_thread.start()

# ========== Main Loop ==========
start_time = time.time()

try:
    while True:
        temp = bme280.temperature
        humidity = bme280.humidity

        # Publish sensor data to MQTT
        sensor_data = json.dumps({
            "temperature": round(temp, 2),
            "humidity": round(humidity, 2)
        })
        client.publish(SENSOR_TOPIC, sensor_data)

        # Save data to Firebase history
        timestamp = datetime.now().isoformat().replace(":", "_").replace(".", "_")
        firebase_data = {
            "temperature": round(temp, 2),
            "humidity": round(humidity, 2)
        }
        db.reference(f"iot_data/history/{timestamp}").set(firebase_data)

        # Fan control logic
        fan_on = (
            control["manual_fan"] if control["manual_fan"] is not None else temp > control["temp_threshold"]
        )
        GPIO.output(FAN_RELAY_PIN, GPIO.HIGH if fan_on else GPIO.LOW)

        # Buzzer control logic
        buzzer_on = (
            control["manual_buzzer"] if control["manual_buzzer"] is not None else temp > control["temp_threshold"]
        )
        GPIO.output(BUZZER_PIN, GPIO.HIGH if buzzer_on else GPIO.LOW)

        # Publish statuses over MQTT
        uptime = int(time.time() - start_time)
        client.publish(STATUS_FAN_TOPIC, "on" if fan_on else "off")
        client.publish(STATUS_BUZZER_TOPIC, "on" if buzzer_on else "off")
        client.publish(STATUS_THRESHOLD_TOPIC, str(control["temp_threshold"]))
        client.publish(UPTIME_TOPIC, str(uptime), retain=True)

        # Update Firebase status over MQTT
        db.reference("iot_data/status").update({
            "fan": "on" if fan_on else "off",
            "buzzer": "on" if buzzer_on else "off",
            "threshold": control["temp_threshold"],
            "uptime": f"{uptime} seconds"
        })

        # print current status to terminal
        print(f"Temp: {temp:.2f} °C, Humidity: {humidity:.2f} %")
        print(f"Fan: {'ON' if fan_on else 'OFF'} | Buzzer: {'ON' if buzzer_on else 'OFF'} | Threshold: {control['temp_threshold']} °C")
        print("-" * 40)

        time.sleep(5) # 5 seconds cycle

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    # Stop blinking thread and cleanup
    stop_threads = True
    blinker_thread.join()

    GPIO.cleanup()
    client.loop_stop()
    client.disconnect()
    updater.stop()

