import serial
import time
from reque import HealthCheck  # Ensure the import path is correct based on your project setup


def read_enrollment_process(ser):
    labelt1 = 0  # Initialize labelt1 to 0
    print("Waiting for enrollment instructions...")
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)  # Print whatever message is received from the sensor
            if line.lower() == "put":
                labelt1 = 1
            elif line.lower() == "remove":
                labelt1 = 2
            elif line.lower() == "putsame":
                labelt1 = 3
            elif line.lower() == "stored":
                labelt1 = 4
                print("labelt1 value:", labelt1)  # Print the value of labelt1 upon "stored"
                break  # Exit the loop once the process is complete



def send_command_to_fingerprint(ser, command):
    ser.write(f"{command}\r\n".encode())
    print(f"Command sent to fingerprint sensor: {command}")


with serial.Serial('COM5', 9600, timeout=1) as finger_ser:
    print(f"Connected to fingerprint sensor on {finger_ser.name}")

    try:
        # Automatically send the 'ENROLL' command upon starting the script
        time.sleep(2)
        send_command_to_fingerprint(finger_ser, "ENROLL")
        time.sleep(1)

        # Instantiate HealthCheck to get the last ID from the mapping
        health_check = HealthCheck()
        id_mapping = health_check.getAllIDs()
        last_id = max(id_mapping.keys())  # Find the highest numerical key

        # Send the last ID number as a separate command
        send_command_to_fingerprint(finger_ser, str(last_id))
        print("Last ID sent:", last_id)

        # Read and process enrollment messages
        read_enrollment_process(finger_ser)
    except serial.SerialException as e:
        print(f"Serial port error: {e}")

