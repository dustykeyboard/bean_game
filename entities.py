import pygame
import random

class entity(object):
    def __init__(self, rect, color):
        self.type = 'unknown'
        self.vel = 5
        self.color = color
        self.isDucking = False
        self.isFalling = False
        self.fallingVelocity = 0

        self.rect = pygame.Rect(rect)
        self.isMobile = True

    def fall(self, area):
        if self.isMobile:
            self.fallingVelocity += 0.6
            self.rect.move_ip(0, self.fallingVelocity)
            if not(area.contains(self.rect)):
                self.rect.clamp_ip(area)
                self.isFalling = False
                self.fallingVelocity = 0

    def checkForCollisions(self, rects):
        for rect in rects:
            if self.rect != rect: 
                if self.rect.colliderect(rect):
                    return True
        return False

    def tick(self, area):
        self.fall(area)
        self.rect.clamp_ip(area)


    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

class playerEntity(entity):
    def __init__(self, rect, color):
        entity.__init__(self, rect, color)
        self.health = 5

    def speed(self):
        return self.vel - 1 if self.isDucking else self.vel
    
    def moveLeft(self):
        self.rect.move_ip(-self.speed(), 0)

    def moveRight(self):
        self.rect.move_ip(self.speed(), 0)
    
    def duck(self):
        self.isDucking = True

    def jump(self):
        if not(self.isFalling):
            self.isFalling = True
            self.fallingVelocity = -8
            if (self.isDucking):
                self.fallingVelocity = -10
        self.isDucking = False

    def checkForCollisions(self, rects):
        return self.rect.collidelistall(rects)
    
    def damaged(self):
        self.health -= 1

    def alive(self):
        return self.health > 0


class enemyEntity(entity):
    def __init__(self, rect):
        color = (0, random.randint(100,255), 0)
        entity.__init__(self, rect, color)
        self.type = 'enemy'
        self.vel = 2
        self.direction = random.randint(0,1) * 2 -1
    
    def wander(self):
        self.rect.move_ip(self.direction, 0)

    def tick(self, area, rects):
        self.wander()
        if not(area.contains(self.rect)):
            self.direction *= -1
        if self.checkForCollisions(rects):
            self.direction *= -1
        entity.tick(self, area)


class terrainEntity(entity):
    def __init__(self, rect, color):
        entity.__init__(self, rect, color)
        self.type = 'terrain'
        self.isMobile = False
