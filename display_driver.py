import time
from typing import List
import datetime
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from image_utils import create_game_image, get_disconnect_image, concatenate_images
from data_utils import get_daily_game_info
from config import *
import sys

def should_poll(game_info, elapsed_sec):
    poll_time = POLLING_FREQUENCY if game_info is not None else EMERGENCY_POLLING_FREQUENCY
    return elapsed_sec >= poll_time

def scroll_game_image(game_infos: List[dict]):
    options = get_led_matrix_options()
    matrix = RGBMatrix(options=options)
    # set up a backup image when connection is lost
    if game_infos[0] is not None:
        if len(game_infos) < 2:
            game_infos = [game_infos[0]] * 2
        combined_image, _, _ = create_game_image(**game_infos[0])
        for game_info in game_infos[1:]:
            next_image, _, _ = create_game_image(**game_info)
            combined_image = concatenate_images(combined_image, next_image, MATRIX_COLS // 2)
    else:
        combined_image, _, _ = get_disconnect_image()

    combined_image_width, combined_image_height = combined_image.width, combined_image.height

    try:
        x_offset = combined_image_width
        canvas = matrix.CreateFrameCanvas()
        # While image is on screen
        while x_offset >= -MATRIX_COLS*options.chain_length:
            # Create a canvas sized to the LED matrix display
            display_region = combined_image.crop((x_offset, 0, x_offset + (MATRIX_COLS*options.chain_length), MATRIX_ROWS))
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
    yesterday_date = datetime.date.today() - datetime.timedelta(days=1)
    yesterday_date_str = yesterday_date.strftime("%Y-%m-%d")
    yesterday_game_data = get_daily_game_info(yesterday_date_str)

    if game_data is None or yesterday_game_data is None:
        game_data = [None]
    else:
        game_data.extend(yesterday_game_data)

    # loop and display
    start = time.time()
    while True:
        try:
            now = time.time()
            elapsed = now - start
            # refresh data at set intervals
            if should_poll(game_data[0], elapsed):
                game_data = get_daily_game_info()
                start = time.time()
            scroll_game_image(game_data)
        except KeyboardInterrupt:
            # Graceful exit on Ctrl+C
            sys.exit(0)
    