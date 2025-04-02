import os
from PIL import Image, ImageDraw, ImageFont
from urllib.parse import urlparse
import cairosvg
import requests
from config import IMAGE_CACHE_DIR, TEAM_LOGO_SIZE, TEXT_FONT_PATH, TEXT_SCORE_FONT_SIZE, TEXT_STANDARD_FONT_SIZE, TEXT_STATE_FONT_SIZE

def get_team_logo(svg_url: str) -> Image:
    """
    Gets and caches an SVG Image from a URL as a PNG file for display.
    Attempts to retrieve from cache before pulling from URL.
    """

    # get identifier for cache (base filename without extension)
    url = urlparse(svg_url)
    key = os.path.splitext(os.path.basename(url.path))[0]

    # search cache
    os.makedirs(IMAGE_CACHE_DIR, exist_ok=True)
    image_save_path = os.path.join(IMAGE_CACHE_DIR, f"{key}.png")
    if not os.path.exists(image_save_path):
        cairosvg.svg2png(url=svg_url, write_to=image_save_path)
    
    # read and resize image for display
    image = Image.open(image_save_path).convert("RGB")
    image = image.resize(TEAM_LOGO_SIZE, Image.Resampling.LANCZOS)
    return image


def create_game_image(awayLogoURL: str, homeLogoURL: str, awayShortName: str, homeShortName: str, score_string: str, state_string: str) -> Image:
    # Load team logos for display
    awayLogo = get_team_logo(awayLogoURL)
    homeLogo = get_team_logo(homeLogoURL)

    # Setup fonts for text display
    font = ImageFont.truetype(TEXT_FONT_PATH, TEXT_STANDARD_FONT_SIZE)
    score_font = ImageFont.truetype(TEXT_FONT_PATH, TEXT_SCORE_FONT_SIZE)
    state_font = ImageFont.truetype(TEXT_FONT_PATH, TEXT_STATE_FONT_SIZE)

    # Create a combined image that will hold the Logo and the text side-by-side
    h_spacing = 7
    image_width, image_height = awayLogo.size
    away_text_width, away_text_height = font.getsize(awayShortName)
    home_text_width, home_text_height = font.getsize(homeShortName)
    state_text_width, state_text_height = state_font.getsize(state_string)
    print(image_width, image_height)
    print(away_text_width, away_text_height)
    score_text_width, score_text_height = score_font.getsize(score_string)
    combined_height = image_height + away_text_height # stacked height of logo and team name
    combined_width = image_width + score_text_width + image_width # width of two logo images and the score text
    
    # Place logos on display image
    combined_image = Image.new('RGB', (combined_width, combined_height))
    combined_image.paste(awayLogo, (0, 0))
    combined_image.paste(homeLogo, (combined_width-image_width, 0))

    # Draw the team names under the logos
    vneg_space = 2
    draw = ImageDraw.Draw(combined_image)
    text_position = (0, image_height-vneg_space)
    print(text_position)
    draw.text(text_position, awayShortName, font=font, fill=(255, 255, 255))

    text_position = (combined_width-home_text_width, image_height-vneg_space)
    print(text_position)
    draw.text(text_position, homeShortName, font=font, fill=(255, 255, 255))


    # Draw score text to the right of the away team logo
    text_position = ((combined_width - score_text_width) // 2, (image_height - away_text_height) // 2)
    print(text_position)
    draw.text(text_position, score_string, font=score_font, fill=(255, 255, 255))

    # Draw state text under the score
    text_position = ((combined_width - state_text_width) // 2, away_text_height)
    print(text_position)
    draw.text(text_position, state_string, font=state_font, fill=(255, 255, 255))

    print(combined_image.width, combined_image.height)
    return combined_image, combined_image.width, combined_image.height

