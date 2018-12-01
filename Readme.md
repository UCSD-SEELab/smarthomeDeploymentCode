# Deploying Hierarchical Models

This repository contains the code for deploying the pretrained hierarchical models on the 
various devices. The repo is divided into 2 folders:
- Library
- HomeDeployment

The Library holds a python module which we wrote for making deployment easier. The 
library contains 2 submodules.

```
/deployModels
	/communicate - Handles the mqtt messaging, makes use of loadModel to predict and 
	send the result to the next layer
	/loadModel - Handles loading the frozen tensorflow modules and produces the output
```
# Installation
# How to use the deployModules module

## Configuration

The first step in using the module is to write a config file which tells the library the
configuration parameters for the mqtt host, port and other relevant information. The 
different fields are given below. Some of the fileds are mandatory while others are 
optional depending on the functionality desired

```
{
	<name of config>: {
		"host": <hostaddress of the broker>,
		"port": <port on which the broker is listening - usually 1883 for mqtt>,
		"keepalive": <keepalive time for mqtt server>,
		"username": <username - login credential for the broker>,
		"pwd": <password for the broker>,
		"topics": <List of topics to which the mqtt client need to subscribe to>,
		"clientID": <clientId of the client - can be assigned manually or autoamted>,
		"sensor": <the sensor name - or the frozen model name>,
		"numInputs": <number of features per sensor/topic - used for initialization>,
		"outputTopic": <the mqtt Topic to which the partial inference should be sent to>,
		"modelDir": <path to the folder where the frozen models are located at> 
	}
}
```

The below table shows which fields are mandatory and their use


Name of Field | Mandatory | Usage
------------- | --------- | -----
host | Yes | Host address
port | Yes | Port on which mqtt host listens on
keepalive | Yes | keepalive value for mqtt server
username | Optional | If the host requires credentials then username needs to be suplied
pwd | Optional | Used if host requires login credentials
topics | Optional | Topics need to be listed, if the mqtt client needs to subscribe for any particular topic. In our architecture, for simplicity, we do not configure point to point communication between the devices in different hierarchy. Instead we use a common message bus on which every device communicate. We partition the hierarchy by configuring each device to subscribe only to those topics that it requires access to.
clientID | Yes | Each node communicating must have a unique clientID
sensor | Yes | This field is used to load the frozen module. The frozen model for each node is of the form <sensor>_frozen.pb. 
numInputs | Yes | This field indicates the number of features for each topic that is subscribed to. This is used for initialization internally.
outputTopic | Yes | This is the topic to which the processed data must be sent to on the broker.
modelDir | Yes | This is the path to the folder in which the frozen models are stored in

## Functions Provided

This section briefly describes the various functionality available in both the classes

### loadModel

The loadModel class is for simply loading the frozen model and performing inference using that model. It takes the input and config file, and loads the corresponding model file as specified by the config. It then performs inference and returns the value.

Example:
```
import json
with open("config.json") as fp:
	conf = json.load(fp)

model = loadModel(conf) #initialize model by passing the config file
#The compute function takes a 2D array as input where each row is a feature vector and returns the output which is the partial inference from the model
result = model.compute([[2.0, 3.0]]) 
print result
# [[[-0.30995443  0.3088935 ]]]
```



https://github.com/j05h/hs100
