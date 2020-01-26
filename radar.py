import pygame
import time
import math

class Radar():

    def __init__(self):
        pygame.init()
        self.__lcd = pygame.display.set_mode((800,600))
        pygame.mouse.set_visible(False)


        self.__radarLineAngle=0
        self.__radarBlipGamma=255
        self.__oldpointAngle=0
        self.__oldpointDistance=0
        self.__compassPoints=[]
        self.__crosshatchLines=[]
        self.__concentricRadii=[]
        self.__radarBox=None
        self.__radarX = 0
        self.__radarY = 0
        self.__radarRadius = 0


    def setup(self, radarX, radarY, radarRadius):
        self.__radarX = radarX
        self.__radarY = radarY
        self.__radarRadius = radarRadius

        #crosshatches
        chAngle=0
        for a in range(0, 4):
            chAngle=a*45
            self.__crosshatchLines.append([self.circleXY(self.__radarX, self.__radarY, chAngle, self.__radarRadius), self.circleXY(self.__radarX, self.__radarY, chAngle+180, self.__radarRadius)])
        
        #concentric circles
        f=0.25
        for a in range(0, 3):
            self.__concentricRadii.append(int(self.__radarRadius*f))
            f=f+0.25

        #points on circumference
        for a in range(0, 360):
            lineEndX = self.__radarX + math.cos(math.radians(a)) * (self.__radarRadius-1)
            lineEndY = self.__radarY + math.sin(math.radians(a)) * (self.__radarRadius-1)
            self.__compassPoints.append((lineEndX, lineEndY))
        
        self.__radarBox=(self.__radarX-self.__radarRadius, self.__radarY-self.__radarRadius, self.__radarRadius*2, self.__radarRadius*2)


    def update(self, pointAngle, pointDistance, maxDistance):
        radarColor=(0,50,0)
        radarLineColor=(0,255,0)
        
        #clear rectangle bounded by circle
        pygame.draw.rect(self.__lcd, (0,0,0), self.__radarBox, 0)

        #draw radar circle
        pygame.draw.circle(self.__lcd, radarColor, (self.__radarX,self.__radarY), self.__radarRadius, 1)
 
        #crosshatches
        for a in range(0, len(self.__crosshatchLines)):
            pygame.draw.line(self.__lcd, radarColor, self.__crosshatchLines[a][0], self.__crosshatchLines[a][1])
       
        # concentric circles
        for a in range(0, len(self.__concentricRadii)):
            pygame.draw.circle(self.__lcd, radarColor, (self.__radarX,self.__radarY), self.__concentricRadii[a], 1)
    
        #draw radar line
        pygame.draw.line(self.__lcd, radarLineColor, (self.__radarX, self.__radarY), self.__compassPoints[self.__radarLineAngle], 3)

        #keep blip inside circle radius
        if (pointDistance > maxDistance-6):
            pointDistance = maxDistance-6

        #transform blip distance proportionally from mileage to circle radius
        blipRatio=maxDistance/self.__radarRadius
        blipRadius=int(pointDistance/blipRatio)

        #calculate blip (x,y)
        blipX=blipRadius*math.cos(math.radians(pointAngle))
        blipY=blipRadius*math.sin(math.radians(pointAngle))

        #transform the coordinates from Unit Circle to Mathematics Circle
        plotX=blipY
        plotY=-blipX

        #reset blip intensity if anything has changed
        if ((pointDistance != self.__oldpointDistance) | (pointAngle != self.__oldpointAngle)):
            self.__oldpointAngle = pointAngle
            self.__oldpointDistance = pointDistance
            self.__radarBlipGamma = 255

        #plot the blip
        pygame.draw.circle(self.__lcd, (self.__radarBlipGamma, self.__radarBlipGamma,0), (self.__radarX+int(plotX),self.__radarY+int(plotY)), 2)

        #fade the blip
        self.__radarBlipGamma-=1
        if (self.__radarBlipGamma < 75):
            self.__radarBlipGamma = 75

        #advance the radar arm
        self.__radarLineAngle+=1
        if (self.__radarLineAngle == 360):
            self.__radarLineAngle=0

        pygame.display.update(self.__radarBox)
        clock = pygame.time.Clock()
        clock.tick(200)

    def circleXY(self, cX, cY, angle, radius):
        x = cX + radius * math.cos(math.radians(angle))
        y = cY + radius * math.sin(math.radians(angle))
        return(int(x),int(y))

    def drawradius(self, xCenter,yCenter,angle):
        self.__lcd.fill((0,0,0))
        pygame.draw.circle(self.__lcd, (0,64,0), (xCenter,yCenter), 160, 1)
        radar_len = 150
        x = xCenter + math.cos(math.radians(angle)) * radar_len
        y = yCenter + math.sin(math.radians(angle)) * radar_len
        self.arrow(self.__lcd, (0,64,0), (128,0,0), (xCenter, yCenter), (x,y), 7)
        pygame.display.update()

    def arrow(self, lcolor, tricolor, start, end, trirad):
        pygame.draw.line(self.__lcd,lcolor,start,end,2)
        rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))+90
        pygame.draw.polygon(self.__lcd, tricolor, ((end[0]+trirad*math.sin(math.radians(rotation)), end[1]+trirad*math.cos(math.radians(rotation))), (end[0]+trirad*math.sin(math.radians(rotation-120)), end[1]+trirad*math.cos(math.radians(rotation-120))), (end[0]+trirad*math.sin(math.radians(rotation+120)), end[1]+trirad*math.cos(math.radians(rotation+120)))))

