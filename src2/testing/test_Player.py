from src2.Player import *
from pytest import *
from copy import deepcopy

def test_ai_wild():
    a = AI("test", Card())
    out = a.wild(2, card=a.card)
    assert isinstance(out, Took)
    assert out["didtake"] == True
    assert a.card == Card().addX(XPlay([0,0], False))