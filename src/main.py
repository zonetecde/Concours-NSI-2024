import webview

from api.api import Api
from models.Labyrinthe import Labyrinthe
    
def main():
    lab = Labyrinthe(20,10)
    lab.draw()

    lab.export("test.txt", 'txt')

    # Instancie l'Api pour communiquer avec la page web
    api = Api()
    window = webview.create_window('Nom du projet', './web/index.html', js_api=api)
    api.set_window(window)  
    webview.start() 

if __name__ == "__main__":
        main()