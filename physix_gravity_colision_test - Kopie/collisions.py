import math
import numpy as numpy
import Config
import Quadtree

def col(display, arr):
    if len(arr) < 10:
        checkObjCollision(arr)
    else:
        Quadtree.quadColl(Quadtree.main(display, arr))


def checkfAndResoveBorderCollision(obj, deltaT):
    speedCorrectionValue = 0 #Objekt zu schnell, da es im Boden beschleunigt wurde

    if obj.position[0]-obj.radius < 0 and obj.velocity[0] < 0:
        obj.velocity[0] = obj.velocity[0] * -1 * Config.ENERGYLOSS_ON_COLISION

        obj.position[0] = obj.position[0] - (obj.position[0] - obj.radius)

    elif obj.position[0] + obj.radius > Config.SCREENWIDTH and obj.velocity[0] > 0:
        obj.velocity[0] = obj.velocity[0] * -1 * Config.ENERGYLOSS_ON_COLISION

        obj.position[0] = obj.position[0] - ((obj.position[0] + obj.radius) - Config.SCREENWIDTH)


    if obj.position[1]-obj.radius < 0 and obj.velocity[1]<0:
        obj.velocity[1] = obj.velocity[1] * -1 * Config.ENERGYLOSS_ON_COLISION

        obj.position[1] = obj.position[1] - (obj.position[1] - obj.radius)

    elif obj.position[1]+obj.radius > Config.SCREENHEIGHT and obj.velocity[1]>0:
        penetrationDepth = ((obj.position[1] + obj.radius) - Config.SCREENHEIGHT)
        #obj.velocity[1] = -1*(math.sqrt(2*Blablabla.GRAVITY * (Blablabla.SCREENHEIGHT-(obj.radius+obj.previousPosition[1])))+obj.previousVelocity[1])
        obj.velocity[1] = -1*(math.sqrt(abs(math.pow(obj.previousVelocity[1], 2)+2*Config.GRAVITY*(Config.SCREENHEIGHT-(obj.radius+obj.previousPosition[1]))))) * Config.ENERGYLOSS_ON_COLISION
        obj.velocity[0] *= Config.ENERGYLOSS_ON_COLISION
        obj.position[1] = obj.position[1] - penetrationDepth
def checkBorderCol(obj):
    if obj.position[0] - obj.radius < 0 and obj.velocity[0] < 0:
        return 1
    elif obj.position[0] + obj.radius > Config.SCREENWIDTH and obj.velocity[0] > 0:
        return 1

    if obj.position[1] - obj.radius < 0 and obj.velocity[1] < 0:
        return 1
    elif obj.position[1] + obj.radius > Config.SCREENHEIGHT and obj.velocity[1] > 0:
        return 1
    else:
        return 0


def growObj(sqrDst, obj1, obj2, objects, physArr, i):
    if sqrDst <= obj1.radius + physArr[i].radius and obj1 != physArr[i]:
        obj1.radius += 0.005
        obj1.mass += physArr[i].mass * 0.001
        objects.remove(obj2)
        physArr.remove(obj2)

def checkObjCollision(objects):
    #print(objects)
    length = len(objects)
    for i in range(length):
        for q in range(length):
            if i == q:
                continue

            a = (objects[i].position[0] - objects[q].position[0])
            b = (objects[i].position[1] - objects[q].position[1])
            if objects[i].radius + objects[q].radius > math.sqrt(a*a + b*b):
                #print("boing", Blablabla.collisionCounter)
                #Blablabla.collisionCounter += 1
                calculateNewVelocities(objects[i], objects[q])

def gravityBetweenTwoObjs(obj1, obj2):
    F = Config.G*(obj1.mass*obj2.mass)/(abs((obj1.position[0]-obj2.position[0])*(obj1.position[1]-obj2.position[1])))
    pass

def gravityAroundImmovable(immovable, obj, deltaTime):
    if immovable == obj:
        return
    a = immovable.position[0] - obj.position[0]
    b = immovable.position[1] - obj.position[1]
    sqrDst = math.sqrt(a*a+b*b)
    if sqrDst<= immovable.radius + obj.radius:
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

def checkObjCollisionPair(objects, neighborObjects):
    #print(objects)
    length = len(objects)
    if length == 2:
        a = (objects[0].position[0] - objects[1].position[0])
        b = (objects[0].position[1] - objects[1].position[1])
        if objects[0].radius + objects[1].radius > math.sqrt(a * a + b * b):
            #print("boing", Blablabla.collisionCounter)
            #Blablabla.collisionCounter += 1
            if objects[0].immovable == True or objects[1].immovable == True:
                if objects[0].immovable == True:
                    calculateNewVelocitiesImmovable(objects[0], objects[1])
                else:
                    calculateNewVelocitiesImmovable(objects[1], objects[0])
            else:
                calculateNewVelocities(objects[0], objects[1])

    for i in range(length):
        for q in range(len(neighborObjects)):
            if objects[i] == neighborObjects[q]:
                #print("ölkasjf")
                #print("obj: ",objects)
                #print(neighborObjects)
                continue
            a = (objects[i].position[0] - neighborObjects[q].position[0])
            b = (objects[i].position[1] - neighborObjects[q].position[1])
            if objects[i].radius + neighborObjects[q].radius > math.sqrt(a*a + b*b):
                if neighborObjects[q].immovable == True or objects[i].immovable == True:
                    if objects[i].immovable == True:
                        calculateNewVelocitiesImmovable(objects[i], neighborObjects[q])
                    else:
                        calculateNewVelocitiesImmovable(neighborObjects[q], objects[i])
                #print("klack", Blablabla.collisionCounter)
                #Blablabla.collisionCounter += 1
                else:
                    calculateNewVelocities(objects[i], neighborObjects[q])

def calculateNewVelocitiesImmovable(immovable, obj2):
    pass

def calculateNewVelocities(obj1, obj2):
    normalVector = getNormalVector(obj1, obj2)
    normalLength = math.sqrt(normalVector[0]*normalVector[0] + normalVector[1]*normalVector[1])
    ###########################################
    #nur temporär Lösung:
    #bei Erschaffung on objs: keine Duplikate --> check if obj mit gleichen Pos. ist in Liste
    #Quadtree fixen: Duplikate in Quadtree, vllt weil Überschneidungen auftreten(?)
    if normalLength == 0:
        return
    #########################################
    unitNormalVector = [normalVector[0]/normalLength, normalVector[1]/normalLength]

    a = (obj1.position[0] - obj2.position[0])
    b = (obj1.position[1] - obj2.position[1])

    displacementfactor = (obj1.radius + obj2.radius - math.sqrt(a * a + b * b)) / 2
    displacement = [displacementfactor * unitNormalVector[0], displacementfactor * unitNormalVector[1]]
    position1 = [obj1.position[0] + displacement[0], obj1.position[1] + displacement[1]]
    position2 = [obj2.position[0] - displacement[0], obj2.position[1] - displacement[1]]

    #normalvector
    normalVector = [position1[0] - position2[0], position1[1] - position2[1]]
    normalLength = math.sqrt(normalVector[0] * normalVector[0] + normalVector[1] * normalVector[1])
    unitNormalVector = [normalVector[0] / normalLength, normalVector[1] / normalLength]
    unitTangentVector = [-unitNormalVector[1], unitNormalVector[0]]

    v1n = numpy.dot(unitNormalVector, obj1.velocity)
    v1t = numpy.dot(unitTangentVector, obj1.velocity)
    v2n = numpy.dot(unitNormalVector, obj2.velocity)
    v2t = numpy.dot(unitTangentVector, obj2.velocity)

    newv1n = (v1n*(obj1.mass-obj2.mass)+2*obj2.mass*v2n)/(obj1.mass+obj2.mass)
    newv2n = (v2n*(obj2.mass-obj1.mass)+2*obj1.mass*v1n)/(obj1.mass+obj2.mass)

    newv1n = [newv1n * unitNormalVector[0], newv1n * unitNormalVector[1]]
    newv2n = [newv2n * unitNormalVector[0], newv2n * unitNormalVector[1]]
    newv1t = [v1t * unitTangentVector[0], v1t * unitTangentVector[1]]
    newv2t = [v2t * unitTangentVector[0], v2t * unitTangentVector[1]]

    #finalVel1 = [(newv1n[0] + newv1t[0])*Blablabla.ENERGYLOSS_ON_COLISION, (newv1n[1] + newv1t[1])*Blablabla.ENERGYLOSS_ON_COLISION]
    #finalVel2 = [(newv2n[0] + newv2t[0])*Blablabla.ENERGYLOSS_ON_COLISION, (newv2n[1] + newv2t[1])*Blablabla.ENERGYLOSS_ON_COLISION]
    finalVel1 = [(newv1n[0] + newv1t[0]),
                 (newv1n[1] + newv1t[1])]
    finalVel2 = [(newv2n[0] + newv2t[0]),
                 (newv2n[1] + newv2t[1])]
    a = (obj1.position[0] - obj2.position[0])
    b = (obj1.position[1] - obj2.position[1])

    displacementfactor = ((obj1.radius + obj2.radius - math.sqrt(a * a + b * b)) / 2 )+ 1#mit + ein paar Pixel, damit collision nicht 2 Mal getriggert wird
    displacement = [displacementfactor * unitNormalVector[0], displacementfactor * unitNormalVector[1]]
    obj1.position = [obj1.position[0] + displacement[0], obj1.position[1] + displacement[1]]
    obj2.position = [obj2.position[0] - displacement[0], obj2.position[1] - displacement[1]]

    obj1.velocity = finalVel1
    obj2.velocity = finalVel2


def getNormalVector(obj1, obj2):
    return [obj1.position[0]-obj2.position[0], obj1.position[1]-obj2.position[1]]

"""
def checkfAndResoveBorderCollision(objects):
    for i in range(len(objects)):
        if objects[i].position[0]-objects[i].radius <= 0 and objects[i].velocity[0] < 0:
            objects[i].velocity[0] = objects[i].velocity[0]*-1 * Blablabla.ENERGYLOSS_ON_COLISION

            objects[i].position[0] = objects[i].position[0] - (objects[i].position[0] - objects[i].radius)

        elif objects[i].position[0] + objects[i].radius >= Blablabla.SCREENWIDTH and objects[i].velocity[0]>0:
            objects[i].velocity[0] = objects[i].velocity[0]*-1 * Blablabla.ENERGYLOSS_ON_COLISION

            objects[i].position[0] = objects[i].position[0] - ((objects[i].position[0] + objects[i].radius) - Blablabla.SCREENWIDTH)


        if objects[i].position[1]-objects[i].radius <= 0 and objects[i].velocity[1]<0:
            objects[i].velocity[1] = objects[i].velocity[1]*-1 * Blablabla.ENERGYLOSS_ON_COLISION

            objects[i].position[1] = objects[i].position[1] - (objects[i].position[1] - objects[i].radius)

        elif objects[i].position[1]+objects[i].radius >= Blablabla.SCREENHEIGHT and objects[i].velocity[1]>0:
            objects[i].velocity[1] = objects[i].velocity[1]*-1 * Blablabla.ENERGYLOSS_ON_COLISION

            objects[i].position[1] = objects[i].position[1] - ((objects[i].position[1] + objects[i].radius) - Blablabla.SCREENHEIGHT)
"""

def getDistance(obj1, obj2):
    return math.sqrt(math.pow(abs(obj1.position[0]-obj2.position[0]),2) + math.pow(abs(obj1.position[1]-obj2.position[1]), 2))
