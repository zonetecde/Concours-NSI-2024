
class NomAlgo:
    cancel = False

    def __init__(self, labyrinthe): # labyrinthe était un objet de la classe Labyrinthe
        """Initialisation de l'algorithme [nom]

        Args:
            labyrinthe (Labyrinthe): L'objet labyrinthe où le labyrinthe sera généré
        """
        self.labyrinthe = labyrinthe

    def start_generation(self):
        """Commence l'algorithme de génération sur le labyrinthe
        """
        self.cancel = False
        # reset la matrice du labyrinthe
        self.labyrinthe.init_matrice()
        
        # appel des fonctions javascript pour la représentation visuelle à chaque étape
        # et modifie en même temps la matrice labyrinthe.matrice
        # à chaque tour de boucle (étape) vérifier que self.cancel = False, sinon on cancel
        # la génération du lab (return)
        pass

    def cancel_generation(self):
        """Annule la génération en cours
        """
        self.cancel = True