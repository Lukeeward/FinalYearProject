####
#### Audio Classification script
#### The supplied folder path containing the split .wavs are classifed
#### with the results sent via PubNub
####

import sys
import time
import os
from time import strftime
import subprocess
from pubnub import Pubnub
import json
import uuid
from collections import Counter

#sys.argvs = Director, starttime, endtime

# Generate a new uuid for this audio episode
epid = uuid.uuid4()

# Get the required classifer file name
# This is changes in listenforapp.py
if os.path.exists('/home/Project/classifer') :
	with open('/home/Project/classifer', 'r') as myfile:
		classiferName = myfile.read()
else :
	classiferName = 'testDogx'
	
# Create the results log file
if not os.path.isdir('/home/Project/Classified/'):
	os.makedirs('/home/Project/Classified/')
filename = '/home/Project/Classified/%s.txt' % strftime('%H_%M_%S')
log = open(filename, 'w')
#Each file in the folder is classifed using pyAudioAnalysis, with results organised into a .txt file
process = subprocess.Popen(['python','-m','pyAudioAnalysis.audioAnalysis','classifyFolder', '-i',sys.argv[1],'--model','knn','--classifier','/home/Project/' + str(classiferName),'--details']
 ,stdout=log, stderr=log)
process.wait()
# initialise an empty array to store the results in
episode = []
FNULL = open(os.devnull, 'w')
#Open the result .txt file
with open(filename, "r") as ifile:
	for line in ifile:
		if not line.strip():
			break
		if not ".wav" in line:
			break
		#For each result pass the type to eventMessage.py
		subprocess.Popen(['python','/home/Project/eventMessage.py', (line.rsplit(None, 1)[-1]), sys.argv[2], str(epid)], stdout=FNULL, stderr=subprocess.STDOUT)
		#Add to list of results
		episode.append(line.rsplit(None, 1)[-1])

# Find the most common type, as this will probably be the main cause of the audio event
data = Counter(episode)
print(data.most_common(1)[0][0])

# Call pictureMessage.py to send the snapshot
subprocess.Popen(['python','/home/Project/pictureMessage.py', str(epid)], stdout=FNULL, stderr=subprocess.STDOUT)

#Initialise PubNub
pubnub = Pubnub(publish_key='pub-c-92b5e647-0c49-49a1-ab2a-4753777f53b9', subscribe_key='sub-c-02de9d80-9a93-11e5-9a49-02ee2ddab7fe',
                secret_key='sec-c-YTM5ZDM5ZmMtOTRmMS00Yzg2LThhYzQtYWI0Zjk2Yzg5M2U3')
channel = 'episodes'
# Organise the episode message details
episodemessage = json.dumps({'level': 0, 'count' : episode, 'start': sys.argv[2], 'end' : sys.argv[3], 'epid' : str(epid)})
# Send via PubNub
pubnub.publish(
    channel = channel,
    message = episodemessage)
# Call PushPythonscript.py to send a Push Notification to the mobile with the common audio type
subprocess.Popen(['python','/home/Project/PushPythonscript.py', (data.most_common(1)[0][0]), sys.argv[2], str(epid)], stdout=FNULL, stderr=subprocess.STDOUT)

