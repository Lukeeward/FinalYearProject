import urllib2
import json
import sys

data = {"tokens": ["cmkB9YYsBOQ:APA91bGRp44kVBWNtwMB0GEdxrsl-QWSd3_hblh34HuWVAOjv5YkWtWruVTu8TlAJtpJSz6_bOcdeacT9CC0nHER76kYX0KuEx97u6LKGTh6_H8CRqk4XAJJQubFifWfc5XP2lXknswJ"],"profile": "final","notification": {"title": "Hi","message": "Hello world!","android": {"title": "Home Track","message": "A " + str(sys.argv[1]) + " has been detected!","payload": {"epid": "4d880b4e-040a-4346-b1b9-d1d54a0d7522","start": "1457887182","end": "1457887194"}}}}
url = 'https://api.ionic.io/push/notifications'
req = urllib2.Request(url, json.dumps(data), {'Content-Type': 'application/json'})
req.add_header('Authorization', 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIyYTBkZDliOS00YTBkLTQ5NDUtODM1Yy1lMzUzODI3M2JlZjkifQ.MHCaBPpIGT4jyhDSD_Bx21AYwysnuRkngiitmfBZOfU')
f = urllib2.urlopen(req)
for x in f:
    print(x)
f.close()