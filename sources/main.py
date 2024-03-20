import os
import webview
import http.server
import socketserver
import threading
from api import Api
from config import DEBUG

def start_server():
    # Se place dans le dossier contenant les fichiers du site
    os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/web/build")
    
    # Lancement du serveur pour le site sur le port 5170
    PORT = 5170
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Serveur lancé sur le port", PORT)
        httpd.serve_forever()


def main():
    # En mode debug, le site est lancé sur le port 5173 (développement avec hot reload) 
    # sinon, le site est lancé sur le port 5170 (production)
    if not DEBUG:
        # Lancement du serveur dans un thread séparé 
        server_thread = threading.Thread(target=start_server)
        server_thread.daemon = True  # Fermeture du thread lorsque le programme principal se termine
        server_thread.start()

    # Création de l'API pour communiquer avec le site
    api = Api()

    # Création de la fenêtre avec le site
    website_port = DEBUG and 5173 or 5170
    window = webview.create_window('Key Mouse Training', 'http://localhost:' + str(website_port), js_api=api, resizable=True, min_size=(850, 650), width=1080, height=720)
    api.set_window(window)

    webview.start()

if __name__ == "__main__":
    main()