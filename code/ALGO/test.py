import pytest
from exercice import mutation_par_remplacement,mutation_par_insertion,mutation_par_deletion

sequence_test= "ATCGGCTAATGCCGTAACGTTAGC" #séquence ADN test
p = 0.4 #taux de mutation test

#Question 2

def test_mutation_par_remplacement():
    #sequence_test = genere_adn(20)
    res = mutation_par_remplacement(sequence_test,p)
    assert len(res)==len(sequence_test)

#Question3

def mutation_par_insertion():
    #sequence_test = genere_adn(15)
    res = mutation_par_insertion(sequence_test,p)
    assert len(res)>=len(sequence_test)

def mutation_par_deletion():
    #sequence_test = genere_adn(30)
    res = mutation_par_deletion(sequence_test,p)
    assert len(res)<=len(sequence_test)
