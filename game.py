import json
import logging
import random
from uuid import uuid4
from util import dotdict
class ColorTextExt:
    def __init__(self, i, j = 0):
        self.fore = i
        self.back = j
    def __repr__(self):
        return self.textFore[self.fore]
    textFore = [
    "\033[37m",      # white
    "\033[31m",      # red
    "\033[32m",      # green
    "\033[33m",      # yellow
    "\033[34m",      # blue
    "\033[35m",      # magenta
    "\033[36m",      # cyan
    "\033[30m",]      # black
    RESET = "\033[0m"      # reset
    PROPMTEXT = "\033[30m" + "\033[47m"
class Blaim:
    claimBy = None
    claimed = None
    role = None

    def __init__(self, claimBy, claimed, role):
        self.claimBy = claimBy
        self.claimed = claimed
        self.role = role

def enum(**enums):
    return type('Enum', (), enums)
class Roles:
    @classmethod
    def roleAtIndex(cls, i):
        return {
            0: cls.WEREWOLF,
            1: cls.SEER,
            2: cls.THIEF,
            3: cls.VILLAGER,
        }.get(i, cls.VILLAGER)

    WEREWOLF = dotdict({"value":0, "name":"WEREWOLF"})
    SEER = dotdict({"value":1, "name":"SEER"})
    THIEF = dotdict({"value":2, "name":"THIEF"})
    VILLAGER = dotdict({"value":3, "name":"VILLAGER"})
    UNKNOWN = dotdict({"value":-1, "name":"UNKNOWN"})

class Game:

    # number of players: werewolf, villager
    ROLES_NUMBER = {
        3: [2,1],
        4: [2,2],
        5: [2,3],
        6: [2,4],
        7: [2,4],
    }

    GAME_STARTING = 'Starting game...'
    CHECKING_PLAYERS = 'Checking players...'
    INVALID_PLAYERS_LENGTH = 'You can only have 3-10 players in this channel ' \
                             'to start a game!'
    GAME_STARTED = 'Everyone, pretend to close your eyes.'

    CENTER_1 = ':black_joker: First card'
    CENTER_2 = ':black_joker: Second card'
    CENTER_3 = ':black_joker: Third card'

    CENTER_NUMBER = 2

    LOOK_OWN_CARD = ':black_joker: Everyone, look at your own card.'
    LOOK_OWN_CARD_ACTION = 'Look'
    LOOK_OWN_CARD_REVEAL = 'You are a {}'

    WEREWOLF_WAKE_UP = ':wolf: Werewolves, wake up and look for other ' \
                       'werewolves.'
    WEREWOLF_ATTACHMENT = 'If you are a werewolf...'
    WEREWOLF_LOOK_FOR_OTHERS = 'Look for others'
    WEREWOLF_LONE = 'You are the lone wolf'
    WEREWOLF_LONE_LOOKED = 'You already looked at a center card'
    WEREWOLF_NOT_LONE = 'You are not the lone wolf'
    WEREWOLF_LIST = 'The other werewolves are: {}'
    WEREWOLF_LONE_ATTACHMENT = 'If you are the lone wolf, check one of the ' \
                               'center cards...'
    WEREWOLF_LOOK_AT_CENTER = 'The {} is a {}'
    WEREWOLF_FALSE = 'You are not a werewolf!'

    SEER_WAKE_UP = ':crystal_ball: Seer, wake up. You make look at another ' \
                   'player\'s card or two of the center cards.'

    numberOfPlayers = 3
    gameTable = []
    gameTableEdited = []
    voteArray = [int]
    claimArray = []

    
    def __init__(self, players):
        self.numberOfPlayers = players
        self.gameTable = self.distribute_cards(self.numberOfPlayers)
        self.gameTableEdited = list(self.gameTable)
        self.voteArray = [0] * self.numberOfPlayers

    def distribute_cards(self, players):
        newGameTable = []
        newGameTable.append(Roles.SEER)
        newGameTable.append(Roles.THIEF)
        newGameTable.append(Roles.WEREWOLF)
        newGameTable.append(Roles.WEREWOLF)
        for i in range(players-2):
            newGameTable.append(Roles.VILLAGER)
        random.shuffle(newGameTable)
        return newGameTable
    def lookAtCard(self,tableNumber):
        return self.gameTable[tableNumber]
    def switchCard(self,myCard,otherCard):
        temp = self.gameTableEdited[otherCard]
        self.gameTableEdited[otherCard] = self.gameTableEdited[myCard]
        self.gameTableEdited[myCard] = temp
        return self.gameTableEdited[myCard]
    def leechCard(self, i):
        return self.gameTableEdited[i] == Roles.WEREWOLF
    def voteFor(self, voteTo, voter):
        print ColorTextExt(voter), voter, " votes ", voteTo, ColorTextExt.RESET
        self.voteArray[voter] = voteTo
    def countVote(self):
        lst = [0] * self.numberOfPlayers
        for i in self.voteArray:
            if i is not None:
                lst[i] = lst[i] + 1
            else:
                lst[random.randint(0, self.numberOfPlayers-1)]
        print ColorTextExt.PROPMTEXT,"The most vote is", lst.index(max(lst)), " who is ", self.gameTableEdited[lst.index(max(lst))].name, ColorTextExt.RESET
    def claimRole(self, role, claiming, claimedBy):
        print ColorTextExt(claimedBy), claimedBy, " claims ", claiming, " to be ", role.name, ColorTextExt.RESET
        newBlaim = Blaim(claimedBy, claiming, role)
        self.claimArray.append(newBlaim)
    def printCurretGame(self):
        print ColorTextExt.PROPMTEXT,"_", ColorTextExt.RESET
        for idx, role in enumerate(self.gameTable):
            print ColorTextExt(idx), idx, " is ", role.name, ColorTextExt.RESET

