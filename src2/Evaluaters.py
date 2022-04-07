class Evaluater: #Super Class
    def __init__(self, xPlays):
        self.xPlays = xPlays
    def disp(self):
        for xPlay in self.xPlays:
            return xPlay.disp()
    def evalAll(self, card):
        '''
        To be overidden by child classes.
        '''
        pass

class LeastSkipped(Evaluater):
    def __init__(self, xPlays):
        super().__init__(xPlays)

    def evalAll(self, card):
        scoringlist = []
        #print("XPlays, ", self.xPlays)
        for xPlay in self.xPlays: # Looping for every play added.
            scoringlist.append([xPlay, xPlay.getScoring(card)]) # Initialize list
        #return scoringlist
        scoringlist.sort(key=lambda x: x[1][0]) # Sort by number of spaces skipped.
        #print("to be returned: ", scoringlist[0][0].__dict__)
        bestXPlayinfo = scoringlist[0]
        if bestXPlayinfo[0].hmnWild == True: #This means that we might not have to take the XPlay
            if bestXPlayinfo[1][0] <= 1: #Only take if skips 1 or none TODO: improve this
                return [bestXPlayinfo[0]]
            else:
                return [] #Empty because should be taken.
        return [bestXPlayinfo[0]] # TODO extend so takes wild then color play on turn if possible