InputError = Exception()

class Player:
    def __init__(self, tag):
        self.tag = tag
    def getWild(self):
        while True:
            response = input(self.tag+", please enter your wild (2-12): ")
            try:
                response = int(response)
                if response in range(2,13):
                    return response
                else:
                    raise InputError
            except InputError:
                print("Please input a valid wild between 2 and 12")
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