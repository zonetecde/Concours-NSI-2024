import random
from time import sleep

class Reaction:
    """Classe permettant de gérer l'exercice "Réaction"
    """
    reactions = []

    ACCENTS = "éèàùçê"
    MAJUSCULES = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    SPECIAUX = ".,;:!?$%&()-_@"
    MINUSCULES = "abcdefghijklmnopqrstuvwxyz"

    @staticmethod
    def init_reactions(autoriser_accent, autoriser_maj, autoriser_speciaux, nombre):
        """Renvoie une liste contenant les différents
        caractères à écrire le plus vite possible ainsi que leur temps d'apparition en ms    

        Args:
            autoriser_accent (boolean): Est-ce que les suites de caractères peuvent contenir des accents ?
            autoriser_maj (boolean): Est-ce que les suites de caractères peuvent contenir des majuscules ?
            autoriser_speciaux (boolean): Est-ce que les suites de caractères peuvent contenir des caractères spéciaux ?
            nombre (int): Le nombre de réactions à générer

        Returns: 
            list: Liste de tuples contenant le temps d'apparition et la suite de caractères à écrire

        Exemple d'output : [(500, "h"), (1900, "zoi"), (4100, "vx"), (700, "lOi")]
        """
        # [*str] transforme str en une liste de chaine de caractère
        alphabet_maj = [*Reaction.MAJUSCULES]
        accents = [*(Reaction.ACCENTS * 2)] # x2 pour qu'ils y soient plus souvent
        speciaux = [*(Reaction.SPECIAUX * 2)] # x2 pour qu'ils y soient plus souvent

        caracteres_possible = [*Reaction.MINUSCULES]

        if autoriser_accent:
            caracteres_possible.extend(accents)
        if autoriser_maj:
            caracteres_possible.extend(alphabet_maj)
        if autoriser_speciaux:
            caracteres_possible.extend(speciaux)

        liste = []

        for i in range(nombre):
            # entre 1,5 secondes et 7 secondes
            temps_aleatoire = random.randint(1500, 7000)

            # composition de la chaine aléatoire
            longueur = random.randint(2, 5)
            
            chaine_aleatoire = ""
            for _ in range(longueur):
                caractere_aleatoire = random.choice(caracteres_possible)
                chaine_aleatoire += caractere_aleatoire

            # ajoute la réaction
            liste.append((temps_aleatoire, chaine_aleatoire))

        Reaction.reactions = liste
    
    @staticmethod
    def lancer_reaction(self, index, api):
        """Lance la réaction à l'index donné

        Args:
            index (int): L'index de la réaction à lancer
            api (Api): L'API pour communiquer avec le site
        """
        # Récupère la réaction à l'index donné sous forme de tuple (temps, chaine)
        reaction = Reaction.reactions[index]

        # Attend le temps donné 
        sleep(reaction[0] / 1000) 

        # Envoie la réaction à la page web
        api.call_js_function("afficherReaction", f'"{reaction[1]}"')

    @staticmethod
    def calculer_score_reaction(data):
        """Calcule le score de l'exercice 'Réaction' à partir des données de l'utilisateur

        Args:
            data (list): Les données de l'utilisateur : 
                         Une liste au format [[reaction, temps], [reaction, temps], [reaction, temps], ...]
        """
        score = 0
        temps_moyen_difficulte = 0
        temps_moyen_total = 0

        for reaction in data:
            temps = reaction[1]
            chaine = reaction[0]

            # On regarde la difficulté de la réaction
            difficulte = 1
            if any(c.isupper() for c in chaine):
                difficulte += 1.5
            if any(c in Reaction.ACCENTS for c in chaine):
                difficulte += 3
            if any(c in Reaction.SPECIAUX for c in chaine):
                difficulte += 5
            if len(chaine) > 3:
                difficulte += 4

            # Calcul du score en fonction du temps mis pour écrire la réaction
            # et l'ajoute au score total
            if temps < 500:
                score += 8 * difficulte
            elif temps < 1000:
                score += 6 * difficulte
            elif temps < 2000:
                score += 3 * difficulte
            elif temps < 3000:
                score += 2 * difficulte
            elif temps < 4000:
                score += 0.75 * difficulte
            elif temps < 5000:
                score += 0.5 * difficulte
            else:
                score += 0.15 * difficulte

            # Calcul du temps moyen pour écrire une réaction (en prenant en compte la difficulté)
            temps_moyen_difficulte += temps / difficulte

        # Calcul du temps moyen total
        temps_moyen_total = sum(reaction[1] for reaction in data) / len(data)

        # Arrondi le score
        return { "score": round(score), "temps_moyen_difficulte": round(temps_moyen_difficulte / len(data)), "temps_moyen_total": round(temps_moyen_total) }