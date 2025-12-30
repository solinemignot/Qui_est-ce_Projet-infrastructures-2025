# On regroupe ici les questions qui sont liées entre elles
# Si l'une des question d'un groupe est oui, alors les autres sont non

QUESTION_GROUPS ={
    "maison": [0, 1, 2, 3],  # Gryffondor, Serpentard, Poufsouffle, Serdaigle
    
    "genre": [4, 5],  # Homme, Femme
    
    "cheveux": [6, 7, 8, 9, 10],  # Noirs, Roux, Blonds, Bruns, Roses

    "animal_type": [14, 15, 16],  # Hibou, Chat, Rat

    "statut": [17, 18], # Professeur, Élève
    
    "sang": [19, 20, 21], # Pur, Mélé, Moldu

    "moralite": [22, 23], # Gentil, Méchant

    "famille": [24, 25, 26, 27], # Potter, Weasley, Black, Malfoy
} 

def get_related_questions(question_index, got_yes=True):
    if not got_yes:
        return []
    
    # Chercher dans quel groupe se trouve cette question
    for group_name, indices in QUESTION_GROUPS.items():
        if question_index in indices:
            return [idx for idx in indices if idx != question_index]
    
    # Si pas dans un groupe, rien à griser automatiquement
    return []