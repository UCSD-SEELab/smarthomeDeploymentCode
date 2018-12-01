import sys
from collections import OrderedDict
import paho.mqtt.client as paho
import json
import time
import subprocess

try:
    __import__('tensorflow')
except ImportError:
    class loadModel():
        pass
else:
    from loadModel import *

class communicate(loadModel):
    def __init__(self, conf, callbacks = None, useTensor = True):
        self.conf = conf
        self.dataDict = OrderedDict()
        self.topics = self.conf['topics']
        self.outputTopic = conf['outputTopic']
        self.mqttClient = paho.Client(conf["clientID"])

        if "username" in self.conf.keys():
            self.mqttClient.username_pw_set(conf["username"], conf["pwd"])
        
        self.mqttClient.connect(self.conf["host"],
                self.conf["port"],
                self.conf["keepalive"])

        if callbacks:
            assert len(self.topics) == len(callbacks), "each topic should have a callback"

            for topic,func in zip(self.topics, callbacks):
                self.dataDict[topic] = [0.0] * conf["numInputs"]
                self.mqttClient.message_callback_add(topic, func)
                self.mqttClient.subscribe(topic)

        if useTensor:
            if 'tensorflow' in sys.modules:
                loadModel.__init__(self, conf)
            else:
                print("error Tensorflow not installed")
                exit()
        else:
            self.modelDir = conf["modelDir"].strip(".")
            self.outputVal = [0] * conf["outputLength"]
            subprocess.call(["make", "-C", conf["modelDir"]])
                
    def sendData(self, topic, msg):
        self.mqttClient.publish(topic, msg)

    def sendStoredData(self, topic):
        self.mqttClient.publish(topic, self.dataDict[topic])

    def startListening(self):
        self.mqttClient.loop_start()

    def stopListening(self):
        self.mqttClient.loop_stop()

    def predictionLoop(self):
        while True:
            feature_vec = []
            for key, vals in self.dataDict.items():
                feature_vec = feature_vec + vals

            result = self.compute([feature_vec])[0]
            print (self.compute([feature_vec]))
            self.sendData(self.outputTopic, "{data:" + str(result) +"}") 
            time.sleep(3)

    def predictFromWeights(self, inputFeat):
        feature_vec = [str(val) for val in inputFeat]
        callArr = ["." + self.modelDir + "compute"] + feature_vec
        process = subprocess.Popen(callArr, stdout = subprocess.PIPE)
        result, err = process.communicate()
        print (result)
        self.sendData(self.outputTopic, "{data:" + str(result) +"}") 
        return json.loads(result)

if __name__ == '__main__':
    with open("../test/config.json", 'r') as confFile:
        conf = json.load(confFile)["local"]

    def blah(mosq, obj, msg):
        datum = json.loads(str(msg.payload))
        print (datum)
        test.dataDict["crk"] = datum["data"][0]
        print(test.dataDict["crk"])

    test = communicate(conf, [blah])
    test.startListening()
    #test.sendData("crk", str("[5.0, 9.0]"))
    #import time
    #time.sleep(5)
    #print("Exiting")
    #test.stopListening()
    test.predictionLoop()

