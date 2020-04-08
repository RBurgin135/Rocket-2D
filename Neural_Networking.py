#wall of Richard Burgins hard work, may it stand eternal and unto it I pledge my life===============================================================================
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
        #Inputs
        #Altitude, displacement, horizontal velocity, vertical velocity, horizontal acceleration, vertical acceleration, fuel, degrees
        for i in range(0,self.HiddenNum)
            self.InputLayer.append(Neuron(1))

        #self.Altitude = Neuron(1)
        #self.Displacement = Neuron(1)
        #self.Hori_Velocity = Neuron(1)
        #self.Verti_Velocity = Neuron(1)
        #self.Hori_Acceleration = Neuron(1)
        #self.Verti_Acceleration = Neuron(1)
        #self.Fuel = Neuron(1)
        #self.Deg = Neuron(1)

        #Hidden
        for i in range(0,6)
            self.HiddenLayer.append(Neuron(1))
        #self.H1 = Neuron(8)
        #self.H2 = Neuron(8)
        #self.H3 = Neuron(8)
        #self.H4 = Neuron(8)
        #self.H5 = Neuron(8)
        #self.H6 = Neuron(8)

        #Outputs
        #Thrust, Turn left, Turn right
        for i in range(0,self.OutputNum)
            self.OutputLayer.append(Neuron(1))
        #self.Thrust = Neuron(6)
        #self.Turn_Right = Neuron(6)
        #self.Turn_Left = Neuron(6)

        #Score
        self.score = 0

    def Forward(self, InputInputs):
        #Input
        #a = self.Displacement.ActivationFunction(Disp[0])
        #b = self.Altitude.ActivationFunction(Disp[1])
        #c = self.Hori_Velocity.ActivationFunction(Velo[0])
        #d = self.Verti_Velocity.ActivationFunction(Velo[1])
        #e = self.Hori_Acceleration.ActivationFunction(Acc[0])
        #f = self.Verti_Acceleration.ActivationFunction(Acc[1])
        #g = self.Fuel.ActivationFunction(Fuel)
        #h = self.Deg.ActivationFunction(Deg)
        HiddenInputs = []
        for i in range(0,self.InputNum):
            HiddenInputs.append(self.InputLayer[i].ActivationFunction(InputInputs[i]))
        
        #Hidden
        #HiddenInputs = [a,b,c,d,e,f,g,h]
        #i = self.H1.ActivationFunction(HiddenInputs)
        #j = self.H2.ActivationFunction(HiddenInputs)
        #k = self.H3.ActivationFunction(HiddenInputs)
        #l = self.H4.ActivationFunction(HiddenInputs)
        OutputInputs = []
        for i in range(0, self.HiddenNum):
            OutputInputs.append(self.HiddenLayer[i].ActivationFunction(HiddenInputs[i])) 

        #Output
        #OutputInputs = [i,j,k,l]
        #m = self.Thrust.ActivationFunction(OutputInputs)
        #n = self.Turn_Left.ActivationFunction(OutputInputs)
        #o = self.Turn_Right.ActivationFunction(OutputInputs)
        OutputOutputs = []
        for i in range(0, self.OutputNum):
            OutputOutputs.append(self.OutputLayer[i].ActivationFunction(Outputnputs[i])) 

        return  OutputOutputs

    def Scoring(self, Velo, Fuel, Success, Disp):
        Score_V = (-Velo[0] *10) + (-Velo[1] *10)
        Score_F = Fuel
        if Disp < 0:
            Score_D = Disp * 10 
        else:
            Score_D = -Disp * 10
        Score_S = 0
        if Success == True:
            Score_S = 10000

        self.score = Score_S  + Score_V + Score_F

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
    
    #clone
    for i in range(0,int(len(Pop)//6)):
        NewNetlist.append(Netlist[0])
        Netlist.pop(0)

    #breed
    Breed()

    #mutate
    Mutatelist = []
    for i in range(0,int(len(Netlist)/2)):
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
    #change the weights and biases a very small amount
    fence = 0.5
    #Inputs
    for x in range(0, len(Net.InputLayer)):
            if random.random() > 0.2:
                for y in range():
                Net.InputLayer[x].weight
                Net
    Net.Altitude.weight[0] += random.uniform(-fence,fence)
    Net.Altitude.bias += random.uniform(-fence,fence)
    Net.Velocity.weight[0] += random.uniform(-fence,fence)
    Net.Velocity.bias += random.uniform(-fence,fence)
    Net.Acceleration.weight[0] += random.uniform(-fence,fence)
    Net.Acceleration.bias += random.uniform(-fence,fence)
    Net.Fuel.weight[0] += random.uniform(-fence,fence)
    Net.Fuel.bias += random.uniform(-fence,fence)

    #Hidden
    for i in range(0,len(Net.H1.weight)):
        Net.H1.weight[i] += random.uniform(-fence,fence)
    Net.H1.bias += random.uniform(-fence,fence)
    for i in range(0,len(Net.H2.weight)):
        Net.H2.weight[i] += random.uniform(-fence,fence)
    Net.H2.bias += random.uniform(-fence,fence)
    for i in range(0,len(Net.H3.weight)):
        Net.H3.weight[i] += random.uniform(-fence,fence)
    Net.H3.bias += random.uniform(-fence,fence)
    for i in range(0,len(Net.H4.weight)):
        Net.H4.weight[i] += random.uniform(-fence,fence)
    Net.H4.bias += random.uniform(-fence,fence) 

    #Outputs
    for i in range(0,len(Net.Thrust.weight)):
        Net.Thrust.weight[i] += random.uniform(-fence,fence)
    Net.Thrust.bias += random.uniform(-fence,fence)

    return Net

def Breed():
    pass