from game import Roles, Game, ColorTextExt
import random
from action import Action, ActionType
#just the thinking
class PlayerAgent:
    nextTalk = 1.0
    sureCard = []
    personWeight = []
    cardWannaBe = Roles.VILLAGER
    # when lying own weight decrease
    def talkingLoop(self, playerObject, timeLeft) :
        pass
    
    def vote(self, playerObject):
        pass

    def claim(self, playerObject):
        pass
    def thinkAboutClaims(self, playerObject):
        pass
    def believingSeer(self, playerObject):
        pass
    def believingThief(self, playerObject):
        pass
        
        
class PlayerAI(PlayerAgent):
    def lookOwnCard(self, playerObject):
        self.sureCard = [Roles.UNKNOWN] * len(playerObject.gameObject.gameTable)
        self.sureCard[playerObject.playerID] = playerObject.myCard
        self.personWeight = [50] * playerObject.gameObject.numberOfPlayers
        self.personWeight[playerObject.playerID] = 100
    def vote(self, playerObject):
        # Random
        # numbers = range(playerObject.gameObject.numberOfPlayers)
        # numbers.remove(playerObject.playerID)
        # random.shuffle(numbers)
        # playerObject.voteFor = numbers.pop()

        #Believe everyone
        if self.sureCard[playerObject.playerID] != Roles.WEREWOLF:
            for claim in playerObject.gameObject.claimArray:
                if claim.role is Roles.WEREWOLF:
                    playerObject.voteFor = claim.claimed
                    return
        else:
            for idx, role in enumerate(self.sureCard):
                if role != Roles.WEREWOLF and role != Roles.UNKNOWN:
                    playerObject.voteFor = idx
                    return
        playerObject.voteFor = (playerObject.playerID + 1) % playerObject.gameObject.numberOfPlayers
    def claim(self, playerObject):
        #honest
        pass
        # playerObject.gameObject.claimRole(playerObject.myCard, playerObject.playerID, playerObject.playerID)
        # playerObject.addAction(Action(playerObject.playerID, ActionType.TRUTH, playerObject.playerID, playerObject.myCard))
    def claimSelf(self, playerObject, card, truth = False):
        playerObject.gameObject.claimRole(card, playerObject.playerID, playerObject.playerID)
        playerObject.addAction(Action(playerObject.playerID, ActionType.TRUTH if truth == True else ActionType.LIE, playerObject.playerID, card))
    def claimBeingSeer(self, playerObject, target, cardSaw, truth = False):
        playerObject.gameObject.claimRole(cardSaw, target, playerObject.playerID)
        playerObject.addAction(Action(playerObject.playerID, ActionType.TRUTH if truth == True else ActionType.LIE, target, cardSaw))
    def claimBeingThief(self, playerObject, target, cardGet, cardWas, truth = False):
        playerObject.gameObject.claimThief(cardGet, target, playerObject.playerID)
        playerObject.addAction(Action(playerObject.playerID, ActionType.TRUTH if truth == True else ActionType.LIE, target, cardWas))
        playerObject.addAction(Action(playerObject.playerID, ActionType.TRUTH if truth == True else ActionType.LIE, playerObject.playerID, cardGet))
        
    def useSkill(self, playerObject):
        #1 SEER
        #2 Thief
        #0 Wolf
        if playerObject.myFirstCard == Roles.SEER:
            numbers = range(playerObject.gameObject.numberOfPlayers)
            numbers.remove(playerObject.playerID)
            random.shuffle(numbers)
            randomCard = numbers.pop()
            # look at table
            if randomCard >= playerObject.gameObject.numberOfPlayers:
                for i in range(playerObject.gameObject.numberOfPlayers, playerObject.gameObject.numberOfPlayers+playerObject.gameObject.CENTER_NUMBER):
                    self.sureCard[i] = playerObject.gameObject.lookAtCard(i)
                    playerObject.addAction(Action(playerObject.playerID, ActionType.LOOK, i, self.sureCard[i]))
                    playerObject.usedSkillOn = i
            else:
                self.sureCard[randomCard] = playerObject.gameObject.lookAtCard(randomCard)
                playerObject.addAction(Action(playerObject.playerID, ActionType.LOOK, randomCard, self.sureCard[randomCard]))
                playerObject.usedSkillOn = randomCard
        elif playerObject.myFirstCard == Roles.THIEF:
            numbers = range(playerObject.gameObject.numberOfPlayers)
            numbers.remove(playerObject.playerID)
            random.shuffle(numbers)
            randomCard = numbers.pop()
            newcard = playerObject.gameObject.switchCard(playerObject.playerID, randomCard)
            playerObject.addAction(Action(playerObject.playerID, ActionType.TRADE, randomCard, newcard, playerObject.myCard))
            self.sureCard[randomCard] = playerObject.myCard
            self.sureCard[playerObject.playerID] = newcard
            playerObject.myCard = newcard
            playerObject.myFirstCard = Roles.WEREWOLF
            playerObject.usedSkillOn = randomCard
        elif playerObject.myFirstCard == Roles.WEREWOLF:
            roleArray = [Roles.VILLAGER, Roles.VILLAGER, Roles.THIEF, Roles.SEER]
            random.shuffle(roleArray)
            self.cardWannaBe = roleArray.pop()
            for i in range(0, playerObject.gameObject.numberOfPlayers):
                if playerObject.gameObject.gameTable[i] is Roles.WEREWOLF:
                    self.sureCard[i] = Roles.WEREWOLF
                    if i is not playerObject.playerID:
                        playerObject.usedSkillOn = i
                        self.personWeight[i] *= 2

    sayingTruthOnce = False

    def talkingLoop(self, playerObject, timeLeft) :
        if not self.sayingTruthOnce:
            self.sayingTruthOnce = True
            # if playerObject.myFirstCard == Roles.SEER:
            #     self.claimSelf(playerObject, Roles.SEER, True)
            #     self.claimBeingSeer(playerObject, playerObject.usedSkillOn, self.sureCard[playerObject.usedSkillOn], True)
            # elif playerObject.myFirstCard == Roles.THIEF:
            #     self.claimBeingThief(playerObject, playerObject.usedSkillOn, self.sureCard[playerObject.playerID], self.sureCard[playerObject.usedSkillOn], True)
            # elif playerObject.myFirstCard == Roles.VILLAGER:
            #     self.claimSelf(playerObject, Roles.VILLAGER, True)
            # elif playerObject.myFirstCard == Roles.WEREWOLF:
            #     playerObject.gameObject.claimRole(Roles.VILLAGER, playerObject.playerID, playerObject.playerID)
        self.lookAtRecentClaim(playerObject)
    
    def thinkAboutClaims(self, playerObject):
        noteSureCard = [None] * len(self.sureCard)
        for idx, role in enumerate(self.sureCard):
            if role != -1:
                noteSureCard[idx] = {'role': role, 'by': playerObject.playerID}
        
        for claim in playerObject.gameObject.claimArray:
            # print "claim", claim
            if noteSureCard[claim.claimed] != None and self.personWeight[claim.claimBy] >= self.personWeight[noteSureCard[claim.claimed]['by']]:
                noteSureCard[claim.claimed] = {'role': claim.role, 'by': claim.claimBy}
            elif noteSureCard[claim.claimed] == None:
                noteSureCard[claim.claimed] = {'role': claim.role, 'by': claim.claimBy}
        roleCount = [0] * Roles.roleCount
        for role in noteSureCard:
            if role != None and role["role"] != Roles.UNKNOWN:
                roleCount[role["role"].value] += 1
        if roleCount[Roles.WEREWOLF.value] > 2 or roleCount[Roles.THIEF.value] > 1 or roleCount[Roles.SEER.value] > 1 or roleCount[Roles.VILLAGER.value] > playerObject.gameObject.numberOfPlayers - playerObject.gameObject.CENTER_NUMBER:
            print ColorTextExt(playerObject.playerID), "something is WRONG!", ColorTextExt.RESET
    
    lastClaimLook = 0
    def lookAtRecentClaim(self, playerObject):
        currentClaim = len(playerObject.gameObject.claimArray)
        if self.lastClaimLook < currentClaim:
            self.lastClaimLook = currentClaim
            if playerObject.gameObject.claimArray:
                lastClaim = playerObject.gameObject.claimArray[-1]
                if playerObject.myFirstCard == Roles.WEREWOLF:
                    if not self.sayingTruthOnce and lastClaim.claimBy == playerObject.usedSkillOn:
                        roleArray = [Roles.VILLAGER, Roles.VILLAGER, Roles.THIEF, Roles.SEER]
                        roleArray.remove(lastClaim.role)
                        random.shuffle(roleArray)
                        self.cardWannaBe = roleArray.pop()
                        print ColorTextExt(playerObject.playerID), "Sure!", ColorTextExt.RESET
                if lastClaim.claimed == playerObject.playerID and lastClaim.claimBy != playerObject.playerID:
                    if playerObject.myFirstCard == Roles.WEREWOLF:
                        if lastClaim.role == self.cardWannaBe:
                            self.claimSelf(playerObject, lastClaim.role)
                            print ColorTextExt(playerObject.playerID), "Sure!", ColorTextExt.RESET
                        else:
                            self.claimSelf(playerObject, self.cardWannaBe)
                            print ColorTextExt(playerObject.playerID), "No I'm not!", ColorTextExt.RESET
                    else:
                        if lastClaim.role == playerObject.myFirstCard:
                            self.claimSelf(playerObject, lastClaim.role, True)
                            print ColorTextExt(playerObject.playerID), "Sure!", ColorTextExt.RESET
                        else:
                            self.claimSelf(playerObject, playerObject.myFirstCard, True)
                            print ColorTextExt(playerObject.playerID), "No I'm not!", ColorTextExt.RESET
            self.thinkAboutClaims(playerObject)
    
    def getSuccessor(self, playerObject):
        pass

    def believingSeer(self, playerObject):
        whoIsSeer = [0] * len(self.sureCard)
        claiming = [-1] * len(self.sureCard)
        hasOne = False
        for claim in playerObject.gameObject.claimArray:
            if claim.role == Roles.SEER:
                hasOne = True
                whoIsSeer[claim.claimed] = self.personWeight[claim.claimBy]
                claiming[claim.claimBy] = claim.claimed
        if hasOne:
            mostSeer = [i for i, x in enumerate(whoIsSeer) if x == max(whoIsSeer)]
            random.shuffle(mostSeer)
            mostSeer = claiming[mostSeer.pop()]
            self.sureCard[mostSeer] = Roles.SEER

    def believingThief(self, playerObject):
        whoIsThief = [-1] * len(self.sureCard)
        claiming = [-1] * len(self.sureCard)
        nextRole = [Roles.UNKNOWN] * len(self.sureCard)
        personGet = [None] * len(self.sureCard)
        hasOne = False
        for idx, claim in enumerate(playerObject.gameObject.claimArray):
            if claim.role == Roles.THIEF:
                if idx != 0 and playerObject.gameObject.claimArray[idx-1].claimBy == claim.claimBy and playerObject.gameObject.claimArray[idx-1].claimed == playerObject.gameObject.claimArray[idx-1].claimBy:
                    hasOne = True
                    thiefStoleClaim = playerObject.gameObject.claimArray[idx-1]
                    whoIsThief[thiefStoleClaim.claimed] = self.personWeight[claim.claimBy]
                    claiming[claim.claimBy] = claim.claimed
                    nextRole[claim.claimBy] = thiefStoleClaim.role
        if hasOne:
            mostThief = [i for i, x in enumerate(whoIsThief) if x == max(whoIsThief)]
            random.shuffle(mostThief)
            mostWasThief = claiming[mostThief.pop()]
            self.sureCard[mostWasThief] = nextRole[mostWasThief]
            self.sureCard[claiming[mostWasThief]] = Roles.THIEF
            print ColorTextExt(playerObject.playerID), mostWasThief, "was thief and should be", nextRole[mostWasThief].name, "from",claiming[mostWasThief], "'s" ,self.sureCard[claiming[mostWasThief]].name, ColorTextExt.RESET

    def getNextAction(self, playerObject):
        if playerObject.gameObject.numberOfPlayers == 3:
            playerObject.gameObject.claimRole(Roles.THIEF, playerObject.playerID, playerObject.playerID)
        elif playerObject.gameObject.numberOfPlayers >= 4:
            if playerObject.myFirstCard == Roles.THIEF:
                #random
                if self.sureCard[playerObject.playerID] == Roles.WEREWOLF:
                    pass
                else:
                    self.claimBeingThief(playerObject, playerObject.usedSkillOn, self.sureCard[playerObject.playerID], self.sureCard[playerObject.usedSkillOn], True)
            elif playerObject.myFirstCard == Roles.WEREWOLF:
                #another random
                pass
            elif playerObject.myFirstCard == Roles.SEER:
                self.claimBeingSeer(playerObject, playerObject.usedSkillOn, self.sureCard[playerObject.usedSkillOn], True)
                if playerObject.usedSkillOn >= playerObject.gameObject.numberOfPlayers:
                    anotherCard = playerObject.gameObject.numberOfPlayers+1 if playerObject.usedSkillOn == playerObject.gameObject.numberOfPlayers else playerObject.gameObject.numberOfPlayers
                    self.claimBeingSeer(playerObject, anotherCard, self.sureCard[anotherCard], True)
            else:
                playerObject.gameObject.claimRole(playerObject.myFirstCard, playerObject.playerID, playerObject.playerID)
        pass

    wolfHistory = -1
    def randomForWerewolf(self, playerObject):
        anotherWolf = self.getAnotherWolf(playerObject)
        if anotherWolf >= 0:
            #exist
            # self.seerAnotherWolf()
            #or
            pass
        else:
            #no another
            pass
        if self.wolfHistory <= -1:
            self.wolfHistory = 0
        for i in range(self.wolfHistory, len(playerObject.gameObject.claimArray)):
            if playerObject.gameObject.claimArray[i].role == Roles.THIEF or playerObject.gameObject.claimArray[i].role == Roles.SEER:
                pass

    wolfApproach = None

    def lieSeerAnotherWolf(self, playerObject):
        #pass only playerObject
        #this funciton takes care of the person and role
        another = self.getAnotherWolf(playerObject)
        roleArray = [Roles.THIEF, Roles.VILLAGER, Roles.VILLAGER]
        random.shuffle(roleArray)
        self.cardWannaBe = Roles.SEER
        self.claimSelf(playerObject, Roles.SEER)
        self.claimBeingSeer(playerObject, another, roleArray.pop())
    def lieSeerRandomCardWerewolf(self, playerObject):
        #pass only playerObject
        #this funciton takes care of the person and role
        self.cardWannaBe = Roles.SEER
        person = range(0, playerObject.gameObject.numberOfPlayers)
        person.remove(playerObject.playerID)
        random.shuffle(person)
        person = person.pop()
        self.claimSelf(playerObject, Roles.SEER)
        self.claimBeingSeer(playerObject, person, Roles.WEREWOLF)
    def lieSeerRandomCardThief(self, playerObject):
        #pass only playerObject
        #this funciton takes care of the person and role
        self.cardWannaBe = Roles.SEER
        person = range(0, playerObject.gameObject.numberOfPlayers)
        person.remove(playerObject.playerID)
        random.shuffle(person)
        person = person.pop()
        self.claimSelf(playerObject, Roles.SEER)
        self.claimBeingSeer(playerObject, person, Roles.THIEF)
    def wolfLieSeerMiddle(self, playerObject):
        self.cardWannaBe = Roles.SEER
        self.claimSelf(playerObject, Roles.SEER)
        randomMid = range(playerObject.gameObject.numberOfPlayers+1, playerObject.gameObject.numberOfPlayers + playerObject.gameObject.CENTER_NUMBER)
        random.shuffle(randomMid)
        roleArray = [Roles.WEREWOLF, Roles.VILLAGER, Roles.VILLAGER, Roles.WEREWOLF, Roles.VILLAGER]
        random.shuffle(roleArray)
        while randomMid:
            nextMid = randomMid.pop()
            nextRole = roleArray.pop()
            self.claimBeingSeer(playerObject, nextMid, nextRole)
    def thiefLieSeerMiddle(self, playerObject):
        self.cardWannaBe = Roles.SEER
        self.claimSelf(playerObject, Roles.SEER)
        randomMid = range(playerObject.gameObject.numberOfPlayers+1, playerObject.gameObject.numberOfPlayers + playerObject.gameObject.CENTER_NUMBER)
        random.shuffle(randomMid)
        roleArray = [Roles.WEREWOLF, Roles.VILLAGER, Roles.VILLAGER, Roles.WEREWOLF, Roles.VILLAGER, Roles.THIEF]
        random.shuffle(roleArray)
        while randomMid:
            nextMid = randomMid.pop()
            nextRole = roleArray.pop()
            self.claimBeingSeer(playerObject, nextMid, nextRole)
    def lieThiefSelf(self, playerObject):
        self.cardWannaBe = Roles.THIEF
        self.claimBeingThief(playerObject, playerObject.playerID, Roles.THIEF, playerObject.playerID)
    def lieVillage(self, playerObject):
        self.cardWannaBe = Roles.VILLAGER
        self.claimSelf(playerObject, Roles.VILLAGER)

    def getAnotherWolf(self, playerObject):
        for idx, card in enumerate(self.sureCard):
            if card is Roles.WEREWOLF and idx != playerObject.playerID:
                return idx
        return -1