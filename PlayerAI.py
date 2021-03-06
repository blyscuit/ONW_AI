from game import Roles, Game, ColorTextExt
import math
import random
from action import Action, ActionType
import itertools
from util import perm_unique, permute_unique
#just the thinking
class PlayerAgent:
    nextTalk = 1.0
    sureCard = []
    thinkingCard = []
    personWeight = []
    cardWannaBe = Roles.VILLAGER
    wasThiefBy = None
    # when lying own weight decrease
    def talkingLoop(self, playerObject, talkedNum, totalTalkTime, currentGameTime, intervalTime) :
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
    def lookAtRecentClaim(self, playerObject):
        pass
        
class PlayerAI(PlayerAgent):
    LastTalkTime = 0
    def decideWhetherToTalk(self, talkedNum, totalTalkTime, currentGameTime, intervalTime):
        prob = 0.1 #TODO calculate this according to RoleLogic
        #              probability, startVal, endVal ,talkNum,endTime, time, timeRate, lastTalkTime
        x = self.geometricProbability(prob, 0.15, 0.8, talkedNum , totalTalkTime, currentGameTime, intervalTime, self.LastTalkTime)
        y = random.random()
        if(y<x):
            self.LastTalkTime = currentGameTime
            return True
        else:
            return False
    allCorrectCombination = []
    def lookOwnCard(self, playerObject):
        self.allCorrectCombination = self.generateAllPossibility(playerObject)
        self.sureCard = [Roles.UNKNOWN] * len(playerObject.gameObject.gameTable)
        self.sureCard[playerObject.playerID] = playerObject.myCard
        self.personWeight = [30] * playerObject.gameObject.numberOfPlayers
        self.personWeight[playerObject.playerID] = 100
    def vote(self, playerObject):
        # Random
        # numbers = range(playerObject.gameObject.numberOfPlayers)
        # numbers.remove(playerObject.playerID)
        # random.shuffle(numbers)
        # playerObject.voteFor = numbers.pop()

        #Believe everyone
        # self.believingSeer(playerObject)
        # self.believingThief(playerObject)
        # self.believingWolf(playerObject)
        self.thinkAboutClaims(playerObject)
        # print ColorTextExt(playerObject.playerID), 'Remove', [ [y.name for y in x] for x in self.allCorrectCombination], ColorTextExt.RESET
        # if playerObject.myCard != Roles.WEREWOLF:
        if self.sureCard[playerObject.playerID] != Roles.WEREWOLF:
        
            self.countPossibility(playerObject)
        
            # for idx, role in enumerate(self.sureCard):
            #     if role is Roles.WEREWOLF:
            #         playerObject.voteFor = idx
            #         return
        else:
            self.countWolfPossibility(playerObject)
            # for idx, role in enumerate(self.sureCard):
            #     if role != Roles.WEREWOLF and role != Roles.UNKNOWN:
            #         playerObject.voteFor = idx
            #         return
        self.countNoWolf(playerObject)
        # playerObject.voteFor = (playerObject.playerID + 1) % playerObject.gameObject.numberOfPlayers
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
            # playerObject.myFirstCard = Roles.WEREWOLF
            playerObject.usedSkillOn = randomCard
        elif playerObject.myFirstCard == Roles.WEREWOLF:
            roleArray = self.listOfNotClaimCards(playerObject)
            filter(lambda a: a != Roles.WEREWOLF, roleArray)
            random.shuffle(roleArray)
            self.cardWannaBe = roleArray.pop()
            for i in range(0, playerObject.gameObject.numberOfPlayers):
                if playerObject.gameObject.gameTable[i] is Roles.WEREWOLF:
                    self.sureCard[i] = Roles.WEREWOLF
                    if i is not playerObject.playerID:
                        playerObject.usedSkillOn = i
                        self.personWeight[i] *= 2

    sayingTruthOnce = False

    talkingSequence = 0

    def talkWithSequence(self, playerObject, sequence):
        # 'talk'
        if playerObject.myFirstCard == Roles.SEER:
            maxSequence = 1
            if sequence == 0:
                self.claimSelf(playerObject, Roles.SEER, True)
            elif sequence == 1:
                self.claimBeingSeer(playerObject, playerObject.usedSkillOn, self.sureCard[playerObject.usedSkillOn], True)
                if playerObject.usedSkillOn >= playerObject.gameObject.numberOfPlayers:
                    anotherCard = playerObject.gameObject.numberOfPlayers+1 if playerObject.usedSkillOn == playerObject.gameObject.numberOfPlayers else playerObject.gameObject.numberOfPlayers
                    self.claimBeingSeer(playerObject, anotherCard, self.sureCard[anotherCard], True)
            else:
                self.talkWithSequence(playerObject, random.randint(0,maxSequence))
        elif playerObject.myFirstCard == Roles.THIEF and playerObject.myCard != Roles.WEREWOLF:
            maxSequence = 0
            if sequence == 0:
                self.claimBeingThief(playerObject, playerObject.usedSkillOn, self.sureCard[playerObject.playerID], self.sureCard[playerObject.usedSkillOn], True)
            else:
                self.talkWithSequence(playerObject, random.randint(0,maxSequence))
        elif playerObject.myFirstCard == Roles.VILLAGER:
            maxSequence = 0
            if sequence == 0:
                self.claimSelf(playerObject, Roles.VILLAGER, True)
            else:
                self.talkWithSequence(playerObject, random.randint(0,maxSequence))
        elif playerObject.myFirstCard == Roles.WEREWOLF or (playerObject.myFirstCard == Roles.THIEF and playerObject.myCard == Roles.WEREWOLF):
            if sequence == 0 and not self.wolfWasSeer:
                self.wolfApproach = self.randomForWerewolf(playerObject)
                self.wolfPop = self.wolfApproach(playerObject, sequence, self.wolfPop)
            elif sequence == 0 and self.wolfWasSeer:
                self.wolfApproach = self.randomForWerewolfForRole(playerObject, self.cardWannaBe)
                self.wolfPop = self.wolfApproach(playerObject, sequence, self.wolfPop)
            else:
                self.wolfPop = self.wolfApproach(playerObject, sequence, self.wolfPop)
        return sequence+1
                
    def talkingLoop(self, playerObject, talkedNum, totalTalkTime, currentGameTime, intervalTime):
        didTalk = False
        willTalk = self.decideWhetherToTalk(talkedNum, totalTalkTime, currentGameTime, intervalTime)
        self.lookAtRecentClaim(playerObject)
        if willTalk :
            self.talkingSequence = self.talkWithSequence(playerObject, self.talkingSequence)
            didTalk = True
        return didTalk
    
    def thinkAboutClaims(self, playerObject):
        # possibleRole = []
        # for i in range(playerObject.gameObject.numberOfPlayers):
        #     possibleRole.append([Roles.WEREWOLF])
        #     if i == playerObject.playerID and playerObject.myFirstCard == Roles.WEREWOLF:
        #         possibleRole[i].append([Roles.THIEF])
        # possibleRole[playerObject.playerID].append(playerObject.myFirstCard)
        # otherClaimsPossible = []
        # for claim in playerObject.gameObject.claimArray:
        #     if claim.claimBy == claim.claimed and (claim.role.cardCount > 1 or (claim.role != playerObject.myFirstCard)):
        #         possibleRole[claim.claimed].append(claim.role)
        #     else:
        #         otherClaimsPossible.append(claim)
        # for otherClaim in otherClaimsPossible:
        #     if claim.claimed == playerObject.playerID:
        #             # remove seer and thief if guest not correct, should do this at the end
        #             if claim.role != playerObject.myFirstCard:
        #                 filter(lambda a: a != Roles.SEER, possibleRole[claim.claimBy])
        #                 filter(lambda a: a != Roles.THIEF, possibleRole[claim.claimBy])

        # 'thinking'

        self.allCorrectCombination = self.generateAllPossibility(playerObject)

        newCombination = list(self.allCorrectCombination)
        for possibility in self.allCorrectCombination:
            if playerObject.myFirstCard == Roles.THIEF:
                if possibility[playerObject.usedSkillOn] != playerObject.myCard:
                    newCombination.remove(possibility)
                    continue
            if possibility[playerObject.playerID] != playerObject.myFirstCard:
                newCombination.remove(possibility)
                continue
            theyDidClaimSelf = [[Roles.UNKNOWN]] * (playerObject.gameObject.numberOfPlayers)
            assumingGoodRole = []
            theyDidClaimOther = []
            centerClaim = [Roles.UNKNOWN] * playerObject.gameObject.CENTER_NUMBER
            myClaimOther = [[Roles.UNKNOWN]] * (playerObject.gameObject.numberOfPlayers)
            for play in range(playerObject.gameObject.numberOfPlayers):
                theyDidClaimOther.append([[Roles.UNKNOWN]] * (playerObject.gameObject.numberOfPlayers))
            for role in possibility:
                if role.win == Roles.WEREWOLF.win:
                    assumingGoodRole.append(False)
                else:
                    assumingGoodRole.append(True)
            for claim in playerObject.gameObject.claimArray:
                if claim.claimed >= playerObject.gameObject.numberOfPlayers or role != Roles.SEER:
                    continue
                if playerObject.playerID == claim.claimBy:
                    if assumingGoodRole[claim.claimBy] == True:
                        myClaimOther[claim.claimed] = [claim.role]
                    else:
                        myClaimOther[claim.claimed] = Roles.inverseRole(claim.role)
                else:
                    if claim.claimed == claim.claimBy:
                        if assumingGoodRole[claim.claimBy] == True:
                            theyDidClaimSelf[claim.claimBy] = [claim.role]
                        else:
                            theyDidClaimSelf[claim.claimBy] = Roles.inverseRole(claim.role)
                    else:
                        if role == Roles.SEER and claim.claimed>=playerObject.gameObject.numberOfPlayers:
                            centerClaim[(claim.claimed-playerObject.gameObject.numberOfPlayers)] = claim.role
                        else:#if claim.claimBy < playerObject.gameObject.numberOfPlayers or claim.claimed < playerObject.gameObject.numberOfPlayers:
                            if assumingGoodRole[claim.claimBy] == True:
                                theyDidClaimOther[claim.claimBy][claim.claimed] = [claim.role]
                            else:
                                # theyDidClaimOther[claim.claimBy][claim.claimed] = Roles.inverseRole(claim.role)
                                theyDidClaimOther[claim.claimBy][claim.claimed] = [Roles.UNKNOWN]
            
            possible = True
            for idx, role in enumerate(possibility):
                if (role not in theyDidClaimSelf[idx] and Roles.UNKNOWN not in theyDidClaimSelf[idx]) or (role not in myClaimOther[idx] and Roles.UNKNOWN not in myClaimOther[idx]):
                    possible = False
                    break
                else:
                    for insideOther in theyDidClaimOther:
                        insideIndexOther = insideOther[idx]
                        if role not in insideIndexOther and Roles.UNKNOWN not in insideIndexOther:
                            possible = False
                            break
                if role == Roles.SEER:
                    roleCount = [0] * Roles.roleCount
                    for roleIn in possibility:
                        roleCount[abs(roleIn.value)] += 1
                    for roleInMid in centerClaim:
                        roleCount[roleInMid.value] += 1
                    if roleCount[Roles.WEREWOLF.value] > 2 or roleCount[Roles.THIEF.value] > 1 or roleCount[Roles.SEER.value] > 1 or roleCount[Roles.VILLAGER.value] > playerObject.gameObject.numberOfPlayers - playerObject.gameObject.CENTER_NUMBER:
                        possible = False
            if possible == False:
                newCombination.remove(possibility)
        # if playerObject.myFirstCard != Roles.WEREWOLF:
        self.allCorrectCombination = newCombination
        self.countNoWolf(playerObject)

        # noteSureCard = [None] * len(self.sureCard)
        # noteSureCard = [None] * len(self.sureCard)
        # lastSeerClaim = None
        # lastThiefClaim = None
        # seerInfoClaim = None
        # thiefInfoClaim = None

        # alreadyBelieveSeer = False
        # alreadyBelieveThief = False
        

        # claimCount = [0] * playerObject.gameObject.numberOfPlayers
        # for idx, role in enumerate(self.sureCard):
        #     if role != -1:
        #         noteSureCard[idx] = {'role': role, 'by': playerObject.playerID}
        
        # for idx, claim in enumerate(playerObject.gameObject.claimArray):
        #     # if claim.claimBy != claim.claimed:
        #     #     claimCount[claim.claimBy] += 1
        #     # if claim.role == Roles.SEER and claim.claimBy == claim.claimed:
        #     #     lastSeerClaim = claim
        #     # if claim.role == Roles.THIEF and claim.claimed == playerObject.playerID:
        #     #     lastThiefClaim = claim
        #     #     try:
        #     #         lastClaim = playerObject.gameObject.claimArray[idx-1]
        #     #         if lastClaim = 
        #     # if lastSeerClaim and claim.claimBy == lastSeerClaim.claimed and claim.claimed != lastSeerClaim.claimed:
        #     #     seerInfoClaim = claim
        #     # if seerInfoClaim and claim.claimBy == seerInfoClaim.claimed and claim.role == seerInfoClaim.role:
        #     #     noteSureCard[lastSeerClaim.claimBy] = 60 - claimCount[lastSeerClaim.claimBy]/3
        #     # if claim.role == playerObject.myFirstCard and lastSeerClaim.claimBy == claim.claimBy and claim.claimed == playerObject.playerID:
        #     #     noteSureCard[lastSeerClaim.claimBy] = 70 - claimCount[lastSeerClaim.claimBy]/3

        #     # print "claim", claim
        #     if noteSureCard[claim.claimed] != None and self.personWeight[claim.claimBy] >= self.personWeight[noteSureCard[claim.claimed]['by']]:
        #         noteSureCard[claim.claimed] = {'role': claim.role, 'by': claim.claimBy}
        #     elif noteSureCard[claim.claimed] == None:
        #         noteSureCard[claim.claimed] = {'role': claim.role, 'by': claim.claimBy}
        # roleCount = [0] * Roles.roleCount
        # for role in noteSureCard:
        #     if role != None and role["role"] != Roles.UNKNOWN:
        #         roleCount[role["role"].value] += 1
        # if roleCount[Roles.WEREWOLF.value] > 2 or roleCount[Roles.THIEF.value] > 1 or roleCount[Roles.SEER.value] > 1 or roleCount[Roles.VILLAGER.value] > playerObject.gameObject.numberOfPlayers - playerObject.gameObject.CENTER_NUMBER:
        #     print ColorTextExt(playerObject.playerID), "something is WRONG!", ColorTextExt.RESET
    def countNoWolf(self, playerObject):
        countWolf = [0] * playerObject.gameObject.numberOfPlayers
        for possibility in self.allCorrectCombination:
            if Roles.BAD_THIEF in possibility:
                countWolf[possibility.index(Roles.BAD_THIEF)] += 1
            else:
                for idx, role in enumerate(possibility):
                    if role == Roles.WEREWOLF:
                        countWolf[idx] += 1
        maxWolf = max(countWolf)
        # if maxWolf <= playerObject.gameObject.numberOfPlayers-3:
        if maxWolf <= 2:
            if playerObject.myFirstCard != Roles.WEREWOLF:
                playerObject.voteFor = (playerObject.playerID + 1) % playerObject.gameObject.numberOfPlayers
            # print ColorTextExt(playerObject.playerID), "There might be no wolf.", ColorTextExt.RESET 
    
    def countPossibility(self, playerObject):
        countWolf = [0] * playerObject.gameObject.numberOfPlayers
        for possibility in self.allCorrectCombination:
            if Roles.BAD_THIEF in possibility:
                countWolf[possibility.index(Roles.BAD_THIEF)] += 1
            else:
                for idx, role in enumerate(possibility):
                    if role == Roles.WEREWOLF and idx != playerObject.playerID:
                        countWolf[idx] += 1
        mostWolf = [i for i, x in enumerate(countWolf) if x == max(countWolf)]
        if playerObject.playerID in mostWolf:
            mostWolf.remove(playerObject.playerID)
        random.shuffle(mostWolf)
        if mostWolf:
            mostWolf = mostWolf.pop()
            playerObject.voteFor = mostWolf
    
    def countWolfPossibility(self, playerObject):
        countBadThief = [0] * playerObject.gameObject.numberOfPlayers
        countWolf = [0] * playerObject.gameObject.numberOfPlayers
        for possibility in self.allCorrectCombination:
            if Roles.BAD_THIEF in possibility and possibility.index(Roles.BAD_THIEF) != playerObject.playerID:
                countBadThief[possibility.index(Roles.BAD_THIEF)] += 1
            else:
                for idx, role in enumerate(possibility):
                    if role == Roles.WEREWOLF and idx != playerObject.playerID:
                        countWolf[idx] += 1
        shouldVote = range(playerObject.gameObject.numberOfPlayers)
        shouldVote.remove(playerObject.playerID)
        if max(countBadThief) > max(countWolf) and random.random() <  (float(max(countBadThief))/float((max(countBadThief) + max(countWolf)))) :
            mostWolf = [i for i, x in enumerate(countBadThief) if x == max(countBadThief)]
            random.shuffle(mostWolf)
            mostWolf = mostWolf.pop()
            playerObject.voteFor = mostWolf
        else:
            random.shuffle(shouldVote)
            mostWolf = [i for i, x in enumerate(countWolf) if x == max(countWolf)]
            if len(mostWolf) >= playerObject.gameObject.numberOfPlayers - 1:
                playerObject.voteFor = shouldVote.pop()
                return
            
            # print ColorTextExt(playerObject.playerIDw), max(countWolf), 'Remove', mostWolf, ColorTextExt.RESET
            for most in mostWolf:
                shouldVote.remove(most)
            mostNotWolf = shouldVote.pop()
            playerObject.voteFor = mostNotWolf

    wolfWasSeer = False
    lastClaimLook = 0
    def lookAtRecentClaim(self, playerObject):
        currentClaim = len(playerObject.gameObject.claimArray)
        if self.lastClaimLook < currentClaim:
            self.lastClaimLook = currentClaim
            if playerObject.gameObject.claimArray:
                lastClaim = playerObject.gameObject.claimArray[-1]
                if playerObject.myFirstCard == Roles.WEREWOLF:
                    if not self.talkingSequence<=0 and lastClaim.claimBy == playerObject.usedSkillOn:
                        roleArray = self.listOfNotClaimCards(playerObject)
                        filter(lambda a: a != Roles.WEREWOLF, roleArray)
                        random.shuffle(roleArray)
                        self.cardWannaBe = roleArray.pop()
                if lastClaim.claimed == playerObject.playerID and lastClaim.claimBy != playerObject.playerID:
                    if playerObject.myFirstCard == Roles.WEREWOLF:
                        self.wolfWasSeer = True
                        if lastClaim.role == self.cardWannaBe:
                            self.claimSelf(playerObject, lastClaim.role)
                            # print ColorTextExt(playerObject.playerID), "Sure!", ColorTextExt.RESET
                        else:
                            print ColorTextExt(playerObject.playerID), "No I'm not!", ColorTextExt.RESET
                            self.claimSelf(playerObject, self.cardWannaBe)
                    else:
                        if lastClaim.role == playerObject.myFirstCard:
                            self.claimSelf(playerObject, lastClaim.role, True)
                            # print ColorTextExt(playerObject.playerID), "Sure!", ColorTextExt.RESET
                        else:
                            print ColorTextExt(playerObject.playerID), "No I'm not!", ColorTextExt.RESET
                            self.claimSelf(playerObject, playerObject.myFirstCard, True)
            self.thinkAboutClaims(playerObject)
    
    def getSuccessor(self, playerObject):
        pass

    # def believingSeer(self, playerObject):
    #     whoIsSeer = [0] * len(self.sureCard)
    #     claiming = [-1] * len(self.sureCard)
    #     hasOne = False
    #     for claim in playerObject.gameObject.claimArray:
    #         if claim.role == Roles.SEER:
    #             hasOne = True
    #             whoIsSeer[claim.claimed] = self.personWeight[claim.claimBy]
    #             claiming[claim.claimBy] = claim.claimed
    #     if hasOne:
    #         mostSeer = [i for i, x in enumerate(whoIsSeer) if x == max(whoIsSeer)]
    #         random.shuffle(mostSeer)
    #         mostSeer = claiming[mostSeer.pop()]
    #         self.sureCard[mostSeer] = Roles.SEER
    #         if self.personWeight[mostSeer] < self.personWeight[playerObject.playerID] - 20:
    #             self.personWeight[mostSeer] += 20

    # def believingWolf(self, playerObject):
    #     whoIsSeer = [0] * len(self.sureCard)
    #     claiming = [-1] * len(self.sureCard)
    #     hasOne = False
    #     for claim in playerObject.gameObject.claimArray:
    #         if claim.role == Roles.WEREWOLF:
    #             hasOne = True
    #             whoIsSeer[claim.claimed] = self.personWeight[claim.claimBy]
    #             claiming[claim.claimBy] = claim.claimed
    #     if hasOne:
    #         mostSeer = [i for i, x in enumerate(whoIsSeer) if x == max(whoIsSeer)]
    #         random.shuffle(mostSeer)
    #         mostSeer = claiming[mostSeer.pop()]
    #         self.sureCard[mostSeer] = Roles.WEREWOLF
    #     else:
    #         self.sureCard[self.personWeight.index(min(self.personWeight))] = Roles.WEREWOLF

    # def believingThief(self, playerObject):
    #     whoIsThief = [-1] * len(self.sureCard)
    #     claiming = [-1] * len(self.sureCard)
    #     nextRole = [Roles.UNKNOWN] * len(self.sureCard)
    #     personGet = [None] * len(self.sureCard)
    #     hasOne = False
    #     for idx, claim in enumerate(playerObject.gameObject.claimArray):
    #         if claim.role == Roles.THIEF:
    #             if idx != 0 and playerObject.gameObject.claimArray[idx-1].claimBy == claim.claimBy and playerObject.gameObject.claimArray[idx-1].claimed == playerObject.gameObject.claimArray[idx-1].claimBy:
    #                 hasOne = True
    #                 thiefStoleClaim = playerObject.gameObject.claimArray[idx-1]
    #                 whoIsThief[thiefStoleClaim.claimed] = self.personWeight[claim.claimBy]
    #                 claiming[claim.claimBy] = claim.claimed
    #                 nextRole[claim.claimBy] = thiefStoleClaim.role
    #     if hasOne:
    #         mostThief = [i for i, x in enumerate(whoIsThief) if x == max(whoIsThief)]
    #         random.shuffle(mostThief)
    #         mostWasThief = claiming[mostThief.pop()]
    #         self.sureCard[mostWasThief] = nextRole[mostWasThief]
    #         self.sureCard[claiming[mostWasThief]] = Roles.THIEF
    #         if self.personWeight[mostSeer] < self.personWeight[playerObject.playerID] - 5:
    #             self.personWeight[mostSeer] += 5
    #         print ColorTextExt(playerObject.playerID), mostWasThief, "was thief and should be", nextRole[mostWasThief].name, "from",claiming[mostWasThief], "'s" ,self.sureCard[claiming[mostWasThief]].name, ColorTextExt.RESET

    # def getNextAction(self, playerObject):
    #     if playerObject.gameObject.numberOfPlayers == 3:
    #         playerObject.gameObject.claimRole(Roles.THIEF, playerObject.playerID, playerObject.playerID)
    #     elif playerObject.gameObject.numberOfPlayers >= 4:
    #         if playerObject.myFirstCard == Roles.THIEF:
    #             #random
    #             if self.sureCard[playerObject.playerID] == Roles.WEREWOLF:
    #                 pass
    #             else:
    #                 self.claimBeingThief(playerObject, playerObject.usedSkillOn, self.sureCard[playerObject.playerID], self.sureCard[playerObject.usedSkillOn], True)
    #         elif playerObject.myFirstCard == Roles.WEREWOLF:
    #             #another random
    #             pass
    #         elif playerObject.myFirstCard == Roles.SEER:
    #             self.claimBeingSeer(playerObject, playerObject.usedSkillOn, self.sureCard[playerObject.usedSkillOn], True)
    #             if playerObject.usedSkillOn >= playerObject.gameObject.numberOfPlayers:
    #                 anotherCard = playerObject.gameObject.numberOfPlayers+1 if playerObject.usedSkillOn == playerObject.gameObject.numberOfPlayers else playerObject.gameObject.numberOfPlayers
    #                 self.claimBeingSeer(playerObject, anotherCard, self.sureCard[anotherCard], True)
    #         else:
    #             playerObject.gameObject.claimRole(playerObject.myFirstCard, playerObject.playerID, playerObject.playerID)
    #     pass

    def randomForWerewolf(self, playerObject):
        anotherWolf = self.getAnotherWolf(playerObject)
        actionList = [self.lieSeerRandomCardWerewolf, self.lieSeerRandomCardThief, self.lieVillage, self.lieThiefSelf]
        if anotherWolf >= 0:
            #exist
            actionList.append(self.lieSeerAnotherWolf)
            # self.seerAnotherWolf()
            #or
            pass
        else:
            #no another
            pass
        if playerObject.myFirstCard == Roles.THIEF:
            actionList.append(self.wolfLieSeerMiddle)
        if playerObject.myFirstCard == Roles.THIEF:
            actionList.append(self.thiefLieSeerMiddle)
        random.shuffle(actionList)
        return actionList.pop()

    def randomForWerewolfForRole(self, playerObject, role):
        anotherWolf = self.getAnotherWolf(playerObject)
        actionList = []
        if role == Roles.VILLAGER:
            actionList = [self.lieVillage]
        elif role == Roles.THIEF:
            actionList = [self.lieThiefSelf]
        elif role == Roles.SEER:
            actionList = [self.lieSeerRandomCardWerewolf, self.lieSeerRandomCardThief]
        if anotherWolf >= 0 and role == Roles.SEER:
            #exist
            actionList.append(self.lieSeerAnotherWolf)
            # self.seerAnotherWolf()
            #or
            pass
        else:
            #no another
            pass
        if playerObject.myFirstCard == Roles.THIEF:
            actionList.append(self.thiefLieSeerMiddle)
        random.shuffle(actionList)
        return actionList.pop()

    wolfApproach = None
    wolfPop = None
    def lieSeerAnotherWolf(self, playerObject, sequ , popping = None):
        #pass only playerObject
        #this funciton takes care of the person and role
        another = self.getAnotherWolf(playerObject)
        roleTarget = None
        if popping:
            roleTarget = popping.pop()
        else:
            roleArray = [Roles.THIEF, Roles.VILLAGER, Roles.VILLAGER]
            random.shuffle(roleArray)
            roleTarget = roleArray.pop()
        maxSeq = 2
        if sequ >= maxSeq:
            sequ = random.randint(1, maxSeq)
        if sequ == 0:
            self.cardWannaBe = Roles.SEER
            self.claimSelf(playerObject, Roles.SEER)
        elif sequ == 1:
            self.claimBeingSeer(playerObject, another, roleTarget)
        elif sequ == 2:
            self.claimSelf(playerObject, Roles.SEER)
        return [roleTarget]
    def lieSeerRandomCardWerewolf(self, playerObject, sequ, popping = None):
        #pass only playerObject
        #this funciton takes care of the person and role
        person = None
        if popping:
            person = popping.pop()
        else:
            person = range(0, playerObject.gameObject.numberOfPlayers)
            person.remove(playerObject.playerID)
            random.shuffle(person)
            person = person.pop()
        
        maxSeq = 2
        if sequ >= maxSeq:
            sequ = random.randint(1, maxSeq)
        if sequ == 0:
            self.cardWannaBe = Roles.SEER
            self.claimSelf(playerObject, Roles.SEER)
        elif sequ == 1:
            self.claimBeingSeer(playerObject, person, Roles.WEREWOLF)
        elif sequ == 2:
            self.claimSelf(playerObject, Roles.SEER)
        return [person]
    def lieSeerRandomCardThief(self, playerObject, sequ, popping = None):
        #pass only playerObject
        #this funciton takes care of the person and role
        person = None
        if popping:
            person = popping.pop()
        else:
            person = range(0, playerObject.gameObject.numberOfPlayers)
            person.remove(playerObject.playerID)
            random.shuffle(person)
            person = person.pop()
        maxSeq = 2
        if sequ >= maxSeq:
            sequ = random.randint(1, maxSeq)
        if sequ == 0:
            self.cardWannaBe = Roles.SEER
            self.claimSelf(playerObject, Roles.SEER)
        elif sequ == 1:
            self.claimBeingSeer(playerObject, person, Roles.THIEF)
        elif sequ == 2:
            self.claimSelf(playerObject, Roles.SEER)
        return [person]
    def wolfLieSeerMiddle(self, playerObject, sequ, popping = None):
        randomMid = []
        roleArray = []
        if popping:
            for tup in popping:
                randomMid.append(tup[0])
                roleArray.append(tup[1])
        else:
            randomMid = range(playerObject.gameObject.numberOfPlayers+1, playerObject.gameObject.numberOfPlayers + playerObject.gameObject.CENTER_NUMBER)
            random.shuffle(randomMid)
            roleArray = [Roles.WEREWOLF, Roles.VILLAGER, Roles.VILLAGER, Roles.WEREWOLF, Roles.VILLAGER]
            random.shuffle(roleArray)

        maxSeq = 2
        if sequ >= maxSeq:
            sequ = random.randint(1, maxSeq)
        if sequ == 0:
            self.cardWannaBe = Roles.SEER
            self.claimSelf(playerObject, Roles.SEER)
        elif sequ == 2:
            self.claimSelf(playerObject, Roles.SEER)

        shouldPop = []
        while randomMid:
            nextMid = randomMid.pop()
            nextRole = roleArray.pop()
            shouldPop.append((nextMid,nextRole))
            if sequ == 1:
                self.claimBeingSeer(playerObject, nextMid, nextRole)
        return shouldPop
    def thiefLieSeerMiddle(self, playerObject, sequ, popping = None):
        randomMid = []
        roleArray = []
        if popping:
            for tup in popping:
                randomMid.append(tup[0])
                roleArray.append(tup[1])
        else:
            randomMid = range(playerObject.gameObject.numberOfPlayers+1, playerObject.gameObject.numberOfPlayers + playerObject.gameObject.CENTER_NUMBER)
            random.shuffle(randomMid)
            roleArray = [Roles.WEREWOLF, Roles.VILLAGER, Roles.VILLAGER, Roles.WEREWOLF, Roles.VILLAGER, Roles.THIEF]
            random.shuffle(roleArray)
            
        maxSeq = 2
        if sequ >= maxSeq:
            sequ = random.randint(1, maxSeq)
        if sequ == 0:
            self.cardWannaBe = Roles.SEER
            self.claimSelf(playerObject, Roles.SEER)
        elif sequ == 2:
            self.claimSelf(playerObject, Roles.SEER)

        shouldPop = []
        while randomMid:
            nextMid = randomMid.pop()
            nextRole = roleArray.pop()
            shouldPop.append((nextMid,nextRole))
            if sequ == 1:
                self.claimBeingSeer(playerObject, nextMid, nextRole)
        return shouldPop
    def lieThiefSelf(self, playerObject, sequ, popping = None):
        self.cardWannaBe = Roles.THIEF
        self.claimBeingThief(playerObject, playerObject.playerID, Roles.THIEF, playerObject.playerID)
        return None
    def lieVillage(self, playerObject, sequ, popping = None):
        self.cardWannaBe = Roles.VILLAGER
        self.claimSelf(playerObject, Roles.VILLAGER)
        return None

    def getAnotherWolf(self, playerObject):
        for idx, card in enumerate(self.sureCard):
            if card is Roles.WEREWOLF and idx != playerObject.playerID:
                return idx
        return -1

    def listOfNotClaimCards(self, playerObject):
        hasCard = [1] * Roles.roleCount
        for i in range(playerObject.gameObject.numberOfPlayers - (playerObject.gameObject.CENTER_NUMBER + 1)):
            hasCard[Roles.VILLAGER.value] += 1
        noteSureCard = [None] * len(self.sureCard)
        for idx, role in enumerate(self.sureCard):
            if role != -1:
                noteSureCard[idx] = {'role': role, 'by': playerObject.playerID}
        
        for claim in playerObject.gameObject.claimArray:
            # print "claim", claim
            try:
                if noteSureCard[claim.claimed] != None and self.personWeight[claim.claimBy] >= self.personWeight[noteSureCard[claim.claimed]['by']]:
                    noteSureCard[claim.claimed] = {'role': claim.role, 'by': claim.claimBy}
                elif noteSureCard[claim.claimed] == None:
                    noteSureCard[claim.claimed] = {'role': claim.role, 'by': claim.claimBy}
            except:
                pass

        roleCount = [0] * Roles.roleCount
        for role in noteSureCard:
            if role != None and role["role"] != Roles.UNKNOWN:
                roleCount[role["role"].value] += 1
        leftCard = []
        for i in range(len(hasCard)):
            hasCard[i] -= roleCount[i]
            for j in range(hasCard[i]):
                leftCard.append(Roles.roleAtIndex(i))
        return leftCard

    def generateAllPossibility(self, playerObject):
        allRole = Roles.GenerateGameRoles(playerObject.gameObject.numberOfPlayers, False)
        allRole = [role.value for role in allRole]
        # possibilities = (permute_unique(allRole))
        # possibilities = set(itertools.permutations(allRole, playerObject.gameObject.numberOfPlayers))
        possibilities = set(itertools.permutations(allRole, playerObject.gameObject.numberOfPlayers))
        possibilities = list(possibilities)
        for possibility in possibilities:
            if Roles.THIEF.value in possibility and Roles.WEREWOLF.value in possibility:
                possibilities.append([Roles.BAD_THIEF.value if x==Roles.THIEF.value else x for x in possibility])
                
        possibilities = [ [Roles.roleAtIndex(y) for y in x] for x in possibilities]
        # print ""
        # print ColorTextExt(playerObject.playerID), 'Remove', [ [y.name for y in x] for x in possibilities], ColorTextExt.RESET
        
        # print ""
        return possibilities

    """
    probability is value that is auto gen and is generated for each robot
    timeRate is time per iteration
    time is the time
    startVal is the heighest achievable probability of talking when time is at start
    endVal is the heighest achievable probability of talking when time is at end
    lastTalkTime is the last time that agent last talked. Start at 0
    timeRate is the ratio between time per iteration
    """
    def geometricProbability(self, probability, startVal, endVal ,talkNum, endTime, time, timeRate, lastTalkTime):
        timeConst = -1*math.log(1+startVal-endVal)/endTime
        envelope = (1+startVal-(math.e**(-1*timeConst*time)))*(0.85**talkNum)
        iteration = (time-lastTalkTime)/(timeRate+0.0)
        #calcProb = (1-probability)*(probability**(iteration-1))*envelope
        calcProb = (1-((1-probability)**(iteration)))*envelope
        #print ("calcProb is: ",calcProb)
        return calcProb