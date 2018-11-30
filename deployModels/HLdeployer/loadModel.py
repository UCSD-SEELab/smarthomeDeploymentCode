import tensorflow as tf
from tensorflow.python.framework import tensor_util
import numpy as np

class loadModel():
    def __init__(self, conf):
        assert "sensor" in conf.keys(), "Sensor name needs to be given"
        assert "modelDir" in conf.keys(), "Unable to find Model directory"

        self.sensorName = conf["sensor"]
        self.modelDir = conf["modelDir"]
        with open(conf["modelDir"] + "variable_list.txt") as fp:
            self.variableList = eval(fp.read())
        self.frozenModel = self.modelDir + conf["sensor"] + "_frozen.pb"
        self.sess = tf.Session()
        self.graph_def = tf.GraphDef()
        self.loadGraph()

    def loadGraph(self):
        with tf.gfile.GFile(self.frozenModel, "r") as f:
            self.graph_def.ParseFromString(f.read())

    def load_frozen_model(self, sensor_input):
        if type(sensor_input) is not np.ndarray:
            sensor_input = np.array(sensor_input)

        new_input = tf.placeholder(tf.float32, [None, sensor_input.shape[1]], self.sensorName)
        keep_prob = tf.placeholder(tf.float32)
    
        variable_name = self.sensorName + "_output"
        for idx, var in enumerate(self.variableList):
            if variable_name in var:
                variable_name = var
                break
    
        output = tf.import_graph_def(
            self.graph_def,
            input_map={"input/" + self.sensorName+":0": new_input, "input/keepprob:0": keep_prob},
            return_elements = [variable_name+":0"]
        )
            
        results = self.sess.run(output, feed_dict={new_input: sensor_input, keep_prob : 1.0})

        return results

    def compute(self, inputData):
        return self.load_frozen_model(inputData)


    
if __name__=="__main__":
    import json
    with open("../test/config.json") as fp:
        conf = json.load(fp)

    model = loadModel(conf)
    res = model.compute([[2, 3]])
    print(res)
    
