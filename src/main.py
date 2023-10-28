import webview

from api.api import Api
    
def main():
    # Instancie l'Api pour communiquer avec la page web
    api = Api()
    window = webview.create_window('Nom du projet', './web/index.html', js_api=api, resizable=True, min_size=(800, 600), width=1080, height=720)
    api.set_window(window) 

    webview.start() 

if __name__ == "__main__":
         main()