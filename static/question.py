from static.perso import personnage

class question():
    def __init__(self,attribut,valeur,question):
        self.attribut = attribut
        self.valeur = valeur
        self.question = question
    
    #on pose la question " est ce que la valeur de l'attribut du personnage est égale à la valeur de la question"
    def poser_question(self, personnage):
        valeur_personnage = getattr(personnage, self.attribut)

        # cas partoculier pour a_animal
        if self.valeur == "ANY":
            if valeur_personnage != "Aucun":
                return True
            else:
                return False

        if valeur_personnage == self.valeur:
            return True
        else:
            return False



