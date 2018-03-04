from numpy import *
import numpy as np
from numpy import random
import matplotlib.pyplot as plt

def loadData(fileA):
    trainMat=[]
    fr=open(fileA)
    Date=[]
    for line in  fr.readlines():
        curLine=line.strip().split(',')
        trainMat.append(map(float,curLine))
    return mat(trainMat)
def sigmoid(inX):
    return 1.0/(1+exp(-inX))
def normalize(data):
    max1 = np.max(data, axis = 0)
    min1 = np.min(data, axis = 0)
    m1 = max1 - min1
    if np.min(np.array(m1)[0], axis = 0) == 0:
        return data
    else:
        return (data - min1) / m1

class NeuralNetwork(object):
    def __init__(self, input_nodes, hidden1_nodes,hidden2_nodes,hidden3_nodes, output_nodes, learning_rate):
        # Set number of nodes in input, hidden and output layers.
        self.input_nodes = input_nodes
        self.hidden1_nodes = hidden1_nodes
        self.hidden2_nodes=hidden2_nodes
        self.hidden3_nodes=hidden3_nodes
        self.output_nodes = output_nodes

        # Initialize weights
        #self.weights_input_to_hidden1=mat([[0.2,0.4,-0.5,-0.4],[-0.3,0.1,0.2,0.2]])
        self.weights_input_to_hidden1=np.random.normal(size=(hidden1_nodes,input_nodes))
        self.weights_hidden1_to_hidden2=np.random.normal(size=(hidden2_nodes,hidden1_nodes+1))
        self.weights_hidden2_to_hidden3=np.random.normal(size=(hidden3_nodes,hidden2_nodes+1))
        self.weights_hidden3_to_output =np.random.normal(size=(output_nodes,hidden3_nodes+1))
        '''
        self.weights_input_to_hidden1 =random.randint(0,1000,size=(hidden1_nodes,input_nodes))
        self.weights_input_to_hidden1=self.weights_input_to_hidden1*1.0/1000
        
        self.weights_hidden1_to_hidden2=random.randint(0,1000,size=(hidden2_nodes,hidden1_nodes+1))
        self.weights_hidden1_to_hidden2=self.weights_hidden1_to_hidden2*1.0/1000
        
        self.weights_hidden2_to_hidden3=random.randint(0,1000,size=(hidden3_nodes,hidden2_nodes+1))
        self.weights_hidden2_to_hidden3=self.weights_hidden2_to_hidden3*1.0/1000
        #self.weights_hidden2_to_output =mat([-0.3,-0.2,0.1])
        self.weights_hidden3_to_output =random.randint(0,1000,size=(output_nodes,hidden3_nodes+1))
        self.weights_hidden3_to_output=self.weights_hidden3_to_output*1.0/1000
        '''
        self.lr = learning_rate
        
        self.activation_function = sigmoid
    
    def train(self, inputs_list,iterator=10):
        # Convert inputs list to 2d array
        inputs = inputs_list[:,:-1]
        inputs=normalize(inputs)
        inputs= np.column_stack((inputs,ones((shape(inputs)[0],1))))
        targets =inputs_list[:,-1]
        cnt=0
        pred=[]
        for it in range(iterator):
            print it
            ax.append(it)
            hidden1_inputs = self.weights_input_to_hidden1*inputs.T # signals into hidden layer)
            hidden1_outputs =self.activation_function(hidden1_inputs) # signals from hidden layer
            hidden1_outputs=np.row_stack((hidden1_outputs,ones((1,shape(hidden1_outputs)[1]))))
            
            hidden2_inputs=self.weights_hidden1_to_hidden2*hidden1_outputs
            hidden2_outputs=self.activation_function(hidden2_inputs)
            hidden2_outputs=np.row_stack((hidden2_outputs,ones((1,shape(hidden2_outputs)[1]))))
            
            hidden3_inputs=self.weights_hidden2_to_hidden3*hidden2_outputs
            hidden3_outputs=self.activation_function(hidden3_inputs)
            hidden3_outputs=np.row_stack((hidden3_outputs,ones((1,shape(hidden3_outputs)[1]))))

            final_inputs =self.weights_hidden3_to_output*hidden3_outputs# signals into final output layer
            final_outputs =final_inputs # signals from final output layer
            # Output error
            output_errors =(targets.T-final_outputs) # Output layer error is the difference between desired target and actual output.)
            cnt=output_errors*output_errors.T
            mse=np.sqrt(cnt*1.0/len(inputs_list))
            '''
            if np.sqrt(cnt*1.0/len(inputs_list))>100:
                self.lr=0.01
            if np.sqrt(cnt*1.0/len(inputs_list))<100:
                self.lr=0.007
            if np.sqrt(cnt*1.0/len(inputs_list))<90:
                self.lr=0.005#8
            if np.sqrt(cnt*1.0/len(inputs_list))<80:
                self.lr=0.004
            if np.sqrt(cnt*1.0/len(inputs_list))<75:
                self.lr=0.003
            if np.sqrt(cnt*1.0/len(inputs_list))<60:
                self.lr=0.002
            '''
            if mse < 90:
                self.lr = 0.008
            if mse < 80:
                self.lr = 0.007
            if mse < 70:
                self.lr = 0.006
            if mse < 60:
                self.lr = 0.003
            if mse < 50:
                self.lr = 0.002
            print "cur:", mse
            ay.append(mse.tolist()[0])
            if it==iterator-1:
                pred.append(final_outputs)

            EW2=self.weights_hidden3_to_output[:,:-1].T*output_errors
            der2=multiply(hidden3_outputs,1-hidden3_outputs)[:-1,:]
            hidden2_errors=multiply(der2,EW2)
            
            EW1=self.weights_hidden2_to_hidden3[:,:-1].T*hidden2_errors
            der1=multiply(hidden2_outputs,1-hidden2_outputs)[:-1,:]
            hidden1_errors=multiply(der1,EW1)
            
            EW0=self.weights_hidden1_to_hidden2[:,:-1].T*hidden1_errors
            der0=multiply(hidden1_outputs,1-hidden1_outputs)[:-1,:]
            hidden_errors=multiply(EW0,der0)
            
            hidden2_grad=output_errors*hidden3_outputs.T
            hidden1_grad=hidden2_errors*hidden2_outputs.T
            hidden0_grad=hidden1_errors*hidden1_outputs.T
            input_grad=hidden_errors*inputs

            self.weights_hidden3_to_output+=self.lr*hidden2_grad/len(inputs)
            self.weights_hidden2_to_hidden3+=self.lr*hidden1_grad/len(inputs)
            self.weights_hidden1_to_hidden2+=self.lr*hidden0_grad/len(inputs)
            self.weights_input_to_hidden1 +=self.lr*input_grad/len(inputs)
        return cnt,pred
    
    def run(self, inputs_list):
        inputs = inputs_list
        inputs=normalize(inputs)
        inputs= np.column_stack((inputs,ones((shape(inputs)[0],1))))
        hidden1_inputs = self.weights_input_to_hidden1*inputs.T # signals into hidden layer)
        hidden1_outputs =self.activation_function(hidden1_inputs) # signals from hidden layer
        hidden1_outputs=np.row_stack((hidden1_outputs,ones((1,shape(hidden1_outputs)[1]))))
        
        hidden2_inputs=self.weights_hidden1_to_hidden2*hidden1_outputs
        hidden2_outputs=self.activation_function(hidden2_inputs)
        hidden2_outputs=np.row_stack((hidden2_outputs,ones((1,shape(hidden2_outputs)[1]))))
        
        hidden3_inputs=self.weights_hidden2_to_hidden3*hidden2_outputs
        hidden3_outputs=self.activation_function(hidden3_inputs)
        hidden3_outputs=np.row_stack((hidden3_outputs,ones((1,shape(hidden3_outputs)[1]))))

        final_inputs =self.weights_hidden3_to_output*hidden3_outputs# signals into final output layer
        final_outputs =final_inputs
        return final_outputs
trainMat=loadData('processed_train_del.csv')
testMat=loadData('processed_test_del.csv')
ax = []
ay = []
for i in range(0, 12):
    trainMat[:,i]=trainMat[:,i]/max(trainMat[:,i])
    testMat[:,i]=testMat[:,i]/max(testMat[:,i])
m,n=shape(trainMat)
NN=NeuralNetwork(n,80,100,40,1,0.007)  
cnt,pre=NN.train(trainMat,10)
print cnt*1.0/m
print pre
final_outputs=NN.run(testMat)
out=final_outputs[0].tolist()[0]
print out
np.savetxt("22_v10.csv", out, fmt="%d", delimiter="\n", newline="\n")
plt.figure("fg10")
plt.plot(ax,ay)
plt.show()