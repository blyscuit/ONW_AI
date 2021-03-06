from PlayerAI import PlayerAgent, PlayerAI
from game import Roles, Game, ColorTextExt
import random
from action import Action, ActionType
class PlayerHuman(PlayerAgent):

    def lookOwnCard(self, playerObject):
        self.sureCard = [-1] * len(playerObject.gameObject.gameTable)
        self.sureCard[playerObject.playerID] = playerObject.myCard
    
    def useSkill(self, playerObject):
        #1 SEER
        #2 Thief
        #0 Wolf
        if playerObject.myCard == Roles.SEER:
            numbers = -1
            while(numbers <= 0 or numbers > playerObject.gameObject.numberOfPlayers+playerObject.gameObject.CENTER_NUMBER - 1):
                var = raw_input("You are SEER, look at number (1-"+ str(playerObject.gameObject.numberOfPlayers+playerObject.gameObject.CENTER_NUMBER - 1) +"): ")
                print ColorTextExt(0), "looking at", var, ColorTextExt.RESET
                try:
                    numbers = int(float(var))
                except ValueError:
                    numbers = -1
            randomCard = numbers
            # look at table
            if randomCard >= playerObject.gameObject.numberOfPlayers:
                for i in range(playerObject.gameObject.numberOfPlayers, playerObject.gameObject.numberOfPlayers+playerObject.gameObject.CENTER_NUMBER):
                    print ColorTextExt(0), i, "is", playerObject.gameObject.lookAtCard(i).name, ColorTextExt.RESET
            else:
                print ColorTextExt(0),randomCard, "is", playerObject.gameObject.lookAtCard(randomCard).name, ColorTextExt.RESET
        elif playerObject.myCard == Roles.THIEF:
            numbers = -1
            while(numbers < 0 or numbers > playerObject.gameObject.numberOfPlayers - 1):
                var = raw_input("You are THIEF, switch with number (0-" + str(playerObject.gameObject.numberOfPlayers-1) + "): ")
                print ColorTextExt(0), "switching with", var, ColorTextExt.RESET
                try:
                    numbers = int(float(var))
                except ValueError:
                    numbers = -1
            randomCard = numbers
            print ColorTextExt(0), "New role:", playerObject.gameObject.switchCard(playerObject.playerID, randomCard).name,ColorTextExt.RESET
        elif playerObject.myCard == Roles.WEREWOLF:
            print ColorTextExt(0), "You are WEREWOLF", ColorTextExt.RESET
            for i in range(0, playerObject.gameObject.numberOfPlayers):
                if playerObject.gameObject.gameTable[i] is Roles.WEREWOLF:
                    print ColorTextExt(0), i, "is WEREWOLF", ColorTextExt.RESET
        elif playerObject.myCard == Roles.VILLAGER:
            print ColorTextExt(0), "You are VILLAGER", ColorTextExt.RESET
    
        var = raw_input("Press ENTER to begin game")

class PlayerVoteHuman(PlayerAI):
    
    def lookOwnCard(self, playerObject):
        self.sureCard = [-1] * len(playerObject.gameObject.gameTable)
        self.sureCard[playerObject.playerID] = playerObject.myCard
    
    def useSkill(self, playerObject):
        #1 SEER
        #2 Thief
        #0 Wolf
        if playerObject.myCard == Roles.SEER:
            numbers = -1
            while(numbers <= 0 or numbers > playerObject.gameObject.numberOfPlayers+playerObject.gameObject.CENTER_NUMBER - 1):
                var = raw_input("You are SEER, look at number (1-"+ str(playerObject.gameObject.numberOfPlayers+playerObject.gameObject.CENTER_NUMBER - 1) +"): ")
                print ColorTextExt(0), "looking at", var, ColorTextExt.RESET
                try:
                    numbers = int(float(var))
                except ValueError:
                    numbers = -1
            randomCard = numbers
            # look at table
            if randomCard >= playerObject.gameObject.numberOfPlayers:
                for i in range(playerObject.gameObject.numberOfPlayers, playerObject.gameObject.numberOfPlayers+playerObject.gameObject.CENTER_NUMBER):
                    print ColorTextExt(0), i, "is", playerObject.gameObject.lookAtCard(i).name, ColorTextExt.RESET
            else:
                print ColorTextExt(0),randomCard, "is", playerObject.gameObject.lookAtCard(randomCard).name, ColorTextExt.RESET
            if randomCard >= playerObject.gameObject.numberOfPlayers:
                for i in range(playerObject.gameObject.numberOfPlayers, playerObject.gameObject.numberOfPlayers+playerObject.gameObject.CENTER_NUMBER):
                    self.sureCard[i] = playerObject.gameObject.lookAtCard(i)
                    playerObject.addAction(Action(playerObject.playerID, ActionType.LOOK, i, self.sureCard[i]))
                    playerObject.usedSkillOn = i
            else:
                self.sureCard[randomCard] = playerObject.gameObject.lookAtCard(randomCard)
                playerObject.addAction(Action(playerObject.playerID, ActionType.LOOK, randomCard, self.sureCard[randomCard]))
                playerObject.usedSkillOn = randomCard
        elif playerObject.myCard == Roles.THIEF:
            numbers = -1
            while(numbers < 0 or numbers > playerObject.gameObject.numberOfPlayers - 1):
                var = raw_input("You are THIEF, switch with number (0-" + str(playerObject.gameObject.numberOfPlayers-1) + "): ")
                print ColorTextExt(0), "switching with", var, ColorTextExt.RESET
                try:
                    numbers = int(float(var))
                except ValueError:
                    numbers = -1
            randomCard = numbers
            newcard = playerObject.gameObject.switchCard(playerObject.playerID, randomCard)
            print ColorTextExt(0), "New role:", newcard.name,ColorTextExt.RESET
            playerObject.addAction(Action(playerObject.playerID, ActionType.TRADE, randomCard, newcard, playerObject.myCard))
            self.sureCard[randomCard] = playerObject.myCard
            self.sureCard[playerObject.playerID] = newcard
            playerObject.myCard = newcard
            # playerObject.myFirstCard = Roles.WEREWOLF
            playerObject.usedSkillOn = randomCard
        elif playerObject.myCard == Roles.WEREWOLF:
            print ColorTextExt(0), "You are WEREWOLF", ColorTextExt.RESET
            for i in range(0, playerObject.gameObject.numberOfPlayers):
                if playerObject.gameObject.gameTable[i] is Roles.WEREWOLF:
                    print ColorTextExt(0), i, "is WEREWOLF", ColorTextExt.RESET
                    self.sureCard[i] = Roles.WEREWOLF
                    if i is not playerObject.playerID:
                        playerObject.usedSkillOn = i
        elif playerObject.myCard == Roles.VILLAGER:
            print ColorTextExt(0), "You are VILLAGER", ColorTextExt.RESET
    
        var = raw_input("Press ENTER to begin game") 
    
    def vote(self, playerObject):
        number = -1
        while number < 0 or number > playerObject.gameObject.numberOfPlayers - 1 or number == playerObject.playerID:
            print ColorTextExt.PROPMTEXT + "Vote to hang person (1-" + str(playerObject.gameObject.numberOfPlayers - 1) + "): " + ColorTextExt.RESET + "\n"
            var = raw_input()
            try:
                number = int(float(var))
                print "Entered", number
            except ValueError:
                print "Wrong format"
                number = -1
        playerObject.voteFor = number
    