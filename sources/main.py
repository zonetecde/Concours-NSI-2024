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

    Un résumé de 500 caractères maximum

    Key Mouse Training est un logiciel d'entraînement à la frappe clavier et à la souris. Il propose des exercices variés pour améliorer la rapidité et la précision de la frappe clavier, ainsi que la coordination main-souris. Le logiciel est divisé en plusieurs exercices, chacun ayant ses propres règles et objectifs. Les exercices sont conçus pour être ludiques et stimulants, tout en permettant de progresser rapidement. Key Mouse Training est un outil idéal pour les personnes souhaitant améliorer leurs compétences en frappe clavier et en utilisation de la souris, que ce soit pour un usage professionnel ou personnel.

    
    Esteban THIS a réalisé l’exercice CoordiMaze avec PyGame dont il n’était pas familier. Il a ainsi acquit des nouvelles notions pour mener à bien son idée. Il a aussi trouver toutes les images et sons libre de droit utilisés dans l'ensemble des exercices de la partie sourie. 

    Lilian Fisher à réalisé l’exercice Rosu et STR avec PyGame. Ses connaissances en Lua et ses projets personnels lui ont permis de réaliser ces exercices avec aisance. Sa détermination et son envie de bien faire lui ont permis de réaliser des exercices de qualité.


Le nom du projet : Key Mouse Training

L’établissement scolaire de l’équipe : Lycée Louis-Vincent, Metz

Les membres de l’équipe : Penelope WELFRINGER-LAPAQUE, Esteban THIS, Rayane STASZEWSKI, Lilian FISCHER, Mathieu BUANNIC

Le niveau d'étude : Terminale 

La composition de la classe de NSI : 1 fille et 4 garçons (ou il demande le nombre de garçon et de fille chez les T5 ?)

Le résumé du projet : Key Mouse Training est un logiciel d'entraînement à la frappe clavier et à la souris. Il propose une diversité d'exercices pour augmenter sa vitesse et sa précision au clavier, en plus d'exercices pour améliorer la coordination entre ses mains et la souris. Le programme est séparé en différents exercices, chacun possédant ses propres règles et paramètres. Les exercices sont créés pour être ludiques et stimulants, tout en permettant de progresser rapidement.

Le lien de la vidéo :

Le lien du dossier technique : 

L’image au format PNG ou JPG : 

La présentation au format PDF : 

Le commentaire de l’enseignant : 

"""