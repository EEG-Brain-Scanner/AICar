import pygame
import math
import neat
import os

import warnings
warnings.filterwarnings("ignore")


local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, "config-feedforward.txt")
config = neat.config.Config(neat.DefaultGenome,
                            neat.DefaultReproduction,
                            neat.DefaultSpeciesSet,
                            neat.DefaultStagnation,
                            config_path)

p = neat.Population(config)
p.add_reporter(neat.StdOutReporter(True))
p.add_reporter(neat.StatisticsReporter())


DARKGREY = (100,100,100)
LIGHTGREY = (200,200,200)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

(width, height) = (1280, 720)
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption('AI Car')

OUTSIDEPOINTS = [(105 , 361 ), (125 , 232 ), (210 , 143 ), (353 , 85  ), (547 , 56  ),
                 (710 , 45  ), (926 , 77  ), (1052, 189 ), (1007, 311 ), (935 , 424 ),
                 (964 , 514 ), (1025, 600 ), (1018, 661 ), (963 , 698 ), (799 , 674 ),
                 (693 , 570 ), (617 , 463 ), (508 , 439 ), (389 , 499 ), (254 , 523 ),
                 (142 , 463 )]
INSIDEPOINTS = [(284, 331), (312, 256), (381, 195), (464, 152), (592, 119), (739, 115),
                (812, 157), (831, 233), (836, 352), (837, 436), (857, 529), (858, 555),
                (847, 566), (824, 565), (789, 535), (724, 432), (682, 332), (622, 256),
                (576, 248), (522, 260), (464, 291), (410, 349), (365, 400), (316, 413),
                (282, 382)]
GATES = [(337 , 249 ), (264 , 106 ), (362 , 232 ), (353 , 73  ), (407 , 192 ), (420 , 64  ),
         (460 , 165 ), (478 , 55  ), (516 , 147 ), (545 , 47  ), (568 , 134 ), (606 , 41  ),
         (618 , 132 ), (662 , 36  ), (666 , 132 ), (732 , 33  ), (719 , 130 ), (802 , 44  ),
         (763 , 152 ), (899 , 61  ), (808 , 193 ), (1005, 128 ), (819 , 233 ), (1048, 259 ),
         (823 , 274 ), (1012, 337 ), (824 , 328 ), (966 , 402 ), (828 , 396 ), (966 , 458 ),
         (829 , 474 ), (986 , 516 ), (842 , 522 ), (1038, 624 ), (846 , 545 ), (1003, 691 ),
         (835 , 558 ), (873 , 697 ), (826 , 557 ), (792 , 685 ), (818 , 548 ), (734 , 630 ),
         (799 , 531 ), (693 , 588 ), (781 , 506 ), (657 , 544 ), (755 , 464 ), (623 , 494 ),
         (726 , 412 ), (593 , 475 ), (679 , 309 ), (565 , 464 ), (597 , 240 ), (527 , 458 ),
         (515 , 251 ), (487 , 470 ), (446 , 296 ), (448 , 486 ), (403 , 345 ), (400 , 509 ),
         (361 , 391 ), (344 , 525 ), (327 , 400 ), (270 , 530 ), (311 , 395 ), (199 , 504 ),
         (299 , 384 ), (122 , 444 ), (292 , 373 ), (101 , 370 ), (291 , 355 ), (105 , 302 ),
         (294 , 338 ), (115 , 250 ), (299 , 323 ), (136 , 202 ), (307 , 304 ), (176 , 161 ),
         (318 , 277 ), (228 , 127 )]

TRACKLINES = []
for x in range(len(OUTSIDEPOINTS)):
    if x < len(OUTSIDEPOINTS) - 1:
        TRACKLINES.append((OUTSIDEPOINTS[x], OUTSIDEPOINTS[x+1]))
    elif x == len(OUTSIDEPOINTS) - 1:
        TRACKLINES.append((OUTSIDEPOINTS[x], OUTSIDEPOINTS[0]))
for x in range(len(INSIDEPOINTS)):
    if x < len(INSIDEPOINTS) - 1:
        TRACKLINES.append((INSIDEPOINTS[x], INSIDEPOINTS[x+1]))
    elif x == len(INSIDEPOINTS) - 1:
        TRACKLINES.append((INSIDEPOINTS[x], INSIDEPOINTS[0]))

#START KITE.COM LINE SEGMENT INTERSECT CODE
def on_segment(p, q, r):
    if r[0] <= max(p[0], q[0]) and r[0] >= min(p[0], q[0]) and r[1] <= max(p[1], q[1]) and r[1] >= min(p[1], q[1]):
        return True
    return False
def orientation(p, q, r):
    val = ((q[1] - p[1]) * (r[0] - q[0])) - ((q[0] - p[0]) * (r[1] - q[1]))
    if val == 0 : return 0
    return 1 if val > 0 else -1
def intersects(seg1, seg2):
    p1, q1 = seg1
    p2, q2 = seg2
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
    if o1 != o2 and o3 != o4:
        return True
    if o1 == 0 and on_segment(p1, q1, p2) : return True
    if o2 == 0 and on_segment(p1, q1, q2) : return True
    if o3 == 0 and on_segment(p2, q2, p1) : return True
    if o4 == 0 and on_segment(p2, q2, q1) : return True
    return False
#END KITE.COM LINE SEGMENT INTERSECT CODE
    
def intersectpoint(seg1, seg2):
    p1 = seg1[0]
    p2 = seg1[1]
    p3 = seg2[0]
    p4 = seg2[1]

    m12 = (p2[1]-p1[1])/(p2[0]-p1[0]) #slope of line from points 1 & 2
    if m12 > 999999: #rounds if slope is infinate (line upwards)
        m12 = 999999
    elif m12 < -999999:
        m12 = -999999
    m34 = (p4[1]-p3[1])/(p4[0]-p3[0]) #slope of line from points 3 & 4
    if m34 > 999999: #rounds if slope is infinate (line upwards)
        m34 = 999999
    elif m34 < -999999:
        m34 = -999999
        
    b12 = p1[1] - m12 * p1[0] #y intercept of line from points 1 & 2
    b34 = p3[1] - m34 * p3[0] #y intercept of line from points 3 & 4

    x = (b34 - b12) / (m12 - m34)
    y = m12 * x + b12

    return(x,y)

class Car():
    def __init__(self):
        self.width = 25
        self.height = 50
        
        self.theta = math.pi/4
        self.pos = (225,250)

        self.speed = 1

        self.score = 0
        self.adjscore = 0
        self.nextgate = 0

        self.hasdied = False
        
    def turnright(self):
        deg = self.turnspeed * math.pi/180
        onerev = 2*math.pi
        if self.theta - deg < 0:
            self.theta = self.theta - deg + onerev
        else:
            self.theta -= deg

    def turnleft(self):
        deg = self.turnspeed * math.pi/180
        onerev = 2*math.pi
        if self.theta + deg > onerev:
            self.theta = self.theta + deg - onerev
        else:
            self.theta += deg

    def accelerate(self):
        if self.speed < 15:
            self.speed += 0.03

    def decelerate(self):
        slow = 0.3
        
        if self.speed - slow > 0:
            self.speed -= slow
        else:
            self.speed = 0

    def updateturnspeed(self):
        self.turnspeed = (2/3)* self.speed

    def updatepos(self):
        self.pos = (
            self.pos[0] + self.speed * math.cos(self.theta),
            self.pos[1] - self.speed * math.sin(self.theta)
            )

    def updatepoints(self):
        self.terminalpoint = (math.cos(self.theta),
                              math.sin(self.theta)) #find values on unit circle
        self.terminalpoint = (self.height * self.terminalpoint[0],
                              self.height * self.terminalpoint[1]) #stretch radius to height
        self.terminalpoint = (self.terminalpoint[0],
                              -1* self.terminalpoint[1]) #flip y direction because pygame is in Q1 not Q2

        self.parallelpointright = (math.cos(self.theta - math.pi/2),
                              math.sin(self.theta - math.pi/2))
        self.parallelpointright = (self.width/2 * self.parallelpointright[0],
                              self.width/2 * self.parallelpointright[1])
        self.parallelpointright = (self.parallelpointright[0],
                              -1 * self.parallelpointright[1])

        self.parallelpointleft = (math.cos(self.theta + math.pi/2),
                              math.sin(self.theta + math.pi/2))
        self.parallelpointleft = (self.width/2 * self.parallelpointleft[0],
                              self.width/2 * self.parallelpointleft[1])
        self.parallelpointleft = (self.parallelpointleft[0],
                              -1 * self.parallelpointleft[1])

        self.toprightpoint = (self.terminalpoint[0] + self.parallelpointright[0],
                              self.terminalpoint[1] + self.parallelpointright[1])

        self.topleftpoint = (self.terminalpoint[0] + self.parallelpointleft[0],
                              self.terminalpoint[1] + self.parallelpointleft[1])

        self.points = [
            (self.parallelpointright[0] + self.pos[0], self.parallelpointright[1] + self.pos[1]),
            (self.parallelpointleft[0] + self.pos[0], self.parallelpointleft[1] + self.pos[1]),
            (self.topleftpoint[0] + self.pos[0], self.topleftpoint[1] + self.pos[1]),
            (self.toprightpoint[0] + self.pos[0], self.toprightpoint[1] + self.pos[1]),            
            ]

        self.lines = [
            (self.points[0], self.points[1]),
            (self.points[1], self.points[2]),
            (self.points[2], self.points[3]),
            (self.points[3], self.points[0])
            ]

    def makeradarlines(self):
        self.leftlinepoints = (self.pos,
                               (self.pos[0]+ math.cos(self.theta + math.pi/2) *1500,
                                self.pos[1]- math.sin(self.theta + math.pi/2) *1500))

        self.frontleftlinepoints = (self.pos,
                               (self.pos[0]+ math.cos(self.theta + math.pi/4) *1500,
                                self.pos[1]- math.sin(self.theta + math.pi/4) *1500))

        self.frontlinepoints = (self.pos,
                               (self.pos[0]+ math.cos(self.theta) *1500,
                                self.pos[1]- math.sin(self.theta) *1500))

        self.frontrightlinepoints = (self.pos,
                               (self.pos[0]+ math.cos(self.theta - math.pi/4) *1500,
                                self.pos[1]- math.sin(self.theta - math.pi/4) *1500))

        self.rightlinepoints = (self.pos,
                               (self.pos[0]+ math.cos(self.theta - math.pi/2) *1500,
                                self.pos[1]- math.sin(self.theta - math.pi/2) *1500))

    def updateradarlines(self):
#LL
        TrackIntersects = []
        for x in TRACKLINES:
            if intersects(x, self.leftlinepoints) == True:
                TrackIntersects.append(x)

        bestdistance = False

        for a in TrackIntersects:
            (intx, inty) = intersectpoint( ((self.leftlinepoints[0][0], -1* self.leftlinepoints[0][1]),
                                           (self.leftlinepoints[1][0], -1* self.leftlinepoints[1][1])),
                                          ((a[0][0], -1* a[0][1]),
                                           (a[1][0], -1* a[1][1])) )
            (intx, inty) = (intx, -1* inty)

            distance = math.sqrt( (intx-self.pos[0])**2 + (inty-self.pos[1])**2 )
            if bestdistance == False:
                bestdistance = (distance, (intx, inty))
            elif distance < bestdistance[0]:
                bestdistance = (distance, (intx, inty))

        self.LLpoint = bestdistance[1]
        self.LLdistance = bestdistance[0]
#FLL
        TrackIntersects = []
        for x in TRACKLINES:
            if intersects(x, self.frontleftlinepoints) == True:
                TrackIntersects.append(x)

        bestdistance = False

        for a in TrackIntersects:
            (intx, inty) = intersectpoint( ((self.frontleftlinepoints[0][0], -1* self.frontleftlinepoints[0][1]),
                                           (self.frontleftlinepoints[1][0], -1* self.frontleftlinepoints[1][1])),
                                          ((a[0][0], -1* a[0][1]),
                                           (a[1][0], -1* a[1][1])) )
            (intx, inty) = (intx, -1* inty)

            distance = math.sqrt( (intx-self.pos[0])**2 + (inty-self.pos[1])**2 )
            if bestdistance == False:
                bestdistance = (distance, (intx, inty))
            elif distance < bestdistance[0]:
                bestdistance = (distance, (intx, inty))

        self.FLLpoint = bestdistance[1]
        self.FLLdistance = bestdistance[0]
#FL
        TrackIntersects = []
        for x in TRACKLINES:
            if intersects(x, self.frontlinepoints) == True:
                TrackIntersects.append(x)

        bestdistance = False

        for a in TrackIntersects:
            (intx, inty) = intersectpoint( ((self.frontlinepoints[0][0], -1* self.frontlinepoints[0][1]),
                                           (self.frontlinepoints[1][0], -1* self.frontlinepoints[1][1])),
                                          ((a[0][0], -1* a[0][1]),
                                           (a[1][0], -1* a[1][1])) )
            (intx, inty) = (intx, -1* inty)

            distance = math.sqrt( (intx-self.pos[0])**2 + (inty-self.pos[1])**2 )
            if bestdistance == False:
                bestdistance = (distance, (intx, inty))
            elif distance < bestdistance[0]:
                bestdistance = (distance, (intx, inty))

        self.FLpoint = bestdistance[1]
        self.FLdistance = bestdistance[0]
#FRL
        TrackIntersects = []
        for x in TRACKLINES:
            if intersects(x, self.frontrightlinepoints) == True:
                TrackIntersects.append(x)

        bestdistance = False

        for a in TrackIntersects:
            (intx, inty) = intersectpoint( ((self.frontrightlinepoints[0][0], -1* self.frontrightlinepoints[0][1]),
                                           (self.frontrightlinepoints[1][0], -1* self.frontrightlinepoints[1][1])),
                                          ((a[0][0], -1* a[0][1]),
                                           (a[1][0], -1* a[1][1])) )
            (intx, inty) = (intx, -1* inty)

            distance = math.sqrt( (intx-self.pos[0])**2 + (inty-self.pos[1])**2 )
            if bestdistance == False:
                bestdistance = (distance, (intx, inty))
            elif distance < bestdistance[0]:
                bestdistance = (distance, (intx, inty))

        self.FRLpoint = bestdistance[1]
        self.FRLdistance = bestdistance[0]
#RL
        TrackIntersects = []
        for x in TRACKLINES:
            if intersects(x, self.rightlinepoints) == True:
                TrackIntersects.append(x)

        bestdistance = False

        for a in TrackIntersects:
            (intx, inty) = intersectpoint( ((self.rightlinepoints[0][0], -1* self.rightlinepoints[0][1]),
                                           (self.rightlinepoints[1][0], -1* self.rightlinepoints[1][1])),
                                          ((a[0][0], -1* a[0][1]),
                                           (a[1][0], -1* a[1][1])) )
            (intx, inty) = (intx, -1* inty)

            distance = math.sqrt( (intx-self.pos[0])**2 + (inty-self.pos[1])**2 )
            if bestdistance == False:
                bestdistance = (distance, (intx, inty))
            elif distance < bestdistance[0]:
                bestdistance = (distance, (intx, inty))

        self.RLpoint = bestdistance[1]
        self.RLdistance = bestdistance[0]

    def checkgate(self):
        crossed = False
        for x in self.lines:
            if intersects(x, (GATES[self.nextgate], GATES[self.nextgate+1])) == True:
                crossed = True

        if crossed == True:
            if self.nextgate + 2 <= 78:
                self.nextgate += 2
            else:
                self.nextgate = 0

            self.score += 0.025

        self.adjscore -= 0.001

    def checkdead(self):
        dead = False
            
        for x in self.lines:
            for y in TRACKLINES:
                if intersects(x, y) == True:
                        dead = True

        if dead == True:
            self.hasdied = True
        else:
            self.hasdied = False

    def checkspeeddead(self):
        if self.speed < 1:
            self.hasdied = True

    def checkgooddead(self):
        if self.score >= 5:
            self.hasdied = True



def run_car(genomes, config):

    nets = []
    cars = []

    for id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

        cars.append(Car())

    for car in cars:
        if car.hasdied == False:
            car.updateturnspeed()
            car.updatepos()
            car.updatepoints()
            car.checkgate()
            car.makeradarlines()
            car.updateradarlines()
            car.checkdead()
            car.checkspeeddead()
            car.checkgooddead()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        for index, car in enumerate(cars):
            if car.hasdied == False:

                genomes[index][1].fitness = car.score + car.adjscore

                output = nets[index].activate([
                    car.LLdistance,
                    car.FLLdistance,
                    car.FLdistance,
                    car.FRLdistance,
                    car.RLdistance,
                    car.speed])

                if output[0] >= 10:
                    car.turnleft()
                elif output[0] <= -10:
                    car.turnright()
                if output[1] > 0:
                    car.accelerate()
                else:
                    car.decelerate()

        alive = 0
        for car in cars:
            if car.hasdied == False:
                alive += 1
        if alive == 0:
            break


        screen.fill(DARKGREY)

        pygame.draw.polygon(screen, LIGHTGREY, OUTSIDEPOINTS)
        pygame.draw.polygon(screen, DARKGREY, INSIDEPOINTS)

        for car in cars:
            if car.hasdied == False:
                car.updateturnspeed()
                car.updatepos()
                car.updatepoints()
                car.checkgate()
                car.makeradarlines()
                car.updateradarlines()
                car.checkdead()
                car.checkspeeddead()
                car.checkgooddead()

                pygame.draw.polygon(screen, RED, car.points)

                pygame.draw.line(screen, (255,153,153), car.leftlinepoints[0], car.LLpoint, 5)
                pygame.draw.line(screen, (255,204,153), car.frontleftlinepoints[0], car.FLLpoint, 5)
                pygame.draw.line(screen, (255,255,153), car.frontlinepoints[0], car.FLpoint, 5)
                pygame.draw.line(screen, (204,255,153), car.frontrightlinepoints[0], car.FRLpoint, 5)
                pygame.draw.line(screen, (153,255,153), car.rightlinepoints[0], car.RLpoint, 5)

                pygame.draw.circle(screen, GREEN, car.LLpoint, 5)
                pygame.draw.circle(screen, GREEN, car.FLLpoint, 5)
                pygame.draw.circle(screen, GREEN, car.FLpoint, 5)
                pygame.draw.circle(screen, GREEN, car.FRLpoint, 5)
                pygame.draw.circle(screen, GREEN, car.RLpoint, 5)

        pygame.display.flip()
        clock.tick(60)


winner = p.run(run_car, 1000000)