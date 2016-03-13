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
#aT.featureAndTrain(["/home/Project/train/Dog","/home/Project/train/Man","/home/Project/train/Clatter","/home/Project/train/Bang", "/home/Project/train/Lownoise"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "knn", "testDogx", False)
test = aT.fileClassification("/home/Project/split/113_16/2016-03-13_1627364.wav", "testDogx","knn")
print("Bark1")
print(test)
test = aT.fileClassification("/home/Project/split/113_16/2016-03-13_1627342.wav", "testDogx","knn")
print("Bark2")
print(test)
test = aT.fileClassification("/home/Project/split/113_16/2016-03-13_1627321.wav", "testDogx","knn")
print("No Bark")
print(test)
#print(test[1])
#test = aT.fileClassification("../shortBark.wav", "../testDog2","knn")
#print("Short Barks:")
#print(test)
#test = aT.fileClassification("/home/pi/Documents/Classified/man/01.wav", "../testDog2","knn")
#print("No Bark:")
#print(test)
#test = aT.fileClassification("../testw.wav", "../testDog2","knn")
#print("nil Barks:")
#print(test)
# test = aT.fileClassification("../shortBark.wav", "../testDog","knn")
# print("Short Barks:")
# print(test)