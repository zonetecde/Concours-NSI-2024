import doctest
import json
import os
import re
import sqlite3

import unicodedata
import urllib.request

class Bac:
    """Classe permettant de gérer l'exercice du jeu du bac.
    """

    def __init__(self):
        """Initialise la connexion à la base de données.
        """
        self.connexion = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "/mots.db")

    def chargement(self):
        """Depuis le fichier mots.json, récupère les diffèrents thèmes et leurs mots et les
        ajoutes dans la base de donnée
        """
        self.executer_sql("DELETE FROM mots") # Supprime tout les mots déjà existant pour éviter les doublons

        dossier_actuel = os.path.dirname(os.path.abspath(__file__))

        with open(dossier_actuel + "\mots.json", encoding="utf8") as f:
            themes = json.load(f)
            for theme in themes:
                nom = theme["Thème_"].capitalize()
                mots = []

                for liste in theme["Listes"]:
                    mots.extend(liste["Mots"])                
                
                # Ajoute tout ces mots à la base de donnée
                sql = 'INSERT INTO mots (theme, lettre, mot, mot_clean) VALUES'
                for mot in mots:
                    if(mot != ""):
                        sql += (f' ("{nom}","{mot[0].upper()}" , "{mot}", "{self.clean_mot(mot)}"),')

                sql = sql[:-1] # enlève la dernière virgule
                self.executer_sql(sql)
                
                print(f"Ajout des mots pour le thème {nom} fini")

        print("Fin de l'ajout")
        

    def clean_mot(self, mot: str):
        """Nettoie un mot en enlevant les accents et en le mettant en minuscule.
        Tous les caractères qui ne sont pas des lettres uniquement (a-z) sont supprimés.
        afin de pouvoir le comparer avec les mots écrits par le joueur.

        >>> b = Bac()
        >>> b.clean_mot("Éléphant")
        'elephant'
        >>> b.clean_mot("Marie-Antoinette")
        'marieantoinette'
        >>> b.clean_mot("École 123")
        'ecole'
        """
        mot_clean = ""
        
        for lettre in mot:
            if lettre.isalpha():
                # Enlève les accents du caractère
                sans_accent = u"".join([c for c in unicodedata.normalize('NFKD', lettre) if not unicodedata.combining(c)])
                # L'ajoute au mot
                mot_clean += sans_accent.lower()

        return mot_clean

    def executer_sql(self, requete):
        """ Exécute une requête SQL sur la base de données locale.
        """
        curseur = self.connexion.cursor()

        # Exécute la requête
        curseur.execute(requete)

        # Valide les changements
        self.connexion.commit()

        # Récupère les résultats
        resultats = curseur.fetchall()

        # Retourne les résultats
        return resultats

    def __del__(self):
        """Ferme la connexion à la base de données lors de la destruction de l'objet.
        """
        self.connexion.close()

    @staticmethod
    def verifier_mot(self, reponses, lettre):
        """Vérifie si les réponses données par le joueur sont correctes.

        Args:
            reponses (list): Liste des réponses données par le joueur.
                             Exemple : [("Animaux", "éléphant"), ("Fruits et légumes", "épinard"), ("Pays", "Paris")]
            lettre (str): La lettre

        Returns:
            list: Liste des réponses correctes et incorrectes.
            Exemple : [True, False, True] 
        """
        # Exécute une requête SQL pour vérifier si le mot est présent dans la base de données pour le thème donné et qu'il commence par la lettre donnée
        # Si le mot est good, mettre True dans la liste, sinon False
        # Attention, ne pas oublier de passer le mot dans clean_mot avant de lancer la requête SQL pour vérifier s'il existe

        return [True, False, True, False, True]

    def url_to_html(self, url):
        """Télécharge le contenu d'une page web et le retourne sous forme de texte.
        """
        fp = urllib.request.urlopen(url)
        bytes = fp.read()

        html = bytes.decode("utf8")
        fp.close()

        return html

# =====================================
# Programme principal 
# =====================================

# Doctest
#doctest.testmod(verbose=False)

# Ajout des mots dans la base de donnée
#mot = Bac()
#mot.chargement()