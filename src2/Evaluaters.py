class Evaluater: #Super Class
    def __init__(self, xPlays):
        self.xPlays = xPlays
    def disp(self):
        for xPlay in self.xPlays:
            return xPlay.disp()
    def evalAll(card):
        '''
        To be overidden by child classes.
        '''
        pass

class LeastSkipped(Evaluater):
    def __init__(self, xPlays):
        super().__init__(xPlays)

    def evalAll(self, card):
        scoringlist = []
        for xPlay in self.xPlays: # Looping for ever play added.
            scoringlist.append([xPlay, xPlay.getScoring(card)]) # Initialize list
        return scoringlist
        scoringlist.sort(key=lambda x: x[1][0]) # Sort by number of spaces skipped.
        return scoringlist # TODO extend beyond this obviously