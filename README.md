# website_blocker
This is a script meant to be run via cron at each reboot. It blocks the website that you input as a string (using the -l argument) or as a file (-f). It checks the local time by using the time package. It also uses argparse to accept arguments at runtime.
