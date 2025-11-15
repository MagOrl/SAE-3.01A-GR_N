from exercice import *
sequence_test= "ATCGGCTAATGCCGTAACGTTAGC" #séquence ADN test
p = 0.4

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
 #taux de mutation test

#Question 2

def test_mutation_par_remplacement():
    #sequence_test = genere_adn(20)
    res = mutation_par_remplacement(sequence_test,p)
    assert len(res)==len(sequence_test)
    assert res is not None
    assert mutation_par_remplacement(sequence_test, -0.2) is None
    res_p0 = mutation_par_remplacement(sequence_test, 0)
    assert res_p0 == sequence_test
    assert sequence_test != res
    assert all(elem in BASE for elem in res)


#Question3

def test_mutation_par_insertion():
    #sequence_test = genere_adn(15)
    res = mutation_par_insertion(sequence_test,p)
    assert len(res)>=len(sequence_test)
    assert res is not None
    assert mutation_par_insertion(sequence_test, 1.5) is None
    res_p0 = mutation_par_insertion(sequence_test, 0)
    assert res_p0 == sequence_test
    assert sequence_test != res
    assert all(elem in BASE for elem in res)


def test_mutation_par_deletion():
    #sequence_test = genere_adn(30)
    res = mutation_par_deletion(sequence_test,p)
    assert len(res)<=len(sequence_test)
    assert res is not None
    assert mutation_par_deletion(sequence_test, 2.5) is None
    res_p0 = mutation_par_deletion(sequence_test, 0)
    assert res_p0 == sequence_test
    assert sequence_test != res
    assert all(elem in BASE for elem in res)


def test_str():
    # Test pour une espèce avérée
    tyrannosaure = Espece("Tyrannosaure", "CAGTACGGTTTAGCAT")
    str_tyrannosaure = "Espèce avérée: Tyrannosaure\nSéquence: CAGTACGGTTTAGCAT\n"
    assert str(tyrannosaure) == str_tyrannosaure
    
    # Test pour une espèce hypothétique
    velociraptor = Espece("Vélociraptor", "CAGTACGGTTTAGCTT")
    ancetre_commun = Espece("Ancêtre Théropode", "", [tyrannosaure, velociraptor])
    str_ancetre = "Espèce hypothétique: Ancêtre Théropode\nSéquence: \nEspèces filles: Tyrannosaure, Vélociraptor"
    assert str(ancetre_commun) == str_ancetre

def test_repr():
    # Test pour une espèce avérée
    tyrannosaure = Espece("Tyrannosaure", "CAGTACGGTTTAGCAT")
    repr_tyrannosaure = "Espece('Tyrannosaure', 'CAGTACGGTTTAGCAT', 0 filles)"
    assert repr(tyrannosaure) == repr_tyrannosaure
    
    # Test pour une espèce hypothétique
    velociraptor = Espece("Vélociraptor", "CAGTACGGTTTAGCTT")
    ancetre_commun = Espece("Ancêtre Théropode", "", [tyrannosaure, velociraptor])
    repr_ancetre = "Espece('Ancêtre Théropode', '', 2 filles)"
    assert repr(ancetre_commun) == repr_ancetre

def test_estimation_distance_mutation():
    ech1 = "ATCTACTAGCT"
    ech2 = "ACCTACAGGGT"
    ech3 = "CAGTACGGTTTAGCAT"
    ech4 = "GCTAGCTAGGCTAGCT"
    assert estimation_distance_mutation(ech1, ech2) == 4
    assert estimation_distance_mutation(ech3, ech4) == 14
    assert estimation_distance_mutation(ech1, ech4) == None


def test_est_hypothetique():
    t_rex = Espece("t-rex", "CAGTACGGTTTAGCAT")
    velociraptor = Espece("velociraptor", "CAGTACGGTTTAGCTT", [])
    assert t_rex.est_hypothetique() == False
    assert velociraptor.est_hypothetique() == False
    ancetre_commun = Espece("ancêtre-théropode", "",
                            [t_rex, velociraptor])
    assert ancetre_commun.est_hypothetique() == True



def test_est_averee():
    t_rex = Espece("t-rex", "CAGTACGGTTTAGCAT")
    velociraptor = Espece("velociraptor", "CAGTACGGTTTAGCTT")
    assert t_rex.est_averee() == True
    assert velociraptor.est_averee() == True
    ancetre_commun = Espece("ancêtre-théropode", "",
                            [t_rex, velociraptor])
    assert ancetre_commun.est_averee() == False


def test_ajouter_espece_fille():
    t_rex = Espece("t-rex", "CAGTACGGTTTAGCAT")
    velociraptor = Espece("velociraptor", "CAGTACGGTTTAGCTT")
    ancetre_commun = Espece("ancêtre-théropode", "",
                            [t_rex, velociraptor])
    assert len(ancetre_commun.especes_filles) == 2
    triceratops = Espece("triceratops", "CAGTACGCATTGGCTT")
    ancetre_commun.ajouter_espece_fille(triceratops)
    assert len(ancetre_commun.especes_filles) == 3

def test_estimation_distance():
    # Test avec séquences de même longueur
    assert estimation_distance("ATCG", "ATCG") == 0
    assert estimation_distance("ATCG", "ATCA") == 1
    assert estimation_distance("ATCTACTAGCT", "ACCTACAGGGT") == 4
    
    # Test avec séquences de longueurs différentes
    assert estimation_distance("ATCG", "ATCGT") == 1
    assert estimation_distance("ATCGT", "ATCG") == 1
    assert estimation_distance("CAGTACGGTTTAGCAT", "GCTAGCTAGGCTAGCT") == 14

def test_calcul_distance():
    # Test avec une espèce avérée (devrait retourner None)
    t_rex = Espece("t-rex", "CAGTACGGTTTAGCAT")
    velociraptor = Espece("velociraptor", "CAGTACGGTTTAGCTT")
    assert t_rex.calcul_distance(velociraptor) == None
    
    # Test avec une espèce hypothétique vs une espèce avérée
    ancetre_commun = Espece("ancêtre-théropode", "", [t_rex, velociraptor])
    triceratops = Espece("triceratops", "CAGTACGCATTGGCTT")
    # Distances: estimation_distance(t_rex.seq, triceratops.seq) = 4, estimation_distance(velociraptor.seq, triceratops.seq) = 3
    # Moyenne: (4 + 3) / 2 = 3.5
    assert ancetre_commun.calcul_distance(triceratops) == 3.5
    
    # Test avec deux espèces hypothétiques
    ancetre2 = Espece("ancêtre2", "", [triceratops])
    # Distances entre filles: t_rex vs triceratops (4), velociraptor vs triceratops (3)
    # Moyenne: (4 + 3) / 2 = 3.5
    assert ancetre_commun.calcul_distance(ancetre2) == 3.5

def test_calcul_distance_none():
    t_rex = Espece("t-rex", "CAGTACGGTTTAGCAT")
    velociraptor = Espece("velociraptor", "CAGTACGGTTTAGCTT")
    assert t_rex.calcul_distance(velociraptor) == None
