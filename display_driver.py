import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from image_utils import create_game_image
from data_utils import get_daily_game_info
from config import MATRIX_ROWS, MATRIX_COLS, DISPLAY_SCROLL_DELAY, get_led_matrix_options
import sys

def scroll_game_image(game_info):
    options = get_led_matrix_options()
    matrix = RGBMatrix(options=options)
    combined_image, combined_image_width, combined_image_height = create_game_image(**game_info)

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
    
    # loop and display
    while True:
        try:
            for game_info in game_data:
                scroll_game_image(game_info)
        except KeyboardInterrupt:
            # Graceful exit on Ctrl+C
            sys.exit(0)
    