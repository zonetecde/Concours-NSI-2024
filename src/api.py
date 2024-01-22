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

    def openMouseTrain(self):
        """Ex: cette fonction est appelé par le code javascript
        lors du clique sur le titre principal

        Returns:
            obj: Un objet avec tout ce qu'on veut renvoyer à la page
        """
        pass
    
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
    