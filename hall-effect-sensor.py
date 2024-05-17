from gpiozero import Button
from signal import pause
import time
import datetime

def sensor_callback():
    # Called if sensor output changes
    timestamp = time.time()
    stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
    if sensor.is_pressed:
        # Magnet
        print("Sensor LOW " + stamp)
    else:
        # No magnet
        print("Sensor HIGH " + stamp)

# Set up the Hall effect sensor on GPIO pin 17
sensor = Button(5, pull_up=True)
sensor.when_pressed = sensor_callback
sensor.when_released = sensor_callback

def main():
    try:
        # Initial sensor check
        sensor_callback()

        # Use pause to handle the asynchronous event detection
        pause()
    except KeyboardInterrupt:
        print("Program stopped by User")

if __name__=="__main__":
    main()
