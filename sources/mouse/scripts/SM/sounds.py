import os
import pygame


pygame.init()
pygame.mixer.init()

class SoundManager:
    def __init__(self):
        folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/sfx"
        self.sounds = {
            'click': pygame.mixer.Sound(folder + '/click.mp3'),
            'confetti': pygame.mixer.Sound(folder + '/confetti.mp3'),
            'giggle': pygame.mixer.Sound(folder + '/giggle.mp3'),
            'OOB'   : pygame.mixer.Sound(folder + '/OOB.mp3'),
            'tp'    : pygame.mixer.Sound(folder + '/tp.mp3'),
            'switch': pygame.mixer.Sound(folder + '/switch.mp3'),
            'spike' : pygame.mixer.Sound(folder + '/spike.mp3'),
            'egg'   : pygame.mixer.Sound(folder + '/egg.mp3')
        }
    def play(self, sound):
        self.sounds[sound].play()