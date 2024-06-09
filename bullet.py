import pygame
pygame.init()

class Bullet:
    
    def __init__(self,x,y):
        self.img = pygame.image.load('starshipbullet.png')
        self.__speed = 20
        self.__time_left = 175
        self.x = x
        self.y = y
        self.disposed = False
         
    def render(self, surface):
        surface.blit(self.img,(self.x, self.y))

    def update(self, elapsed_seconds):
        self.y -= self.__speed * elapsed_seconds
        self.__time_left -= 1
        if self.__time_left <= 0:
            self.disposed = True
        return self.y

    def getPosX(self):
        return self.x

    def getPosY(self):
        return self.y
    


    