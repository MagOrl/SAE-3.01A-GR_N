from exercice import *


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
    velociraptor = Espece("velociraptor", "CAGTACGGTTTAGCTT")
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
