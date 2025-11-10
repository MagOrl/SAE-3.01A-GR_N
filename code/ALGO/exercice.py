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

# ========== 2 Calcul de similarité ==========


# Question 4
def estimation_distance_mutation(echantillon1: str,
                                 echantillon2: str) -> int | None:
    """Renvoie une estimation de manière naïve d'une distance de mutation pour deux échantillons avec permutation seulement

    Args:
        echantillon1 (str): échantillon numéro 1 (doit avoir la même taille que le deuxième)
        echantillon2 (str): échantillon numéro 2 (doit avoir la même taille que le premier)

    Returns:
        int|None: renvoie None si la taille n'est pas la même sinon une estimation de la distance de mutation
    """
    if len(echantillon1) != len(echantillon2):
        return None
    distance = 0
    for indice in range(len(echantillon1)):
        if echantillon1[indice] != echantillon2[indice]:
            distance += 1
    return distance


# ========== 3.2 Les espèces hypothétiques ==========


# Question 10
class Espece():

    def __init__(self, nom, sequence, especes_filles=None):
        """Initialise une espèce (avérée ou hypothétique)
        
        Args:
            nom (str): nom de l'espèce
            sequence (str): séquence ADN de l'espèce
            especes_filles (list[Espece], optional): liste des espèces filles si hypothétique
        """
        self.nom_espece = nom
        if especes_filles is not None:
            self.especes_filles = especes_filles
            self.sequence = ""
        else:
            self.especes_filles = []
            self.sequence = sequence

    def est_hypothetique(self):
        """Vérifie si l'espèce est hypothétique
        
        Returns:
            bool: True si l'espèce a des espèces filles, False sinon
        """
        return len(self.especes_filles) > 0

    def est_averee(self):
        """Vérifie si l'espèce est avérée
        
        Returns:
            bool: True si l'espèce n'a pas d'espèces filles, False sinon
        """
        return not self.est_hypothetique()

    def ajouter_espece_fille(self, espece):
        """Ajoute une espèce fille à cette espèce
        
        Args:
            espece (Espece): l'espèce fille à ajouter
        """
        self.especes_filles.append(espece)

    def __str__(self):
        """Représentation textuelle de l'espèce"""
        if self.est_hypothetique():
            type_espece = "hypothétique"
        else:
            type_espece = "avérée"
        res = f"Espèce {type_espece}: {self.nom_espece}\n"
        res += f"Séquence: {self.sequence}\n"
        if self.est_hypothetique():
            noms = []
            for e in self.especes_filles:
                noms.append(e.nom_espece)
            res += f"Espèces filles: {', '.join(noms)}"
        return res

    def __repr__(self):
        """Représentation pour le débogage"""
        return f"Espece('{self.nom_espece}', '{self.sequence}', {len(self.especes_filles)} filles)"
