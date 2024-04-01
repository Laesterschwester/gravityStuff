import cProfile
import pstats
from random import random, randint
import time
from multiprocessing import Pool
import pygame
import Config
import collisions
import physObj
import Quadtree
import physics
import math

size = (Config.SCREENWIDTH, Config.SCREENHEIGHT)
display = pygame.display.set_mode(size)

def main():
    pygame.init()
    startTime = time.time()

    clock = pygame.time.Clock()
    display.fill((255, 255, 255, 0))


    clock = pygame.time.Clock()
    timeDifference = 0
    deltaTime = 0
    speed = 0

    objects = []
    physArr = []
    for i in range(Config.NUMBEROFOBJS):
        x = randint(15, Config.SCREENWIDTH - 20)
        y = randint(15, Config.SCREENHEIGHT - 20)
        a = randint(-5, 5)
        b = randint(-5, 5)
        #a = 5
        #b = 5
        newObject = physObj.Obj([x, y], 10, Config.RADIUS, [a, b])
        objects.append(newObject)
        physArr.append(newObject)

    starThingy = physObj.Obj([Config.SCREENWIDTH / 2, Config.SCREENHEIGHT / 2], 10, 10, [0, 0], (255, 50, 50), True)
    objects.append(starThingy)

    play = True

    while play:
        display.fill((200, 200, 200))

        #Hintergrund mit Alpha
        """s = pygame.Surface((1000, 750))  # the size of your rect
        s.set_alpha(20)  # alpha level
        s.fill((255, 255, 255))  # this fills the entire surface
        display.blit(s, (0, 0))"""

        #pygame.draw.rect(display, (2,2,2), pygame.Rect(30, 30, 60, 60), 2)
        """for i in range(len(objects)):
            for j in range(len(objects)):
                collisions.gravityAroundImmovable(objects[i], objects[j], deltaTime)
                #collisions.repulsionAroundImmovable(starThingy, object, deltaTime)"""

        for i in range(len(physArr)-1, -1, -1):
            physics.gravityAroundImmovable(starThingy, physArr[i], deltaTime)

            a = starThingy.position[0] - physArr[i].position[0]
            b = starThingy.position[1] - physArr[i].position[1]
            sqrDst = math.sqrt(a * a + b * b)
            #print(objects[i])
            #print(i)
            #
            """if sqrDst <= starThingy.radius + physArr[i].radius and starThingy != physArr[i]:
                starThingy.radius += 0.005
                starThingy.mass += physArr[i].mass*0.001
                objects.remove(objects[i])
                physArr.remove(physArr[i])"""
        #physics.springForce(starThingy, physArr[0],deltaTime, 100, 10)
        #physics.springForce(physArr[0], starThingy, deltaTime, 100, 10)

        #physics.gravityAll(objects, deltaTime)                         #hier für Schwerkraft zwischen mehreren Objekten

        for object in physArr:
            object.updatePos(speed)

            collisions.checkfAndResoveBorderCollision(object, deltaTime)
            if collisions.checkBorderCol(object):
                physArr.remove(object)
                objects.remove(object)
                continue

        physObj.drawArr(objects)

        collisions.col(display, physArr)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        #pygame.event.get()

        ticks = pygame.time.get_ticks()
        deltaTime = ticks - timeDifference
        speed = deltaTime/20 #200 ist gut
        #print(1000/deltaTime, " fps")
        #print(ticks)
        #print("-----------------------------------------------------------------------------------------------------------")
        timeDifference = ticks
        clock.tick(200)
        pygame.display.update()

        if Config.BENCHMARK:
            if time.time()-startTime>10:
                play = False

def xSquared(x):
    return x * x
def multiP():
    array = [i for i in range(1000)]
    with Pool(processes=2) as pool:
        return pool.map(xSquared, array)

if __name__ == '__main__':
    if Config.BENCHMARK:
        profiler = cProfile.Profile()
        profiler.enable()

        main()

        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats('cumtime')
        stats.print_stats()
        stats.dump_stats('profiler_results.prof')
    else:
        #print(multiP())
        #time.sleep(3)
        main()
#Fg = G*m1*m2/r^2