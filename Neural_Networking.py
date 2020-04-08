#=========================wall of Richard Burgins hard work, may it stand eternal and unto it I pledge my life======================================================
#===================================================================================================================================================================
#===================================================================================================================================================================

import math
import random
import numpy

#Objects==========
class NeuralNet:
    def __init__(self):
        self.InputNum = 8
        self.HiddenNum = 6
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
            self.HiddenLayer.append(Neuron(1))

        #Outputs
        #Thrust, Turn left, Turn right
        for i in range(0,self.OutputNum):
            self.OutputLayer.append(Neuron(1))

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
            OutputInputs.append(self.HiddenLayer[i].ActivationFunction(HiddenInputs[i])) 

        #Output
        OutputOutputs = []
        for i in range(0, self.OutputNum):
            OutputOutputs.append(self.OutputLayer[i].ActivationFunction(OutputInputs[i])) 

        return  OutputOutputs

    def Scoring(self, Velo, Fuel, Success, Disp):
        Score_V = (-Velo[0] *10) + (-Velo[1] *10)
        Score_F = Fuel
        if Disp < 0:
            Score_D = Disp * 100
        else:
            Score_D = -Disp * 100
        Score_S = 0
        if Success == True:
            Score_S = 10000

        self.score = Score_S  + Score_V + Score_F + Score_D

#======= 
class Neuron:
    def __init__(self, num_inputs):
        self.bias = 0
        self.weight = []
        for i in range(0,num_inputs):
            self.weight.append(random.uniform(-1,1))

    def ActivationFunction(self, Input):
        total = sum(numpy.multiply(Input,self.weight))
        return (self.ReLU(total)+ self.bias)

    def ReLU(self, x):
        result = max(x, 0)
        return result

    def sigmoid(self, x):
        result = 1/(1+math.exp(-x))
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
        Netlist[len(Netlist)-1].Scoring(Pop[i].testU, Pop[i].fuel, Pop[i].SUCCESS, Pop[i].disp[0])
    
    Netlist = Sort(Netlist)
    #breed
    Breedlist = Breed(Netlist)
    print("Breedlist length: ",len(Breedlist))

    #clone
    for i in range(0,int(len(Pop)//6)):
        NewNetlist.append(Netlist[0])
        Netlist.pop(0)

    NewNetlist = NewNetlist + Breedlist
    
    #mutate
    Mutatelist = []
    for i in range(int(len(Pop)//6)-1 ,len(Netlist)):
        result = Netlist[i]
        if random.uniform(0,1)> 0.5:
            result = Mutate(Netlist[i])
        Mutatelist.append(result)

    #The rest of Netlist are removed
    NewNetlist = NewNetlist + Mutatelist

    return NewNetlist

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
    fence = 0.5
    prob = 0.2
    
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

    return Net

def Breed(Net):
    ChildList = []
    for i in range(0, (len(Net)-1)):
        Child = NeuralNet()

        #Average of inputs
        for x in range(0, len(Net.InputLayer)):
            for y in range(0, len(Net.InputLayer[x].weight)):
                Child.InputLayer[x].weight[y] = (Net[x].InputLayer.weight[y] + Net[x+1].InputLayer.weight[y])/2
            Child.InputLayer[x].Bias = (Net[x].InputLayer.bias + Net[x+1].InputLayer.bias)/2
        
        #Average of hiddens
        for x in range(0, len(Net.HiddenLayer)):
            for y in range(0, len(Net.HiddenLayer[x].weight)):
                Child.HiddenLayer[x].weight[y] = (Net[x].HiddenLayer.weight[y] + Net[x+1].HiddenLayer.weight[y])/2
            Child.HiddenLayer[x].Bias = (Net[x].HiddenLayer.bias + Net[x+1].HiddenLayer.bias)/2

        #Average of outputs
        for x in range(0, len(Net.OutputLayer)):
            for y in range(0, len(Net.OutputLayer[x].weight)):
                Child.OutputLayer[x].weight[y] = (Net[x].OutputLayer.weight[y] + Net[x+1].OutputLayer.weight[y])/2
            Child.OutputLayer[x].Bias = (Net[x].OutputLayer.bias + Net[x+1].OutputLayer.bias)/2
            
        ChildList.append(Child)

    return ChildList