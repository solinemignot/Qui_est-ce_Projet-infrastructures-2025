13/11 - Soline : 

Je viens de créer le git, et j'ai créer plus ou moins l'architecture du projet : 
- static folder : là il y a la description des personnages (personnages.json) et on mettra les photos des persos (peut-être mais même pas sûr)
- templates : c'est là qu'il y a les codes des pages du site. 

J'ai commencé avec la page d'accueil. Je sais que pour l'instant c'est assez moche mdr mais c'était pour voir comment ça marchait de mettre une photo (le Harry Potter) et de faire un bouton sur lequel on peut cliquer. Le bouton renvoie à la page jeu.html qui sera le gros du projet. 

Pour ouvrir le serveur et voir les pages, il faut juste run : 

'flask run --debug' 

dans le terminal et ça à l'air de faire l'affaire.



\\ update leena 
j'ai ajouté les images en local, je pense qu'on peut debattre des personnes (pa assez de filles ou whatever, j'en ai ajouter d'autres dans le dossier qui sont pas dans la grille (ou sinon on peut juste étendre la grille pour le rendre plus dur))

liste déroulante de questions, mettre en grisé les perso qui ne répondent pas aux caractères et choisir en mode random un perso au début
⦁	J'ai ajouté 4 filles pour la parité et ça nous fait 24 persos comme le vrai qui est-ce, j'ai ajouté leurs caractéristiques sur le dictionnaire caractéristique
⦁	j'ai mis une liste déroulant pour les questions plutôt que une entrée manuelle sinon c'est trop dur à gérer 
⦁	j'ai fait une fonction qui pour chaque question séléctionnée va griser les persos qui ne respectent pas la condition qui est a priori respectée par le perso choisi de manière random
⦁	pour ajouter/enlever des questions : faut modifier les fichiers questions_map et dans jeu.html

Améliorations possibles:
⦁	J'ai pas gérer l'initialisation: sur l'entrée on peut faire reprendre la partie ou en commencer une nouvelle 
⦁	gérer la fin de jeu, quand il reste plus que un perso j'ai pas du tout gérer la fin de jeu 
⦁	peut être afficher à l'écran qqch (au moins la réponse oui/non à chaque question)
⦁	bouton retour à l'accueil ou proposer une nouvelle partie 
⦁	extension: en faire un jeu dans les deux sens: laisser la possibilité au joueur de choisir un perso et on choisi des question np.random pour que "l'IA" derrière suppr des perso en même temps et comme ça si l'ia trouve le perso avant le joueur , il a perdu
⦁	améliorer en général l'esthétique

25/11 : avancées Tea

J'ai géré la fin de partie : j'ai ajouté une possibilité de deviner le personnage directement parmis les personnages possibles restants. Une fois la partie terminée, possibilité de rejouer une partie.
J'ai aussi ajouté un bouton retour à l'accueil

J'ai également ajouté l'étape avant le commencement du jeu où l'utilisateur choisi un personnage. 
Ce personnage est stocké dans session["secret_joueur"]. Pour l'instant on en fait rien, ce sera à utiliser lorsqu'on implémente l'IA qui doit deviner le perso du joueur

30/11 : avancées Tania

J'ai modifié la structure du code pour faire de la POO. Ca facilite la manipulation. Maintenant si on veut ajouter des perso ou des questions on modifie seulement les fichiers textes et le code s'adapte. 

Le jeu ne se resetait pas quand on faisait une nouvelle partie j'ai corrigé 
j'ai ajouté quelques animations : le choixpeau et reponse oui/non a chaque question posé 


21/12 : avancées Tania 

j'ai modifié la partie solo + duo pour que le joueur grise lui meme les cartes.
- idée d'amelioration : quand on repond faux aux questions de l'ordi des fois il elimine tout le monde. A ce moment la ce serait bien d'avoir un message qui s'affiche en mode "desolée aucun personnage ne correpond à ta reponse"
- aussi ajouter des indications de jeu pour guider l'utilisateur 