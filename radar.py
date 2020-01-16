import pygame
import time
import math

def drawradius(lcd,xCenter,yCenter,angle):
    lcd.fill((0,0,0))
    pygame.draw.circle(lcd, (0,64,0), (xCenter,yCenter), 160, 1)
    radar_len = 150
    x = xCenter + math.cos(math.radians(angle)) * radar_len
    y = yCenter + math.sin(math.radians(angle)) * radar_len
    arrow(lcd, (0,64,0), (128,0,0), (xCenter, yCenter), (x,y), 7)
    pygame.display.update()

def arrow(screen, lcolor, tricolor, start, end, trirad):
    pygame.draw.line(screen,lcolor,start,end,2)
    rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))+90
    pygame.draw.polygon(screen, tricolor, ((end[0]+trirad*math.sin(math.radians(rotation)), end[1]+trirad*math.cos(math.radians(rotation))), (end[0]+trirad*math.sin(math.radians(rotation-120)), end[1]+trirad*math.cos(math.radians(rotation-120))), (end[0]+trirad*math.sin(math.radians(rotation+120)), end[1]+trirad*math.cos(math.radians(rotation+120)))))

def circleXY(cX, cY, angle, radius):
    x = cX + radius * math.cos(math.radians(angle))
    y = cY + radius * math.sin(math.radians(angle))
    return(int(x),int(y))

def drawRadarLine(lcd,radarX,radarY,radarRadius,blipAngle,blipDistance,maxBlipDistance):
    global radarAngle
    global radarBlipGamma
    global oldBlipAngle
    global oldBlipDistance

    radarColor=(0,50,0)
    radarLineColor=(0,255,0)
    
    #clear rectangle bounded by circle
    radarBox=(radarX-radarRadius, radarY-radarRadius, radarRadius*2, radarRadius*2)
    pygame.draw.rect(lcd, (0,0,0), radarBox, 0)

    #draw radar circle
    pygame.draw.circle(lcd, radarColor, (radarX,radarY), radarRadius, 1)
    #crosshatches
    chAngle=0
    for a in range(0, 4):
        chAngle=a*45
        pygame.draw.line(lcd, radarColor, circleXY(radarX, radarY, chAngle, radarRadius), circleXY(radarX, radarY, chAngle+180, radarRadius))

    
    # concentric circles
    pygame.draw.circle(lcd, radarColor, (radarX,radarY), int(radarRadius*0.25), 1)
    pygame.draw.circle(lcd, radarColor, (radarX,radarY), int(radarRadius*0.50), 1)
    pygame.draw.circle(lcd, radarColor, (radarX,radarY), int(radarRadius*0.75), 1)


    #draw radar line
    lineEndX = radarX + math.cos(math.radians(radarAngle)) * (radarRadius-1)
    lineEndY = radarY + math.sin(math.radians(radarAngle)) * (radarRadius-1)
    pygame.draw.line(lcd, radarLineColor, (radarX, radarY), (lineEndX,lineEndY), 3)

    #keep blip inside circle radius
    if (blipDistance > maxBlipDistance-6):
        blipDistance = maxBlipDistance-6

    #transform blip distance proportionally from mileage to circle radius
    blipRatio=maxBlipDistance/radarRadius
    blipRadius=int(blipDistance/blipRatio)

    #calculate blip (x,y)
    blipX=blipRadius*math.cos(math.radians(blipAngle))
    blipY=blipRadius*math.sin(math.radians(blipAngle))

    #transform the coordinates from Unit Circle to Mathematics Circle
    plotX=blipY
    plotY=-blipX

    #reset blip intensity if anything has changed
    if ((blipDistance != oldBlipDistance) | (blipAngle != oldBlipAngle)):
        oldBlipAngle = blipAngle
        oldBlipDistance = blipDistance
        radarBlipGamma = 255

    #plot the blip
    pygame.draw.circle(lcd, (radarBlipGamma, radarBlipGamma,0), (radarX+int(plotX),radarY+int(plotY)), 3)

    #csFont= pygame.font.SysFont("Arial", 12)
    #txt = csFont.render(callsign, 1, (255,255,0))
    #lcd.blit(txt, (radarX+int(plotX)-23,radarY+int(plotY)-20))

    #fade the blip
    radarBlipGamma-=(0.20)
    if (radarBlipGamma < 75):
        radarBlipGamma = 75

    #advance the radar arm
    radarAngle+=0.25
    if (radarAngle == 360):
        radarAngle=1

    pygame.display.flip()


pygame.init()
# set display size
lcd = pygame.display.set_mode((800,600))
pygame.mouse.set_visible(False)

planeAngle=45
planeDistance=35
maxPlaneDistance=80

radarAngle=0
radarBlipGamma=255
oldBlipAngle=0
oldBlipDistance=0


idx=0
while True:
    drawRadarLine(lcd,200,150,80,planeAngle,planeDistance,maxPlaneDistance)
    idx+=1
    if (idx % 1000 == 0):
        planeDistance+=5
        planeAngle-=3


