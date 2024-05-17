import serial
import threading

def read_from_serial(ser):
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print("Arduino:", line)

def write_to_serial(ser):
    while True:
        user_input = input("Enter a message to send: ")
        ser.write((user_input + '\n').encode('utf-8'))
        print("Sent:", user_input)

# Initialize the serial connection
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()

# Create and start threads for reading and writing
read_thread = threading.Thread(target=read_from_serial, args=(ser,))
write_thread = threading.Thread(target=write_to_serial, args=(ser,))

read_thread.start()
write_thread.start()

# Keep the main thread running
read_thread.join()
write_thread.join()
