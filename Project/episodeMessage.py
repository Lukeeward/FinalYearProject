from pubnub import Pubnub
import json
import time
import sys
from time import strftime

pubnub = Pubnub(publish_key='pub-c-92b5e647-0c49-49a1-ab2a-4753777f53b9', subscribe_key='sub-c-02de9d80-9a93-11e5-9a49-02ee2ddab7fe',
                secret_key='sec-c-YTM5ZDM5ZmMtOTRmMS00Yzg2LThhYzQtYWI0Zjk2Yzg5M2U3')
	
channel = 'episodes'
Videomessage = json.dumps({'level': 0, 'duration': sys.argv[1], 'start' : (strftime("%Y-%m-%d %H:%M"))})

pubnub.publish(
    channel = channel,
    message = Videomessage)