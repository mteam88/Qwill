# Meat of the AI
Penalty = Exception

class woption:
    def __init__(self, placement):
        #print("placement: ", placement)
        self.skipped = False
        self.scoreincr = False
        self.placement = placement

    @classmethod
    def evaluateall(self, optionsl): # TODO: eval by scoreincr if skipped is same
        bestskip = 15
        bestskipi = False
        optn = False
        for i, optn in enumerate(optionsl):
            if bestskip >= optn.skipped:
                bestskip = optn.skipped
                bestskipi = i
        #print("bestskip: ",bestskip)
        return optn

    def displayopt(self): #displays to user (only for debugging)
        #print("evaluating", self)
        #print("placement", self.placement)
        #print("would skip", self.skipped)
        pass
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
        llastxs = QH.lastxs(lists)
        current = (None, 12)
        for val in possible:
            if val[1] == 10:
                return val
            if val[1] < current[1]:
                current = val
        if current[1] - llastxs[current[0]] > 4: #if more than 4 spaces are skipped, take a penalty instead of playing
            raise Penalty
        return current


def takewild(lists, wilds, clrolls, true_Dice):
# TODO: Complete helper function (not always false)
    emptyspotsO = QH.emptyspots(lists, true_Dice)
    #print(emptyspotsO)
    wild = sum(wilds)
    #print(wild)
    colorofe,indexofe = map(list, zip(*emptyspotsO))
    #print(colorofe, indexofe)
    indices = [index for index, element in enumerate(indexofe) if element == wild]
    #print(indices)
    options = []

    for ind in indices:
        clr = colorofe[ind]
        #print("color: ", clr)
        #print("wild: ", wild)
        nio = QH.numindex(clr, wild)
        #print("nio: ", nio)
        if tuple(nio) in emptyspotsO:
            #print("nio possible: ", nio)
            options.append(woption(nio))
    #print("options: ", options)

    lastxl = QH.lastxs(lists)
    for option in options:
        option.skipped = option.placement[1] - lastxl[option.placement[0]]
        #print("skipped", option.skipped ,"for ", option)

    bestoptn = woption.evaluateall(options)
    if not bestoptn:
        return False, lists

    #bestoptn.displayopt()

    if bestoptn.skipped == 1: #takes wild if none are skipped
        # TODO: Improve skipped number above, probably whole function
        QH.addX(lists, bestoptn.placement[0], bestoptn.placement[1], muffled=True)
        print("Took wild")
        return [0,wild], lists
    else:
        return False, lists


def takehumanwild(lists, wild, true_Dice):
# TODO: Complete helper function, remember to only return a blocking play if
#      has 5 Xs in row to play in
    return False, lists


import random as rand
import QHelper as QH