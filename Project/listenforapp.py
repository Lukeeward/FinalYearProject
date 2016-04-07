####
#### Run at device startup
#### The script stays listening on the PubNub channel and responds to the specific commands
####

from pubnub import Pubnub
import json
import os
import subprocess
import netifaces as ni

FNULL = open(os.devnull, 'w')

#Get device IP
ip = ni.ifaddresses('eth0')[2][0]['addr']

#Initialise the variable
f = open('/home/Project/classifer','w')
f.write('testDogx')
f.close()

#Set up PubNub
pubnub = Pubnub(
    publish_key = "pub-c-92b5e647-0c49-49a1-ab2a-4753777f53b9",
    subscribe_key = "sub-c-02de9d80-9a93-11e5-9a49-02ee2ddab7fe")
channel = "commands"

def callback(message, channel):
	# Get the command string
	command = (message['command'])
	
	#Stop Motion and soundProcess.py
	if command == "motionstop":
		print("stopping motion")
		# Create the stop-script file
		# When noticed in the soundProcess.py loop it will cause it to exit
		open('/home/Project/stop-script', 'a').close()
		# Stop the Motion daemon
		subprocess.Popen(['start-stop-daemon', '--stop', '--name', 'motion'],stdout=FNULL, stderr=subprocess.STDOUT)
		# Clear the folders to avoid over filling memory
		dirPath = "/var/lib/motion"
		fileList = os.listdir(dirPath)
		for fileName in fileList:
			os.remove(dirPath+"/"+fileName)
			
		dirPath = "/home/Project/wav"
		fileList = os.listdir(dirPath)
		for fileName in fileList:
			filedirList = os.listdir(dirPath+"/"+fileName)
			for files in filedirList:
				os.remove(dirPath+"/"+fileName+"/"+files)
			os.rmdir(dirPath+"/"+fileName)
			
		dirPath = "/home/Project/split"
		fileList = os.listdir(dirPath)
		for fileName in fileList:
			filedirList = os.listdir(dirPath+"/"+fileName)
			for files in filedirList:
				os.remove(dirPath+"/"+fileName+"/"+files)
			os.rmdir(dirPath+"/"+fileName)
	
	# Start motion and soundProcess.py
	if command == "motionstart":
		print("starting motion")
		# Remove the stop-script if it exists, otherwise soundProcess will not start
		if os.path.exists('/home/Project/stop-script') :
			os.remove('/home/Project/stop-script') 
		# Start soundProcess.py
		subprocess.Popen(['python', '/home/Project/soundProcess.py'])
		# Start Motion daemon
		subprocess.Popen(['motion'],stdout=FNULL, stderr=subprocess.STDOUT)

	# Pause the motion detection
	if command == "detectionstop":
		print("stopping detection")
		# curl to the motion pause address in localhost
		subprocess.Popen(['curl','-s','-o','/dev/null','http://' + ip + ':8080/0/detection/pause'])
		
	# Start the motion detection
	if command == "detectionstart":
		print("starting detection")
		# curl to the motion start address in localhost
		subprocess.Popen(['curl','-s','-o','/dev/null','http://' + ip + ':8080/0/detection/start'])
		
	# Switch of the entire device
	if command == "off":
		print("shutting down")
		# Initiate the shutdown command
		subprocess.Popen(['shutdown', '-h', 'now'])
		
	# Change the classifer file used in classifySounds.py
	if command == "dog":
		print("Dog, changing classifer")
		# Write the new classifer name into the classifer file
		f = open('/home/Project/classifer','w')
		f.write('testDogx')
		f.close()
		
	# Change the classifer file used in classifySounds.py
	if command == "nodog":
		print("No Dog, changing classifer")
		# Write the new classifer name into the classifer file
		f = open('/home/Project/classifer','w')
		f.write('noDogy')
		f.close()
	
# Subscribe to the PubNub command channel
pubnub.subscribe(
	channel,
	callback = callback)