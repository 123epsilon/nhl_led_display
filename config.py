import os
from rgbmatrix import RGBMatrixOptions

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_CACHE_DIR = os.path.join(WORK_DIR, "nhl_team_logos")
TEAM_LOGO_SIZE = (30, 20) # chosen to retain the 3:2 aspect ratio for NHL logos
TEXT_FONT_PATH = os.path.join(WORK_DIR, "fonts", "bright_lights_.ttf")
TEXT_SCORE_FONT_SIZE = 18
TEXT_STANDARD_FONT_SIZE = 14
TEXT_STATE_FONT_SIZE = 8
DISPLAY_SCROLL_DELAY = 0.1 # delay before shifting pixels (in seconds), controls scroll speed
EMERGENCY_POLLING_FREQUENCY = 10 # Number of seconds after which to poll when there's a network error
POLLING_FREQUENCY = 60 # Number of seconds after which to poll for new data
DISCONNECT_IMAGE_PATH = os.path.join(WORK_DIR, "img", "wifi-cross.png")

MATRIX_ROWS = 32
MATRIX_COLS = 64

def get_led_matrix_options():
    options = RGBMatrixOptions()
    options.rows = MATRIX_ROWS
    options.cols = MATRIX_COLS
    options.chain_length = 1
    options.parallel = 1
    options.gpio_slowdown = 2
    options.hardware_mapping = 'adafruit-hat'
    return options