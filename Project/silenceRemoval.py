#Splits each noise event into its separate noise peaks, removing the silences
#each split wav file can then be classified as to the noise

import pyaudio
import wave
import sys
import time
import audioop
import os
from time import strftime
import subprocess

SilenceThreshold = 6000
audio_bank = []
SilenceLimit = 3
CurrentSilence = 0
WavSplit = 0
CHUNK = 1024
directory = ''
wavFile = wave.open(sys.argv[1],'rb')

##sys.argv = filename, recnumber, starttime, endtime

def removeSilence(data):
	global CurrentSilence, WavSplit, directory
	isNotSilent = True
	level = audioop.max(data, 2)
	if level < SilenceThreshold:
		print("silent" + str(CurrentSilence))
		CurrentSilence = CurrentSilence + 1
		isNotSilent = False
		
	if CurrentSilence >=  SilenceLimit and audio_bank:
		if len(audio_bank) >= 10:
			print("making dat ting" + str(len(audio_bank)))
			directName = str(sys.argv[2]) + ('%s' % strftime("%d_%H"))
			directory = '/home/Project/split/' + directName
			if not os.path.isdir(directory):
				os.makedirs(directory)
			filename = directory + ('/%s.wav' % (strftime("%Y-%m-%d_%H%M%S") + str(WavSplit)))
			newFile = wave.open(filename, 'w')
			newFile.setparams((1, 2, 44100, 44100, 'NONE', 'not compressed'))
			newFile.writeframes(''.join(audio_bank))
			newFile.close()
		WavSplit = WavSplit + 1
		CurrentSilence = 0
		del audio_bank[:]
		
	if level > SilenceThreshold:
		print(level)
		audio_bank.append(data)
		
		
def callback(in_data, frame_count, time_info, status):
	data = wavFile.readframes(frame_count)
	removeSilence(data)
	return (data, pyaudio.paContinue)
	
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
FNULL = open(os.devnull, 'w')
tt = subprocess.Popen(['python','/home/Project/classifySounds.py', str(directory), sys.argv[3], sys.argv[4]],stdout=FNULL, stderr=subprocess.STDOUT)

