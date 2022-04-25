from src2.Player import *
from pytest import *
from copy import deepcopy

def test_ai_wild():
    testcard = Card()
    a = AI("test", testcard)
    out = a.wild(2, card=a.card)
    assert isinstance(out, Took)
    assert out["didtake"] == True
    assert a.card == Card().addX(XPlay([0,0], False))
    out = a.wild(2, card=a.card)
    assert isinstance(out, Took)
    assert out["didtake"] == True
    testcard2 = Card()
    testcard2.addX(XPlay([0,0], False))
    testcard2.addX(XPlay([1,0], False))
    assert a.card == testcard2
    out = a.wild(2, card=a.card)
    assert isinstance(out, Took)
    assert out["didtake"] == False
    testcard3 = Card()
    testcard3.addX(XPlay([0,0], False))
    testcard3.addX(XPlay([1,0], False))
    assert a.card == testcard2

def test_ai_turn(): #TODO: Improve this
    testcard = Card()
    