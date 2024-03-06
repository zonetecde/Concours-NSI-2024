import os
import sys

from keyboard.bac.bac import Bac
from keyboard.reaction.reaction import Reaction
from keyboard.typescript.typescript import TypeScript
from keyboard.stenographie.stenographie import Stenographie

# Permet de ce placer dans le dossier contenant les scripts ROSU
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/scripts/Rosu")
from mouse.scripts.Rosu.menu import Rosu

class Api:
    """Classe Api
    Cette classe permet la communication entre le code python
    et le code javascript de la page web.

    Les méthodes de cette classe sont appelées par le code javascript
    et peuvent appeler des fonctions javascript.
    """

    def __init__(self):
        pass

    def set_window(self, window):
        """Set l'objet window pour pouvoir communiquer avec le code JS

        Args:
            window (Window): La fenêtre de webview
        """
        self.window = window

    def restart(self):
        # Ferme la fenêtre et relance le main.py
        # se place dans le meme dossier que ce fichier
        self.window.hide()

        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        os.system("py main.py")

    def ouvrir_exercice(self, nom):
        """Ouvre un exercice fait en python

        Args:
            nom (str): Le nom de l'exercice
        """
        if nom == "Rosu!":
            Rosu.start_rosu()

    def recuperer_phrase_aleatoire_typescript(self, langue: str):
        """Récupère une phrase aléatoire d'un article wikipedia aléatoire pour l'exercice 'Type Script'

        Args:
            langue (str): La langue de la phrase
        """
        return TypeScript.get_random_sentence(self, langue)

    def calculer_score_typescript(self, data):
        """Calcule le score de l'exercice 'Type Script' à partir des données de l'utilisateur

        Args:
            data (dict): Les données de l'utilisateur : 
                         le temps mis, le nombre d'erreurs et le nombre de caractères total
        """
        return TypeScript.calculer_score_typescript(self, data)
    
    def verifier_mot_bac(self, reponses, lettre):
        """Vérifie si les réponses données par le joueur sont correctes dans l'exercice 'Bac'

        Args:
            reponses (list): Liste des réponses du joueur.
            lettre (str): La lettre

        Returns:
            list: Liste des réponses correctes et incorrectes.
                Exemple : [True, False, True] 
        """
        bac = Bac()
        return bac.verifier_mot(reponses, lettre)
    
    def get_themes_bac(self):
        """Récupère les thèmes pour l'exercice 'Bac' à partir de la lettre donnée

        Args:
            lettre (str): La lettre
        """
        bac = Bac()
        return bac.get_themes()
    
    def get_valid_letters_bac(self, themes):
        """Récupère les lettres valides (= les lettres possibles) pour l'exercice 'Bac'
        """
        bac = Bac()
        return bac.get_valid_letters(themes)
    
    def init_reaction(self, autoriser_accent, autoriser_maj, autoriser_speciaux, nombre):
        """Initialise l'exercice 'Réaction'

        Args:
            autoriser_accent (boolean): Est-ce que les suites de caractères peuvent contenir des accents ?
            autoriser_maj (boolean): Est-ce que les suites de caractères peuvent contenir des majuscules ?
            autoriser_speciaux (boolean): Est-ce que les suites de caractères peuvent contenir des caractères spéciaux ?
            nombre (int): Le nombre de réactions à générer
        """
        return Reaction.init_reactions(autoriser_accent, autoriser_maj, autoriser_speciaux, nombre)
    
    def lancer_reaction(self, index):
        """Pour l'exercice "Réaction", lance la réaction à l'index donné

        Args:
            index (int): L'index de la réaction à lancer
        """
        return Reaction.lancer_reaction(self, index, self)
    
    def calculer_score_reaction(self, data):
        """Calcule le score de l'exercice 'Réaction' à partir des données de l'utilisateur

        Args:
            data (list): Les données de l'utilisateur : 
                         Une liste au format [[reaction, temps], [reaction, temps], [reaction, temps], ...]
        """
        return Reaction.calculer_score_reaction(data)

    def recuperer_phrase_aleatoire_voxforge(self, langue):
        """Récupère une phrase aléatoire de voxforge.org

        Args:
            langue (str): La langue de la phrase

        Returns:    
            list: Les phrases avec leurs audios
        """
        ste = Stenographie()
        return ste.get_audios_with_texts(langue)
    
    def verifier_phrase_stenographie(self, phrase_original, phrase_tapee, majs, orthographe, ponctuations):
        """Vérifie si la phrase donnée par le joueur est correcte

        Args:
            phrase_original (str): La phrase originale
            phrase_tapee (str): La phrase donnée par le joueur
            majs (bool): Est-ce que on compare les majuscules ?
            orthographe (bool): Est-ce que on compare l'orthographe ?
            ponctuations (bool): Est-ce que on compare les ponctuations ?
        """
        ste = Stenographie()
        return ste.verifier_phrase(phrase_original, phrase_tapee, majs, orthographe, ponctuations)

    def call_js_function(self, function_name, params = ""):
        """Appel une fonction javascript dans la page web

        Args:
            function_name (str): Le nom de la fonction
            params (str): Les paramètres à passé à la fonction
                          Attention à ne pas oublier de mettre des "" s'il s'agit d'un str
        """
        self.window.evaluate_js("window.{function}({params})"
                                .format(function = function_name, 
                                        params = params))
    