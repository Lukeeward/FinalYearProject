#from scipy.io.wavfile import read
#import numpy as np

#a = read("testbarks.wav")
#x = np.array(a[1])
#w = np.fft.fft(x)
#freqs = np.fft.fftfreq(len(w))
#print(w)
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

from pyAudioAnalysis import audioTrainTest as aT
aT.featureAndTrain(["/home/Project/train/Dog","/home/Project/train/Man","/home/Project/train/Clatter","/home/Project/train/Bang", "/home/Project/train/Lownoise"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "knn", "testDogy", False)
#Clatter short
#test = aT.fileClassification("/home/Project/train/Clatter/clatter3.wav", "testDogx","knn")
#print("Expected: Clatter")
#print(test)
#Loud door knock
#test = aT.fileClassification("/home/Project/train/Clatter/2016-03-13_1341393.wav", "testDogx","knn")
#print("Expected: Clatter")
#print(test)
#Dropping on hard floor
#test = aT.fileClassification("/home/Project/train/Clatter/2016-01-14_1013132.wav", "testDogx","knn")
#print("Expected: Clatter")
#print(test)
#Bang, short thud
#test = aT.fileClassification("/home/Project/train/Bang/2016-01-13_0909361.wav", "testDogx","knn")
#print("Expected: Bang")
#print(test)
#Bang, Watery hit 
#test = aT.fileClassification("/home/Project/train/Bang/2016-01-14_1012051.wav", "testDogx","knn")
#print("Expected: Bang")
#print(test)
##Distant thud
#test = aT.fileClassification("/home/Project/train/Bang/2016-01-13_1034023.wav", "testDogx","knn")
#print("Expected: Bang")
#print(test)
# test = aT.fileClassification("../shortBark.wav", "../testDog","knn")
# print("Short Barks:")
# print(test)