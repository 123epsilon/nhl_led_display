import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from image_utils import create_game_image, get_disconnect_image
from data_utils import get_daily_game_info
from config import *
import sys

def should_poll(game_info, elapsed_sec):
    poll_time = POLLING_FREQUENCY if game_info is not None else EMERGENCY_POLLING_FREQUENCY
    return elapsed_sec >= poll_time

def scroll_game_image(game_info):
    options = get_led_matrix_options()
    matrix = RGBMatrix(options=options)
    # set up a backup image when connection is lost
    if game_info is not None:
        combined_image, combined_image_width, combined_image_height = create_game_image(**game_info)
    else:
        combined_image, combined_image_width, combined_image_height = get_disconnect_image()

    try:
        x_offset = combined_image_width
        canvas = matrix.CreateFrameCanvas()
        # While image is on screen
        while x_offset >= -MATRIX_COLS:
            # Create a canvas sized to the LED matrix display
            display_region = combined_image.crop((x_offset, 0, x_offset + MATRIX_COLS, MATRIX_ROWS))
            canvas.SetImage(display_region, 0, 0)

            # Scroll left by one pixel
            x_offset -= 1

            canvas = matrix.SwapOnVSync(canvas)
            time.sleep(DISPLAY_SCROLL_DELAY)
    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        pass


if __name__ == "__main__":
    game_data = get_daily_game_info()
    if game_data is None:
        game_data = [None]
    
    # loop and display
    start = time.time()
    while True:
        try:
            i = 0
            game_info = game_data[i]
            while i < len(game_data):
                now = time.time()
                elapsed = now - start
                # refresh data at set intervals
                if should_poll(game_info, elapsed):
                    game_data = get_daily_game_info()
                    start = time.time()
                    # this shouldn't ever happen for daily games, but why not be safe?
                    if i >= len(game_data):
                        i = 0
                
                game_info = game_data[i]
                scroll_game_image(game_info)
                i += 1
        except KeyboardInterrupt:
            # Graceful exit on Ctrl+C
            sys.exit(0)
    