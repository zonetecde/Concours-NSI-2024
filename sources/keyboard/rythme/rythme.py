import json
import os
import random
from time import sleep

class Rythme:
    """Classe permettant de gérer l'exercice "Rythme"
    """
    @staticmethod
    def recuperer_niveaux():
        """Recupere les niveaux"""
        # Les niveaux se trouvent dans le dossier `/saves/`
        folder = os.path.dirname(os.path.abspath(__file__)) + "/saves/"

        if not os.path.exists(folder):
            os.makedirs(folder)

        files = os.listdir(folder)

        niveaux_txt = [f for f in files if f.endswith(".json") and "copy" not in f]
        niveaux = [json.load(open(folder + f, "r", encoding="utf-8")) for f in niveaux_txt]

        return niveaux
