from keyboard.bac.bac import Bac
from keyboard.typescript.typescript import TypeScript
from mouse.scripts.ROSU.ROSU_menu import Rosu

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
        return Bac.verifier_mot(self, reponses, lettre)

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
    