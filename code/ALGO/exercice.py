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

    def est_hypothetique(self):
        """Vérifie si l'espèce est hypothétique
        
        Returns:
            bool: True si l'espèce a des espèces filles, False sinon
        """
        if self.especes_filles is None or not self.especes_filles:
            return False
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

    # Question 11

    def calcul_distance(self, espece_cible):
        """Distance moyenne entre self (hypothétique) et espece_cible (avérée ou hypothétique).
        Retourne None si self n'est pas hypothétique ou si aucune comparaison valide.
        """
        if self.est_averee():
            return None

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
    print(sequence1)
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
