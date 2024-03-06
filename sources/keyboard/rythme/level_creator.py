import datetime
import os
import msvcrt
import threading
from pygame import mixer

from pynput import keyboard # pip install pynput

class KeyCounter:
    def __init__(self, register_key):
        self.current_key = None
        self.register_key = register_key

    def key_pressed(self, key):
        """Appelée lorsque l'utilisateur appuie sur une touche	
        
        Args:
            key (str): La touche appuyée
        """
        if self.current_key != key:
            self.current_key = key
            
            # Enregistre le temps actuel pour compter combien de temps la touche est restée appuyée
            self.timer = datetime.datetime.now()

    def key_released(self, key):
        """Appelée lorsque l'utilisateur relâche une touche

        Args:
            key (str): La touche relâchée
        """
        # Enregistre le temps actuel pour calculer combien de temps la touche est restée appuyée
        temps_actuel = datetime.datetime.now()
        time = (temps_actuel - self.timer).total_seconds()

        # Si la touche est restée appuyée plus de 0.7 secondes 
        if time > 0.7:
            self.register_key(key, time)
        else:
            self.register_key(key, 0)

    def lancer_compteur(self):
        """Lance le compteur de touches appuyées
        """
        with keyboard.Listener(on_press=self.key_pressed, on_release=self.key_released) as listener:
            listener.join()

class LevelCreator:
    def __init__(self) -> None:
        pass

    def create_level(self, nom, difficulte, son):
        """Crée un niveau avec les paramètres donnés

        Args:
            nom (str): Le nom du niveau
            difficulte (int): La difficulté du niveau (sur 5)
            son (str): Le son du niveau (dans le dossier "audios")
        """
        print("Création du niveau : ", nom, difficulte, son)
        print("Appuyez sur une touche pour jouer l'audio et commencer la création du niveau")

        # Joue l'audio
        mixer.init()
        mixer.music.load(son)
        mixer.music.play()

    def register_key(self, key, time):
        """Enregistre une touche appuyée par l'utilisateur

        Args:
            key (str): La touche appuyée
            time (float): Le temps pendant lequel la touche a été appuyée. 0 si la touche compte une seule fois
        """
        print("Touche appuyée : ", key, time) 

        # Ici il faut sauvegarder la touche, si elle est restée appuyée ou non, et combien de temps
        # et aussi le moment où elle a été appuyée dans le son
        # à la fin sauvegarde le niveau dans un fichier JSON avec le nom, la difficulté, le son, et les touches appuyées

AUDIO_PATH = os.path.dirname(__file__) + "/audios/"

level_creator = LevelCreator()
level_creator.create_level("Mettre un nom", 1, AUDIO_PATH + "son1.mp3")

# Lance le compteur de touches appuyées (sur un thread séparé pour pas bloquer le programme)
counter = KeyCounter(level_creator.register_key)
thread = threading.Thread(target=counter.lancer_compteur)
thread.start()

# Permet de ne pas fermer le programme
msvcrt.getch()

# Pour les audios libre de droit, voir : https://pixabay.com/fr/music/