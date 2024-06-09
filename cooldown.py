import pygame

pygame.init()

class Cooldown():
    def __init__(self,time):
        self.ready = False
        self.time = time
        

        
    def update(self, elapsed_seconds):
        self.time -= elapsed_seconds
        if self.time <= 0:
            self.ready = True
        
        
    def reset(self, time):
        self.time = time
        self.ready = False