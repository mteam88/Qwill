class Player:
    def __init__(self, tag):
        self.tag = tag
    def getWild(self):
        return input(tag+", please enter your wild")
    @classmethod
    def initPlayers(cls):
        '''
        Initialize humans. Returns list of Player objects.
        '''
        tags = []
        while True:
            tags.append(Player(input('\nPlayer name/tag (blank entry aborts): ')))
            if not tags[-1].tag:
                tags.pop()
                break
        print('Selected player names/tags:', [i.tag for i in tags], sep='\n')
        return tags