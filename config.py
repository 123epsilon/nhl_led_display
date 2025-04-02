import os
from rgbmatrix import RGBMatrixOptions

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_CACHE_DIR = os.path.join(WORK_DIR, "nhl_team_logos")
TEAM_LOGO_SIZE = (15, 10) # chosen to retain the 3:2 aspect ratio for NHL logos
TEXT_FONT_PATH = "/home/dennis/Desktop/led_examples/rpi-rgb-led-matrix/fonts/bright_lights_.ttf"
TEXT_SCORE_FONT_SIZE = 8
TEXT_STANDARD_FONT_SIZE = 8
TEXT_STATE_FONT_SIZE = 6
DISPLAY_SCROLL_DELAY = 0.1 # delay before shifting pixels (in seconds), controls scroll speed

MATRIX_ROWS = 16
MATRIX_COLS = 32

def get_led_matrix_options():
    options = RGBMatrixOptions()
    options.rows = MATRIX_ROWS
    options.cols = MATRIX_COLS
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat'
    return options