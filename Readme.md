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

# How to use the deployModules module

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
