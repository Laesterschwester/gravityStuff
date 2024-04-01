import pygame
import copy
import Config
import collisions
import main
import math

def drawArr(arr):
    for object in arr:
        object.drawObjs()

class Obj:
    radius = Config.RADIUS
    #erstes Argument Display entfernt. auch bei initialisierungsaufruf natürlich
    def __init__(self, position, mass=None, radius=None, velocity=None, color=None, immovable=None):
        #self.display = display
        self.position = position
        self.previousPosition = position
        if color:
            self.color = color
        else:
            self.color = Config.BLACK
        if mass:
            self.mass = mass
        else:
            self.mass = 10

        if radius:
            self.radius = radius
        else:
            self.radius = Config.RADIUS
        if velocity:
            self.velocity = velocity
            self.previousVelocity = velocity
        else:
            self.velocity = [3, 0]
            self.previousVelocity = [3, 0]
        self.kinE = 1/2*self.mass*(self.velocity[0]+self.velocity[1])**2
        self.move = True
        if immovable:
            self.immovable = immovable
        else:
            self.immovable = False
    def updatePos(self, deltaTime):
         #könnte man vllt auf quadtree auslagern


        self.previousVelocity = copy.copy(self.velocity)
        self.previousPosition = copy.copy(self.position)

        self.position[0] += self.velocity[0] * deltaTime
        self.velocity[1] = self.velocity[1] + Config.GRAVITY * deltaTime
        self.position[1] += self.velocity[1] * deltaTime

        #collisions.checkfAndResoveBorderCollision(self, deltaTime)
        #self.gravity(deltaTime)
        #pygame.draw.circle(main.display, self.color, self.position, self.radius)

    def drawObjs(self):

        speed = math.sqrt(self.velocity[0]**2+self.velocity[1]**2)
        """r = 200 * 1/(1+1.1**(-speed+50))
        b = 200 * 1/(1+1.1**(speed-40))
        print(speed)"""
        #r = min(200*0.01*speed, 255)
        #b = max(200*-0.01*speed+1, 10)

        r = min(0.01 * speed, 1)*200
        b = max(-0.01 * speed + 1, 0)*100
        color = (r, 40, b)
        pygame.draw.circle(main.display, color, self.position, self.radius)

