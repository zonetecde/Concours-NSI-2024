import os
import sqlite3


class Bac:
    """Classe permettant de gérer l'exercice du jeu du bac.
    """

    def chargement(self):
        """Depuis deux sites internets, récupère les mots de chaque thème 
        et les enregistre dans une base de données locale.
        """
        # site 1 : https://liste-mots.com/dico-du-petit-bac/
        # site 2 : https://dico-petitbac.com/

        # Pour procéder, on va télécharger les pages web de ces sites
        # par exemple, pour le site 1 :
        urls = [("https://liste-mots.com/dico-du-petit-bac/liste-des-animaux-de-a-a-z/", "Animaux"),
                ("https://liste-mots.com/dico-du-petit-bac/liste-des-fruits-et-legumes/", "Fruits et légumes"),
                ("https://liste-mots.com/dico-du-petit-bac/liste-des-pays-du-monde/", "Pays"),
                ("https://liste-mots.com/dico-du-petit-bac/liste-des-legumes-a-a-z/", "Légumes"),
                ("https://liste-mots.com/dico-du-petit-bac/liste-des-fruits-a-a-z/", "Fruits"),
                ("https://liste-mots.com/dico-du-petit-bac/liste-des-capitales-du-monde-a-a-z/", "Capitales"),
                ("https://liste-mots.com/dico-du-petit-bac/liste-des-animaux-de-a-a-z/liste-des-races-de-chiens-de-a-a-z/", "Races de chiens"),
                ("https://liste-mots.com/dico-du-petit-bac/liste-des-fleurs-a-a-z/", "Fleurs"),
                ("https://liste-mots.com/dico-du-petit-bac/liste-de-prenoms-de-garcon-et-de-fille-a-a-z/prenoms-de-fille/", "Prénoms de fille"),
                ("https://liste-mots.com/dico-du-petit-bac/liste-de-prenoms-de-garcon-et-de-fille-a-a-z/liste-de-prenoms-de-garcon/", "Prénoms de garçon"),
                ("https://liste-mots.com/dico-du-petit-bac/liste-de-films/", "Films"),
                ("https://liste-mots.com/dico-du-petit-bac/liste-des-series-tv-de-a-a-z/", "Séries TV"),
                ("https://liste-mots.com/dico-du-petit-bac/liste-des-fromages/", "Fromages"),
                ("https://liste-mots.com/dico-du-petit-bac/liste-des-couleurs-de-a-a-z/", "Couleurs"),
                ("https://liste-mots.com/dico-du-petit-bac/liste-dacteurs-et-dactrices/", "Acteurs et actrices"),
                ("https://liste-mots.com/dico-du-petit-bac/liste-des-pokemon-a-a-z/", "Pokémon"),
                ("https://liste-mots.com/dico-du-petit-bac/liste-de-vetements/", "Vêtements"),
                ("https://liste-mots.com/dico-du-petit-bac/liste-de-moyens-de-transport/", "Moyens de transport"),
                ("https://liste-mots.com/dico-du-petit-bac/liste-des-metiers-de-a-a-z/", "Métiers"),
                ("https://liste-mots.com/dico-du-petit-bac/liste-de-tout-les-sports-a-a-z/", "Sports"),
                ("https://liste-mots.com/dico-du-petit-bac/liste-des-outils/", "Outils"),
                ("https://liste-mots.com/dico-du-petit-bac/liste-des-qualites-et-defauts-a-a-z/", "Qualités et défauts"),
                ("https://liste-mots.com/dico-du-petit-bac/parties-du-corps-humain/", "Parties du corps humain"),
                ("https://liste-mots.com/dico-du-petit-bac/liste-dobjets/", "Objets"),
                ("https://liste-mots.com/liste-des-marques/", "Marques"),
                ("https://liste-mots.com/marques-de-voitures/", "Marques de voitures")]
        
        # Pour chaque url, on télécharge la page web
        # On récupère les mots de la page (en regardant ils sont entre quelles balises)
        # On enregistre les mots dans la base de données locale (sqlite3)
        # On oublie pas de nettoyer les mots avant de les enregistrer dans la base de données avec la méthode clean_mot

        # INSERT INTO mots (theme, mot) values ("le theme", "le mot en minusucle et sans accent")

    def clean_mot(self, mot):
        """Nettoie un mot en enlevant les accents et en le mettant en minuscule.
        Tous les caractères qui ne sont pas des lettres uniquement (a-z) sont supprimés.
        Exemple : "Éléphant" devient "elephant", "École 123" devient "ecole", "Marie-Antoinette" devient "marieantoinette"
        afin de pouvoir le comparer avec les mots écrits par le joueur.
        """
        # Retourne le mot en minuscule, sans accents
        pass

    def executer_sql(self, requete):
        """ Exécute une requête SQL sur la base de données locale.
        """
        # Ouvre la base de données
        connexion = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "/mots.db")
        curseur = connexion.cursor()

        # Exécute la requête
        curseur.execute(requete)

        # Récupère les résultats
        resultats = curseur.fetchall()

        # Ferme la base de données
        connexion.close()

        # Retourne les résultats
        return resultats
    
    def verifier_mot(self, reponses):
        """Vérifie si les réponses données par le joueur sont correctes.

        Args:
            reponses (list): Liste des réponses données par le joueur.
            Exemple : [("Animaux", "éléphant"), ("Fruits et légumes", "épinard"), ("Pays", "Paris")]

        Returns:
            list: Liste des réponses correctes et incorrectes.
            Exemple : [True, False, True] 
        """
        # Exécute une requête SQL pour vérifier si le mot est présent dans la base de données pour le thème donné
        # Si le mot est présent, retourne True, sinon retourne False
        # Attention, ne pas oublier de passer le mot dans clean_mot avant de lancer la requête SQL pour vérifier s'il existe
        pass

# Exemple d'utilisation (à supprimer)
mot = Bac()
print(mot.executer_sql("SELECT * FROM mots"))