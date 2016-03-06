import sys
import time
import os
from time import strftime
import subprocess
from pubnub import Pubnub
import json
import uuid

#sys.argvs = Director, starttime, endtime

epid = uuid.uuid4()

if not os.path.isdir('/home/Project/Classified/'):
	os.makedirs('/home/Project/Classified/')
filename = '/home/Project/Classified/%s.txt' % strftime('%H_%M_%S')
log = open(filename, 'w')
#subprocess.Popen(['python','-m','pyAudioAnalysis.audioAnalysis','classifyFolder', '-i',sys.argv[1],'--model','knn','--classifier','/home/pi/Documents/testDog3','--details','>',filename])

process = subprocess.Popen(['python','-m','pyAudioAnalysis.audioAnalysis','classifyFolder', '-i',sys.argv[1],'--model','knn','--classifier','/home/Project/testDog3','--details']
 ,stdout=log, stderr=log)

process.wait()
episode = []
FNULL = open(os.devnull, 'w')
with open(filename, "r") as ifile:
	for line in ifile:
		if not line.strip():
			break
		if not ".wav" in line:
			break
		#if "Dog" in line:
		subprocess.Popen(['python','eventMessage.py', (line.rsplit(None, 1)[-1]), sys.argv[2], str(epid)], stdout=FNULL, stderr=subprocess.STDOUT)
		#list of classifications
		episode.append(line.rsplit(None, 1)[-1])
		
subprocess.Popen(['python','pictureMessage.py' str(epid)], stdout=FNULL, stderr=subprocess.STDOUT)
#send the episode summary to the cloud
pubnub = Pubnub(publish_key='pub-c-92b5e647-0c49-49a1-ab2a-4753777f53b9', subscribe_key='sub-c-02de9d80-9a93-11e5-9a49-02ee2ddab7fe',
                secret_key='sec-c-YTM5ZDM5ZmMtOTRmMS00Yzg2LThhYzQtYWI0Zjk2Yzg5M2U3')
	
channel = 'episodes'
Videomessage = json.dumps({'level': 0, 'count' : episode, 'start': sys.argv[2], 'end' : sys.argv[3], 'epid' : str(epid)})

pubnub.publish(
    channel = channel,
    message = Videomessage)
# out, err = process.communicate()
# test = out.splitlines()

# for s in test:
	# if "Dog" in s:
		# print(s)
