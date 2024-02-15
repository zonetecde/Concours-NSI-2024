import html
import urllib.request
import re

class Generateur:
    MIN_LENGTH = 200 # Longueur minimale d'une phrase aléatoire

    def __init__(self, langue = "fr") -> None:
        """Initialise le générateur de texte aléatoire

        Args:
            langue (str, optional): La langue du texte. Defaults to "fr".
        """
        self.langue = "fr"
        self.wikipedia_url = "https://" + self.langue +".wikipedia.org/wiki/Special:Random"

    def get_random_article(self):
        """Récupère le code HTML d'un article wikipedia aléatoire

        Returns:
            str: Le code HTML de l'article
        """
        fp = urllib.request.urlopen(self.wikipedia_url)
        mybytes = fp.read()

        html = mybytes.decode("utf8")
        fp.close()

        return html
    
    def get_article(self, html):
        """Récupère le texte de l'article wikipedia

        Args:
            html (str): Le code HTML de l'article

        Returns:
            str: Le texte de l'article
        """
        # Trouve tous les paragraphes de l'article
        paragraphes = re.findall(r'<p>(.*?)</p>', html, re.DOTALL)

        # Clean les paragraphes
        paragraphes = [self.clean_text(p) for p in paragraphes]

        # Les paragraphes sont concaténés pour former un seul texte
        text = " ".join(paragraphes)

        return text

        
    def get_random_sentences(self, paragraphe: str):
        """Récupère une ou des phrases aléatoires d'un paragraphe
        pour avoir un texte d'une certaine longueur

        Args:
            paragraphe (str): Le paragraphe à analyser

        Returns:
            str: Une phrase aléatoire
        """
        text = ""
        
        phrases = paragraphe.split(".")

        i = 0
        while len(text) < self.MIN_LENGTH and i < len(phrases):
            text = phrases[i]
            i += 1
            
        return text.strip()
        
    def clean_text(self, text):
        """Applique plusieurs nettoyages sur le texte afin de le rendre plus lisible

        Args:
            text (str): Le texte à nettoyer

        Returns:
            str: Le texte nettoyé
        """
        # Supprime les balises seul du texte (ex: <b>, <br>, <hr>, <img>)
        clean_text = re.sub(r'<.*?>', '', text)
        
        # Supprime tous les contenus entre parenthèses du texte (ex: le phonétique)
        clean_text = re.sub(r'\(.*?\)', '', clean_text)
        
        # Supprime tous les contenus entre crochets du texte (ex: le phonétique)
        clean_text = re.sub(r'\[.*?\]', '', clean_text)

        # Supprime les espaces multiples
        clean_text = re.sub(r'\s+', ' ', clean_text)

        # Supprime les espaces entre les mots et les ponctuations
        clean_text = re.sub(r'\s([,;.:!?])', r'\1', clean_text)

        # Supprime les caractères spéciaux HTML
        clean_text = html.unescape(clean_text)

        # Remplace les guillemets français par des guillemets anglais
        clean_text = clean_text.replace("« ", "\"").replace(" »", "\"")      

        # Remplace les apostrophes françaises par des apostrophes anglaises
        clean_text = clean_text.replace("’", "'")  
 
        return clean_text.strip()
    
    def get_text(self):
        """Récupère une phrase aléatoire d'un article wikipedia aléatoire

        Returns:
            str: Une phrase aléatoire d'une certaine longueur
        """
        html = self.get_random_article()

        article = self.get_article(html)

        random_sentence = self.get_random_sentences(article)

        if random_sentence == "" or len(random_sentence) < self.MIN_LENGTH:
            return self.get_text()
       
        return random_sentence
