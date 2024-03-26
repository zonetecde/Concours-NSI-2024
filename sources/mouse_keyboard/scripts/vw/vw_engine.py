import pygame
import random
import time
import sys
import os 
import sqlite3
import queue 

ASSETS_FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/assets/"

class Engine:
    """Gère l'execution de l'exercice Verbal Warfare
    """
    CHARACTERE_DE_REMPLACEMENT = "_"
    BLANC = (255, 255, 255)
    NOIR = (0, 0, 0)
    VITESSE_DEFILEMENT = 1
    
    def __init__(self):
        self.largeur_ecran = pygame.display.get_desktop_sizes()[0][0]
        self.hauteur_ecran = pygame.display.get_desktop_sizes()[0][1]
        self.ecran = None
        self.police = None
        self.rectangles_mots = {}
        self.score = 0 # Score de l'utilisateur
        self.temps_dernier_mot = 0 # Temps du dernier mot ajouté
        self.temps_debut = 0 # Temps du début du jeu
        self.duree_jeu = 60 # Durée du jeu max
        self.en_cours = True
        self.input_text = "" # Texte saisi par l'utilisateur
        self.rate = 0 # Nombre de mots ratés
        self.temps_avant_nouveau_mot = 1 # Temps avant d'ajouter un nouveau mot
        self.chargeur = queue.Queue() # Chargeur de mots
        self.combo = 0 # Combo de mots réussis
        self.connexion = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "/mots.db") # Connexion à la base de données
        self.dictionnaires = self.executer_sql("SELECT mot FROM mots") # Récupère tous les mots de la base de données

    def verifier_mot_clique(self, pos):
        """
        Vérifie si un mot a été cliqué par l'utilisateur

        Args:
            pos (tuple): La position du clic de l'utilisateur
        """
        mot_clique = None
        for mot, rect in self.rectangles_mots.items():
            if rect.collidepoint(pos):
                mot_clique = mot
                break
        return mot_clique

    def remplir_mot(self, mot_clique):
        """
        Remplis le mot cliqué par l'utilisateur avec les lettres écrites

        Args:
            mot_clique (str): Le mot cliqué par l'utilisateur (ex: "B__jour")
            
        Returns:
            str: Le mot à compléter (ex: "Bonjour")
        """
        if self.chargeur.empty():
            lettre_ecrites = self.input_text.lower()
        else:
            lettre_ecrites = self.chargeur.get()
            
        mot_incomplet = mot_clique.lower()

        if not mot_clique:
            return ""
        if len(lettre_ecrites) < mot_incomplet.count(self.CHARACTERE_DE_REMPLACEMENT):
            return mot_clique

        # remplace les lettres par des `_` pour comparer
        z = 0
        for i in range(len(mot_incomplet)):
            if mot_incomplet[i] == self.CHARACTERE_DE_REMPLACEMENT:
                mot_incomplet = mot_incomplet[:i] + lettre_ecrites[z] + mot_incomplet[i+1:]
                z += 1

        return mot_incomplet

    
    def check_existance(self, mot):
        """
        Vérifie si le mot existe dans la base de données

        Args:
            mot (str): Le mot à vérifier
            
        Returns:
            bool: True si le mot existe, False sinon
        """
        data = self.executer_sql(f"SELECT mot FROM mots WHERE mot = '{mot}'")
        return len(data) > 0

    def incrementer_score(self, mot):
        """
        Incrémente le score de l'utilisateur

        Args:
            mot (str): Le mot qui a été complété (ex: "B__jour")
        """
        if self.combo > 0:
            self.score += round(mot.count(self.CHARACTERE_DE_REMPLACEMENT)*(self.VITESSE_DEFILEMENT/2)*self.combo)
        else:
            self.score += round(mot.count(self.CHARACTERE_DE_REMPLACEMENT)*(self.VITESSE_DEFILEMENT/2))

    def handle_mouse_click(self, pos):
        """
        Gère le clic de l'utilisateur

        Args:
            pos (tuple): La position du clic de l'utilisateur
        """
        mot_clique = self.verifier_mot_clique(pos)
        if mot_clique:
            mot_complet = self.remplir_mot(mot_clique)
            if self.check_existance(mot_complet):
                self.combo +=1
                self.incrementer_score(mot_clique)
                # Supprime le mot cliqué de l'écran
                del self.rectangles_mots[mot_clique]
                # Réinitialise l'input
                self.input_text = ""
                # Joue le son de shoot
                pygame.mixer.music.load(ASSETS_FOLDER + "shoot.mp3")
                pygame.mixer.music.play()
            else:
                self.rate += 1
                self.combo = 0

    def ajouter_mot(self):
        """ Ajoute un mot à l'écran toutes les 3 secondes
        """
        # Génère un mot toutes les 3 secondes
        if time.time() - self.temps_dernier_mot >= self.temps_avant_nouveau_mot:
            # Génère un mot aléatoire
            mot = self.generer_mot()
            # Ajoute le mot à l'écran
            rect_mot = self.police.render(mot, True, self.NOIR).get_rect(
                center=(
                    0,
                    random.randint(100, self.hauteur_ecran - 100),
                )
            )
            self.rectangles_mots[mot] = rect_mot
            self.temps_dernier_mot = time.time()
            self.temps_avant_nouveau_mot = random.randint(3, 6)

    def deplacer_mots(self):
        """Déplace les mots d'un côté à l'autre de l'écran
        """
        for mot, rect in list(self.rectangles_mots.items()):
            rect.centerx += self.VITESSE_DEFILEMENT
            if rect.centerx > self.largeur_ecran:
                del self.rectangles_mots[mot]
                self.rate += 1
                self.combo = 0

    def afficher_viseur(self, pos):
        """Affiche l'image du viseur à la position de la souris

        Args:
            pos (tuple): La position de la souris
        """
        viseur = pygame.image.load(ASSETS_FOLDER + "viseur.png")
        viseur = pygame.transform.scale(viseur, (110, 110))
        self.ecran.blit(viseur, (pos[0] - viseur.get_width() // 2, pos[1] - viseur.get_height() // 2))

    def start(self, difficulte=1):
        self.VITESSE_DEFILEMENT = difficulte
        # Initialiser pygame
        pygame.init()

        # Configurer l'affichage
        self.ecran = pygame.display.set_mode((self.largeur_ecran, self.hauteur_ecran), pygame.FULLSCREEN)
        pygame.display.set_caption("Verbal Warfare")

        # Initialiser le dictionnaire des rectangles de mots
        self.rectangles_mots = {}

        # Définir la police
        self.police = pygame.font.Font(None, self.hauteur_ecran // 16)

        # Définir le temps de début
        self.temps_debut = time.time()

        # Charger l'image de fond
        background = pygame.image.load(ASSETS_FOLDER + "background.jpg")
        background = pygame.transform.scale(background, (self.largeur_ecran, self.hauteur_ecran))
        
        # Boucle de jeu
        while self.en_cours:
            # Affiche l'image de fond
            self.ecran.blit(background, (0, 0))

            # Vérifier les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.en_cours = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)

                elif event.type == pygame.KEYDOWN:
                    # Joue le son de la touche pressée
                    pygame.mixer.music.load(ASSETS_FOLDER + "keypress.mp3")
                    pygame.mixer.music.play()
                    # Gérer la saisie de l'utilisateur
                    if event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.input_text = ""
                    elif event.key == pygame.K_ESCAPE:
                        self.en_cours = False  
                    elif event.key == 1073742050 or event.key == pygame.K_SPACE or  event.key == pygame.K_RETURN: #code de alt
                        #met le contenu de l'input dans le chargeur  
                        self.chargeur.put(self.input_text)
                        self.input_text = ""
                    else:
                        self.input_text += event.unicode

            # Affiche l'image du viseur à la position de la souris
            self.afficher_viseur(pygame.mouse.get_pos())

            # Générer un nouveau mot toutes les X secondes
            self.ajouter_mot()
                
            # Déplacer les mots d'un côté à l'autre de l'écran
            self.deplacer_mots()
    
            # Dessiner les mots à l'écran
            for mot, rect in self.rectangles_mots.items():
                self.ecran.blit(self.police.render(mot, True, self.NOIR), rect)

            # Dessiner le score à l'écran
            texte_score = self.police.render("Score : " + str(self.score), True, self.NOIR)
            self.ecran.blit(texte_score, (10, 10))

            # calcul le temps restant
            self.duree_jeu = 60 - int(time.time() - self.temps_debut)

            # Dessiner le temps restant à l'écran
            texte_temps = self.police.render("Temps : " + str(self.duree_jeu), True, self.NOIR)
            self.ecran.blit(
                texte_temps, (self.largeur_ecran - texte_temps.get_width() - 10, 10)
            )
            
            texte_chargeur = self.police.render("Chargeur : "+ str(list(self.chargeur.queue)), True, self.NOIR)
            self.ecran.blit(
                texte_chargeur, (self.largeur_ecran - texte_chargeur.get_width() - 50, 60)
            )
            
            texte_combo = self.police.render("Combo : "+ str(self.combo), True, self.NOIR)
            self.ecran.blit(
                texte_combo, (self.largeur_ecran - texte_combo.get_width() - 50, 110)
            )

            # Dessiner la zone d'input qui fait du 200x50, bord noir et fond blanc
            input_width = max(200, self.police.size(self.input_text)[0] + 10)
            
            pygame.draw.rect(self.ecran, self.NOIR, (self.largeur_ecran // 2 - input_width // 2, self.hauteur_ecran - 100, input_width, 50))
            pygame.draw.rect(self.ecran, self.BLANC, (self.largeur_ecran // 2 - input_width // 2 + 2, self.hauteur_ecran - 98, input_width - 4, 46))

            # dessine le texte saisi par l'utilisateur
            texte_input = self.police.render(self.input_text, True, self.NOIR)
            self.ecran.blit(
                texte_input,
                (
                    self.largeur_ecran // 2 - texte_input.get_width() // 2,
                    self.hauteur_ecran - 95,
                ),
            )
            

            # Terminer le jeu après 60 secondes
            if self.duree_jeu <= 0:
                self.en_cours = False
                
            # Mettre à jour l'affichage
            pygame.display.flip()

        # Fin de l'exercice
        texte_fin_jeu = self.police.render("Fin de l'exercice", True, self.NOIR)
        texte_score = self.police.render("Score : " + str(self.score), True, self.NOIR)
        self.ecran.blit(
            texte_score,
            (
                self.largeur_ecran // 2 - texte_score.get_width() // 2,
                self.hauteur_ecran // 2 - texte_score.get_height() // 2 - 50,
            )
        )
        self.ecran.blit(
            texte_fin_jeu,
            (
                self.largeur_ecran // 2 - texte_fin_jeu.get_width() // 2,
                self.hauteur_ecran // 2 - texte_fin_jeu.get_height() // 2,
            ),
        )
        texte_precision = self.police.render("Raté(s) : " + str(self.rate), True, self.NOIR)
        self.ecran.blit(
            texte_precision,
            (
                self.largeur_ecran // 2 - texte_score.get_width() // 2,
                self.hauteur_ecran // 2 - texte_score.get_height() // 2 - 100,
            )
        )
        pygame.display.flip()

        # Attendre quelques secondes avant de quitter
        pygame.time.wait(3000)

        # Quitter pygame
        pygame.quit()
        

    def generer_mot(self):
        """Génère un mot aléatoire à compléter.

        Returns:
            tuple: Dans la forme (mot_complet, mot_incomplet)
            exemple: ("Bonjour", "B__jour")
        """
        mot = ""

        # Choisit un mot aléatoire dans la liste des mots >= 5 lettres
        while len(mot) < 5:
            mot = random.choice(self.dictionnaires)[0]

        # Met des `_` dans le mot (maximum 3) pour compléter le mot
        mot_complet = mot
        nombre_lettres_a_ajouter = random.randint(1, 2)
     
        indices = random.randint(0, len(mot) - nombre_lettres_a_ajouter - 1)
        for index in range(indices, indices + nombre_lettres_a_ajouter):
            mot = mot[:index] + self.CHARACTERE_DE_REMPLACEMENT + mot[index + 1:]

        return mot

    def executer_sql(self, requete):
        """ Exécute une requête SQL sur la base de données locale.
        """
        curseur = self.connexion.cursor()

        try:
            # Exécute la requête
            curseur.execute(requete)

            # Récupère les résultats
            resultats = curseur.fetchall()
        except Exception as e:
            resultats = [] # Si la requête contient des accents ou autes

        # Retourne les résultats
        return resultats
    
if __name__ == "__main__":
    pygame.init()

    jeu = Engine()
    jeu.start()
