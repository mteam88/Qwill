# Meat of the AI
Penalty = Exception

class woption:
    def __init__(self, placement):
        #print("placement: ", placement)
        self.skipped = False
        self.scoreincr = False
        self.placement = placement

    @classmethod
    def evaluateall(self, optionsl, lists): # TODO: eval by scoreincr if skipped is same
        bestskip = 15
        bestskipi = "none"
        optn = False
        for i, optn in enumerate(optionsl):
            if optn.placement[1] == 10 and lists[optn.placement[0]].count(1) >= 5: # always do blocking play
                return optn # TODO: improve so it checks which blocking play to do if multiple are possible
            if bestskip >= optn.skipped:
                #print(bestskip, optn.skipped)
                bestskip = optn.skipped
                bestskipi = i
        #print("bestskip: ",bestskip)
        #print("bestskipi: ",bestskipi)
        if bestskipi == "none":
            return False
        return optionsl[bestskipi]

    def displayopt(self): #displays to user (only for debugging)
        print("evaluating", self)
        print("placement", self.placement)
        print("would skip", self.skipped)
        #pass
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
# TODO: Remember to raise
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
    wild = sum(wilds) #finding wilds sum
    #print(wild)
    colorofe,indexofe = map(list, zip(*emptyspotsO)) # disects options into color and index
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

    bestoptn = woption.evaluateall(options, lists)
    if not bestoptn:
        return False, lists

    #bestoptn.displayopt()

    if bestoptn.skipped == 1: #takes wild if none are skipped
        # TODO: Improve skipped number above, probably whole function
        QH.addX(lists, bestoptn.placement[0], bestoptn.placement[1], muffled=True)
        print("Took wild")
        return [bestoptn.placement[0],wild], lists
    else:
        return False, lists


def takehumanwild(lists, wild, true_Dice, emptyspots, numindex, lastxs, addX):
# TODO: Complete helper function, remember to only return a blocking play if
#      has 5 Xs in row to play in
    emptyspotsO = emptyspots(lists, true_Dice) #empty spots options variable.
#    print(emptyspotsO)
    colorofe,indexofe = map(list, zip(*emptyspotsO)) # disects options into color and index
#    print(colorofe,indexofe)
    #indices = [index for index, element in enumerate(indexofe) if element == wild]
    indices = []
    options = []
    for index, element in enumerate(indexofe):
#        if element == wild:
#            print("pass 1")
        if numindex(colorofe[index],wild)[1] == element:
            #print(colorofe[index],element)
            #print("pass 2")
            indices.append(element)
            options.append(woption([colorofe[index],element]))
#        print(numindex(colorofe[index],wild)[1])
#        print(element)
    """
        for ind in indices:
            clr = colorofe[ind]
            print("color: ", clr)
            print("wild: ", wild)
            nio = numindex(clr, wild)
            print("nio: ", nio)
            if tuple(nio) in emptyspotsO:
                print("nio possible: ", nio)
                options.append(woption(nio))
    """
    #print("options: ", options)
    lastxl = lastxs(lists)
    #print(lastxl)

    for opt in options:
        opt.skipped = opt.placement[1] - lastxl[opt.placement[0]]
        #print(opt.placement[1] - lastxl[opt.placement[0]])
        #print("IMPORTANT: skipped", opt.skipped ,"for ", opt)

    bestoptn = woption.evaluateall(options, lists)

    if bestoptn == False:
        print("no bestoptn")
        return False, lists

    #print("bestoptn:")
    #bestoptn.displayopt()

    if bestoptn.placement[1] == 10: #takes wild if none are skipped or if blocking play 
        # TODO: Improve skipped number above, probably whole function, makes sure it knows not to block if not 5 xs
        bestoptnrow = lists[bestoptn.placement[0]]
        print(bestoptn)
        if bestoptn.placement[1] == 10:
            if bestoptnrow.count(1) >= 5:
                #print("IMPORTANT!!!!:  ", bestoptnrow.count(1))
                addX(lists, bestoptn.placement[0], bestoptn.placement[1], muffled=False)
                print("Took human wild")
                return bestoptn.placement, lists
            else:
                return False, lists  
    elif bestoptn.skipped == 1:
        addX(lists, bestoptn.placement[0], bestoptn.placement[1], muffled=False)
        #print("Took human wild no skip")
        return bestoptn.placement, lists
    else:
        return False, lists
    return False, lists
