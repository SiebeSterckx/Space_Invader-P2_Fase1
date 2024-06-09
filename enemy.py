import pygame
import random

pygame.init()

class mine():
    def __init__(self,x,y):
        self.img = pygame.image.load('tie.png')
        self.speed = 10
        self.x = x
        self.y = y
        self.directions = ["U", "D", "L", "LU", "LD", "R", "RU", "RD"]
        self.directionsR = ["R", "RU", "RD"]
        self.directionsL = ["L", "LU", "LD"]
        self.directionsU = ["U","LU","RU"]
        self.directionsD = ["D", "LD", "RD"]
        self.direction = self.directions[random.randint(0,7)]

    def render(self, surface):
        surface.blit(self.img,(self.x, self.y))
    
    def setPos(self, x, y):
        self.x = x
        self.y = y
        
    def update(self, elapsed_seconds):
        if (self.x >= 950):
            self.direction = self.directionsL[random.randint(0,2)]
        if (self.x <= 0):
            self.direction = self.directionsR[random.randint(0,2)]
        if (self.y >= 670):
            self.direction = self.directionsU[random.randint(0,2)]
        if (self.y <=0):
            self.direction = self.directionsD[random.randint(0,2)]
        if ("D" in self.direction):
            self.y += (elapsed_seconds * self.speed)
        if ("U" in self.direction):
            self.y -= (elapsed_seconds * self.speed)
        if ("R" in self.direction):
            self.x += (elapsed_seconds * self.speed)
        if ("L" in self.direction):
            self.x -= (elapsed_seconds * self.speed)
        return self.x, self.y

    def getPosX(self):
        return self.x

    def getPosY(self):
        return self.y