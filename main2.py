#Run tests:
#import subprocess
#subprocess.run(["pytest", "src2/testing/"])

#Import
import random, sys, logging
random.seed(200)
from src import Card, XPlay, Player, LeastSkipped, AI, Human, newround, isgameover, PlayerList
from copy import deepcopy, copy

logging.basicConfig(level=logging.WARNING)

def main(player_list):
    newround(player_list,isfirstround=True)
    gameover = False
    while not gameover:
        newround(player_list)
        for active_player, (took, wild) in player_list.funcall("turn"):

            gameover = isgameover(player_list)
            if took.ispenalty: # Set in turn, true if AI took penalty
                print(f'"{active_player.tag}" took a penalty. They now have {active_player.card.penalty} penalties.')
                gameover = isgameover(player_list)


            for player, wildoutput in player_list.funcall("wild", wild, active=active_player):
                (didtake, tookwhat) = wildoutput.values() # Get specific values (dict unpacking)
                gameover = isgameover(player_list)

                if didtake: # Print message saying that a player took a wild.
                    print(f'"{player.tag}" took the wild "{wild}" from "{active_player.tag}"')

#main(Player.initPlayers())
from Player import PlayerList, AI, Human
plist = PlayerList([AI('cpu_quill', Card()), Human('me', Card())])
main(plist)