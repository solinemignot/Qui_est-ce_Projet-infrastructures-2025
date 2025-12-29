###### PERSONNAGES #######

#on construit les personnages à partir des caracteristiques
from static.perso_caract import caracteristiques_personnages
from static.perso import personnage

def construire_personnage():
        personnages = []
        for nom, caracteristiques in caracteristiques_personnages.items():
            perso = personnage(
                nom=nom,
                description=caracteristiques.get("description"),
                maison=caracteristiques.get("maison"),
                genre=caracteristiques.get("genre"),
                cheveux=caracteristiques.get("cheveux"),
                lunettes=caracteristiques.get("lunettes"),
                baguette_particuliere=caracteristiques.get("baguette_particuliere"),
                animal=caracteristiques.get("animal"),
                professeur=caracteristiques.get("professeur"),
                sang=caracteristiques.get("sang"),
                role=caracteristiques.get("role"),
                trait_distinctif=caracteristiques.get("trait_distinctif"),
                moralite=caracteristiques.get("moralite"),
                famille=caracteristiques.get("famille"),
                survit_fin=caracteristiques.get("survit_fin"),
                meurt_dans_saga=caracteristiques.get("meurt_dans_saga"),
                bataille_finale=caracteristiques.get("bataille_finale"),
                role_majeur=caracteristiques.get("role_majeur"),
                figure_autorite=caracteristiques.get("figure_autorite"),
                evolution_perception=caracteristiques.get("evolution_perception"),
                camp_ambigu=caracteristiques.get("camp_ambigu"),
                famille_importante=caracteristiques.get("famille_importante"),
                proche_harry=caracteristiques.get("proche_harry"),
                mort_marquante=caracteristiques.get("mort_marquante"),
                pouvoir_special=caracteristiques.get("pouvoir_special"),
                present_longtemps=caracteristiques.get("present_longtemps")
            )
            personnages.append(perso)
        return personnages

liste_personnages = construire_personnage()


###### QUESTIONS #######
from static.question import question
from static.questions_map import questions_map_facile, questions_map_difficile
def construire_liste_questions(difficulty="easy"):
    if difficulty == "easy":
        source = questions_map_facile
    else:
        source = questions_map_difficile

    return [
        question(attribut, valeur, texte)
        for (attribut, valeur, texte) in source.values()
    ]

liste_questions = construire_liste_questions()
