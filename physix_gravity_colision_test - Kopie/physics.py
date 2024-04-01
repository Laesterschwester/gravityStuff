import Config
import math

def pendulumTether():
    pass


def springForce(obj1, obj2, deltaT, restDist, springConst):
    a = (obj1.position[0]-obj2.position[0])
    b = (obj1.position[1]-obj2.position[1])
    distance = math.sqrt(a**2+b**2)
    if distance==0:
        return
    obj1obj2VectorNormal = [-a/distance, -b/distance]
    obj2obj1VectorNormal = [a/distance, b/distance]
    x = restDist - distance
    F = -springConst*x
    #wird die Kraft auf beide aufgeteilt oder wird sie auf beide gerechnet?
    obj1.velocity[0] += F*obj1obj2VectorNormal[0]*deltaT*0.0001
    obj1.velocity[1] += F*obj1obj2VectorNormal[1]*deltaT*0.0001
    obj2.velocity[0] += F*obj2obj1VectorNormal[0]*deltaT*0.0001
    obj2.velocity[1] += F*obj2obj1VectorNormal[1]*deltaT*0.0001

    #Energieverlust
    """obj1.velocity[0] *= 0.999
    obj1.velocity[1] *= 0.999
    obj2.velocity[0] *= 0.999
    obj2.velocity[1] *= 0.999"""
    #wars des schon?

    pass

def gravity(self, deltaTime):
    gravity = Config.GRAVITY
    self.velocity[1] = self.velocity[1] + gravity * deltaTime



def gravityBetweenTwoObjs(obj1, obj2, deltaTime):
    if obj1 == obj2:
        return
    a = obj1.position[0] - obj2.position[0]
    b = obj1.position[1] - obj2.position[1]
    sqrDst = math.sqrt(a*a+b*b)
    if sqrDst <= obj1.radius + obj2.radius:
        return
    forceDir1 = [a/sqrDst, b/sqrDst]
    forceDir2 = [-a/sqrDst, -b/sqrDst]

    force1 = [forceDir1[0] * Config.G * obj2.mass * obj1.mass / sqrDst, forceDir1[1] * Config.G * obj2.mass * obj1.mass / sqrDst]
    acceleration1 = [force1[0] / obj1.mass, force1[1] / obj1.mass]

    force2 = [forceDir2[0] * Config.G * obj2.mass * obj1.mass / sqrDst, forceDir2[1] * Config.G * obj2.mass * obj1.mass / sqrDst]
    acceleration2 = [force2[0] / obj2.mass, force2[1] / obj2.mass]

    obj1.velocity[0] += acceleration1[0] * deltaTime
    obj1.velocity[1] += acceleration1[1] * deltaTime

    obj2.velocity[0] += acceleration2[0] * deltaTime
    obj2.velocity[1] += acceleration2[1] * deltaTime

def gravityAll(arr, deltaTime):
    for i in arr:
        for j in arr:
            if i == j:
                continue
            gravityAroundImmovable(i, j, deltaTime)

def gravityAroundImmovable(immovable, obj, deltaTime):
    if immovable == obj:
        return
    a = immovable.position[0] - obj.position[0]
    b = immovable.position[1] - obj.position[1]
    sqrDst = math.sqrt(a*a+b*b)
    if sqrDst <= immovable.radius + obj.radius:
        return
    forceDir = [a/sqrDst, b/sqrDst]
    force = [forceDir[0]*Config.G*obj.mass*immovable.mass/sqrDst, forceDir[1]*Config.G*obj.mass*immovable.mass/sqrDst]
    acceleration = [force[0]/obj.mass, force[1]/obj.mass]
    obj.velocity[0] += acceleration[0] * deltaTime
    obj.velocity[1] += acceleration[1] * deltaTime

def repulsionAroundImmovable(immovable, obj, deltaTime):
    if immovable == obj:
        return
    divisor = math.sqrt((immovable.position[0] - obj.position[0])**2 + (immovable.position[1] - obj.position[1])**2)
    if divisor == 0:
        return
    F = Config.G * (immovable.mass * obj.mass) / divisor
    vector = [obj.position[0] - immovable.position[0], obj.position[1] - immovable.position[1]]
    vectorLength = math.sqrt(vector[0]**2+vector[1]**2)
    acceleration = [F*vector[0]/vectorLength, F*vector[1]/vectorLength] #F*normalvector
    obj.velocity[0] += acceleration[0]
    obj.velocity[1] += acceleration[1]