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
    def __init__(self, conf, callbacks = None):
        self.conf = conf
        self.dataDict = OrderedDict()
        self.topics = self.conf['topics']
        self.mqttClient = paho.Client(conf["clientID"])

        if "username" in self.conf.keys():
            self.mqttClient.username_pw_set(conf["username"], conf["pwd"])
        
        self.mqttClient.connect(self.conf["host"],
                self.conf["port"],
                self.conf["keepalive"])

        if callbacks:
            assert len(self.topics) == len(callbacks), "each topic should have a callback"

            for topic,func in zip(self.topics, callbacks):
                self.dataDict[topic] = [2, 3]
                self.mqttClient.message_callback_add(topic, func)
                self.mqttClient.subscribe(topic)

            if 'tensorflow' in sys.modules:
                loadModel.__init__(self, conf)
                
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

            print self.compute([feature_vec])
            time.sleep(3)

    def predictFromWeights(self, inputFeat):
        feature_vec = [str(val) for val in inputFeat]
        callArr = ["./compute"].extend(feature_vec)
        process = subprocess.Popen(callArr, stdout = subprocess.PIPE)
        result, err = process.communicate()
        print (result)
        return json.loads(result)

if __name__ == '__main__':
    with open("./config.json", 'r') as confFile:
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

