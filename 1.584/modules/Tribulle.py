#coding: utf-8
import re, time as _time, traceback

# Modules
from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers
from collections import deque

class Tribulle:
    try:
        
        def __init__(self, player, server):
            self.client = player
            self.server = player.server
            self.Cursor = player.Cursor

            self.TRIBE_RANKS = "0|${trad#TG_0}|0;0|${trad#TG_1}|0;2|${trad#TG_2}|0;3|${trad#TG_3}|0;4|${trad#TG_4}|32;5|${trad#TG_5}|160;6|${trad#TG_6}|416;7|${trad#TG_7}|932;8|${trad#TG_8}|2044;9|${trad#TG_9}|2046"
            
        def getTime(self):
            return int(_time.time() // 60)

        def sendPacket(self, code, result):
            self.client.sendPacket([60, 3], ByteArray().writeShort(code).writeBytes(result).toByteArray())
      
        def sendPacketToPlayer(self, playerName, code, result):
            player = self.server.players.get(playerName)
            if player != None:
                player.tribulle.sendPacket(code, result)

        def sendPacketWholeTribe(self, code, result, all=False):
            for player in self.server.players.values():
                if player.playerCode != self.client.playerCode or all:
                    if player.tribeCode == self.client.tribeCode:
                        player.tribulle.sendPacket(code, result)

        def sendPacketWholeChat(self, chatID, code, result, all=False):
            for player in self.server.players.values():
                if player.playerCode != self.client.playerCode or all:
                    if chatID in player.chats:
                        player.tribulle.sendPacket(code, result)

        def updateTribeData(self):
            for player in self.server.players.values():
                if player.tribeCode == self.client.tribeCode:
                    player.tribeHouse = self.client.tribeHouse
                    player.tribeMessage = self.client.tribeMessage
                    player.tribeRanks = self.client.tribeRanks

        def parseTribulleCode(self, code, packet):
            if self.client.isBlockAttack:
                if code == 28:
                    self.sendFriendsList(packet)
                elif code == 30:
                    self.closeFriendsList(packet)
                elif code == 18:
                    self.addFriend(packet)
                elif code == 20:
                    self.removeFriend(packet)
                elif code == 46:
                    self.sendIgnoredsList(packet)
                elif code == 42:
                    self.ignorePlayer(packet)
                elif code == 44:
                    self.removeIgnore(packet)
                elif code == 52:
                    self.whisperMessage(packet)
                elif code == 60:
                    self.disableWhispers(packet)
                elif code == 10:
                    self.changeGender(packet)
                elif code == 22:
                    self.marriageInvite(packet)
                elif code == 24:
                    self.marriageAnswer(packet)
                elif code == 26:
                    self.marriageDivorce(packet)
                elif code == 108:
                    self.sendTribeInfo(packet)
                elif code == 84:
                    self.createTribe(packet)
                elif code == 78:
                    self.tribeInvite(packet)
                elif code == 80:
                    self.tribeInviteAnswer(packet)
                elif code == 98:
                    self.changeTribeMessage(packet)
                elif code == 102:
                    self.changeTribeCode(packet)
                elif code == 110:
                    self.closeTribe(packet)
                elif code == 118:
                    self.createNewTribeRank(packet)
                elif code == 120:
                    self.deleteTribeRank(packet)
                elif code == 116:
                    self.renameTribeRank(packet)
                elif code == 122:
                    self.changeRankPosition(packet)
                elif code == 114:
                    self.setRankPermition(packet)
                elif code == 112:
                    self.changeTribePlayerRank(packet)
                elif code == 132:
                    self.showTribeHistorique(packet)
                elif code == 82:
                    self.leaveTribe(packet)
                elif code == 104:
                    self.kickPlayerTribe(packet)
                elif code == 126:
                    self.setTribeMaster(packet)
                elif code == 128:
                    self.finishTribe(packet)
                elif code == 54:
                    self.customChat(packet)
                elif code == 48:
                    self.chatMessage(packet)
                elif code == 58:
                    self.chatMembersList(packet)
                elif code == 50:
                    self.sendTribeChatMessage(packet)
                else:
                    if self.server.isDebug:
                        print("[%s] [WARN][%s] Invalid Tribulle code -> Code: %s packet: %s" %(_time.strftime("%H:%M:%S"), self.client.playerName, code, repr(packet.toByteArray())))
                        with open("./logs/Errors/Debug.log", "a") as f:
                            f.write("[%s] [WARN][%s] Invalid Tribulle code -> Code: %s packet: %s\n" %(_time.strftime("%H:%M:%S"), self.client.playerName, code, repr(packet.toByteArray())))
                        f.close()
                
        def sendFriendsList(self, readPacket):
            if self.client.isBlockAttack:
                p = ByteArray().writeShort(3 if readPacket == None else 34)
                if readPacket == None:
                    p.writeByte(self.client.gender).writeInt(self.client.playerID)
                if self.client.marriage == "":
                    p.writeInt(0).writeUTF("").writeByte(1).writeInt(0).writeByte(1).writeByte(1).writeInt(1).writeUTF("").writeInt(0)
                else:
                    self.Cursor.execute("select Username, PlayerID, Gender, LastOn from Users where Username = %s", [self.client.marriage])
                    r = self.Cursor.fetchall()
                    player = self.server.players.get(self.client.marriage)
                    for rs in r:
                        p.writeInt(rs[1]).writeUTF(rs[0].lower()).writeByte(rs[2]).writeInt(rs[1]).writeByte(1).writeBoolean(self.server.checkConnectedAccount(rs[0])).writeInt(4).writeUTF(player.roomName if player else "").writeInt(rs[3])
                
                infos = {}
                self.Cursor.execute("select Username, PlayerID, FriendsList, Marriage, Gender, LastOn from Users where Username in (%s)" %(Utils.joinWithQuotes(self.client.friendsList)))
                for rs in self.Cursor.fetchall():
                    infos[rs[0]] = [rs[1], rs[2], rs[3], rs[4], rs[5]]

                self.client.openingFriendList = True
                isOnline = []
                friendsOn = []
                friendsOff = []
                isOffline = []
                for playerName in self.client.friendsList:
                    if not playerName in infos:
                        continue
                    if not self.client.friendsList == ['']:
                        player = self.server.players.get(playerName)
                        info = infos[playerName]
                        isFriend = self.client.playerName in player.friendsList if player != None else self.client.playerName in info[1].split(",")
                        if self.server.checkConnectedAccount(playerName):
                            if isFriend:
                                friendsOn.append(playerName)
                            else:
                                isOnline.append(playerName)
                        else:
                            if isFriend:
                                friendsOff.append(playerName)
                            else:
                                isOffline.append(playerName)
                playersNames = friendsOn + isOnline + friendsOff + isOffline
                
                p.writeShort(len(playersNames)-1 if playersNames == [''] else len(playersNames))
                for playerName in playersNames:
                    if not playerName in infos:
                        continue
                    if not playersNames == ['']:
                        info = infos[playerName]
                        player = self.server.players.get(playerName)
                        isFriend = self.client.playerName in player.friendsList if player != None else self.client.playerName in info[1].split(",")
                        genderID = player.gender if player else int(info[3])
                        isMarriage = self.client.playerName == player.marriage if player else info[2] == self.client.playerName
                        p.writeInt(info[0]).writeUTF(playerName.lower()).writeByte(genderID).writeInt(info[0]).writeByte(1 if isFriend else 0).writeBoolean(self.server.checkConnectedAccount(playerName)).writeInt(4 if isFriend and player != None else 1).writeUTF(player.roomName if isFriend and player != None else "").writeInt(info[4] if isFriend else 0)
                if readPacket == None:
                    p.writeShort(len(self.client.ignoredsList)-1 if self.client.ignoredsList == [''] else len(self.client.ignoredsList))

                    for playerName in self.client.ignoredsList:
                        if not self.client.ignoredsList == ['']:
                            p.writeUTF(playerName.lower())
                    p.writeUTF(self.client.tribeName)
                    p.writeInt(self.client.tribeCode)
                    p.writeUTF(self.client.tribeMessage)
                    p.writeInt(self.client.tribeHouse)
                    if not self.client.tribeRanks == "":
                        rankInfo = self.client.tribeRanks.split(";")
                        rankName = rankInfo[self.client.tribeRank].split("|")
                        p.writeUTF(rankName[1])
                        p.writeInt(rankName[2])
                    else:
                        p.writeUTF("")
                        p.writeInt(0)
                self.client.sendPacket([60, 3], p.toByteArray())
                if not readPacket == None and not self.client.marriage == "":
                    self.sendPacket(15 if readPacket == "0" else 29, ByteArray().writeInt(self.client.tribulleID+1).writeByte(1).toByteArray())
                self.client.isBlockAttack = False
                self.client.blockAttack()
##            else:
##                self.client.sendMessage("<ROSE>,")
                
        def closeFriendsList(self, readPacket):
            self.client.openingFriendList = False
            self.sendPacket(31, ByteArray().writeBytes(readPacket.toByteArray()).writeByte(1).toByteArray())

        def addFriend(self, readPacket):
            tribulleID, playerName = readPacket.readInt(), Utils.parsePlayerName(readPacket.readUTF())
            #if not "#" in playerName: playerName += "#0000"
            id = self.server.getPlayerID(playerName)
            player = self.server.players.get(playerName)
            isFriend = self.checkFriend(playerName, self.client.playerName)
            self.Cursor.execute("select Username, PlayerID, Gender, LastOn from Users where Username = %s", [playerName])
            rs = self.Cursor.fetchone()
            if not self.server.checkExistingUser(playerName):
                self.sendPacket(19, ByteArray().writeInt(tribulleID).writeByte(12).toByteArray())
            else:
                self.client.friendsList.append(playerName)
                if playerName in self.client.ignoredsList:
                    self.client.ignoredsList.remove(playerName)
                self.sendPacket(36, ByteArray().writeInt(rs[1]).writeUTF(Utils.parsePlayerName(playerName)).writeByte(rs[2]).writeInt(rs[1]).writeShort(self.server.checkConnectedAccount(playerName)).writeInt(4 if isFriend else 0).writeUTF(player.roomName if isFriend and player != None else "").writeInt(rs[3] if isFriend else 0).toByteArray())
                self.sendPacket(19, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
                if player != None:
                    player.tribulle.sendPacket(35, ByteArray().writeInt(self.client.playerID).writeUTF(self.client.playerName.lower()).writeByte(self.client.gender).writeInt(self.client.playerID).writeByte(1).writeByte(self.server.checkConnectedAccount(self.client.playerName)).writeInt(4 if isFriend else 0).writeUTF(self.client.roomName if isFriend else "").writeInt(self.client.lastOn if isFriend else 0).toByteArray())
            
        def removeFriend(self, readPacket):
            tribulleID, playerName = readPacket.readInt(), Utils.parsePlayerName(readPacket.readUTF())
            packet = ByteArray()
            id = self.server.getPlayerID(playerName)
            player = self.server.players.get(playerName)

            if playerName in self.client.friendsList:
                packet.writeInt(id)
                self.client.friendsList.remove(playerName)
                self.sendPacket(37, packet.toByteArray())
                self.sendPacket(21, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
                if player != None:
                    player.tribulle.sendPacket(35, ByteArray().writeInt(self.client.playerID).writeUTF(self.client.playerName.lower()).writeByte(self.client.gender).writeInt(self.client.playerID).writeShort(1).writeInt(0).writeUTF("").writeInt(0).toByteArray())              

        def sendFriendConnected(self, playerName):
            if playerName in self.client.friendsList:
                id = self.server.getPlayerID(playerName)
                player = self.server.players.get(playerName)
                self.sendPacket(35, ByteArray().writeInt(player.playerID).writeUTF(playerName.lower()).writeByte(player.gender).writeInt(player.playerID).writeByte(1).writeByte(1).writeInt(1).writeUTF("").writeInt(player.lastOn).toByteArray())
                self.sendPacket(32, ByteArray().writeUTF(player.playerName.lower()).toByteArray())
                   
        def sendFriendChangedRoom(self, playerName, langueID):
            if playerName in self.client.friendsList:
                player = self.server.players.get(playerName)
                self.sendPacket(35, ByteArray().writeInt(player.playerID).writeUTF(playerName.lower()).writeByte(player.gender).writeInt(player.playerID).writeByte(1).writeByte(1).writeInt(4).writeUTF(player.roomName).writeInt(player.lastOn).toByteArray())
                    
        def sendFriendDisconnected(self, playerName):
            if playerName in self.client.friendsList:
                self.Cursor.execute("select Username, PlayerID, Gender, LastOn from Users where Username = %s", [playerName])
                rs = self.Cursor.fetchone()
                self.sendPacket(35, ByteArray().writeInt(rs[1]).writeUTF(playerName.lower()).writeByte(rs[2]).writeInt(rs[1]).writeByte(1).writeByte(0).writeInt(1).writeUTF("").writeInt(rs[3]).toByteArray())
                self.sendPacket(33, ByteArray().writeUTF(playerName.lower()).toByteArray())
                
        def sendIgnoredsList(self, readPacket):
            tribulleID = readPacket.readInt()
            packet = ByteArray().writeInt(tribulleID).writeShort(len(self.client.ignoredsList))
            for playerName in self.client.ignoredsList:
                packet.writeUTF(playerName)
            self.sendPacket(47, packet.toByteArray())
    
        def ignorePlayer(self, readPacket):
            tribulleID, playerName = readPacket.readInt(), Utils.parsePlayerName(readPacket.readUTF())
            #if not "#" in playerName: playerName += "#0000"
            packet = ByteArray().writeInt(tribulleID)

            if not self.server.checkExistingUser(playerName):
                self.sendPacket(43, packet.writeByte(12).toByteArray())
            else:
                self.client.ignoredsList.append(playerName)

                if playerName in self.client.friendsList:
                    self.client.friendsList.remove(playerName)
                self.sendPacket(43, packet.writeByte(1).toByteArray())

        def removeIgnore(self, readPacket):
            tribulleID, playerName = readPacket.readInt(), Utils.parsePlayerName(readPacket.readUTF())
            packet = ByteArray().writeInt(tribulleID)

            self.client.ignoredsList.remove(playerName)
            self.sendPacket(45, packet.writeByte(1).toByteArray())

        def whisperMessage(self, readPacket):
            tribulleID, playerName, message = readPacket.readInt(), Utils.parsePlayerName(readPacket.readUTF()), readPacket.readUTF().replace("\n", "").replace("&amp;#", "&#").replace("<", "&lt;")
            isCheck = self.server.checkMessage(message)

            if self.client.cheeseCount > 3:
                if self.client.isGuest:
                        self.client.sendLangueMessage("", "$Créer_Compte_Parler")
                        
                elif not message == "":
                    can = True

                    packet = ByteArray().writeInt(tribulleID)
                    if playerName.startswith("*") or not playerName in self.server.players:
                        can = False
                        packet.writeByte(12)
                        packet.writeShort(0)
                        self.sendPacket(53, packet.toByteArray())
                    else:
                        if self.client.isMute:
                            if not self.client.isGuest:
                                muteInfo = self.server.getModMuteInfo(self.client.playerName)
                                timeCalc = Utils.getHoursDiff(muteInfo[1])
                                if timeCalc <= 0:
                                    self.server.removeModMute(self.client.playerName)
                                else:
                                    can = False
                                    self.client.sendModMute(self.client.playerName, timeCalc, muteInfo[0], True)

                        if can:
                            player = self.server.players.get(playerName)
                            if player != None:
                                if player.silenceType != 0:
                                    if (self.client.privLevel >= 3 or (player.silenceType == 2 and self.checkFriend(playerName, self.client.playerName))):
                                        pass
                                    else:
                                        self.sendSilenceMessage(playerName, tribulleID)
                                        return

                                if not (self.client.playerName in player.ignoredsList) and not isCheck:
                                    player.tribulle.sendPacket(66, ByteArray().writeUTF(self.client.playerName.lower()).writeInt(self.client.langueID+1).writeUTF(player.playerName.lower()).writeUTF(message).toByteArray())
                                self.sendPacket(66, ByteArray().writeUTF(self.client.playerName.lower()).writeInt(player.langueID+1).writeUTF(player.playerName.lower()).writeUTF(message).toByteArray())

                                if isCheck:
                                    self.server.sendStaffMessage(7, "[<V>WHISPER</V>][<V>SPAM</V>][<V>" + self.client.roomName + "</V>][<T>" + self.client.playerName + "</T>] sent a link in the message: [<J>" + str(message) + "</J>].")    

                                if not self.client.playerName in self.server.chatMessages:
                                    messages = deque([], 60)
                                    messages.append([_time.strftime("%Y/%m/%d %H:%M:%S"), "> [%s] %s" %(player.playerName, message)])
                                    self.server.chatMessages[self.client.playerName] = messages
                                else:
                                    self.server.chatMessages[self.client.playerName].append([_time.strftime("%Y/%m/%d %H:%M:%S"), "> [%s] %s" %(player.playerName, message)])
            else:
                self.client.sendMessage("<ROSE>You need 3 cheeses to speak.")            

        def disableWhispers(self, readPacket):
            tribulleID, type, message = readPacket.readInt(), readPacket.readByte(), readPacket.readUTF()
            self.sendPacket(61, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())

            self.client.silenceType = type
            self.client.silenceMessage = "" if self.server.checkMessage(message) else message

        def sendSilenceMessage(self, playerName, tribulleID):
            player = self.server.players.get(playerName)
            if player != None:
                self.sendPacket(53, ByteArray().writeInt(tribulleID).writeByte(25).writeUTF(player.silenceMessage).toByteArray())

        def changeGender(self, readPacket):
            tribulleID, gender = readPacket.readInt(), readPacket.readByte()
            self.client.gender = gender
            self.sendPacket(12, ByteArray().writeInt(tribulleID).writeByte(gender).toByteArray())
            self.sendPacket(12, ByteArray().writeByte(gender).toByteArray())
            self.client.sendProfile(self.client.playerName)
            #for player in self.server.players.values():
            #    if self.client.playerName and player.playerName in self.client.friendsList and player.friendsList:
            #        player.tribulle.sendPacket(11, ByteArray().writeInt(tribulleID).writeByte(gender).toByteArray())

    
        def marriageInvite(self, readPacket):
            tribulleID, playerName = readPacket.readInt(), Utils.parsePlayerName(readPacket.readUTF())
            packet = ByteArray().writeInt(tribulleID)

            player = self.server.players.get(playerName)
            if not self.server.checkConnectedAccount(playerName) or not self.server.checkExistingUser(playerName):
                self.sendPacket(23, packet.writeByte(11).toByteArray())
            elif not player.marriage == "":
                self.sendPacket(23, packet.writeByte(15).toByteArray())
            else:
                if not self.client.playerName in player.ignoredMarriageInvites:
                    player.marriageInvite = [self.client.playerName, tribulleID]
                    player.tribulle.sendPacket(38, ByteArray().writeUTF(self.client.playerName).toByteArray())
                    self.sendPacket(23, packet.writeByte(1).toByteArray())

    
        def marriageAnswer(self, readPacket):
            tribulleID, playerName, answer = readPacket.readInt(), Utils.parsePlayerName(readPacket.readUTF()), readPacket.readByte()

            player = self.server.players.get(playerName)
            if player != None:
                if answer == 0:
                    self.sendPacket(25, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
                    player.tribulle.sendPacket(40, ByteArray().writeUTF(self.client.playerName.lower()).toByteArray())

                elif answer == 1:
                    player.marriage = self.client.playerName
                    self.client.marriage = player.playerName

                    if not self.client.playerName in player.friendsList:
                        player.friendsList.append(self.client.playerName)

                    if not player.playerName in self.client.friendsList:
                        self.client.friendsList.append(player.playerName)

                    self.sendPacket(39, ByteArray().writeUTF(player.playerName.lower()).toByteArray())
                    player.tribulle.sendPacket(39, ByteArray().writeUTF(self.client.playerName.lower()).toByteArray())

                    if self.client.openingFriendList:
                        self.sendFriendsList("0")

                    if player.openingFriendList:
                        player.tribulle.sendFriendsList("0")

                    self.sendPacket(37, ByteArray().writeInt(player.playerID).toByteArray())
                    player.tribulle.sendPacket(37, ByteArray().writeInt(self.client.playerID).toByteArray())

                    self.sendPacket(25, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
                    
        def marriageDivorce(self, readPacket):
            tribulleID = readPacket.readInt()

            time = Utils.getTime() + 3600

            self.sendPacket(41, ByteArray().writeUTF(self.client.marriage).writeByte(1).toByteArray())
            player = self.server.players.get(self.client.marriage)
            if player != None:
                player.tribulle.sendPacket(41, ByteArray().writeUTF(player.marriage).writeByte(1).toByteArray())
                player.marriage = ""
                player.lastDivorceTimer = time
            else:
                self.removeMarriage(self.client.marriage, time)

            self.client.marriage = ""
            self.client.lastDivorceTimer = time
            
        def sendTribe(self, isNew):
            if self.client.tribeName == "":
                self.sendPacket(Identifiers.tribulle.send.ET_ErreurInformationsTribu, ByteArray().writeInt(0).writeByte(0).toByteArray())
                return

            if not self.client.tribeChat in self.client.chats:
                self.client.chats.append(self.client.tribeChat)

            self.sendPacket(Identifiers.tribulle.send.ET_SignaleRejointCanal, ByteArray().writeInt(self.client.tribeChat).writeUTF("~" + self.client.tribeName.lower()).writeBytes(chr(0) * 5).toByteArray())
            self.sendPacketWholeTribe(Identifiers.tribulle.send.ET_SignaleMembreRejointCanal, ByteArray().writeInt(self.client.tribeChat).writeInt(self.client.playerID).writeUTF(self.client.playerName.lower()).toByteArray())
            self.sendTribeInfo()

        def sendLoginMessageTribe(self):
            packet = ByteArray()
            packet.writeInt(0)
            packet.writeInt(0)
            packet.writeInt(0)
            packet.writeInt(0)
            packet.writeInt(0)
            packet.writeShort(1)
            packet.writeInt(0)
            packet.writeShort(0)

            members = self.getTribeMembers(self.client.tribeCode)
            packet.writeShort(len(members))

            infos = {}
            self.Cursor.execute("select Username, PlayerID, Gender, LastOn, TribeRank, TribeJoined from Users where Username in (%s)" %(Utils.joinWithQuotes(members)))
            for rs in self.Cursor.fetchall():
                infos[rs[0]] = [rs[1], rs[2], rs[3], rs[4], rs[5]]

            for member in members:
                if not member in infos:
                    continue

                info = infos[member]
                player = self.server.players.get(member)
                packet.writeInt(info[0])
                packet.writeUTF(member.lower())
                packet.writeByte(info[1])
                packet.writeInt(info[0])
                packet.writeInt(info[2] if not self.server.checkConnectedAccount(member) else 0)
                packet.writeByte(info[3])
                packet.writeInt(4)
                packet.writeUTF(player.roomName if player != None else "")
            

        def sendTribeInfo(self, readPacket=""):
                if not readPacket == "":
                    tribulleID, connected = readPacket.readInt(), readPacket.readByte()
                else:
                    tribulleID = self.client.tribulleID + 1
                    connected = 0
                if self.client.tribeName == "":
                    self.sendPacket(109, ByteArray().writeInt(self.client.tribulleID).writeByte(17).toByteArray())
                    return
                members = self.getTribeMembers(self.client.tribeCode)
                packet = ByteArray()
                packet.writeInt(self.client.tribeCode)
                packet.writeUTF(self.client.tribeName)
                packet.writeUTF(self.client.tribeMessage)
                packet.writeInt(self.client.tribeHouse)
                
                infos = {}
                self.client.isTribeOpen = True
                self.Cursor.execute("select Username, PlayerID, Gender, LastOn, TribeRank, TribeJoined from Users where Username in (%s)" %(Utils.joinWithQuotes(members)))
                for rs in self.Cursor.fetchall():
                    infos[rs[0]] = [rs[1], rs[2], rs[3], rs[4], rs[5]]

                isOnline = []
                isOffline = []

                for member in members:
                    if self.server.checkConnectedAccount(member):
                        isOnline.append(member)
                    else:
                        isOffline.append(member)

                if connected == 1:
                    playersTribe = isOnline + isOffline
                else:
                    playersTribe = isOnline

                packet.writeShort(len(playersTribe))
                    
                for member in playersTribe:
                    if not member in infos:
                        continue

                    info = infos[member]
                    player = self.server.players.get(member)
                    packet.writeInt(info[0])
                    packet.writeUTF(member.lower())
                    packet.writeByte(info[1])
                    packet.writeInt(info[0])
                    packet.writeInt(info[2] if not self.server.checkConnectedAccount(member) else 0)
                    packet.writeByte(info[3])
                    packet.writeInt(4)
                    packet.writeUTF(player.roomName if player != None else "")

                packet.writeShort(len(self.client.tribeRanks.split(";")))

                for rank in self.client.tribeRanks.split(";"):
                    ranks = rank.split("|")
                    packet.writeUTF(ranks[1]).writeInt(ranks[2])

                self.sendPacket(130, packet.toByteArray())
                self.client.isBlockAttack = False
                self.client.blockAttack()
            
        def closeTribe(self, readPacket):
            tribulleID = readPacket.readInt()
            self.client.isTribeOpen = False
            self.sendPacket(111, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())

        def sendTribeMemberConnected(self):
            self.sendPacketWholeTribe(88, ByteArray().writeUTF(self.client.playerName.lower()).toByteArray(), True)
            self.sendPacketWholeTribe(131, ByteArray().writeInt(self.client.playerID).writeUTF(self.client.playerName.lower()).writeByte(self.client.gender).writeInt(self.client.playerID).writeInt(0).writeByte(self.client.tribeRank).writeInt(1).writeUTF("").toByteArray())

        def sendTribeMemberChangeRoom(self):
            self.sendPacketWholeTribe(131, ByteArray().writeInt(self.client.playerID).writeUTF(self.client.playerName.lower()).writeByte(self.client.gender).writeInt(self.client.playerID).writeInt(0).writeByte(self.client.tribeRank).writeInt(4).writeUTF(self.client.roomName).toByteArray())

        def sendTribeMemberDisconnected(self):
            self.sendPacketWholeTribe(90, ByteArray().writeUTF(self.client.playerName.lower()).toByteArray())
            self.sendPacketWholeTribe(131, ByteArray().writeInt(self.client.playerID).writeUTF(self.client.playerName.lower()).writeByte(self.client.gender).writeInt(self.client.playerID).writeInt(self.client.lastOn).writeByte(self.client.tribeRank).writeInt(1).writeUTF("").toByteArray())
            
        def sendPlayerInfo(self):
            self.sendPacket(Identifiers.tribulle.send.ET_ReponseDemandeInfosJeuUtilisateur, ByteArray().writeInt(0).writeInt(self.client.playerID).writeInt(self.client.playerID).writeInt(self.getInGenderMarriage(self.client.playerName)).writeInt(self.server.getPlayerID(self.client.marriage) if not self.client.marriage == "" else 0).writeUTF(self.client.marriage).toByteArray())

        def createTribe(self, readPacket):
            tribulleID, tribeName = readPacket.readInt(), readPacket.readUTF()
            createTime = self.getTime()
            if len(tribeName) > 77:
                self.client.sendMessage("Max 77 Chararacters")
                return
            if not "<" in tribeName or not ">" in tribeName:
                self.sendPacket(85, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
                if not self.checkExistingTribe(tribeName):
                    if self.client.shopCheeses >= 500:
                        self.Cursor.execute("insert into Tribe  values(NULL, %s, '', '0', %s, '', %s, %s, 0)", [tribeName, self.TRIBE_RANKS, self.client.playerName, self.server.lastChatID])
                        self.client.shopCheeses -= 500
                        self.client.tribeCode = self.Cursor.lastrowid
                        self.client.tribeRank = 9
                        self.client.tribeName = tribeName
                        self.client.tribeJoined = createTime
                        self.client.tribeMessage = "Welcome To Transformice :)"
                        self.client.tribeRanks = self.TRIBE_RANKS

                        self.setTribeHistorique(self.client.tribeCode, 1, createTime, self.client.playerName, tribeName)

                        self.client.updateDatabase()

                        self.sendPacket(89, ByteArray().writeUTF(self.client.tribeName).writeInt(self.client.tribeCode).writeUTF(self.client.tribeMessage).writeInt(0).writeUTF(self.client.tribeRanks.split(";")[9].split("|")[1]).writeInt(2049).toByteArray())
                    else:
                        self.client.sendMessage("You dont have enough cheeses!")
                else:
                    self.client.sendMessage("The tribe aleardy exists!")
            else:
                self.client.sendMessage("<ROSE>Tribename contains HTML.")
        def tribeInvite(self, readPacket):
            tribulleID, playerName = readPacket.readInt(), Utils.parsePlayerName(readPacket.readUTF())
            packet = ByteArray().writeInt(tribulleID)
            player = self.server.players.get(playerName)

            if not self.server.checkConnectedAccount(playerName) or not self.server.checkExistingUser(playerName):
                self.sendPacket(79, packet.writeByte(11).toByteArray())
            elif not player.tribeName == "":
                self.sendPacket(79, packet.writeByte(18).toByteArray())
            else:
                if not self.client.tribeCode in player.ignoredTribeInvites:
                    player.tribeInvite = [tribulleID, self.client]
                    player.tribulle.sendPacket(86, ByteArray().writeUTF(self.client.playerName.lower()).writeUTF(self.client.tribeName).toByteArray())
                    self.sendPacket(79, packet.writeByte(1).toByteArray())

        def tribeInviteAnswer(self, readPacket):
            tribulleID, playerName, answer = readPacket.readInt(), readPacket.readUTF(), readPacket.readByte()
            resultTribulleID = int(self.client.tribeInvite[0])
            player = self.client.tribeInvite[1]
            self.client.tribeInvite = []

            if player != None:

                if answer == 0:
                    self.client.ignoredTribeInvites.append(player.tribeCode)
                    player.tribulle.sendPacket(87, ByteArray().writeUTF(self.client.playerName.lower()).writeByte(0).toByteArray())

                elif answer == 1:
                    members = self.getTribeMembers(player.tribeCode)
                    members.append(self.client.playerName)
                    self.setTribeMembers(player.tribeCode, members)

                    self.client.tribeCode = player.tribeCode
                    self.client.tribeRank = 0
                    self.client.tribeName = player.tribeName
                    self.client.tribeJoined = self.getTime()
                    tribeInfo = self.getTribeInfo(self.client.tribeCode)
                    self.client.tribeName = str(tribeInfo[0])
                    self.client.tribeMessage = str(tribeInfo[1])
                    self.client.tribeHouse = int(tribeInfo[2])
                    self.client.tribeRanks = tribeInfo[3]
                    self.client.tribeChat = int(tribeInfo[4])

                    self.setTribeHistorique(self.client.tribeCode, 2, self.getTime(), player.playerName, self.client.playerName)

                    packet = ByteArray()
                    packet.writeUTF(self.client.tribeName)
                    packet.writeInt(self.client.tribeCode)
                    packet.writeUTF(self.client.tribeMessage)
                    packet.writeInt(self.client.tribeHouse)

                    rankInfo = self.client.tribeRanks.split(";")
                    rankName = rankInfo[self.client.tribeRank].split("|")
                    packet.writeUTF(rankName[1])
                    packet.writeInt(rankName[2])
                    self.sendPacket(89, packet.toByteArray())
                    player.tribulle.sendPacket(87, ByteArray().writeUTF(self.client.playerName).writeByte(1).toByteArray())
                    self.sendPacketWholeTribe(91, ByteArray().writeUTF(self.client.playerName).toByteArray(), True)
                    for member in members:
                        player = self.server.players.get(member)
                        if player != None:
                            if player.isTribeOpen:
                                player.tribulle.sendTribeInfo()

        def changeTribeMessage(self, readPacket):
            tribulleID, message = readPacket.readInt(), readPacket.readUTF()
            self.Cursor.execute("update Tribe set Message = %s where Code = %s", [message, self.client.tribeCode])
            self.client.tribeMessage = message
            self.setTribeHistorique(self.client.tribeCode, 6, self.getTime(), message, self.client.playerName)
            self.updateTribeData()
            self.sendTribeInfo()
            self.sendPacketWholeTribe(125, ByteArray().writeUTF(self.client.playerName.lower()).writeUTF(message).toByteArray(), True)
            
        def changeTribeCode(self, readPacket):
            tribulleID, mapCode = readPacket.readInt(), readPacket.readInt()
            self.Cursor.execute("update Tribe set House = %s where Code = %s", [mapCode, self.client.tribeCode])
            
            mapInfo = self.client.room.getMapInfo(mapCode)
            if mapInfo[0] == None:
                self.client.sendPacket(Identifiers.old.send.Tribe_Result, [16])
            elif mapInfo[4] != 22 and mapInfo[4] != 0 and mapInfo[4] != 1 and mapInfo[4] != 2 and mapInfo[4] != 3 and mapInfo[4] != 4 and mapInfo[4] != 5 and mapInfo[4] != 6 and mapInfo[4] != 7 and mapInfo[4] != 8 and mapInfo[4] != 9 and mapInfo[4] != 10 and mapInfo[4] != 11 and mapInfo[4] != 13 and mapInfo[4] != 17 and mapInfo[4] != 18 and mapInfo[4] != 19 and mapInfo[4] != 22 and mapInfo[4] != 41 and mapInfo[4] != 42 and mapInfo[4] != 44:
            #elif mapInfo[4] in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 17, 18, 19, 22, 41, 42, 44]:
                self.client.sendPacket(Identifiers.old.send.Tribe_Result, [17])

            elif mapInfo[0] != None and mapInfo[4] == 22:
                self.setTribeHistorique(self.client.tribeCode, 8, self.getTime(), self.client.playerName, mapCode)
                    
            room = self.server.rooms.get("*\x03" + self.client.tribeName)
            if room != None:
                room.mapChange()

            self.updateTribeData()
            self.sendTribeInfo()

        def createNewTribeRank(self, readPacket):
            tribulleID, rankName = readPacket.readInt(), readPacket.readUTF()

            ranksID = self.client.tribeRanks.split(";")
            s = ranksID[1]
            f = ranksID[1:]
            f = ";".join(map(str, f))
            s = "%s|%s|%s" % ("0", rankName, "0")
            del ranksID[1:]
            ranksID.append(s)
            ranksID.append(f)
            self.client.tribeRanks = ";".join(map(str, ranksID))
            members = self.getTribeMembers(self.client.tribeCode)
            for playerName in members:
                player = self.server.players.get(playerName)
                tribeRank = self.getPlayerTribeRank(playerName)
                if player != None:
                    if player.tribeRank >= 1:
                        player.tribeRank += 1
                        self.Cursor.execute("update users set TribeRank = %s where Username = %s", [tribeRank+1, playerName])
                else:
                    if tribeRank >= 1:
                        self.Cursor.execute("update users set TribeRank = %s where Username = %s", [tribeRank+1, playerName])

            self.updateTribeRanks()
            self.updateTribeData()
            self.sendTribeInfo()
            for member in members:
                player = self.server.players.get(member)
                if player != None:
                    if player.isTribeOpen:
                        player.tribulle.sendTribeInfo()

        def deleteTribeRank(self, readPacket):
            tribulleID, rankID = readPacket.readInt(), readPacket.readByte()

            rankInfo = self.client.tribeRanks.split(";")
            del rankInfo[rankID]
            self.client.tribeRanks = ";".join(map(str, rankInfo))

            self.updateTribeRanks()
            self.updateTribeData()

            members = self.getTribeMembers(self.client.tribeCode)
            for playerName in members:
                player = self.server.players.get(playerName)
                if player != None:
                    if player.tribeRank == rankID:
                        player.tribeRank = 0
                    else:
                        continue
                else:
                    tribeRank = self.getPlayerTribeRank(playerName)
                    if tribeRank == rankID:
                        self.Cursor.execute("update users set TribeRank = 0 where Username = %s", [playerName])
                    else:
                        continue
            for playerName in members:
                player = self.server.players.get(playerName)
                tribeRank = self.getPlayerTribeRank(playerName)
                if player != None:
                    if player.tribeRank >= 1:
                        player.tribeRank -= 1
                        self.Cursor.execute("update users set TribeRank = %s where Username = %s", [tribeRank-1, playerName]) 
                else:
                    if tribeRank >= 1:
                        self.Cursor.execute("update users set TribeRank = %s where Username = %s", [tribeRank-1, playerName]) 
            self.sendTribeInfo()
            for member in members:
                player = self.server.players.get(member)
                if player != None:
                    if player.isTribeOpen:
                        player.tribulle.sendTribeInfo()
            
        def renameTribeRank(self, packet):
            tribulleID, rankID, rankName = packet.readInt(), packet.readByte(), packet.readUTF()
            rankInfo = self.client.tribeRanks.split(";")
            rank = rankInfo[rankID].split("|")
            rank[1] = rankName
            rankInfo[rankID] = "|".join(map(str, rank))
            self.client.tribeRanks = ";".join(map(str, rankInfo))
            self.updateTribeRanks()
            self.updateTribeData()
            self.sendTribeInfo()
            members = self.getTribeMembers(self.client.tribeCode)
            for member in members:
                player = self.server.players.get(member)
                if player != None:
                    if player.isTribeOpen:
                        player.tribulle.sendTribeInfo()

        def changeRankPosition(self, packet):
            if self.client.isBlockAttack:
                tribulleID, rankID, rankID2 = packet.readInt(), packet.readByte(), packet.readByte()
                ranks = self.client.tribeRanks.split(";")
                rank = ranks[rankID]
                rank2 = ranks[rankID2]
                ranks[rankID] = rank2
                ranks[rankID2] = rank
                self.client.tribeRanks = ";".join(map(str, ranks))
                self.updateTribeRanks()
                self.updateTribeData()
                up = (rankID2 > rankID)
                down = (rankID > rankID2)
                members = self.getTribeMembers(self.client.tribeCode)
                for member in members:
                    player = self.server.players.get(member)
                    if player != None:
                        if player.tribeRank == rankID:
                            player.tribeRank = rankID2
                            self.Cursor.execute("update users set TribeRank = %s where Username = %s", [rankID2, member])
                        if up:
                            if player.tribeRank == rankID2:
                                player.tribeRank -= 1
                                self.Cursor.execute("update users set TribeRank = %s where Username = %s", [rankID2 - 1, member])
                        if down:
                            if player.tribeRank == rankID2:
                                player.tribeRank += 1
                                self.Cursor.execute("update users set TribeRank = %s where Username = %s", [rankID2 + 1, member])
                    else:   
                        self.Cursor.execute("select TribeRank from users where Username = %s", [member])
                        rankPlayer = self.Cursor.fetchone()[0]

                        if rankPlayer == rankID:
                            self.Cursor.execute("update users set TribeRank = %s where Username = %s", [rankID2, member])
                        if up:
                            if rankPlayer == rankID2:
                                self.Cursor.execute("update users set TribeRank = %s where Username = %s", [rankID2 - 1, member])
                        if down:
                            if rankPlayer == rankID2:
                                self.Cursor.execute("update users set TribeRank = %s where Username = %s", [rankID2 + 1, member])
                    
                self.updateTribeRanks()
                self.updateTribeData()
                self.sendTribeInfo()
                self.client.isBlockAttack = False
                self.client.blockAttack()
                for member in members:
                    player = self.server.players.get(member)
                    if player != None:
                        if player.isTribeOpen:
                            player.tribulle.sendTribeInfo()

        def setRankPermition(self, packet):
            if self.client.isBlockAttack:
                tribulleID, rankID, permID, type = packet.readInt(), packet.readByte(), packet.readInt(), packet.readByte()
                rankInfo = self.client.tribeRanks.split(";")
                perms = rankInfo[rankID].split("|")
                soma = 0
                if type == 0:
                    soma = int(perms[2]) + 2**permID
                elif type == 1:
                    soma = int(perms[2]) - 2**permID
                perms[2] = str(soma)
                join = "|".join(map(str, perms))
                rankInfo[rankID] = join
                self.client.tribeRanks = ";".join(map(str, rankInfo))
                self.updateTribeRanks()
                self.updateTribeData()
                self.sendTribeInfo()
                self.client.isBlockAttack = False
                self.client.blockAttack()
                members = self.getTribeMembers(self.client.tribeCode)
                for member in members:
                    player = self.server.players.get(member)
                    if player != None:
                        if player.isTribeOpen:
                            player.tribulle.sendTribeInfo()

        def changeTribePlayerRank(self, packet):
            tribulleID, playerName, rankID = packet.readInt(), packet.readUTF(), packet.readByte()

            rankInfo = self.client.tribeRanks.split(";")
            rankName = rankInfo[rankID].split("|")[1]

            player = self.server.players.get(playerName)
            self.Cursor.execute("select Username, PlayerID, Gender, LastOn from Users where Username = %s", [playerName])
            rs = self.Cursor.fetchone()
            if player != None:
                player.tribeRank = rankID
                self.Cursor.execute("update users set TribeRank = %s where Username = %s", [rankID, playerName])
            else:
                self.Cursor.execute("update users set TribeRank = %s where Username = %s", [rankID, playerName])
            self.setTribeHistorique(self.client.tribeCode, 5, self.getTime(), playerName, str(rankID), rankName, self.client.playerName)
            self.sendPacket(131, ByteArray().writeInt(rs[1]).writeUTF(playerName.lower()).writeByte(rs[2]).writeInt(rs[1]).writeInt(0 if self.server.checkConnectedAccount(playerName) else rs[3]).writeByte(rankID).writeInt(1).writeUTF("" if player == None else player.roomName).toByteArray())
            self.sendPacketWholeTribe(124, ByteArray().writeUTF(self.client.playerName.lower()).writeUTF(playerName.lower()).writeUTF(rankName).toByteArray(), True)
            self.sendPacket(113, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
            members = self.getTribeMembers(self.client.tribeCode)
            for member in members:
                player = self.server.players.get(member)
                if player != None:
                    if player.isTribeOpen:
                        player.tribulle.sendTribeInfo()

        def showTribeHistorique(self, readPacket):
            tribulleID, sla, sla2 = readPacket.readInt(), readPacket.readInt(), readPacket.readInt()

            historique = self.getTribeHistorique(self.client.tribeCode).split("|")
            
            packet = ByteArray()
            packet.writeInt(tribulleID)
            packet.writeShort(len(historique) - 1 if historique == [''] else len(historique))
            for event in historique:
                event = event.split("/")
                if not historique == [''] and not event[1] == '':
                    packet.writeInt(event[1])
                    packet.writeInt(event[0])
                    if int(event[0]) == 8:
                        packet.writeUTF('{"code":"%s","auteur":"%s"}' % (event[3], event[2]))
                    elif int(event[0]) == 6:
                        try:
                            packet.writeUTF('{"message":"%s","auteur":"%s"}' % (event[2], event[3]))
                        except:
                            pass
                    elif int(event[0]) == 5:
                        packet.writeUTF('{"cible":"%s","ordreRang":"%s","rang":"%s","auteur":"%s"}' % (event[2], event[3], event[4], event[5]))
                    elif int(event[0]) == 4:
                        packet.writeUTF('{"membreParti":"%s","auteur":"%s"}' % (event[2], event[2]))
                    elif int(event[0]) == 3:
                        packet.writeUTF('{"membreExclu":"%s","auteur":"%s"}' % (event[2], event[3]))
                    elif int(event[0]) == 2:
                        packet.writeUTF('{"membreAjoute":"%s","auteur":"%s"}' % (event[3], event[2]))
                    elif int(event[0]) == 1:
                        packet.writeUTF('{"tribu":"%s","auteur":"%s"}' % (event[3], event[2]))

            packet.writeInt(len(historique))
            
            self.sendPacket(133, packet.toByteArray())
    
        def leaveTribe(self, packet):
            tribulleID = packet.readInt()
            p = ByteArray().writeInt(tribulleID)

            if self.client.tribeRank == (len(self.client.tribeRanks.split(";"))-1):
                p.writeByte(4)
            else:
                p.writeByte(1)
                
                self.sendPacketWholeTribe(92, ByteArray().writeUTF(self.client.playerName.lower()).toByteArray(), True)

                members = self.getTribeMembers(self.client.tribeCode)
                if self.client.playerName in members:
                    members.remove(self.client.playerName)
                    self.setTribeMembers(self.client.tribeCode, members)

                    self.setTribeHistorique(self.client.tribeCode, 4, self.getTime(), self.client.playerName)
                    
                    self.client.tribeCode = 0
                    self.client.tribeName = ""
                    self.client.tribeRank = 0
                    self.client.tribeJoined = 0
                    self.client.tribeHouse = 0
                    self.client.tribeMessage = ""
                    self.client.tribeRanks = ""
                    self.client.tribeChat = 0
                for member in members:
                    player = self.server.players.get(member)
                    if player != None:
                        if player.isTribeOpen:
                            player.tribulle.sendTribeInfo()
            self.sendPacket(83, p.toByteArray())

        def kickPlayerTribe(self, packet):
            tribulleID, playerName = packet.readInt(), packet.readUTF()
            p = ByteArray().writeInt(tribulleID)
            player = self.server.players.get(playerName)

            tribeCode = player.tribeCode if player != None else self.getPlayerTribeCode(playerName)

            if tribeCode != 0:
                p.writeByte(1)
                members = self.getTribeMembers(self.client.tribeCode)
                if playerName in members:
                    members.remove(playerName)
                    self.setTribeMembers(self.client.tribeCode, members)
                    
                    self.setTribeHistorique(self.client.tribeCode, 3, self.getTime(), playerName, self.client.playerName)
                    self.sendPacketWholeTribe(93, ByteArray().writeUTF(playerName.lower()).writeUTF(self.client.playerName.lower()).toByteArray(), True)

                    if player != None:
                        player.tribeCode = 0
                        player.tribeName = ""
                        player.tribeRank = 0
                        player.tribeJoined = 0
                        player.tribeHouse = 0
                        player.tribeMessage = ""
                        player.tribeRanks = ""
                        player.tribeChat = 0
                    else:
                        self.Cursor.execute("update users set TribeCode = 0, TribeRank = 0, TribeJoined = 0 where Username = %s", [playerName])
                members = self.getTribeMembers(self.client.tribeCode)
                for member in members:
                    player = self.server.players.get(member)
                    if player != None:
                        if player.isTribeOpen:
                            player.tribulle.sendTribeInfo()
            self.sendPacket(105, p.toByteArray())

        def setTribeMaster(self, packet):
            tribulleID, playerName = packet.readInt(), packet.readUTF()

            rankInfo = self.client.tribeRanks.split(";")
            self.client.tribeRank = (len(rankInfo)-2)
            self.Cursor.execute("update users set TribeRank = %s where Username = %s", [len(rankInfo)-2, self.client.playerName])
            player = self.server.players.get(playerName)
            if player != None:
                player.tribeRank = (len(rankInfo)-1)
                self.Cursor.execute("update users set TribeRank = %s where Username = %s", [len(rankInfo)-1, playerName])
            else:
                self.Cursor.execute("update users set TribeRank = %s where Username = %s", [len(rankInfo)-1, playerName])
            self.Cursor.execute("select Username, PlayerID, Gender, LastOn from Users where Username = %s", [playerName])
            rs = self.Cursor.fetchone()
            self.sendPacket(131, ByteArray().writeInt(rs[1]).writeUTF(playerName.lower()).writeByte(rs[2]).writeInt(rs[1]).writeInt(0 if self.server.checkConnectedAccount(playerName) else rs[3]).writeByte(len(rankInfo)-1).writeInt(4).writeUTF("" if player == None else player.roomName).toByteArray())
            self.sendPacket(131, ByteArray().writeInt(self.client.playerID).writeUTF(self.client.playerName.lower()).writeByte(self.client.gender).writeInt(self.client.playerID).writeInt(0).writeByte(len(rankInfo)-2).writeInt(4).writeUTF(self.client.roomName).toByteArray())
            self.sendPacket(127, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
            members = self.getTribeMembers(self.client.tribeCode)
            for member in members:
                player = self.server.players.get(member)
                if player != None:
                    if player.isTribeOpen:
                        player.tribulle.sendTribeInfo()

        def finishTribe(self, packet):
            tribulleID = packet.readInt()
            p = ByteArray()
            p.writeInt(tribulleID).writeByte(1)
            members = self.getTribeMembers(self.client.tribeCode)
            self.Cursor.execute("update users set TribeCode = 0, TribeRank = 0, TribeJoined = 0 where TribeCode = %s", [self.client.tribeCode])
            self.Cursor.execute("delete from Tribe where Code = %s", [self.client.tribeCode])
            for member in members:
                player = self.server.players.get(member)
                if player != None:
                    player.tribulle.sendPacket(93, ByteArray().writeUTF(player.playerName.lower()).writeUTF(self.client.playerName.lower()).toByteArray())
                    player.tribeCode, player.tribeRank, player.tribeJoined, player.tribeHouse, player.tribeChat, player.tribeRankID = 0, 0, 0, 0, 0, 0
                    player.tribeMessage, player.tribeName = "", ""
                    player.tribeRanks = ""
                    player.tribeInvite = []
                    player.tribulle.sendPacket(127, p.toByteArray())
                self.client.sendPacket([6, 9], ByteArray().writeUTF("Tribe distributed.").toByteArray())

        def customChat(self, packet):
            tribulleID, chatName = packet.readInt(), packet.readUTF()

            if re.match("^[ a-zA-Z0-9]*$", chatName):
                chatID = self.getChatID(chatName)
                if chatID == -1:
                    chatID = self.server.lastChatID + 1
                    self.server.configs("ids.lastChatID", str(chatID))
                    self.Cursor.execute("insert into Chats (ID, Name) values (%s, %s)", [chatID, chatName])

                chatID = self.getChatID(chatName)

                self.client.chats.append(chatID)
                self.sendPacket(62, ByteArray().writeUTF(chatName).toByteArray())
                self.sendPacket(55, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
            else:
                self.sendPacket(55, ByteArray().writeInt(tribulleID).writeByte(8).toByteArray())

        
            
        def chatMessage(self, packet):
            tribulleID, chatName, message = packet.readInt(), packet.readUTF(), packet.readUTF()
            chatID = self.getChatID(chatName)
            self.sendPacketWholeChat(chatID, 64, ByteArray().writeUTF(self.client.playerName.lower()).writeInt(self.client.langueID+1).writeUTF(chatName).writeUTF(message).toByteArray(), True)
            self.sendPacket(49, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
            #self.client.sendWhisperMessageAdmin(1, "[<J>%s</J>] [<J>%s</J>] [<J>CHAT</J>] - %s => %s" %(self.client.ipAddress, chatName, self.client.playerName, message))
            
        def chatMembersList(self, packet):
            tribulleID, chatName = packet.readInt(), packet.readUTF()
            p = ByteArray().writeInt(tribulleID).writeByte(1)
            chatID = self.getChatID(chatName)
            length = 0
            for player in self.server.players.values():
                if chatID in player.chats:
                    length += 1
            p.writeShort(length)

            for player in self.server.players.values():
                if chatID in player.chats:
                    p.writeUTF(player.playerName)
            self.sendPacket(59, p.toByteArray())

        def sendTribeChatMessage(self, readPacket):
            tribulleID, message = readPacket.readInt(), readPacket.readUTF()
            self.sendPacketWholeTribe(65, ByteArray().writeUTF(self.client.playerName.lower()).writeUTF(message).toByteArray(), True)
            #self.client.sendWhisperMessageAdmin(1, "[TRIBECHAT] [<J>%s</J>] - [<J>%s</J>] - [%s]: <CH>%s" %(self.client.ipAddress, self.client.tribeName, self.client.playerName, message))

        def getGenderID(self, genderID, isFriendToo, isMarriedWithMe):
            dictionary = {0:{0:{0:0, 1:1}, 1:{0:2, 1:3}}, 1:{0:{0:4, 1:5}, 1:{0:6, 1:7}}, 2:{0:{0:8, 1:9}, 1:{0:10, 1:11}}}
            return dictionary[genderID][int(isMarriedWithMe)][int(isFriendToo)]

        def getPlayerLastOn(self, playerName):
            player = self.server.players.get(playerName)
            if player != None:
                return self.server.players[playerName].lastOn
            else:
                self.Cursor.execute("select LastOn from Users where Username = %s", [playerName])
                rs = self.Cursor.fetchone()
                if rs:
                    return rs[0]
                else:
                    return 0

        def checkFriend(self, playerName, playerNameToCheck):
            checkList = self.server.players[playerName].friendsList if playerName in self.server.players else self.getUserFriends(playerName)
            return playerNameToCheck in checkList

        def getUserFriends(self, playerName):
            self.Cursor.execute("select FriendsList from Users where Username = %s", [playerName])
            rs = self.Cursor.fetchone()
            if rs:
                return rs[0]
            else:
                return []

        def getPlayerGender(self, playerName):
            self.Cursor.execute("select Gender from Users where Username = %s", [playerName])
            rs = self.Cursor.fetchone()
            if rs:
                return rs[0]
            else:
                return 0

        def getPlayerTribeRank(self, playerName):
            self.Cursor.execute("select TribeRank from users where Username = %s", [playerName])
            rs = self.Cursor.fetchone()
            if rs:
                return rs[0]
            else:
                return 0

        def getPlayerMarriage(self, playerName):
            self.Cursor.execute("select Marriage from Users where Username = %s", [playerName])
            rs = self.Cursor.fetchone()
            if rs:
                return rs[0]
            else:
                return ""

        def removeMarriage(self, playerName, time):
            self.Cursor.execute("update Users set Marriage = '', LastDivorceTimer = %s where Username = %s", [time, playerName])

        def getInGenderMarriage(self, playerName):
            if playerName in self.server.players:
                player = self.server.players.get(playerName)
                gender = player.gender
                marriage = player.marriage
            else:
                gender = self.getPlayerGender(playerName)
                marriage = self.getPlayerMarriage(playerName)
            return (5 if gender == 1 else 9 if gender == 2 else 1) if marriage == "" else (7 if gender == 1 else 11 if gender == 2 else 3)

        def getInGendersMarriage(self, marriage, gender):
            return (5 if gender == 1 else 9 if gender == 2 else 1) if marriage == "" else (7 if gender == 1 else 11 if gender == 2 else 3)

        def updateTribeRanks(self):
            self.Cursor.execute("update tribe set Ranks = %s where Code = %s", [self.client.tribeRanks, self.client.tribeCode])

        def getTribeMembers(self, tribeCode):
            self.Cursor.execute("select Members from Tribe where Code = %s", [tribeCode])
            rs = self.Cursor.fetchone()
            if rs:
                return rs[0].split(",")
            else:
                return []

        def setTribeMembers(self, tribeCode, members):
            self.Cursor.execute("update Tribe set Members = %s where Code = %s", [",".join(map(str, members)), tribeCode])

        def checkExistingTribe(self, tribeName):
            self.Cursor.execute("select 1 from Tribe where Name = %s", [tribeName])
            return self.Cursor.fetchone() != None

        def checkExistingTribeRank(self, rankName):
            for rank in self.client.tribeRanks.values():
                checkRankName = rank.split("|")[0]
                if checkRankName == rankName:
                    return True
            return False

        def getTribeHistorique(self, tribeCode):
            self.Cursor.execute("select Historique from Tribe where Code = %s", [tribeCode])
            rs = self.Cursor.fetchone()
            if rs:
                return rs[0]
            else:
                return ""

        def setTribeCache(self, tribeCode, historique):
            self.Cursor.execute("update Tribe set historique = %s where Code = %s", [historique, tribeCode])

        def setTribeHistorique(self, tribeCode, *data):
            historique = self.getTribeHistorique(tribeCode)
            if historique == "":
                historique = "/".join(map(str, data))
            else:
                historique = "/".join(map(str, data)) + "|" + historique
            self.setTribeCache(tribeCode, historique)

        def getChatID(self, chatName):
            self.Cursor.execute("select ID from Chats where Name = %s", [chatName])
            rs = self.Cursor.fetchone()
            if rs:
                return rs[0]
            else:
                return -1

        def getPlayerTribeCode(self, playerName):
            self.Cursor.execute("select TribeCode from users where Username = %s", [playerName])
            rs = self.Cursor.fetchone()
            if rs:
                return rs[0]
            else:
                return 0

        def getTribeInfo(self, tribeCode):
            tribeRanks = ""
            self.Cursor.execute("select * from tribe where Code = %s", [tribeCode])
            rs = self.Cursor.fetchone()
            if rs:
                tribeRanks = rs[4]
                return [rs[1], rs[2], rs[3], tribeRanks, rs[7]]
            else:
                return ["", "", 0, tribeRanks, 0]
    except:
        with open("./logs/Errors/Tribulle.log", "a") as f:
            traceback.print_exc(file=f)
            f.write("\n")
        pass
