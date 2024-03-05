from difflib import SequenceMatcher
import os
import random
import re
import shutil
import urllib.request

import requests
import sys
import tarfile
import unicodedata

# Permet de ce placer dans le dossier sources
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config import DEBUG

class Stenographie:
    def get_audios_with_texts(self):
        """Récupère des audios et leur retranscription depuis voxforge.org

        Returns:
            list de tuple: Liste de tuple contenant le texte et le chemin d'accès vers l'audio.
        """
        try:
            self.delete_old_audios()
            
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

            to_dir = self.get_static_folder_path()

            with open(text_file, "r", encoding="UTF-8") as file:
                for line in file:
                    # Le chemin d'accès vers l'audio est entre le début et le premier espace
                    data = line.split(" ", maxsplit=1)
                    audio_path = os.path.join(os.path.dirname(folder_path), data[0]).replace("/", "\\").replace("mfc", "wav") + ".wav"
                    text = data[1].capitalize().replace("\n", "")

                    # Vérifie que le fichier audio existe
                    if os.path.isfile(audio_path):
                        # Déplace le fichier audio dans le dossier static/audios/stenographie pour pouvoir l'utiliser dans le site
                        # Lui ajoute un nom aléatoire pour éviter les doublons
                        random_name = ""
                        while os.path.isfile(to_dir + random_name) or random_name == "":
                            random_name = str(random.randint(0, 999_999)) + ".wav"

                        os.rename(audio_path, to_dir + random_name)

                        text = text.strip()

                        audios.append((text, f"/audio/stenographie/{random_name}"))

            # Supprime le dossier tgz temporaire
            os.remove(filepath)
            # Supprime le dossier d'extraction temporaire
            shutil.rmtree(folder_path) 

            # renvoie la liste de tuple (format : [(texte, chemin_audio), (texte, chemin_audio), ...])
            return audios
        except Exception as e:
            print('stenographie: Erreur à la ligne {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            print(e)
            return []
    
    def delete_old_audios(self):
        """Supprime les anciens fichiers audios
        """
        # Supprime les ancien fichiers audios
        dir = self.get_static_folder_path()

        # Si le dossier n'existe pas, le crée
        if not os.path.exists(dir):
            os.makedirs(dir)
        
        for file in os.listdir(dir):
            try:
                os.remove(dir + file)
            except PermissionError:
                pass

    def get_static_folder_path(self):
        """Renvoie le chemin d'accès vers le dossier static du site
        """
        if not DEBUG:
            return os.path.dirname(os.path.dirname(os.path.dirname(__file__))).replace("\\", "/") + "/web/build/audio/stenographie/"
        else:
            return os.path.dirname(os.path.dirname(os.path.dirname(__file__))).replace("\\", "/") + "/web/static/audio/stenographie/"

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
    
    def verifier_phrase(self, phrase_original, phrase_tapee, majs, orthographe, ponctuations):
        """Vérifie si la réponse donnée par l'utilisateur est correcte

        Args:
            phrase_original (str): La phrase originale
            phrase_tapee (str): La phrase tapée par l'utilisateur
            majs (bool): True si les majuscules sont prises en compte, False sinon
            orthographe (bool): True si l'orthographe est prise en compte, False sinon
            ponctuations (bool): True si les ponctuations sont prises en compte, False sinon

        Returns:
            bool: True si la réponse est correcte, False sinon
        """
        if not majs:
            phrase_original = phrase_original.lower()
            phrase_tapee = phrase_tapee.lower()

        if not orthographe:
            # Enlève les accents
            phrase_original = self.enlever_accent(phrase_original)
            phrase_tapee = self.enlever_accent(phrase_tapee)

            # Enlève les `s` à la fin des mots 
            phrase_original = re.sub(r'\bs\b', '', phrase_original)
            phrase_tapee = re.sub(r'\bs\b', '', phrase_tapee)

            # Corrige les fautes de terminaisons
            phrase_original = self.enlever_terminaisons(phrase_original)
            phrase_tapee = self.enlever_terminaisons(phrase_tapee)
        
        if not ponctuations:
            phrase_original = re.sub(r'[^\w\s]', '', phrase_original)
            phrase_tapee = re.sub(r'[^\w\s]', '', phrase_tapee)

        # Enlève les espaces
        phrase_original = phrase_original.strip().replace(" ", "-")
        phrase_tapee = phrase_tapee.strip().replace(" ", "-")

        # Vérifie si les deux phrases sont les mêmes et calcul un pourcentage de ressemblance
        return phrase_original == phrase_tapee, self.similarity(phrase_original, phrase_tapee)
    
    def similarity(self, a, b):
        """Calcul le pourcentage de ressemblance entre deux phrases

        Args:
            a (str): La première phrase
            b (str): La deuxième phrase

        Returns:
            float: Le pourcentage de ressemblance
        """
        return round(SequenceMatcher(None, a, b).ratio() * 100, 2)

    def enlever_accent(self, phrase):
        """Enlève les accents d'une phrase

        Args:
            phrase (str): La phrase

        Returns:
            str: La phrase sans accents
        """
        return ''.join(c for c in unicodedata.normalize('NFD', phrase)
                  if unicodedata.category(c) != 'Mn')

    def enlever_terminaisons(self, phrase):
        """Met toutes les terminaisons `ées`, `és`, `ée`, `er`, `ai`, `aient`, `ais`, `ait` en `er`
        et met toutes les termisaisons `is`, `it`, `ie`, `ient` en `i`

        Args:
            phrase (str): La phrase

        Returns:
            str: La phrase modifiée
        """
        phrase = re.sub(r'\b(?:ées|és|ée|ai|aient|ais|ait)\b', 'er', phrase)
        phrase = re.sub(r'\b(?:is|it|ie|ient)\b', 'i', phrase)
        return phrase

# stenographie = Stenographie()
# print(stenographie.get_audios_with_texts())