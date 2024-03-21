import pygame
import random
import time
import sys
import os 
import sqlite3

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/scripts/vw")


class Jeu:
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

    def demarrer(self):
        # Initialiser pygame
        pygame.init()

        # Configurer l'affichage
        self.ecran = pygame.display.set_mode((self.largeur_ecran, self.hauteur_ecran), pygame.FULLSCREEN)
        pygame.display.set_caption("Verbal Warfare")

        # Définir les couleurs
        BLANC = (255, 255, 255)
        NOIR = (0, 0, 0)

        # Initialiser le dictionnaire des rectangles de mots
        self.rectangles_mots = {}

        # Définir la police
        self.police = pygame.font.Font(None, 36)

        # Définir le temps de début
        self.temps_debut = time.time()

        # Boucle de jeu
        while self.en_cours:
            # Effacer l'écran
            self.ecran.fill(BLANC)

            # Vérifier les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.en_cours = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Vérifier si le clic de souris est sur un mot
                    pos = pygame.mouse.get_pos()
                    mot_clique = None
                    for mot, rect in self.rectangles_mots.items():
                        if rect.collidepoint(pos):
                            mot_clique = mot
                            break

                    # Si un mot est cliqué et le contenu de l'input correspond, augmenter le score et générer un nouveau mot
                    if mot_clique and self.input_text.lower() == mot_clique[1].lower():
                        self.score += 1
                        del self.rectangles_mots[mot_clique]
                        self.input_text = ""

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

            # Générer un nouveau mot toutes les secondes
            if time.time() - self.temps_debut >= 1:
                mot = self.generer_mot()
                rect_mot = self.police.render(mot[1], True, NOIR).get_rect(
                    center=(
                        #random.choice([0, self.largeur_ecran]), je fixerais pour avoir les 2 cotes
                        0,
                        random.randint(100, self.hauteur_ecran - 100),
                    )
                )
                self.rectangles_mots[mot] = rect_mot
                self.duree_jeu -= 1
                self.temps_debut = time.time()
                
            # Déplacer les mots d'un côté à l'autre de l'écran
            for mot, rect in list(self.rectangles_mots.items()):
                rect.move_ip(1, 0) 
                if rect.centerx > self.largeur_ecran:
                    del self.rectangles_mots[mot]  
        

            # Dessiner les mots à l'écran
            for mot, rect in self.rectangles_mots.items():
                self.ecran.blit(self.police.render(mot[0], True, NOIR), rect)

            # Dessiner le score à l'écran
            texte_score = self.police.render("Score : " + str(self.score), True, NOIR)
            self.ecran.blit(texte_score, (10, 10))

            # Dessiner le temps restant à l'écran
            texte_temps = self.police.render("Temps : " + str(self.duree_jeu), True, NOIR)
            self.ecran.blit(
                texte_temps, (self.largeur_ecran - texte_temps.get_width() - 10, 10)
            )

            # Dessiner la zone d'input
            texte_input = self.police.render(self.input_text, True, NOIR)
            rect_input = texte_input.get_rect(center=(self.largeur_ecran // 2, self.hauteur_ecran - 50))
            pygame.draw.rect(self.ecran, BLANC, rect_input)
            pygame.draw.rect(self.ecran, NOIR, rect_input, 2)
            self.ecran.blit(texte_input, rect_input)
            
            # Terminer le jeu après 60 secondes
            if self.duree_jeu <= 0:
                self.en_cours = False
                
            # Mettre à jour l'affichage
            pygame.display.flip()



        # Fin du jeu
        texte_fin_jeu = self.police.render("Fin du jeu", True, NOIR)
        texte_score = self.police.render("Score : " + str(self.score), True, NOIR)
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
        pygame.time.wait(3000)

        # Quitter pygame
        pygame.quit()
        

    def generer_mot(self):
        # Connect to the database
        #conn = sqlite3.connect('mots.db')
        #cursor = conn.cursor()

        # Fetch all the words from the database
        #cursor.execute("SELECT mot FROM mots")
        #mots = [row[0] for row in cursor.fetchall()]

        # Close the database connection
        #conn.close()
        mots = ["rayane", "lilian", "mathieu", "esteban", "penelope"]
        mot_complet = random.choice(mots)
        index = random.randint(0, len(mot_complet) - 1)
        mot_incomplet = mot_complet[:index] + "_" + mot_complet[index+1:]
        return mot_incomplet, mot_complet


