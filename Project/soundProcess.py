####
#### Reads audio stream and records audio segments above the threshold into a .wav
#### The file information is then passed to silenceRemoval.py when called.
####

import sys
import pyaudio
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

##Maximum sound level threshold
max_level = 25000
##How many seconds should we wait for new noise
silence_limit = 2
##The max length, in seconds, a single .wax file should be to avoid long classificaiton
max_recording = 300
##Current length in seconds
current_running = 0;
##The recording number
rec_number = 0
##The array of audio bytes to be stored into a .wav
audio_array = []
##The current amount of recorded silence, in seconds.
current_silence = 10000000000000
##The start of the recording
start_time = ''

##Get the devices current IP Address, in order to call a localhost curl script later.
ni.ifaddresses('eth0')
ip = ni.ifaddresses('eth0')[2][0]['addr']
print ip # Should print the current IP

##Process_audio callback receives the current audio byte from the PyAudio Stream
def process_audio(data):
	##Check if the stop script exists, this will be created outside of this script in order to remotely stop the loop
	if os.path.exists('/home/Project/stop-script') :
		#If it exists remove it
		os.remove('/home/Project/stop-script')
		#Exit the script
		sys.exit()
	# Retreive global variables
	global current_silence, audio_array, rec_number, start_time, current_running
	#Should record should be false at the start as the sound byte has yet to be level checked
	should_record = False
	
	##Get the current audio sections max audio level
	level = audioop.max(data, 2)
	#Set the level_char to '.', this is printed to the console allowing visual feedback as to recording
	level_char = u'.'
	#if current level is above the maximum threshold
	if level > max_level:
		#Change level_char to '!' annoucing the audio is above threshold
		level_char = u'!'
		#Reset the current silence
		current_silence = 0
		#Set recording flag to true to start recording
		should_record = True
	else:
		#Otherwise its just silence so set char to '.'
		level_char = u'.'
		#Add increment the current silence
		current_silence = current_silence + 1
		
	##If its been silent longer than should be recorded
	if current_silence <= silence_limit:
		should_record = True 
		
	##If recording should stop and the audio_array contains data
	##Then write to a .wav file with the data
	if (should_record == False and len(audio_array) > 0) or current_running > max_recording:
		#make the directory for that hour
		directory = '/home/Project/wav/%s/' % strftime("%Y-%m-%d_%H")
		if not os.path.isdir(directory):
			os.makedirs(directory)
		#Create the file name for the .wav
		filename = directory + ('%s.wav' % strftime("%Y-%m-%d_%H%M%S"))
		wavefile = wave.open(filename, 'w')
		wavefile.setparams((1, 2, 44100, 44100, 'NONE', 'not compressed'))
		wavefile.writeframes(''.join(audio_array))
		wavefile.close()
		##reset the audio_array
		audio_array = []
		#Change the level char to indecate a recording has taken place
		level_char = u'R'
		#curl the Motion snapshot address in localhost to generate a snapshot
		subprocess.Popen(['curl','-s','-o','/dev/null','http://' + ip + ':8080/0/action/snapshot'])
		##removal silence and split up the wav file
		splitlog = open("/home/Project/splitlog.txt", "w")
		subprocess.Popen(['python','/home/Project/silenceRemoval.py', str(filename), str(rec_number), str(start_time), str(int(time.time()))], stdout=splitlog)
		#Increment the recording number and reset start time and current running length
		rec_number = rec_number + 1
		start_time = ''
		current_running = 0;
	#If data should be recorded save this data in an array
	if should_record:
		#Set the recording start time if its blank
		if start_time == '':
			start_time = int(time.time())
		audio_array.append(data)
		current_running = current_running + 1;
		
	log_level_data(level,level_char)
	sys.stdout.write(level_char)
	sys.stdout.flush()
	
#Log the current recorded level data
def log_level_data(audio_max,the_icon):
	with open("/home/Project/log.txt", "a") as myfile:
		myfile.write(" " + the_icon + str(audio_max))
	
#Read in the audio data stream and pass in_data to process_audio
def read_stream(in_data, frame_count, time_info, status_flags):
	process_audio(in_data)
	return ("", 0)

def print_time():
	da_msg = "\n%s " % (strftime("%Y-%m-%d %H:%M"))
	sys.stdout.write(da_msg)
	sys.stdout.flush()

##Open an audio stream from the device
p = pyaudio.PyAudio()
##Change input_device_index to correct device index
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