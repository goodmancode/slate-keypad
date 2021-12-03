# Slate Macro Keypad
#
# UCF Senior Design Project - Group 8
# Summer - Fall '21
#

"""
This version runs on Feather nRF52840 Express with a 3.5" FeatherWing
"""

# Enable or disable startup prints ("false" improves boot speed during reload)
startup_prints = True

# Enable or disable main loop prints ("false" improves speed during use)
main_loop_prints = True

# Enable or disable joystick position change prints
print_joystick = False

# Flag to disable all console prints (set to "True" for production, improves speed)
disable_prints = False

if disable_prints == True:
    startup_prints = False
    main_loop_prints = False
    print_joystick = False

# Enable / disable USER key to enter REPL
enable_repl_key = True

# Print starting memory
import gc
gc.collect()
if startup_prints:
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
from layers import slate_config
from adafruit_simplemath import map_range
from adafruit_hid.mouse import Mouse

MEDIA = 1
KEY = 2
STRING = 3
KEY_PRESS = 4
KEY_RELEASE = 5
CHANGE_LAYER = 6
MOUSE_CLICK = 7
MOUSE_MOVE = 8
OPEN_APP = 9

LEFT_BUTTON = 1
MIDDLE_BUTTON = 4
RIGHT_BUTTON = 2

# Garbage collect and print free memory space
gc.collect()
if startup_prints:
    print("[MemCheck] bytes free after imports:\t\t\t\t" + str(gc.mem_free()))

# Pin Assignments
KEY_PINS = (
    board.SCL,  # Key 0
    board.D11,  # Key 1
    board.D12,  # Key 2
    board.D13,  # Key 3
    board.RX, # Key 4
    board.TX,  # Key 5
    board.D2,  # Key 6
    board.SDA,  # Key 7
)
ENC_CLK = board.A0
ENC_DT = board.A1
ENC_SW = board.A2
JOY_X = board.A5
JOY_Y = board.A4
JOY_SW = board.A3
VDIV_PIN = board.VOLTAGE_MONITOR
REPL_PIN = board.SWITCH

# Set up REPL button
repl_button = digitalio.DigitalInOut(REPL_PIN)
repl_button.direction = digitalio.Direction.INPUT
repl_button.pull = digitalio.Pull.UP

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
def batteryPercentage(voltage):
    return round(map_range(voltage,3.4,4.2,0,100))

# Print battery percentage at startup
last_battery_voltage = round(get_voltage_averaged(battery), 2)
current_battery_voltage = last_battery_voltage
battery_charging = False
battery_poll_timer = 0
if startup_prints:
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

# Scales analog joystick values in range -100 to 100 (adjust to desired min/max)
def scaleJoyPosition(position):
    return (round(map_range(position[0], 300, 65000, -100, 100)), round(map_range(position[1], 300, 65000, -100, 100)))
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
    mouse = Mouse(usb_hid.devices)
    if startup_prints:
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
ble_mouse = Mouse(ble_hid.devices)

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
loading_background_tilegrid.x = -5
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
    display.width // 20, (display.height - 20) // 20, 1
)
connect_palette = displayio.Palette(1)
connect_palette[0] = 0x0

# scale connect screen background
connect_background_scale_group = displayio.Group(scale=20)
connect_background_tilegrid = displayio.TileGrid(
    connect_background, pixel_shader=connect_palette
)
connect_background_tilegrid.y = 1
connect_background_scale_group.append(connect_background_tilegrid)

# connect screen label
connect_label = bitmap_label.Label(terminalio.FONT, text="Connect to host via\nUSB or Bluetooth...", scale=3)
connect_label.anchor_point = (0.5, 0.5)
connect_label.anchored_position = (display.width // 2, display.height // 2)

# append background and label to the group
connect_group.append(connect_background_scale_group)
connect_group.append(connect_label)

# GridLayout to hold the icons
# size and location can be adjusted to fit
# different sized screens.
layout = GridLayout(
    x=14,
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

# input feedback label at top-left of screen
input_label = bitmap_label.Label(terminalio.FONT)
input_label.color = 0x00FF00
input_label.anchor_point = (0.0, 0.0)
input_label.anchored_position = (6, 4)
main_group.append(input_label)

# layer label at the top of the screen
layer_label = bitmap_label.Label(terminalio.FONT)
layer_label.anchor_point = (0.5, 0.0)
layer_label.anchored_position = (display.width // 2, 4)
main_group.append(layer_label)

# Battery indicator at the top of the screen
battery_label = bitmap_label.Label(terminalio.FONT)
battery_label.anchor_point = (1.0, 0.0)
battery_label.anchored_position = (display.width - 6, 4)
main_group.append(battery_label)

# Charging indicator
charging_group = displayio.Group()
charging_indicator = displayio.OnDiskBitmap("/icons/blanksymbol.bmp")
charging_indicator_grid = displayio.TileGrid(charging_indicator, pixel_shader=charging_indicator.pixel_shader)
charging_indicator_grid.x = display.width - 46
charging_indicator_grid.y = 6
charging_group.append(charging_indicator_grid)
main_group.append(charging_group)

# Bluetooth connection indicator
ble_group = displayio.Group()
ble_indicator = displayio.OnDiskBitmap("/icons/bluetooth.bmp")
ble_indicator_grid = displayio.TileGrid(ble_indicator, pixel_shader=ble_indicator.pixel_shader)
ble_indicator_grid.x = display.width - 63
ble_indicator_grid.y = 6
main_group.append(ble_group)

# USB connection indicator
usb_group = displayio.Group()
usb_indicator = displayio.OnDiskBitmap("/icons/usb.bmp")
usb_indicator_grid = displayio.TileGrid(usb_indicator, pixel_shader=usb_indicator.pixel_shader)
usb_indicator_grid.x = display.width - 90
usb_indicator_grid.y = 6
main_group.append(usb_group)

# right side layer buttons
next_layer_btn = IconWidget("", "icons/layer_next.bmp", on_disk=True)
next_layer_btn.x = display.width - 42
next_layer_btn.y = display.height - 100
main_group.append(next_layer_btn)

prev_layer_btn = IconWidget("", "icons/layer_prev.bmp", on_disk=True)
prev_layer_btn.x = display.width - 42
prev_layer_btn.y = 110
main_group.append(prev_layer_btn)

home_layer_btn = IconWidget("", "icons/layer_home.bmp", on_disk=True)
home_layer_btn.x = display.width - 42
home_layer_btn.y = 28
main_group.append(home_layer_btn)

def changeChargingSymbol(image_path):
    global charging_indicator_grid
    charging_indicator = displayio.OnDiskBitmap(image_path)
    charging_indicator_grid = displayio.TileGrid(charging_indicator, pixel_shader=charging_indicator.pixel_shader)
    charging_indicator_grid.x = display.width - 46
    charging_indicator_grid.y = 6
    charging_group.pop()
    charging_group.append(charging_indicator_grid)

def showBluetoothSymbol(show_bluetooth):
    global ble_indicator_grid
    global ble_group
    if show_bluetooth:
        ble_group.append(ble_indicator_grid)
    if not show_bluetooth:
        try:
            ble_group.pop()
        except IndexError:
            print("[ERROR] ble_group.pop(): ble_group already empty.")
            pass

def showUSBSymbol(show_usb):
    global usb_indicator_grid
    global usb_group
    if show_usb:
        usb_group.append(usb_indicator_grid)
    if not show_usb:
        try:
            usb_group.pop()
        except IndexError:
            print("[ERROR] usb_group.pop(): usb_group already empty.")
            pass

def isBatteryCharging():
    global last_battery_voltage
    global current_battery_voltage
    global usb_power
    # USB Host detected, charging status is guaranteed
    if supervisor.runtime.usb_connected:
        return True
    # When connecting a USB power source, the battery voltage
    # jumps ~ +0.05V, therefore charging is likely occurring (hacky)
    if current_battery_voltage - last_battery_voltage >= 0.03:
        usb_power = True
        return True
    if last_battery_voltage - current_battery_voltage >= 0.03:
        usb_power = False
        return False
    if usb_power:
        return True
    else:
        return False

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
        if main_loop_prints:
            print("[MemCheck] bytes free after popping an icon:\t\t\t" + str(gc.mem_free()))

    # set the layer labeled at the top of the screen
    layer_label.text = slate_config["layers"][layer_index]["name"]
    battery_label.text = "{}%".format(batteryPercentage(last_battery_voltage))
    # Garbage collect and print free memory space
    gc.collect()
    if main_loop_prints:
        print("[MemCheck] bytes free before loading custom icons:\t\t" + str(gc.mem_free()))
    # loop over each shortcut and it's index
    for i, shortcut in enumerate(slate_config["layers"][layer_index]["touch_shortcuts"]):
        # create an icon for the current shortcut
        _new_icon = IconWidget(shortcut["label"], shortcut["icon"], on_disk=True)
        # Garbage collect and print free memory space
        gc.collect()
        if main_loop_prints:
            print("[MemCheck] bytes free after loading icon " + str(i) + ":\t\t\t" + str(gc.mem_free()))
        # add it to the list of icons
        _icons.append(_new_icon)

        # add it to the grid layout
        # calculate it's position from the index
        layout.add_content(_new_icon, grid_position=(i % 4, i // 4), cell_size=(1, 1))

    # hide the loading screen
    time.sleep(0.05)
    main_group.pop()

def connect_screen():
    global battery_poll_timer
    global current_time
    global last_battery_voltage
    # show the connect screen
    battery_label.text = "{}%".format(batteryPercentage(last_battery_voltage))
    last_layer_name = layer_label.text
    layer_label.text = ""
    main_group.append(connect_group)
    time.sleep(0.05)
    battery_poll_timer = 0
    while not (supervisor.runtime.usb_connected or ble.connected):
        current_time = time.time()
        if (current_time - battery_poll_timer) >= 5:
            current_battery_voltage = round(get_voltage_averaged(battery), 2)
            battery_poll_timer = current_time
            if current_battery_voltage < last_battery_voltage:
                if main_loop_prints:
                    print("[System] battery voltage: " + str(current_battery_voltage))
                last_battery_voltage = current_battery_voltage
                battery_label.text = "{}%".format(batteryPercentage(last_battery_voltage))
    if supervisor.runtime.usb_connected:
        kbd = Keyboard(usb_hid.devices)
        cc = ConsumerControl(usb_hid.devices)
        kbd_layout = KeyboardLayoutUS(kbd)
        mouse = Mouse(usb_hid.devices)
        if main_loop_prints:
            print("[USB] connected and HID service started.")
    if ble.connected:
        if main_loop_prints:
            print("[Bluetooth] connected.")
    layer_label.text = last_layer_name
    current_battery_voltage = round(get_voltage_averaged(battery), 2)
    battery_poll_timer = time.time()
    main_group.pop()
    gc.collect()
    if main_loop_prints:
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
        # Mouse click
        elif _action[0] == MOUSE_CLICK:
            if bluetooth:
                ble_mouse.press(_action[1])
                ble_mouse.release(_action[1])
            else:
                mouse.press(_action[1])
                mouse.release(_action[1])
        # Mouse movement
        elif _action[0] == MOUSE_MOVE:
            if bluetooth:
                ble_mouse.move(_action[1][0], _action[1][1], _action[1][2])
            else:
                mouse.move(_action[1][0], _action[1][1], _action[1][2])
        elif _action[0] == OPEN_APP:
            if bluetooth:
                ble_kbd.press(*[Keycode.GUI, Keycode.R])
                ble_kbd.release(*[Keycode.GUI, Keycode.R])
                time.sleep(0.25)
                ble_kbd_layout.write(_action[1])
                ble_kbd.press(*[Keycode.ENTER])
                ble_kbd.release(*[Keycode.ENTER])
            else:
                kbd.press(*[Keycode.GUI, Keycode.R])
                kbd.release(*[Keycode.GUI, Keycode.R])
                time.sleep(0.1)
                kbd_layout.write(_action[1])
                kbd.press(*[Keycode.ENTER])
                kbd.release(*[Keycode.ENTER])
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
    if startup_prints:
        print("[Bluetooth] advertising.")
    ble.start_advertising(advertisement, scan_response)
    ble_advertising = True
else:
    if startup_prints:
        print("[Bluetooth] already connected.")
    print(ble.connections)
    ble_advertising = False
    showBluetoothSymbol(True)

# Garbage collect and print free memory space
gc.collect()
if startup_prints:  
    print("[MemCheck] bytes free before load_layer:\t\t\t" + str(gc.mem_free()))
# load the first layer to start
load_layer(current_layer)

battery_poll_timer = time.time()
fully_charged = False
charging_indicator_visible = False
usb_indicator_visible = False
usb_power = False

#  main loop
while True:
    # Check if REPL key pressed
    if repl_button.value == False:
        break
    # Poll battery every 5 seconds and print at every 0.01v change
    current_battery_voltage = round(get_voltage_averaged(battery), 2)
    battery_charging = isBatteryCharging()
    current_time = time.time()
    if battery_charging and not charging_indicator_visible:
        if main_loop_prints:
            print("[Status] Power connected, displaying charging indicator.")
        changeChargingSymbol("/icons/charging.bmp")
        charging_indicator_visible = True
    if not battery_charging and charging_indicator_visible:
        if main_loop_prints:
            print("[Status] Power disconnected, hiding charging indicator.")
        changeChargingSymbol("/icons/blanksymbol.bmp")
        fully_charged = False
        charging_indicator_visible = False
    if (current_time - battery_poll_timer) >= 5:
        if battery_charging:
            if last_battery_voltage >= 4.2 and fully_charged == False:
                if main_loop_prints:
                    print("[Status] Battery full, changing charging indicator to green.")
                changeChargingSymbol("/icons/charged.bmp")
                fully_charged = True
            if current_battery_voltage > last_battery_voltage:
                if main_loop_prints:
                    print("[System] Battery voltage: " + str(current_battery_voltage))
                last_battery_voltage = current_battery_voltage
                battery_label.text = "{}%".format(batteryPercentage(last_battery_voltage))
        else:
            if current_battery_voltage < last_battery_voltage:
                if main_loop_prints:
                    print("[System] Battery voltage: " + str(current_battery_voltage))
                last_battery_voltage = current_battery_voltage
                battery_label.text = "{}%".format(batteryPercentage(last_battery_voltage))
        battery_poll_timer = current_time

    # Display USB indicator if connected to USB host
    if not usb_indicator_visible and supervisor.runtime.usb_connected:
        if main_loop_prints:
            print("[Status] USB host connected, displaying USB host indicator.")
        showUSBSymbol(True)
        usb_indicator_visible = True

    if usb_indicator_visible and not supervisor.runtime.usb_connected:
        if main_loop_prints:
            print("[Status] USB host disconnected, hiding USB host indicator.")
        showUSBSymbol(False)
        usb_indicator_visible = False

    # Bluetooth
    if not ble_advertising and not ble.connected:
        if main_loop_prints:
            print("[Status] BLE host disconnected, hiding BLE host indicator.")
        showBluetoothSymbol(False)
        ble.start_advertising(advertisement, scan_response)
        ble_advertising = True
        if main_loop_prints:
            print("[Bluetooth] advertising.")
    connected_message_printed = False
    if ble.connected:
        just_connected = ble_advertising
        if just_connected:
            if main_loop_prints:
                print("[Status] BLE host connected, displaying BLE host indicator.")
            showBluetoothSymbol(True)
            if main_loop_prints:
                print("[Bluetooth] connected.")
        ble_advertising = False

    # Wait at connect screen if not connected to a Host device
    if not (supervisor.runtime.usb_connected or ble.connected):
        if main_loop_prints:
            print("[System] host device not found. Waiting on connection...")
        last_battery_voltage = connect_screen()
    

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
    
    # Physical key events and actions
    keyevent = keys.events.get()
    if keyevent:
        if main_loop_prints:
            print(keyevent)
        if keyevent.pressed and layer_uses_keys:
            # update input feedback label at top of screen
            input_label.text = "KEY " + str(keyevent.key_number)
            # get actions for this key from config object
            for key in slate_config["layers"][current_layer]["key_shortcuts"]:
                if key["assigned_key"] == keyevent.key_number:
                    _cur_actions = key["actions"]
                    break
            performActions(_cur_actions)
        if keyevent.released and layer_uses_keys:
            input_label.text = "     "

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
            if main_loop_prints:
                print("[Encoder] position: " + str(encoder_current_pos))
    # Check if encoder rotated counter-clockwise
    if encoder_change < 0:
        for _ in range(-encoder_change):
            # Perform decrement macro
            if layer_uses_encoder:
                _cur_actions = slate_config["layers"][current_layer]["encoder"].get("decrement")
                performActions(_cur_actions)
            if main_loop_prints:
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
        if main_loop_prints:
            print("[Encoder] button pressed.")
        encoder_button_state = None

    # Check if joystick position changed
    joystick_current_pos = scaleJoyPosition((joystick_x.value, joystick_y.value))
    # X position changed
    if abs(joystick_current_pos[0] - joystick_last_pos[0]) > 5:
        if print_joystick: print("[Joystick] position: " + str(joystick_current_pos))
        # Only implmentation currently is for discrete movement, not analog
        # X-
        if joystick_current_pos[0] > 95 and layer_uses_joystick:
            _cur_actions = slate_config["layers"][current_layer]["joystick"].get("x-")
            performActions(_cur_actions)
        # X+
        if joystick_current_pos[0] < -95 and layer_uses_joystick:
            _cur_actions = slate_config["layers"][current_layer]["joystick"].get("x+")
            performActions(_cur_actions)
        joystick_last_pos = joystick_current_pos
    # Y position changed
    if abs(joystick_current_pos[1] - joystick_last_pos[1]) > 5:
        if print_joystick: print("[Joystick] position: " + str(joystick_current_pos))
        # Only implmentation currently is for discrete movement, not analog
        # Y-
        if joystick_current_pos[1] > 95 and layer_uses_joystick:
            _cur_actions = slate_config["layers"][current_layer]["joystick"].get("y-")
            performActions(_cur_actions)
        # Y+
        if joystick_current_pos[1] < -95 and layer_uses_joystick:
            _cur_actions = slate_config["layers"][current_layer]["joystick"].get("y+")
            performActions(_cur_actions)
        joystick_last_pos = joystick_current_pos
    # Check if joystick button pressed
    if not joystick_button.value and joystick_button_state is None:
        joystick_button_state = "pressed"
    if joystick_button.value and joystick_button_state == "pressed":
        # Perform joystick button macro
        _cur_actions = slate_config["layers"][current_layer]["joystick"].get("button")
        performActions(_cur_actions)
        if print_joystick: print("[Joystick] button pressed.")
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
                                input_label.text = "SCREENKEY " + str(index + 1)
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
                                input_label.text = "            "
    else:  # screen not touched

        # empty the pressed icons list
        _pressed_icons.clear()
