import os
import webview
import http.server
import socketserver
import threading
from api.api import Api

DEBUG = True

def start_server():
    # Dossier contenant les fichiers du site
    os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/web/build")
    
    # Lancement du serveur pour le site
    PORT = 5170
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Serveur lancé sur le port ", PORT)
        httpd.serve_forever()


def main():
    if not DEBUG:
        # Lancement du serveur dans un thread séparé 
        server_thread = threading.Thread(target=start_server)
        server_thread.daemon = True  # Fermeture du thread lorsque le programme principal se termine
        server_thread.start()

    # Création de l'API pour communiquer avec le site
    api = Api()
    print("test")
    # Création de la fenêtre avec le site 
    website_port = DEBUG and 5173 or 5170
    window = webview.create_window('Nom du projet', 'http://localhost:' + str(website_port), js_api=api, resizable=True, min_size=(800, 600), width=1080, height=720)
    api.set_window(window)

    webview.start()

if __name__ == "__main__":
    main()
