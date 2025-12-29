# Qui est-ce ? (Harry Potter)

Projet réalisé dans le cadre du cours Infrastructures et Systèmes Logiciels par Téa TOSCAN DU PLANTIER, Ndoumbé BAYO, Tania ADMANE, Soline MIGNOT et Leena BOYINA.
Il s’agit d’une adaptation du jeu "Qui est-ce" ? développée en Python / Flask avec une interface web interactive sur le thème de Harry Potter.

## Présentation du projet
L’utilisateur a le choix entre deux modes:


**Mode solo**  
Le joueur pose des questions pour deviner le personnage choisi aléatoirement par l’ordinateur.

**Mode humain contre ordi**

Le joueur affronte l’ordinateur.
Chaque joueur choisit un personnage, pose des questions et élimine progressivement les personnages impossibles.

*Deux niveaux de difficulté sont disponibles en mode duo* :
- Facile : questions de l’ordinateur choisies aléatoirement
- Difficile : questions optimisées pour réduire l’espace de recherche

## Logique du jeu

Chaque personnage est défini par un ensemble de caractéristiques booléennes (par exemple : cheveux clairs, porte des lunettes, est un eleve, etc.)

Lorsqu’une question est posée, elle renvoie une réponse Oui / Non pour un personnage donné. Les personnages incompatibles sont éliminés. L’ensemble des personnages restants réduit petit à petit


## Lancer le projet

- Installer les dépendances
- Run app.py
- Accéder à l’application à partir du lien donné dans le terminal
