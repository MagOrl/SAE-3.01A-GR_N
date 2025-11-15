import random as r
# Exercice 1
# Ensemble des bases azotées de l'ADN
BASE = {"A", "T", "C", "G"}


def genere_adn(longueur: int) -> str:
    """
    Génère une séquence ADN aléatoire de longueur donnée.

    Args:
        longueur (int): Longueur de la séquence à générer

    Returns:
        str: Séquence ADN composée des bases A, T, C, G

    Raises:
        ValueError: Si la longueur est négative
    """
    if longueur < 0:
        raise ValueError("La longueur doit être positive ou nulle")

    sequence = ""
    for _ in range(longueur):
        sequence += r.choice(list(BASE))
    return sequence


# Exercice 6
def sequence_levenshtein(seq_a: str, seq_b: str) -> int:
    """
    Calcule la distance de Levenshtein entre deux séquences.
    Args:
        seq_a (str): Première séquence
        seq_b (str): Deuxième séquence

    Returns:
        int: Distance de Levenshtein entre les deux séquences
    """
    if seq_a == seq_b:
        return 0
    elif len(seq_a) == 0:
        return len(seq_b)
    elif len(seq_b) == 0:
        return len(seq_a)
    else:
        dis = [[0] * (len(seq_b) + 1) for _ in range(len(seq_a) + 1)]

        for i in range(len(seq_a) + 1):
            dis[i][0] = i
        for j in range(len(seq_b) + 1):
            dis[0][j] = j

        for i in range(1, len(seq_a) + 1):
            for j in range(1, len(seq_b) + 1):
                cout = 0 if seq_a[i - 1] == seq_b[j - 1] else 1
                dis[i][j] = min(
                    dis[i - 1][j] + 1,  
                    dis[i][j - 1] + 1,  
                    dis[i - 1][j - 1] + cout  
                )

        return dis[-1][-1]
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
        if especes_filles is not None or especes_filles:
            self.especes_filles = especes_filles
            self.sequence = ""
        else:
            self.especes_filles = []
            self.sequence = sequence

    def est_hypothetique(self) -> bool:
        """
        Vérifie si l'espèce est hypothétique.

        Returns:
            bool: True si l'espèce a des espèces filles, False sinon
        """
        return len(self.especes_filles) > 0

    def est_averee(self) -> bool:
        """
        Vérifie si l'espèce est avérée.
        Returns:
            bool: True si l'espèce n'a pas d'espèces filles, False sinon
        """
        return not self.est_hypothetique()
    def est_hypothetique(self):
        """Vérifie si l'espèce est hypothétique
        
        Returns:
            bool: True si l'espèce a des espèces filles, False sinon
        """
        if self.especes_filles is None or not self.especes_filles:
            return False
        return len(self.especes_filles) > 0        
      
    def ajouter_espece_fille(self, espece) -> None:
        """
        Ajoute une espèce fille à cette espèce.

        Args:
            espece (Espece): L'espèce fille à ajouter
        """
        self.especes_filles.append(espece)

    def ajouter_espece_fille(self, espece):
        """Ajoute une espèce fille à cette espèce
        
        Args:
            espece (Espece): l'espèce fille à ajouter
        """
        self.especes_filles.append(espece)
    def calcul_distance(self, espece_cible):
        """Distance moyenne entre self (hypothétique) et espece_cible (avérée ou hypothétique).
        Retourne None si self n'est pas hypothétique ou si aucune comparaison valide.
        """
        if self.est_averee():
            return estimation_distance(self.sequence,espece_cible.sequence)
        total_dist = 0
        cpt = 0
        if espece_cible.est_averee():
            for e in self.especes_filles:
                dist = estimation_distance(e.sequence, espece_cible.sequence)
                total_dist += dist
                cpt += 1
        else:
            for e in self.especes_filles:
                for f in espece_cible.especes_filles:
                    dist = estimation_distance(e.sequence, f.sequence)
                    total_dist += dist
                    cpt += 1
        if cpt:
            return total_dist / cpt

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



# Question 11
def estimation_distance(sequence1, sequence2):
    """
    Calcule une estimation de la distance entre deux séquences en comptant les différences
    dans les positions communes et en ajoutant la longueur de la partie restante de la séquence la plus longue.
    Args:
        sequence1 (str or list): La première séquence à comparer.
        sequence2 (str or list): La deuxième séquence à comparer.
    Returns:
        int: Le nombre total de différences, incluant les positions non communes.
    """
    diff = 0
    if len(sequence1) > len(sequence2):
        longueur_equi = len(sequence2)
        seq_reste = sequence1
    else:
        longueur_equi = len(sequence1)
        seq_reste = sequence2
    for i in range(longueur_equi):
        if sequence1[i] != sequence2[i]:
            diff += 1
    diff += len(seq_reste) - longueur_equi
    return diff

# Question 12
def arbre_phylogenetic(nb_espece: int, taille_seq: int) -> Espece:
    """
    Construit un arbre phylogénétique à partir d'espèces générées aléatoirement.
    Args:
        nb_espece (int): Nombre d'espèces initiales à générer
        taille_seq (int): Longueur des séquences ADN pour chaque espèce

    Returns:
        Espece: Racine de l'arbre phylogénétique (espèce hypothétique)
    Raises:
        ValueError: Si nb_espece < 2 ou taille_seq < 0
    """
    if nb_espece < 2:
        raise ValueError("Le nombre d'espèces doit être au moins 2")
    if taille_seq < 0:
        raise ValueError("La taille des séquences doit être positive ou nulle")

    list_esp = []
    for i in range(nb_espece):
        list_esp.append(Espece(f"Dino {i}", genere_adn(taille_seq)))
   
    while len(list_esp) > 1:
        min_distance = taille_seq + 1
        esp1_min = None
        esp2_min = None
        for i, esp1 in enumerate(list_esp):
            for j, esp2 in enumerate(list_esp):
                if i != j:
                    distance = esp1.calcul_distance(esp2)
                    if distance < min_distance:
                        min_distance = distance
                        esp1_min = esp1
                        esp2_min = esp2

        list_esp.remove(esp1_min)
        list_esp.remove(esp2_min)
        nouvelle_espece = Espece(
            f"{esp1_min.nom_espece} + {esp2_min.nom_espece}", "",
            [esp1_min, esp2_min])
        list_esp.append(nouvelle_espece)

    return list_esp[0]

if __name__ == "__main__":
    arbre = arbre_phylogenetic(6, 4)
    print(arbre)

