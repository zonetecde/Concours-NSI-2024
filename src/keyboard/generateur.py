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
    
    def get_paragraph_h1(self):
        html = self.get_random_article()
        coo = []
        stock = []
        for text in range(len(html)):
            if html[text] == "<" and html[text+1] == "p":
                stock.append(text + 2)
            if html[text] == "p" and html[text+1] == ">":
                coo = [stock.pop(-1), text-1]
                return html[coo[0]: coo[1]]
    
    def get_paragraph_a(self):
        paragraph = self.get_paragraph_h1()
        coo = []
        stock = []
        for depart, arrivee in paragraph:
            for text in range(len(paragraph)):
                if paragraph[text] == "<" and paragraph[text+1] == "a":
                    stock.append(text)
                if paragraph[text] == "a" and paragraph[text+1] == ">":
                    coo.append(stock.pop(-1), text+1)
        return paragraph, coo
    
    def get_phonetique(self):
        paragraph, coo_a = self.get_paragraph_a()
        coo = []
        stock = []
        for depart, arrivee in paragraph:
            for text in range(len(paragraph)):
                if paragraph[text] == "/":
                    stock.append(text)
                if paragraph[text] == "/":
                    coo.append(stock.pop(-1), text+1)
        return paragraph, coo_a, coo

    def pop_paragraph(self):
        paragraph, coo_a, coo_phon = self.get_phonetique()
        paragraph = paragraph[0:]
