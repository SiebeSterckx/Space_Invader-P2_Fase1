import pygame
import time

import enemy
import sound
import looping
import bullet
import random
import cooldown

looper = looping.LoopingVariable(-1000)
font = pygame.font.Font("Freedom-10eM.ttf", 36)
font2 = pygame.font.Font("Nasa21-l23X.ttf", 32)
explosions = [pygame.image.load("explosion/1.png"), pygame.image.load("explosion/2.png"),pygame.image.load("explosion/3.png"), pygame.image.load("explosion/4.png"), pygame.image.load("explosion/5.png"), pygame.image.load("explosion/6.png"), pygame.image.load("explosion/7.png"), pygame.image.load("explosion/8.png"), pygame.image.load("explosion/9.png"),]

def main():

    pygame.init()
    
    surface=create_main_surface()
    state = State(surface)

    pygame.mixer.music.load("star_wars_theme.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()

    game = True
    while game:
        time.sleep(1/60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
             raise SystemExit

        state.process_collisions()        
        process_key_input(state)
        state.update(clock.get_time()/100)
        state.render(surface)
        pygame.display.flip()
        pygame.display.set_caption('Pew Pew da Pinkies')
        clock.tick()
        if state.getSpaceship().isDead():
            game = False
    ending = pygame.image.load('ending.png')
    pygame.mixer.music.unload()
    pygame.mixer.music.load("ending.mp3")
    pygame.mixer.music.set_volume(3)
    pygame.mixer.music.play(-1)
    end = True
    while end:
        surface.fill((255,255,255))
        surface.blit(ending, (250, 50))
        text = font.render('GAME OVER', False, (0,0,0))
        text2 = font2.render('your score was:  '+str(state.points), False, (0,0,0))
        surface.blit(text, (400, 550))
        surface.blit(text2, (400, 600))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
             raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_ENTER:
                    end = False
                if event.key == pygame.K_RETURN:
                    end = False
    main()

def create_main_surface():
    screen_size = (1024, 768)
    return pygame.display.set_mode(screen_size)

def process_key_input(state):
    pressed = pygame.key.get_pressed()
    spaceship = state.getSpaceship()
    bullets = state.getBullets()
    x = spaceship.getPos()[0]
    y = spaceship.getPos()[1]
    if pressed[pygame.K_DOWN]:
        if pressed[pygame.K_LEFT]:
            spaceship.setPos(x-6, y+6)
        elif pressed[pygame.K_RIGHT]:
            spaceship.setPos(x+6, y+6)
        else:
            spaceship.setPos(x, y+6)
    if pressed[pygame.K_UP]:
        if pressed[pygame.K_LEFT]:
            spaceship.setPos(x-6, y-6)
        elif pressed[pygame.K_RIGHT]:
            spaceship.setPos(x+6, y-6)
        else:
            spaceship.setPos(x, y-6)
    if pressed[pygame.K_LEFT]:
        if pressed[pygame.K_UP]:
            spaceship.setPos(x-6, y-6)
        elif pressed[pygame.K_DOWN]:
            spaceship.setPos(x-6, y+6)
        else:
            spaceship.setPos(x-6, y)
    if pressed[pygame.K_RIGHT]:
        if pressed[pygame.K_UP]:
            spaceship.setPos(x+6, y-6)
        elif pressed[pygame.K_DOWN]:
            spaceship.setPos(x+6, y+6)
        else:
            spaceship.setPos(x+6, y)
    if pressed[pygame.K_SPACE]:
        if state.cooldown.ready:
            bullets.append(bullet.Bullet((spaceship.getXpos()+18.5),(spaceship.getYpos()-10)))
            soundlib.play('shots/pew')
            state.cooldown.reset(4)

       
class State:
    def __init__(self, surface):
        self.__spaceship = Spaceship()
        self.__background=Background()
        self.__surface = surface
        self.__bullets = []
        self.__mine = enemy.mine(random.randint(0,950),random.randint(0,200))
        self.cooldown = cooldown.Cooldown(4)
        self.pointImg = pygame.image.load('punt.png')
        self.points = 0

    def process_collisions(self):
        x1 = self.__spaceship.getXpos()
        x2 = self.__spaceship.getXpos()+70
        y1 = self.__spaceship.getYpos()
        y2 = self.__spaceship.getYpos()-98
        enemyX = self.__mine.getPosX()
        enemyY = self.__mine.getPosY()
        if x1 <= enemyX <= x2:
            if y2 <= enemyY <= y1:
                self.playExplosion(enemyX, enemyY)
                self.points += 1
                self.__spaceship.removeLive()
                self.__mine.setPos(random.randint(0,950),random.randint(0,200))
                soundlib.play_random_explosion()
        for b in self.__bullets:
            x1 = self.__mine.getPosX()-10
            x2 = self.__mine.getPosX()+45
            y1 = self.__mine.getPosY()+10
            y2 = self.__mine.getPosY()-45
            bulletX = b.getPosX()
            bulletY = b.getPosY()
            if x1 <= bulletX <= x2:
                if y2 <= bulletY <= y1:
                    self.playExplosion(x1, y1)
                    self.points += 1
                    self.__mine.setPos(random.randint(0,950),random.randint(0,200))
                    soundlib.play_random_explosion()
                                   
    def clear_surface(self, surface):
        surface.fill((0,52,83))

    def playExplosion(self, x, y):
        for e in explosions:
            self.__surface.blit(e, (x, y))
            pygame.display.flip()
            time.sleep(0.01)

    def getSpaceship(self):
        return self.__spaceship

    def render(self, surface):
        self.clear_surface(surface)
        self.__background.render(surface)
        self.__spaceship.updateLives(surface)
        self.renderPoints(surface, self.points)
        self.__spaceship.render(surface)
        looper.increase(7)
        for bullet in self.__bullets:
            bullet.render(surface)
        self.__mine.render(surface)
        
    def renderPoints(self, surface, points):
        surface.blit(self.pointImg, (0,0))
        text = font2.render("x"+str(points), False, (0,0,0))
        surface.blit(text, (40, 0))

    
    def update(self, elapsed_seconds):
        for bullet in self.__bullets:
            if bullet.disposed:
                self.__bullets.remove(bullet)

            bullet.update(elapsed_seconds)
        self.__mine.update(elapsed_seconds)
        self.cooldown.update(elapsed_seconds)
    
    def getSpaceship(self):
        return self.__spaceship

    def getBullets(self):
        return self.__bullets

    def getBullet(self):
        return self.__bullet
    


class Background:
    def __init__(self):
        one = self.__create_image()
        two = self.__flip_image(one)
        self.__img=self.__join_images(two, one)
        self.__y=0

    def __create_image(self):
        backImg = pygame.image.load('background.png')
        return backImg

    def __flip_image(self, surface):
        surface = pygame.transform.flip(surface, False, True)
        return surface
    
    def __join_images(self, surface, surface2):
        screen_size = (1028, 4206)
        screen = pygame.Surface(screen_size)
        screen.blit(surface, (0, 0))
        screen.blit(surface2, (0, 2103))
        return screen

    def render(self, surface):
        self.__y = looper.value()
        surface.blit(self.__img, (0,self.__y))
        surface.blit(self.__img, (0,self.__y - self.__img.get_height()))



class Spaceship:
    def __init__(self):
        self.__Img = pygame.image.load('milleniumFalcon.png')
        self.__liveImg = pygame.image.load('obi.png')
        self.__x = 450
        self.__y = 500
        self.lives = 3

    def isDead(self):
        if self.lives == 0:
            return True
        return False

    def render (self, surface):
        surface.blit(self.__Img, (self.__x, self.__y))

    def getPos(self):
        return (self.__x, self.__y)

    def getXpos(self):
        return self.__x
    
    def getYpos(self):
        return self.__y

    def removeLive(self):
        self.lives -= 1

    def setPos(self, x, y):
        if 0 < x < 950:
            self.__x = x
        if 0 < y < 670:
            self.__y = y
    def updateLives(self, surface):
        surface.blit(self.__liveImg, (0,700))
        if self.lives >= 2:
            surface.blit(self.__liveImg, ((self.__liveImg.get_width()),700))
        if self.lives == 3:
            surface.blit(self.__liveImg, ((self.__liveImg.get_width()*2), 700))

soundlib=sound.Soundlibrary()
main()