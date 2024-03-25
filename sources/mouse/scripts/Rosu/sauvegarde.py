import json
from typing import List

class Sauvegarde:
    """Classe Sauvegarde. Permet de stocker les données de sauvegarde du joueur.
    """

    def __init__(self, nom_niveau, meilleur_score = "", note = "", precision = 0) -> None:
        """Constructeur de la classe Sauvegarde

        Args:
            nom_niveau (str): Le nom du niveau associé à la sauvegarde.
            meilleur_score (str, optional): Le meilleur score du joueur. Defaults to "".
            note (str, optional): La note du joueur. Defaults to "".
            precision (int, optional): La précision du joueur. Defaults to 0.
        """
        self.nom_niveau = nom_niveau # Nom du niveau de la sauvegarde
        self.meilleur_score = meilleur_score  # Meilleur score du joueur
        self.note = note # Note du joueur
        self.precision = precision # Précision du joueur
