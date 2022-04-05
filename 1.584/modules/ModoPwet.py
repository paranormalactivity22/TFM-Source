# -*- coding: iso-8859-15 -*-
from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers
import math

class ModoPwet:

    def __init__(self, player, server):
        self.client = player
        self.server = player.server
        self.isReportedType = ""
        self.isReported = False

    def checkReport(self, array, playerName):
        return playerName in array

    def ReportType(self, type):
        if type == 0: return "Hack"
        elif type == 1: return "Spam / Flood"
        elif type == 2: return "Insults"
        elif type == 3: return "Phishing"
        return "Other"

    def makeReport(self, playerName, type, comments):
        playerName = Utils.parsePlayerName(playerName)
        modName = self.client.playerName
        player = self.server.players.get(playerName)
        if player != None:
            player.isReportedType = type
            roomName = player.room.name
            self.server.reportedUsers.append(playerName)
            player.lastroom = roomName
            self.client.sendmodServerMessage("<ROSE>[Modopwet]</ROSE> The player <BV>%s</BV> has been reported for <N>%s</N> in room [%s] (<a href='event:modopwetfollow#%s'><FC>Follow</FC></a> - <a href='event:modopwetwatch#%s'><FC>Watch</FC></a>)." % (playerName,self.ReportType(type),roomName, playerName, playerName))
        
        if self.server.players.get(playerName):
            if playerName in self.server.reports:
                if modName in self.server.reports[playerName]['reporters']:
                    r = self.server.reports[playerName]['reporters'][modName]
                    if r[0] != type:
                        self.server.reports[playerName]['reporters'][modName]=[type,comments,Utils.getTime()]
                else:
                    self.server.reports[playerName]['reporters'][modName]=[type,comments,Utils.getTime()]
                self.server.reports[playerName]['state'] = 'online' if self.server.checkConnectedAccount(playerName) else 'disconnected'
            else:
                self.server.reports[playerName] = {}
                self.server.reports[playerName]['reporters'] = {modName:[type,comments,Utils.getTime()]}
                self.server.reports[playerName]['state'] = 'online' if self.server.checkConnectedAccount(playerName) else 'disconnected'
                self.server.reports[playerName]['language'] = self.getModopwetLangue(playerName)
                self.server.reports[playerName]['isMuted'] = False
            self.updateModoPwet()
            self.client.sendBanConsideration()
            
    def getModopwetLangue(self, playerName):
        player = self.server.players.get(playerName)
        if player != None:
            return player.langue
        else:
            return 0

    def updateModoPwet(self):
        for player in self.server.players.values():
            if player.isModoPwet and player.privLevel >= 7:
                player.modoPwet.openModoPwet(True)

    def getPlayerNotificationStatus(self, playerName):
        player = self.server.players.get(playerName)
        if player != None:
            return player.isReported
        else:
            return False

    def getPlayerRoomName(self, playerName, type):
        player = self.server.players.get(playerName)
        if player != None:
            for client in self.server.players.values():
            
                return player.roomName
        else:
            return '0'
            
    def getRoomMods(self,room):
        s = []
        i = ""
        for player in self.server.players.values():
            if player.roomName == room and player.privLevel >= 7:
                s.append(player.playerName)
                
        if len(s) == 1:
            return s[0]
        else:
            for name in s:
                i = i+name+", "
        return i
        
    def getPlayerKarma(self, playerName):
        player = self.server.players.get(playerName)
        if player:
            return player.playerKarma
        else:
            return 0
    
    def getReportType(self, playerName):
        player = self.server.players.get(playerName)
        if player:
            return self.ReportType(player.isReportedType)
        else:
            return "None"
    
    def banHack(self, playerName,iban):
        if self.server.banPlayer(playerName, 360, "Hack (last warning before account deletion)", self.client.playerName, iban):
            self.client.sendServerMessage("%s banned the player %s for 360h. Reason: Hack (last warning before account deletion)." %(self.client.playerName, playerName))
        self.updateModoPwet()
        
    def deleteReport(self,playerName,handled):
        if handled == 0: # [deleted]
            self.server.reports[playerName]["state"] = "deleted"
            self.server.reports[playerName]["deletedby"] = self.client.playerName
            #if playerName in self.server.reports:
                #del self.server.reports[playerName]
        else: # [handled]
            if self.getReportType(playerName) == "Hack":
                self.server.banPlayer(playerName, 24, "Hack", self.client.playerName, "iban")
            elif self.getReportType(playerName) == "Insults":
                self.server.mutePlayerIP(playerName, 1, "Insults", self.client.playerName)
            elif self.getReportType(playerName) == "Phishing":
                self.server.IbanPlayer(playerName, 360, "Phishing", self.client.playerName, "iban")
            elif self.getReportType(playerName) == "Spam / Flood":
                self.server.mutePlayerIP(playerName, 1, "Flood", self.client.playerName)
            else:
                pass
            self.server.reports[playerName]["state"] = "deleted"
            self.server.reports[playerName]["deletedby"] = self.client.playerName
        self.updateModoPwet()
        
    def SortingKey(self, array):
        for i in array[1]["reporters"]:
            return array[1]["reporters"][i][2]
            
    def sortReports(self,reports,sort):  
        if sort:
            return sorted(reports.items(), key=self.SortingKey,reverse=True)
        else:
            return sorted(reports.items(), key=lambda x: len(x[1]["reporters"]),reverse=True)
    
    def openModoPwet(self,isOpen=False,modopwetOnlyPlayerReports=False,sortBy=False):
        if isOpen:
            if len(self.server.reports) <= 0:
                self.client.sendPacket(Identifiers.send.Modopwet_Open, 0)
            else:
                self.client.sendPacket(Identifiers.send.Modopwet_Open, 0)
                reports,bannedList,deletedList,disconnectList = self.sortReports(self.server.reports,sortBy),{},{},[]
                sayi = 0
                p = ByteArray()  
                for i in reports:
                    playerName = i[0]
                    v = self.server.reports[playerName]
                    if self.client.modoPwetLangue == 'ALL' or v["language"] == self.client.modoPwetLangue:
                        player = self.server.players.get(playerName)
                        TimePlayed = math.floor(player.playerTime/3600) if player else 0
                        playerNameRoom = player.roomName if player else "0"
                        sayi += 1
                        self.client.lastReportID += 1
                        if sayi >= 255:
                            break  
                        p.writeByte(sayi)
                        p.writeShort(self.client.lastReportID)
                        p.writeUTF(v["language"])
                        p.writeUTF(playerName)
                        p.writeUTF(playerNameRoom)
                        p.writeByte(1)
                        p.writeUTF(self.getRoomMods(playerNameRoom))
                        p.writeInt(TimePlayed)
                        p.writeByte(int(len(v["reporters"])))
                        for name in v["reporters"]:
                            r = v["reporters"][name]
                            p.writeUTF(name)
                            p.writeShort(self.getPlayerKarma(name))
                            p.writeUTF(r[1])
                            p.writeByte(r[0])
                            p.writeShort(int(Utils.getSecondsDiff(r[2])/60))
                                
                        mute = v["isMuted"]
                        p.writeBoolean(mute) #isMute
                        if mute:
                            p.writeUTF(v["mutedBy"])
                            p.writeShort(v["muteHours"])
                            p.writeUTF(v["muteReason"])
                            
                        if v['state'] == 'banned':
                            x = {}
                            x['banhours'] = v['banhours']
                            x['banreason'] = v['banreason']
                            x['bannedby'] = v['bannedby']
                            bannedList[playerName] = x
                        if v['state'] == 'deleted':
                            x = {}
                            x['deletedby'] = v['deletedby']
                            deletedList[playerName] = x
                        if v['state'] == 'disconnected':
                            disconnectList.append(playerName)

                self.client.sendPacket(Identifiers.send.Modopwet_Open, ByteArray().writeByte(int(len(reports))).writeBytes(p.toByteArray()).toByteArray())
                for user in disconnectList:
                    self.changeReportStatusDisconnect(user)

                for user in deletedList.keys():
                    self.changeReportStatusDeleted(user, deletedList[user]['deletedby'])

                for user in bannedList.keys():
                    self.changeReportStatusBanned(user, bannedList[user]['banhours'], bannedList[user]['banreason'], bannedList[user]['bannedby'])

    def changeReportStatusDisconnect(self, playerName):
        self.client.sendPacket(Identifiers.send.Modopwet_Disconnected, ByteArray().writeUTF(playerName).toByteArray())
        player = self.server.players.get(playerName)
        if player != None:
            player.isReported = False

    def changeReportStatusDeleted(self, playerName, deletedby):
        self.client.sendPacket(Identifiers.send.Modopwet_Deleted, ByteArray().writeUTF(playerName).writeUTF(deletedby).toByteArray())
        player = self.server.players.get(playerName)
        if player != None:
            player.isReported = False
        
    def changeReportStatusBanned(self, playerName, banhours, banreason, bannedby):
        self.client.sendPacket(Identifiers.send.Modopwet_Banned, ByteArray().writeUTF(playerName).writeUTF(bannedby).writeInt(int(banhours)).writeUTF(banreason).toByteArray())
        player = self.server.players.get(playerName)
        if player != None:
            player.isReported = False

    def openChatLog(self, playerName):
        if playerName in self.server.chatMessages:
            packet = ByteArray().writeUTF(playerName).writeByte(len(self.server.chatMessages[playerName]))
            for message in self.server.chatMessages[playerName]:
                packet.writeUTF(message[1]).writeUTF(message[0])
            packet.writeUTF(self.server.chatMessages[playerName][len(self.server.chatMessages[playerName])-1][1])
            packet.writeUTF(self.server.chatMessages[playerName][len(self.server.chatMessages[playerName])-1][0])
            self.client.sendPacket(Identifiers.send.Modopwet_Chatlog, packet.toByteArray())
            