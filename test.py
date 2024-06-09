import pygame
import math

def main():
    pygame.init()
    state = State()
    frames = [pygame.image.load(f'explosion/{i}.png') for i in range(1, 9)]
    clock = pygame.time.Clock()
    animation = FrameBasedAnimation(frames, 0.1)

    surface=create_main_surface()
    pygame.mixer.music.load("musica.ogg")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    while True:
        clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
             raise SystemExit
            if event.type == pygame.KEYDOWN:
                print("You pressed a button congrats!")
        elapsed_seconds = pygame.time.Clock.get_time()
        animation.update(elapsed_seconds)
        state.render_frame(surface)
        state.update()
        pygame.display.flip()

def create_main_surface():
    screen_size = (1024, 768)
    return pygame.display.set_mode(screen_size)       

class FrameBasedAnimation:
    def __init__(self, animations, duration):
        self.__animations = animations
        self.__duration = duration
        self.__single_duration = duration/len(animations)
        self.__elapsed_seconds = 0
    
    def render(self, surface):
        if self.__elapsed_seconds > self.__duration:
            return
        surface.blit(self.__animations[math.floor(self.__elapsed_seconds)*10,(500,500)])

    def update(self, elapsed_seconds):
        self.__elapsed_seconds += elapsed_seconds
        
class State:
    x = 0
    def __init__(self):
        self.x = 0

    def update(self):
        self.x = self.x+1

    def clear_surface(self, surface):
        surface.fill((0,0,0))

    def render_frame(self, surface):
        self.clear_surface(surface)
        colour = (0,0,255) #blue
        circle_center = (self.x, 350)
        circle_radius = 300
        pygame.draw.circle(surface,colour, circle_center, circle_radius)

    

    

main()