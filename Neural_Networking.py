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
        self.layernum = 3 #number of layers
        self.neuronnum = [8,4,3] #neurons for each layer
        self.inputnum = [1,8,4] #inputs for each layer

        #layers
        self.Layers = []
        for x in range(0,self.layernum): #cycles through layers
            self.Layers.append([]) #adds a new layer
            for y in range(0,self.neuronnum[x]): #cycles through neurons
                self.Layers[x].append(Neuron(self.inputnum[x])) #adds the neurons to the layer with specified number of inputs

        #Score
        self.score = 0

    def Forward(self, Inputs):
        Processing = [[]]
        for i in range(0,len(Inputs)): #cycles through the inputs so each neuron in the input layer has its own input
            Processing[0].append(self.Layers[0][i].ActivationFunction(Inputs[i])) #runs inputs through activation function and adds outputs to processing
        for x in range(0,self.layernum): #cycles through the layers after the input layer
            Processing.append([]) 
            for y in range(0,self.neuronnum[x]):#cycles through neurons
                Processing[x+1].append(self.Layers[x][y].ActivationFunction(Processing[x])) #runs inputs through activation function and adds outputs to processing

        return  Processing[len(Processing)-1] #returns output layers outputs

    def Scoring(self, Details):
        self.score = 0
        if Details[0] == "SUCCESS":
            self.score += 1*(10**16)
        elif Details[0] == "FAIL":
            self.score += 800
        self.score += -Details[1][1] * 50
        #self.score += int((999 - abs(Details[1][0])) *(10**6))
        self.score += abs(Details[2]) *10
        self.score += - abs(Details[3]) * 9
        self.score += Details[4]
       
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
        Netlist[len(Netlist)-1].Scoring([Pop[i].status, Pop[i].testU, Pop[i].testdeg, Pop[i].disp[0], Pop[i].fuel])
    
    #print("===============================================")
    #for i in Netlist:
    #    print(i.score)
    #for i in range(0,3):
    #    print(Pop[i].disp[0])
    Netlist = Sort(Netlist)
    

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
    for z in range(0, len(Net.Layers)): #cycles through layers
        for x in range(0, len(Net.Layers[z])): #cycles through neurons
            for y in range(0, len(Net.Layers[z][x].weight)): #cycles through weights
                if random.random() > prob:
                    Net.Layers[z][x].weight[y] += random.uniform(-fence,fence) #mutates weights
            if random.random() > prob:
                Net.Layers[z][x].bias += random.uniform(-fence,fence) #mutates bias

    Net.score = -99999998
    return Net

def Breed(ParentA,ParentB):
    Child = NeuralNet()

    #Average of inputs
    for z in range(0, len(ParentA.Layers)): #cycles through layers
        for x in range(0, len(ParentA.Layers[z])-1): #cycles through neurons
            for y in range(0, len(ParentA.Layers[z][x].weight)): #cycles through weights
                Child.Layers[z][x].weight[y] = (ParentA.Layers[z][x].weight[y] + ParentB.Layers[z][x+1].weight[y])/2 #finds average between two parent weights
            Child.Layers[z][x].Bias = (ParentA.Layers[z][x].bias + ParentB.Layers[z][x+1].bias)/2 #finds average between two parent biases
        
    #puts children at the back
    Child.score = -99999999
    return Child

def Write(GenNumber, Pop):
    name =  input("Name the file to save: ")
    f = open(name+".txt", "w")
    Nets = []
    for i in range(0,len(Pop)):
        Nets.append(Pop[i].Nn)
    
    #encodes the data
    f.write((str(GenNumber)+","))
    for z in range(0,len(Nets)): #cycles through the nets
        f.write("N,")
        for x in range(0, len(Nets[z].Layers)): #cycles through layers
            f.write("L,")
            for y in range(0, len(Nets[z].Layers[x])): #cycles through neurons
                f.write("n,")
                for i in range(0, len(Nets[z].Layers[x][y].weight)): #cycles through weights
                    f.write(("w,"+str(Nets[z].Layers[x][y].weight[i])+","))
                f.write(("b,"+str(Nets[z].Layers[x][y].bias)+","))
    f.close()

def Read(Pop):
    name =  input("Name the file to load: ")
    f = open(name+".txt", "r")

    #decodes the data
    block = f.readline()
    chunks = block.split(",")
    #declaring indexes
    Ni = -1
    GenNumber = int(chunks[0])
    for i in range(0,len(chunks)):
        if chunks[i] == "N":#cycles through the nets
            Ni += 1
            Li = -1
        if chunks[i] == "L": #cycles through the layers
            Li += 1
            ni = -1
        if chunks[i] == "n":#cycles through neurons
            ni += 1
            wi = -1
        if chunks[i] == "w":#cycles through weights
            wi += 1
            Pop[Ni].Nn.Layers[Li][ni].weight[wi] = float(chunks[i+1])
        if chunks[i] == "b":
            Pop[Ni].Nn.Layers[Li][ni].bias = float(chunks[i+1])

    #resets rocket
    StartAltitude = random.randint(2500,2500)
    StartDisplacement = random.randint(-500,-500)
    for i in range(0, len(Pop)):
        Pop[i].__init__(StartDisplacement, StartAltitude, True)


    return Pop, GenNumber