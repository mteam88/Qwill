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


def bestplay(lists, possible, richter=0, lastxs=False):
    if not possible: # Checking if no plays are possible
        raise Penalty # Choosing to take a QWIXX penalty
# TODO: Complete helper function (not random selection), remember to raise
#     Penalty exception when that is AI choice or no choices are passed.
    if richter == 0:
        return rand.choice(possible)

    if richter == 1: #richter 1 is leftmost play selected 
        current = (None, 12)
        for val in possible:
            if val[1] == 10:
                return val
            if val[1] < current[1]:
                current = val
        return current

    if richter == 2: # BETA
        llastxs = lastxs(lists)
        current = (None, 12)
        for val in possible:
            if val[1] == 10:
                return val
            if val[1] < current[1]:
                current = val
        if current[1] - llastxs[current[0]] > 4: #if more than 4 spaces are skipped, take a penalty instead of playing
            raise Penalty
        return current


def takewild(lists, wilds, clrolls, true_Dice, addX, emptyspots, numindex):
# TODO: Complete helper function (not always false)
    emptyspotsO = emptyspots(lists, true_Dice)
    print(emptyspotsO)
    wild = sum(wilds)
    print(wild)
    colorofe,indexofe = map(list, zip(*emptyspotsO))
    print(colorofe, indexofe)
    indices = [index for index, element in enumerate(indexofe) if element == wild]
    print(indices)
    options = []
    for ind in indices:
        clr = colorofe[ind]
        #print("color: ", clr)
        #print("wild: ", wild)
        nio = numindex(clr, wild)
        #print("nio: ", nio)
        options.append(nio)
    print(options)
    # TODO: eval options
    if False:
        addX(lists, wild[0], wild, muffled=True)
        print("Took wild")
        return [0,wild], lists
    else:
        return False, lists


def takehumanwild(lists, wild, true_Dice):
# TODO: Complete helper function, remember to only return a blocking play if
#      has 5 Xs in row to play in
    return False, lists
