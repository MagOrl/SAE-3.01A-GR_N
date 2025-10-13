import pytest
from ..exploitation_sequence import genere_adn, BASE

def test_genere_adn_length():
    seq = genere_adn(10)
    assert isinstance(seq, str)
    assert len(seq) == 10

