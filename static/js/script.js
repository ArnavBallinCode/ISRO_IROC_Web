const socket = io.connect("http://localhost:5000");

socket.on("connect", () => {
    document.getElementById("status-dot").style.backgroundColor = "green";
    document.getElementById("status-text").textContent = "Connected";
});

socket.on("mavlink_data", (data) => {
    if (data.mavpackettype === "AHRS2" || data.mavpackettype === "AHRS3") {
        document.getElementById("roll").textContent = data.roll.toFixed(2);
        document.getElementById("pitch").textContent = data.pitch.toFixed(2);
        document.getElementById("yaw").textContent = data.yaw.toFixed(2);
    }
    if (data.mavpackettype === "VFR_HUD") {
        document.getElementById("airspeed").textContent = data.airspeed.toFixed(2);
        document.getElementById("groundspeed").textContent = data.groundspeed.toFixed(2);
        document.getElementById("heading").textContent = data.heading;
        document.getElementById("altitude").textContent = data.alt.toFixed(2);
        document.getElementById("climb").textContent = data.climb.toFixed(2);
    }
    if (data.lat !== undefined && data.lng !== undefined) {
        document.getElementById("lat").textContent = data.lat;
        document.getElementById("lng").textContent = data.lng;
    }
});
