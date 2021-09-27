# Slate Macro Keypad
#
# UCF Senior Design Project - Group 8
# Summer - Fall '21
#

"""
This version runs on Feather nRF52840 Express with a 3.5" FeatherWing
"""
# Print starting memory
import gc
gc.collect()
print("[MemCheck] bytes free before imports:\t\t\t\t" + str(gc.mem_free()))

# Imports
import time
import supervisor
import displayio
import terminalio
import rotaryio
import digitalio
import analogio
import board
import keypad
import adafruit_ble
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_display_text import bitmap_label
from adafruit_displayio_layout.layouts.grid_layout import GridLayout
from adafruit_displayio_layout.widgets.icon_widget import IconWidget
from adafruit_featherwing import tft_featherwing_35
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.keycode import Keycode
from layers import (
    slate_config,
    KEY,
    STRING,
    MEDIA,
    KEY_PRESS,
    KEY_RELEASE,
    CHANGE_LAYER,
)
from helpers import *
from adafruit_simplemath import map_range

# Garbage collect and print free memory space
gc.collect()
print("[MemCheck] bytes free after imports:\t\t\t\t" + str(gc.mem_free()))

# Pin Assignments
KEY_PINS = (
    board.D13,  # Key 0
    board.D12,  # Key 1
    #board.PIN_NUM  # Key 2
    #board.PIN_NUM  # Key 3
    #board.PIN_NUM  # Key 4
    #board.PIN_NUM  # Key 5
    #board.PIN_NUM  # Key 6
    #board.PIN_NUM  # Key 7
)
ENC_CLK = board.A1
ENC_DT = board.A2
ENC_SW = board.A3
JOY_X = board.A4
JOY_Y = board.A5
JOY_SW = board.RX
VDIV_PIN = board.VOLTAGE_MONITOR
REPL = board.SWITCH

# User switch to stop code execution
repl = digitalio.DigitalInOut(REPL)
repl.switch_to_input(pull=digitalio.Pull.UP)

# Scales battery voltage values in range 0-100
battery = analogio.AnalogIn(VDIV_PIN)
def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2
def get_voltage_averaged(pin):
    averaged = 0
    for i in range(0,50):
        averaged += get_voltage(pin)
    averaged /= 50
    return averaged
def batteryPercentage():
    return round(map_range(get_voltage(battery),3.4,4.2,0,100))

# Print battery percentage at startup
last_battery_voltage = round(get_voltage_averaged(battery), 2)
current_battery_voltage = last_battery_voltage
battery_charging = supervisor.runtime.usb_connected
current_time = time.time()
battery_poll_timer = 0
print("[System] battery voltage: "+ str(last_battery_voltage))

# Physical keys setup
keys = keypad.Keys(KEY_PINS, value_when_pressed=False, pull=True)

# Rotary encoder setup
encoder = rotaryio.IncrementalEncoder(ENC_CLK, ENC_DT)
encoder_last_pos = encoder.position
encoder_button = digitalio.DigitalInOut(ENC_SW)
encoder_button.direction = digitalio.Direction.INPUT
encoder_button.pull = digitalio.Pull.UP
encoder_button_state = None

# Joystick setup
joystick_x = analogio.AnalogIn(JOY_X)
joystick_y = analogio.AnalogIn(JOY_Y)
joystick_last_pos = scaleJoyPosition((joystick_x.value, joystick_y.value))
joystick_button = digitalio.DigitalInOut(JOY_SW)
joystick_button.direction = digitalio.Direction.INPUT
joystick_button.pull = digitalio.Pull.UP
joystick_button_state = None

# USB HID setup
if supervisor.runtime.usb_connected:
    kbd = Keyboard(usb_hid.devices)
    cc = ConsumerControl(usb_hid.devices)
    kbd_layout = KeyboardLayoutUS(kbd)
    print("[USB] connected and HID service started.")

# Bluetooth HID setup
ble_hid = HIDService()
device_info = DeviceInfoService(software_revision=adafruit_ble.__version__,
                                manufacturer="Adafruit Industries")
advertisement = ProvideServicesAdvertisement(ble_hid)
advertisement.appearance = 961
scan_response = Advertisement()
scan_response.complete_name = "CircuitPython HID"
ble = adafruit_ble.BLERadio()
ble_kbd = Keyboard(ble_hid.devices)
ble_kbd_layout = KeyboardLayoutUS(ble_kbd)
ble_cc = ConsumerControl(ble_hid.devices)

# display and touchscreen initialization
displayio.release_displays()
tft_featherwing = tft_featherwing_35.TFTFeatherWing35()
display = tft_featherwing.display
touchscreen = tft_featherwing.touchscreen

# variables to enforce timout between icon presses
COOLDOWN_TIME = 0.5
LAST_PRESS_TIME = -1

# 'mock' icon indexes for the layer buttons
# used for debouncing
PREV_LAYER_INDEX = -1
NEXT_LAYER_INDEX = -2
HOME_LAYER_INDEX = -3

# start on first layer
current_layer = 0

# Make the main_group to hold everything
main_group = displayio.Group()
display.show(main_group)

# loading screen
loading_group = displayio.Group()

# black background, screen size minus side buttons
loading_background = displayio.Bitmap(
    (display.width) // 10, (display.height // 10), 1
)
loading_palette = displayio.Palette(1)
loading_palette[0] = 0x0

# scaled group to match screen size minus side buttons
loading_background_scale_group = displayio.Group(scale=10)
loading_background_tilegrid = displayio.TileGrid(
    loading_background, pixel_shader=loading_palette
)
loading_background_tilegrid.x = -4
loading_background_tilegrid.y = 2
loading_background_scale_group.append(loading_background_tilegrid)

# loading screen label
loading_label = bitmap_label.Label(terminalio.FONT, text="Loading...", scale=3)
loading_label.anchor_point = (0.5, 0.5)
loading_label.anchored_position = (display.width // 2, display.height // 2)

# append background and label to the group
loading_group.append(loading_background_scale_group)
loading_group.append(loading_label)

# Connect to host screen
connect_group = displayio.Group()

# black background, screen size minus side buttons
connect_background = displayio.Bitmap(
    display.width // 20, display.height // 20, 1
)
connect_palette = displayio.Palette(1)
connect_palette[0] = 0x0

# scale connect screen background
connect_background_scale_group = displayio.Group(scale=20)
connect_background_tilegrid = displayio.TileGrid(
    connect_background, pixel_shader=connect_palette
)
connect_background_scale_group.append(connect_background_tilegrid)

# connect screen label
connect_label = bitmap_label.Label(terminalio.FONT, text="Connect to host via\nUSB or Bluetooth...", scale=3)
connect_label.anchor_point = (0.5, 0.5)
connect_label.anchored_position = (display.width // 2, display.height // 2)

# Battery indicator at the top of the screen (connect screen)
battery_label_connect = bitmap_label.Label(terminalio.FONT)
battery_label_connect.anchor_point = (1.0, 0.0)
battery_label_connect.anchored_position = (display.width - 60, 4)

# append background and label to the group
connect_group.append(connect_background_scale_group)
connect_group.append(battery_label_connect)
connect_group.append(connect_label)

# GridLayout to hold the icons
# size and location can be adjusted to fit
# different sized screens.
layout = GridLayout(
    x=20,
    y=20,
    width=420,
    height=290,
    grid_size=(4, 3),
    cell_padding=6,
)

# list that holds the IconWidget objects for each icon.
_icons = []

# list that holds indexes of currently pressed icons and layer buttons
# used for debouncing
_pressed_icons = []

# layer label at the top of the screen
layer_label = bitmap_label.Label(terminalio.FONT)
layer_label.anchor_point = (0.5, 0.0)
layer_label.anchored_position = (display.width // 2, 4)
main_group.append(layer_label)

# Battery indicator at the top of the screen
battery_label = bitmap_label.Label(terminalio.FONT)
battery_label.anchor_point = (1.0, 0.0)
battery_label.anchored_position = (display.width - 60, 4)
main_group.append(battery_label)

# Charging indicator
charging_indicator = displayio.OnDiskBitmap("/icons/blanksymbol.bmp")
charging_indicator_grid = displayio.TileGrid(charging_indicator, pixel_shader=charging_indicator.pixel_shader)
charging_indicator_grid.x = display.width - 108
charging_indicator_grid.y = 6
main_group.append(charging_indicator_grid)

# Bluetooth connection indicator
ble_indicator = displayio.OnDiskBitmap("/icons/blanksymbol.bmp")
ble_indicator_grid = displayio.TileGrid(ble_indicator, pixel_shader=ble_indicator.pixel_shader)
ble_indicator_grid.x = display.width - 125
ble_indicator_grid.y = 6
main_group.append(ble_indicator_grid)

# right side layer buttons
next_layer_btn = IconWidget("", "icons/layer_next.bmp", on_disk=True)
next_layer_btn.x = display.width - 40
next_layer_btn.y = display.height - 100
next_layer_btn.resize = (40, 100)
main_group.append(next_layer_btn)

prev_layer_btn = IconWidget("", "icons/layer_prev.bmp", on_disk=True)
prev_layer_btn.x = display.width - 40
prev_layer_btn.y = 110
prev_layer_btn.resize = (40, 100)
main_group.append(prev_layer_btn)

home_layer_btn = IconWidget("", "icons/layer_home.bmp", on_disk=True)
home_layer_btn.x = display.width - 40
home_layer_btn.y = 0
home_layer_btn.resize = (40, 100)
main_group.append(home_layer_btn)

def changeChargingSymbol(image_path, layer):
    try:
        main_group.remove(layer)
    except ValueError:
        print("passing on ValueError")
        pass
    charging_indicator = displayio.OnDiskBitmap(image_path)
    charging_indicator_grid = displayio.TileGrid(charging_indicator, pixel_shader=charging_indicator.pixel_shader)
    charging_indicator_grid.x = display.width - 108
    charging_indicator_grid.y = 6
    main_group.append(charging_indicator_grid)

def changeBluetoothSymbol(image_path, layer):
    try:
        main_group.remove(layer)
    except ValueError:
        print("passing on ValueError")
        pass
    ble_indicator = displayio.OnDiskBitmap(image_path)
    ble_indicator_grid = displayio.TileGrid(ble_indicator, pixel_shader=ble_indicator.pixel_shader)
    ble_indicator_grid.x = display.width - 125
    ble_indicator_grid.y = 6
    main_group.append(ble_indicator_grid)

# helper method to load icons for an index by its index in the
# list of layers
def load_layer(layer_index):
    # show the loading screen
    main_group.append(loading_group)
    time.sleep(0.05)

    # resets icon lists to empty
    global _icons
    _icons = []
    layout._cell_content_list = []

    # remove previous layer icons from the layout
    while len(layout) > 0:
        layout.pop()
        gc.collect()
        print("[MemCheck] bytes free after popping an icon:\t\t\t" + str(gc.mem_free()))

    # set the layer labeled at the top of the screen
    layer_label.text = slate_config["layers"][layer_index]["name"]
    battery_label.text = "{:.2f}v".format(last_battery_voltage)
    # Garbage collect and print free memory space
    gc.collect()
    print("[MemCheck] bytes free before loading custom icons:\t\t" + str(gc.mem_free()))
    # loop over each shortcut and it's index
    for i, shortcut in enumerate(slate_config["layers"][layer_index]["touch_shortcuts"]):
        # create an icon for the current shortcut
        _new_icon = IconWidget(shortcut["label"], shortcut["icon"], on_disk=True)
        # Garbage collect and print free memory space
        gc.collect()
        print("[MemCheck] bytes free after loading icon " + str(i) + ":\t\t\t" + str(gc.mem_free()))
        # add it to the list of icons
        _icons.append(_new_icon)

        # add it to the grid layout
        # calculate it's position from the index
        layout.add_content(_new_icon, grid_position=(i % 4, i // 4), cell_size=(1, 1))

    # hide the loading screen
    time.sleep(0.05)
    main_group.pop()

def connect_screen(last_battery_voltage):
    # show the connect screen
    battery_label_connect.text = "{:.2f}v".format(last_battery_voltage)
    main_group.append(connect_group)
    time.sleep(0.05)
    battery_poll_timer = 0
    while not (supervisor.runtime.usb_connected or ble.connected):
        current_time = time.time()
        if (current_time - battery_poll_timer) >= 5:
            current_battery_voltage = round(get_voltage_averaged(battery), 2)
            if current_battery_voltage < last_battery_voltage:
                print("[System] battery voltage: " + str(current_battery_voltage))
                last_battery_voltage = current_battery_voltage
                battery_label_connect.text = "{:.2f}v".format(last_battery_voltage)
            battery_poll_timer = current_time
    if supervisor.runtime.usb_connected:
        kbd = Keyboard(usb_hid.devices)
        cc = ConsumerControl(usb_hid.devices)
        kbd_layout = KeyboardLayoutUS(kbd)
        print("[USB] connected and HID service started.")
    if ble.connected:
        print("[Bluetooth] connected.")
    battery_poll_timer = time.time()
    main_group.pop()
    gc.collect()
    print("[MemCheck] bytes free before loading after host connected:\t\t" + str(gc.mem_free()))
    return last_battery_voltage

def performActions(_cur_actions):
    # Check whether to send over Bluetooth
    bluetooth = False
    if ble.connected:
        bluetooth = True
    # tuple means it's a single action
    if isinstance(_cur_actions, tuple):
        # put it in a list by itself
        _cur_actions = [_cur_actions]
    # loop over the actions
    for _action in _cur_actions:
        # HID keyboard keys
        if _action[0] == KEY:
            if bluetooth:
                ble_kbd.press(*_action[1])
                ble_kbd.release(*_action[1])
            else:
                kbd.press(*_action[1])
                kbd.release(*_action[1])
        # String to write from layout
        elif _action[0] == STRING:
            if bluetooth:
                ble_kbd_layout.write(_action[1])
            else:
                kbd_layout.write(_action[1])
        # Consumer control code
        elif _action[0] == MEDIA:
            if bluetooth:
                ble_cc.send(_action[1])
            else:
                cc.send(_action[1])
        # Key press
        elif _action[0] == KEY_PRESS:
            if bluetooth:
                ble_kbd.press(*_action[1])
            else:
                kbd.press(*_action[1])
        # Key release
        elif _action[0] == KEY_RELEASE:
            if bluetooth:
                ble_kbd.release(*_action[1])
            else:
                kbd.release(*_action[1])
        # Change Layer
        elif _action[0] == CHANGE_LAYER:
            if isinstance(
                _action[1], int
            ) and 0 <= _action[1] < len(
                slate_config["layers"]
            ):
                current_layer = _action[1]
                load_layer(_action[1])
        # if there are multiple actions
        if len(_cur_actions) > 1:
            # small sleep to make sure
            # OS can respond to previous action
            time.sleep(0.2)

# append the grid layout to the main_group
# so it gets shown on the display
main_group.append(layout)

# check existing Bluetooth connection
if not ble.connected:
    print("[Bluetooth] advertising.")
    ble.start_advertising(advertisement, scan_response)
    ble_advertising = True
else:
    print("[Bluetooth] already connected.")
    print(ble.connections)
    ble_advertising = False
    changeBluetoothSymbol("/icons/bluetooth.bmp", ble_indicator_grid)

# Garbage collect and print free memory space
gc.collect()
print("[MemCheck] bytes free before load_layer:\t\t\t" + str(gc.mem_free()))
# load the first layer to start
load_layer(current_layer)

battery_poll_timer = time.time()
fully_charged = False
charging_indicator_visible = False

#  main loop
while True:
     # DEBUGGING - User switch will stop code if pressed
    if not repl.value:
        print("Stopping code execution...")
        break
    # Poll battery every 10 seconds and print at every 0.01v change
    current_battery_voltage = round(get_voltage_averaged(battery), 2)
    battery_charging = supervisor.runtime.usb_connected
    current_time = time.time()
    if battery_charging and not charging_indicator_visible:
        print("Changing symbol to charging")
        changeChargingSymbol("/icons/charging.bmp", charging_indicator_grid)
        charging_indicator_visible = True
    if not battery_charging and charging_indicator_visible:
        ("Changing symbol to nothing")
        changeChargingSymbol("/icons/blanksymbol.bmp", charging_indicator_grid)
        fully_charged = False
        charging_indicator_visible = False
    if (current_time - battery_poll_timer) >= 5:
        if battery_charging:
            if last_battery_voltage >= 4.2 and fully_charged == False:
                print("attempting to turn indicator green")
                changeChargingSymbol("/icons/charged.bmp", charging_indicator_grid)
                fully_charged = True
            if current_battery_voltage > last_battery_voltage:
                print("[System] battery voltage: " + str(current_battery_voltage))
                last_battery_voltage = current_battery_voltage
                battery_label.text = "{:.2f}v".format(last_battery_voltage)
        else:
            if current_battery_voltage < last_battery_voltage:
                print("[System] battery voltage: " + str(current_battery_voltage))
                last_battery_voltage = current_battery_voltage
                battery_label.text = "{:.2f}v".format(last_battery_voltage)
        battery_poll_timer = current_time

    # Wait at connect screen if not connected to a Host device
    if not (supervisor.runtime.usb_connected or ble.connected):
        print("[System] host device not found. Waiting on connection...")
        last_battery_voltage = connect_screen(last_battery_voltage)

    # Determine if layer uses input types
    layer_uses_keys = False
    layer_uses_encoder = False
    layer_uses_joystick = False
    if "key_shortcuts" in slate_config["layers"][current_layer]:
        layer_uses_keys = True
    if "encoder" in slate_config["layers"][current_layer]:
        layer_uses_encoder = True
    if "joystick" in slate_config["layers"][current_layer]:
        layer_uses_joystick = True

    # Bluetooth
    if not ble_advertising and not ble.connected:
        ble.start_advertising(advertisement)
        ble_advertising = True
        changeBluetoothSymbol("/icons/blanksymbol.bmp", ble_indicator_grid)
        print("[Bluetooth] advertising.")
    connected_message_printed = False
    if ble.connected:
        just_connected = ble_advertising
        if just_connected:
            changeBluetoothSymbol("/icons/bluetooth.bmp", ble_indicator_grid)
            print("[Bluetooth] connected.")
        ble_advertising = False
    
    # Physical key events and actions
    keyevent = keys.events.get()
    if keyevent:
        print(keyevent)
        if keyevent.pressed and layer_uses_keys:
            # get actions for this key from config object
            for key in slate_config["layers"][current_layer]["key_shortcuts"]:
                if key["assigned_key"] == keyevent.key_number:
                    _cur_actions = key["actions"]
                    break
            performActions(_cur_actions)

    # Rotary encoder events and actions
    encoder_current_pos = encoder.position
    encoder_change = encoder_current_pos - encoder_last_pos
    # Check if encoder rotated clockwise
    if encoder_change > 0:
        for _ in range(encoder_change):
            # Perform increment macro
            if layer_uses_encoder:
                _cur_actions = slate_config["layers"][current_layer]["encoder"].get("increment")
                performActions(_cur_actions)
            print("[Encoder] position: " + str(encoder_current_pos))
    # Check if encoder rotated counter-clockwise
    if encoder_change < 0:
        for _ in range(-encoder_change):
            # Perform decrement macro
            if layer_uses_encoder:
                _cur_actions = slate_config["layers"][current_layer]["encoder"].get("decrement")
                performActions(_cur_actions)
            print("[Encoder] position: " + str(encoder_current_pos))
    encoder_last_pos = encoder_current_pos
    # Check if encoder button pressed
    if not encoder_button.value and encoder_button_state is None:
        encoder_button_state = "pressed"
    if encoder_button.value and encoder_button_state == "pressed":
        # Perform encoder button macro
        if layer_uses_encoder:
            _cur_actions = slate_config["layers"][current_layer]["encoder"]["button"]
            performActions(_cur_actions)
        print("[Encoder] button pressed.")
        encoder_button_state = None

    # Check if joystick position changed
    joystick_current_pos = scaleJoyPosition((joystick_x.value, joystick_y.value))
    # X position changed
    if abs(joystick_current_pos[0] - joystick_last_pos[0]) > 5:
        print("[Joystick] position: " + str(joystick_current_pos))
        joystick_last_pos = joystick_current_pos
    # Y position changed
    if abs(joystick_current_pos[1] - joystick_last_pos[1]) > 5:
        print("[Joystick] position: " + str(joystick_current_pos))
        joystick_last_pos = joystick_current_pos
    # Check if joystick button pressed
    if not joystick_button.value and joystick_button_state is None:
        joystick_button_state = "pressed"
    if joystick_button.value and joystick_button_state == "pressed":
        # Perform joystick button macro
        _cur_actions = slate_config["layers"][current_layer]["joystick"].get("button")
        performActions(_cur_actions)
        print("[Joystick] button pressed.")
        joystick_button_state = None

    # Touchscreen events and actions
    if touchscreen.touched:
        # loop over all data in touchscreen buffer
        while not touchscreen.buffer_empty:
            touches = touchscreen.touches
            # loop over all points touched
            for point in touches:
                if point:
                    # current time, used for timeout between icon presses
                    _now = time.monotonic()

                    # if the timeout has passed
                    if _now - LAST_PRESS_TIME > COOLDOWN_TIME:
                        # print(point)

                        # map the observed minimum and maximum touch values
                        # to the screen size
                        y = point["y"] - 250
                        x = 4096 - point["x"] - 250
                        y = y * display.width // (3820 - 250)
                        x = x * display.height // (3820 - 250)

                        # touch data is 90 degrees rotated
                        # flip x, and y here to account for that
                        p = (y, x)
                        # print(p)

                        # Next layer button pressed
                        if (
                            next_layer_btn.contains(p)
                            and NEXT_LAYER_INDEX not in _pressed_icons
                        ):

                            # increment layer
                            current_layer += 1
                            # wrap back to beginning from end
                            if current_layer >= len(slate_config["layers"]):
                                current_layer = 0
                            # load the new layer
                            load_layer(current_layer)

                            # save current time to check for timeout
                            LAST_PRESS_TIME = _now

                            # append this index to pressed icons for debouncing
                            _pressed_icons.append(NEXT_LAYER_INDEX)

                        # home layer button pressed
                        if (
                            home_layer_btn.contains(p)
                            and HOME_LAYER_INDEX not in _pressed_icons
                        ):
                            # 0 index is home layer
                            current_layer = 0
                            # load the home layer
                            load_layer(current_layer)

                            # save current time to check for timeout
                            LAST_PRESS_TIME = _now

                            # append this index to pressed icons for debouncing
                            _pressed_icons.append(HOME_LAYER_INDEX)

                        # Previous layer button pressed
                        if (
                            prev_layer_btn.contains(p)
                            and PREV_LAYER_INDEX not in _pressed_icons
                        ):

                            # decrement layer
                            current_layer -= 1
                            # wrap back to end from beginning
                            if current_layer < 0:
                                current_layer = len(slate_config["layers"]) - 1

                            # load the new layer
                            load_layer(current_layer)

                            # save current time to check for timeout
                            LAST_PRESS_TIME = _now

                            # append this index to pressed icons for debouncing
                            _pressed_icons.append(PREV_LAYER_INDEX)

                        # loop over current layer icons and their indexes
                        for index, icon_shortcut in enumerate(_icons):
                            # if this icon was pressed
                            if icon_shortcut.contains(p):
                                # debounce logic, check that it wasn't already pressed
                                if index not in _pressed_icons:
                                    # print("pressed {}".format(index))

                                    # get actions for this icon from config object
                                    _cur_actions = slate_config["layers"][
                                        current_layer
                                    ]["touch_shortcuts"][index]["actions"]

                                    performActions(_cur_actions)

                                    # save current time to check for timeout
                                    LAST_PRESS_TIME = _now
                                    # append this index to pressed icons for debouncing
                                    _pressed_icons.append(index)
    else:  # screen not touched

        # empty the pressed icons list
        _pressed_icons.clear()
