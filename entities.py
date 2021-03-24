import pygame
import random

class entity(object):
    def __init__(self,x,y,width,height,vel,color, resolution, floor=0):
        self.x = x
        self.y = y
        self.floor = floor
        self.width = width
        self.height = height
        self.vel = vel
        self.color = color
        self.isDucking = False
        self.isJumping = False
        self.fallingVelocity = 0
        self.resolution = resolution

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win):
        height = self.height
        y = self.y
        if self.isDucking:
            height = self.height / 2
            y = self.y + height
        pygame.draw.rect(win, self.color, (self.x, y, self.width, height))

class playerEntity(entity):
    def speed(self):
        return self.vel - 1 if self.isDucking else self.vel
    
    def moveLeft(self):
        self.x = max(0, self.x - self.speed())

    def moveRight(self):
        self.x = min(self.resolution[0] - self.width, self.x + self.speed())
    
    def duck(self):
        self.isDucking = True

    def jump(self):
        if not(self.isJumping):
            self.isJumping = True
            self.fallingVelocity = -8
            if (self.isDucking):
                self.fallingVelocity = -10
        self.isDucking = False

    def fall(self):
        if (self.isJumping):
            self.fallingVelocity += 0.6
            self.y += self.fallingVelocity
            if (self.y >= self.floor):
                self.y = min(self.y, self.floor)
                self.isJumping = False
                self.fallingVelocity = 0

class enemyEntity(entity):

    def wander(self):
        random.seed()
        self.vel = random.randrange(-2,2)
        self.x += self.vel
        self.x = max(0, self.x - self.vel)
        self.x = min(self.resolution[0] - self.width, self.x + self.vel)
