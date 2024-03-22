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


    """
    img 500x500 dans root
    presentation en pdf
    500 char résumé
    video matthieu
    
    candidater -> lien ppx


    FONCTIONNEMENT ET OPÉRATIONNALITÉ :
Pouvez-vous présenter l’état d’avancement du projet au moment du dépôt ? (ce qui est terminé, en cours de réalisation, reste à faire)
Quelles approches avez-vous mis en œuvre pour vérifier l’absence de bugs et garantir une facilité d'utilisation de votre projet ?
Quelles sont les difficultés rencontrées et les solutions apportées ?


Le code déposé est fonctionnel et peut être exécuté sans erreur. Il contient 5 exerices d'entraimenebt au clavier, 3 exercices d'entrainement à la souris et 1 exercice combinant le clavier et la souris.

Nous aurions aimé ajouter plus d'exercices, mais nous avons manqué de temps pour les implémenter. Nous avons également rencontré des difficultés, notammant au niveau de l'affichage en fonction de la résolution de l'écran. Nous avons ainsi dû adapter l'affichage pour que les exercices soient visibles sur tous les écrans. Une autre difficulté a été de trouver des ressources libre de droit pour les images des exercices. Nous avons donc dû créer nos propres images pour les exercices.

Les exercices sont vérifiés pour garantir leur bon fonctionnement et leur facilité d'utilisation. Nous avons mis en place des tests unitaires un peu partout dans le code pour vérifier le bon fonctionnement des fonctions. Nous avons également fait tester le logiciel par de nombreuses personnes pour vérifier la facilité d'utilisation, la compréhension des exercices et la présence d'éventuels bugs.
    """