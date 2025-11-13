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


# ========== 3.2 Les espèces hypothétiques ==========


# Question 10
class Espece:
    """
    Représente une espèce de dinosaure, avérée ou hypothétique.
    """

    def __init__(self, nom: str, sequence: str, especes_filles=None):
        """
        Initialise une espèce (avérée ou hypothétique).

        Args:
            nom (str): Nom de l'espèce
            sequence (str): Séquence ADN de l'espèce (vide pour les espèces hypothétiques)
            especes_filles (list[Espece], optional): Liste des espèces filles si hypothétique
        """
        self.nom_espece = nom
        if especes_filles is not None:
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

    def ajouter_espece_fille(self, espece) -> None:
        """
        Ajoute une espèce fille à cette espèce.

        Args:
            espece (Espece): L'espèce fille à ajouter
        """
        self.especes_filles.append(espece)

    def __str__(self) -> str:
        """
        Représentation textuelle de l'espèce.

        Returns:
            str: Description de l'espèce avec son type et ses caractéristiques
        """
        if self.est_hypothetique():
            type_espece = "hypothétique"
            res = f"Espèce {type_espece}: {self.nom_espece}\n"
            noms = [e.nom_espece for e in self.especes_filles]
            res += f"Espèces filles: {', '.join(noms)}"
        else:
            type_espece = "avérée"
            res = f"Espèce {type_espece}: {self.nom_espece}\n"
            res += f"Séquence: {self.sequence}"

        return res

    def __repr__(self) -> str:
        """
        Représentation pour le débogage.

        Returns:
            str: Nom de l'espèce
        """
        return self.nom_espece


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

    def calcule_distance(esp1: Espece, esp2: Espece) -> float:
        """
        Calcule la distance entre deux espèces (avérées ou hypothétiques).
        
        Args:
            esp1 (Espece): Première espèce
            esp2 (Espece): Deuxième espèce

        Returns:
            float: Distance entre les deux espèces
        """
        if esp1.est_averee() and esp2.est_averee():
            return sequence_levenshtein(esp1.sequence, esp2.sequence)
        elif esp1.est_averee() and esp2.est_hypothetique():
            distances = [
                calcule_distance(esp1, fille) for fille in esp2.especes_filles
            ]
            return sum(distances) / len(distances)
        elif esp1.est_hypothetique() and esp2.est_averee():
            distances = [
                calcule_distance(fille, esp2) for fille in esp1.especes_filles
            ]
            return sum(distances) / len(distances)
        else:
            distances = []
            for fille1 in esp1.especes_filles:
                for fille2 in esp2.especes_filles:
                    distances.append(calcule_distance(fille1, fille2))
            return sum(distances) / len(distances)

    while len(list_esp) > 1:
        min_distance = taille_seq + 1
        esp1_min = None
        esp2_min = None
        for i, esp1 in enumerate(list_esp):
            for j, esp2 in enumerate(list_esp):
                if i != j:
                    distance = calcule_distance(esp1, esp2)
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
