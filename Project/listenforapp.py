from pubnub import Pubnub
import json
import os
import subprocess
import netifaces as ni

FNULL = open(os.devnull, 'w')

#Get device IP
ip = ni.ifaddresses('eth0')[2][0]['addr']

#Initalise the variable
f = open('/home/Project/classifer','w')
f.write('testDogx')
f.close()

#Set up PubNub
pubnub = Pubnub(
    publish_key = "pub-c-92b5e647-0c49-49a1-ab2a-4753777f53b9",
    subscribe_key = "sub-c-02de9d80-9a93-11e5-9a49-02ee2ddab7fe")
channel = "commands"

def callback(message, channel):
	command = (message['command'])
	##HomeTracker
	#stop video
	if command == "motionstop":
		print("stopping motion")
		open('/home/Project/stop-script', 'a').close()
		subprocess.Popen(['start-stop-daemon', '--stop', '--name', 'motion'],stdout=FNULL, stderr=subprocess.STDOUT)
		dirPath = "/var/lib/motion"
		fileList = os.listdir(dirPath)
		for fileName in fileList:
			os.remove(dirPath+"/"+fileName)
	
	#start video
	if command == "motionstart":
		print("starting motion")
		if os.path.exists('/home/Project/stop-script') :
			os.remove('/home/Project/stop-script') 
			print('removing')
		subprocess.Popen(['python', '/home/Project/soundProcess.py'])
		subprocess.Popen(['motion'],stdout=FNULL, stderr=subprocess.STDOUT)
	##motion
	#stop motion detection
	if command == "detectionstop":
		print("stopping detection")
		subprocess.Popen(['curl','-s','-o','/dev/null','http://' + ip + ':8080/0/detection/pause'])
		
	#start motion detection
	if command == "detectionstart":
		print("starting detection")
		subprocess.Popen(['curl','-s','-o','/dev/null','http://' + ip + ':8080/0/detection/start'])
		
	##system
	#Switch off device
	if command == "off":
		print("shutting down")
		subprocess.Popen(['shutdown', '-h', 'now'])
		
	##Change classification
	if command == "dog":
		print("Dog, changing classifer")
		f = open('/home/Project/classifer','w')
		f.write('testDogx') # python will convert \n to os.linesep
		f.close()
		#subprocess.Popen(['shutdown', '-h', 'now'])
		
	if command == "nodog":
		print("No Dog, changing classifer")
		f = open('/home/Project/classifer','w')
		f.write('noDogy') # python will convert \n to os.linesep
		f.close()
		#subprocess.Popen(['shutdown', '-h', 'now'])
	
	
pubnub.subscribe(
	channel,
	callback = callback)