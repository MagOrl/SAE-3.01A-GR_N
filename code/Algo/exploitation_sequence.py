import random as r

BASE = {'A', 'T', 'C', 'G'}

# Question 2

def mutation_par_remplacement(sequence: str, p: float) -> str:
    """    
    La fonction permet de simuler une mutation en remplaçant une base par une autre aleatoirement.


    Args:
        sequence (str): une séquence ADN 
        p (float): taux de mutation avec p ∈ [0, 1]

    Returns:
        str: nouvelle séquence en simulant des mutations de remplacement aléatoires avec probabilité p.
    """
    if not 0 <= p <= 1:
        print("Erreur : la valeur de p doit être dans [0,1]")  # Message d'erreur si p invalide
        return None  

    nvl_seq = "" 
    for base in sequence:  
        if r.uniform(0, 1) <= p:  # Tirage aléatoire pour décider si on remplace
            nvl_seq += r.choice(list(BASE))  # Remplace la base par une base aléatoire
        else:
            nvl_seq += base  # Sinon, on garde la base originale
    return nvl_seq 


# Question 3

def mutation_par_insertion(sequence: str, p: float) -> str:
    """    
    La fonction permet de simuler une mutation en ajoutant une base aleatoirement.


    Args:
        sequence (str): une séquence ADN 
        p (float): taux de mutation avec p ∈ [0, 1]

    Returns:
        str: nouvelle séquence en simulant des mutations par insertion aléatoires avec probabilité p.
    """
    if not 0 <= p <= 1:
        print("Erreur : la valeur de p doit être dans [0,1]")
        return None

    nvl_seq = ""
    for base in sequence:  
        nvl_seq += base  # On ajoute la base actuelle
        if r.uniform(0, 1) <= p:  # Tirage aléatoire pour décider si on insère une base
            nvl_seq += r.choice(list(BASE))  # Insertion d'une base aléatoire après la base actuelle
    return nvl_seq


def mutation_par_deletion(sequence: str, p: float) -> str:
    """    
    La fonction permet de simuler une mutation en supprimant une base aleatoirement.

    Args:
        sequence (str): une séquence ADN 
        p (float): taux de mutation avec p ∈ [0, 1]

    Returns:
        str: nouvelle séquence en simulant des mutations par suppression aléatoires avec probabilité p.
    """
    if not 0 <= p <= 1:
        print("Erreur : la valeur de p doit être dans [0,1]")
        return None

    nvl_seq = ""
    for base in sequence:
        if r.uniform(0, 1) > p:  # Tirage aléatoire pour décider si on garde la base
            nvl_seq += base  # On garde la base avec probabilité 1-p
        # Sinon, on supprime la base (on ne l'ajoute pas à nvl_seq)
    return nvl_seq

