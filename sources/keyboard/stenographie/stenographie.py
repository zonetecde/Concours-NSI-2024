import os
import random
import re
import urllib.request

import requests
import sys
import tarfile

class Stenographie:
    def get_audios_with_texts(self):
        """Récupère des audios et leur retranscription depuis voxforge.org

        Returns:
            list de tuple: Liste de tuple contenant le texte et le chemin d'accès vers l'audio.
        """
        
        # De la page https://www.voxforge.org/home/downloads/speech/french-speech-files?pn=1 
        # à https://www.voxforge.org/home/downloads/speech/french-speech-files?pn=76 (inclus)

        # Prend une page aléatoire entre 1 et 76 au format https://www.voxforge.org/home/downloads/speech/french-speech-files?pn=LE NUMERO DE LA PAGE
        page_url = self.get_random_voxforge_page_url()

        # Récupère le contenu de la page
        html = self.get_html(page_url)

        # Récupère un lien aléatoire parmis tout ceux de la page (voir sur le site comment sont organisés les liens)
        # ex de lien obtenu : https://www.voxforge.org/home/downloads/speech/french-speech-files/benob-20090314-dth2#MprUm_W0agc6Eqk3TBv-nQ
        links = self.get_links_in_voxforge_page(html)

        random_link = random.choice(links) # lien aléatoire

        # De ce lien, récupère le fichier .tgz 
        tgz_download_link = self.get_tgz_download_link(random_link)

        # Télécharge le fichier .tgz dans le dossier audio 
        filepath = self.download_tgz(tgz_download_link)

        # décompresse le fichier .tgz
        # dans le fichier tgz se trouve un autre fichier .tar, il faut aussi le décompresser
        folder_path = self.extract_tgz(filepath, os.path.dirname(filepath))

        # dans le fichier tar se trouve un dossier contenant les audios et un fichier texte avec la retranscription de l'audio
        # les fichiers audios se trouvent dans le dossier wav et les retrancriptions dans le dossier etc/PROMPTS
        # Récupère le texte et le chemin d'accès vers l'audio et les met dans une liste de tuple
        audios = []
        text_file = os.path.join(folder_path, "etc/PROMPTS")

        with open(text_file, "r", encoding="UTF-8") as file:
            for line in file:
                # Le chemin d'accès vers l'audio est entre le début et le premier espace
                data = line.split(" ", maxsplit=1)
                audio_path = os.path.join(os.path.dirname(folder_path), data[0])
                text = data[1].capitalize().replace("\n", "")
                audios.append((text, audio_path))

        # renvoie la liste de tuple (format : [(texte, chemin_audio), (texte, chemin_audio), ...])
        return audios
    
    def get_html(self, url):
        """Télécharge le contenu d'une page web et le retourne sous forme de texte.
        """
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        fp = urllib.request.urlopen(req)
        bytes = fp.read()

        html = bytes.decode("utf8")
        fp.close()

        return html
    
    def get_random_voxforge_page_url(self):
        """Renvoie une page aléatoire de voxforge.org
        Entre 1 et 76
        """
        random_page = random.randint(1, 76)
        return f'https://www.voxforge.org/home/downloads/speech/french-speech-files?pn={random_page}'

    def get_links_in_voxforge_page(self, html):
        """Récupère les liens dans une page de voxforge.org
        """
        # Entre <td class="oddThread"><a href=" et ">
        links = re.findall(r'<td class="oddThread"><a href="(.*?)">', html)
        # Enlève les liens qui amènent vers un profile
        links = list(filter(lambda link: "viewProfile" not in link, links))
        # Ajoute au début des liens la source du site (https://www.voxforge.org/)
        links = [f"https://www.voxforge.org/{link}" for link in links]

        return links

    def get_tgz_download_link(self, url):
        """Récupère le lien de téléchargement du .tgz sur une page voxforge.org

        Args:
            url (str): url de la page (ex: https://www.voxforge.org/home/downloads/speech/french-speech-files/nbara-20160203-pkd#zMNM6jv5nOFCo0Wz1eM_0Q)
        """
        html = self.get_html(url)
        # Le lien se trouve entre /compressed.gif"><a href=" et ">
        link = re.findall(r'/compressed.gif"><a href="(.*?)">', html)[0]
        return link

    def download_tgz(self, url):
        """Télécharge un fichier .tgz depuis une url

        Args:
            url (str): url du fichier .tgz

        Returns:
            (str): Le path vers le fichier téléchargé
        """
        dir = os.path.dirname(os.path.abspath(__file__)) + "/audios/"

        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, allow_redirects=True, headers=headers)
        
        # Nom de fichier aléatoire
        filepath = str(random.randint(0, 999_999)) + ".tgz"

        # Sauvegarde le fichier sur le disque
        open(dir + filepath, 'wb').write(r.content)
        
        return dir + filepath

    def extract_tgz(self, filepath, where):
        """Décompresse un fichier .tgz

        Args:
            path (str): chemin d'accès vers le fichier .tgz

        Returns:
            (str): Le nom du dossier où le contenu a été extrait
        """
        tar = tarfile.open(filepath, 'r')
        folder_name = ""

        for item in tar:
            tar.extract(item, where)
            folder_name = item.name

        return os.path.join(where, os.path.dirname(os.path.dirname(folder_name))) 

# stenographie = Stenographie()
# print(stenographie.get_audios_with_texts())