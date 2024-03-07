import pygame


pygame.init()
pygame.mixer.init()

class SoundManager:
    def __init__(self):
        self.sounds = {
            'click': pygame.mixer.Sound('sources/mouse/sfx/click.mp3'),
            'confetti': pygame.mixer.Sound('sources/mouse/sfx/confetti.mp3'),
            'giggle': pygame.mixer.Sound('sources/mouse/sfx/giggle.mp3'),
            'OOB'   : pygame.mixer.Sound('sources/mouse/sfx/OOB.mp3')
        }
    
    def play(self, sound):
        self.sounds[sound].play()