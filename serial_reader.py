import serial
import requests
import time

ser = serial.Serial("COM3", 9600, timeout=1)
time.sleep(2)  # Allow time for the connection to stabilize

latest_data = {"heart_rate": None, "blood_oxygen": None, "dog_id": None}

DOG_ID = 7 # Change this for different Arduinos

while True:
    if ser.in_waiting > 0:
        try:
            line = ser.readline().decode('utf-8').strip()
            key, value = line.split(",")

            if key == "HR":
                latest_data["heart_rate"] = int(value)
            elif key == "O2":
                latest_data["blood_oxygen"] = int(value)

            # Assign the hardcoded dog_id
            latest_data["dog_id"] = DOG_ID  

            # Send data when both HR & O2 are available
            if latest_data["heart_rate"] is not None and latest_data["blood_oxygen"] is not None:
                response = requests.post("http://127.0.0.1:5000/update_health", json=latest_data)
                print("Sent:", latest_data, "Response:", response.status_code)

                latest_data = {"heart_rate": None, "blood_oxygen": None, "dog_id": DOG_ID}  # Reset only HR & O2

        except Exception as e:
            print("Error:", e)

    time.sleep(1)

