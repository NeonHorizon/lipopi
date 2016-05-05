LiPoPi Power Up / Power Down version
======

This version builds on the original and allows the push button switch to both power up the Raspberry Pi,
as shown already, as well as trigger an orderly shutdown of the Pi when it is pressed once the Pi has booted.

This uses a Python script that is run as a service from *systemd*, the Linux init system that starts up certain processes when the system boots.

==

###Circuit Schematic

![schematic](/pictures/lipopi_schematic_powerboost.png)

==

###Breadboard Layouts

This circuit has been tested with both the 500C and 1000C models of Adafruit PowerBoost Chargers.
The pin layout differs between the two boards and so two diagrams are shown here.

![schematic](/pictures/lipopi_breadboard_powerboost_500C.png)

![schematic](/pictures/lipopi_breadboard_powerboost_1000C.png)


==

###Setting up the Service with systemd

1: Copy the service file to /etc/systemd

$ sudo cp lipopi.service /etc/systemd/system/.

2: Enable the service

$ sudo systemctl enable lipopi.service
$ sudo systemctl start  lipopi.service

There is no need to restart the Pi

3: Try it out...

Log files will be written to /home/pi/lipopi - change this in the lipopi.py script


