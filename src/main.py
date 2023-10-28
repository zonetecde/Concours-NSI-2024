import webview

from api.api import Api
from models.Labyrinthe import Labyrinthe
    
def main():
    lab = Labyrinthe(20,10)
    lab.draw()

    lab.export("test.txt", 'txt')

    # Instancie l'Api pour communiquer avec la page web
    api = Api()
    window = webview.create_window('Nom du projet', './web/build/index.html', js_api=api, resizable=True, min_size=(800, 600), width=1080, height=720)
    api.set_window(window) 

    webview.start() 

if __name__ == "__main__":
        main()