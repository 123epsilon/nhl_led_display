# NHL LED Display

This project uses the [NHL API](https://github.com/Zmalski/NHL-API-Reference) and [`rpi-rgb-led-matrix`](https://github.com/hzeller/rpi-rgb-led-matrix/tree/master) to display daily scores on an LED display.

[Example Display](https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExYjBoMGE2dG1rcWN2bm0zZjh2Mm83NTRvdDczdzRxZXJvbTJwNWJmdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/JUPn9ZXY5U3Y6KxcM8/giphy.gif)

# Running

You'll have to set up an LED RGB display and install the necessary requirements. I recommend following[this tutorial](https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/driving-matrices) for Raspberry Pi using the AdaFruit Matrix HAT+RTC. The tutorial above will install `rpi-rgb-led-matrix` into your python environment.

Then install the additional python requirements:
```python
pip install -r requirements.txt
``` 

To run on the display:
```python
python display_driver.py
```

# Editing Configuration Settings

If you have a different display size or are using different interface hardware (for example, not using the AdaFruit Matrix HAT+RTC) you may need to edit the display parameters. `config.py` is the central location where all major display settings are controlled. You can edit the expected dimensions of the display matrix, font sizes, and change where team logos are cached. 
