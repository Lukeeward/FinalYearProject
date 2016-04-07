####
#### Send the event message using PubNub
####

from pubnub import Pubnub
import json
import time
import sys
from time import strftime

# Initialise PubNub
pubnub = Pubnub(publish_key='pub-c-92b5e647-0c49-49a1-ab2a-4753777f53b9', subscribe_key='sub-c-02de9d80-9a93-11e5-9a49-02ee2ddab7fe',
                secret_key='sec-c-YTM5ZDM5ZmMtOTRmMS00Yzg2LThhYzQtYWI0Zjk2Yzg5M2U3')
channel = 'events'

# Organise the message details passed from classifySounds.py
Videomessage = json.dumps({'type': "audio", 'level': 0, 'reason' : sys.argv[1], 'time': sys.argv[2], 'epid' : sys.argv[3]})

# Publish message
pubnub.publish(
    channel = channel,
    message = Videomessage)