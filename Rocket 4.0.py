#Rocket that lands itself
global g
g = 1
global PopSize
PopSize = 20
import pygame
from pygame import FULLSCREEN
import random
pygame.font.init()
import math
import Neural_Networking as Networking
import time

#window setup
import ctypes
user32 = ctypes.windll.user32
global scr_width
global scr_height
scr_width = user32.GetSystemMetrics(0)
scr_height = user32.GetSystemMetrics(1)
window = pygame.display.set_mode((scr_width,scr_height),FULLSCREEN)
pygame.display.set_caption("Rocket 3.0")

#Objects====
#======
class Rocket:
    def __init__(self, disp, Alt, Overide):
        #Rocket values
        self.fuel = 100
        self.disp = [disp,Alt]
        self.strength = -25
        self.thrust = [0,0]
        self.deg = 0

        #pygame content
        self.On = pygame.image.load("Rocket on.png")
        self.Off = pygame.image.load("Rocket off.png")
        self.Broken = pygame.image.load("Rocket no-fuel.png")
        self.image = self.Off
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        X = G.X - self.disp[0] - self.width()/2
        Y = G.Y - self.disp[1] - self.height()/2
        self.blit = [X - self.image.get_width()/2, Y - self.image.get_height()/2]

        #testing values
        self.crash = False
        self.SUCCESS = False
        self.tested = False
        self.testU = [0,0]

        #mass values
        self.R_m = 10
        self.F_m = self.fuel * 0.03
        self.Total_m = self.R_m + self.F_m

        #SUVAT values
        self.u = [0,0]
        self.a = [0,0]
        self.s = [0,0]

        if Overide == False:
            self.Nn = Networking.NeuralNet()

    def Active(self):
        if self.fuel > 0:
            self.strength
            self.fuel -=1
            self.image = self.On
        else:
            self.image = self.Broken

        radians = math.radians(self.deg)
        opp = self.strength * math.sin(radians)
        adj = self.strength * math.cos(radians)
        self.thrust = -opp
        self.thrust = adj

=====================================================================
    def Calculate(self):
        #find updated mass
        self.F_m = self.fuel * 0.02
        self.Total_m = self.R_m + self.F_m

        for i in range(0,1):
            #find resultant force in axis (F=ma)       
            Resultant_F = (g*self.Total_m) + self.thrust

            self.a[i] = 0
            if Resultant_F != 0:
                self.a[i] =  Resultant_F / self.Total_m

            #find displacement on axis (s = ut- 1/2 at^2)
            self.s[i] = self.u[i] - 0.5*self.a[i]

            #crash and success query============================================
            if (self.disp[i] - self.s[i]) <=0:
                if (self.crash == False) and (self.u > 25):
                    #============================================================
                    self.crash = True
                    self.tested = True
                    self.testU[i] = self.u[i]
                if self.crash == False and (self.blitX > P.X and (self.blitX+self.width) < (P.X+P.width)):
                    self.SUCCESS = True
                    self.tested = True
                    self.testU = self.u[i]
                
                self.s[i] = 0
                self.u[i] = 0
                self.deg = 0

                self.disp[i] -= self.s[i]
                self.blit[i] += self.s[i]


        #show rocket
        window.blit(self.image,(self.blit[0]] , self.blit[1]))
=====================================================================
    def Reset(self):
        #find velocity used in next Calculate (v = u + at)
        for i in range(0,1):
            self.u[i] = self.u[i] + self.a[i]

            #reset values
            self.thrust[i] = 0
        self.image = self.Off
           
#======
class Ground:
    def __init__(self):
        self.X = -5000
        self.Y = scr_height- 50
        self.rect_width = 10000 
        self.rect_height = 50

        self.details = self.X, self.Y, self.rect_width, self.rect_height
        self.rect = pygame.Rect(self.details)
        
    def Show(self):
        self.details = self.X, self.Y, self.rect_width, self.rect_height
        self.rect = pygame.draw.rect(window,(211,211,211),self.details)
        
#======
class Pad:
    def __init__(self):
        self.X = scr_width/2-100
        self.Y = G.Y
        self.width = 200
        self.height = 25
        self.details = self.X, self.Y, self.width, self.height
        self.colour = (255,195,77)
        self.text = "<LANDING>"
    
    def Show(self):        
        self.Y = G.Y
        
        self.details = self.X, self.Y, self.width, self.height
        self.rect = pygame.draw.rect(window,self.colour,self.details)

        SubFont = pygame.font.SysFont('', 25)
        Text = SubFont.render(self.text, False, (255,255,255))
        window.blit(Text,(self.X+60,self.Y+2))

#Functions====        
def Background(Num):
    #Stars
    Star = pygame.image.load("Star.png")
    window.fill((0,0,0))
    for x in range(0,50):
        for y in range(0,100):
            if y % 2 == 0:
                window.blit(Star,(G.X+200+200* x, G.Y-50-200*y))
            else:
                window.blit(Star,(G.X+350+200* x, G.Y-50-200*y))
    
    #Gen number
    SubFont = pygame.font.SysFont('', 100)
    Text = SubFont.render("GEN "+str(Num), False, (255,255,255))
    window.blit(Text,(0,0))

def AI(Pop):
    for i in range(0,len(Pop)):
        if Pop[i].tested == False:
            ForwardInputs = [Pop[i].disp[0],Pop[i].disp[1], Pop[i].u[0], Pop[i].u[1], Pop[i].a[0], Pop[i].a[1], Pop[i].fuel, Pop[i].deg]
            result = Pop[i].Nn.Forward(ForwardInputs)
            if result[0] > 0.5:
                Pop[i].Active()
            if result[1] > 0.5:
                Pop[i].deg += 1
            if result[0] > 0.5:
                Pop[i].deg += 1

def Diagnostics(Pop):
    Y = scr_height-40
    for i in range(0,len(Pop)):
        X = 10+40*i
        details = X, Y, 20, 20
        if Pop[i].tested == False: 
            #state indicator
            if Pop[i].image == Pop[i].On:
                pygame.draw.rect(window,(237,28,36),details)
            elif Pop[i].image == Pop[i].Off:
                pygame.draw.rect(window,(153,217,234),details)
            else:
                pygame.draw.rect(window,(255,127,39),details)
            
            #fuel gauge
            if Pop[i].fuel > 0:
                details = (X, Y+21, Pop[i].fuel/4, 5)
                pygame.draw.rect(window,(255,127,39),details)

            #Altimeter
            details = (X-6, Y+20-Pop[i].disp[1]/15, 5, Pop[i].disp[1]/15)
            pygame.draw.rect(window,(255,255,127),details)
        else:
            if Pop[i].SUCCESS == True:
                pygame.draw.rect(window,(76,166,76),details)
            else:
                pygame.draw.rect(window,(166,166,166),details)

def GenerationMngmnt(Pop, GenNumber):
    GenTest = True
    for i in range(0, PopSize):
        if Pop[i].tested == False:
            GenTest = False

    if GenTest == True:
        #Prep for next Gen
        time.sleep(0.5)
        GenNumber += 1
        
        NewNets = Networking.Review(Pop)


        #new gen
        StartAltitude = random.randint(2500,5000)
        for i in range(0,len(NewNets)):
            Pop[i].Nn = NewNets[i]
            Pop[i].__init__(StartAltitude, True)

        NewRockets = []
        for i in range(0, PopSize - len(NewNets)):
            NewRockets.append(Rocket(StartAltitude, False))
            Pop.pop(len(NewNets))

        Pop = Pop + NewRockets
    return GenNumber, Pop

G = Ground()
P = Pad()
Pop = []
StartAltitude = random.randint(2500,5000)
StartDisplacement = random.randint(2500,5000)
for i in range(0,PopSize):
    Pop.append(Rocket(StartDisplacement, StartAltitude, False))
GenNumber = 1

RUN = True
while RUN:
    pygame.time.delay(10)
    AI(Pop)         

    Background(GenNumber)

    for i in range(0,PopSize):
        Pop[i].Calculate()

    G.Show()
    P.Show()
    Diagnostics(Pop)

    pygame.display.update()
    for i in range(0, PopSize):
        Pop[i].Reset()
    
    #generation managment
    GenNumber, Pop = GenerationMngmnt(Pop, GenNumber)
pygame.quit()

        
