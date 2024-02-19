import random


class Reaction:
    """Classe permettant de gérer l'exercice "Réaction"
    """

    @staticmethod
    def recuperer_reactions(autoriser_accent, autoriser_maj, autoriser_speciaux):
        """Renvoie une liste contenant les différents
        caractères à écrire le plus vite possible ainsi que leur temps d'apparition en ms    

        Args:
            autoriser_accent (boolean): Est-ce que les suites de caractères peuvent contenir des accents ?
            autoriser_maj (boolean): Est-ce que les suites de caractères peuvent contenir des majuscules ?
            autoriser_speciaux (boolean): Est-ce que les suites de caractères peuvent contenir des caractères spéciaux ?

        Returns: 
            list: Liste de tuples contenant le temps d'apparition et la suite de caractères à écrire

        Exemple d'output : [(500, "h"), (1900, "zoi"), (4100, "vx"), (700, "lOi")]
        """
        # [*str] transforme str en une liste de chaine de caractère
        alphabet_maj = [*"ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
        accents = [*("éèàùçêë" * 2)] # x2 pour qu'ils y soient plus souvent
        speciaux = [*(".,;:!?$%&()-_@" * 2)] # x2 pour qu'ils y soient plus souvent

        caracteres_possible = [*"abcdefghijklmnopqrstuvwxyz"]

        if autoriser_accent:
            caracteres_possible.extend(accents)
        if autoriser_maj:
            caracteres_possible.extend(alphabet_maj)
        if autoriser_speciaux:
            caracteres_possible.extend(speciaux)

        liste = []

        for i in range(10):
            # entre 400ms et 6 secondes
            temps_aleatoire = random.randint(400, 6000)

            # composition de la chaine aléatoire
            longueur = random.randint(1, 4)
            
            chaine_aleatoire = ""
            for _ in range(longueur):
                caractere_aleatoire = random.choice(caracteres_possible)
                chaine_aleatoire += caractere_aleatoire

            # ajoute la réaction
            liste.append((temps_aleatoire, chaine_aleatoire))

        return liste

                
print(Reaction.recuperer_reactions(True, True, True))