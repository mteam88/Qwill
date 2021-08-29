# Meat of the AI
import random as rand
Penalty = Exception


#def addX(lists, color, index, muffled=False):
#    """
#    Returns lists with an added "1" at colors index
#    lists: a list with 4 lists, each of which have 12 elements (index 0-11)
#    color: an integer (0, 1, 2, 3) representing which list to modify
#    index: index of to add "1" (0,1,2...,10,11)
#    """
#    try:
#        lists[color][index] = 1
#    except IndexError as e:
#        print('ERROR')
#        if not muffled:
#            raise e
#    return lists


def bestplay(lists, possible, richter=0):
    if not possible:
        raise Penalty
# TODO: Complete helper function (not random selection), remember to raise
#     Penalty exception when that is AI choice or no choices are passed.
    if richter == 0:
        current = (None, 12)
        for val in possible:
            if val[1] == 10:
                return val
            if val[1] < current[1]:
                current = val
        return current


def takewild(lists, wild, clrolls, true_Dice):
# TODO: Complete helper function (not always false)
    return False, lists


def takehumanwild(lists, wild, true_Dice):
# TODO: Complete helper function, remember to only return a blocking play if
#      has 5 Xs in row to play in
    return False, lists
