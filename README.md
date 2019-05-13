LiPoPi
=======

- **Description:** LiPoPi is a guide to setting up the Raspberry Pi with a LiPo battery including both running and charging it
- **Project Website:** [GitHub](https://github.com/NeonHorizon/lipopi)
- **Requirements:** A Raspberry Pi and an Adafruit [PowerBoost 500 Charger](https://www.adafruit.com/product/1944) or [1000C Charger](https://www.adafruit.com/products/2465)
- **Skillset:** Requires soldering skills and a basic knowledge of the command line
- **License:** GPL Version 3

---

### Power-Up / Power-Down Version

See [this page](/README.power_up_power_down.md) for a version in which the push button switch can both power up the Raspberry Pi and trigger an orderly shutdown.

---

### Advanced Version With Battery Level Monitoring

See [this page](https://github.com/craic/pi_power) for advanced version of this project which includes the features of the power up/down version above as well as battery level monitoring.

---

### Basic Version Features
- Push button to power up the Pi (requires a long push - good for preventing accidental starts)
- Automatic shut off of the PowerBoost power supply after the Pi is shutdown
- Automatic graceful shutdown of the Pi when the battery is low (to stop SD card corruption)
- Single power socket to both charge and run the Pi
- If using the example layout, the power button, power socket and SD card are located all on one end (makes cases nicer)

![overview](https://raw.github.com/NeonHorizon/lipopi/master/pictures/overview.jpg)

---

### How it Works
When pushed the LiPoPi power button connects the battery output (Bat) to the enable line (EN) on the Adafruit PowerBoost which then powers up boosting the LiPo's 3.7v to the ~5.2v required by the Pi. This causes the Pi to begin to boot and after about 3 seconds GPIO 14 (UART TXD) goes high (due to its unique characteristic of going to 3.3v whilst the Pi is running and back to 0v when the Pi is shut down). This then takes over the job of keeping the enable line on the PowerBoost high and the Pi remains powered up even after the pushbutton is released.

Whilst the Pi is running the PowerBoost informs the Pi of the battery status by switching the LB / LBO pin (which is connected to GPIO 15 - UART RXD) low when the battery is low. This is picked up by a cron task on the Pi which initiates a graceful shutdown making sure no data is lost and the SD card does not get corrupted. Once the Pi is shutdown (for whatever reason) GPIO 14 goes low again, causing the PowerBoost's enable line to drop and the whole system to power off.

We've had a question about how long the batteries will last, a few of you might wish to know how to calculate this. For more information see the [thread here](https://github.com/NeonHorizon/lipopi/issues/4)

---

### Hardware
![circuit](https://raw.github.com/NeonHorizon/lipopi/master/pictures/circuit.png)

*(Please Note: Do not connect devices which use GPIO 14 or 15 (UART/Serial) to the Pi at the same time as this circuit as they will cause your Pi to power off or shutdown)*

1. Connect the PowerBoost's 5v output to your Raspberry Pi either by soldering wires directly between the two (you can use the GPIO to power the Pi for example) or by attaching the optional USB socket to the PowerBoost and using a regular micro USB cable between the two.

2. Put a known good SD card in your Pi, connect a LiPo battery to the PowerBoost and check that the Pi starts up straight away and runs correctly (you may need to charge the battery first).

3. Shut everything down and disconnect the LiPo again.

4. Solder a 100k resistor between one of the ground lines (GND) on the PowerBoost and the enable line (EN). (See notes about Raspberry Pi 3)

5. Connect the LiPo back up to the PowerBoost and if you have fitted the resistor correctly you will notice this time it doesn't power up on its own, this is because the resistor pulls the enable line low.

6. Disconnect the LiPo again.

7. Connect a pushbutton between the battery output (Bat) on the PowerBoost and the same enable line (EN) you previously connected the resistor to.

8. Connect the LiPo back up to the PowerBoost, again the Pi should not start.

9. Press and hold the button just long enough to check the Pi power light comes on (confirming your wiring is correct) but not enough for it to start booting (if you do accidentally go too far, shutdown the Pi before releasing the power button).

10. Disconnect the LiPo again.

11. Connect a 10k GPIO protection resistor between Pin 8 (GPIO 14 - UART TXD) on the Raspberry Pi and the PowerBoost enable line (EN) (the same place that the resistor and pushbutton are connected to).

12. Connect the LiPo back up to the PowerBoost, again the Pi should not start.

13. Press and hold the button for at least 3 seconds, the Pi should start booting. If you have done step 1 of the software instructions when you release the button the Pi should continue booting.

14. Shutdown the Pi with the shutdown command (DO NOT use the halt command), the Pi should shut down followed by the PowerBoost shutting off.

15. Connect a wire between the low battery line (LB / LBO) on the PowerBoost and pin 10 (GPIO 15 - UART RXD) on the Raspberry Pi, this is to tell the Pi when the battery is low (you can use a different GPIO if you prefer).

---

### Special Note About Raspberry Pi 3

Previously unlike the other Pi's the Raspberry Pi 3's software emulated version of the UART meanst that GPIO 14 was not high by default. The way to resolve this was to enable the console which produced enough data that we could "pretend" GPIO 14 was high by placing a 100uf capacitor across the 100k resistor.

However this appears to be solved in the newer versions so you can use the Pi3 in the same way as with the other models.

---

### Software
1. Run sudo raspi-config and select "Interfacing Options" followed by "Serial" and answer "Would you like a login shell to be accessible over serial?" with No, followed by "Would you like the serial port hardware to be enabled?" with yes.

2. Run wget -N https://raw.github.com/NeonHorizon/lipopi/master/low_bat_shutdown to get the example script which checks for low battery and shuts down the Pi (if you prefer you could write this in Python or whatever).

3. Make it executable with chmod +x low_bat_shutdown

4. If you used a pin other than GPIO 15 for the low battery line (hardware step 15), edit this file and change the pin number (otherwise you don't need to edit it at all).

5. Execute this script by typing ./low_bat_shutdown nothing should happen. If the Pi shuts down then you did something wrong in Hardware step 15.

6. Either leave the script in your home directory or move it to somewhere on the Pi where it wont get deleted, it needs to be run regularly by the system to check for low battery, if you delete it your Pi wont shut down!

7. Go into the cron directory where scheduled tasks are by typing cd /etc/cron.d

8. Fetch the example script (which repeatedly checks for low battery) by typing wget -N https://raw.github.com/NeonHorizon/lipopi/master/power_check

9. Edit the script and change the path (underneath where it says command) to the full path of your low_bat_shutdown script (where you moved it in step 6), by default it looks in the Pi home directory.

10. The last part of the script ( >> /home/pi/low_bat_shutdown.log 2&>1 ) produces a log file in your home directory, you can change this if you wish.

11. If all is good you should be able to leave the Pi running and when the battery gets low it should shut down. You can check this worked OK by running the Pi until it goes off then powering it up again (once you have connected power) and checking the log file. If the file is blank then the Pi was not shutdown properly.

---

### Example Implementation
![running](https://raw.github.com/NeonHorizon/lipopi/master/pictures/running.jpg)
![connectors](https://raw.github.com/NeonHorizon/lipopi/master/pictures/connectors.jpg)
![wiring](https://raw.github.com/NeonHorizon/lipopi/master/pictures/wiring.jpg)
![angle](https://raw.github.com/NeonHorizon/lipopi/master/pictures/angle.jpg)
![charging](https://raw.github.com/NeonHorizon/lipopi/master/pictures/charging.jpg)

---

### License Information

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).

---

### Credits

- [Daniel Bull](https://google.com/+DanielBull)
- [Rob Jones](https://github.com/craic)
- [Simon](https://github.com/macsimski)
- [Tom McIntyre](https://github.com/tommcintyre)
- [Jean Rocco](https://github.com/jeanrocco)
- [Steve Johnson](https://github.com/svenyonson)
