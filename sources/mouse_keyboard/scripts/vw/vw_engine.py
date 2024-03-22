import pygame
import random
import time
import sys
import os 
import sqlite3

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/scripts/vw")


class MotObject(pygame.sprite.Sprite):
    def __init__(self, mot, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.mot = mot
        self.image = pygame.Surface((100, 50))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        self.rect.x += 1
        if self.rect.x > 1280:
            self.kill()

    
        

class Jeu:
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
        self.score = 0
        self.temps_debut = 0
        self.duree_jeu = 60
        self.en_cours = True
        self.input_text = ""
        self.rate = 0
        self.temps_avant_nouveau_mot = 1 # Temps avant d'ajouter un nouveau mot

        self.connexion = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "/mots.db")
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
        lettre_ecrites = self.input_text.lower()
        mot_incomplet = mot_clique.lower()

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
        self.score += mot.count(self.CHARACTERE_DE_REMPLACEMENT)

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
                self.incrementer_score(mot_clique)
                # Supprime le mot cliqué de l'écran
                del self.rectangles_mots[mot_clique]
                # Réinitialise l'input
                self.input_text = ""
            else:
                self.rate += 1

    def ajouter_mot(self):
        """ Ajoute un mot à l'écran toutes les 3 secondes
        """
        # Génère un mot toutes les 3 secondes
        if time.time() - self.temps_debut >= self.temps_avant_nouveau_mot:
            # Génère un mot aléatoire
            mot = self.generer_mot()
            # Ajoute le mot à l'écran
            #mot_obj = MotObject(mot, 0, random.randint(100, self.hauteur_ecran - 100))

            

            rect_mot = self.police.render(mot, True, self.NOIR).get_rect(
                center=(
                    #random.choice([0, self.largeur_ecran]), je fixerais pour avoir les 2 cotes
                    0,
                    random.randint(100, self.hauteur_ecran - 100),
                )
            )
            self.rectangles_mots[mot] = rect_mot
            self.duree_jeu -= 1
            self.temps_debut = time.time()
            self.temps_avant_nouveau_mot = random.randint(1, 3)

    def deplacer_mots(self):
        """Déplace les mots d'un côté à l'autre de l'écran
        """
        for mot, rect in list(self.rectangles_mots.items()):
            rect.move_ip(self.VITESSE_DEFILEMENT, 0) 
            if rect.centerx > self.largeur_ecran:
                del self.rectangles_mots[mot]
                self.rate += 1

    def start(self):
        # Initialiser pygame
        pygame.init()

        # Configurer l'affichage
        self.ecran = pygame.display.set_mode((self.largeur_ecran, self.hauteur_ecran), pygame.FULLSCREEN)
        pygame.display.set_caption("Verbal Warfare")

        # Initialiser le dictionnaire des rectangles de mots
        self.rectangles_mots = {}

        # Définir la police
        self.police = pygame.font.Font(None, 36)

        # Définir le temps de début
        self.temps_debut = time.time()

        # Boucle de jeu
        while self.en_cours:
            # Effacer l'écran
            self.ecran.fill(self.BLANC)

            # Vérifier les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.en_cours = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)

                elif event.type == pygame.KEYDOWN:
                    # Gérer la saisie de l'utilisateur
                    if event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.input_text = ""
                    elif event.key == pygame.K_ESCAPE:
                        self.en_cours = False  
                    else:
                        self.input_text += event.unicode

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

            # Dessiner le temps restant à l'écran
            texte_temps = self.police.render("Temps : " + str(self.duree_jeu), True, self.NOIR)
            self.ecran.blit(
                texte_temps, (self.largeur_ecran - texte_temps.get_width() - 10, 10)
            )

            # Dessiner la zone d'input
            texte_input = self.police.render(self.input_text, True, self.NOIR)
            rect_input = texte_input.get_rect(center=(self.largeur_ecran // 2, self.hauteur_ecran - 50))
            pygame.draw.rect(self.ecran, self.BLANC, rect_input)
            pygame.draw.rect(self.ecran, self.NOIR, rect_input, 2)
            self.ecran.blit(texte_input, rect_input)
            
            # Terminer le jeu après 60 secondes
            if self.duree_jeu <= 0:
                self.en_cours = False
                
            # Mettre à jour l'affichage
            pygame.display.flip()

        # Fin du jeu
        texte_fin_jeu = self.police.render("Fin du jeu", True, self.NOIR)
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
        pygame.display.flip()

        # Attendre quelques secondes avant de quitter
        pygame.time.wait(2000)

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

        print(mot_complet, mot)
        return mot

    def executer_sql(self, requete):
        """ Exécute une requête SQL sur la base de données locale.
        """
        curseur = self.connexion.cursor()

        # Exécute la requête
        curseur.execute(requete)

        # Récupère les résultats
        resultats = curseur.fetchall()

        # Retourne les résultats
        return resultats
    
if __name__ == "__main__":
    pygame.init()

    jeu = Jeu()
    jeu.start()
