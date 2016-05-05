LiPoPi Power Up / Power Down version
======

This version builds on the original and allows the push button switch to both power up the Raspberry Pi,
as shown already, as well as trigger an orderly shutdown of the Pi when it is pressed once the Pi has booted.

This uses a Python script that is run as a service from *systemd*, the Linux init system that starts up certain processes when the system boots.

==

###How It Works

![schematic](/pictures/lipopi_schematic_powerboost.png)

The Low Battery signal path is identical to the LiPoPi original and the Power Up path ony differs by the addition of a 1N4001 diode between
the switch and the Enable pin. This path relies on GPIO 14 being pulled high once the Pi is running. The diode prevents this from pulling GPIO 18 high.

The Power Down path pulls GPIO 18 high when the pushbutton switch is pressed. The Python script reacts to this trigger and initiates a system shutdown.

So what are the two 1N4001 diodes in series doing ? The Battery can have a voltage from around 4.7V when fully charged down to 3.2V when discharged.
But the Pi can only tolerate 3.3V on its GPIO pins. You could handle this using two resistors to create a voltage divider (e.g. 33K and 100K) but in our case we
the voltage drop inherent in diodes to lower this from 4.2V down to 2.8V (each 1N4001 has a forward voltage drop of around 0.7V).
This is close enough to 3.3V that it will trigger the GPIO pin without the risk of damage.

==

###Adafruit PowerBoost Charger 500C versus 1000C


==

###Breadboard Layouts

This circuit has been tested with both the 500C and 1000C models of Adafruit PowerBoost Chargers.
The pin layout differs between the two boards and so two diagrams are shown here.

![schematic](/pictures/lipopi_breadboard_powerboost_500C.png)

![schematic](/pictures/lipopi_breadboard_powerboost_1000C.png)


==

###Setting up the Service with systemd

1: Copy the service file to /etc/systemd

```bash
$ sudo cp lipopi.service /etc/systemd/system/.
```

2: Enable the service

```bash
$ sudo systemctl enable lipopi.service
$ sudo systemctl start  lipopi.service
```

There is no need to restart the Pi

3: Try it out...

Log files will be written to /home/pi/lipopi - change this in the lipopi.py script


