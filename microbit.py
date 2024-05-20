import serial
import time

# Open serial port (adjust the port as necessary, usually it is /dev/ttyACM0 or /dev/ttyUSB0)
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

# Open a log file to write the compass values
with open('microbit-log.txt', 'w') as log_file:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            log_file.write(f"{time.time()},{line}\n")
            log_file.flush()
        time.sleep(0.5)
