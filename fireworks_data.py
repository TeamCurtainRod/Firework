import random
import math
import pygame
import pygame.mixer

MAX_X_SPEED =  20.  # pixels per second
MAX_Y_SPEED = 200.  # pixels per second
MAX_EXPLODE_SPEED = 100.  # pixels per second
MAX_FUSE    =  20.  # seconds
MIN_FUSE    =   5.  # seconds
EMBER_FUSE_LENGTH = 2.5 # seconds
GRAVITY     =  35.  # pixels per second per second

STATE_LAUNCH  = 1
STATE_EXPLODE = 2
STATE_GROUND  = 3
STATE_BURN    = 4

TAIL_SIZE     = 10
EXPLODE_COUNT = 20

    
class Firework:

    def __init__(self, width, height):
        self.x = width/10.    
        self.y = height
        self.dx =   width/30. 
        self.dy = - height/3.5 
        self.fuse  = (-self.dy)/GRAVITY
        self.state = STATE_LAUNCH
        self.tail  = [ (int(self.x), int(self.y)) for i in range(TAIL_SIZE) ]
        pygame.mixer.init()
        self.explosion_sound = pygame.mixer.Sound("RPG.wav")
        self.explosion_sound.play()
        
        return

    def evolve(self, dt, width, height):
        self.x    += self.dx * dt
        self.y    += self.dy * dt
        self.dy   += GRAVITY * dt
        self.fuse -= dt
        
        self.tail.append( (int(self.x), int(self.y)) )
        self.tail.pop(0)
        
        if self.fuse <= 0 and self.state == STATE_LAUNCH:
            self.fuse = EMBER_FUSE_LENGTH
            self.state = STATE_EXPLODE
            
        if self.fuse <= 0 and self.state == STATE_BURN:
            self.state = STATE_GROUND
            
        if self.y > height:
            self.state = STATE_GROUND
            
        return

    def explode(self, width, height):
        embers = []
        for j in range(EXPLODE_COUNT):
            direction = j*2.0*math.pi/EXPLODE_COUNT
            dy = math.sin(direction) * MAX_EXPLODE_SPEED
            dx = math.cos(direction) * MAX_EXPLODE_SPEED
            e = Firework(width, height)
            e.x = self.x
            e.y = self.y
            e.dx = self.dx + dx
            e.dy = self.dy + dy
            e.fuse = self.fuse
            e.state = STATE_BURN
            e.tail  = [ (int(e.x), int(e.y)) for i in range(TAIL_SIZE) ]
            embers.append(e)
        return embers
            

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

    def getTail(self):
        return self.tail
    
    def getState(self):
        return self.state
    

class FireworksData:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.emptySky()
        self.addOne()
        return

    def addOne(self):
        f = Firework(self.width, self.height)
        self.fireworks.append(f)
        return

    def emptySky(self):
        self.fireworks = []
        return
            
    def getWidth(self):
        return self.width
        
    def getHeight(self):
        return self.height

    def evolve(self, dt):
        for f in self.fireworks:
            f.evolve(dt, self.width, self.height)
            if f.getState() == STATE_GROUND:
                self.fireworks.remove(f)
            elif f.getState() == STATE_EXPLODE:
                self.fireworks.remove(f)
                embers = f.explode(self.width, self.height)
                self.fireworks.extend(embers)

        if len(self.fireworks) == 0:
            self.addOne()
            
        return

    def getFireworks(self):
        return self.fireworks
    

