# NHL LED Display

This project uses the [NHL API](https://github.com/Zmalski/NHL-API-Reference) and [`rpi-rgb-led-matrix`](https://github.com/hzeller/rpi-rgb-led-matrix/tree/master) to display daily scores on an LED display.

[Example 16x32 Display](https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExYjBoMGE2dG1rcWN2bm0zZjh2Mm83NTRvdDczdzRxZXJvbTJwNWJmdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/JUPn9ZXY5U3Y6KxcM8/giphy.gif)

[Example 32x64 (x2) Display](https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnA3NmhxdmFsaTJ2cjhrMzVjcHAyc3N3cWNoYjNlY2R4NXpicHBsZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/So3XI5yCYzYygH5u9c/giphy.gif)

# Running Manually

You'll have to set up an LED RGB display and install the necessary requirements. I recommend following [this tutorial](https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/driving-matrices) for Raspberry Pi using the AdaFruit Matrix HAT+RTC. The tutorial above will install `rpi-rgb-led-matrix` into your python environment.

Then install the additional python requirements:
```python
pip install -r requirements.txt
``` 

To run on the display:
```python
python display_driver.py
```

# Editing Configuration Settings

If you have a different display size or are using different interface hardware (for example, not using the AdaFruit Matrix HAT+RTC) you may need to edit the display parameters. `config.py` is the central location where all major display settings are controlled. You can edit the expected dimensions of the display matrix, font sizes, and change where team logos are cached. You should definitely make sure that `MATRIX_ROWS`, `MATRIX_COLS`, and `chain_length` are set appropriately for your matrix setup.

```python
# config.py
WORK_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_CACHE_DIR = os.path.join(WORK_DIR, "nhl_team_logos")
TEAM_LOGO_SIZE = (30, 20) # chosen to retain the 3:2 aspect ratio for NHL logos
TEXT_FONT_PATH = os.path.join(WORK_DIR, "fonts", "bright_lights_.ttf")
TEXT_SCORE_FONT_SIZE = 18
TEXT_STANDARD_FONT_SIZE = 14
TEXT_STATE_FONT_SIZE = 8
DISPLAY_SCROLL_DELAY = 0.1 # delay before shifting pixels (in seconds), controls scroll speed
EMERGENCY_POLLING_FREQUENCY = 10 # Number of seconds after which to poll when there's a network error
POLLING_FREQUENCY = 60
...
```

# Network Configuration
## Using `raspi-config` (easy)
You can use the `raspi-config` configuration manager to edit your wireless settings.
```bash
ssh <user>@raspberrypi.local
sudo raspi-config
```
Then, visit `System Settings > Network` to edit your WPA2 credentials.

## Using `NetworkManager`
When you flash your Raspberry Pi OS for the first time, you'll get the opportunity to preconfigure a wireless network so that you can immediately `ssh` onto the board. The `NetworkManager` utility allows you to change this setting or add more wireless networks to your board's configuration. You can use the `nmcli` tool, but it's sometimes more expedient to just create a new `nmconnection` file manually.

```bash
cd /etc/system/NetworkManager/system-connections
sudo nano preconfigured.nmconnection # edit existing configuration
sudo nano <network_name>.nmconnection
```
### Example Connection File
```bash
[connection]
id=<network_name>
type=wifi

[wifi]
ssid=<network_ssid>
mode=infrastructure

[wifi-security]
key-mgmt=wpa-psk
psk=<network_password>

[ipv4]
method=auto

[ipv6]
method=auto
```

# Setting up the service to run on boot

We can use `systemctl` to setup this display to run on startup.

We can start by throwing all the logic we need into an easy-to-run script:
```bash
#!/bin/bash
# run_nhl.sh
source /path/to/your/venv/bin/activate
python /path/to/nhl_led_display/display_driver.py
```

Allow execution:
```bash
chmod +x /path/to/run_nhl.sh
```

Now we can start to create our service using `systemctl`.

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
