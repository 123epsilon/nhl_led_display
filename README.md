# NHL LED Display

This project uses the [NHL API](https://github.com/Zmalski/NHL-API-Reference) and [`rpi-rgb-led-matrix`](https://github.com/hzeller/rpi-rgb-led-matrix/tree/master) to display daily scores on an LED display.

[Example Display](https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExYjBoMGE2dG1rcWN2bm0zZjh2Mm83NTRvdDczdzRxZXJvbTJwNWJmdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/JUPn9ZXY5U3Y6KxcM8/giphy.gif)

# Running Manually

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

# Setting up the service to run on boot

We can use `systemctl` to setup this display to run on startup.

We can start by throwing all the logic we need into an easy to run script:
```bash
#!/bin/bash
# run_nhl.sh
source /path/to/your/venv/bin/activate
python /path/to/nhl_led_display/display_driver.py
```

Then set the permissions appropriately:
```bash
chmod +x /path/to/run_nhl.sh
```

Now we can start to create our service using systemctl.

```bash
sudo nano /etc/systemd/system/nhl_scoreboard.service
```

This is what `nhl_scoreboard.service` should look like
```
[Unit]
Description=Run NHL Scoreboard Display
After=network.target

[Service]
ExecStart=/path/to/run_nhl.sh
WorkingDirectory=/path/to/nhl_led_display
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

Then use the following to set up and start the service
```bash
sudo chmod 644 /etc/systemd/system/nhl_scoreboard.service
sudo systemctl daemon-reload # needs to be rerun if you edit the service file
sudo systemctl enable nhl_scoreboard.service
sudo systemctl start nhl_scoreboard.service
```

You can check the status of the service by running

```bash
sudo systemctl status nhl_scoreboard.service
```

And voila! The display will start automatically when your device boots up!