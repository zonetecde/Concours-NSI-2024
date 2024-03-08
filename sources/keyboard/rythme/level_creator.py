import datetime
import json
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
        self.current_key = None

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
    def __init__(self, nom, difficulte, son, completion) -> None:
        """ Initialise un créateur de niveau

        Args:
            nom (str): Le nom du niveau
            difficulte (int): La difficulté du niveau (sur 5)
            son (str): Le son du niveau (dans le dossier "audios")
            completion (bool): Si c'est un ajout au niveau ou une création
        """
        self.nom = nom
        self.difficulte = difficulte
        self.son = son

        self.timer = None
        self.touches = []

        if completion:
            self.load()

    def load(self):
        """Charge un niveau depuis un fichier
        """
        save_file = LEVEL_PATH + "niveau_" + self.nom + ".json"
        if os.path.exists(save_file):
            with open(save_file, "r", encoding="utf-8") as file:
                level_obj = json.load(file)
                self.touches = level_obj["Touches"]
                self.nom = level_obj["Nom"]
                self.son = level_obj["Audio"]
                self.difficulte = level_obj["Difficulte"]

    def create_level(self):
        """Crée un niveau avec les paramètres donnés
        """
        print("Création du niveau : ", self.nom, self.difficulte, self.son)

        # Joue l'audio
        mixer.init()
        mixer.music.load(AUDIO_PATH + self.son)
        mixer.music.play()

        self.start_time = datetime.datetime.now()

    def register_key(self, key, time):
        """Enregistre une touche appuyée par l'utilisateur

        Args:
            key (str): La touche appuyée
            time (float): Le temps pendant lequel la touche a été appuyée. 0 si la touche compte une seule fois
        """

        if type(key) != keyboard.KeyCode:
            self.save()
            print("Niveau sauvegardé")
            exit()

        print("Touche appuyée : ", key.char, time) 

        # Ajoute la touche pressé au niveau
        now = datetime.datetime.now()
        temps = (now - self.start_time).total_seconds()
        self.touches.append({'key': key.char, 'hold_time':time, 'hold': time != 0, 'time':temps})

    def save(self):
        """Sauvegarde dans un fichier les données du niveau
        """
        with open(LEVEL_PATH + "niveau_" + self.nom + ".json", "w", encoding="utf-8") as file:
            level_obj = {
                "Nom": self.nom,
                "Audio": self.son,
                "Difficulte": self.difficulte,
                "Touches" : self.touches
            }

            json.dump(level_obj, file)

AUDIO_PATH = os.path.dirname(__file__) + "/audios/"
LEVEL_PATH = os.path.dirname(__file__) + "/saves/"

level_creator = LevelCreator("Blue Ocean", 1, "niv1.mp3", True)
level_creator.create_level()

# Lance le compteur de touches appuyées (sur un thread séparé pour pas bloquer le programme)
counter = KeyCounter(level_creator.register_key)
thread = threading.Thread(target=counter.lancer_compteur)
thread.start()

# Permet de ne pas fermer le programme
msvcrt.getch()

# Pour les audios libre de droit, voir : https://pixabay.com/fr/music/