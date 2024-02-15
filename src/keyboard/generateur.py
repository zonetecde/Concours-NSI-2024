import requests
import urllib.request
import re
import random

class Generateur:
    def __init__(self, langue = "fr") -> None:
        self.langue = "fr"
        self.wikipedia_url = "https://" + self.langue +".wikipedia.org/wiki/Special:Random"

    def get_random_article(self):
        fp = urllib.request.urlopen(self.wikipedia_url)
        mybytes = fp.read()

        html = mybytes.decode("utf8")
        fp.close()


        # écrire la variable content dans un fichier texte
        # with open("content.txt", "w", encoding="utf8") as f:
        #     f.write(mystr)

        return html
    
    def get_paragraph_h1(self):
        html = self.get_random_article()
        paragraphes = re.findall(r'<p>(.*?)</p>', html, re.DOTALL)
        if paragraphes:
            return random.choice(paragraphes)
        else:
            return "Paragraphe non trouvé"
        
    def clean_text(self):
        text = self.get_paragraph_h1()
        clean_text = re.sub(r'<.*?>', '', text)
        clean_text = re.sub(r'\(.*?\)', '', clean_text)
        clean_text = re.sub(r'\[.*?\]', '', clean_text)
        return clean_text.strip()
