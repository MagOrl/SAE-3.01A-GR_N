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