####
#### Splits each noise event into its separate noise peaks, removing the silences
#### each split wav file can then be classified.
####

import pyaudio
import wave
import sys
import time
import audioop
import os
from time import strftime
import subprocess

## The maximum audio level threshold
SilenceThreshold = 6000
## The array of audio bytes to be stored in a .wav
audio_array = []
## The Max silence length
SilenceLimit = 3
## The current silence length 
CurrentSilence = 0
## The amount of new wav files split from the original
WavSplit = 0
## The initialised directory
directory = ''
## The supplied original .wav file from soundProcess.py
wavFile = wave.open(sys.argv[1],'rb')

##sys.argv = filename, recnumber, starttime, endtime

## Each audio segment is passed as 'data', if above the threshold the data is stored in a .wav
def removeSilence(data):
	# Get global variables
	global CurrentSilence, WavSplit, directory
	# Get max audio level for segment
	level = audioop.max(data, 2)
	# If the max level is below the threshold the silence counter is incremented
	if level < SilenceThreshold:
		CurrentSilence = CurrentSilence + 1
	# If the current silence is above the limit for silence
	if CurrentSilence >=  SilenceLimit and audio_array:
		# If the current audio array length is below 10 (seconds)
		if len(audio_array) >= 10:
			# Generate new .wav directory path
			directName = str(sys.argv[2]) + ('%s' % strftime("%d_%H"))
			directory = '/home/Project/split/' + directName
			if not os.path.isdir(directory):
				os.makedirs(directory)
			# Create new .wav file containing current array data
			filename = directory + ('/%s.wav' % (strftime("%Y-%m-%d_%H%M%S") + str(WavSplit)))
			newFile = wave.open(filename, 'w')
			newFile.setparams((1, 2, 44100, 44100, 'NONE', 'not compressed'))
			newFile.writeframes(''.join(audio_array))
			newFile.close()
		# Increment wavsplit counter and reset variables
		WavSplit = WavSplit + 1
		CurrentSilence = 0
		del audio_array[:]
	# If the current level is above the threshold then append the array
	if level > SilenceThreshold:
		audio_array.append(data)
		
# PyAudio stream callback, passing the audio data bytes to removeSilence
def callback(in_data, frame_count, time_info, status):
	data = wavFile.readframes(frame_count)
	removeSilence(data)
	return (data, pyaudio.paContinue)
	
# Open a new audio stream from the original supplied .wav
p = pyaudio.PyAudio()
stream = p.open(
				format=p.get_format_from_width(wavFile.getsampwidth()),
                channels=wavFile.getnchannels(),
                rate=wavFile.getframerate(),
                output=True,
                stream_callback=callback
	)

stream.start_stream()

while stream.is_active():
    time.sleep(0.1)
	
stream.stop_stream()
stream.close()
wavFile.close()
p.terminate()
## When .wav has finished being read call the classify script 
## passing the directory of the split files and episode information
FNULL = open(os.devnull, 'w')
tt = subprocess.Popen(['python','/home/Project/classifySounds.py', str(directory), sys.argv[3], sys.argv[4]],stdout=FNULL, stderr=subprocess.STDOUT)

