# This entrypoint file to be used in development. Start by reading README.md
from RPS_game import play, mrugesh, abbey, quincy, kris, human, random_player
from RPS import player
from unittest import main

N=1000
play (player, quincy, N)
play(player, mrugesh, N)
play(player, abbey, N)
play(player, kris, N)
