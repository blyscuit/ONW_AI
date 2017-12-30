from game import Game, ColorTextExt, Roles
from player import Player
from PlayerAI import PlayerAI
from PlayerHuman import PlayerHuman
import threading
from threading import _Timer
from threading import Thread
import time
import sys
from timeit import Timer
from multiprocessing import Process
from Tkinter import *

class MyDialog:
    def __init__(self, parent):

        top = self.top = Toplevel(parent)

        Label(top, text="Vote").pack()

        self.e = Entry(top)
        self.e.pack(padx=5)

        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):

        print "value is", self.e.get()

        self.top.destroy()


class CustomTimer(_Timer):
    def __init__(self, interval, function, args=[], kwargs={}):
        self._original_function = function
        super(CustomTimer, self).__init__(
            interval, self._do_execute, args, kwargs)

    def _do_execute(self, *a, **kw):
        self.result = self._original_function(*a, **kw)

    def join(self):
        super(CustomTimer, self).join()
        return self.result

gamePlaying = 0
startTime = time.time()
def timesUp():
    # thread1.exit()
    # thread2.exit()
    return False
def gameover():
    for player in playerArray:
        player.playerAI.thinkAboutClaims(player)
        player.playerAI.claim(player)
    for player in playerArray:
        player.playerAI.vote(player)
        game.voteFor(player.voteFor, player.playerID)
    print ColorTextExt.PROPMTEXT, "Game Over", ColorTextExt.RESET
    game.countVote()
    game.printCurretGame()

GAMETIME = 4.0
nPlayers = 0
while(nPlayers > 6 or nPlayers < 3):
    var = raw_input(ColorTextExt.PROPMTEXT + "Please enter number of players (3-6): " + ColorTextExt.RESET)
    try:
        nPlayers = int(float(var))
    except ValueError:
        nPlayers = 0
print ColorTextExt.PROPMTEXT, "Starting a game with", var, "players", ColorTextExt.RESET
game = Game(nPlayers)
playerArray = []
for idx, card in enumerate(game.gameTable):
    if (idx < game.numberOfPlayers):
        newPlayer = None
        if idx == 0:
            newPlayer = Player(card, idx, game, PlayerHuman())
        else:
            newPlayer = Player(card, idx, game, PlayerAI())
        playerArray.append(newPlayer)
        newPlayer.playerAI.lookOwnCard(newPlayer)
        newPlayer.playerAI.useSkill(newPlayer)
        # print playerArray.l
        # new1Player.playerAI.vote(newPlayer)
        # game.voteFor(newPlayer.voteFor, newPlayer.playerID)

gamePlaying = threading.Timer(GAMETIME, timesUp).start()
threading.Timer(GAMETIME, gameover).start()
# CustomTimer(GAMETIME, timesUp).start()
# CustomTimer(GAMETIME, gameover).start()
def inputLoop():
    print ColorTextExt.PROPMTEXT + "What are you? \n " + "WEREWOLF = 0,SEER = 1,THIEF = 2,VILLAGER = 3 \n " + "v[roles]: t[roles][person]" + ColorTextExt.RESET + "\n"
    while 1:
        input_string = raw_input()
        if input_string[:1].lower() == "v":
            try:
                inN = int(float(input_string[1:]))
                playerArray[0].voteFor = inN
                print "You voted: ", inN
            except ValueError:
                print "Wrong vote format"
        elif input_string[:1].lower() == "t":
            try:
                game.claimThief(int(float(input_string[2:3])), int(float(input_string[1:2])), 0)
            except ValueError:
                print "Wrong vote format"
        else:
            try:
                game.claimRole(Roles.roleAtIndex(int(float(input_string))), 0, 0 )
                # print "You claimed to be: ", input_string
            except ValueError:
                print "Wrong format"
def AIRunning():
    while 1:
        timeleft = GAMETIME - (time.time() - startTime)
        for player in playerArray:
            player.playerAI.talkingLoop(player)
    pass

thread1 = threading.Thread( target=inputLoop)
thread2 = threading.Thread( target=AIRunning)

thread1.daemon = True
thread2.daemon = True

thread1.start()
thread2.start()
