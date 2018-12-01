import sys
sys.path.append('../../Library/')
import json

from deployModels.HLdeployer.communicate import *

def on_msg_kitchen(mosq, obj, msg):
    datum = json.loads(str(msg.payload))
    com.dataDict["kitchen_inference"] = datum["data"][0]
    print ("recieved kitchen", com.dataDict["MetaSense_inference"])

def on_msg_livingroom(mosq, obj, msg):
    datum = json.loads(str(msg.payload))
    com.dataDict["livingroom_inference"] = datum["data"][0]
    print("recieved livingroom", com.dataDict["livingroom_inference"])

def on_msg_smartthings(mosq, obj, msg):
    datum = json.loads(str(msg.payload))
    com.dataDict["smartthings_inference"] = datum["data"][0]
    print("recieved mat", com.dataDict["smartthings_inference"])

def on_msg_watch(mosq, obj, msg):
    datum = json.loads(str(msg.payload))
    com.dataDict["watch/nnjson"] = datum["data"][0]
    print("recieved watch", com.dataDict["watch/nnjson"])

def on_msg_localization(mosq, obj, msg):
    datum = json.loads(str(msg.payload))
    com.dataDict["localization_inference"] = datum["data"][0]
    print("recieved localization", com.dataDict["localization_inference"])

with open("./config.json", 'r') as confFile:
    conf = json.load(confFile)["test"]

com = communicate(conf, [on_msg_kitchen, on_msg_livingroom, on_msg_smartthings, on_msg_watch, on_msg_localization])
com.startListening()
com.predictionLoop()


