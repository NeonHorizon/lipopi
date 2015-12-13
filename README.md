LiPoPi
=======

- **Description:** LiPoPi is a guide to setting up the Raspberry Pi with a LiPo battery including both running and charging it
- **Project Website:** [GitHub](https://github.com/NeonHorizon/lipopi)
- **Requirements:** A Raspberry Pi (any model) and an Adafruit PowerBoost 500 Charger (Adafruit 1944)
- **Skillset:** Requires soldering skills and a basic knowledge of the command line
- **License:** GPL Version 3

###Features
- Push button to power up the Pi (requires a long push - good for preventing accidental starts)
- Automatic shut off of the power supply after the Pi is shutdown
- Automatic graceful shutdown of the Pi when the battery is low (to stop SD card corruption)
- Single power socket to both charge and run the Pi
- If using the example layout, the power button, power socket and SD card are located all on one end (makes cases nicer)

==
![overview](https://raw.github.com/NeonHorizon/lipopi/master/pictures/overview.jpg)

###How it Works
The LiPoPi power button once pushed connects the battery output (Bat) to the enable line (EN) on the Adafruit PowerBoost and it then powers up boosting the LiPo's 3.7v to the 5.2v required by the Pi. This causes the Pi to begin to boot and after about 3 seconds GPIO 14 (UART TXD) goes high (due to its unique characteristic of going to 3.3v whilst the Pi is running and back to 0v when the Pi is shut down). GPIO 14 then takes over the job of keeping the enable line on the PowerBoost high and the Pi remains powered up even after the pushbutton is released. Whilst the Pi is running the PowerBoost informs the Pi of the battery status by switching the LBO pin (which is connected to GPIO 15 - UART RXD) high when its low. This is picked up by a cron task on the Pi which initiates a graceful shutdown making sure no data is lost and the SD card does not get corrupted. Once the Pi is shutdown (for whatever reason) GPIO 14 goes low again, causing the PowerBoost enable line to drop and the whole system to power off.

###Hardware
![circuit](https://raw.github.com/NeonHorizon/lipopi/master/pictures/circuit.png)

1. Connect the PowerBoost's 5v output to your Raspberry Pi either by soldering wires directly between the two (you can use the GPIO to power the Pi for example) or by attaching the optional USB socket to the PowerBoost and using a regular micro USB cable between the two.

2a. Put a known good SD card in your Pi, connect a LiPo battery to the PowerBoost and check the Pi starts up straight away and runs correctly (you may need to charge the battery first).

2b. Shut everything down and disconnect the LiPo again.

3. Solder a 100k resistor between one of the ground lines (GND) on the PowerBoost and the enable line (EN).

4a. Connect the LiPo back up to the PowerBoost and if you have fitted the resistor correctly you will notice this time it doesn't power up on its own, this is because the resistor pulls the enable line low.

4b. Disconnect the LiPo again.

5. Connect a pushbutton between the same enable line (EN) you previously connected the resistor to and the battery output (Bat) on the PowerBoost.

6a. Connect the LiPo back up to the PowerBoost, the Pi should not start.

6b. Press and hold the button just long enough to check the Pi power light comes on (confirming your wiring is correct) but not enough for it to start booting (if you do accidentally go too far, shutdown the Pi before releasing the power button).

6c. Disconnect the LiPo again.

7. Connect a 10k GPIO protection resistor between to the Pin 8 (GPIO 14 - UART TXD) on the Raspberry Pi and the same enable line (EN) on the PowerBoost that the resistor and pushbutton are connected to.

8a. Connect the LiPo back up to the PowerBoost, the Pi should not start.

8b. Press and hold the button for at least 3 seconds, the Pi should start booting, then let go of the button, the Pi should remain on and continue booting.

8c. Shutdown the Pi with the shutdown command (DO NOT use the halt command), the Pi should shut down followed by the PowerBoost shutting off.

9. Connect a wire between the low battery line (LB / LBO) on the PowerBoost and pin 10 (GPIO 15 - UART RXD) on the Raspberry Pi, this is to tell the Pi when the battery is low (you can use a different GPIO if you prefer).

###Software
1. Run sudo raspi-config and under "Advanced Options" select "Serial" followed by "No". This prevents the Pi using GPIO 14 for the console and which would shut off the power.

2a. Run wget -N https://raw.github.com/NeonHorizon/lipopi/master/low_bat_shutdown to get the example script which checks for low battery and shuts down the Pi (if you prefer you could write this in Python or whatever).

2b. Make it executable with chmod +x low_bat_shutdown.

2c. If you used a pin other than GPIO 14 when you wired up the low battery line in Hardware step 9, edit this file and change the pin number, otherwise you don't need to edit it at all.

2d. Execute the script by typing ./low_bat_shutdown nothing should happen. If the Pi shuts down then you did something wrong in Hardware step 9.

2c. Either leave the script in your home directory or move it to somewhere on the Pi where it wont get deleted, it needs to be run regularly by the system to check for low battery, if you delete it your Pi wont shut down!

3a. Go into the cron directory where scheduled tasks are set by typing cd /etc/cron.d

3b. Fetch the example script (which repeatedly checks for low battery) by typing wget -N https://raw.github.com/NeonHorizon/lipopi/master/power_check

3c. Edit the script and change the path (underneath where it says command) to the full path of your low_bat_shutdown script (where you moved it in step 2c), by default it looks in the Pi home directory.

3d. The last part of the script ( >> /home/pi/low_bat_shutdown.log 2&>1 ) produces a log file in your home directory, you can change this if you wish.

4. If all is good you should be able to leave the Pi running and when the battery gets low it should shut down, you can check it worked OK by powering back up the Pi once you have charged the battery and checking the log file. If the file is blank then the Pi was not shutdown properly.

###Example Implimentation
![running](https://raw.github.com/NeonHorizon/lipopi/master/pictures/running.jpg)
![connectors](https://raw.github.com/NeonHorizon/lipopi/master/pictures/connectors.jpg)
![wiring](https://raw.github.com/NeonHorizon/lipopi/master/pictures/wiring.jpg)
![angle](https://raw.github.com/NeonHorizon/lipopi/master/pictures/angle.jpg)
![charging](https://raw.github.com/NeonHorizon/lipopi/master/pictures/charging.jpg)


###License Information

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).
