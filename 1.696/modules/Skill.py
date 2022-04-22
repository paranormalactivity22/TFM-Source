#coding: utf-8
import asyncio
# Modules
from ByteArray import ByteArray
from Identifiers import Identifiers

class Skills:
    def __init__(self, player, server):
        self.client = player
        self.server = player.server
        self.rangeArea = 85

    def sendExp(self, level, exp, nextLevel):
        self.client.sendPacket(Identifiers.send.Shaman_Exp, ByteArray().writeShort(level - 1).writeInt(exp).writeInt(nextLevel).toByteArray())

    def sendGainExp(self, amount):
        self.client.sendPacket(Identifiers.send.Shaman_Gain_Exp, ByteArray().writeInt(amount).toByteArray())

    def sendEarnedExp(self, xp, numCompleted):
        self.client.sendPacket(Identifiers.send.Shaman_Earned_Exp, ByteArray().writeShort(xp).writeShort(numCompleted).toByteArray())

    def sendEarnedLevel(self, playerName, level):
        self.client.room.sendAll(Identifiers.send.Shaman_Earned_Level, ByteArray().writeUTF(playerName).writeShort(level - 1).toByteArray())
    
    def sendTeleport(self, type, posX, posY):
        self.client.room.sendAll(Identifiers.send.Teleport, ByteArray().writeByte(type).writeShort(posX).writeShort(posY).toByteArray())
    
    def sendSkillObject(self, objectID, posX, posY, angle):
        self.client.room.sendAll(Identifiers.send.Skill_Object, ByteArray().writeShort(posX).writeShort(posY).writeByte(objectID).writeShort(angle).writeInt(0).writeBoolean(False).toByteArray())
    
    def sendShamanSkills(self, refresh):
        packet = ByteArray().writeByte(len(self.client.playerSkills))
        for skill in self.client.playerSkills.items():
            packet.writeByte(skill[0]).writeByte(skill[1])

        packet.writeBoolean(refresh)

        self.client.sendPacket(Identifiers.send.Shaman_Skills, packet.toByteArray())
    
    def sendEnableSkill(self, id, count):
        self.client.sendPacket(Identifiers.send.Enable_Skill, ByteArray().writeUnsignedByte(id).writeUnsignedByte(count).toByteArray())
    
    def sendShamanFly(self, fly):
        self.client.room.sendAllOthers(self.client, Identifiers.send.Shaman_Fly, ByteArray().writeInt(self.client.playerCode).writeBoolean(fly).toByteArray())
    
    def sendProjectionSkill(self, posX, posY, dir):
        self.client.room.sendAllOthers(self.client, Identifiers.send.Projection_Skill, ByteArray().writeShort(posX).writeShort(posY).writeShort(dir).toByteArray())
    
    def sendConvertSkill(self, objectID):
        self.client.room.sendAll(Identifiers.send.Convert_Skill, ByteArray().writeInt(objectID).writeByte(0).toByteArray())
    
    def sendDemolitionSkill(self, objectID):
        self.client.room.sendAll(Identifiers.send.Demolition_Skill, ByteArray().writeInt(objectID).toByteArray())
    
    def sendBonfireSkill(self, px, py, seconds):
        self.client.room.sendAll(Identifiers.send.Bonfire_Skill, ByteArray().writeShort(px).writeShort(py).writeByte(seconds).toByteArray())
    
    def sendSpiderMouseSkill(self, px, py):
        self.client.room.sendAll(Identifiers.send.Spider_Mouse_Skill, ByteArray().writeShort(px).writeShort(py).toByteArray())

    def sendRolloutMouseSkill(self, playerCode):
        self.client.room.sendAll(Identifiers.send.Rollout_Mouse_Skill, ByteArray().writeInt(playerCode).toByteArray())

    def sendDecreaseMouseSkill(self, playerCode):
        self.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(playerCode).writeShort(70).writeBoolean(True).toByteArray())
    
    def sendLeafMouseSkill(self, playerCode):
        self.client.room.sendAll(Identifiers.send.Leaf_Mouse_Skill, ByteArray().writeByte(1).writeInt(playerCode).toByteArray())
    
    def sendIceMouseSkill(self, playerCode, iced):
        self.client.room.sendAll(Identifiers.send.Iced_Mouse_Skill, ByteArray().writeInt(playerCode).writeBoolean(iced).toByteArray())

    def sendGravitationalSkill(self, seconds, velX, velY):
        self.client.room.sendAll(Identifiers.send.Gravitation_Skill, ByteArray().writeInt(seconds).writeInt(velX).writeInt(velY).toByteArray())
    
    def sendGrapnelSkill(self, playerCode, px, py):
        self.client.room.sendAll(Identifiers.send.Grapnel_Mouse_Skill, ByteArray().writeInt(playerCode).writeShort(px).writeShort(py).toByteArray())
    
    def sendEvolutionSkill(self, playerCode):
        self.client.room.sendAll(Identifiers.send.Evolution_Skill, ByteArray().writeInt(playerCode).writeByte(100).toByteArray())

    def sendGatmanSkill(self, playerCode):
        self.client.room.sendAll(Identifiers.send.Gatman_Skill, ByteArray().writeInt(playerCode).writeByte(1).toByteArray())
    
    def sendRestorativeSkill(self, objectID, id):
        self.client.room.sendAll(Identifiers.send.Restorative_Skill, ByteArray().writeInt(objectID).writeInt(id).toByteArray())
    
    def sendRecyclingSkill(self, id):
        self.client.room.sendAll(Identifiers.send.Recycling_Skill, ByteArray().writeShort(id).toByteArray())
    
    def sendAntigravitySkill(self, objectID):
        self.client.room.sendAll(Identifiers.send.Antigravity_Skill, ByteArray().writeInt(objectID).writeShort(0).toByteArray())
    
    def sendHandymouseSkill(self, handyMouseByte, objectID):
        self.client.room.sendAll(Identifiers.send.Handymouse_Skill, ByteArray().writeByte(handyMouseByte).writeInt(objectID).writeByte(self.client.room.lastHandymouse[1]).writeInt(self.client.room.lastHandymouse[0]).toByteArray())

    def earnExp(self, isShaman, exp):
        gainExp = exp * (((3 if self.client.shamanLevel < 30 else (6 if self.client.shamanLevel >= 30 and self.client.shamanLevel < 60 else 10)) if self.client.shamanType == 0 else (5 if self.client.shamanLevel < 30 else (10 if self.client.shamanLevel >= 30 and self.client.shamanLevel < 60 else 20))) if isShaman else 1)
        self.client.shamanExp += gainExp
        if self.client.shamanExp < self.client.shamanExpNext:
            self.sendGainExp(self.client.shamanExp)
            self.sendExp(self.client.shamanLevel, self.client.shamanExp, self.client.shamanExpNext)
            if isShaman:
                self.sendEarnedExp(gainExp, exp)
        else:
            if self.client.shamanLevel < 300:
                self.client.shamanLevel += 1
                self.client.shamanExp -= self.client.shamanExpNext
                if self.client.shamanExp < 0:
                    self.client.shamanExp = 0

                self.client.shamanExpNext += 90

                self.sendExp(self.client.shamanLevel, 0, self.client.shamanExpNext)
                self.sendGainExp(self.client.shamanExp)
                if isShaman:
                    self.sendEarnedExp(gainExp, exp)

                if self.client.shamanLevel >= 20:
                    self.sendEarnedLevel(self.client.playerName, self.client.shamanLevel)

    def buySkill(self, skill):
        if self.client.shamanLevel - 1 > len(self.client.playerSkills):
            if skill in self.client.playerSkills:
                self.client.playerSkills[skill] += 1
            else:
                self.client.playerSkills[skill] = 1
            self.sendShamanSkills(True)

    def redistributeSkills(self):
        if self.client.shopCheeses >= self.client.shamanLevel:
            if len(self.client.playerSkills) >=  1:
                if self.client.canRedistributeSkills:
                    self.client.shopCheeses -= self.client.shamanLevel
                    self.client.playerSkills = {}
                    self.sendShamanSkills(True)
                    self.client.canRedistributeSkills = False
                    if self.client.resSkillsTimer != None: self.client.resSkillsTimer.cancel()
                    self.client.resSkillsTimer = self.server.loop.call_later(600, setattr, self, "canRedistributeSkills", True)
                    self.client.totem = [0, ""]
                else:
                    self.client.sendPacket(Identifiers.send.Redistribute_Error_Time)
        else:
            self.client.sendPacket(Identifiers.send.Redistribute_Error_Cheeses)

    def getTimeSkill(self):
        if 0 in self.client.playerSkills:
            self.client.room.addTime += self.client.playerSkills[0] * 5

    def getkills(self):
        if self.client.isShaman:
            if 4 in self.client.playerSkills and not self.client.room.isDoubleMap:
                self.client.canShamanRespawn = True

            for skill in [5, 8, 9, 11, 12, 26, 28, 29, 31, 41, 46, 48, 51, 52, 53, 60, 62, 65, 66, 67, 69, 71, 74, 80, 81, 83, 85, 88, 90, 93]:
                if skill in self.client.playerSkills and not (self.client.room.isSurvivor and skill == 81):
                    self.sendEnableSkill(skill, self.client.playerSkills[skill] * 2 if skill in [28, 65, 74] else self.client.playerSkills[skill])

            for skill in [6, 30, 33, 34, 44, 47, 50, 63, 64, 70, 73, 82, 84, 92]:
                if skill in self.client.playerSkills:
                    if skill == 6: self.client.ambulanceCount = skill
                    self.sendEnableSkill(skill, 1)

            for skill in [7, 14, 27, 86, 87, 94]:
                if skill in self.client.playerSkills:
                    self.sendEnableSkill(skill, 100)

            for skill in [10, 13]:
                if skill in self.client.playerSkills:
                    self.sendEnableSkill(skill, 3)

            if 20 in self.client.playerSkills:
                count = self.client.playerSkills[20]            
                self.sendEnableSkill(20, [114, 118, 120, 122, 126][(5 if count > 5 else count) - 1])

            if 21 in self.client.playerSkills:
                self.bubblesCount = self.client.playerSkills[21]

            if 22 in self.client.playerSkills and not self.client.room.currentMap in [108, 109]:
                count = self.client.playerSkills[22]
                self.sendEnableSkill(22, [25, 30, 35, 40, 45][(5 if count > 5 else count) - 1])

            if 23 in self.client.playerSkills:
                count = self.client.playerSkills[23]            
                self.sendEnableSkill(23, [40, 50, 60, 70, 80][(5 if count > 5 else count) - 1])

            if 24 in self.client.playerSkills:
                self.client.isOpportunist = True

            if 32 in self.client.playerSkills:
                self.client.iceCount += self.client.playerSkills[32]

            if 40 in self.client.playerSkills:
                count = self.client.playerSkills[40]            
                self.sendEnableSkill(40, [30, 40, 50, 60, 70][(5 if count > 5 else count) - 1])

            if 42 in self.client.playerSkills:
                count = self.client.playerSkills[42]            
                self.sendEnableSkill(42, [240, 230, 220, 210, 200][(5 if count > 5 else count) - 1])

            if 43 in self.client.playerSkills:
                count = self.client.playerSkills[43]            
                self.sendEnableSkill(43, [240, 230, 220, 210, 200][(5 if count > 5 else count) - 1])

            if 45 in self.client.playerSkills:
                count = self.client.playerSkills[45]
                self.sendEnableSkill(45, [110, 120, 130, 140, 150][(5 if count > 5 else count) - 1])

            if 49 in self.client.playerSkills:
                count = self.client.playerSkills[49]
                self.sendEnableSkill(49, [80, 70, 60, 50, 40][(5 if count > 5 else count) - 1])

            if 54 in self.client.playerSkills:
                self.sendEnableSkill(54, 130)

            if 72 in self.client.playerSkills:
                count = self.client.playerSkills[72]            
                self.sendEnableSkill(72, [25, 30, 35, 40, 45][(5 if count > 5 else count) - 1])

            if 89 in self.client.playerSkills and not self.client.room.isSurvivor:
                count = self.client.playerSkills[89]            
                self.sendEnableSkill(49, [56, 52, 48, 44, 40][(5 if count > 5 else count) - 1])
                self.sendEnableSkill(54, [96, 92, 88, 84, 80][(5 if count > 5 else count) - 1])

            if 91 in self.client.playerSkills:
                self.client.desintegration = True

    def getPlayerSkills(self, skills):
        if 1 in skills:
            self.sendEnableSkill(1, [110, 120, 130, 140, 150][(5 if skills[1] > 5 else skills[1]) - 1])

        if 2 in skills:
            self.sendEnableSkill(2, [114, 126, 118, 120, 122][(5 if skills[2] > 5 else skills[2]) - 1])

        if 68 in skills:
            self.sendEnableSkill(68, [96, 92, 88, 84, 80][(5 if skills[68] > 5 else skills[68]) - 1])

    def placeSkill(self, objectID, code, px, py, angle):
        if code == 36:
            for player in self.client.room.clients.values():
                if self.checkQualifiedPlayer(px, py, player):
                    player.sendPacket(Identifiers.send.Can_Transformation, 1)
                    break

        elif code == 37:
            for player in self.client.room.clients.values():
                if self.checkQualifiedPlayer(px, py, player):
                    self.sendTeleport(36, player.posX, player.posY)
                    player.room.movePlayer(player.playerName, self.client.posX, self.client.posY, False, 0, 0, True)
                    self.sendTeleport(37, self.client.posX, self.client.posY)
                    break

        elif code == 38:
            for player in self.client.room.clients.values():
                if player.isDead and not player.hasEnter and not player.isAfk and not player.isShaman and not player.isNewPlayer:
                    if self.client.ambulanceCount > 0:
                        self.client.ambulanceCount -= 1
                        self.client.room.respawnSpecific(player.playerName)
                        player.isDead = False
                        player.hasCheese = False
                        player.room.movePlayer(player.playerName, self.client.posX, self.client.posY, False, 0, 0, True)
                        self.sendTeleport(37, self.client.posX, self.client.posY)
                    else:
                        break
            self.client.room.sendAll(Identifiers.send.Skill, chr(38) + chr(1))

        elif code == 42:
            self.sendSkillObject(3, px, py, 0)

        elif code == 43:
            self.sendSkillObject(1, px, py, 0)

        elif code == 47:
            if self.client.room.numCompleted > 1:
                for player in self.client.room.clients.values():
                    if player.hasCheese and self.checkQualifiedPlayer(px, py, player):
                        player.playerWin(0)
                        break

        elif code == 55:
            for player in self.client.room.clients.values():
                if not player.hasCheese and self.client.hasCheese and self.checkQualifiedPlayer(px, py, player):
                    player.sendGiveCheese()
                    self.client.sendRemoveCheese()
                    self.client.hasCheese = False
                    break

        elif code == 56:
            self.sendTeleport(36, self.client.posX, self.client.posY)
            self.client.room.movePlayer(self.client.playerName, px, py, False, 0, 0, False)
            self.sendTeleport(37, px, py)

        elif code == 57:
            if self.client.room.cloudID == -1:
                self.client.room.cloudID = objectID
            else:
                self.client.room.removeObject(self.client.room.cloudID)
                self.client.room.cloudID = objectID

        elif code == 61:
            if self.client.room.companionBox == -1:
                self.client.room.companionBox = objectID
            else:
                self.client.room.removeObject(self.client.room.companionBox)
                self.client.room.companionBox = objectID

        elif code == 70:
            self.sendSpiderMouseSkill(px, py)

        elif code == 71:
            for player in self.client.room.clients.values():
                if self.checkQualifiedPlayer(px, py, player):
                    self.sendRolloutMouseSkill(player.playerCode)
                    self.client.room.sendAll(Identifiers.send.Skill, chr(71) + chr(1))
                    break

        elif code == 73:
            for player in self.client.room.clients.values():
                if self.checkQualifiedPlayer(px, py, player):
                    self.sendDecreaseMouseSkill(player.playerCode)
                    break

        elif code == 74:
            for player in self.client.room.clients.values():
                if self.checkQualifiedPlayer(px, py, player):
                    self.sendLeafMouseSkill(player.playerCode)
                    break

        elif code == 75:
            self.client.room.sendAll(Identifiers.send.Remove_All_Objects_Skill)

        elif code == 76:
            self.sendSkillObject(5, px, py, angle)

        elif code == 79:
            if not self.client.room.isSurvivor:
                for player in self.client.room.clients.values():
                    if self.checkQualifiedPlayer(px, py, player):
                        self.sendIceMouseSkill(player.playerCode, True)
                self.client.room.sendAll(Identifiers.send.Skill, chr(79) + chr(1))
                self.server.loop.call_later(self.client.playerSkills[82] * 2, lambda: self.sendIceMouseSkill(player.playerCode, False))

        elif code == 81:
            self.sendGravitationalSkill(self.client.playerSkills[63] * 2, 0, 0)

        elif code == 83:
            for player in self.client.room.clients.values():
                if self.checkQualifiedPlayer(px, py, player):
                    player.sendPacket(Identifiers.send.Can_Meep, 1)
                    break

        elif code == 84:
            self.sendGrapnelSkill(self.client.playerCode, px, py)

        elif code == 86:
            if 86 in self.client.playerSkills:
                self.sendBonfireSkill(px, py, self.client.playerSkills[86] * 4)

        elif code == 92:
            self.getSkills()
            self.client.room.sendAll(Identifiers.send.Reset_Shaman_Skills)

        elif code == 93:
            for player in self.client.room.clients.values():
                if self.checkQualifiedPlayer(px, py, player):
                    self.sendEvolutionSkill(player.playerCode)
                    break

        elif code == 94:
            self.sendGatmanSkill(self.client.playerCode)

    def parseEmoteSkill(self, emote):
        count = 0
        if emote == 0 and 3 in self.client.playerSkills:
            for player in self.client.room.clients.values():
                if self.client.playerSkills[3] >= count and player != self.client:
                    if player.posX >= self.client.posX - 400 and player.posX <= self.client.posX + 400:
                        if player.posY >= self.client.posY - 300 and player.posY <= self.client.posY + 300:
                            player.sendPlayerEmote(0, "", False, False)
                            count += 1
                else:
                    break

        elif emote == 4 and 61 in self.client.playerSkills:
            for player in self.client.room.clients.values():
                if self.client.playerSkills[61] >= count and player != self.client:
                    if player.posX >= self.client.posX - 400 and player.posX <= self.client.posX + 400:
                        if player.posY >= self.client.posY - 300 and player.posY <= self.client.posY + 300:
                            player.sendPlayerEmote(2, "", False, False)
                            count += 1
                else:
                    break

        elif emote == 8 and 25 in self.client.playerSkills:
            for player in self.client.room.clients.values():
                if self.client.playerSkills[25] >= count and player != self.client:
                    if player.posX >= self.client.posX - 400 and player.posX <= self.client.posX + 400:
                        if player.posY >= self.client.posY - 300 and player.posY <= self.client.posY + 300:
                            player.sendPlayerEmote(3, "", False, False)
                            count += 1
                else:
                    break

    def checkQualifiedPlayer(self, px, py, player):
        if not player.playerName == self.client.playerName and not player.isShaman:
            if player.posX >= px - 85 and player.posX <= px + 85:
                if player.posY >= py - 85 and player.posY <= py + 85:
                    return True
        return False

    def getShamanBadge(self):
        if self.client.equipedShamanBadge != 0:
            return self.client.equipedShamanBadge

        badgesCount = [0, 0, 0, 0, 0]

        for skill in self.client.playerSkills.items():
            if skill[0] > -1 and skill[0] < 14:
                badgesCount[0] += skill[1]
            elif skill[0] > 19 and skill[0] < 35:
                badgesCount[1] += skill[1]
            elif skill[0] > 39 and skill[0] < 55:
                badgesCount[2] += skill[1]
            elif skill[0] > 59 and skill[0] < 75:
                badgesCount[4] += skill[1]
            elif skill[0] > 79 and skill[0] < 95:
                badgesCount[3] += skill[1]

        return -(badgesCount.index(max(badgesCount)))
