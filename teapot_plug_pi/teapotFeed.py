import sys
sys.path.append('../')
import json
import time

from deployModels.HLdeployer.communicate import *

with open("./config.json", 'r') as confFile:
    conf = json.load(confFile)["test"]

com = communicate(conf, useTensor = False)

while True:
    #print com.compute([[1, 2]])
    print com.predictFromWeights([1,2])
    time.sleep(5)
