
# MAVLink Web Interface  

## 🚀 Overview  
This project provides a **web-based interface** to interact with a MAVLink-enabled drone. It uses **Flask, Socket.IO, and pymavlink** to receive MAVLink messages and display real-time telemetry data.  

🔹 **Features:**  
✔️ Real-time MAVLink data streaming (AHRS, GPS, VFR HUD, etc.)  
✔️ WebSocket-based frontend for live updates  
✔️ Simulated MAVLink data for testing  

---

## 📌 Setup Instructions  

### 1️⃣ Install Dependencies  
Ensure you have Python 3.11+ and `venv` installed. Then, run:  

```bash
python -m venv myenv
source myenv/bin/activate  # macOS/Linux
myenv\Scripts\activate     # Windows

pip install flask flask-socketio pymavlink
```

---

### 2️⃣ Start the MAVLink Server  
Run the **Flask-SocketIO** server to listen for MAVLink messages:  

```bash
python server.py
```

✅ Server will be available at **http://127.0.0.1:5000**  

---

### 3️⃣ Simulate MAVLink Data  
To test without a real drone, send **fake MAVLink data** via UDP:  

```bash
python fake_mavlink.py
```

💡 This will send **AHRS2 telemetry data** every second.  

---

## 📜 Project Structure  
```
📂 MAVLink-Web-Interface
│── server.py          # Flask-SocketIO server handling MAVLink messages
│── fake_mavlink.py    # Script to send fake MAVLink data over UDP
│── templates/
│   ├── index.html     # Frontend web interface (Flask template)
│── static/
│   ├── script.js      # WebSocket client for real-time updates
│── README.md          # Project documentation
```

---

## 🔗 Related MAVLink Web Interfaces  
If you're looking for **fully-featured web-based MAVLink solutions**, check out these projects:  

- **[WebGCS](https://github.com/kiorpesc/WebGCS)** – Browser-based ground control station  
- **[Rpanion-server](https://github.com/stephendade/Rpanion-server)** – Web interface for MAVLink companion computers  
- **[mavlink2rest](https://github.com/mavlink/mavlink2rest)** – Exposes MAVLink as a REST API  
- **[APWeb](https://github.com/ArduPilot/APWeb)** – Web server interface for ArduPilot  


