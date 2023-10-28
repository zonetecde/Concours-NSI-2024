import json

class Labyrinthe:
    matrice = []

    def __init__(self, width, height):
        """Initialisation d'un labyrinthe

        Args:
            width (int): La largeur du labyrinthe
            height (int): La hauteur du labyrinthe
        """
        self.width = width
        self.height = height

        self.init_matrice()

    def init_matrice(self):
        """Création de la matrice représentant le labyrinthe
        """
        # 0 = vide, 1 = mur
        for x in range(self.height):
            self.matrice.append([])
            for y in range(self.width):
                self.matrice[x].append('0')

        # Ajout des bordures tout autour du labyrinthe
        for x in range(self.width):
            self.matrice[0][x] = '1'
            self.matrice[self.height - 1][x] = '1'
        for y in range(self.height):
            self.matrice[y][0] = '1'
            self.matrice[y][self.width - 1] = '1'

    def draw(self):
        """Dessine le labyrinthe dans la console
        """
        for x in range(self.height):
            for y in range(self.width):
                print(self.matrice[x][y], end='')
            print()

    def export(self, filename, type='txt', add_border = True):
        """Exporte le labyrinthe dans un fichier

        TODO: Ajouter un paramètre pour l'entrée et la sortie

        Args:
            filename (str): Nom du fichier 
            type (str, optional): Type du fichier : txt ou json. Defaults to 'txt'.
        """
        # exporte le labyrinthe en plain text
        if type == 'txt':
            with open(filename, 'w') as f:
                for x in range(self.height):
                    for y in range(self.width):
                        f.write(self.matrice[x][y])
                    f.write('\n')
        # exporte le labyrinthe en json
        elif type == 'json':
            with open(filename, 'w') as f:
                f.write(json.dumps(self, default=lambda o: o.__dict__))