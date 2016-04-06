# -*- coding: utf-8 -*-

# Percentage value from 1-100, used to detect noise
##RECORD_SENSITIVITY = 10

##
##
##TODO: limit recording by a max time eg 10 mins
##
##
import sys

try:
  import pyaudio
except ImportError:
  print("pyaudio needs to be installed")
  sys.exit(1)

import wave
import time
import os
import datetime
import json
import subprocess
from time import strftime
from datetime import datetime
import audioop
import netifaces as ni
import sys

##used for getting snapshots
##from SimpleCV import Camera
##cam = Camera()

##Maximum sound level threshold
MAX_LEVEL = 25000
# How many seconds should we wait for new noise
RECORDING_LIMIT = 2
MAX_RECORDING = 300
CURRENT_RUNNING = 0;
RecNumber = 0

audio_bank = []
current_silence = 10000000000000

startTime = ''

ni.ifaddresses('eth0')
ip = ni.ifaddresses('eth0')[2][0]['addr']
print ip  # should print "192.168.100.37"

def callbackfn(m, n):
	print(m)

def process_audio(data):
	if os.path.exists('/home/Project/stop-script') :
		os.remove('/home/Project/stop-script')
		sys.exit()
	global current_silence, audio_bank, RecNumber, startTime, CURRENT_RUNNING
	should_record = False
	
	##Get the current chunks max audio level
	level = audioop.max(data, 2)
	level_char = u'.'
	sys.stdout.write(str(level))
	#if current level is above the maximum threshold
	if level > MAX_LEVEL:
		level_char = u'!'
		current_silence = 0
		should_record = True
	else:
		level_char = u'.'
		current_silence = current_silence + 1
		
	##If its been silent longer than should be recorded
	if current_silence <= RECORDING_LIMIT:
		should_record = True 
		
	##If recording should stop and the audio_bank contains data
	##Then write to a .wav file with the data
	if (should_record == False and len(audio_bank) > 0) or CURRENT_RUNNING > MAX_RECORDING:
		#make the directory for that hour
		directory = '/home/Project/wav/%s/' % strftime("%Y-%m-%d_%H")
		if not os.path.isdir(directory):
			os.makedirs(directory)
		#make filename
		filename = directory + ('%s.wav' % strftime("%Y-%m-%d_%H%M%S"))
		wavefile = wave.open(filename, 'w')
		wavefile.setparams((1, 2, 44100, 44100, 'NONE', 'not compressed'))
		wavefile.writeframes(''.join(audio_bank))
		wavefile.close()
		##reset the audiobank
		audio_bank = []
		level_char = u'R'
		FNULL = open(os.devnull, 'w')
		##take snapshot
		subprocess.Popen(['curl','-s','-o','/dev/null','http://' + ip + ':8080/0/action/snapshot'])
		##removal silence and split up the wav file
		f = open("/home/Project/blah.txt", "w")
		subprocess.Popen(['python','/home/Project/silenceRemoval.py', str(filename), str(RecNumber), str(startTime), str(int(time.time()))], stdout=f)
		print(str(startTime))
		print(str(int(time.time())))
		RecNumber = RecNumber + 1
		startTime = ''
		CURRENT_RUNNING = 0;
	##If data should be recorded save this data in an array
	if should_record:
		#record audio data to bank
		if startTime == '':
			startTime = int(time.time())
		audio_bank.append(data)
		CURRENT_RUNNING = CURRENT_RUNNING + 1;
		
	log_level_data(level,level_char)
	sys.stdout.write(level_char)
	sys.stdout.flush()

def log_level_data(audio_max,the_icon):
	with open("/home/Project/log.txt", "a") as myfile:
		myfile.write(" " + the_icon + str(audio_max))
	

def read_stream(in_data, frame_count, time_info, status_flags):
	process_audio(in_data)
	return ("", 0)

def print_time():
	da_msg = "\n%s " % (strftime("%Y-%m-%d %H:%M"))
	sys.stdout.write(da_msg)
	sys.stdout.flush()

	##main stream processing
p = pyaudio.PyAudio()
##count = p.get_device_count()
##for i in range(count):
	##print(p.get_device_info_by_index(i))
stream = p.open(
	format = pyaudio.paInt16,
	channels = 1,
	rate =  44100,
	frames_per_buffer = 44100,
	stream_callback = read_stream,
	input = True,
	input_device_index = 1
	)


last_second = 0
print_time()
while stream.is_active():
	time.sleep(1)
	if strftime("%S") < last_second:
		print_time()
	last_second = strftime("%S")


stream.close()
p.terminate()