import random as r

# Ensemble des bases azotées de l'ADN
BASE = {"A", "T", "C", "G"}

# =============================================
# Question 1
# =============================================
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


# =============================================
# Question 2
# =============================================
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


# =============================================
# Question 3
# =============================================
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


# =============================================
# Question 4
# =============================================
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

# =============================================
# Question 6 (facultative)
# =============================================
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
    
# =============================================
# Question 10
# =============================================
class Espece():

    def __init__(self, nom, sequence="", especes_filles=None):
        """
        Initialise une espèce.
        - Si especes_filles est None → espèce avérée avec sequence
        - Sinon → espèce hypothétique avec filles, sequence ignorée
        """
        self.nom_espece = nom
        if especes_filles is not None:
            self.especes_filles = especes_filles
            self.sequence = ""  # pas de séquence pour hypothétique
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
        return len(self.especes_filles) == 0
        
    def ajouter_espece_fille(self, espece) -> None:
        """
        Ajoute une espèce fille à cette espèce.

        Args:
            espece (Espece): L'espèce fille à ajouter
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


# =============================================
# Question 11
# =============================================
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


# =============================================
# Question 12
# =============================================
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


# =============================================
# Menu Simple Executable
# =============================================
if __name__ == "__main__":
    import os
    os.system('cls' if os.name == 'nt' else 'clear')  # Nettoie l'écran

    while True:
        print("\n" + "="*50)
        print("   MENU ADN   ")
        print("="*50)
        print("1. Générer une séquence ADN")
        print("2. Mutation par remplacement")
        print("3. Mutation par insertion")
        print("4. Mutation par suppression")
        print("5. Distance naïve (même longueur)")
        print("6. Distance de Levenshtein")
        print("7. Distance estimée (insertions/suppressions)")
        print("8. Construire un arbre phylogénétique")
        print("0. Quitter")
        print("-"*50)

        choix = input("Choisissez une option (0-8) : ").strip()

        # Quitter
        if choix == "0":
            print("Au revoir !")
            break

        # 1. Générer ADN
        elif choix == "1":
            try:
                n = int(input("Longueur de la séquence : "))
                seq = genere_adn(n)
                print(f"Séquence générée : {seq}")
            except Exception as e:
                print(f"Erreur : {e}")

        # 2. Mutation remplacement
        elif choix == "2":
            seq = input("Séquence ADN : ").upper()
            try:
                p = float(input("Taux de mutation (0 à 1) : "))
                result = mutation_par_remplacement(seq, p)
                if result is not None:
                    print(f"Après mutation : {result}")
            except Exception as e:
                print(f"Erreur : {e}")

        # 3. Mutation insertion
        elif choix == "3":
            seq = input("Séquence ADN : ").upper()
            try:
                p = float(input("Taux d'insertion (0 à 1) : "))
                result = mutation_par_insertion(seq, p)
                if result is not None:
                    print(f"Après insertion : {result}")
            except Exception as e:
                print(f"Erreur : {e}")

        # 4. Mutation suppression
        elif choix == "4":
            seq = input("Séquence ADN : ").upper()
            try:
                p = float(input("Taux de suppression (0 à 1) : "))
                result = mutation_par_deletion(seq, p)
                if result is not None:
                    print(f"Après suppression : {result}")
            except Exception as e:
                print(f"Erreur : {e}")

        # 5. Distance naïve
        elif choix == "5":
            s1 = input("Séquence 1 : ").upper()
            s2 = input("Séquence 2 : ").upper()
            dist = estimation_distance_mutation(s1, s2)
            if dist is None:
                print("Erreur : les séquences doivent avoir la même longueur !")
            else:
                print(f"Distance naïve : {dist}")

        # 6. Levenshtein
        elif choix == "6":
            s1 = input("Séquence 1 : ").upper()
            s2 = input("Séquence 2 : ").upper()
            dist = sequence_levenshtein(s1, s2)
            print(f"Distance de Levenshtein : {dist}")

        # 7. Distance estimée (Q11)
        elif choix == "7":
            s1 = input("Séquence 1 : ").upper()
            s2 = input("Séquence 2 : ").upper()
            dist = estimation_distance(s1, s2)
            print(f"Distance estimée : {dist}")

        # 8. Arbre phylogénétique
        elif choix == "8":
            try:
                nb = int(input("Nombre d'espèces (min 2) : "))
                taille = int(input("Taille des séquences ADN : "))
                print("Construction de l'arbre en cours...")
                arbre = arbre_phylogenetic(nb, taille)
                print("\nArbre phylogénétique construit !")
                print(arbre)
            except Exception as e:
                print(f"Erreur : {e}")

        else:
            print("Option invalide !")
        
        input("\nAppuyez sur Entrée pour continuer...")
        os.system('cls' if os.name == 'nt' else 'clear')