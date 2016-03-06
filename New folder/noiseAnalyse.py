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
#aT.featureAndTrain(["/home/pi/Documents/Classified/Dog","/home/pi/Documents/Classified/person","/home/pi/Documents/Classified/clatter","/home/pi/Documents/Classified/frantic"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "knn", "testDog3", False)
#test = aT.fileClassification("../scottish.wav", "../knnSM","knn")
#print(test)
#test = aT.fileClassification("../scottish.wav", "../testDog2","knn")
#print("No Bark:")
#print(test)
test = aT.fileClassification("/home/pi/Documents/wav/2015-12-16_13/2015-12-16_133050.wav", "/home/pi/Documents/testDog3","knn")
#print("Several Barks:")
print(test)
print(test[1])
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