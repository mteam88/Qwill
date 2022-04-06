import random, sys
from src2 import Card, XPlay, Player, LeastSkipped, AI
from copy import deepcopy, copy
gameover = False

player_list = Player.initPlayers()
main_card = Card()
ai = AI(main_card)

while not gameover:
    print("\nAI turn: (begin round "+str(main_card.roundnum)+" )")
    took = ai.eval(ai._getXPlays(main_card.true_Dice)[0], main_card)
    if took == True:
        print("Took a play")
    else:
        main_card.penalty += 5
        print("Took a penalty")
    #print(ai._getXPlays(main_card.true_Dice))
    for player in player_list:
        print("Player(s) turn(s): ")
        took = ai.eval(AI._getXPlaysfromwild(player.getWild(), hmnWild=True), main_card)
        if took == True:
            print("Took that wild")
        else:
            print("Did not take that wild")
    main_card.roundnum += 1 #Update round counter





testCard = Card(initlist=[[1,1,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,1,1,0,1,0,0], [0,0,0,0,1,1,1,1,1,0,0,0], [1,0,1,0,0,0,0,0,0,0,0,0]], true_Dice=[True, True, True, False], penalty=0)

leastSkippedEval = LeastSkipped([XPlay([1, 0], True), XPlay([0, 2], True), XPlay([1, 1], True), XPlay([2, 1], True), XPlay([0, 0], True), XPlay([3, 3], True)])
#print([x[1] for x in leastSkippedEval.evalAll(testCard)])
'''
otherCard = Card(initlist=[[1,1,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,1,1,0,1,0,0], [0,0,0,0,1,1,1,1,1,0,0,0], [1,0,1,0,0,0,0,0,0,0,0,0]], true_Dice=[True, True, True, False], penalty=0)

x = testCard.getLists()
newCard = Card(initlist=deepcopy(testCard))
newCard.addX([0,2])
print(repr(testCard))
print(repr(newCard))
print(repr(otherCard))'''

try: #Tests
    assert XPlay([0,0], True).isPossible(testCard) == False #Cannot overide previous positions
    assert XPlay([1,10], True).isPossible(testCard) == False #Cannot lock row if not 5 xs already
    assert XPlay([2,10], True).isPossible(testCard) == True #Can lock row if 5 xs already
    assert XPlay([3,5], True).isPossible(testCard) == False #Cannot take play because color is locked
except AssertionError as e:
    print("ERROR IN TESTING")
    #raise e