from pubnub import Pubnub
import json
import time
import sys
from time import strftime
import base64
from PIL import Image

pubnub = Pubnub(publish_key='pub-c-92b5e647-0c49-49a1-ab2a-4753777f53b9', subscribe_key='sub-c-02de9d80-9a93-11e5-9a49-02ee2ddab7fe',
                secret_key='sec-c-YTM5ZDM5ZmMtOTRmMS00Yzg2LThhYzQtYWI0Zjk2Yzg5M2U3')
	
channel = 'snapshots'

def _error(message):
	print(message)
	
	
snapshot = Image.open("/var/lib/motion/lastsnap.jpg")
snapshot = snapshot.resize((320,240),Image.ANTIALIAS)
snapshot.save("/home/Project/scaled.jpg",optimize=True,quality=85)

with open("/home/Project/scaled.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())


pubnub.publish(
    channel = channel,
    message = {"picture" : encoded_string, "epid" : sys.argv[1]}, 
	error=_error)