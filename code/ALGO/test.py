import pytest
from exercice import BASE,mutation_par_remplacement,mutation_par_insertion,mutation_par_deletion

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
