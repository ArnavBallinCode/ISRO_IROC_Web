document.addEventListener("DOMContentLoaded", () => {
    const socket = io.connect("http://localhost:5001");

    // Connection status
    const statusDot = document.getElementById("status-dot");
    const statusText = document.getElementById("status-text");

    socket.on("connect", () => {
        console.log("✅ Connected to server");
        statusDot.style.backgroundColor = "green";
        statusText.textContent = "Connected";
    });

    socket.on("disconnect", () => {
        statusDot.style.backgroundColor = "red";
        statusText.textContent = "Disconnected";
    });

    // Data handler with null checks and field mapping
    socket.on("mavlink_data", (data) => {
        console.log("Incoming data:", data);
        
        // Process all possible data fields
        const fields = [
            { id: "roll", key: "roll", suffix: "°" },
            { id: "pitch", key: "pitch", suffix: "°" },
            { id: "yaw", key: "yaw", suffix: "°" },
            { id: "altitude", key: "altitude", suffix: " m" },
            { id: "lat", key: "lat", suffix: "" },
            { id: "lng", key: "lng", suffix: "" },
            { id: "airspeed", key: "airspeed", suffix: " m/s" },
            { id: "groundspeed", key: "groundspeed", suffix: " m/s" },
            { id: "heading", key: "heading", suffix: "°" },
            { id: "climb", key: "climb", suffix: " m/s" }
        ];

        fields.forEach(field => {
            if (data[field.key] !== undefined) {
                const element = document.getElementById(field.id);
                if (element) {
                    // Special handling for GPS coordinates (more decimal places)
                    const isGps = field.id === "lat" || field.id === "lng";
                    const decimalPlaces = isGps ? 6 : 2;
                    element.textContent = data[field.key].toFixed(decimalPlaces) + field.suffix;
                }
            }
        });

        // Debug: Show raw data in console
        console.table({
            'Packet Type': data.mavpackettype,
            'Roll': data.roll?.toFixed(2),
            'Pitch': data.pitch?.toFixed(2),
            'Yaw': data.yaw?.toFixed(2),
            'Altitude': data.altitude?.toFixed(2),
            'Latitude': data.lat?.toFixed(6),
            'Longitude': data.lng?.toFixed(6),
            'Airspeed': data.airspeed?.toFixed(2),
            'Groundspeed': data.groundspeed?.toFixed(2),
            'Heading': data.heading?.toFixed(2),
            'Climb Rate': data.climb?.toFixed(2)
        });
    });
});