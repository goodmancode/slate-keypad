from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode

MEDIA = 1
KEY = 2
STRING = 3
KEY_PRESS = 4
KEY_RELEASE = 5
CHANGE_LAYER = 6

slate_config = {
    "layers": [
        {
            "name": "Slate",
            "touch_shortcuts": [
                {
                    "label": "Slate Logo",
                    "icon": "icons/slate.bmp",
                    "actions": (STRING, "Slate"),
                },
                {
                    "label": "Slate Logo",
                    "icon": "icons/slate.bmp",
                    "actions": (STRING, "Slate"),
                },
                {
                    "label": "Slate Logo",
                    "icon": "icons/slate.bmp",
                    "actions": (STRING, "Slate"),
                },
                {
                    "label": "Slate Logo",
                    "icon": "icons/slate.bmp",
                    "actions": (STRING, "Slate"),
                },
                {
                    "label": "Slate Logo",
                    "icon": "icons/slate.bmp",
                    "actions": (STRING, "Slate"),
                },
                {
                    "label": "Slate Logo",
                    "icon": "icons/slate.bmp",
                    "actions": (STRING, "Slate"),
                },
                {
                    "label": "Slate Logo",
                    "icon": "icons/slate.bmp",
                    "actions": (STRING, "Slate"),
                },
                {
                    "label": "Slate Logo",
                    "icon": "icons/slate.bmp",
                    "actions": (STRING, "Slate"),
                },
                {
                    "label": "Slate Logo",
                    "icon": "icons/slate.bmp",
                    "actions": (STRING, "Slate"),
                },
                {
                    "label": "Slate Logo",
                    "icon": "icons/slate.bmp",
                    "actions": (STRING, "Slate"),
                },
                {
                    "label": "Slate Logo",
                    "icon": "icons/slate.bmp",
                    "actions": (STRING, "Slate"),
                },
                {
                    "label": "Slate Logo",
                    "icon": "icons/slate.bmp",
                    "actions": (STRING, "Slate"),
                },
            ],
            "key_shortcuts": [
                {
                    "assigned_key": 0,
                    "actions": (STRING, "Slate"),
                },
                {
                    "assigned_key": 1,
                    "actions": (STRING, "Keypad"),
                },
                {
                    "assigned_key": 2,
                    "actions": (None, None),
                },
                {
                    "assigned_key": 3,
                    "actions": (None, None),
                },
                {
                    "assigned_key": 4,
                    "actions": (None, None),
                },
                {
                    "assigned_key": 5,
                    "actions": (None, None),
                },
                {
                    "assigned_key": 6,
                    "actions": (None, None),
                },
                {
                    "assigned_key": 7,
                    "actions": (None, None),
                },
            ],
            "encoder": {
                "increment": (MEDIA, ConsumerControlCode.VOLUME_INCREMENT),
                "decrement": (MEDIA, ConsumerControlCode.VOLUME_DECREMENT),
                "button": (MEDIA, ConsumerControlCode.PLAY_PAUSE),
            },
            "joystick": {
                "button": (STRING, "Slate"),
            }
        },
        {
            "name": "Youtube Controls",
            "touch_shortcuts": [
                {
                    "label": "Play",
                    "icon": "icons/pr_play.bmp",
                    "actions": (KEY, [Keycode.K]),
                },
                {
                    "label": "Pause",
                    "icon": "icons/pr_pause.bmp",
                    "actions": (KEY, [Keycode.K]),
                },
                {
                    "label": "Rewind",
                    "icon": "icons/pr_rewind.bmp",
                    "actions": (KEY, [Keycode.LEFT_ARROW]),
                },
                {
                    "label": "FastForward",
                    "icon": "icons/pr_ffwd.bmp",
                    "actions": (KEY, [Keycode.RIGHT_ARROW]),
                },
                {
                    "label": "Previous",
                    "icon": "icons/pr_previous.bmp",
                    "actions": (KEY, [Keycode.RIGHT_SHIFT, Keycode.P]),
                },
                {
                    "label": "Next",
                    "icon": "icons/pr_next.bmp",
                    "actions": (KEY, [Keycode.RIGHT_SHIFT, Keycode.N]),
                },
                {
                    "label": "Vol -",
                    "icon": "icons/pr_voldown.bmp",
                    "actions": (MEDIA, ConsumerControlCode.VOLUME_DECREMENT),
                },
                {
                    "label": "Vol +",
                    "icon": "icons/pr_volup.bmp",
                    "actions": (MEDIA, ConsumerControlCode.VOLUME_INCREMENT),
                },
                {
                    "label": "Fullscreen",
                    "icon": "icons/pr_fullscreen.bmp",
                    "actions": (KEY, [Keycode.F]),
                },
                {
                    "label": "Slow",
                    "icon": "icons/pr_slow.bmp",
                    "actions": (KEY, [Keycode.RIGHT_SHIFT, Keycode.COMMA]),
                },
                {
                    "label": "Fast",
                    "icon": "icons/pr_fast.bmp",
                    "actions": (KEY, [Keycode.RIGHT_SHIFT, Keycode.PERIOD]),
                },
                {
                    "label": "Mute",
                    "icon": "icons/pr_mute.bmp",
                    "actions": (KEY, [Keycode.M]),
                },
            ],
        },
    ]
}