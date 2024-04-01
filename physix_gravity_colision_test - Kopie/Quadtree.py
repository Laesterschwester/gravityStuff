from random import randint

import pygame
import Config
import collisions

quadList = []
globalhead = None

class Node:
    def __init__(self, objs=None, width=None, height=None, position=None, previousNode=None, locationCode=None):
        self.topLeft = None
        self.topRight = None
        self.bottomLeft = None
        self.bottomRight = None
        self.previousNode = previousNode
        self.width = width
        self.height = height
        self.position = position
        self.objs = objs
        self.locationCode = locationCode

    def __len__(self):
        if self.objs:
            """print(self.objs)
            print(len(self.objs))"""
            return len(self.objs)
        else:
            return 0

    def __getitem__(self):
        return self.objs


class Quadtree:
    def __init__(self, head):
        self.head = head


    def initQuadtree(self, points, curr, display):
        if len(points) > 2:
            if Config.DRAW_QUADTREE:
                pygame.draw.rect(display, (0, 0, 0), (curr.position[0], curr.position[1], curr.width, curr.height), 3)

            newWidth = curr.width/2
            newHeight = curr.height/2

            """#nur node erstellen, wenn auch was rein kommt
            topLeft = []
            bottomRight = []
            bottomLeft = []
            topRight = []
            for i in range(len(points)):
                if points[i].position[0] < curr.position[0] + newWidth:
                    if points[i].position[1] < curr.position[1] + newHeight:
                        if curr.topLeft == None:
                            curr.topLeft = Node(None, newWidth, newHeight, curr.position, curr,
                                                (str(curr.locationCode) + '1') if curr.locationCode != None else 1)
                        topLeft.append(points[i])
                    else:
                        if curr.bottomLeft == None:
                            curr.bottomLeft = Node(None, newWidth, newHeight,
                                                   [curr.position[0], curr.position[1] + newHeight], curr,
                                                   (str(curr.locationCode) + '3') if curr.locationCode != None else 3)
                        bottomLeft.append(points[i])
                else:
                    if points[i].position[1] < curr.position[1] + newHeight:
                        if curr.topRight == None:
                            curr.topRight = Node(None, newWidth, newHeight,
                                                 [curr.position[0] + newWidth, curr.position[1]], curr,
                                                 (str(curr.locationCode) + '2') if curr.locationCode != None else 2)
                        topRight.append(points[i])
                    else:
                        if curr.bottomRight == None:
                            curr.bottomRight = Node(None, newWidth, newHeight,
                                                    [curr.position[0] + newWidth, curr.position[1] + newHeight], curr,
                                                    (str(curr.locationCode) + '4') if curr.locationCode != None else 4)
                        bottomRight.append(points[i])
            #print("die neuen arrays: ", topLeft, "\n", bottomLeft, "\n", bottomRight, "\n", bottomLeft)
            print("points: ", points)
            print("topRight", topRight)
            print("topLeft ", topLeft)
            print("bottomRight", bottomRight)
            print("bottomLeft", bottomLeft)
            if curr.topRight != None:
                self.initQuadtree(topRight, curr.topRight, display)
            if curr.topLeft != None:
                self.initQuadtree(topLeft, curr.topLeft, display)
            if curr.bottomRight != None:
                self.initQuadtree(bottomRight, curr.bottomRight, display)
            if curr.bottomLeft != None:
                self.initQuadtree(bottomLeft, curr.bottomLeft, display)"""

            curr.topLeft = Node(None, newWidth, newHeight, curr.position, curr, (str(curr.locationCode)+'1')if curr.locationCode!=None else 1)
            curr.topRight = Node(None, newWidth, newHeight, [curr.position[0]+newWidth, curr.position[1]], curr, (str(curr.locationCode)+'2')if curr.locationCode!=None else 2)
            curr.bottomLeft = Node(None, newWidth, newHeight, [curr.position[0], curr.position[1]+newHeight], curr, (str(curr.locationCode)+'3')if curr.locationCode!=None else 3)
            curr.bottomRight = Node(None, newWidth, newHeight, [curr.position[0]+newWidth, curr.position[1]+newHeight], curr, (str(curr.locationCode)+'4')if curr.locationCode!=None else 4)

            topRight = []
            topLeft = []
            bottomRight = []
            bottomLeft = []
            for i in range(len(points)):
                if points[i].position[0] < curr.position[0]+newWidth:
                    if points[i].position[1] < curr.position[1]+newHeight:
                        topLeft.append(points[i])
                    else:
                        bottomLeft.append(points[i])
                else:
                    if points[i].position[1] < curr.position[1]+newHeight:
                        topRight.append(points[i])
                    else:
                        bottomRight.append(points[i])
            #print("die neuen arrays: ", topLeft,"\n", bottomLeft,"\n", bottomRight,"\n", bottomLeft)
            
            self.initQuadtree(topRight, curr.topRight, display)
            self.initQuadtree(topLeft, curr.topLeft, display)
            self.initQuadtree(bottomRight, curr.bottomRight, display)
            self.initQuadtree(bottomLeft, curr.bottomLeft, display)
        else:
            curr.objs = points
            # leere nodes ignorieren
            if points:
                quadList.append(curr)

            if Config.DRAW_QUADTREE:
                pygame.draw.rect(display, (0, 0, 0), (curr.position[0], curr.position[1], curr.width, curr.height), 1)
            #quadList.append((curr.locationCode, curr)) #vllt nur curr übergeben?

            #print("##################################################")
            #if curr.objs:
                #print("velocity: ", curr.objs[0].velocity)
            #print(curr.locationCode)
            #print("neighbors: ")
            #print(allNeighbors(int(curr.locationCode)))

def quadColl(list):
    # startet bei niedrigster Node und holt sich den rechten, den unteren und den unten rechts Nachbarn und speichert diese in einem Array, das dann dem colCheck übergeben wird
    # rekursiv für ALLE Blattknoten
    for i in range(len(quadList)):
    #for i in range(len(quadList)):
        #curr = quadList[i]
        curr = quadList[i]
        neighbors = []

        # l == 1, lu == 2, u == 3; ur == 4, r == 5, rd == 6, d == 7, dl == 8

        leftLocCode = findNeighborsLocationCode(int(curr.locationCode), 1, 1)
        topLeftLocCode = findNeighborsLocationCode(int(curr.locationCode), 2, 1)
        upLocCode = findNeighborsLocationCode(int(curr.locationCode), 3, 1)
        topRightLocCode = findNeighborsLocationCode(int(curr.locationCode), 4, 1)
        rightLocCode = findNeighborsLocationCode(int(curr.locationCode), 5, 1)
        bottomRightLocCode = findNeighborsLocationCode(int(curr.locationCode), 6, 1)
        downLocCode = findNeighborsLocationCode(int(curr.locationCode), 7, 1)
        bottomLeftLocCode = findNeighborsLocationCode(int(curr.locationCode), 8, 1)
        #print("currentNode#################################################################################################", curr.position)
        #print("startLocCode: ", curr.locationCode)
        #print("rightLocCode: ", rightLocCode)
        #print("leftLocCode: ", leftLocCode)
        #print("upLocCode: ", upLocCode)
        #print("downLocCode: ", downLocCode)
        #print("topLeft: ", topLeftLocCode)
        #print("topRight: ", topRightLocCode)
        #print("bottomLeft: ", bottomLeftLocCode)
        #print("bottomRight: ", bottomRightLocCode)

        #hier theoretisch die korrekten locCodes und doppelte ignorieren. es kann passieren, dass ein großer Nachbar mehrfach hinzugefügt wird...
        if upLocCode:
            objs = getNeighborNodeObjsUp(upLocCode)
            if objs:
                neighbors += objs
        if rightLocCode:
            objs = getNeighborNodeObjsR(rightLocCode)
            if objs:
                neighbors += objs
        if downLocCode:
            objs = getNeighborNodeObjsD(downLocCode)
            if objs:
                neighbors += objs
        if leftLocCode:
            objs = getNeighborNodeObjsL(leftLocCode)
            if objs:
                neighbors += objs
        if bottomLeftLocCode:
            objs = getNeighborNodeObjsDL(bottomLeftLocCode)
            if objs:
                neighbors += objs
        if bottomRightLocCode:
            objs = getNeighborNodeObjsDR(bottomRightLocCode)
            if objs:
                neighbors += objs
        if topLeftLocCode:
            objs = getNeighborNodeObjsUL(topLeftLocCode)
            if objs:
                neighbors += objs
        if topRightLocCode:
            objs = getNeighborNodeObjsUR(topRightLocCode)
            if objs:
                neighbors += objs
        """if upLocCode:
            neighbors += getNeighborNodeObjsUp(upLocCode)
        if rightLocCode:
            neighbors += getNeighborNodeObjsR(rightLocCode)
        if downLocCode:
            neighbors += getNeighborNodeObjsD(downLocCode)
        if leftLocCode:
            neighbors += getNeighborNodeObjsL(leftLocCode)
        if bottomLeftLocCode:
            neighbors += getNeighborNodeObjsDL(bottomLeftLocCode)
        if bottomRightLocCode:
            neighbors += getNeighborNodeObjsDR(bottomRightLocCode)
        if topLeftLocCode:
            neighbors += getNeighborNodeObjsUL(topLeftLocCode)
        if topRightLocCode:
            neighbors += getNeighborNodeObjsUR(topRightLocCode)
"""
        # print("neighbors", neighbors)
        #collisions.checkObjCollision(neighbors)
        collisions.checkObjCollisionPair(curr.objs, neighbors)

def quadCollPP(list):
    # startet bei niedrigster Node und holt sich den rechten, den unteren und den unten rechts Nachbarn und speichert diese in einem Array, das dann dem colCheck übergeben wird
    # rekursiv für ALLE Blattknoten
    #for i in range(len(list)):
    #for i in range(len(quadList)):
    #curr = quadList[i]
    print(list)
    curr = list
    neighbors = []

    # l == 1, lu == 2, u == 3; ur == 4, r == 5, rd == 6, d == 7, dl == 8

    leftLocCode = findNeighborsLocationCode(int(curr.locationCode), 1, 1)
    topLeftLocCode = findNeighborsLocationCode(int(curr.locationCode), 2, 1)
    upLocCode = findNeighborsLocationCode(int(curr.locationCode), 3, 1)
    topRightLocCode = findNeighborsLocationCode(int(curr.locationCode), 4, 1)
    rightLocCode = findNeighborsLocationCode(int(curr.locationCode), 5, 1)
    bottomRightLocCode = findNeighborsLocationCode(int(curr.locationCode), 6, 1)
    downLocCode = findNeighborsLocationCode(int(curr.locationCode), 7, 1)
    bottomLeftLocCode = findNeighborsLocationCode(int(curr.locationCode), 8, 1)
    #print("currentNode#################################################################################################", curr.position)
    #print("startLocCode: ", curr.locationCode)
    #print("rightLocCode: ", rightLocCode)
    #print("leftLocCode: ", leftLocCode)
    #print("upLocCode: ", upLocCode)
    #print("downLocCode: ", downLocCode)
    #print("topLeft: ", topLeftLocCode)
    #print("topRight: ", topRightLocCode)
    #print("bottomLeft: ", bottomLeftLocCode)
    #print("bottomRight: ", bottomRightLocCode)

    #hier theoretisch die korrekten locCodes und doppelte ignorieren. es kann passieren, dass ein großer Nachbar mehrfach hinzugefügt wird...
    if upLocCode:
        objs = getNeighborNodeObjsUp(upLocCode)
        if objs:
            neighbors += objs
    if rightLocCode:
        objs = getNeighborNodeObjsR(rightLocCode)
        if objs:
            neighbors += objs
    if downLocCode:
        objs = getNeighborNodeObjsD(downLocCode)
        if objs:
            neighbors += objs
    if leftLocCode:
        objs = getNeighborNodeObjsL(leftLocCode)
        if objs:
            neighbors += objs
    if bottomLeftLocCode:
        objs = getNeighborNodeObjsDL(bottomLeftLocCode)
        if objs:
            neighbors += objs
    if bottomRightLocCode:
        objs = getNeighborNodeObjsDR(bottomRightLocCode)
        if objs:
            neighbors += objs
    if topLeftLocCode:
        objs = getNeighborNodeObjsUL(topLeftLocCode)
        if objs:
            neighbors += objs
    if topRightLocCode:
        objs = getNeighborNodeObjsUR(topRightLocCode)
        if objs:
            neighbors += objs
    """if upLocCode:
        neighbors += getNeighborNodeObjsUp(upLocCode)
    if rightLocCode:
        neighbors += getNeighborNodeObjsR(rightLocCode)
    if downLocCode:
        neighbors += getNeighborNodeObjsD(downLocCode)
    if leftLocCode:
        neighbors += getNeighborNodeObjsL(leftLocCode)
    if bottomLeftLocCode:
        neighbors += getNeighborNodeObjsDL(bottomLeftLocCode)
    if bottomRightLocCode:
        neighbors += getNeighborNodeObjsDR(bottomRightLocCode)
    if topLeftLocCode:
        neighbors += getNeighborNodeObjsUL(topLeftLocCode)
    if topRightLocCode:
        neighbors += getNeighborNodeObjsUR(topRightLocCode)
"""
    # print("neighbors", neighbors)
    #collisions.checkObjCollision(neighbors)
    collisions.checkObjCollisionPair(curr.objs, neighbors)

def getNeighborNodeObjsUp(neighborLocCode):
    neighborLocCode = str(neighborLocCode)
    #vllt übergeben als jedes Mal auslesen?
    currNode = globalhead
    for i in neighborLocCode:
        neighborCode = i
        if neighborCode < '3':
            if neighborCode == '1':
                if currNode.topLeft != None:
                    currNode = currNode.topLeft
                else:
                    return neighborRecU(currNode)
            else:
                if currNode.topRight != None:
                    currNode = currNode.topRight
                else:
                    return neighborRecU(currNode)
        else:
            if neighborCode == '3':
                if currNode.bottomLeft != None:
                    currNode = currNode.bottomLeft
                else:
                    return neighborRecU(currNode)
            else:
                if currNode.bottomRight != None:
                    currNode = currNode.bottomRight
                else:
                    return neighborRecU(currNode)
    return neighborRecU(currNode)
def getNeighborNodeObjsR(neighborLocCode):
    neighborLocCode = str(neighborLocCode)
    #vllt übergeben als jedes Mal auslesen?
    currNode = globalhead
    for i in neighborLocCode:
        neighborCode = i
        if neighborCode < '3':
            if neighborCode == '1':
                if currNode.topLeft != None:
                    currNode = currNode.topLeft
                else:
                    return neighborRecR(currNode)
            else:
                if currNode.topRight != None:
                    currNode = currNode.topRight
                else:
                    return neighborRecR(currNode)
        else:
            if neighborCode == '3':
                if currNode.bottomLeft != None:
                    currNode = currNode.bottomLeft
                else:
                    return neighborRecR(currNode)
            else:
                if currNode.bottomRight != None:
                    currNode = currNode.bottomRight
                else:
                    return neighborRecR(currNode)
    return neighborRecR(currNode)
def getNeighborNodeObjsD(neighborLocCode):
    neighborLocCode = str(neighborLocCode)
    #vllt übergeben als jedes Mal auslesen?
    currNode = globalhead
    for i in neighborLocCode:
        neighborCode = i
        if neighborCode < '3':
            if neighborCode == '1':
                if currNode.topLeft != None:
                    currNode = currNode.topLeft
                else:
                    return neighborRecD(currNode)
            else:
                if currNode.topRight != None:
                    currNode = currNode.topRight
                else:
                    return neighborRecD(currNode)
        else:
            if neighborCode == '3':
                if currNode.bottomLeft != None:
                    currNode = currNode.bottomLeft
                else:
                    return neighborRecD(currNode)
            else:
                if currNode.bottomRight != None:
                    currNode = currNode.bottomRight
                else:
                    return neighborRecD(currNode)
    return neighborRecD(currNode)
def getNeighborNodeObjsL(neighborLocCode):
    neighborLocCode = str(neighborLocCode)
    #vllt übergeben als jedes Mal auslesen?
    currNode = globalhead
    for i in neighborLocCode:
        neighborCode = i
        if neighborCode < '3':
            if neighborCode == '1':
                if currNode.topLeft != None:
                    currNode = currNode.topLeft
                else:
                    return neighborRecL(currNode)
            else:
                if currNode.topRight != None:
                    currNode = currNode.topRight
                else:
                    return neighborRecL(currNode)
        else:
            if neighborCode == '3':
                if currNode.bottomLeft != None:
                    currNode = currNode.bottomLeft
                else:
                    return neighborRecL(currNode)
            else:
                if currNode.bottomRight != None:
                    currNode = currNode.bottomRight
                else:
                    return neighborRecL(currNode)
    return neighborRecL(currNode)
def getNeighborNodeObjsUL(neighborLocCode):
    neighborLocCode = str(neighborLocCode)
    #vllt übergeben als jedes Mal auslesen?
    currNode = globalhead
    for i in neighborLocCode:
        neighborCode = i
        if neighborCode < '3':
            if neighborCode == '1':
                if currNode.topLeft != None:
                    currNode = currNode.topLeft
                else:
                    return neighborRecLu(currNode)
            else:
                if currNode.topRight != None:
                    currNode = currNode.topRight
                else:
                    return neighborRecLu(currNode)
        else:
            if neighborCode == '3':
                if currNode.bottomLeft != None:
                    currNode = currNode.bottomLeft
                else:
                    return neighborRecLu(currNode)
            else:
                if currNode.bottomRight != None:
                    currNode = currNode.bottomRight
                else:
                    return neighborRecLu(currNode)
    return neighborRecLu(currNode)
def getNeighborNodeObjsUR(neighborLocCode):
    neighborLocCode = str(neighborLocCode)
    #vllt übergeben als jedes Mal auslesen?
    currNode = globalhead
    for i in neighborLocCode:
        neighborCode = i
        if neighborCode < '3':
            if neighborCode == '1':
                if currNode.topLeft != None:
                    currNode = currNode.topLeft
                else:
                    return neighborRecRu(currNode)
            else:
                if currNode.topRight != None:
                    currNode = currNode.topRight
                else:
                    return neighborRecRu(currNode)
        else:
            if neighborCode == '3':
                if currNode.bottomLeft != None:
                    currNode = currNode.bottomLeft
                else:
                    return neighborRecRu(currNode)
            else:
                if currNode.bottomRight != None:
                    currNode = currNode.bottomRight
                else:
                    return neighborRecRu(currNode)
    return neighborRecRu(currNode)
def getNeighborNodeObjsDR(neighborLocCode):
    neighborLocCode = str(neighborLocCode)
    #vllt übergeben als jedes Mal auslesen?
    currNode = globalhead
    for i in neighborLocCode:
        neighborCode = i
        if neighborCode < '3':
            if neighborCode == '1':
                if currNode.topLeft != None:
                    currNode = currNode.topLeft
                else:
                    return neighborRecRd(currNode)
            else:
                if currNode.topRight != None:
                    currNode = currNode.topRight
                else:
                    return neighborRecRd(currNode)
        else:
            if neighborCode == '3':
                if currNode.bottomLeft != None:
                    currNode = currNode.bottomLeft
                else:
                    return neighborRecRd(currNode)
            else:
                if currNode.bottomRight != None:
                    currNode = currNode.bottomRight
                else:
                    return neighborRecRd(currNode)
    return neighborRecRd(currNode)
def getNeighborNodeObjsDL(neighborLocCode):
    neighborLocCode = str(neighborLocCode)
    #vllt übergeben als jedes Mal auslesen?
    currNode = globalhead
    for i in neighborLocCode:
        neighborCode = i
        if neighborCode < '3':
            if neighborCode == '1':
                if currNode.topLeft != None:
                    currNode = currNode.topLeft
                else:
                    return neighborRecL(currNode)
            else:
                if currNode.topRight != None:
                    currNode = currNode.topRight
                else:
                    return neighborRecL(currNode)
        else:
            if neighborCode == '3':
                if currNode.bottomLeft != None:
                    currNode = currNode.bottomLeft
                else:
                    return neighborRecL(currNode)
            else:
                if currNode.bottomRight != None:
                    currNode = currNode.bottomRight
                else:
                    return neighborRecL(currNode)
    return neighborRecL(currNode)


def neighborRecR(node):
    if node.topLeft == None:
        return node.objs
    else:
        return neighborRecR(node.bottomLeft) + neighborRecR(node.topLeft)
def neighborRecU(node):
    if node.topLeft == None:
        return node.objs
    else:
        return neighborRecU(node.bottomLeft) + neighborRecU(node.bottomRight)
def neighborRecL(node):
    if node.topLeft == None:
        return node.objs
    else:
        return neighborRecL(node.topRight) + neighborRecL(node.bottomRight)
def neighborRecD(node):
    if node.topLeft == None:
        return node.objs
    else:
        return neighborRecD(node.topRight) + neighborRecD(node.topLeft)
def neighborRecRu(node):
    while node.bottomLeft:
        node = node.bottomLeft
    return node.objs
def neighborRecLu(node):
    while node.bottomRight:
        node = node.bottomRight
    return node.objs
def neighborRecRd(node):
    while node.topLeft:
        node = node.topLeft
    return node.objs
def neighborRecLd(node):
    while node.topRight:
        node = node.topRight
    return node.objs


def findNeighborsLocationCode(currLocationCode, direction, i):
    strCurrLocationCode = str(currLocationCode)
    """if not i:
        i = 0
    if i >= len(strCurrLocationCode) + 1:
        # print("gibts net?")
        return None
    #l == 1, lu == 2, u == 3; ur == 4, r == 5, rd == 6, d == 7, dl == 8
    if direction == 5:
        if strCurrLocationCode[-i] == '1':
            return currLocationCode + 10**(i-1)
        elif strCurrLocationCode[-i] == '2':
            return findNeighborsLocationCode(currLocationCode - 10**(i-1), 5, i+1)
        elif strCurrLocationCode[-i] == '3':
            return currLocationCode + 10**(i-1)
        elif strCurrLocationCode[-i] == '4':
            return findNeighborsLocationCode(currLocationCode - 10**(i-1), 5, i+1)

    elif direction == 1:
        if strCurrLocationCode[-i] == '1':
            return findNeighborsLocationCode(currLocationCode + 10**(i-1), 1, i+1)
        elif strCurrLocationCode[-i] == '2':
            return currLocationCode - 10**(i-1)
        elif strCurrLocationCode[-i] == '3':
            return findNeighborsLocationCode(currLocationCode + 10**(i-1), 1, i+1)
        elif strCurrLocationCode[-i] == '4':
            return currLocationCode - 10**(i-1)

    elif direction == 7:
        if strCurrLocationCode[-i] == '1':
            return currLocationCode + 2*10**(i-1)
        elif strCurrLocationCode[-i] == '2':
            return currLocationCode + 2*10**(i-1)
        elif strCurrLocationCode[-i] == '3':
            return findNeighborsLocationCode(currLocationCode - 2*10**(i-1), 7, i+1)
        elif strCurrLocationCode[-i] == '4':
            return findNeighborsLocationCode(currLocationCode - 2*10**(i-1), 7, i+1)

    #l == 1, lu == 2, u == 3; ur == 4, r == 5, rd == 6, d == 7, dl == 8

    elif direction == 3:
        if strCurrLocationCode[-i] == '1':
            return findNeighborsLocationCode(currLocationCode + 2*10**(i-1), 3, i+1)
        elif strCurrLocationCode[-i] == '2':
            return findNeighborsLocationCode(currLocationCode + 2*10**(i-1), 3, i+1)
        elif strCurrLocationCode[-i] == '3':
            return currLocationCode - 2*10**(i-1)
        elif strCurrLocationCode[-i] == '4':
            return currLocationCode - 2*10**(i-1)

    if direction == 4:
        if strCurrLocationCode[-i] == '1':
            return findNeighborsLocationCode(currLocationCode + 3*10**(i-1), 3, i+1)
        elif strCurrLocationCode[-i] == '2':
            return findNeighborsLocationCode(currLocationCode + 10**(i-1), 4, i+1)
        elif strCurrLocationCode[-i] == '3':
            return currLocationCode - 10**(i-1)
        elif strCurrLocationCode[-i] == '4':
            return findNeighborsLocationCode(currLocationCode - 3*10**(i-1), 5, i+1)
    #l == 1, lu == 2, u == 3; ur == 4, r == 5, rd == 6, d == 7, dl == 8

    elif direction == 6:
        if strCurrLocationCode[-i] == '1':
            return currLocationCode + 3*10**(i-1)
        elif strCurrLocationCode[-i] == '2':
            return findNeighborsLocationCode(currLocationCode + 10**(i-1), 5, i+1)
        elif strCurrLocationCode[-i] == '3':
            return findNeighborsLocationCode(currLocationCode - 10**(i-1), 7, i+1)
        elif strCurrLocationCode[-i] == '4':
            return findNeighborsLocationCode(currLocationCode - 3*10**(i-1), 6, i+1)

    elif direction == 8:
        if strCurrLocationCode[-i] == '1':
            return findNeighborsLocationCode(currLocationCode + 3*10**(i-1), 1, i+1)
        elif strCurrLocationCode[-i] == '2':
            return currLocationCode + 10**(i-1)
        elif strCurrLocationCode[-i] == '3':
            return findNeighborsLocationCode(currLocationCode - 10**(i-1), 8, i+1)
        elif strCurrLocationCode[-i] == '4':
            return findNeighborsLocationCode(currLocationCode - 3*10**(i-1), 7, i+1)

    elif direction == 2:
        if strCurrLocationCode[-i] == '1':
            return findNeighborsLocationCode(currLocationCode + 3*10**(i-1), 2, i+1)
        elif strCurrLocationCode[-i] == '2':
            return findNeighborsLocationCode(currLocationCode + 10**(i-1), 3, i+1)
        elif strCurrLocationCode[-i] == '3':
            return findNeighborsLocationCode(currLocationCode - 10**(i-1), 1, i+1)
        elif strCurrLocationCode[-i] == '4':
            return currLocationCode - 3*10**(i-1)"""
    for character in reversed(strCurrLocationCode):
        if direction < 5:
            if direction == 1:
                if character == '1':
                    currLocationCode = (currLocationCode + 10 ** (i - 1))
                    direction = 1
                elif character == '2':
                    return currLocationCode - 10 ** (i - 1)
                elif character == '3':
                    currLocationCode = currLocationCode + 10 ** (i - 1)
                    direction = 1
                elif character == '4':
                    return currLocationCode - 10 ** (i - 1)
            elif direction == 2:
                if character == '1':
                    currLocationCode = currLocationCode + 3 * 10 ** (i - 1)
                    direction = 2
                elif character == '2':
                    currLocationCode = currLocationCode + 10 ** (i - 1)
                    direction = 3
                elif character == '3':
                    currLocationCode =currLocationCode - 10 ** (i - 1)
                    direction = 2
                elif character == '4':
                    return currLocationCode - 3 * 10 ** (i - 1)
            elif direction == 3:
                if character == '1':
                    currLocationCode = currLocationCode + 2 * 10 ** (i - 1)
                    direction = 3
                elif character == '2':
                    currLocationCode = currLocationCode + 2 * 10 ** (i - 1)
                    direction = 3
                elif character == '3':
                    return currLocationCode - 2 * 10 ** (i - 1)
                elif character == '4':
                    return currLocationCode - 2 * 10 ** (i - 1)
            else:
                if character == '1':
                    currLocationCode = currLocationCode + 3 * 10 ** (i - 1)
                    direction = 3
                elif character == '2':
                    currLocationCode = currLocationCode + 10 ** (i - 1)
                    direction = 4
                elif character == '3':
                    return currLocationCode - 10 ** (i - 1)
                elif character == '4':
                    currLocationCode = currLocationCode - 3 * 10 ** (i - 1)
                    direction = 5
        else:
            if direction == 5:
                if character == '1':
                    return currLocationCode + 10 ** (i - 1)
                elif character == '2':
                    currLocationCode = currLocationCode - 10 ** (i - 1)
                    direction = 5
                elif character == '3':
                    currLocationCode = currLocationCode + 10 ** (i - 1)
                elif character == '4':
                    currLocationCode = currLocationCode - 10 ** (i - 1)
                    direction = 5
            elif direction == 6:
                if character == '1':
                    return currLocationCode + 3 * 10 ** (i - 1)
                elif character == '2':
                    currLocationCode = currLocationCode + 10 ** (i - 1)
                    direction = 5
                elif character == '3':
                    currLocationCode = currLocationCode - 10 ** (i - 1)
                    direction = 7
                elif character == '4':
                    currLocationCode = currLocationCode - 3 * 10 ** (i - 1)
                    direction = 7
            elif direction == 7:
                if character == '1':
                    return currLocationCode + 2 * 10 ** (i - 1)
                elif character == '2':
                    return currLocationCode + 2 * 10 ** (i - 1)
                elif character == '3':
                    currLocationCode = currLocationCode - 2 * 10 ** (i - 1)
                    direction = 7
                elif character == '4':
                    currLocationCode = currLocationCode - 2 * 10 ** (i - 1)
                    direction = 7
            else:
                if strCurrLocationCode[-i] == '1':
                    currLocationCode = currLocationCode + 3 * 10 ** (i - 1)
                    direction = 1
                elif character == '2':
                    return currLocationCode + 10 ** (i - 1)
                elif character == '3':
                    currLocationCode = currLocationCode - 10 ** (i - 1)
                    direction = 8
                elif character == '4':
                    currLocationCode = currLocationCode - 3 * 10 ** (i - 1)
                    direction = 7
        i += 1
    return None


def allNeighbors(locationCode):
    return [findNeighborsLocationCode(locationCode, "r", 1), findNeighborsLocationCode(locationCode, "l", 1), findNeighborsLocationCode(locationCode, "u", 1), findNeighborsLocationCode(locationCode, "d", 1), findNeighborsLocationCode(locationCode, "rd", 1), findNeighborsLocationCode(locationCode, "ru", 1), findNeighborsLocationCode(locationCode, "ld", 1), findNeighborsLocationCode(locationCode, "lu", 1)]

def getHead():
    return globalhead

def main(display, objs):
    quadList.clear()
    headNode = Node(None, Config.SCREENWIDTH, Config.SCREENHEIGHT, [0, 0], None, None)
    global globalhead
    globalhead = headNode
    new_Quad = Quadtree(headNode)
    new_Quad.initQuadtree(objs, headNode, display)
    return quadList