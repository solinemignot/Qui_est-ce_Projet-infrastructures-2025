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
                famille=caracteristiques.get("famille")
            )
            personnages.append(perso)
        return personnages

liste_personnages = construire_personnage()


###### QUESTIONS #######
from static.question import question
from static.questions_map import questions_map
def construire_questions():
    questions = []
    for key, (attribut, valeur,qst) in questions_map.items():
        q = question(attribut, valeur, qst)
        questions.append(q)
    return questions

liste_questions = construire_questions()
