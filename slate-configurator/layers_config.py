MEDIA = 1
KEY = 2
STRING = 3
KEY_PRESS = 4
KEY_RELEASE = 5
CHANGE_LAYER = 6
MOUSE_CLICK = 7
MOUSE_MOVE = 8

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
                "increment": (MEDIA, 0xE9),
                "decrement": (MEDIA, 0xEA),
                "button": (MEDIA, 0xCD),
            },
            "joystick": {
                "x+": (MOUSE_MOVE, [-100, 0, 0]),
                "x-": (MOUSE_MOVE, [100, 0, 0]),
                "y+": (MOUSE_MOVE, [0, 100, 0]),
                "y-": (MOUSE_MOVE, [0, -100, 0]),
                "button": (MOUSE_CLICK, 1),
            }
        },
        {
            "name": "Slate2",
            "touch_shortcuts": [
                {
                    "label": "Yeet",
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
                    "actions": (KEY, 0x04),
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
                "increment": (MEDIA, 0xE9),
                "decrement": (MEDIA, 0xEA),
                "button": (MEDIA, 0xCD),
            },
            "joystick": {
                "x+": (MOUSE_MOVE, [-100, 0, 0]),
                "x-": (MOUSE_MOVE, [100, 0, 0]),
                "y+": (MOUSE_MOVE, [0, 100, 0]),
                "y-": (MOUSE_MOVE, [0, -100, 0]),
                "button": (MOUSE_CLICK, 1),
            }
        },
        {
            "name": "Slate3",
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
                "increment": (MEDIA, 0xE9),
                "decrement": (MEDIA, 0xEA),
                "button": (MEDIA, 0xCD),
            },
            "joystick": {
                "x+": (MOUSE_MOVE, [-100, 0, 0]),
                "x-": (MOUSE_MOVE, [100, 0, 0]),
                "y+": (MOUSE_MOVE, [0, 100, 0]),
                "y-": (MOUSE_MOVE, [0, -100, 0]),
                "button": (MOUSE_CLICK, 1),
            }
        },
    ]
}