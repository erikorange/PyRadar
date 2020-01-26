import pygame
import time
import math
from radar import Radar



rdr = Radar()

planeAngle=45
planeDistance=35
maxPlaneDistance=200

rdr.setup(400,200,150)

idx=0
while True:
    rdr.update(planeAngle,planeDistance,maxPlaneDistance)
    idx+=1
    if (idx % 10 == 0):
        planeDistance+=1
        planeAngle-=3


