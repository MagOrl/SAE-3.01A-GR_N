import pytest
from exercice import *

sequence_test= "ATCGGCTAATGCCGTAACGTTAGC" #séquence ADN test
p = 0.4 #taux de mutation test

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
