import requests
import urllib.request

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
    
    def get_paragraph(self):
        pass