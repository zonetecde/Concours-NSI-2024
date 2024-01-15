import requests

class Generateur:
    def __init__(self, langue = "fr") -> None:
        self.langue = "fr"
        self.wikipedia_url = "https://" + self.langue +".wikipedia.org/wiki/Special:Random"

    def getRandomArticle(self):
        r = requests.get(self.wikipedia_url)
       
        print( r.content)
        return  r.content