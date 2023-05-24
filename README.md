# oopsgenie

What
-----
Controls a stoplight based on open/acked alert count from the Ops Genie API using Raspberry Pi GPIO pins.  Red if there are open, un-acked alerts.  Yellow if there are open, acked alerts.  Green if no open alerts.  Does not account for "seen."

How
-----
Make sure to cp settings.py-dist to settings.py and configure.

In the author's case, lights are driven by a buffer chip which is then hooked to three solid-state relays.  The code doesn't care much about how you wire it up, as long as you use GPIO pins.

Oh, probably might need to `pip install RPi.GPIO`

At Boot
-----
Copy oopsgenie.service file to /etc/systemd/system.  Edit unit file to have appropriate path to boot.sh and username.  Run `sudo systemctl enable oopsgenie` to enable at boot.

