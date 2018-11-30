import sys
sys.path.append('../../Library/')
import json

from deployModels.HLdeployer.communicate import *

def on_msg_tvplug(mosq, obj, msg):
    datum = json.loads(str(msg.payload))
    com.dataDict["tv_plug_inference"] = datum["data"][0]
    print ("recieved tv plug", com.dataDict["tv_plug_inference"])

with open("./config.json", 'r') as confFile:
    conf = json.load(confFile)["test"]

com = communicate(conf, [on_msg_tvplug])
com.startListening()
com.predictionLoop()


