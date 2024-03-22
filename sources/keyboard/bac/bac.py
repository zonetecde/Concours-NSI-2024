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

    def verifier_mot(self, reponses, lettre: str):
        """Vérifie si les réponses données par le joueur sont correctes.

        Args:
            reponses (list): Liste des réponses données par le joueur.
                                Exemple : [("Animaux", "éléphant"), ("Fruits et légumes", "épinard"), ("Pays", "Paris")]
            lettre (str): La lettre

        Returns:
            list: Liste des réponses correctes et incorrectes.
            Exemple : [True, False, False] 
        """
        assert len(reponses) > 0, "Il faut au moins une réponse"

        lettre = lettre.upper()
        list_rep = []

        for theme, reponse in reponses:
            clean_rep = self.clean_mot(reponse)

            if len(clean_rep) > 0 and clean_rep[0] == lettre.lower():
                resultat = self.executer_sql(f"SELECT COUNT(*) FROM mots WHERE theme = '{theme}' AND mot_clean = '{clean_rep}' AND lettre = '{lettre}'")[0][0]
                if resultat == 0:
                    list_rep.append(False)
                else:
                    list_rep.append(True)
            else:
                list_rep.append(False)
        return list_rep

    def url_to_html(self, url):
        """Télécharge le contenu d'une page web et le retourne sous forme de texte.
        """
        fp = urllib.request.urlopen(url)
        bytes = fp.read()

        html = bytes.decode("utf8")
        fp.close()

        return html
    
    def get_valid_letters(self, themes):
        """
        Renvoie les lettres qui ont des mots pour tout les themes
        """
        assert len(themes) > 0, "Il faut au moins un thème"

        alphabet = [*"ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
        lettres_valides = []
        for lettre in alphabet:
            valide = True # On suppose que la lettre est valide jusqu'à preuve du contraire

            for theme in themes:
                # Vérifie si il y a au moins un mot pour la lettre et le thème donné	
                resultat = self.executer_sql(f"SELECT COUNT(*) FROM mots WHERE theme = '{theme}' AND lettre = '{lettre}'") [0][0]

                # Si il n'y a pas de mot pour la lettre et le thème donné, on ne le met pas dans la liste
                if resultat == 0:
                    valide = False
                    break

            if valide == True:
                lettres_valides.append(lettre)

        return lettres_valides
    
    def get_themes(self):
        """
        Récupère les themes de la base de donnée
        """
        themes = self.executer_sql("SELECT DISTINCT theme FROM mots")
        return [theme[0] for theme in themes]
                    
# =====================================
# Programme principal 
# =====================================

# Doctest
#doctest.testmod(verbose=False)

# Ajout des mots dans la base de donnée
# mot = Bac()
# print(mot.get_themes())
    