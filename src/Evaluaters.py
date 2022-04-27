import logging
from Scoresheet import XPlay

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

    def evalAll(self, card) -> XPlay:

        # Check if any are blocking plays and always take one if there is.
        if (lockingplay := self._checkalllocking(self.xPlays)): # Hooray walrus operator!
            return [lockingplay]

        scoringlist = [[xPlay, xPlay.getScoring(card)] for xPlay in self.xPlays]
        scoringlist.sort(key=lambda x: x[1][0]) # Sort by number of spaces skipped.

        if scoringlist: 
            bestXPlayinfo = scoringlist[0] # Set bestxplayinfo
        elif self.iswild == False:
            raise Penalty
        else:
            return []

        if bestXPlayinfo[0].plyrWild == True: #This means that we might not have to take the XPlay
            return [bestXPlayinfo[0]] if bestXPlayinfo[1][0] <= 2 else []

        return [bestXPlayinfo[0]] # TODO extend so takes wild then color play on turn if possible


    # Internal Helper Methods
    @staticmethod
    def _checklocking(play) -> bool:
        "Returns True if locking play."
        return play.position[1] == 10
    
    @classmethod # So can call _checklocking here
    def _checkalllocking(cls, playslist):
        "Returns a locking play if there is one in playslist."
        for play in playslist:
            if cls._checklocking(play):
                return play