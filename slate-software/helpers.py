# A collection of helper functions

# Simulates arduino map() function
def scale(value, fromLow, fromHigh, toLow, toHigh):
    return (((value - fromLow) * (toHigh - toLow)) / (fromHigh - fromLow)) + toLow

# Scales analog joystick values in range -100 to 100 (adjust to desired min/max)
def scaleJoyPosition(position):
    return (round(scale(position[0], 300, 65000, -100, 100)), round(scale(position[1], 300, 65000, -100, 100)))