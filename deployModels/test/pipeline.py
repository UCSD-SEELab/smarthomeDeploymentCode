from deployModels.HLdeployer.communicate import *
import json

def blah(mosq, obj, msg):
    print(str(msg.payload))
    

with open("./config.json", 'r') as confFile:
    conf = json.load(confFile)["local"]

ab = communicate(conf, [blah])
ab.sendData("crk", str(12))
ab.startListening()
while True:
    pass
