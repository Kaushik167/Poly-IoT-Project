# 🍞 Smart Bakery IoT Monitoring & Control System

An end-to-end Internet of Things (IoT) solution designed for commercial bakery environments where temperature and humidity critically affect product quality.  
The system provides **remote monitoring**, **real-time alerts**, and **remote control** of environmental conditions using:

- **Raspberry Pi**
- **BME280 Sensor**
- **MQTT**
- **Firebase**
- **Telegram Bot**

---

## 📘 Project Overview

Commercial bakeries rely heavily on **stable temperature and humidity** for dough preparation, proofing, and ingredient storage.

This IoT system allows floor managers to:

- Monitor live environmental conditions remotely  
- Receive alerts when thresholds are exceeded  
- Control the air-conditioning system (simulated with a fan)  
- Access a dashboard from any smart device  
- View real-time and historical data  

The system integrates hardware sensing, cloud data visualization, MQTT communication and user interfaces into one unified IoT solution.

---

## 🎯 Objectives

- ✔ Real-time temperature & humidity monitoring  
- ✔ Automatic & manual cooling control  
- ✔ Trigger alerts when temperature exceeds thresholds  
- ✔ Remote access via web, mobile, MQTT & Telegram  
- ✔ Historical trend visualisation  
- ✔ Centralized cloud storage and synchronization  
- ✔ Multi-platform control and feedback  

---

## 🧱 System Architecture

### 🏭 **Edge Layer (Physical Bakery Environment)**  
- Raspberry Pi (edge computing + gateway)  
- BME280 temperature & humidity sensor  
- 5V fan (simulated air-conditioning system)  
- Buzzer (alert system)  
- LEDs to indicate AUTO / MANUAL control  

### 📡 **Communication Layer (MQTT)**  
- Lightweight and fast publish/subscribe model  
- Sends sensor readings  
- Receives control commands  
- Ensures real-time communication between devices and dashboard  

### ☁️ **Cloud Layer (Firebase)**  
- Realtime database for storing:  
  - Sensor history  
  - Device status  
  - Control state  
- Hosts web dashboard interface  

### 👤 **User Layer**  
- Firebase-hosted web dashboard  
- Telegram Bot  
- MQTT mobile app  

---

## 🔧 Hardware Components

- Raspberry Pi  
- BME280 Temperature & Humidity Sensor  
- 5V DC Fan  
- Active Buzzer  
- Relay module (for fan control)  
- White & Red LEDs for mode/status indication  
- Breadboard + jumper wires  

---

## 🧩 Software Components

- Python (primary logic running on Raspberry Pi)  
- MQTT with Mosquitto broker  
- Paho-MQTT client  
- Firebase Realtime Database  
- Firebase Admin SDK  
- HTML / CSS / JavaScript (dashboard UI)  
- Chart.js (data visualization)  
- Telegram Bot API  

---

## 🌐 Features

### 🌡 Real-Time Monitoring  
- Live temperature & humidity readings  
- Threshold-based logic for alerts  
- System uptime monitoring  
- Online/offline status reporting  

### 🌀 Automated Cooling System  
- Fan automatically turns on when temperature exceeds threshold  
- Buzzer triggers during high-temperature events  
- Both components support **Manual** and **Auto** modes  

### 📱 Multi-Platform Control  
- Web dashboard  
- Telegram bot commands  
- MQTT app remote controls  

### 📊 Data Visualization  
- Real-time temperature & humidity graphs  
- Historical data stored in Firebase  
- Dynamic, auto-updating charts  

### 🛡 User Authentication  
- Username/password login  
- Password reset functionality  
- Persistent login sessions  

---

## 📡 MQTT Topics

**Published by Raspberry Pi**
- `sensor/bme280` – Temperature & humidity  
- `status/fan` – Fan ON/OFF  
- `status/buzzer` – Buzzer ON/OFF  
- `status/threshold` – Current threshold  
- `status/uptime` – System uptime  
- `status/availability` – Online/offline  

**Received by Raspberry Pi**
- `control/fan` – ON / OFF / AUTO  
- `control/buzzer` – ON / OFF / AUTO  
- `config/threshold` – Update temperature threshold  

---

## 🌈 Dashboard (Cloud Layer)

The Firebase dashboard provides:

- ✔ Live temperature & humidity  
- ✔ Fan & Buzzer status  
- ✔ Control buttons: ON / OFF / AUTO  
- ✔ Login, Signup & Password Reset  
- ✔ Real-time graphs using Chart.js  
- ✔ Full history view  

Fully responsive for both mobile & desktop.

---

## 🤖 Telegram Bot Commands

| Command | Function |
|--------|----------|
| `/start` | Show help message |
| `/status` | Shows current temp, humidity, fan & buzzer mode |
| `/fan on/off/auto` | Control the fan |
| `/buzzer on/off/auto` | Control the buzzer |
| `/threshold <value>` | Change temperature threshold |

---

## 📊 IoT Data Flow

1. BME280 collects sensor data  
2. Raspberry Pi processes & publishes via MQTT  
3. Data stored in Firebase  
4. Dashboard retrieves and visualises data  
5. User sends commands via Web/MQTT/Telegram  
6. Pi executes commands (fan, buzzer, threshold)  

---

## ⚙️ Raspberry Pi GPIO Map

| Component | GPIO Pin | Mode | Description |
|----------|----------|------|-------------|
| BME280 SDA | GPIO 2 | Input | I²C Data |
| BME280 SCL | GPIO 3 | Input | I²C Clock |
| Fan (Relay) | GPIO 18 | Output | Controls fan |
| Buzzer | GPIO 17 | Output | Alarm |
| White LED | GPIO 27 | Output | Fan Auto/Manual Indicator |
| Red LED | GPIO 22 | Output | Buzzer Auto/Manual Indicator |

---

## 🚧 Challenges Faced

### 🔹 Sensor Misreadings  
Solved with shorter wiring and stable power.

### 🔹 GPIO Conflicts  
Prevented using a pin assignment table.

### 🔹 MQTT Connection Drops  
Added reconnection + buffering logic.

### 🔹 Topic Naming Mistakes  
Standardized topics using configuration constants.

### 🔹 Unstable Threshold Behaviour  
Implemented calibration + remote adjustable slider.

---

## ✨ Improvements & Recommended Add-Ons

- Temperature prediction using ML  
- Email/SMS alert integration  
- Daily PDF report generation  
- React-based improved dashboard  
- Additional sensors (CO₂, motion, airflow)  
- Node-RED for graphical flow automation  
- Migration to HTTPS + secure auth  

---

## 📎 Links

### 🌐 Web Dashboard  
https://smart-bakery-bc347.web.app/

### 🤖 Telegram Bot  
https://t.me/IOTP_smartbakery_bot
