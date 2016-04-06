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

epid = uuid.uuid4()

if os.path.exists('/home/Project/classifer') :
	with open('/home/Project/classifer', 'r') as myfile:
		classiferName = myfile.read()
else :
	classiferName = 'testDogx'

if not os.path.isdir('/home/Project/Classified/'):
	os.makedirs('/home/Project/Classified/')
filename = '/home/Project/Classified/%s.txt' % strftime('%H_%M_%S')
log = open(filename, 'w')
#Each file in folder is classifed, with results organised into a .txt file
process = subprocess.Popen(['python','-m','pyAudioAnalysis.audioAnalysis','classifyFolder', '-i',sys.argv[1],'--model','knn','--classifier','/home/Project/' + str(classiferName),'--details']
 ,stdout=log, stderr=log)

process.wait()
episode = []
FNULL = open(os.devnull, 'w')
#Open the result .txt file
with open(filename, "r") as ifile:
	for line in ifile:
		if not line.strip():
			break
		if not ".wav" in line:
			break
		#Message the result to messaging service
		subprocess.Popen(['python','/home/Project/eventMessage.py', (line.rsplit(None, 1)[-1]), sys.argv[2], str(epid)], stdout=FNULL, stderr=subprocess.STDOUT)
		#Add to list of classifications
		episode.append(line.rsplit(None, 1)[-1])

data = Counter(episode)
print(data.most_common(1)[0][0])
#Send picture message
subprocess.Popen(['python','/home/Project/pictureMessage.py', str(epid)], stdout=FNULL, stderr=subprocess.STDOUT)
#send the episode summary to messaging service
pubnub = Pubnub(publish_key='pub-c-92b5e647-0c49-49a1-ab2a-4753777f53b9', subscribe_key='sub-c-02de9d80-9a93-11e5-9a49-02ee2ddab7fe',
                secret_key='sec-c-YTM5ZDM5ZmMtOTRmMS00Yzg2LThhYzQtYWI0Zjk2Yzg5M2U3')
	
channel = 'episodes'
episodemessage = json.dumps({'level': 0, 'count' : episode, 'start': sys.argv[2], 'end' : sys.argv[3], 'epid' : str(epid)})
pubnub.publish(
    channel = channel,
    message = episodemessage)

subprocess.Popen(['python','/home/Project/PushPythonscript.py', (data.most_common(1)[0][0]), sys.argv[2], str(epid)], stdout=FNULL, stderr=subprocess.STDOUT)

