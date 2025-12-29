questions_map_facile = {
    # Maison
    "maison_gryffondor": ("maison", "Gryffondor", "Est-ce que la maison est Gryffondor ?"),
    "maison_serpentard": ("maison", "Serpentard", "Est-ce que la maison est Serpentard ?"),
    "maison_poufsouffle": ("maison", "Poufsouffle", "Est-ce que la maison est Poufsouffle ?"),
    "maison_serdaigle": ("maison", "Serdaigle", "Est-ce que la maison est Serdaigle ?"),

    # Genre
    "genre_h": ("genre", "H", "Est-ce que le personnage est un homme ?"),
    "genre_f": ("genre", "F", "Est-ce que le personnage est une femme ?"),

    # Cheveux
    "cheveux_noirs": ("cheveux", "Noirs", "Est-ce que le personnage a les cheveux noirs ?"),
    "cheveux_roux": ("cheveux", "Roux", "Est-ce que le personnage a les cheveux roux ?"),
    "cheveux_blonds": ("cheveux", "Blonds", "Est-ce que le personnage a les cheveux blonds ?"),
    "cheveux_bruns": ("cheveux", "Bruns", "Est-ce que le personnage a les cheveux bruns ?"),
    "cheveux_roses": ("cheveux", "Roses", "Est-ce que le personnage a les cheveux roses ?"),

    # Lunettes
    "lunettes": ("lunettes", True, "Est-ce que le personnage porte des lunettes ?"),

    # Baguette particulière
    "baguette_particuliere": (
        "baguette_particuliere",
        True,
        "Est-ce que le personnage a une baguette particulière ?",
    ),

    # Animal (A un animal → True si animal != "Aucun")
    "a_animal": ("animal", "ANY", "Est-ce que le personnage a un animal ?"),
    "animal_hibou": ("animal", "Hibou", "Est-ce que le personnage a un hibou comme animal ?"),
    "animal_chat": ("animal", "Chat", "Est-ce que le personnage a un chat comme animal ?"),
    "animal_rat": ("animal", "Rat", "Est-ce que le personnage a un rat comme animal ?"),

    # Professeur
    "professeur": ("professeur", True, "Est-ce que le personnage est professeur ?"),
    "eleve": ("professeur", False, "Est-ce que le personnage est élève ?"),

    # Sang
    "sang_pur": ("sang", "Pur", "Est-ce que le personnage est de sang pur ?"),
    "sang_mele": ("sang", "Mélé", "Est-ce que le personnage est de sang mêlé ?"),
    "sang_moldu": ("sang", "Moldu", "Est-ce que le personnage est né-moldu ?"),

    # Morale
    "gentil": ("moralite", "Gentil", "Est-ce que le personnage est plutôt gentil ?"),
    "mechant": ("moralite", "Méchant", "Est-ce que le personnage est plutôt méchant ?"),

    # Familles
    "famille_potter": ("famille", "Potter", "Est-ce que le personnage appartient à la famille Potter ?"),
    "famille_weasley": ("famille", "Weasley", "Est-ce que le personnage appartient à la famille Weasley ?"),
    "famille_black": ("famille", "Black", "Est-ce que le personnage appartient à la famille Black ?"),
    "famille_malfoy": ("famille", "Malfoy", "Est-ce que le personnage appartient à la famille Malfoy ?"),

    # Traits distinctifs
    "trait_cicatrice": ("trait_distinctif", "Cicatrice", "Est-ce que le personnage a une cicatrice particulière ?"),
}

questions_map_difficile = {

    # Destin
    "survit_fin": (
        "survit_fin",
        True,
        "Est-ce que le personnage survit jusqu'à la fin de la saga ?"
    ),
    "meurt_saga": (
        "meurt_dans_saga",
        True,
        "Est-ce que le personnage meurt pendant la saga ?"
    ),

    # Bataille finale
    "bataille_finale": (
        "bataille_finale",
        True,
        "Est-ce que le personnage participe à la bataille finale de Poudlard ?"
    ),

    #genre
    "genre_f": ("genre", "F", "Est-ce que le personnage est une femme ?"),

    # Importance
    "role_majeur": (
        "role_majeur",
        True,
        "Est-ce que le personnage a un rôle majeur dans l'histoire ?"
    ),
    "figure_autorite": (
        "figure_autorite",
        True,
        "Est-ce que le personnage est une figure d’autorité ?"
    ),

    # Évolution
    "evolution_perception": (
        "evolution_perception",
        True,
        "Est-ce que l'avis sur ce personnage change au fil de la saga ?"
    ),
    "camp_ambigu": (
        "camp_ambigu",
        True,
        "Est-ce que le personnage a une loyauté ambiguë ?"
    ),

    # Famille / héritage
    "famille_importante": (
        "famille_importante",
        True,
        "Est-ce que la famille du personnage est importante dans la saga ?"
    ),

    # Relations
    "proche_harry": (
        "proche_harry",
        True,
        "Est-ce que le personnage est proche de Harry Potter ?"
    ),

    # Statut spécial
    "non_eleve": (
        "professeur",
        True,
        "Est-ce que le personnage n'est pas un élève ?"
    ),

    # Sang (plus dur car moins visible)
    "sang_pur": (
        "sang",
        "Pur",
        "Est-ce que le personnage est de sang pur ?"
    ),
    "sang_mele": (
        "sang",
        "Mélé",
        "Est-ce que le personnage est de sang mêlé ?"
    ),

    # Camp sombre
    "lie_voldemort": (
        "moralite",
        "Méchant",
        "Est-ce que le personnage est lié au camp de Voldemort ?"
    ),

    # Traits narratifs
    "mort_marquante": (
        "mort_marquante",
        True,
        "Est-ce que la mort du personnage est marquante ?"
    ),

    # Pouvoir / statut
    "pouvoir_special": (
        "pouvoir_special",
        True,
        "Est-ce que le personnage a une capacité magique particulière ?"
    ),

    # Apparitions
    "present_plusieurs_tomes": (
        "present_longtemps",
        True,
        "Est-ce que le personnage apparaît dans plusieurs tomes ?"
    ),
}
