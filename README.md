🍞 Smart Bakery IoT Monitoring & Control System

An end-to-end Internet of Things (IoT) solution designed for commercial bakery environments where temperature and humidity critically affect product quality. The system provides remote monitoring, real-time alerts, and remote control of environmental conditions using Raspberry Pi, BME280, MQTT, Firebase, and Telegram Bot integration.

📌 Table of Contents

📘 Project Overview

🎯 Objectives

🧱 System Architecture

🔧 Hardware Components

🧩 Software Components

🌐 Features

📡 MQTT Topics

🌈 Dashboard (Cloud Layer)

🤖 Telegram Bot Commands

📊 IoT Data Flow

⚙️ Raspberry Pi GPIO Map

🚧 Challenges Faced

✨ Improvements & Recommended Add-Ons

📎 Links

📘 Project Overview

Commercial bakeries rely heavily on stable temperature and humidity for dough preparation, proofing, and ingredient storage. This IoT system allows floor managers to:

Monitor live conditions remotely

Receive alerts when thresholds are exceeded

Control air-conditioning systems (simulated with a fan)

Access dashboards from any smart device

View real-time and historical data

The system integrates hardware sensing, communication, cloud data visualization, and user interfaces (web, mobile, Telegram bot) into one unified IoT solution.

🎯 Objectives

✔ Real-time temperature & humidity monitoring
✔ Automatic & manual control of cooling system
✔ Trigger alarms when threshold is exceeded
✔ Remote access using smart devices
✔ Data visualization with trends & history
✔ Cloud-synchronized status and controls
✔ Multi-platform user interaction (Web, MQTT, Telegram)

🧱 System Architecture
🏭 Edge Layer (Physical Bakery Environment)

Raspberry Pi (edge computing + gateway)

BME280 Temperature & Humidity Sensor

Fan (simulated air-conditioning system)

Buzzer (alert system)

Status LEDs for AUTO / MANUAL modes

📡 Communication Layer

MQTT protocol for lightweight messaging

Publishes sensor data

Subscribes to control commands

Topic-based communication for scalability

☁️ Cloud Layer

Firebase Realtime Database

Stores live data, history, controls, system status

Hosts web dashboard

👤 User Layer

Firebase web dashboard

MQTT mobile apps

Telegram Bot for remote commands

Real-time control panel + graph analytics

🔧 Hardware Components

Raspberry Pi (main controller & gateway)

BME280 Sensor (temperature & humidity)

5V Fan (simulated cooling system)

Active Buzzer (alarms)

Relay Module (fan control)

LED Indicators (manual/auto modes)

Jumper wires + breadboard

🧩 Software Components

Python (Raspberry Pi logic)

MQTT (Mosquitto broker)

Firebase Realtime Database

HTML/CSS/JS Dashboard

Chart.js for graphs

Telegram Bot API

Paho-MQTT for messaging

Firebase Admin SDK

🌐 Features
🌡 Real-Time Monitoring

Live temperature & humidity readings

Automatic threshold-based decisions

Uptime monitoring

Online/offline status reporting

🌀 Automated Cooling System

Fan turns ON when temperature exceeds threshold

Buzzer activates for high-temp alerts

Both can be switched to manual override

📱 Multi-Platform Control

Web dashboard for live control

Telegram bot commands

MQTT app manual overrides

📊 Data Visualization

Real-time graph plotting

Historical dataset (timestamped)

Dynamic charts for temp & humidity

🛡 User Authentication

Username/password login

Password reset

Persistent sessions

📡 MQTT Topics
Topic	Direction	Description
sensor/bme280	Pi → Broker	Publishes temperature & humidity
status/fan	Pi → Broker	Fan ON/OFF status
status/buzzer	Pi → Broker	Buzzer ON/OFF status
control/fan	User → Pi	Manual/Auto fan overwrite
control/buzzer	User → Pi	Manual/Auto buzzer overwrite
config/threshold	User → Pi	Update temperature threshold
status/threshold	Pi → Broker	Current threshold value
status/uptime	Pi → Broker	System uptime
status/availability	Pi → Broker	online/offline
🌈 Dashboard (Cloud Layer)

The Firebase web app includes:

✔ Live sensor data
✔ Fan & buzzer control buttons
✔ Auto/manual switching
✔ Temperature & humidity charts
✔ Login / Signup / Password reset
✔ Historical data plotting

Fully responsive for mobile & desktop.

🤖 Telegram Bot Commands
Command	Function
/start	Show command help
/status	Display live temp, humidity & system status
/fan on/off/auto	Manually control the fan
/buzzer on/off/auto	Control the buzzer
/threshold <value>	Set temperature threshold
📊 IoT Data Flow

Sensor captures data

Raspberry Pi processes and publishes via MQTT

Data is stored in Firebase

Dashboard retrieves and displays data

User sends commands (Web/MQTT/Telegram)

Cloud relays control instructions

Raspberry Pi executes the command (fan/buzzer)

⚙️ Raspberry Pi GPIO Map
Component	Pin	Direction	Description
BME280 SDA	GPIO 2	Input	I2C Data
BME280 SCL	GPIO 3	Input	I2C Clock
Fan (Relay)	GPIO 18	Output	Controls AC/Fan
Buzzer	GPIO 17	Output	Alarm
White LED	GPIO 27	Output	Fan Auto/Manual Indicator
Red LED	GPIO 22	Output	Buzzer Auto/Manual Indicator
🚧 Challenges Faced
🔹 Sensor Misreadings

Fixed with shorter wiring + secure connections.

🔹 GPIO Conflicts

Resolved using a pin assignment table.

🔹 MQTT Connection Loss

Added reconnection logic & buffering.

🔹 Topic Mismatches

Used centralized config + testing.

🔹 Unstable thresholds

Implemented calibration & remote slider-based adjustment.

✨ Improvements & Recommended Add-Ons

Add predictive analytics (forecasting temp spikes)

Implement email/SMS alerts

Automate daily reports (PDFs)

Upgrade dashboard UI using React

Add more sensors (CO₂, airflow, motion)

Use Node-RED for visual flow programming

Migrate to HTTPS + strengthened auth

📎 Links
🌐 Web Dashboard

https://smart-bakery-bc347.web.app/

🤖 Telegram Bot

https://t.me/IOTP_smartbakery_bot
