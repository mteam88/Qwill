import logging
from Scoresheet import XPlay
from typing import List

THRESHOLD = 2

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
    def __init__(self, *args, threshold=THRESHOLD, **kwargs):
        self.threshold = threshold
        super().__init__(*args, **kwargs)

    def evalAll(self, card) -> List[XPlay]:

        # Check if any are blocking plays and always take one if there is.
        if (lockingplay := self._checkalllocking(self.xPlays)): # Hooray walrus operator!
            return [lockingplay]

        scoringlist = self._generatescoringlist(card)
        
        scoringlist.sort(key=lambda x: x[1][0]) # Sort by number of spaces skipped.

        if scoringlist: 
            bestXPlayinfo = scoringlist[0] # Set bestxplayinfo

        elif self.iswild == False:
            raise Penalty
        else:
            return []

        if bestXPlayinfo[0].plyrWild == True: #This means that we might not have to take the XPlay
            return [bestXPlayinfo[0]] if bestXPlayinfo[1][0] <= self.threshold else []

        return [bestXPlayinfo[0]] # TODO extend so takes wild then color play on turn if possible


    # Internal Helper Methods
    def _generatescoringlist(self, card):
        return [[xplay, xplay.getScoring(card)] for xplay in self.xPlays]

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