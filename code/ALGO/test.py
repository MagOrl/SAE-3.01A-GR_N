from exercice import *


def test_genere_adn_length():
    seq = genere_adn(10)
    assert isinstance(seq, str)
    assert len(seq) == 10


def test_sequence_levenshtein():
    cpt = 0
    for i in range(100):
        seq1 = genere_adn(6)
        seq2 = genere_adn(6)
        res = sequence_levenshtein(seq1, seq2)
        cpt += res
        print(cpt)
        assert res <= 6
    assert 3 <= (cpt / 100) < 5


def test_arbre_phylogenetic():
    arbre = arbre_phylogenetic(3, 4)

    assert isinstance(arbre, Espece)

    assert arbre.est_hypothetique()

    assert arbre.sequence == ""

    assert len(arbre.especes_filles) == 2

    def compter_feuilles(espece):
        if espece.est_averee():
            return 1
        else:
            total = 0
            for fille in espece.especes_filles:
                total += compter_feuilles(fille)
            return total

    # Vérifier qu'il y a exactement 3 feuilles (espèces avérées)
    nb_feuilles = compter_feuilles(arbre)
    assert nb_feuilles == 3
