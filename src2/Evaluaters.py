import logging

class Penalty(Exception):
    pass

class Evaluater: #Super Class
    def __init__(self, xPlays, iswild=False):
        self.xPlays = xPlays
        self.iswild = iswild

    def disp(self):
        for xPlay in self.xPlays:
            return xPlay.disp()

    def evalAll(self, card):
        '''
        To be overidden by child classes.
        '''
        raise NotImplementedError

class LeastSkipped(Evaluater):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def evalAll(self, card):
        scoringlist = []
        for xPlay in self.xPlays: # Looping for every play added.
            scoringlist.append([xPlay, xPlay.getScoring(card)]) # Initialize list
        scoringlist.sort(key=lambda x: x[1][0]) # Sort by number of spaces skipped.

        if scoringlist:
            bestXPlayinfo = scoringlist[0]
        else: # No plays, must take penalty if turn
            if self.iswild == False:
                raise Penalty
            return []
        
        if bestXPlayinfo[0].position[1] == 10:
            return [bestXPlayinfo[0]]

        if bestXPlayinfo[0].plyrWild == True: #This means that we might not have to take the XPlay
            if bestXPlayinfo[1][0] <= 2: #Only take if skips 1 or none
                return [bestXPlayinfo[0]]

            else:
                return [] #Empty because should be taken.

        return [bestXPlayinfo[0]] # TODO extend so takes wild then color play on turn if possible