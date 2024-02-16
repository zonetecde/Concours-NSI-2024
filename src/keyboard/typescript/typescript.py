from keyboard.typescript.generateur import Generateur


class TypeScript:
    """ Classe TypeScript
    Permet de gérer l'exercice "Type Script"
    """

    @staticmethod
    def get_random_sentence(self, langue):
        """Récupère une phrase aléatoire d'un article wikipedia aléatoire

        Args:
            langue (str): La langue de la phrase

        Returns:
            str: Une phrase aléatoire
        """
        generateur = Generateur(langue)
        return generateur.get_text()

    @staticmethod
    def calculer_score_typescript(self, data):
        """Cette fonction est appelé par le code javascript
        lorsque l'utilisateur a fini l'exercice "Type Script"

        Returns:
            obj: Les différentes données de l'exercice : le temps mis, le nombre d'erreurs et le nombre de caractères total
        """

        temps_mis = data["temps_mis"]
        nb_erreurs = data["nb_erreurs"]
        nb_caracteres = data["nb_caracteres"]

        minutes = temps_mis // 60000
        secondes = int((temps_mis % 60000) / 1000)

        #temps mis string mm:ss without using string containation
        temps_mis_string = str(minutes) + ":" + str(secondes if secondes >= 10 else '0' + str(secondes))
        nb_caracteres_corrects = nb_caracteres - nb_erreurs
        nbre_caractere_minute = nb_caracteres_corrects / (temps_mis / 60000)
        nbre_caractere_seconde = nb_caracteres_corrects / (temps_mis / 1000)
        precision = nb_caracteres_corrects / nb_caracteres
        score = (nbre_caractere_minute * precision)

        return {
            "tempsMisString": temps_mis_string,
            "nbErreurs": nb_erreurs,
            "nbCaracteres": nb_caracteres,
            "vitesse":  round(nbre_caractere_seconde, 2),
            "precision":  round(precision, 2),
            "score":  round(score, 2)
        }