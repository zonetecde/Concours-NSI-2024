from keyboard.typescript import TypeScript
from mouse.scripts.ROSU.ROSU_menu import Rosu

class Api:
    """Classe Api
    Cette classe permet la communication entre le code python
    et le code javascript de la page web.

    Pour appeler du code python depuis javascript : 
    pywebview.api.nom_de_la_methode_python().then((e) => {
        // ce que python a retourné se trouve dans la variable e 
    });

    Pour appeler du code javascript depuis python :
    self.call_js_function(nom_de_la_fonction, parametres)
    """

    def __init__(self):
        pass

    def set_window(self, window):
        """Set l'objet window pour pouvoir communiquer avec le code JS

        Args:
            window (Window): La fenêtre de webview
        """
        self.window = window

    def openPythonProject(self, nom):
        """Ouvre un exercice fait en python

        Args:
            nom (str): Le nom de l'exercice
        """
        print("test")
        if nom == "Rosu!":
            print("test2")

            Rosu.start_rosu()

    def recuperer_phrase_aleatoire_typescript(self):
        """Biais de communication entre le code javascript et le code python. 
        Récupère une phrase aléatoire d'un article wikipedia aléatoire pour l'exercice 'Type Script'"""
        return {"phrase": TypeScript.get_random_sentence(self)}

    def calculer_score_typescript(self, data):
        """Biais de communication entre le code javascript et le code python.
        Calcule le score de l'exercice 'Type Script'"""
        return TypeScript.calculer_score_typescript(self, data)
    
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
    