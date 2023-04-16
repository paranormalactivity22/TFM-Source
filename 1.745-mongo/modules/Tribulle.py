#coding: utf-8
import re, time as _time

# Modules
from ByteArray import ByteArray
from Identifiers import Identifiers

# Utils
from utils import Utils

# Library
from collections import deque

class Tribulle:
    def __init__(self, player, server):
        self.client = player
        self.server = player.server
        self.Cursor = player.Cursor

        self.TRIBE_RANKS = "0|${trad#TG_0}|0;0|${trad#TG_1}|0;2|${trad#TG_2}|0;3|${trad#TG_3}|0;4|${trad#TG_4}|32;5|${trad#TG_5}|160;6|${trad#TG_6}|416;7|${trad#TG_7}|932;8|${trad#TG_8}|2044;9|${trad#TG_9}|2046"

    def getTime(self):
        return int(_time.time() // 60)

    def sendPacket(self, code, result):
        self.client.sendPacket(Identifiers.send.Tribulle, ByteArray().writeShort(code).writeBytes(result).toByteArray())

    def sendPacketToPlayer(self, playerName, code, result):
        player = self.server.players.get(playerName)
        if player != None:
            player.tribulle.sendPacket(code, result)

    def sendPacketWholeTribe(self, code, result, all=False):
        for player in self.server.players.copy().values():
            if player.playerCode != self.client.playerCode or all:
                if player.tribeCode == self.client.tribeCode:
                    player.tribulle.sendPacket(code, result)

    def sendPacketWholeChat(self, chatName, code, result, all=False):
        for player in self.server.players.copy().values():
            if player.playerCode != self.client.playerCode or all:
                if player.playerName in self.server.chats[chatName]:
                    player.tribulle.sendPacket(code, result)

    def updateTribeData(self):
        for player in self.server.players.copy().values():
            if player.tribeCode == self.client.tribeCode:
                player.tribeHouse = self.client.tribeHouse
                player.tribeMessage = self.client.tribeMessage
                player.tribeRanks = self.client.tribeRanks

    def parseTribulleCode(self, code, packet):
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
            self.server.loop.create_task(self.changeTribeCode(packet))
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
        elif code == 56:
            self.leaveChat(packet)
        elif code == 48:
            self.chatMessage(packet)
        elif code == 58:
            self.chatMembersList(packet)
        elif code == 50:
            self.sendTribeChatMessage(packet)
        else:
            if self.server.isDebug:
                print("[%s] [WARN][%s] Invalid tribulle code -> Code: %s packet: %s" %(_time.strftime("%H:%M:%S"), self.client.playerName, code, repr(packet.toByteArray())))

    def platformAuthentication(self, status):
        self.client.sendPacket(Identifiers.send.New_Tribulle, ByteArray().writeBoolean(status).toByteArray())

    def sendFriendsList(self, readPacket):
        p = ByteArray().writeShort(3 if readPacket == None else 34)
        if readPacket == None:
            p.writeByte(self.client.gender).writeInt(self.client.playerID)
        if self.client.marriage == "":
            p.writeInt(0).writeUTF("").writeByte(0).writeInt(0).writeByte(0).writeByte(0).writeInt(1).writeUTF("").writeInt(0)
        else:
            player = self.server.players.get(self.client.marriage)
            if player == None:
                rs = self.Cursor['users'].find_one({'Username':self.client.marriage})
            else:
                rs = {'Marriage':self.client.marriage, 'PlayerID': player.playerID, 'Gender': player.gender, 'LastOn': player.lastOn}
            p.writeInt(rs['PlayerID']).writeUTF(rs['Marriage'].lower()).writeByte(rs['Gender']).writeInt(rs['PlayerID']).writeByte(1).writeBoolean(self.server.checkConnectedAccount(rs['Marriage'])).writeInt(4).writeUTF(player.roomName if player else "").writeInt(rs['LastOn'])
        self.client.openingFriendList = readPacket != None
        isOnline = []
        friendsOn = []
        friendsOff = []
        isOffline = []
        infos = {}
        friendsList = self.client.friendsList.copy()
        for friend in friendsList:
            player = self.server.players.get(friend)
            if player != None:
                infos[friend] = [player.playerID, ",".join(player.friendsList), player.marriage, player.gender, player.lastOn]
                isFriend = self.client.playerName in player.friendsList
                if isFriend:
                    friendsOn.append(friend)
                else:
                    isOnline.append(friend)
                friendsList.remove(friend)

        for name in friendsList:
            for rs in self.Cursor['users'].find({'Username':name}):
                infos[rs['Username']] = [rs['PlayerID'], rs['FriendsList'], rs['Marriage'], rs['Gender'], rs['LastOn']]
                isFriend = self.client.playerID in map(int, filter(None, rs['FriendsList'].split(",")))
                if isFriend:
                    friendsOff.append(rs['Username'])
                else:
                    isOffline.append(rs['Username'])

        playersNames = friendsOn + isOnline + friendsOff + isOffline
        if "" in playersNames:
            playersNames.remove("")
        if "" in self.client.ignoredsList:
            self.client.ignoredsList.remove("")
        p.writeShort(len(playersNames))
        for playerName in playersNames:
            if not playerName in infos:
                continue

            info = infos[playerName]
            player = self.server.players.get(playerName)
            isFriend = self.client.playerName in player.friendsList if player != None else self.client.playerID in map(int, filter(None, info[1].split(",")))
            genderID = player.gender if player else int(info[3])
            isMarriage = self.client.playerName == player.marriage if player else info[2] == self.client.playerName
            p.writeInt(info[0]).writeUTF(playerName.lower()).writeByte(genderID).writeInt(info[0]).writeByte(1 if isFriend else 0).writeBoolean(self.server.checkConnectedAccount(playerName)).writeInt(4 if isFriend and player != None else 1).writeUTF(player.roomName if isFriend and player != None else "").writeInt(info[4] if isFriend else 0)
        if readPacket == None:
            p.writeShort(len(self.client.ignoredsList))

            for playerName in self.client.ignoredsList:
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

    def closeFriendsList(self, readPacket):
        self.client.openingFriendList = False
        self.sendPacket(31, ByteArray().writeBytes(readPacket.toByteArray()).writeByte(1).toByteArray())

    def addFriend(self, readPacket):
        tribulleID, playerName = readPacket.readInt(), Utils.parsePlayerName(readPacket.readUTF())
        if len(self.client.friendsList) >= 200:
            self.sendPacket(19, ByteArray().writeInt(tribulleID).writeByte(7).toByteArray())
            return
        elif not self.server.checkExistingUser(playerName):
            self.sendPacket(19, ByteArray().writeInt(tribulleID).writeByte(12).toByteArray())
            return
        elif playerName == self.client.playerName or playerName in self.client.friendsList:
            self.sendPacket(19, ByteArray().writeInt(tribulleID).writeByte(4).toByteArray())
            return

        player = self.server.players.get(playerName)
        isFriend = self.checkFriend(playerName, self.client.playerName)
        if not player:
            rss = self.Cursor['users'].find_one({'Username':playerName})
            rs = [playerName, rss['PlayerID'], rss['Gender'], rss['LastOn']]
        else:
            rs = [playerName, player.playerID, player.gender, player.lastOn]

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
            player = self.server.players.get(playerName)
            self.sendPacket(35, ByteArray().writeInt(player.playerID).writeUTF(playerName.lower()).writeByte(player.gender).writeInt(player.playerID).writeByte(1).writeByte(1).writeInt(1).writeUTF("").writeInt(player.lastOn).toByteArray())
            self.sendPacket(32, ByteArray().writeUTF(player.playerName.lower()).toByteArray())

    def sendFriendChangedRoom(self, playerName, langueID):
        if playerName in self.client.friendsList:
            player = self.server.players.get(playerName)
            if player == None:
                 return
            self.sendPacket(35, ByteArray().writeInt(player.playerID).writeUTF(playerName.lower()).writeByte(player.gender).writeInt(player.playerID).writeByte(1).writeByte(1).writeInt(4).writeUTF(player.roomName).writeInt(player.lastOn).toByteArray())

    def sendFriendDisconnected(self, playerName):
        if playerName in self.client.friendsList:
            player = self.server.players.get(playerName)
            if not player:
                rss = self.Cursor['users'].find_one({'Username':playerName})
                if rs == None:
                    return
                rs = [rss['Username'],rss['PlayerID'],rss['Gender'],rss['LastOn']]
            else:
                rs = [playerName, player.gender, player.lastOn]
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
        packet = ByteArray().writeInt(tribulleID)

        if len(self.client.ignoredsList) >= 200:
            self.sendPacket(43, packet.writeByte(7).toByteArray())
            return
        elif not self.server.checkExistingUser(playerName):
            self.sendPacket(43, packet.writeByte(12).toByteArray())
            return
        elif playerName == self.client.playerName or playerName in self.client.ignoredsList:
            self.sendPacket(43, packet.writeByte(4).toByteArray())
            return

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

        if message in ["\n", "\r", chr(2), "<BR>", "<br>"]:
            self.server.sendServerMessage("<font color='#00C0FF'>[ANTI-BOT] - Suspect BOT - IP: [</font><J>%s<font color='#00C0FF'>]</font>" % self.client.ipAddress)
            self.client.transport.close()
            return

        if self.client.isGuest:
            self.client.sendLangueMessage("", "$Créer_Compte_Parler")
        elif not message == "":
            can = True

            packet = ByteArray().writeInt(tribulleID)
            if playerName.startswith("*") or not playerName in self.server.players:
                can = False
                packet.writeByte(11)
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
                        if (self.client.privLevel >= 7 or (player.silenceType == 1 and self.checkFriend(playerName, self.client.playerName))):
                            pass
                        else:
                            self.sendSilenceMessage(playerName, tribulleID)
                            return

                    if not (self.client.playerName in player.ignoredsList) and not isCheck and playerName != self.client.playerName:
                        player.tribulle.sendPacket(66, ByteArray().writeUTF(self.client.playerName.lower()).writeInt(self.client.langueID+1).writeUTF(player.playerName.lower()).writeUTF(message).toByteArray())
                    self.sendPacket(66, ByteArray().writeUTF(self.client.playerName.lower()).writeInt(player.langueID+1).writeUTF(player.playerName.lower()).writeUTF(message).toByteArray())

                    if isCheck:
                        self.server.sendServerMessage("<V>%s<BL> is whispering to <V>%s<BL> with suspicious words. [<R>%s<BL>]." %(self.client.playerName, playerName, message))

                    if not self.client.playerName in self.server.chatMessages:
                         messages = deque([], 60)
                         messages.append([_time.strftime("%Y/%m/%d %H:%M:%S"), message, self.client.roomName])
                         self.server.chatMessages[self.client.playerName] = {}
                         self.server.chatMessages[self.client.playerName][player.playerName] = messages
                    elif not player.playerName in self.server.chatMessages[self.client.playerName]:
                        messages = deque([], 60)
                        messages.append([_time.strftime("%Y/%m/%d %H:%M:%S"), message, self.client.roomName])
                        self.server.chatMessages[self.client.playerName][player.playerName] = messages
                    else:
                         self.server.chatMessages[self.client.playerName].append([_time.strftime("%Y/%m/%d %H:%M:%S"), message, self.client.roomName])

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
        self.sendPacket(11, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
        self.sendPacket(12, ByteArray().writeByte(gender).toByteArray())
        for player in self.server.players.copy().values():
            if player.playerName in self.client.friendsList and self.client.playerName in player.friendsList:
                if player.openingFriendList:
                    player.tribulle.sendFriendsList("0")

    def marriageInvite(self, readPacket):
        tribulleID, playerName = readPacket.readInt(), Utils.parsePlayerName(readPacket.readUTF())
        packet = ByteArray().writeInt(tribulleID)

        player = self.server.players.get(playerName)
        if not self.server.checkConnectedAccount(playerName) or not self.server.checkExistingUser(playerName):
            self.sendPacket(23, packet.writeByte(11).toByteArray())
        elif not player.marriage == "":
            self.sendPacket(23, packet.writeByte(14).toByteArray())
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
            self.removeMarriage(self.client.marriage)

        self.client.marriage = ""
        self.client.lastDivorceTimer = time

    def sendTribe(self, isNew):
        if self.client.tribeName == "":
            self.sendPacket(87, ByteArray().writeInt(0).writeByte(0).toByteArray())
            return

        if not self.client.tribeChat in self.client.chats:
            self.client.chats.append(self.client.tribeChat)

        self.sendPacket(27, ByteArray().writeInt(self.client.tribeChat).writeUTF("~" + self.client.tribeName.lower()).writeBytes(chr(0) * 5).toByteArray())
        self.sendPacketWholeTribe(29, ByteArray().writeInt(self.client.tribeChat).writeInt(self.client.playerID).writeUTF(self.client.playerName.lower()).toByteArray())
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
        for member in members:
            player = self.server.players.get(member)
            if player != None:
                infos[playerName] = [player.playerID, player.gender, player.lastOn, player.tribeRank, player.tribeJoined]
                members.remove(member)

        for member in members:
            rs = self.Cursor['users'].find_one({'Username':member})
            infos[member] = [rs['PlayerID'], rs['Gender'], rs['LastOn'], rs['TribeRank'], rs['TribeJoined']]

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

        isOnline = []
        isOffline = []
        infos = {}
        for member in members:
            rs = self.Cursor['users'].find_one({'Username':member})
            infos[member] = [rs['PlayerID'], rs['Gender'], rs['LastOn'], rs['TribeRank'], rs['TribeJoined']]
            isOffline.append(member)

        for member in members:
            player = self.server.players.get(member)
            if player != None:
                infos[member] = [player.playerID, player.gender, player.lastOn, player.tribeRank, player.tribeJoined]
                isOnline.append(member)
                isOffline.remove(member)

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
        self.client.isTribeOpen = True

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
        self.sendPacket(166, ByteArray().writeInt(0).writeInt(self.client.playerID).writeInt(self.client.playerID).writeInt(self.getInGenderMarriage(self.client.playerName)).writeInt(self.server.getPlayerID(self.client.marriage) if not self.client.marriage == "" else 0).writeUTF(self.client.marriage).toByteArray())

    def createTribe(self, readPacket):
        if self.client.tribeCode != 0: return
        tribulleID, tribeName = readPacket.readInt(), readPacket.readUTF()

        if tribeName == "" or not re.match("^[ a-zA-Z0-9]*$", tribeName) or "<" in tribeName or ">" in tribeName:
            self.sendPacket(85, ByteArray().writeInt(tribulleID).writeByte(8).toByteArray())
        elif self.checkExistingTribe(tribeName):
            self.sendPacket(85, ByteArray().writeInt(tribulleID).writeByte(9).toByteArray())
        elif self.client.shopCheeses < 500:
            self.sendPacket(85, ByteArray().writeInt(tribulleID).writeByte(14).toByteArray())
        else:
            self.sendPacket(85, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
            createTime = self.getTime()
            self.server.lastTribeID += 1
            self.Cursor['tribe'].insert_one({'Code':self.server.lastTribeID, 'Name': tribeName, 'Message': '', 'House': 0, 'Ranks': self.TRIBE_RANKS, 'Historique': '', 'Members': str(self.client.playerID), 'Chat': 0, 'Points': 0, 'createTime': createTime})
            self.client.shopCheeses -= 500
            self.client.tribeCode = self.server.lastTribeID
            self.client.tribeRank = 9
            self.client.tribeName = tribeName
            self.client.tribeJoined = createTime
            self.client.tribeMessage = ""
            self.client.tribeRanks = self.TRIBE_RANKS

            self.setTribeHistorique(self.client.tribeCode, 1, createTime, self.client.playerName, tribeName)

            self.sendPacket(89, ByteArray().writeUTF(self.client.tribeName).writeInt(self.client.tribeCode).writeUTF(self.client.tribeMessage).writeInt(0).writeUTF(self.client.tribeRanks.split(";")[9].split("|")[1]).writeInt(2049).toByteArray())

    def tribeInvite(self, readPacket):
        tribulleID, playerName = readPacket.readInt(), Utils.parsePlayerName(readPacket.readUTF())

        player = self.server.players.get(playerName)
        if len(self.getTribeMembers(self.client.tribeCode)) >= 1000:
            self.sendPacket(79, ByteArray().writeInt(tribulleID).writeByte(7).toByteArray())
        elif playerName.startswith("*") or player == None or playerName == self.client.playerName:
            self.sendPacket(79, ByteArray().writeInt(tribulleID).writeByte(11).toByteArray())
        elif player.tribeName != "":
            self.sendPacket(79, ByteArray().writeInt(tribulleID).writeByte(18).toByteArray())
        elif len(player.tribeInvite) != 0:
            self.sendPacket(79, ByteArray().writeInt(tribulleID).writeByte(6).toByteArray())
        elif not self.client.tribeCode in player.ignoredTribeInvites:
            player.tribeInvite = [tribulleID, self.client]
            player.tribulle.sendPacket(86, ByteArray().writeUTF(self.client.playerName.lower()).writeUTF(self.client.tribeName).toByteArray())
            self.sendPacket(79, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())

    def tribeInviteAnswer(self, readPacket):
        tribulleID, playerName, answer = readPacket.readInt(), readPacket.readUTF(), readPacket.readByte()
        resultTribulleID = int(self.client.tribeInvite[0])
        player = self.client.tribeInvite[1]
        self.client.tribeInvite = []

        if self.client.tribeCode != 0:
            self.sendPacket(81, ByteArray().writeInt(tribulleID).writeByte(18).toByteArray())
        elif player == None:
            self.sendPacket(81, ByteArray().writeInt(tribulleID).writeByte(17).toByteArray())
        elif len(self.getTribeMembers(player.tribeCode)) >= 1000:
            self.sendPacket(81, ByteArray().writeInt(tribulleID).writeByte(7).toByteArray())
        else:
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
                self.client.updateDatabase()
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
        if len(message) > 500:
            self.sendPacket(99, ByteArray().writeInt(tribulleID).writeByte(22).toByteArray())
            return

        self.Cursor['tribe'].update_one({'Code':self.client.tribeCode},{'$set':{'Message':message}})
        self.client.tribeMessage = message
        self.setTribeHistorique(self.client.tribeCode, 6, self.getTime(), message, self.client.playerName)
        self.updateTribeData()
        self.sendTribeInfo()
        self.sendPacketWholeTribe(125, ByteArray().writeUTF(self.client.playerName.lower()).writeUTF(message).toByteArray(), True)

    async def changeTribeCode(self, readPacket):
        tribulleID, mapCode = readPacket.readInt(), readPacket.readInt()
        self.Cursor['tribe'].update_one({'Code':self.client.tribeCode},{'$set':{'House':mapCode}})

        mapInfo = await self.client.room.getMapInfo(mapCode)
        if mapInfo[0] == None:
            self.client.sendPacket(Identifiers.old.send.Tribe_Result, [16])
        elif mapInfo[4] != 22:
            self.client.sendPacket(Identifiers.old.send.Tribe_Result, [17])

        elif mapInfo[0] != None and mapInfo[4] == 22:
            self.setTribeHistorique(self.client.tribeCode, 8, self.getTime(), self.client.playerName, mapCode)

        room = self.server.rooms.get("*\x03" + self.client.tribeName)
        if room != None:
            await room.mapChange()

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
            else:
                if tribeRank >= 1:
                    self.Cursor['users'].update_one({'Username':playerName},{'$set':{'TribeRank':tribeRank+1}})

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
                    self.Cursor['users'].update_one({'Username':playerName},{'$set':{'TribeRank':0}})
                else:
                    continue
            else:
                tribeRank = self.getPlayerTribeRank(playerName)
                if tribeRank == rankID:
                    self.Cursor['users'].update_one({'Username':playerName},{'$set':{'TribeRank':0}})
                else:
                    continue
        for playerName in members:
            player = self.server.players.get(playerName)
            tribeRank = self.getPlayerTribeRank(playerName)
            if player != None:
                if player.tribeRank >= 1:
                    player.tribeRank -= 1
            else:
                if tribeRank >= 1:
                    self.Cursor['users'].update_one({'Username':playerName},{'$set':{'TribeRank':tribeRank-1}})
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
                if up:
                    if player.tribeRank == rankID2:
                        player.tribeRank -= 1
                if down:
                    if player.tribeRank == rankID2:
                        player.tribeRank += 1
            else:
                rankPlayer = self.Cursor['users'].find_one({'Username':member})['TribeRank']

                if rankPlayer == rankID:
                    self.Cursor['users'].update_one({'Username':member},{'$set':{'TribeRank':rankID2}})
                if up:
                    if rankPlayer == rankID2:
                        self.Cursor['users'].update_one({'Username':member},{'$set':{'TribeRank':rankID2-1}})
                if down:
                    if rankPlayer == rankID2:
                        self.Cursor['users'].update_one({'Username':member},{'$set':{'TribeRank':rankID2+1}})

        self.updateTribeRanks()
        self.updateTribeData()
        self.sendTribeInfo()
        for member in members:
            player = self.server.players.get(member)
            if player != None:
                if player.isTribeOpen:
                    player.tribulle.sendTribeInfo()

    def setRankPermition(self, packet):
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
        if not player:
            rss = self.Cursor['users'].find_one({'Username':playerName})
            rs = [rss['Username'],rss['PlayerID'],rss['Gender'],rss['LastOn']]
            self.Cursor['users'].update_one({'Username':playerName},{'$set':{'TribeRank':rankID}})
        else:
            rs = [playerName, player.playerID, player.gender, player.lastOn]
            player.tribeRank = rankID
            self.Cursor['users'].update_one({'Username':playerName},{'$set':{'TribeRank':rankID}})

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
                    packet.writeUTF('{"message":"%s","auteur":"%s"}' % (event[2], event[3]))
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
                    self.Cursor['users'].update_one({'Username':playerName},{'$set':{'TribeRank':0,'TribeCode':0,'TribeJoined':0}})
                else:
                    self.Cursor['users'].update_one({'Username':playerName},{'$set':{'TribeRank':0,'TribeCode':0,'TribeJoined':0}})

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
        player = self.server.players.get(playerName)
        if player:
            player.tribeRank = (len(rankInfo)-1)
            rs = [playerName, player.playerID, player.gender, player.lastOn]
        else:
            self.Cursor['users'].update_one({'Username':playerName},{'$set':{'TribeRank':len(rankInfo)-1}})
            rss = self.Cursor['users'].find_one({'Username':playerName})
            rs = [rss['Username'],rss['PlayerID'],rss['Gender'],rss['LastOn']]

        self.sendPacket(131, ByteArray().writeInt(rs[1]).writeUTF(playerName.lower()).writeByte(rs[2]).writeInt(rs[1]).writeInt(0 if self.server.checkConnectedAccount(playerName) else rs[3]).writeByte(len(rankInfo)-1).writeInt(4).writeUTF("" if player == None else player.roomName).toByteArray())
        self.sendPacket(131, ByteArray().writeInt(self.client.playerID).writeUTF(self.client.playerName.lower()).writeByte(self.client.gender).writeInt(self.client.playerID).writeInt(0).writeByte(len(rankInfo)-2).writeInt(4).writeUTF(self.client.roomName).toByteArray())
        self.sendPacket(127, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
        members = self.getTribeMembers(self.client.tribeCode)
        for member in members:
            player = self.server.players.get(member)
            if player != None:
                if player.isTribeOpen:
                    player.tribulle.sendTribeInfo()
                    self.Cursor['users'].update_one({'Username':playerName},{'$set':{'TribeRank':len(rankInfo)-1}})
                    

    def finishTribe(self, packet):
        tribulleID = packet.readInt()
        p = ByteArray()
        p.writeInt(tribulleID).writeByte(1)
        members = self.getTribeMembers(self.client.tribeCode)
        for member in members:
            player = self.server.players.get(member)
            if player:
                player.tribeCode = 0
                player.tribeRank = 0
                player.tribeJoined = 0
                player.tribeHouse = 0
                player.tribeChat = 0
                player.tribeRankID = 0
                player.tribeMessage = ""
                player.tribeName = ""
                player.tribeRanks = ""
                player.tribeInvite = []
                player.tribulle.sendPacket(93, ByteArray().writeUTF(player.playerName.lower()).writeUTF(self.client.playerName.lower()).toByteArray())
                self.Cursor['users'].update({'TribeCode':self.client.tribeCode},{'$set':{'TribeCode':0,'TribeRank':0,'TribeJoined':0}})
                if player != self.client:
                    player.tribulle.sendPacket(127, p.toByteArray())
                members.remove(member)
        if len(members) > 0:
            self.Cursor['users'].update({'TribeCode':self.client.tribeCode},{'$set':{'TribeCode':0,'TribeRank':0,'TribeJoined':0}})

        self.sendPacket(129, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
        self.Cursor['tribe'].remove({'Code':self.client.tribeCode})

    def customChat(self, packet):
        tribulleID, chatName = packet.readInt(), packet.readUTF()

        if chatName in self.server.chats and len(self.server.chats[chatName]) >= 100:
            self.sendPacket(55, ByteArray().writeInt(tribulleID).writeByte(7).toByteArray())
        if re.match("^(%s=^(%s:(%s!.*_$).)*$)(%s=^(%s:(%s!_{2,}).)*$)[A-Za-z][A-Za-z0-9_]{2,11}$", chatName):
            self.sendPacket(55, ByteArray().writeInt(tribulleID).writeByte(8).toByteArray())
        else:
            if chatName in self.server.chats and not self.client.playerName in self.server.chats[chatName]:
                self.server.chats[chatName].append(self.client.playerName)
            elif not chatName in self.server.chats:
                self.server.chats[chatName] = [self.client.playerName]

            self.sendPacket(62, ByteArray().writeUTF(chatName).toByteArray())
            self.sendPacket(55, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
        
    def leaveChat(self, packet):
        tribulleID, chatName = packet.readInt(), packet.readUTF()
        if chatName in self.server.chats and self.client.playerName in self.server.chats[chatName]:
            self.server.chats[chatName].remove(self.client.playerName)
            self.sendPacket(63, ByteArray().writeUTF(chatName).toByteArray())
            self.sendPacket(57, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())

    def chatMessage(self, packet):
        tribulleID, chatName, message = packet.readInt(), packet.readUTF(), packet.readUTF()
        self.sendPacketWholeChat(chatName, 64, ByteArray().writeUTF(self.client.playerName.lower()).writeInt(self.client.langueID+1).writeUTF(chatName).writeUTF(message).toByteArray(), True)
        self.sendPacket(49, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())

    def chatMembersList(self, packet):
        tribulleID, chatName = packet.readInt(), packet.readUTF()
        p = ByteArray().writeInt(tribulleID).writeByte(1).writeShort(len(self.server.chats[chatName]))

        for player in self.server.players.copy().values():
            if chatName in self.server.chats and self.client.playerName in self.server.chats[chatName]:
                p.writeUTF(player.playerName)
        self.sendPacket(59, p.toByteArray())

    def sendTribeChatMessage(self, readPacket):
        tribulleID, message = readPacket.readInt(), readPacket.readUTF()
        self.sendPacketWholeTribe(65, ByteArray().writeUTF(self.client.playerName.lower()).writeUTF(message).toByteArray(), True)

    def getGenderID(self, genderID, isFriendToo, isMarriedWithMe):
        dictionary = {0:{0:{0:0, 1:1}, 1:{0:2, 1:3}}, 1:{0:{0:4, 1:5}, 1:{0:6, 1:7}}, 2:{0:{0:8, 1:9}, 1:{0:10, 1:11}}}
        return dictionary[genderID][int(isMarriedWithMe)][int(isFriendToo)]

    def getPlayerLastOn(self, playerName):
        player = self.server.players.get(playerName)
        if player != None:
            return self.server.players[playerName].lastOn
        else:
            rs = self.Cursor['users'].find_one({'Username':playerName})
            if rs:
                return rs['LastOn']
            else:
                return 0

    def checkFriend(self, playerName, playerNameToCheck):
        checkList = self.server.players[playerName].friendsList if playerName in self.server.players else self.getUserFriends(playerName)
        return playerNameToCheck in checkList

    def getUserFriends(self, playerName):
        player = self.server.players.get(playerName)
        if player != None:
            return self.server.players[playerName].friendsList
        rs = self.Cursor['users'].find_one({'Username':playerName})
        if rs:
            return rs['FriendsList'].split(",")
        else:
            return []

    def getPlayerGender(self, playerName):
        player = self.server.players.get(playerName)
        if player != None:
            return self.server.players[playerName].gender
        rs = self.Cursor['users'].find_one({'Username':playerName})
        if rs:
            return rs['Gender']
        else:
            return 0

    def getPlayerTribeRank(self, playerName):
        player = self.server.players.get(playerName)
        if player != None:
            return self.server.players[playerName].tribeRank
        rs = self.Cursor['users'].find_one({'Username':playerName})
        if rs:
            return rs['TribeRank']
        else:
            return 0

    def getPlayerMarriage(self, playerName):
        player = self.server.players.get(playerName)
        if player != None:
            return self.server.players[playerName].marriage
        rs = self.Cursor['users'].find_one({'Username':playerName})
        if rs:
            return rs['Marriage']
        else:
            return ""

    def removeMarriage(self, playerName):
        player = self.server.players.get(playerName)
        if player != None:
            self.server.players[playerName].marriage = ''
        else:
            self.Cursor['users'].update_one({'Username':playerName},{'$set':{'Marriage':''}})

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
        self.Cursor['tribe'].update_one({'Code':self.client.tribeCode},{'$set':{'Ranks':self.client.tribeRanks}})

    def getTribeMembers(self, tribeCode):
        rs = self.Cursor['tribe'].find_one({'Code':tribeCode})
        if rs:
            _datas = map(int, rs['Members'].split(","))
            datas = []
            for data in _datas:
                datas.append(self.server.getPlayerName(data))
            return datas
        else:
            return []

    def setTribeMembers(self, tribeCode, members):
        self.Cursor['tribe'].update_one({'Code':tribeCode},{'$set':{'Members':",".join(map(str, [self.server.getPlayerID(member) for member in members]))}})

    def checkExistingTribe(self, tribeName):
        return self.Cursor['tribe'].find_one({'Name':tribeName}) != None

    def checkExistingTribeRank(self, rankName):
        for rank in self.client.tribeRanks.values():
            checkRankName = rank.split("|")[0]
            if checkRankName == rankName:
                return True
        return False

    def getTribeHistorique(self, tribeCode):
        rs = self.Cursor['tribe'].find_one({'Code':tribeCode})
        if rs:
            return rs['Historique']
        else:
            return ""

    def setTribeCache(self, tribeCode, historique):
        self.Cursor['tribe'].update_one({'Code':tribeCode},{'$set':{'Historique':historique}})

    def setTribeHistorique(self, tribeCode, *data):
        historique = self.getTribeHistorique(tribeCode)
        if historique == "":
            historique = "/".join(map(str, data))
        else:
            historique = "/".join(map(str, data)) + "|" + historique
        self.setTribeCache(tribeCode, historique)

    def getChatID(self, chatName):
        rs = self.Cursor['chats'].find_one({'Name':chatName})
        if rs:
            return rs['ID']
        else:
            return -1

    def getPlayerTribeCode(self, playerName):
        player = self.server.players.get(playerName)
        if playerName:
            return player.tribeCode

        rs = self.Cursor['users'].find_one({'Username':playerName})
        if rs:
            return rs['TribeCode']
        else:
            return 0

    def getTribeInfo(self, tribeCode):
        rs = self.Cursor['tribe'].find_one({'Code':tribeCode})
        if rs:
            return [rs['Name'], rs['Message'], rs['House'], rs['Ranks'], tribeCode]
        else:
            return ["", "", 0, self.TRIBE_RANKS, 0]
