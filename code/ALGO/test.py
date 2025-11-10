from exercice import *
def test_genere_adn_length():
    seq = genere_adn(10)
    assert isinstance(seq, str)
    assert len(seq) == 10

def test_sequence_levenshtein():
    cpt = 0
    for i in range(100):
        seq1= genere_adn(6)        
        seq2= genere_adn(6)
        res = sequence_levenshtein(seq1,seq2)
        cpt += res 
        print(cpt)
        assert res <= 6        
    assert 3<=(cpt/100)< 5