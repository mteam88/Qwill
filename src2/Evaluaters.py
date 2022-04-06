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
        print("XPlays, ", self.xPlays)
        for xPlay in self.xPlays: # Looping for every play added.
            scoringlist.append([xPlay, xPlay.getScoring(card)]) # Initialize list
        #return scoringlist
        scoringlist.sort(key=lambda x: x[1][0]) # Sort by number of spaces skipped.
        #print("to be returned: ", scoringlist[0][0])
        return scoringlist[0][0] # TODO extend beyond this obviously