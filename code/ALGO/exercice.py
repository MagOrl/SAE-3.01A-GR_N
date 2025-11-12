import random as r

# Exercice 1

BASE = {"A", "T", "C", "G"}


def genere_adn(longeur: int) -> str:
    sequence = ""
    for _ in range(longeur):
        sequence += r.choice(list(BASE))
    return sequence


# Exercice 6
def sequence_levenshtein(seq_a: str, seq_b: str) -> int:
    if seq_a == seq_b:
        return 0
    elif len(seq_a) == 0:
        return len(seq_a)
    elif len(seq_b) == 0:
        return len(seq_b)
    else:
        cout = 0
        dis = [[0] * (len(seq_b) + 1) for _ in range(len(seq_a) + 1)]
        for i in range(len(seq_a) + 1):
            dis[i][0] = i
        for j in range(len(seq_b) + 1):
            dis[0][j] = j

        for i in range(1, len(seq_a) + 1):
            for j in range(1, len(seq_b) + 1):
                cout = [0, 1][seq_a[i - 1] != seq_b[j - 1]]
                dis[i][j] = min(dis[i - 1][j] + 1, dis[i][j - 1] + 1,
                                dis[i - 1][j - 1] + cout)
        return dis[-1][-1]


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
            res += f"Séquence: {self.sequence}\n"
        else:
            type_espece = "avérée"
            res = f"Espèce {type_espece}: {self.nom_espece}\n"
        if self.est_hypothetique():
            noms = []
            for e in self.especes_filles:
                noms.append(e.nom_espece)
            res += f"Espèces filles: {', '.join(noms)}"
        return res

    def __repr__(self):
        """Représentation pour le débogage"""


# Question 12

def arbre_phylogenetic(nb_espece, taille_seq):
    list_esp = []
    for i in range(nb_espece):
        list_esp.append(Espece(f'Dino {i}', genere_adn(taille_seq)))
        
    def calcule_distance(esp1:Espece,esp2:Espece):
        if esp1.est_averee or esp2.est_averee:
            return sequence_levenshtein(esp1.sequence,esp2.sequence)
        res = 0
        if esp1.est_hypothetique:
            for enf in esp1.especes_filles:
                if enf.est_hypothetique:
                    res+=calcule_distance(enf,esp2)
                else:
                    res+=1/2*(sequence_levenshtein(enf,esp1))
        if esp2.est_hypothetique:
            for enf in esp2.especes_filles:
                if enf.est_hypothetique:
                    res+=calcule_distance(esp1,enf)
                else:
                    res+=1/2*(sequence_levenshtein(enf,esp2))
        return res

    while len(list_esp) > 1:
        min = taille_seq + 1
        esp1_min = None 
        esp2_min = None
        for esp1 in list_esp:
            for esp2 in list_esp:
                if esp1!=esp2:
                    dis = calcule_distance(esp1,esp2)
                    if min>dis:
                        min = dis 
                        esp1_min = esp1
                        esp2_min = esp2
        list_esp.remove(esp1_min)
        list_esp.remove(esp2_min)
        nouv_esp = Espece(f"{esp2_min.nom_espece} + {esp2_min.nom_espece}",[esp1_min,esp2_min])
        list_esp.append(nouv_esp)
    return list_esp[0]
    
print(arbre_phylogenetic(6,4))    
    
    
#d(A+B,x) = 1/2(d(A,x),d(B,x)) calcule moyenne de distance 

