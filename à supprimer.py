
"""

> PRÉSENTATION GÉNÉRALE :
Pouvez-vous présenter en quelques mots votre projet ?
Comment est né ce projet ? Quelle était la problématique de départ ? 
Quels sont les objectifs ? À quels besoins répondez-vous ?

Notre projet KMT, Key Mouse Training, est né à la suite d'une problématique quotidienne rencontrée par notre ami Matthieu, atteint d'un handicap moteur. En effet, il lui est difficile de se servir d'un clavier et d'une souris, bien que cela soit nécessaire pour l'utilisation de son ordinateur en classe, étant donné qu'il souffre aussi de dysgraphie.

Ainsi est apparue l'idée de créer un logiciel qui permettrait d'apprendre la dactylographie, mais aussi de se servir de la souris. KMT regroupe donc un ensemble d'exercices et de mini-jeux éducatifs pour un apprentissage efficace et ludique de l'utilisation du clavier et de la souris. Chaque exercice possède plusieurs niveaux de difficulté, permettant de s'adapter à tous les utilisateurs et favorisant une progression constante.

Key Mouse Training a été développé en Python, avec l'utilisation de la librairie pywebview pour l'interface graphique en Svelte, un framework JavaScript. Le site est hébergé localement et communique avec le programme principal via une API, combinant ainsi les avantages de Python et de JavaScript pour un logiciel complet et performant. De plus, KMT exploite des bases de données pour stocker les différentes données textuelles utilisées dans les exercices.

Le projet tire également parti d'informations provenant d'Internet, telles que Wikipedia pour récupérer des phrases utilisées dans les exercices de dactylographie, ou encore VoxForge pour récupérer des enregistrements de voix pour les exercices de sténographie. De plus, KMT propose différents langages pour certains exercices, permettant une utilisation internationale.

La partie relative à la souris de KMT a été développée en utilisant PyGame, ce qui a permis de trouver un juste équilibre entre la simplicité d'utilisation et la complexité des exercices. En effet, la souris est un outil simple, mais il est difficile de créer des exercices à la fois ludiques et éducatifs. Ainsi, nous avons pu concevoir des exercices visant à améliorer la précision, la rapidité et la coordination des mouvements de la souris.





> ORGANISATION DU TRAVAIL :
Pouvez-vous présenter chaque membre de l’équipe et préciser son rôle dans ce projet ?
Comment avez-vous réparti les tâches et pourquoi ?
Combien de temps avez-vous passé sur le projet ? Avez-vous travaillé en dehors de l’établissement scolaire ?
Quels sont les outils et/ou les logiciels utilisés pour la communication et le partage du code ?
Vous veillerez au bon équilibre des différentes tâches dans le groupe. Chaque membre de l’équipe doit impérativement réaliser un aspect technique du projet (hors design, gestion de projet).



Penelope WELFRINGER-LAPAQUE a été en charge du Python de la partie clavier, ainsi que de l'exploitation de la base de données. Ainsi, son travail a permis au logiciel d'utiliser les ressources d'internet et de vérifier les réponses des utilisateurs, ainsi que de générer les différentes données des exercices en fonction de la difficulté choisie par l'utilisateur. Ce rôle lui a été attribué pour sa maîtrise de la programmation en Python et de la gestion des bases de données.

Rayane STASZEWSKI a été en charge de l'interface utilisateur en Web, plus précisément avec le framework Svelte dont il est très familier. Il a aussi fait le lien entre JavaScript et Python pour la communication entre les exercices relatifs au clavier. Ainsi, son travail a permis de créer une interface graphique intuitive et agréable à utiliser pour les exercices au clavier. Ce rôle lui a été attribué pour sa maîtrise du Web et de la création d'interfaces graphiques.

Mathieu BUANNIC a réalisé les exercices mélangeant la souris et le clavier en Web et Python. Son expérience personnelle lui a donné plus de recul sur les différentes problématiques à aborder pour les exercices, et nous a donc été de fort utile pour la conception de ces derniers.

Nous avons commencé par définir les fonctionnalités que nous souhaitions implémenter dans le logiciel, ainsi que les différents exercices que à proposer dans chaque partie, puis nous avons réparti les tâches en fonction des compétences de chacun. Nous avons ensuite commencé à travailler sur le projet, en utilisant la plateforme Discord pour la communication et l'organisation du travail et GitHub pour partager notre code. 

Cela fait, Rayane a créé un "template" en Svelte pour l'interface graphique, et Penelope a commencé à travailler sur le back-end des exercices claviers. Mathieu a commencé à travailler sur ses exercices mélangeant souris et clavier, et enfin Lilian et Esteban sur leurs exercices de souris. Cette disposure nous a permis de travailler en parallèle sur le projet, et de gagner du temps. 

Nous avons tous travaillé sur le projet pendant environ 3 mois, en dehors de l'établissement scolaire, en utilisant principalement nos ordinateurs personnels. Nous avons également eu l'occasion de travailler sur le projet pendant les vacances scolaires, ce qui nous a permis de consacrer plus de temps au projet. 

LES ÉTAPES DU PROJET :
Présenter les différentes étapes du projet (de l’idée jusqu’à la finalisation du projet)

Réunis au CDI, nous avons commencé à explorer différentes idées. Parmis elle, un simulateur de physique, un automate cellulaire, et un logiciel permettant l'apprentissage de la dactylographie et l'aide à l'utilisateur du clavier. C'est cette dernière idée qui a retenu notre attention, car elle répondait à un besoin réel et nous permettait de mettre en pratique nos compétences en programmation. Puis, pour le rendre plus complet, Esteban et Lilian ont eu l'idée d'ajouter des exercices pour la souris, afin de rendre le logiciel plus complet et de répondre à un besoin plus large.

Chacun savait ce qu'il avait à faire, et nous avons commencé à travailler sur le projet. Après avoir fini une fonctionnalité ou un exercice, nous le faisions tester par les autres membres du groupe, afin d'avoir leur ressenti et de corriger les éventuels bugs. Nous avons également fait tester notre logiciel à Matthieu, pour avoir un retour d'expérience d'une personne en situation de handicap.


> OUVERTURE :
Quelles sont les nouvelles fonctionnalités à moyen terme ? Avez-vous des idées d’amélioration de votre projet ?
Pourriez-vous apporter une analyse critique de votre projet ? Si c’était à refaire, que changeriez-vous dans votre organisation, les fonctionnalités du projet et les choix techniques ?
Quelles compétences/appétences/connaissances avez-vous développé grâce à ce concours ?
En quoi votre projet favorise-t-il l’inclusion ?

À moyen terme, nous aimerions ajouter de nouveaux exercices pour la souris, ainsi que pour ceux mélangeant les deux. Nous aimerions également ajouter un système de progression, qui permettrait à l'utilisateur de suivre sa progression dans les différents exercices, et de voir ses points faibles et ses points forts en détail. Nous aimerions également ajouter un système de classement, qui permettrait à l'utilisateur de se comparer aux autres utilisateurs, et de voir où il se situe par rapport à eux. Ce dernier point n'étais malheursement pas possible car en dehors du cadre du concours, et l'utilisation d'un serveur de stockage distant n'était donc pas possible. Enfin, nous aurions aimé supporter plus de langues, pour toucher un public plus large.	

Notre projet, bien que performant, n'est pas parfait. En effet, certains exercices se rapportent plus à des jeux qu'à des exercices éducatifs, et nous aimerions les retravailler pour les rendre plus éducatifs. Nous aurions également aimé partager la même interface graphique pour les exercices de souris et de clavier, mais cela n'était pas possible à cause de la complexité des exercices de souris, et la nécessité d'apprendre un tout nouveau langage pour les réaliser.

Ils nous aient aussi déja arrivé de changer complètement une codebase à cause de problèmes de performances, ou de bugs. Si c'était à refaire, nous aurions aimé mieux réfléchir à la structure de notre code avant d'y plonger. Nous aurions également aimé mieux réfléchir à la conception de nos exercices, pour les rendre plus éducatifs et plus adaptés à notre public cible. Enfin, nous aurions aimé mieux réfléchir à l'organisation de notre projet, pour mieux répartir les tâches et mieux communiquer entre nous; certains malentendus ont pu survenir, et nous aurions aimé les éviter.

Grâce à ce concours, nous avons développé de nombreuses compétences, que ce soit en programmation, en gestion de projet, ou en communication. Plus particulièrement, nous avons appris à utiliser SQLite avec Python, à utiliser GitHub pour partager notre code, à apprendre pour Matthieu le framework Svelte.
 Nous avons également appris à travailler en équipe, à partager nos idées et à les mettre en commun pour créer un logiciel complet et performant. Nous avons également appris à travailler en dehors de l'établissement scolaire, à gérer notre temps en s'imposant des dead-lines et à nous organiser pour mener à bien notre projet. 

Notre projet favorise l'inclusion, car il permet aux personnes débutante, intermédiaire ou atteint de handicap de s'entraîner à l'utilisation du clavier et de la souris, et de progresser à leur rythme. De plus, il est disponible en plusieurs langues, ce qui permet à des personnes du monde entier de l'utiliser.


DOCUMEBTATION TECHNIQUE :
# Windows et Linux

Pour commencer à utiliser Key Mouse Training, cloner le dépôt GitHub à l'aide de la commande suivante :

```
gh repo clone zonetecde/Concours-NSI-2023
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

"""