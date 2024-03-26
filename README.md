# Windows et Linux

Pour commencer à utiliser Key Mouse Training, cloner le dépôt GitHub à l'aide de la commande suivante :

```
gh repo clone zonetecde/Concours-NSI-2024
```

Ensuite, ouvrir le dossier du projet dans un terminal, et installer les dépendances à l'aide de la commande suivante :

```
pip install -r requirements.txt
```

Enfin, lancer le programme à l'aide de la commande suivante :

```
python sources/main.py
```

# Debug

Pour modifier le code, il est nécessaire d'installer Node.js et npm, puis d'installer les dépendances à l'aide de la commande suivante :

```
cd sources/web
npm install
```

Ensuite, pour lancer le serveur de développement, utiliser la commande suivante :

```
npm run dev
```

Enfin, changer dans le fichier `sources/config.py` la variable `DEBUG` à `True`, et lancer le programme à l'aide de la commande suivante :

```
python sources/main.py
```

# Production

Pour lancer le programme en production après avoir modifié le code, utiliser la commande suivante :

```
cd sources/web
npm run build
```

Ensuite, changer dans le fichier `sources/config.py` la variable `DEBUG` à `False`, et lancer le programme à l'aide de la commande suivante :

```
python sources/main.py
```
