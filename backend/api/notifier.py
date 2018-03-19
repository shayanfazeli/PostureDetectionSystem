import os
from sys import platform
import time

def notify(title, text):
	if platform == "linux" or platform == "linux2":
	    os.system("""
	    	notify-send "{}" "{}"
	    	""".format(text, title))
	elif platform == "darwin":
	    os.system("""
	              osascript -e 'display notification "{}" with title "{}"'
	              """.format(text, title))

def notification_process(bad_posture, sitting_too_long): 
	bad_posture_cooldown = 0
	sitting_too_long_cooldown = 0
	COOLDOWN = 20

	while True:
		if bad_posture.value == 1 and bad_posture_cooldown == 0:
			notify("Bad Posture", "Bad posture was detected.")
			bad_posture_cooldown = COOLDOWN
			bad_posture.value = 0
		if sitting_too_long.value == 1 and sitting_too_long_cooldown == 0:
			notify("Sitting too long", "You have been sitting for too long. Take a break!")
			sitting_too_long_cooldown = COOLDOWN
			sitting_too_long.value = 0

		if bad_posture_cooldown > 0:
			bad_posture_cooldown -= 1
			bad_posture.value = 0
		if sitting_too_long_cooldown > 0:
			sitting_too_long_cooldown -= 1
			sitting_too_long.value = 0

		if bad_posture_cooldown:
			bad_posture_cooldown -= 1
		if sitting_too_long_cooldown:
			sitting_too_long_cooldown -= 1

		time.sleep(1)




