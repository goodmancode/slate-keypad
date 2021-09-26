# A collection of helper functions
from adafruit_simplemath import map_range

# Scales analog joystick values in range -100 to 100 (adjust to desired min/max)
def scaleJoyPosition(position):
    return (round(map_range(position[0], 300, 65000, -100, 100)), round(map_range(position[1], 300, 65000, -100, 100)))