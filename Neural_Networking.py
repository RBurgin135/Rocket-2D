#=========================wall of Richard Burgins hard work, may it stand eternal and unto it I pledge my life======================================================
#===================================================================================================================================================================
#===================================================================================================================================================================

import copy
import math
import random
import numpy

#Objects==========
class NeuralNet:
    def __init__(self):
        self.InputNum = 8
        self.HiddenNum = 4
        self.OutputNum = 3

        #layers
        self.InputLayer = []
        self.HiddenLayer = []
        self.OutputLayer = []
        #Inputs
        #Altitude, displacement, horizontal velocity, vertical velocity, horizontal acceleration, vertical acceleration, fuel, degrees
        for i in range(0,self.InputNum):
            self.InputLayer.append(Neuron(1))

        #Hidden
        for i in range(0,self.HiddenNum):
            self.HiddenLayer.append(Neuron(self.InputNum))

        #Outputs
        #Thrust, Turn left, Turn right
        for i in range(0,self.OutputNum):
            self.OutputLayer.append(Neuron(self.HiddenNum))

        #Score
        self.score = 0

    def Forward(self, InputInputs):
        #Input
        HiddenInputs = []
        for i in range(0,self.InputNum):
            HiddenInputs.append(self.InputLayer[i].ActivationFunction(InputInputs[i]))
        
        #Hidden
        OutputInputs = []
        for i in range(0, self.HiddenNum):
            OutputInputs.append(self.HiddenLayer[i].ActivationFunction(HiddenInputs)) 

        #Output
        OutputOutputs = []
        for i in range(0, self.OutputNum):
            OutputOutputs.append(self.OutputLayer[i].ActivationFunction(OutputInputs)) 

        return  OutputOutputs

    def Scoring(self, Details):
        self.score = 0
        self.score += -abs(Details[0])*1000 
        #self.score += -Details[1][0] * 50
        #self.score += -Details[1][1] * 50
        #self.score += Details[2] * 10
        if Details[3] == True:
            self.score += 1000000

#======= 
class Neuron:
    def __init__(self, num_inputs):
        self.bias = 0
        self.weight = []
        for i in range(0,num_inputs):
            self.weight.append(random.uniform(-1,1))

    def ActivationFunction(self, Input):
        total = sum(numpy.multiply(Input,self.weight))
        return (self.sigmoid(total)+ self.bias)

    def ReLU(self, x):
        result = max(x, 0)
        return result

    def sigmoid(self, x):
        try:
            result = 1/(1+math.exp(-x))
        except:
            OverflowError
            if x>0:
                result = 1
            else:
                result = 0

        return result

    def step(self, x):
        if x > 0:
            return 1
        else:
            return -1

#Functions==========
def Review(Pop):
    Netlist = []
    NewNetlist = []
    for i in range(0,len(Pop)):
        Netlist.append(Pop[i].Nn) 
        Netlist[len(Netlist)-1].Scoring([Pop[i].disp[0], Pop[i].testU, Pop[i].fuel, Pop[i].SUCCESS])
    
    Netlist = Sort(Netlist)
    #print("Score: ",Pop[0].Nn.score)
    #print("Velocity: ",Pop[0].testU)

    #Clone
    CloneNo = int(len(Pop)//6)
    for i in range(0, CloneNo):
        NewNetlist.append(copy.deepcopy(Netlist[i]))

    #Breed
    BreedNo =  int(len(Pop)//2)
    for i in range(0, BreedNo):
        A = copy.deepcopy(Netlist[random.randint(0, len(Netlist)-1)//2])
        B = copy.deepcopy(Netlist[random.randint(0, len(Netlist)-1)//2])
        NewNetlist.append(Breed(A,B))

    #Mutate
    MutateNo = len(Pop) - (BreedNo + CloneNo)
    for i in range(0, MutateNo):
        TestSubject = copy.deepcopy(Netlist[random.randint(0, len(Netlist)-1)])
        NewNetlist.append(Mutate(TestSubject))

    return Sort(NewNetlist)

def Sort(List):
    #Bubble sort
    Sorted = False
    while Sorted == False:
        Sorted = True
        for i in range(0, len(List)-1):
            if List[i].score < List[i+1].score:
                Sorted = False
                Buffer = List[i]
                List[i] = List[i+1]
                List[i+1] = Buffer


    return List

def Mutate(Net):
    #Fence is the max degree of mutation, prob is the likelihood of mutating
    fence = 0.01
    prob = 0.7
    
    #Inputs
    for x in range(0, len(Net.InputLayer)):
        for y in range(0, len(Net.InputLayer[x].weight)):
            if random.random() > prob:
                Net.InputLayer[x].weight[y] += random.uniform(-fence,fence)
        if random.random() > prob:
            Net.InputLayer[x].bias += random.uniform(-fence,fence)

    #Hidden
    for x in range(0, len(Net.HiddenLayer)):
        for y in range(0, len(Net.HiddenLayer[x].weight)):
            if random.random() > prob:
                Net.HiddenLayer[x].weight[y] += random.uniform(-fence,fence)
        if random.random() > prob:
            Net.HiddenLayer[x].bias += random.uniform(-fence,fence)

    #Outputs
    for x in range(0, len(Net.OutputLayer)):
        for y in range(0, len(Net.OutputLayer[x].weight)):
            if random.random() > prob:
                Net.OutputLayer[x].weight[y] += random.uniform(-fence,fence)
        if random.random() > prob:
            Net.OutputLayer[x].bias += random.uniform(-fence,fence)

    Net.score = -99999998
    return Net

def Breed(ParentA,ParentB):
    Child = NeuralNet()

    #Average of inputs
    for x in range(0, len(ParentA.InputLayer)-1):
        for y in range(0, len(ParentA.InputLayer[x].weight)):
            Child.InputLayer[x].weight[y] = (ParentA.InputLayer[x].weight[y] + ParentB.InputLayer[x+1].weight[y])/2
        Child.InputLayer[x].Bias = (ParentA.InputLayer[x].bias + ParentB.InputLayer[x+1].bias)/2
    
    #Average of hiddens
    for x in range(0, len(ParentA.HiddenLayer)-1):
        for y in range(0, len(ParentA.HiddenLayer[x].weight)):
            Child.HiddenLayer[x].weight[y] = (ParentA.HiddenLayer[x].weight[y] + ParentB.HiddenLayer[x+1].weight[y])/2
        Child.HiddenLayer[x].Bias = (ParentA.HiddenLayer[x].bias + ParentB.HiddenLayer[x+1].bias)/2

    #Average of outputs
    for x in range(0, len(ParentA.OutputLayer)-1):
        for y in range(0, len(ParentA.OutputLayer[x].weight)):
            Child.OutputLayer[x].weight[y] = (ParentA.OutputLayer[x].weight[y] + ParentB.OutputLayer[x+1].weight[y])/2
        Child.OutputLayer[x].Bias = (ParentA.OutputLayer[x].bias + ParentB.OutputLayer[x+1].bias)/2
        
    #puts children at the back
    Child.score = -99999999
    return Child