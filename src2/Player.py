from Evaluaters import *
from random import randint
from Scoresheet import XPlay, Card

class InputError(Exception):
    pass

class Player:
    def __init__(self, tag):
        self.tag = tag
    def getWild(self):
        '''Get wild from player. Returns number that was rolled, not XPlay or index. Should be overwritten.'''
        pass
    def turn(self):
        '''Take turn. Returns [dict object with {bool True if took X (False on penalty), any/all XPlays used list(empty if none or human)}
            , wild (as a number)]'''
        pass
    def wild(self):
        '''Decide if should take wild based on card. Returns Returns [dict object with {bool True if took X (False on penalty)
            , any/all XPlays used list(empty if none or human)}
            , wild (as a number)]'''
    @classmethod
    def initPlayers(cls):
        '''
        Initialize all players. Returns list of Human and AI objects (with Player superclassed).
        '''
        players = []
        while True:
            tag = input('\nPlayer name/tag (blank entry aborts) (prefix with "cpu_" to create a cpu): ')
            if tag != '':
                if tag.split('_')[0] == 'cpu':
                    players.append(AI(tag, Card()))
                else:
                    players.append(Human(tag, Card()))
            else: break
        print('Selected player names/tags:', [player.tag for player in players], sep='\n')
        return players

class Human(Player):
    def __init__(self, tag, card):
        super().__init__(tag)
        #self.tag = tag
        self.card = card  # Not used      
    def turn(self, card):
        while True:
            response = input(self.tag+", please enter your wild (2-12): ")
            try:
                response = int(response)
                if response in range(2,13):
                    return [[], response]
                else:
                    raise InputError
            except (InputError,ValueError):
                print("Please input a valid integer wild between 2 and 12")
    def wild(self, wild, card=None):
        pass


class AI(Player):
    '''
    Class that interprets card state and decides what to do based on Evaluaters and Card
    '''
    def __init__(self, tag, card):
        super().__init__(tag)
        #self.tag = tag
        self.card = card # Not used

    def _getXPlays(self, true_Dice):
        '''
        returns list that contains XPlay objects for 'False' dice, but 'False' for 'True' dice also returns rolls
        Rolls dice by self
        '''
        rolls = []
        for i in range(2):
            rolls.append(randint(1,6))
        for i in true_Dice:
            if not i:
                rolls.append(randint(1,6))
            else:
                rolls.append(False)
        #print("rolls: ", rolls)
        #Now turn rolls into XPlay 
        plays = []
        for i in range(2): #for both wilds added to colors
            for j in range(4): #for all color dice
                clroll = rolls[j+2] #color value currently being processed
                if clroll is not False: #Is color actually rolled (may be locked)
                    realrolls = [rolls[0] + clroll, rolls[1] + clroll] #Get actual numbers on scorecard
                    if j >= 2: #Is number is blue or green
                        for i, _ in enumerate(realrolls): #for both numbers in realrolls (added each wild to color)
                            toapp = XPlay([j, 12 - realrolls[i]], False) #12 - val to get index from number
                            plays.append(toapp) #append to list
                    else: #Means number is yellow or red
                        for i, _ in enumerate(realrolls): #for both numbers in realrolls (added each wild to color)
                            plays.append(XPlay([j, realrolls[i] - 2], False)) # val - 2 to get index from number
        plays += AI._getXPlaysfromwild(sum(rolls[0:2])) # Get all of the wild plays
        return plays, rolls #return data

    def turn(self, card):
        playslist, rolls = self._getXPlays(card.true_Dice)
        plays = self.eval(playslist, card)
        took = self._gettookfromXPlays(plays, card)
        return [took, sum(rolls[0:2])] # latter is wild returned from _getXPlays() function 

    @classmethod
    def _getXPlaysfromwild(cls, wildint, plyrWild=False):
        plays = []
        for i in range(2): #for red and yellow that the two wilds added could go in
            plays.append(XPlay([i,wildint], True, plyrWild=plyrWild)) # append wild play for every color
        for i in range(2): #for blue and green that the two wilds added could go in
            plays.append(XPlay([i,12-wildint], True, plyrWild=plyrWild)) # append wild play for every color
        return plays

    @classmethod
    def _gettookfromXPlays(cls, plays, card):
        '''Helper function to get Took object from list of XPlays selected by eval() method'''
        took = Took({"didtake": False, "tookwhat": []}) # Defaults to did take penalty
        if plays != []:
            for play in plays: # Add penalty taking functionality (if plays == [])
                took["didtake"] = True
                took["tookwhat"].append(play)
                card.addX(play.position)
        elif plays == []:
            took["didtake"] = False
            took["tookwhat"] = []
        else:
            print("Warning: plays is unusual.(at AI._gettookfromXPlays() classmethod)")
        return took

    def eval(self, playslist, card):
        lse = LeastSkipped(playslist)
        return lse.evalAll(card)
        #print("evalall out: ", lse.evalAll(card))
    
    def wild(self, wild, card=None):
        if card == None:
            raise Exception('No card passed to AI.wild()')
        plays = self.eval(self._getXPlaysfromwild(wild, plyrWild=True), card)[0] # Note the [0] bit, eval can only return one best for human wild
        card.addX(play)
        took = self._gettookfromXPlays(plays, card)
        return took
        

class Took(dict): # Super simple class (pun intended) to make naming and extending easier.
    def __init__(self, dict):
        super().__init__(dict)