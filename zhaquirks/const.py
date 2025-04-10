"""Common constants for zhaquirks."""

from zigpy.quirks import (
    SIG_ENDPOINTS,
    SIG_EP_INPUT,
    SIG_EP_OUTPUT,
    SIG_EP_PROFILE,
    SIG_EP_TYPE,
    SIG_MANUFACTURER,
    SIG_MODEL,
    SIG_MODELS_INFO,
    SIG_NODE_DESC,
    SIG_SKIP_CONFIG,
)
import zigpy.types as t

ARGS = "args"
ATTR_ID = "attr_id"
ATTRIBUTE_ID = "attribute_id"
ATTRIBUTE_NAME = "attribute_name"
BUTTON = "button"
BUTTON_1 = "button_1"
BUTTON_2 = "button_2"
BUTTON_3 = "button_3"
BUTTON_4 = "button_4"
BUTTON_5 = "button_5"
BUTTON_6 = "button_6"
CLICK_TYPE = "click_type"
CLOSE = "close"
CLUSTER_COMMAND = "cluster_command"
CLUSTER_ID = "cluster_id"
COMMAND = "command"
COMMAND_ATTRIBUTE_UPDATED = "attribute_updated"
COMMAND_BUTTON_DOUBLE = "button_double"
COMMAND_BUTTON_HOLD = "button_hold"
COMMAND_BUTTON_SINGLE = "button_single"
COMMAND_CLICK = "click"
COMMAND_DOUBLE = "double"
COMMAND_FURIOUS = "furious"
COMMAND_HOLD = "hold"
COMMAND_ID = "command_id"
COMMAND_M_INITIAL_PRESS = "initial_press"
COMMAND_M_LONG_PRESS = "long_press"
COMMAND_M_LONG_RELEASE = "long_release"
COMMAND_M_MULTI_PRESS_COMPLETE = "multi_press_complete"
COMMAND_M_MULTI_PRESS_ONGOING = "multi_press_ongoing"
COMMAND_M_SHORT_RELEASE = "short_release"
COMMAND_M_SWLATCHED = "switch_latched"
COMMAND_MOVE = "move"
COMMAND_MOVE_COLOR_TEMP = "move_color_temp"
COMMAND_MOVE_ON_OFF = "move_with_on_off"
COMMAND_MOVE_SATURATION = "move_saturation"
COMMAND_MOVE_TO_SATURATION = "move_to_saturation"
COMMAND_MOVE_TO_LEVEL_ON_OFF = "move_to_level_with_on_off"
COMMAND_OFF = "off"
COMMAND_OFF_WITH_EFFECT = "off_with_effect"
COMMAND_ON = "on"
COMMAND_PRESS = "press"
COMMAND_QUAD = "quadruple"
COMMAND_RECALL = "recall"
COMMAND_RELEASE = "release"
COMMAND_SHAKE = "shake"
COMMAND_SINGLE = "single"
COMMAND_STEP = "step"
COMMAND_STEP_COLOR_TEMP = "step_color_temp"
COMMAND_STEP_HUE = "step_hue"
COMMAND_STEP_ON_OFF = "step_with_on_off"
COMMAND_STEP_SATURATION = "step_saturation"
COMMAND_STOP = "stop"
COMMAND_STOP_MOVE_STEP = "stop_move_step"
COMMAND_STOP_ON_OFF = "stop_with_on_off"
COMMAND_STORE = "store"
COMMAND_TILT = "Tilt"
COMMAND_TOGGLE = "toggle"
COMMAND_TRIPLE = "triple"
DESCRIPTION = "description"
DEVICE_TYPE = SIG_EP_TYPE
DIM_DOWN = "dim_down"
DIM_UP = "dim_up"
DOUBLE_PRESS = "remote_button_double_press"
ALT_DOUBLE_PRESS = "remote_button_alt_double_press"
ENDPOINT_ID = "endpoint_id"
ENDPOINTS = SIG_ENDPOINTS
INPUT_CLUSTERS = SIG_EP_INPUT
LEFT = "left"
LONG_PRESS = "remote_button_long_press"
LONG_RELEASE = "remote_button_long_release"
ALT_LONG_PRESS = "remote_button_alt_long_press"
ALT_LONG_RELEASE = "remote_button_alt_long_release"
MANUFACTURER = SIG_MANUFACTURER
MODEL = SIG_MODEL
MODELS_INFO = SIG_MODELS_INFO
MOTION_EVENT = "motion_event"
NODE_DESCRIPTOR = SIG_NODE_DESC
OCCUPANCY_EVENT = "occupancy_event"
OCCUPANCY_STATE = 0
OFF = 0
ON = 1
OPEN = "open"
OUTPUT_CLUSTERS = SIG_EP_OUTPUT
PARAMS = "params"
PRESS_TYPE = "press_type"
PRESSED = "initial_switch_press"
PROFILE_ID = SIG_EP_PROFILE
QUADRUPLE_PRESS = "remote_button_quadruple_press"
QUINTUPLE_PRESS = "remote_button_quintuple_press"
RELATIVE_DEGREES = "relative_degrees"
RIGHT = "right"
ROTATED = "device_rotated"
ROTATED_FAST = "device_rotated_fast"
ROTATED_SLOW = "device_rotated_slow"
STOP = "stop"
SHAKEN = "device_shaken"
SHORT_PRESS = "remote_button_short_press"
ALT_SHORT_PRESS = "remote_button_alt_short_press"
SKIP_CONFIGURATION = SIG_SKIP_CONFIG
SHORT_RELEASE = "remote_button_short_release"
TOGGLE = "toggle"
TRIPLE_PRESS = "remote_button_triple_press"
TURN_OFF = "turn_off"
TURN_ON = "turn_on"
UNKNOWN = "Unknown"
VALUE = "value"
ZHA_SEND_EVENT = "zha_send_event"
ZONE_STATUS_CHANGE_COMMAND = 0x0000
ZONE_STATE = 0x0000
ZONE_TYPE = 0x0001
ZONE_STATUS = 0x0002


class BatterySize(t.enum8):
    """Battery sizes."""

    No_battery = 0x00
    Built_in = 0x01
    Other = 0x02
    AA = 0x03
    AAA = 0x04
    C = 0x05
    D = 0x06
    CR2 = 0x07
    CR123A = 0x08
    CR2450 = 0x09
    CR2032 = 0x0A
    CR1632 = 0x0B
    Unknown = 0xFF
