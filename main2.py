#Run tests:
#import subprocess
#subprocess.run(["pytest", "src2/testing/"])

#Import
import random, sys, logging
from src2 import Card, XPlay, Player, LeastSkipped, AI, Human, newround
from copy import deepcopy, copy

logging.basicConfig(level=logging.CRITICAL)

def main(player_list):
    newround(player_list,isfirstround=True)
    gameover = False
    while not gameover:
        newround(player_list)
        for active_player, (took, wild) in player_list.funcall("turn"):

            for player, wildoutput in player_list.funcall("wild", wild, active=active_player):
                (didtake, tookwhat) = wildoutput.values() # Get specific values (dict unpacking)

                if didtake: # Print message saying that a player took a wild.
                    print(f'"{player.tag}" took the wild "{wild}" from "{active_player.tag}"')

main(Player.initPlayers())