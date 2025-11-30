questions_map = {
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
    "trait_quidditch": ("trait_distinctif", "Quidditch", "Est-ce que le personnage joue au Quidditch ?"),
}
