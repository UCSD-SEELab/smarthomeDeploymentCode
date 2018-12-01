import sys
sys.path.append('../../Library/')
import json
import time
from hs100 import core
import numpy as np

from deployModels.HLdeployer.communicate import *

with open("./config.json", 'r') as confFile:
    conf = json.load(confFile)["test"]

com = communicate(conf)
plug = core.Core('192.168.1.8', 9999, False)
plugBuf = [0.0] * 3
counter = 0

while True:
    plugReading = plug.request('meter')['emeter']['get_realtime']
    plugBuf[counter] = plugReading['current']
    counter = (counter + 1) % 3
    feat1 = (np.mean(plugBuf) - 0.147135305) / 0.31036106
    feat2 = (np.var(plugBuf) - 0.0036457) / 0.0285838
    result = com.compute([[feat1, feat2]])[0]
    com.sendData(conf["outputTopic"], "{data: " + str(result) + "}")
    #print com.predictFromWeights([1,2])
    time.sleep(5)
