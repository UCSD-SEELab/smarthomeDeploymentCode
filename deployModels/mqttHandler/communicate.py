import paho.mqtt.client as paho
import json

class communicate():
    def __init__(self, conf, callbacks):

        self.conf = conf
        self.topics = self.conf['topics']
        self.mqttClient = paho.Client(conf["clientID"])
        if "username" in self.conf.keys():
            self.mqttClient.username_pw_set(conf["username"], conf["pwd"])
        
        self.mqttClient.connect(self.conf["host"],
                self.conf["port"],
                self.conf["keepalive"])
        assert len(self.topics) == len(callbacks), "each topic should have a callback"

        for topic,func in zip(self.topics, callbacks):
            self.mqttClient.message_callback_add(topic, func)
            self.mqttClient.subscribe(topic)

    def sendData(self, topic, msg):
        self.mqttClient.publish(topic, msg)

    def startListening(self):
        self.mqttClient.loop_start()

    def stopListening(self):
        self.mqttClient.loop_stop()

if __name__ == '__main__':
    with open("./config.json", 'r') as confFile:
        conf = json.load(confFile)["local"]
    def blah(mosq, obj, msg):
        print(str(msg.payload))

    test = communicate(conf, [blah])
    test.sendData("crk", str("testing mqtt"))
    print("starting mqtt loop")
    test.startListening()
    import time
    time.sleep(5)
    print("Exiting")
    test.stopListening()

