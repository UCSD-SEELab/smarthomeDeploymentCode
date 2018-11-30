import sys
sys.path.append('../../Library/')
import json

from deployModels.HLdeployer.communicate import *

def on_msg_metasense(mosq, obj, msg):
    datum = json.loads(str(msg.payload))
    com.dataDict["MetaSense/nnjson"] = datum["data"][0]
    print ("recieved metasense", com.dataDict["MetaSense/nnjson"])

def on_msg_plug(mosq, obj, msg):
    datum = json.loads(str(msg.payload))
    com.dataDict["teapot_plug_inference"] = datum["data"][0]
    print("recieved plug", com.dataDict["teapot_plug_inference"])

def on_msg_mat(mosq, obj, msg):
    datum = json.loads(str(msg.payload))
    com.dataDict["pressuremat_inference"] = datum["data"][0]
    print("recieved mat", com.dataDict["pressuremat_inference"])

with open("./config.json", 'r') as confFile:
    conf = json.load(confFile)["test"]

com = communicate(conf, [on_msg_metasense, on_msg_mat, on_msg_plug])
com.startListening()
com.predictionLoop()


