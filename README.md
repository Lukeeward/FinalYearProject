# Final year project
---------------------
## Synopsis
When installed onto a linux device, this program can be used as for home security analysing and classifiying live audio.
This program listen to the live audio supplied by a microphone, splits the separate sound segments and classifies them against the testDogx classifier model. 
The results are sent using the PubNub api, which can be received by the supplied mobile app.

## Breakdown
#####

## Dependencies
Installation commands
```
apt-get install python-opencv
apt-get install python-pygame
apt-get install lsof
apt-get install ipython python-opencv python-scipy python-numpy python-setuptools python-pip
apt-get install motion
apt-get install python-pyaudio python3-pyaudio
apt-get install python-dev
apt-get install python3-scipy
apt-get install libchromaprint-dev
apt-get install python-matplotlib 
apt-get install libgsl0-dev 
apt-get install python-sklearn
pip install pubnub
easy_install simplejson
wget http://sourceforge.net/projects/mlpy/files/mlpy%203.5.0/mlpy-3.5.0.tar.gz
tar xvf mlpy-3.5.0.tar.gz
cd mlpy-3.5.0
python setup.py install
apt-get install git
git clone https://github.com/tyiannak/pyAudioAnalysis.git
pip install scikits.talkbox
pip install eyeD3
apt-get install python-netifaces
```
---------------
## Instllation
- Install Dependencies.
- Download 'Project' Folder and place in /home.
  - If placed elsewhere, change path in all scripts.
- Ensure input_device_index is correct in soundProcess.py, line 129.
- Ensure Motion is setup correctly and replace /etc/motion/motion.conf with supplied motion.conf file.
- Change the PubNub API keys to your own.
- Change IonicPush token keys inside PushPythonscript.py to your own. 
  - Or comment out the call in classifySounds.py, line 58.

### Optional
- If using mobile app: set listenforapp.py to run on startup 

--------------
## Running
Run soundProcess.py or set up mobile app to send the ON command.
