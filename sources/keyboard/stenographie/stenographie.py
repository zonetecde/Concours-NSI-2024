import random
import urllib3


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

        # De ce lien, récupère le fichier .tgz (voir sur le site oú il est situé)
        tgz_download_link = self.get_tgz_download_link(random_link)

        # Télécharge le fichier .tgz dans le dossier audio 
        self.download_tgz(tgz_download_link)

        # décompresse le fichier .tgz
        # dans le fichier tgz se trouve un autre fichier .tar, il faut aussi le décompresser
        self.decompress_tgz("audio/le_fichier.tgz")
        self.decompress_tar("audio/le_dossier_tgz_decompresse/le_fichier.tar")

        # dans le fichier tar se trouve un dossier contenant les audios et un fichier texte avec la retranscription de l'audio
        # les fichiers audios se trouvent dans le dossier wav et les retrancriptions dans le dossier etc/PROMPTS
        # Récupère le texte et le chemin d'accès vers l'audio et les met dans une liste de tuple

        # renvoie la liste de tuple (format : [(texte, chemin_audio), (texte, chemin_audio), ...])
    
    def get_html(self, url):
        """Télécharge le contenu d'une page web et le retourne sous forme de texte.
        """
        fp = urllib3.request.urlopen(url)
        bytes = fp.read()

        html = bytes.decode("utf8")
        fp.close()

        return html
    
    def get_random_voxforge_page_url(self):
        """Renvoie une page aléatoire de voxforge.org
        Entre 1 et 76
        """
        pass

    def get_links_in_voxforge_page(self, html):
        """Récupère les liens dans une page de voxforge.org

        """
        pass

    def get_tgz_download_link(self, url):
        """Récupère le lien de téléchargement du .tgz sur une page voxforge.org

        Args:
            url (str): url de la page (ex: https://www.voxforge.org/home/downloads/speech/french-speech-files/nbara-20160203-pkd#zMNM6jv5nOFCo0Wz1eM_0Q)
        """
        html = self.get_html(url)
        pass

    def download_tgz(self, url):
        """Télécharge un fichier .tgz depuis une url

        Args:
            url (str): url du fichier .tgz
        """
        pass

    def decompress_tgz(self, path):
        """Décompresse un fichier .tgz

        Args:
            path (str): chemin d'accès vers le fichier .tgz
        """
        pass

    def decompress_tar(self, path):
        """Décompresse un fichier .tar

        Args:
            path (str): chemin d'accès vers le fichier .tar
        """
        pass


stenographie = Stenographie()
print(stenographie.get_audios_with_texts())