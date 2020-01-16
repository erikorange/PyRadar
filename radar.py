import pygame
import time
import math


def drawRadarLine(lcd,xCenter,yCenter,angle):
    lcd.fill((0,0,0))
    pygame.draw.circle(lcd, (0,64,0), (xCenter,yCenter), 160, 1)
    radar_len = 150
    x = xCenter + math.cos(math.radians(angle)) * radar_len
    y = yCenter + math.sin(math.radians(angle)) * radar_len
    pygame.draw.line(lcd, (0,64,0), (xCenter, yCenter), (x,y), 1)
    pygame.display.update()

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

def plot(screen, angle, radius):
    x1=radius*math.cos(math.radians(angle))
    y1=radius*math.sin(math.radians(angle))

    x=y1
    y=-x1
    pygame.draw.circle(screen, (0,255, 0), (400+int(x),300+int(y)), 2)

pygame.init()
# set display size
lcd = pygame.display.set_mode((800,600))
pygame.mouse.set_visible(False)
lcd.fill((0,0,0))

pygame.draw.circle(lcd, (0,255,0), (400,300), 160, 1)
while True:
    for x in range(360):
        drawRadarLine(lcd,400,300,x)
        plot(lcd,x,100)
        pygame.display.update()
        time.sleep(0.01)




