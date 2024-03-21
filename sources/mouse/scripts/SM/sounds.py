import os
import pygame


pygame.init()
pygame.mixer.init()

class SoundManager:
    """ Class permettant de gérer les sons du jeu
    """
    def __init__(self):
        folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/sfx"
        # Dictionnaire contenant les sons du jeu (clé : nom du son, valeur : path)
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
        """ Fonction permettant de jouer un son

        Args:
            sound (str): Nom du son à jouer
        """
        self.sounds[sound].play()