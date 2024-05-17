import serial
import threading
import time

def read_from_serial(ser):
    system_ready = False  # Flag to check if system is ready
    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                if "System ready" in line:
                    print("Arduino:", line)
                    system_ready = True  # Set the flag when "System ready" is received
                elif system_ready:
                    # Only print other messages after the system is ready
                    print("Arduino:", line)
    except KeyboardInterrupt:
        print("Exiting program.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        ser.close()

# Initialize the serial connection
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()

# Create and start thread for reading
read_thread = threading.Thread(target=read_from_serial, args=(ser,))
read_thread.start()

# Keep the main thread running and handle a graceful exit
try:
    while read_thread.is_alive():
        read_thread.join(1)
except KeyboardInterrupt:
    print("Program interrupted by user.")
