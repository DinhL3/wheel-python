from gpiozero import RotaryEncoder
from signal import pause

# Define the pins used for the rotary encoder
encoder = RotaryEncoder(6, 5, max_steps=0)

# The encoder has 20 steps per 360-degree rotation
STEPS_PER_ROTATION = 20

def get_angle():
# Calculate and return the current angle on a 360-degree scale.
    return (encoder.steps % STEPS_PER_ROTATION) * (360 / STEPS_PER_ROTATION)

def display_value():
# Display the current value in degrees.
    angle = get_angle()
    print(f"Current Angle: {angle:.2f}°")

# Set the callback to the function to be executed when rotated
encoder.when_rotated = display_value

display_value()

pause()
