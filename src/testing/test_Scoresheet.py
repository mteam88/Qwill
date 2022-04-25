from src2.Scoresheet import *
from pytest import *
from copy import deepcopy

def test_createcard():
    testcard = Card()
    assert testcard == [[0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0]]
    assert testcard.true_Dice == [False, False, False, False]
    testcard2 = Card(initlist=[[1,1,1,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0]])
    assert testcard2 == [[1,1,1,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0]]

def test_addx():
    testcard = Card()
    testcard.addX(XPlay([0,0], False))
    assert testcard == [[1,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0]]

def test_addx_ispossible():
    x = XPlay([0,0], False)
    x2 = XPlay([1,0], False)
    testcard = Card()
    assert x.isPossible(testcard) == True
    testcard2 = Card(initlist=[[1,1,1,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0]])
    assert x.isPossible(testcard2) == False
    testcard3 = deepcopy(testcard2)
    testcard3.true_Dice = [False, True, False, True]
    assert x2.isPossible(testcard3) == False

def test_scorecard():
    testcard = Card()
    assert testcard.scoreCard() == 0
    testcard.addX(XPlay([0,1], False))
    assert testcard.scoreCard() == 1
    testcard.addX(XPlay([1,1], False))
    assert testcard.scoreCard() == 2
    testcard.addX(XPlay([1,2], False))
    assert testcard.scoreCard() == 4

def test_findlastXs():
    testcard = Card()
    assert XPlay.findlastXs(testcard) == [-1,-1,-1,-1]
    testcard.addX(XPlay([0,1], False)) 
    assert XPlay.findlastXs(testcard) == [1,-1,-1,-1]