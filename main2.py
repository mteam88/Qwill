import random, sys
from src2 import Card, XPlay, Player, LeastSkipped, AI, Human
from copy import deepcopy, copy
gameover = False

player_list = Player.initPlayers()

while not gameover:
    print("\nRound "+str(player_list[0].card.roundnum)) #Using first player's roundnum, perhaps change to a class called GameState or something
    for player in player_list: # Loop through all players
        took, wild = player.turn(player.card)
        if took != []: # If player took value
            print(took) # debug only
        else:
            print("Did not take that wild")
        # TODO: go through all players and run '.wild()' method on them
        for player in player_list:
            player.wild(wild, card=player.card)
    for player in player_list: 
        player.card.roundnum += 1 #Update round counter for all players
        if isinstance(player, AI):
            print(player.tag+"'s card after round: ", player.card)





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