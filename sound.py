import pygame
import os
import random

pygame.init()

class Soundlibrary:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = self.__create_sound_table(self.__find_audio_files('assets/sounds'))
        self.explosions = self.__create_sound_table(self.__find_audio_files('assets/sounds/explosions'))

    def __find_audio_files(self,root):
        self.filelist = os.listdir(root)
        allfiles = list()

        for entry in self.filelist:
            fullPath = os.path.join(root, entry)
            if os.path.isdir(fullPath):
                allfiles = allfiles + self.__find_audio_files(fullPath)
            else:
                allfiles.append(fullPath)
        return  allfiles

    def __derive_id(self,path):
        small = path.replace('\\', '/')
        simpel = small.replace('.ogg','')
        id = simpel.split('/')
        first = id[len(id)-2]
        second = id[len(id)-1]
        derive_id = ''.join(first + '/' + second)
        return derive_id

    def __create_sound_table(self,paths):
        table = {}
        for path in paths:
            print(path)
            table[self.__derive_id(path)] = pygame.mixer.Sound(path)
        return table

    def play(self,key):
        sound = self.sounds[key]
        if sound is not None:
            sound.play()

    def play_random_explosion(self):
        random_explosion = random.choice(list(self.explosions.values()))
        if random_explosion is not None:
            random_explosion.play()

