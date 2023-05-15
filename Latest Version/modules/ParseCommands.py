#coding: utf-8
import re, sys, json, os, base64, hashlib, time, random, asyncio, ast
"""
9 Admin, 8 Mod, 7 Arb, 6 MC, 5 FC, 4 LC, 3 - FS, 2 VIP, 1 PPL
Commands: /resign, /colormouse, /colornick, /lsbulle, /execpacket, /geoip, /tag

./tag [tag] [mapcode] [description] : Adds a tag to a map, or removes it if the map already had it
"""
# Modules
from langues import Langues
from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers
from Exceptions import ServerException
from modules import Lua

# Library
from datetime import datetime

class Commands:
    def __init__(self, client, server):
        self.client = client
        self.server = client.server
        self.Cursor = client.Cursor
        self.currentArgsCount = 0
        self.argsNotSplited = ""
        self.lastsonar = 0
        self.owners = ["Chatta#5324"] # i forgor 
        self.commands = {}
        self.__init_2()
        
    def requireLevel(self, level=0, roomOwner=False, roomStrm=False, lua=False, mc=False, fc=False, arb=False, fs=False):
        if self.client.room.isTribeHouse and self.client.privLevel < 6:
            return self.requireTribePerm(2046)
        elif roomStrm and not self.client.privLevel >= 5 and not self.client.isFunCorpPlayer and not self.client.isArbitre:
            if self.client.room.roomName == "*strm_" + self.client.playerName:
                return True
        elif roomOwner and self.client.privLevel < 6:
            return self.client.room.roomCreator == self.client.playerName or (self.client.isMapCrew if mc else False)
        return self.client.privLevel >= level or (self.client.isLuaCrew if lua else False) or (self.client.isMapCrew if mc else False) or (self.client.isFunCorpPlayer if fc else False) or (self.client.isArbitre if arb else False) or (self.client.isFashionSquad if fs else False)

    def requireArgs(self, arguments):
        if self.currentArgsCount < arguments:
            self.client.playerException.Invoke("moreargs")
            return False
        return self.currentArgsCount == arguments

    def requireTribePerm(self, permId):
        if self.client.room.isTribeHouse:
            rankInfo = self.client.tribeRanks.split(";")
            rankName = rankInfo[self.client.tribeRank].split("|")
            if rankName[2] in str(permId):
                return True
        return False
    
    def requireOwner(self):
        return self.client.playerName in self.owners
    
    def command(self,func=None,tribe=False,args=0,level=0,owner=False,roomOwner=False,roomStrm=False,lua=False,mc=False,fc=False,arb=False,fs=False,alies=[],reqrs=[]):
        if not func:
            reqrs=[]
            if tribe > 0: reqrs.append(['tribe',tribe])
            if args > 0: reqrs.append(['args',args])
            if level > 0: reqrs.append(['level',(level,roomOwner,roomStrm,lua,mc,fc,arb,fs)])
            if owner: reqrs.append(['owner'])
            return lambda x: self.command(x,tribe,args,level,owner,roomOwner,roomStrm,lua,mc,fc,arb,fs,alies,reqrs)
        else:
            for i in alies + [func.__name__]: self.commands[i] = [reqrs,func]
    
    async def parseCommand(self, command):
        values = command.split(" ")
        command = values[0].lower()
        args = values[1:]
        argsCount = len(args)
        self.argsNotSplited = " ".join(args)
        self.currentArgsCount = argsCount
        self.commandName = command
        self.Cursor['commandlog'].insert_one({'Time':Utils.getTime(),'Username':self.client.playerName,'Command':command})
        if command in self.commands:
            for i in self.commands[command][0]: 
                if i[0] == "level": 
                    if not self.requireLevel(*i[1]): return
                elif i[0] == "args":
                    if not self.requireArgs(i[1]): return
                elif i[0] == "tribe":
                    if not self.requireTribePerm(i[1]):
                        if command in ["inv", "invkick", "neige"]: # special tribe commands.
                            return
                        elif not (self.client.privLevel > 5 or self.client.room.roomName == "*strm_" + self.client.playerName or (self.client.room.isFuncorp == True and (self.client.privLevel == 4 or self.client.isFunCorpPlayer))):
                            return
                else:
                    if not self.requireOwner(): return
            await self.commands[command][1](self, *args)
    
    def __init_2(self):
# Guest / Souris Commands

        @self.command(alies=["die", "kill"])
        async def mort(self):
            if not self.client.isDead and not self.client.room.disableMortCommand:
                self.client.isDead = True
                if not self.client.room.noAutoScore: self.client.playerScore += 1
                self.client.sendPlayerDied()
                self.client.room.checkChangeMap()

        @self.command
        async def ping(self):
            self.client.sendClientMessage(f"ping ~{self.client.PInfo[2]}", 1)

        @self.command(alies=['profil','perfil','profiel'])
        async def profile(self, name=''):
            self.client.sendProfile(Utils.parsePlayerName(name) if name else self.client.playerName)

        @self.command(alies=["temps"])
        async def time(self):
            self.client.playerTime += abs(Utils.getSecondsDiff(self.client.loginTime))
            self.client.loginTime = Utils.getTime()
            temps = map(int, [self.client.playerTime // 86400, self.client.playerTime // 3600 % 24, self.client.playerTime // 60 % 60, self.client.playerTime % 60])
            self.client.sendLangueMessage("", "$TempsDeJeu", *temps)

        @self.command
        async def tutorial(self):
            self.client.enterRoom("\x03[Tutorial] %s" %(self.client.playerName))


# Player Commands

        @self.command(alies=['editor'], level=1)
        async def editeur(self):
            self.client.sendPacket(Identifiers.send.Room_Type, 1)
            self.client.enterRoom("\x03[Editeur] %s" %(self.client.playerName))
            self.client.sendPacket(Identifiers.old.send.Map_Editor, [])

        @self.command(level=1)
        async def info(self, mapCode, oldMapCode=""):
            if oldMapCode != "":
                await self.client.room.CursorMaps.execute("select Name, YesVotes, NoVotes, Perma from Maps where Code = ?", [mapCode])
                rss = await self.client.room.CursorMaps.fetchall()
                for rs in rss:
                    MapName = rs["Name"]
                    YesVotes = int(rs["YesVotes"])
                    NoVotes = int(rs["NoVotes"])
                    Perma = rs["Perma"]
                    totalVotes = YesVotes + NoVotes
                    if totalVotes < 1: totalVotes = 1
                    Rating = (1.0 * self.client.room.mapYesVotes / totalVotes) * 100
                    rate = str(Rating).split(".")[0]
                    if rate == "Nan": rate = "0"
                    self.client.sendClientMessage("<BL>"+MapName+" - @"+mapCode+" - "+str(totalVotes)+" - "+rate+"% - P"+str(Perma)+".</BL>", 1)
            else:
                totalVotes = self.client.room.mapYesVotes + self.client.room.mapNoVotes
                if totalVotes < 1: totalVotes = 1
                Rating = (1.0 * self.client.room.mapYesVotes / totalVotes) * 100
                rate = str(Rating).split(".")[0]
                if rate == "Nan": rate = "0"
                self.client.sendClientMessage("<BL>"+self.client.room.mapName+" - @"+str(self.client.room.mapCode)+" - "+str(totalVotes)+" - "+rate+"% - P"+str(self.client.room.mapPerma)+".</BL>", 1)

        @self.command(level=1)
        async def lsmap(self, playerName=''):
            if playerName == '':
                playerName = self.client.playerName
            else:
                if not self.client.privLevel > 5 and not self.client.isMapCrew and not self.client.isArbitre:
                    return
                
            mapList = ""
            mapCount = 0
            await self.client.room.CursorMaps.execute("select * from Maps where Name = ?", [playerName])
            for rs in await self.client.room.CursorMaps.fetchall():
                mapCount += 1
                yesVotes = rs["YesVotes"]
                noVotes = rs["NoVotes"]
                totalVotes = yesVotes + noVotes
                if totalVotes < 1: totalVotes = 1
                rating = (1.0 * yesVotes / totalVotes) * 100
                mapList += "\n<N>%s</N> - @%s - %s - %s%s - P%s" %(rs["Name"], rs["Code"], totalVotes, str(rating).split(".")[0], "%", rs["Perma"])

            self.client.sendLogMessage("<font size= \"12\"><V>%s<N>'s maps: <BV>%s %s</font>" %(playerName, mapCount, mapList))

        @self.command(level=1)
        async def mapcrew(self):
            staffMessage = "$MapcrewPasEnLigne"
            staffMembers = {}
            for player in self.server.players.copy().values():
                if player.privLevel == 6 or player.isMapCrew:
                    if player.langue.lower() in staffMembers:
                        names = staffMembers[player.langue.lower()]
                        names.append(player.playerName)
                        staffMembers[player.langue.lower()] = names
                    else:
                        names = []
                        names.append(player.playerName)
                        staffMembers[player.langue.lower()] = names
            if len(staffMembers) > 0:
                staffMessage = "$MapcrewEnLigne"
                for member in staffMembers.items():
                    staffMessage += f"<br>[{member[0]}] <BV>{('<BV>, </BV>').join(member[1])}</BV>"
            self.client.sendLangueMessage("", staffMessage)

        @self.command(args=1)
        async def mjj(self, roomName):
            if roomName.startswith("#"):
                if roomName[1:] in self.server.minigames:
                    self.client.enterRoom(f"{self.client.langue.lower()}-{roomName}" + "1")
            else:
                self.client.enterRoom(({0:"", 3:"vanilla", 8:"survivor", 9:"racing", 11:"music", 2:"bootcamp", 10:"defilante", 16:"village"}[self.client.lastGameMode]) + roomName)

        @self.command(level=1)
        async def mod(self):
            staffMessage = "$ModoPasEnLigne"
            staffMembers = {}
            for player in self.server.players.copy().values():
                if player.privLevel == 8:
                    if player.langue.lower() in staffMembers:
                        names = staffMembers[player.langue.lower()]
                        names.append(player.playerName)
                        staffMembers[player.langue.lower()] = names
                    else:
                        names = []
                        names.append(player.playerName)
                        staffMembers[player.langue.lower()] = names
            if len(staffMembers) > 0:
                staffMessage = "$ModoEnLigne"
                for member in staffMembers.items():
                    staffMessage += f"<br>[{member[0]}] <BV>{('<BV>, </BV>').join(member[1])}</BV>"
            self.client.sendLangueMessage("", staffMessage)

        @self.command(level=9, roomOwner=True)
        async def mulodrome(self):
             if not self.client.room.isMulodrome:
                for player in self.client.room.clients.copy().values():
                    player.sendPacket(Identifiers.send.Mulodrome_Start, 1 if player.playerName == self.client.playerName else 0)

        @self.command(level=1, roomOwner=True)
        async def pw(self, password=''):
            self.client.room.roomDetails[10] = password
            if self.currentArgsCount == 0:
                Message = "$MDP_Desactive"
            else: 
                Message = f"$Mot_De_Passe : {password}"
            self.client.sendLangueMessage("", Message)

        @self.command(level=1)
        async def resettotem(self):
            if self.client.room.isTotemEditor:
                self.client.totem = [0 , ""]
                self.client.tempTotem = [0 , ""]
                self.client.resetTotem = True
                self.client.isDead = True
                self.client.sendPlayerDied()
                self.client.room.checkChangeMap()

        @self.command(level=1)
        async def sauvertotem(self):
            if self.client.room.isTotemEditor:
                self.client.totem[0] = self.client.tempTotem[0]
                self.client.totem[1] = self.client.tempTotem[1]
                self.client.sendPlayerDied()
                self.client.enterRoom(self.server.recommendRoom(self.client.langue))

        @self.command(level=1, alies=["titre", "titulo", "titel"])
        async def title(self, titleID=0):
            if self.currentArgsCount == 0:
                p = ByteArray()
                p2 = ByteArray()
                titlesCount = 0
                starTitlesCount = 0
                for title in self.client.titleList:
                    titleInfo = str(title).split(".")
                    titleNumber = int(titleInfo[0])
                    titleStars = int(titleInfo[1])
                    if titleStars > 1:
                        p.writeShort(titleNumber).writeByte(titleStars)
                        starTitlesCount += 1
                    else:
                        p2.writeShort(titleNumber)
                        titlesCount += 1
                self.client.sendPacket(Identifiers.send.Titles_List, ByteArray().writeShort(titlesCount).writeBytes(p2.toByteArray()).writeShort(starTitlesCount).writeBytes(p.toByteArray()).toByteArray())
            else:
                found = False
                for title in self.client.titleList:
                    if str(title).split(".")[0] == titleID:
                        found = True

                if found:
                    self.client.titleNumber = int(titleID)
                    for title in self.client.titleList:
                        if str(title).split(".")[0] == titleID:
                            self.client.titleStars = int(str(title).split(".")[1])
                    self.client.sendPacket(Identifiers.send.Change_Title, ByteArray().writeByte(self.client.gender).writeShort(titleID).toByteArray())

        @self.command(level=1)
        async def totem(self):
            if self.client.shamanSaves >= self.server.minimumNormalSaves:
                self.client.enterRoom("\x03[Totem] %s" %(self.client.playerName))


# Tribe commands
        @self.command(level=6, tribe=2046, args=1, mc=True, roomStrm=True)
        async def ch(self, playerName):
            player = self.server.players.get(playerName)
            if player != None:
                if self.client.room.forceNextShaman == player.playerCode:
                    self.client.sendLangueMessage("", "$PasProchaineChamane", player.playerName)
                    self.client.room.forceNextShaman = -1
                else:
                    self.client.sendLangueMessage("", "$ProchaineChamane", player.playerName)
                    self.client.room.forceNextShaman = player.playerCode
            else:
                self.client.playerException.Invoke("unknownuser")

        @self.command(level=6, tribe=2046, mc=True)
        async def csr(self):
            ml = []
            for player in self.server.players.copy().values():
                m1.append(player.playerName)
            randomplayer = random.choice(ml)
            player = self.server.players.get(randomplayer)
            if player != None:
                player.isSync = True
                self.client.room.currentSyncCode = player.playerCode
                self.client.room.currentSyncName = player.playerName
                self.client.sendLangueMessage("", "$NouveauSync <V> %s" %(player))

        @self.command(level=1, tribe=2046, args=1)
        async def inv(self, playerName):
            if self.server.checkConnectedAccount(playerName) and not playerName in self.client.tribulle.getTribeMembers(self.client.tribeCode):
                player = self.server.players.get(playerName)
                player.invitedTribeHouses.append(self.client.tribeName)
                player.sendPacket(Identifiers.send.Tribe_Invite, ByteArray().writeUTF(self.client.playerName).writeUTF(self.client.tribeName).toByteArray())
                self.client.sendLangueMessage("", "$InvTribu_InvitationEnvoyee", "<V>"+player.playerName+"</V>")

        @self.command(level=1, tribe=2046, args=1)
        async def invkick(self, playerName):
            if self.server.checkConnectedAccount(playerName) and not playerName in self.client.tribulle.getTribeMembers(self.client.tribeCode):
                player = self.server.players.get(playerName)
                if self.client.tribeName in player.invitedTribeHouses:
                    player.invitedTribeHouses.remove(self.client.tribeName)
                    self.client.sendLangueMessage("", "$InvTribu_AnnulationEnvoyee", "<V>" + player.playerName + "</V>")
                    player.sendLangueMessage("", "$InvTribu_AnnulationRecue", "<V>" + self.client.playerName + "</V>")
                    if player.roomName == "*" + chr(3) + self.client.tribeName:
                        player.enterRoom(self.server.recommendRoom(self.client.langue))

        @self.command(level=1, tribe=2046)
        async def module(self, moduleid=''):
            if moduleid == "":
                self.client.sendClientMessage("Module list:", 1)
                for key in self.server.officialminigames:
                    self.client.sendMessage(f"<VP>#{key}</VP> : {self.client.room.getPlayersCountbyRoom('#'+key)}")
            elif moduleid[:1] == "stop":
                if self.client.room.luaRuntime != None:
                    self.client.room.luaRuntime.stopModule()
            else:
                module = self.server.minigames.get(moduleid[:1])
                if module != None:
                    self.client.room.luaRuntime = Lua(self.client.room, self.server)
                    self.client.room.luaRuntime.owner = self.client.playerName
                    self.client.room.luaRuntime.RunCode(module)

        @self.command(level=9, tribe=2046, args=1, roomStrm=True)
        async def music(self, music=''):
            self.client.room.sendAll(Identifiers.old.send.Music, []) if len(music) == 0 else self.client.room.sendAll(Identifiers.old.send.Music, [music])

        @self.command(level=1, tribe=2046)
        async def neige(self):
            if self.client.room.isSnowing:
                self.client.room.startSnow(0, 0, not self.client.room.isSnowing)
                self.client.room.isSnowing = False
            else:
                self.client.room.startSnow(1000, 60, not self.client.room.isSnowing)
                self.client.room.isSnowing = True

        @self.command(level=6, tribe=2046, mc=True, alies=["sy?"])
        async def __commande_syquestionmark(self):
            self.client.sendLangueMessage("", "$SyncEnCours : [%s]" %(self.client.room.currentSyncName))

        @self.command(level=6, tribe=2046, mc=True, args=1)
        async def sy(self, playerName):
            player = self.server.players.get(playerName)
            if player != None:
                player.isSync = True
                self.client.room.currentSyncCode = player.playerCode
                self.client.room.currentSyncName = player.playerName
                if self.client.room.mapCode != -1 or self.client.room.EMapCode != 0:
                    self.client.sendPacket(Identifiers.old.send.Sync, [player.playerCode, ""])
                    self.client.sendLangueMessage("", "$NouveauSync <V> %s" %(player.playerName))
                else:
                    self.client.sendPacket(Identifiers.old.send.Sync, [player.playerCode])
                    self.client.sendLangueMessage("", "$NouveauSync <V> %s" %(player.playerName))
            else:
                self.client.playerException.Invoke("unknownuser")


# Lua and Fashion Squad Commands
        @self.command(level=3, fs=True)
        async def lsfs(self):
            if not self.client.privLevel in [3, 9] and not self.client.isFashionSquad:
                return
                
            FS = ""
            for player in self.server.players.copy().values():
                if player.isFashionSquad or player.privLevel == 3:
                    FS += "<font color='#ffb6c1'>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </font><br>"
            if FS != "":
                self.client.sendMessage(FS.rstrip("\n"))
            else:
                self.client.playerException.Invoke("noonlinestaff", "Fashion Squads")

        @self.command(level=4, lua=True)
        async def lslua(self):
            if not self.client.privLevel in [4, 9] and not self.client.isLuaCrew:
                return
        
            LuaCrews = ""
            for player in self.server.players.copy().values():
                if player.isLuaCrew or player.privLevel == 4:
                    LuaCrews += "<font color='#79bbac'>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </font><br>"
            if LuaCrews != "":
                self.client.sendMessage(LuaCrews.rstrip("\n"))
            else:
                self.client.playerException.Invoke("noonlinestaff", "Lua Crews")


# Funcorp Commands
        @self.command(level=5, fc=True)
        async def changenick(self, *args):
            if not self.client.privLevel in [5, 9] and not self.client.isFunCorpPlayer:
                return
        
            if self.client.room.isFuncorp:
                dump = []
                msgpl = []
                for arg in args:
                    dump.append(arg)
                if dump[-1] == "off":
                    for argument in dump[:-1]:
                        player = self.client.room.clients.get(argument)
                        if player != None:
                            msgpl.append(player.playerName)
                            player.mouseName = ""
                    if len(msgpl) > 0:
                        self.client.sendClientMessage(f"The following players has changed their nicknames to default: <BV>{', '.join(map(str, msgpl))}</BV>", 1)
                else:
                    ppnickname = []
                    for argument in dump:
                        player = self.client.room.clients.get(argument)
                        if player != None:
                            msgpl.append(player)
                        else:
                            ppnickname.append(argument)
                    for player in msgpl:
                        player.mouseName = ' '.join(map(str, ppnickname))
                    if len(msgpl) > 0:
                        self.client.sendClientMessage(f"The following players has changed their nicknames to {' '.join(map(str, ppnickname))} : <BV>{','.join(map(str, msgpl))}</BV>", 1)
            else:
                self.client.playerException.Invoke("requireFC")

        @self.command(level=5, fc=True, roomStrm=True)
        async def changesize(self, *args):
            if not self.client.privLevel in [5, 9] and not self.client.isFunCorpPlayer and not self.client.room.roomName == "*strm_" + self.client.playerName:
                return
            
            if self.client.room.isFuncorp:
                dump = []
                players = []
                msg = []
                size = 0
                for arg in args:
                    dump.append(arg)

                if dump[0] == "*":
                    if dump[1] == "off":
                        for player in self.client.room.clients.copy().values():
                            self.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(100).writeBoolean(False).toByteArray())
                        self.client.sendClientMessage("All players now have their regular size.", 1)
                    else:
                        size = int(dump[1])
                        if size >= 1500: size = 100
                        for player in self.client.room.clients.copy().values():
                            self.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(size).writeBoolean(False).toByteArray())
                        self.client.sendClientMessage("All players now have the same size: <BV>" + str(size) + "</BV>.", 1)
                else:
                    for argument in dump[:-1]:
                        player = self.client.room.clients.get(argument)
                        if player != None:
                            players.append(player)
                    if dump[-1] == "off":
                        for player in players:
                            self.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(100).writeBoolean(False).toByteArray())
                            msg.append(player.playerName)
                        self.client.sendClientMessage(f"The following players now have their regular size: <BV>{', '.join(map(str, msg))}</BV>", 1)
                    else:
                        size = int(dump[-1])
                        if size >= 1500: size = 100
                        for player in players:
                            self.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(size).writeBoolean(False).toByteArray())
                            msg.append(player.playerName)
                        self.client.sendClientMessage(f"The following players now have the size {str(size)}: <BV>{', '.join(map(str, msg))}</BV>", 1)
            else:
                self.client.playerException.Invoke("requireFC")

        @self.command(level=5, fc=True, roomStrm=True)
        async def funcorp(self, showhelp=''):
            if not self.client.privLevel in [5, 9] and not self.client.isFunCorpPlayer and not self.client.room.roomName == "*strm_" + self.client.playerName:
                return
        
            if self.currentArgsCount == 0:
                if self.client.room.isFuncorp:
                    for player in self.client.room.clients.copy().values():
                        player.sendLangueMessage("", "<FC>$FunCorpDesactive</FC>")
                        self.client.room.isFuncorp = False
                        player.mouseName = ""
                        player.tempMouseColor = ""
                else:
                    for player in self.client.room.clients.copy().values():
                        player.sendLangueMessage("", "<FC>$FunCorpActive</FC>")
                        self.client.room.isFuncorp = True
            else:
                if showhelp == "help":
                    if self.client.room.roomName == "*strm_" + self.client.playerName and not (self.client.privLevel in [5, 9] or self.client.isFunCorpPlayer):
                        self.client.sendLogMessage(self.FunCorpPlayerCommands()) # strm_
                    else:
                        self.client.sendLogMessage(self.FunCorpMemberCommands()) # FC member

        @self.command(level=5, fc=True, roomStrm=True)
        async def linkmice(self, *args):
            if not self.client.privLevel in [5, 9] and not self.client.isFunCorpPlayer and not self.client.room.roomName == "*strm_" + self.client.playerName:
                return
        
            if self.client.room.isFuncorp:
                dump = []
                msg = []
                players = []
            
                for arg in args:
                    dump.append(arg)
                
                if dump[0] == "*":
                    if self.currentArgsCount == 2:
                        if dump[1] == "off":
                            for player in self.client.room.clients.copy().values():
                                self.client.room.sendAll(Identifiers.send.Soulmate, ByteArray().writeBoolean(False).writeInt(player.playerCode).writeInt(self.client.playerCode).toByteArray())
                            self.client.sendClientMessage("All the links have been removed.", 1)
                    else:
                        for player in self.client.room.clients.copy().values():
                            self.client.room.sendAll(Identifiers.send.Soulmate, ByteArray().writeBoolean(True).writeInt(player.playerCode).writeInt(self.client.playerCode).toByteArray())
                        self.client.sendClientMessage("All the players are now linked.", 1)
                        
                else:
                    for argument in dump:
                        player = self.client.room.clients.get(argument)
                        if player != None:
                            players.append(player)
                    if dump[-1] == "off":
                        for player in players:
                            self.client.room.sendAll(Identifiers.send.Soulmate, ByteArray().writeBoolean(False).writeInt(player.playerCode).writeInt(players[0].playerCode).toByteArray())
                            msg.append(player.playerName)
                        self.client.sendClientMessage(f"The links involving the following players have been removed: <BV>{', '.join(map(str, msg))}</BV>", 1)
                    else:
                        for player in players:
                            self.client.room.sendAll(Identifiers.send.Soulmate, ByteArray().writeBoolean(True).writeInt(player.playerCode).writeInt(players[0].playerCode).toByteArray())
                            msg.append(player.playerName)
                        self.client.sendClientMessage(f"The following players are now linked: <BV>{', '.join(map(str, msg))}</BV>", 1)
            else:
                self.client.playerException.Invoke("requireFC") 

        @self.command(level=5, fc=True)
        async def lsfc(self):
            if not self.client.privLevel in [5, 9] and not self.client.isFunCorpPlayer:
                return
        
            FunCorps = ""
            for player in self.server.players.copy().values():
                if player.isFunCorpPlayer or player.privLevel == 5:
                    FunCorps += "<FC>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </FC><br>"
            if FunCorps != "":
                self.client.sendMessage(FunCorps.rstrip("\n"))
            else:
                self.client.sendClientMessage("Don't have any online Fun Corps at moment.", 1)

        @self.command(level=5, fc=True, roomStrm=True)
        async def meep(self, *args):
            if not self.client.privLevel in [5, 9] and not self.client.isFunCorpPlayer and not self.client.room.roomName == "*strm_" + self.client.playerName:
                return
        
            if self.client.room.isFuncorp:
                dump = []
                players = []
                msg = []
                for arg in args:
                    dump.append(arg)

                if dump[0] == "*":
                    if self.currentArgsCount == 2:
                        if dump[1] == "off":
                            for player in self.client.room.clients.copy().values():
                                player.sendPacket(Identifiers.send.Can_Meep, 0)
                            self.client.sendClientMessage("All the meep powers have been removed.", 1)
                    else:
                        for player in self.client.room.clients.copy().values():
                            player.sendPacket(Identifiers.send.Can_Meep, 1)
                        self.client.sendClientMessage("Meep powers given to all players in the room.", 1)
                else:
                    for argument in dump:
                        player = self.client.room.clients.get(argument)
                        if player != None:
                            players.append(player)
                    if dump[-1] == "off":
                        for player in players:
                            player.sendPacket(Identifiers.send.Can_Meep, 0)
                            msg.append(player.playerName)
                        self.client.sendClientMessage(f"Meep powers removed from players: <BV>{', '.join(map(str, msg))}</BV>", 1)
                    else:
                        for player in players:
                            player.sendPacket(Identifiers.send.Can_Meep, 1)
                            msg.append(player.playerName)
                        self.client.sendClientMessage(f"Meep powers given to players: <BV>{', '.join(map(str, msg))}</BV>", 1)
            else:
                self.client.playerException.Invoke("requireFC")

        @self.command(level=5, fc=True)
        async def roomevent(self):
            if not self.client.privLevel in [5, 9] and not self.client.isFunCorpPlayer:
                return
        
            if self.client.room.isFuncorp:
                self.client.room.isFuncorpRoomName = not self.client.room.isFuncorpRoomName
                self.client.sendClientMessage('Sucessfull disabled the room color.' if self.client.room.isFuncorpRoomName else 'Sucessfull enabled the room color.', 1)
            else:
                self.client.playerException.Invoke("requireFC")

        @self.command(level=5, fc=True, roomStrm=True)
        async def transformation(self, *args):
            if not self.client.privLevel in [5, 9] and not self.client.isFunCorpPlayer and not self.client.room.roomName == "*strm_" + self.client.playerName:
                return
        
            if self.client.room.isFuncorp:
                dump = []
                players = []
                msg = []
                for arg in args:
                    dump.append(arg)

                if dump[0] == "*":
                    if self.currentArgsCount == 2:
                        if dump[1] == "off":
                            for player in self.client.room.clients.copy().values():
                                player.sendPacket(Identifiers.send.Can_Transformation, 0)
                            self.client.sendClientMessage("All the transformations powers have been removed.", 1)
                    else:
                        for player in self.client.room.clients.copy().values():
                            player.sendPacket(Identifiers.send.Can_Transformation, 1)
                        self.client.sendClientMessage("Transformations powers given to all players in the room.", 1)
                else:
                    for argument in dump:
                        player = self.client.room.clients.get(argument)
                        if player != None:
                            players.append(player)
                    if dump[-1] == "off":
                        for player in players:
                            player.sendPacket(Identifiers.send.Can_Transformation, 0)
                            msg.append(player.playerName)
                        self.client.sendClientMessage(f"Transformations powers removed to players: <BV>{', '.join(map(str, msg))}</BV>", 1)
                    else:
                        for player in players:
                            player.sendPacket(Identifiers.send.Can_Transformation, 1)
                            msg.append(player.playerName)
                        self.client.sendClientMessage(f"Transformations powers given to players: <BV>{', '.join(map(str, msg))}</BV>", 1)
            else:
                self.client.playerException.Invoke("requireFC")

        @self.command(level=5, fc=True)
        async def tropplein(self, players=0):
            if (self.client.privLevel == 5 or self.client.isFunCorpPlayer) and not self.client.room.isFuncorp:
                return
            if self.currentArgsCount == 0:
                self.client.sendClientMessage("The current maximum number of players is: <BV>"+str(self.client.room.roomDetails[8]) + "</BV>", 1)
            else:
                maxPlayers = 0 if int(players) > 200 or int(players) < 1 else int(players)
                self.client.room.roomDetails[8] = maxPlayers
                self.client.sendClientMessage("Maximum number of players in the room is set to: <BV>" +str(maxPlayers) + "</BV>", 1)



# MapCrew Commands
        @self.command(level=6, mc=True, alies=['del'])
        async def __commande_del(self, mapCode=''):
            if not self.client.privLevel in [6, 9] and not self.client.isMapCrew:
                return
        
            if mapCode == '':
                mapCode = self.client.room.mapCode
            else:
                mapCode = mapCode.replace('@', '')
            await self.client.room.CursorMaps.execute("update Maps set Perma = ? where Code = ?", ["44", mapCode])
            self.client.sendClientMessage("Successfull deleted the map: @"+str(mapCode)+".", 1)

        @self.command(level=6, mc=True, args=1)
        async def changeperm(self, category):
            category = int(category)
            if (self.client.privLevel in [7, 8] or self.isArbitre) and category not in [44, 43, 38]:
                return
            mapCode = self.client.room.mapCode
            mapName = self.client.room.mapName
            currentCategory = self.client.room.mapPerma
            if mapCode != -1:
                if category in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 17, 18, 19, 20, 21, 22, 23, 24, 32, 34, 38, 41, 42, 43, 44, 45, 66]:
                    self.client.sendClientMessage(f"[{mapName}] @{mapCode} : {currentCategory} -> {category}", 1)
                    await self.client.room.CursorMaps.execute("update Maps set Perma = ? where Code = ?", [category, mapCode])

        @self.command(level=6, mc=True)
        async def lsmc(self):
            Mapcrews = ""
            for player in self.server.players.copy().values():
                if player.isMapCrew or player.privLevel == 6:
                    Mapcrews += "<BV>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </BV><br>"
            if Mapcrews != "":
                self.client.sendMessage(Mapcrews.rstrip("\n"))
            else:
                self.client.playerException.Invoke("noonlinestaff", "Map Crews")

        @self.command(level=6, args=1)
        async def lsperma(self, category):
            if not self.client.privLevel in [6, 9] and not self.client.isMapCrew:
                return
        
            category = int(category)
            if category in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 17, 18, 19, 20, 21, 22, 23, 24, 32, 34, 38, 41, 42, 43, 44, 45, 66]:
                mapList = ""
                mapCount = 0
                await self.client.room.CursorMaps.execute("select * from Maps where Perma = ?", [category])
                rss = await self.client.room.CursorMaps.fetchall()
                for rs in rss:
                    mapCount += 1
                    yesVotes = rs["YesVotes"]
                    noVotes = rs["NoVotes"]
                    totalVotes = yesVotes + noVotes
                    if totalVotes < 1: totalVotes = 1
                    rating = (1.0 * yesVotes / totalVotes) * 100
                    mapList += "\n<N>%s</N> - @%s - %s - %s%s - P%s" %(rs["Name"], rs["Code"], totalVotes, str(rating).split(".")[0], "%", rs["Perma"])
                self.client.sendLogMessage("<font size=\"12\"><N>Total Maps </N> <BV>%s</BV> <N>with category: </N> <V>%s %s</V></font>" %(mapCount, category, mapList))

        @self.command(level=5, mc=True, fc=True, roomStrm=True, tribe=2046) ########
        async def np(self, code=0):
            if (self.client.privLevel == 5 or self.client.isFunCorpPlayer and not self.client.room.isFuncorp) or self.client.room.isVotingMode:
                return
                
            if self.currentArgsCount == 0:
                await self.client.room.mapChange()
                return

            if code.startswith("@"):
                if len(code[1:]) < 1 or not code[1:].isdigit():
                    self.client.sendLangueMessage("", "$CarteIntrouvable")
                    return
                mapInfo = await self.client.room.getMapInfo(int(code[1:]))
                if mapInfo[0] == None:
                    self.client.sendLangueMessage("", "$ChargementCarteInconnue")
                    self.client.sendLangueMessage("", f"$ProchaineCarte : {mapInfo[0]} - {code}")
                    return

                self.client.room.forceNextMap = code
                if self.client.room.changeMapTimer != None:
                    try:self.client.room.changeMapTimer.cancel()
                    except:self.client.room.changeMapTimer = None
                await self.client.room.mapChange()

            elif code.isdigit():
                mapInfo = await self.client.room.getMapInfo(int(code[1:]))
                if mapInfo[0] == None:
                    self.client.sendLangueMessage("", "$ChargementCarteInconnue")
                    self.client.sendLangueMessage("", f"$ProchaineCarte : Vanilla - {code}")
                    return
            
                self.client.room.forceNextMap = f"{code}"
                if self.client.room.changeMapTimer != None:
                    try:self.client.room.changeMapTimer.cancel()
                    except:self.client.room.changeMapTimer = None
                await self.client.room.mapChange()

        @self.command(level=5, mc=True, fc=True, roomStrm=True, tribe=2046, args=1) ########
        async def npp(self, code):
            if (self.client.privLevel == 5 or self.client.isFunCorpPlayer and not self.client.room.isFuncorp) or self.client.room.isVotingMode:
                return
                
            if code.startswith("@"):
                if len(code[1:]) < 1 or not code[1:].isdigit():
                    self.client.sendLangueMessage("", "$CarteIntrouvable")
                    return
                mapInfo = await self.client.room.getMapInfo(int(code[1:]))
                if mapInfo[0] == '':
                    self.client.sendLangueMessage("", "$ChargementCarteInconnue")
                    self.client.sendLangueMessage("", "$CarteIntrouvable2", code)
                    return
                    
                self.client.room.forceNextMap = code
                self.client.sendLangueMessage("", f"$ProchaineCarte : {mapInfo[0]} - {code}")
            elif code.isdigit():
                mapInfo = await self.client.room.getMapInfo(code)
                if mapInfo[0] == '':
                    self.client.sendLangueMessage("", "$ChargementCarteInconnue")
                    self.client.sendLangueMessage("", "$CarteIntrouvable2", code)
                    return
            
                self.client.room.forceNextMap = f"{code}"
                self.client.sendLangueMessage("", f"$ProchaineCarte : Vanilla - {code}")



# Arbitre Commands
        @self.command(level=1)
        async def ban(self, playerName, hours=24, *args):
            if self.client.room.roomName == "*strm_" + self.client.playerName: # STRM support
                player = self.server.players.get(playerName)
                if player != None and player.roomName == self.client.roomName:
                    player.enterRoom(self.server.recommendRoom(player.langue))
                    self.client.sendClientMessage(f"{player.playerName} has been roomkicked from [{str.lower(player.room.name)}] by {self.client.playerName}.")
            elif self.currentArgsCount == 1: # Vote Populaire Support
                self.server.voteBanPopulaire(playerName, self.client.playerName, self.client.ipAddress)
            else:
                if self.client.privLevel >= 7 or self.client.isArbitre:
                    result = self.server.checkBanUser(playerName)
                    if result == -1:
                        reason = self.argsNotSplited.split(" ", 2)[2]
                        if self.server.checkConnectedAccount(playerName):
                            self.client.sendClientMessage(f"The player {playerName} got banned for {hours}h ({reason})", 1)
                            self.client.sendServerMessageOthers(f"{self.client.playerName} banned the player {playerName} for {hours}h ({reason}).")
                            self.server.banPlayer(playerName, int(hours), reason, self.client.playerName, False)
                        else:
                            self.client.sendClientMessage(f"The player {playerName} got banned for {hours}h ({reason})", 1)
                            self.client.sendServerMessageOthers(f"{self.client.playerName} offline banned the player {playerName} for {hours}h ({reason}).")
                            self.server.banPlayer(playerName, int(hours), reason, self.client.playerName, False)
                    elif result == 1:
                        self.client.playerException.Invoke("useralreadybanned", playerName)
                    else:
                        self.client.playerException.Invoke("unknownuser")

        @self.command(level=7, arb=True, args=1)
        async def banhack(self, playerName):
            player = self.server.players.get(playerName)
            if player != None:
                hours = self.server.getTotalBanHours(playerName) // 360
                if hours <= 0:
                    hours = 1
                hours *= 360
                reason = "Hack. Your account will be permanently banned if you continue to violate the rules!"
                t = self.server.fastRacingRecords
                if playerName in t["records"]:
                    s = [playerName,len(t["records"][playerName])]
                    if s in t["sequentialrecords"]:
                        index = t["sequentialrecords"].index(s)
                        t["sequentialrecords"].pop(index)
                    for mapcode in t["records"][playerName]:
                        if mapcode in t["recordmap"]:
                            del t["recordmap"][mapcode]
                    del t["records"][playerName]
                    await self.client.room.CursorMaps.execute("update Maps set Time = ?, Player = ?, RecDate = ? where Player = ?", [0, "", 0, playerName])
                self.server.banPlayer(player.playerName, hours, reason, self.client.playerName, False)
                self.client.sendServerMessageOthers("%s banned the player %s for %sh (%s)" %(self.client.playerName, playerName, hours, reason))
            else:
                self.client.playerException.Invoke("unknownuser")

        @self.command(level=7, args=3)
        async def banip(self, ip, hours, reason):
            decip = Utils.DecodeIP(ip)
            if decip in self.server.IPTempBanCache:
                self.client.sendClientMessage(f"The IP [{ip}] is already banned, please wait.", 1)
            else:
                st = False
                for player in self.server.players.copy().values():
                    if player.ipAddress == decip:
                        st = True
                        player.transport.close()
                self.server.tempBanIP(decip, hours)
                if st:
                    self.client.sendServerMessageOthers(f"{self.client.playerName} banned the IP {ip} for {hours}h ({reason}).")
                else:
                    self.client.sendServerMessageOthers(f"{self.client.playerName} offline banned the IP {ip} for {hours}h ({reason}).")
                self.client.sendClientMessage(f"The IP {ip} got banned.", 1)

        @self.command(level=7, args=1, arb=True)
        async def casier(self, xxx):
            st = False
            message = "<p align='center'><N>Sanction Logs for <V>"+xxx+"</V></N>\n</p><p align='left'>Currently running sanctions: </p><br>"
            if xxx.startswith('#') and '.' in xxx:
                r = self.Cursor['casierlog'].find({"IP":xxx})
            else:
                r = self.Cursor['casierlog'].find({"Name":xxx})
            for rs in r[0:200]:
                st = True
                name,ip,state,timestamp,modName,time,reason = rs['Name'],rs['IP'],rs['State'],rs['Timestamp'],rs['Moderator'],rs['Time'],rs['Reason']
                fromtime = str(datetime.fromtimestamp(float(int(timestamp))))
                if time == '': time = 0
                sanctime = (int(time)*60*60)
                totime = datetime.fromtimestamp(float(int(timestamp) + sanctime))
                totime1 = datetime.utcfromtimestamp(float(int(timestamp) + sanctime))
                if state in ["UNMUTE", "UNBAN"]:
                    message = message + "<G><font size='12'><p align='left'> - </G><G><b>" + state + "</b> (" + str(ip) + ") by " + modName + "</font></G>\n"
                    message = message + "<G><p align='left'><font size='9'>    " + fromtime + "</font></G>\n\n"
                elif state == "MUMUTE":
                    message = message + "<N><font size='12'><p align='left'> - <b><V></N>" + state + " " + str(time) + "h</V></b><N> (" + str(ip) + ") by " + modName + " : <BL>" + reason + "</BL>\n"
                    message = message + "<p align='left'><font size='9'>    " + fromtime + "</font>\n\n"
                else:
                    message = message + "<N><font size='12'><p align='left'> - <b><V></N>" + state + " " + str(time) + "h</V></b><N> (" + str(ip) + ") by " + modName + " : <BL>" + reason + "</BL>\n"
                    if totime1 != None:
                        message = message + "<p align='left'><font size='9'><N2>    " + fromtime + " | "+ str(totime) + " → "+ str(totime1) + "</N2>\n\n"
                    elif totime != None:
                        message = message + "<p align='left'><font size='9'><N2>    " + fromtime + " → "+ str(totime) + "</N2>\n\n"
                    else:
                        message = message + "<p align='left'><font size='9'><N2>    " + fromtime + "</N2>\n\n"
            if st:
                self.client.sendLogMessage(message)
            else:
                self.client.playerException.Invoke("unknownuserorip")

        @self.command(level=7, arb=True)
        async def chatfilter(self, option, *args):
            if option == "list":
                msg = "Filtered strings:\n"
                for message in self.server.serverList:
                    msg += message + "\n"
                self.client.sendLogMessage(msg)
                
            elif option == "del":
                name = self.argsNotSplited.split(" ", 1)[1].replace("http://www.", "").replace("https://www.", "").replace("http://", "").replace("https://", "").replace("www.", "")
                if not name in self.server.serverList:
                    self.client.sendClientMessage(f"The string <N>[{name}]</N> is not in the filter.", 1)
                else:
                    self.server.serverList.remove(name)
                    self.client.sendClientMessage(f"The string <N>[{name}]</N> has been removed from the filter.", 1)
                    
            elif option == "add":
                name = self.argsNotSplited.split(" ", 1)[1].replace("http://www.", "").replace("https://www.", "").replace("http://", "").replace("https://", "").replace("www.", "")
                if name in self.server.serverList:
                    self.client.sendClientMessage(f"The string <N>[{name}]</N> is already filtered (matches [{name}]).", 1)
                else:
                    self.server.serverList.append(name)
                    self.client.sendClientMessage(f"The string <N>[{name}]</N> has been added to the filter.", 1)

        @self.command(level=7, arb=True, args=1)
        async def chatlog(self, playerName):
            self.client.modoPwet.openChatLog(playerName)

        @self.command(level=7, arb=True, args=1)
        async def clearban(self, playerName):
            if self.server.checkConnectedAccount(playerName):
                player = self.server.players.get(playerName)
                if player != None:
                    if len(player.voteBan) > 0:
                        player.voteBan = []
                        self.client.sendServerMessageOthers(f"{self.client.playerName} removed all ban votes of {playerName}.")
                        self.client.sendClientMessage(f"Successfully removed all ban votes of {playerName}", 1)
                    else:
                        self.client.sendClientMessage(f"{playerName} does not contains any ban votes.", 1)
                else:
                     self.client.playerException.Invoke("unknownuser")

        @self.command(level=5, arb=True, fc=True)
        async def closeroom(self, *args):
            if (self.client.privLevel == 5 or self.client.isFunCorpPlayer) and not self.client.room.isFuncorp and self.currentArgsCount > 0:
                return
            elif not self.client.privLevel in [7, 8, 9] and not self.isArbitre:
                return
                
            if self.currentArgsCount > 0:
                roomName = self.argsNotSplited.split(" ", 0)[0]
                try:
                    for client in [*self.server.rooms[roomName].clients.values()]:
                        client.enterRoom(self.server.recommendRoom(client.langue))
                    self.client.sendServerMessageOthers(str(self.client.playerName)+" closed the room ["+roomName+"].")
                    self.client.sendClientMessage(f"The room {roomName} got closed.", 1)
                except KeyError:
                    self.client.sendClientMessage("The room [<J>"+roomName+"</J>] doesn't exists.", 1)
            else:
                roomName = self.client.room.name
                for player in [*self.client.room.clients.copy().values()]:
                    player.enterRoom(self.server.recommendRoom(player.langue))
                self.client.sendServerMessageOthers(str(self.client.playerName)+" closed the room ["+roomName+"].")
                self.client.sendClientMessage(f"The room {roomName} got closed.", 1)

        @self.command(level=5, arb=True, args=1)
        async def commu(self, community):
            community = community[0:2].upper()
            try:
                self.client.langueID = Langues.getLangues().index(community)
                self.client.langue = community
                self.client.enterRoom(self.server.recommendRoom(community))
            except:
                self.client.sendClientMessage(f"The community {community} is invalid.", 1)

        @self.command(level=7)
        async def creator(self, roomName=''):
            if roomName == '':
                self.client.sendClientMessage("Room [<J>"+self.client.room.name+"</J>]'s creator: <BV>"+self.client.room.roomCreator+"</BV>", 1)
            else:
                for room in self.server.rooms.values():
                    if room.community == roomName[0:2] and room.roomName == roomName[3:]:
                        self.client.sendClientMessage(f"Room [<J>{roomName}</J>]'s creator: <BV>"+room.roomCreator+"</BV>", 1)
                        return
                self.client.sendClientMessage(f"Room [<J>{roomName}</J>] does not exist.", 1)

        @self.command(level=7, arb=True, args=1, alies=['removerecord'])
        async def delrecord(self, mapCode):
            if await self.server.checkRecordMap(mapCode):
                await self.client.room.CursorMaps.execute("update Maps set Time = ? and Player = ? and RecDate = ? where Code = ?", [0, "", 0, str(mapCode)])
                self.client.sendServerMessage("The map's record: @"+str(mapCode)+" was removed by <BV>"+str(self.client.playerName)+"</BV>.")
            else:
                self.client.playerException.Invoke("norecordfound")

        @self.command(level=7, arb=True, args=1, alies=['chercher'])
        async def find(self, text):
            result = ""
            for player in self.server.players.copy().values():
                if player.playerName.startswith(text):
                    result += "<BV>%s</BV> -> %s\n" %(player.playerName, player.room.name)
            result = result.rstrip("\n")
            self.client.sendClientMessage(result, 1) if result != "" else self.client.sendClientMessage("No results were found.", 1)

        @self.command(level=7, arb=True, args=1, alies=['join'])
        async def follow(self, playerName):
            player = self.server.players.get(playerName)
            if player != None:
                self.client.enterRoom(player.roomName)
            else:
                self.client.playerException.Invoke("unknownuser")

        @self.command(level=7, arb=True)
        async def iban(self, playerName, hours, *args):
            result = self.server.checkBanUser(playerName)
            if result == -1:
                reason = self.argsNotSplited.split(" ", 2)[2]
                if self.server.checkConnectedAccount(playerName):
                    self.client.sendClientMessage(f"The player {playerName} got banned for {hours}h ({reason}).", 1)
                    self.client.sendServerMessageOthers(f"{self.client.playerName} banned the player {playerName} for {hours}h ({reason}).")
                    self.server.banPlayer(playerName, int(hours), reason, self.client.playerName, True)
                else:
                    self.client.sendClientMessage(f"The player {playerName} got banned for {hours}h ({reason}).", 1)
                    self.client.sendServerMessageOthers(f"{self.client.playerName} offline banned the player {playerName} for {hours}h ({reason}).")
                    self.server.banPlayer(playerName, int(hours), reason, self.client.playerName, True)
            elif result == 1:
                self.client.playerException.Invoke("useralreadybanned", playerName)
            else:
                self.client.playerException.Invoke("unknownuser")

        @self.command(level=7, arb=True, args=1)
        async def ibanhack(self, playerName):
            player = self.server.players.get(playerName)
            if player != None:
                hours = self.server.getTotalBanHours(playerName) // 360
                if hours <= 0:
                    hours = 1
                hours *= 360
                reason = "Hack. Your account will be permanently banned if you continue to violate the rules!"
                t = self.server.fastRacingRecords
                if playerName in t["records"]:
                    s = [playerName,len(t["records"][playerName])]
                    if s in t["sequentialrecords"]:
                        index = t["sequentialrecords"].index(s)
                        t["sequentialrecords"].pop(index)
                    for mapcode in t["records"][playerName]:
                        if mapcode in t["recordmap"]:
                            del t["recordmap"][mapcode]
                    del t["records"][playerName]
                    await self.client.room.CursorMaps.execute("update Maps set Time = ?, Player = ?, RecDate = ? where Player = ?", [0, "", 0, playerName])
                self.server.banPlayer(player.playerName, hours, reason, self.client.playerName, True)
                self.client.sendServerMessageOthers("%s banned the player %s for %sh (%s)" %(self.client.playerName, playerName, hours, reason))
            else:
                self.client.playerException.Invoke("unknownuser")

        @self.command(level=7, arb=True)
        async def imute(self, playerName, hours, *args):
            if self.server.checkExistingUser(playerName):
                if self.server.checkTempMute(playerName):
                    self.client.playerException.Invoke("useralreadymuted", playerName)
                else:
                    reason = self.argsNotSplited.split(" ", 2)[2]
                    mutehours = int(hours) if hours.isdigit() else 1
                    mutehours = 9999999 if (mutehours > 9999999) else mutehours
                    self.server.mutePlayer(playerName, mutehours, reason, self.client.playerName, True, True)
                    self.client.sendClientMessage(f"The player {playerName} got muted", 1)
            else:
                self.client.playerException.Invoke("unknownuser")

        @self.command(level=7)
        async def infotribu(self, *args):
            tribeName = self.argsNotSplited.split(" ", 0)[0]
            message = f"<p align='center'>Tribe <J>{tribeName}</J><BR>"
            r = self.Cursor['tribe'].find({'Name':tribeName})
            for rs in r:
                totalmembers = len(self.client.tribulle.getTribeMembers(rs["Code"]))
                tribehouse = str(rs["House"])
                tribeid = str(rs["Code"])
                message += "<p align='left'><N>Id:</N> <R>%s</R><BR><N>Tribehouse map : @%s</N><BR><BR><N>Members: %s</N><BR>" % (tribeid, tribehouse, totalmembers)
                for member in self.client.tribulle.getTribeMembers(rs["Code"]):
                    tribeRank = self.client.tribulle.getPlayerTribeRank(member)
                    rankInfo = rs["Ranks"].split(";")
                    rankName = rankInfo[tribeRank].split("|")
                    pl1 = self.server.players.get(member)
                    if pl1 != None:
                        message += f"<N>-<N> <V>{member}</V> : <BL>{rankName[1]}</BL> <N>(</N><font color = '{pl1.ipDetails[3]}'>{Utils.EncodeIP(pl1.ipAddress)}</font><N> / {pl1.roomName})</N>\n"
                    else:
                        message += f"<N>-<N> <V>{member}</V> : <BL>{rankName[1]}</BL>\n"
                message += "<BR><N>Ranks & rights:</N><BR>"
                perms = []
                for i in range(0, 10):
                    ranks = rs["Ranks"].split(";")
                    ranks = ranks[i].split("|")
                    rankid = int(ranks[2])
                    message += "<N> - </N><V>"+str(ranks)+"</V>\n"
            if message != f"<p align='center'>Tribe <J>{tribeName}</J><BR>":
                self.client.sendLogMessage(message)
            else:
                self.client.sendClientMessage(f"The tribe <BV>{tribeName}</BV> does not exist.", 1)

        @self.command(level=7, args=1, arb=True)
        async def ip(self, playerName):
            player = self.server.players.get(playerName)
            if player != None:
                self.client.sendClientMessage(f"<BV>{playerName}</BV>'s IP address: {Utils.EncodeIP(player.ipAddress)}\n {player.ipDetails[0]} - {player.ipDetails[1]} ({player.ipDetails[2]}) - Community [{player.langue}]", 1)
            else:
                self.client.playerException.Invoke("unknownuser")

        @self.command(level=7, arb=True, args=1)
        async def ipnom(self, ipAddress):
            List = "Logs for the IP address ["+ipAddress+"]:"
            for rs in self.Cursor['loginlogs'].find({'Ip':ipAddress}).distinct("Username"):
                if self.server.checkConnectedAccount(rs):
                    List += "<br>" + rs + " <G>(online)</G>"
                else:
                    List += "<br>" + rs
            self.client.sendClientMessage(List, 1)

        @self.command(level=7, arb=True, args=1)
        async def kick(self, playerName):
            player = self.server.players.get(playerName)
            if player != None:
                player.room.removeClient(player)
                player.transport.close()
                self.client.sendServerMessageOthers(f"The player {playerName} has been kicked by {self.client.playerName}.")
                self.client.sendClientMessage(f"The player {playerName} got kicked", 1)
            else:
                self.client.playerException.Invoke("unknownuser")

        @self.command(level=7, args=1, arb=True)
        async def l(self, xxx):
            if "." not in xxx:
                r = self.Cursor['loginlogs'].find({'Username':xxx})
                if r == None:
                    self.client.playerException.Invoke("notloggedin", xxx)
                else:
                    message = "<p align='center'>Connection logs for player: <BL>"+xxx+"</BL>\n</p>"
                    for rs in r[0:200]:
                        message += f"<p align='left'><V>[ {xxx} ]</V> <BL>{rs['Time']}</BL><G> ( <font color = '{rs['IPColor']}'>{rs['Ip']}</font> - {rs['Country']} ) {rs['ConnectionID']} - {rs['Community']}</G><br>"
                    self.client.sendLogMessage(message)
            else:
                r = self.Cursor['loginlogs'].find({'Ip':xxx})
                if r == None:
                    pass
                else:
                    message = "<p align='center'>Connection logs for IP Address: <V>"+xxx.upper()+"</V>\n</p>"
                    for rs in r[0:200]:
                        message += f"<p align='left'><V>[ {rs['Username']} ]</V> <BL>{rs['Time']}</BL><G> ( <font color = '{rs['IPColor']}'>{xxx}</font> - {rs['Country']} ) {rs['ConnectionID']} - {rs['Community']}</BL><br>"
                    self.client.sendLogMessage(message)

        @self.command(level=7)
        async def log(self):
            message = "<p align='center'><N>Sanction Logs</N>\n</p>"
            r = self.Cursor['casierlog'].find({})
            for rs in r[0:200]:
                name,ip,state,timestamp,modName,time,reason = rs['Name'],rs['IP'],rs['State'],rs['Timestamp'],rs['Moderator'],rs['Time'],rs['Reason']
                fromtime = str(datetime.fromtimestamp(float(int(timestamp))))
                if time == '': time = 0
                sanctime = (int(time)*60*60)
                totime = datetime.fromtimestamp(float(int(timestamp) + sanctime))
                totime1 = datetime.utcfromtimestamp(float(int(timestamp) + sanctime))
                if state not in ["UNMUTE", "UNBAN", "MUMUTE"]:
                    message = message + "<N><font size='12'><p align='left'> - <b><V></N>" + state + " " + str(time) + "h</V></b><N> (" + str(ip) + ") by " + modName + " : <BL>" + reason + "</BL>\n"
                    if totime1 != None:
                        message = message + "<p align='left'><font size='9'><N2>    " + fromtime + " | "+ str(totime) + " → "+ str(totime1) + "</N2>\n\n"
                    elif totime != None:
                        message = message + "<p align='left'><font size='9'><N2>    " + fromtime + " → "+ str(totime) + "</N2>\n\n"
                    else:
                        message = message + "<p align='left'><font size='9'><N2>    " + fromtime + "</N2>\n\n"
            self.client.sendLogMessage(message)

        @self.command(level=7, arb=True)
        async def ls(self, *args):
            if self.currentArgsCount == 0:
                data = []
                for room in self.server.rooms.values():
                    bulle = "bulle" + str(room.bulle_id)
                    if room.name.startswith("*") and not room.name.startswith("*" + chr(3)):
                        data.append(["xx", room.name, room.getPlayerCount(), bulle if not room.isTribeHouse else "maison"])
                    elif room.name.startswith(str(chr(3))) or room.name.startswith("*" + chr(3)):
                        if room.name.startswith(("*" + chr(3))):
                            data.append(["xx", room.name, room.getPlayerCount(), bulle if not room.bulle_id == 8 else "maison"])
                        else:
                            data.append(["*", room.name, room.getPlayerCount(), bulle if not room.bulle_id == 8 else "maison"])
                    else:
                        data.append([room.community, room.roomName, room.getPlayerCount(), bulle if not room.bulle_id == 8 else "maison"])
                result = "<N>List of rooms:</N>"
                for roomInfo in data:
                    if roomInfo[3] == "maison":
                        result += "\n<BL>%s</BL> <G>(%s / %s) :</G> <V>%s</V>" % (roomInfo[1] ,str.lower(roomInfo[0]), roomInfo[3], roomInfo[2])
                    else:
                        result += "\n<BL>%s-%s</BL> <G>(%s / %s) :</G> <V>%s</V>" % (str.lower(roomInfo[0]), roomInfo[1] ,str.lower(roomInfo[0]), roomInfo[3], roomInfo[2])
                result += "\n<J>Total players:</J> <R>%s</R>" %(len(self.server.players))
                self.client.sendLogMessage(result)
            else:
                roomName = self.argsNotSplited.split(" ", 0)[0] if (len(args) >= 1) else ""
                totalusers = 0
                users, rooms, message = 0, [], ""
                for room in self.server.rooms.values():
                    bulle = "bulle" + str(room.bulle_id)
                    if room.name.find(roomName) != -1:
                        rooms.append([room.name, room.community, room.getPlayerCount(), bulle if not room.bulle_id == 8 else "maison"])
                        
                message += "<N>List of rooms matching [%s]:</N>" % (roomName)
                for roomInfo in rooms:
                    message += "\n"
                    message += "<BL>%s <G>(%s / %s)</G> : <V>%s</V>" % (str.lower(roomInfo[0]), str.lower(roomInfo[1]), roomInfo[3], roomInfo[2])
                    totalusers = totalusers + roomInfo[2]
                message += "\n<J>Total players:</J> <R>%s</R>" % (totalusers)
                self.client.sendLogMessage(message)

        @self.command(level=7, arb=True)
        async def lsarb(self):
            Arbitres = ""
            for player in self.server.players.copy().values():
                if player.isArbitre or player.privLevel == 7:
                    Arbitres += "<font color='#B993CA'>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </font><br>"
            if Arbitres != "":
                self.client.sendMessage(Arbitres.rstrip("\n"))
            else:
                self.client.sendClientMessage("Don't have any online Arbitres at moment.", 1)

        @self.command(level=7, arb=True)
        async def lsc(self):
            result = {}
            for room in self.server.rooms.values():
                if room.community in result:
                    result[room.community] = result[room.community] + room.getPlayerCount()
                else:
                    result[room.community] = room.getPlayerCount()
            message = ""
            for community in result.items():
                if community[1] > 0:
                    message += "<BL>%s:<BL> <V>%s</V>\n" %(community[0].upper(), community[1])
            message += "<J>Total players:</J> <R>%s</R>" %(sum(result.values()))
            self.client.sendLogMessage(message)

        @self.command(level=7, arb=True)
        async def lsmodo(self):
            Moderateurs = ""
            for player in self.server.players.copy().values():
                if player.privLevel == 8:
                    Moderateurs += "<font color='#C565FE'>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </font><br>"
            if Moderateurs != "":
                self.client.sendMessage(Moderateurs.rstrip("\n"))
            else:
                self.client.sendClientMessage("Don't have any online Moderators at moment.", 1)

        @self.command(level=7, arb=True)
        async def lsroom(self, *args):
            if self.currentArgsCount == 0:
                Message = "Players in room ["+str(self.client.roomName[:2].lower() + self.client.roomName[2:])+"]: "+str(self.client.room.getPlayerCount())+"\n"
                for player in [*self.client.room.clients.copy().values()]:
                    if not player.isHidden:
                        Message += "<BL>%s / </BL><font color = '%s'>%s</font> <G>(%s)</G>\n" % (player.playerName, player.ipDetails[3], Utils.EncodeIP(player.ipAddress), player.ipDetails[1])
                    else:
                        Message += "<BL>%s / </BL><font color = '%s'>%s</font> <G>(%s)</G> <BL>(invisible)</BL>\n" % (player.playerName, player.ipDetails[3], Utils.EncodeIP(player.ipAddress), player.ipDetails[1])
                Message = Message.rstrip("\n")
                self.client.sendClientMessage(Message, 1)
            else:
                roomName = self.argsNotSplited.split(" ", 0)[0]
                try:
                    players = 0
                    for player in [*self.server.rooms[roomName].clients.values()]:
                        players += 1
                    Message = "<V>[•]</V> Players in room ["+roomName+"]: "+str(players)+"\n"
                    for player in [*self.server.rooms[roomName].clients.values()]:
                        if not player.isHidden:
                            Message += "<BL>%s / </BL><font color = '%s'>%s</font> <G>(%s)</G>\n" % (player.playerName, player.ipDetails[3], Utils.EncodeIP(player.ipAddress), player.ipDetails[1])
                        else:
                            Message += "<BL>%s / </BL><font color = '%s'>%s</font> <G>(%s)</G> <BL>(invisible)</BL>\n" % (player.playerName, player.ipDetails[3], Utils.EncodeIP(player.ipAddress), player.ipDetails[1])
                    Message = Message.rstrip("\n")
                    self.client.sendClientMessage(Message, 1)
                except KeyError:
                    self.client.sendClientMessage("The room ["+roomName+"] doesn't exist.", 1)

        @self.command(level=7)
        async def max(self):
            self.client.sendClientMessage(f"Total Players: {len(self.server.players.copy().values())} / {self.server.MaximumPlayers}", 1)

        @self.command(level=7, arb=True, args=1)
        async def mumute(self, playerName):
            if self.server.checkConnectedAccount(playerName):
                self.server.sendMumute(playerName, self.client.playerName)
                self.client.sendClientMessage(""+ playerName + " got mumuted.", 1)

        @self.command(level=7, arb=True)
        async def mute(self, playerName, hours, *args):
            if self.server.checkExistingUser(playerName):
                if self.server.checkTempMute(playerName):
                    self.client.playerException.Invoke("useralreadymuted", playerName)
                else:
                    reason = self.argsNotSplited.split(" ", 2)[2]
                    mutehours = int(hours) if hours.isdigit() else 1
                    mutehours = 9999999 if (mutehours > 9999999) else mutehours
                    self.server.mutePlayer(playerName, mutehours, reason, self.client.playerName, True, False)
                    self.client.sendClientMessage(f"The player {playerName} got muted", 1)
            else:
                self.client.playerException.Invoke("unknownuser")

        @self.command(level=7, arb=True, args=1)
        async def ninja(self, playerName):
            player = self.server.players.get(playerName)
            if player != None:
                if self.server.players[player.playerName].followed == None:
                    if player.playerName != self.client.playerName:
                        roomName = player.room.name
                        if not roomName == "" and not roomName == self.client.roomName and not "[Editeur]" in roomName and not "[Totem]" in roomName:
                            self.client.isHidden = True
                            self.client.sendPlayerDisconnect()
                            self.client.isDead = True
                            self.client.enterRoom(roomName)
                            self.client.sendPacket(Identifiers.send.Watch, ByteArray().writeUTF(player.playerName).writeBoolean(True).toByteArray())
                            self.server.players[player.playerName].followed = self.client
                            self.client.sendServerMessage(self.client.playerName+ " has ninja'd the player "+player.playerName)
                else:
                    self.client.isHidden = False
                    self.client.sendPacket(Identifiers.send.Watch, ByteArray().writeUTF("").writeBoolean(False).toByteArray())
                    self.client.enterRoom(self.client.lastroom)
                    self.server.players[player.playerName].followed == None
            else:
                self.client.playerException.Invoke("unknownuser")

        @self.command(level=7, arb=True, args=1)
        async def nomip(self, playerName):
            player = self.server.players.get(playerName)
            if player != None:
                ipList=playerName+"'s last known IP addresses:"
                for rs in self.Cursor['loginlogs'].find({'Username':playerName}).distinct("Ip"):
                    ipList += "<br>" + rs
                self.client.sendClientMessage(ipList, 1)
            else:
                self.client.playerException.Invoke("unknownuser")

        @self.command(level=7, arb=True, args=1)
        async def prison(self, playerName):
            player = self.server.players.get(playerName)
            if player != None:
                if player.isPrisoned:
                    player.isPrisoned = False
                    self.client.sendServerMessageOthers(f"{player.playerName} unprisoned by {self.client.playerName}.")
                    self.client.sendClientMessage(f"{player.playerName} got unprisoned.", 1)
                    player.enterRoom("1")
                else:
                    player.enterRoom(self.client.roomName)
                    player.isPrisoned = True
                    self.client.sendServerMessageOthers(f"{player.playerName} prisoned by {self.client.playerName}.")
                    self.client.sendClientMessage(f"{player.playerName} got prisoned.", 1)
            else:
                self.client.playerException.Invoke("unknownuser")

        @self.command(level=7, args=1, arb=True)
        async def relation(self, playerName):
            player = self.server.players.get(playerName)
            if player != None:
                displayed = []
                List = "The player <BV>"+str(player.playerName)+"</BV> has the following relations:"
                rss = self.Cursor['loginlogs'].find({"Ip":Utils.EncodeIP(player.ipAddress)})
                for rs in rss:
                    if rs['Username'] in displayed: continue
                    if self.server.players.get(str(rs['Username'])) == None:
                        d = self.Cursor['loginlogs'].find({"Username":str(rs['Username'])})
                        ips = []
                        ips2 = []
                        for i in d:
                            if i['Ip'] in ips2: continue
                            ips.append(f"<font color='{i['IPColor']}'>{i['Ip']}</font>")
                            ips2.append(i['Ip'])
                        toshow = ", ".join(ips)
                        List += f"<br>- <BV>{rs['Username']}</BV> : {toshow}"
                    else:
                        ip31 = self.server.players.get(str(rs['Username']))
                        List += f"<br>- <BV>{rs['Username']}</BV> : <font color='{ip31.ipDetails[3]}'>{Utils.EncodeIP(ip31.ipAddress)}</font> (current IP)"
                    displayed.append(rs['Username'])
                self.client.sendClientMessage(List, 1)
            else:
                self.client.playerException.Invoke("unknownuser")

        @self.command(level=5, arb=True, args=1, alies=["room*", "salon*", "sala*"])
        async def __commande_roomasterisk(self, roomName):
            community = roomName[0:2].upper()
            try:
                self.client.langueID = Langues.getLangues().index(community)
                self.client.langue = community
                self.client.enterRoom(roomName)
            except:
                self.client.sendClientMessage(f"The community {community} is invalid.", 1)

        @self.command(level=5, arb=True, fc=True, args=1)
        async def roomkick(self, playerName):
            if (self.client.privLevel == 5 or self.client.isFunCorpPlayer) and not self.client.room.isFuncorp and self.currentArgsCount > 0:
                return
            elif not self.client.privLevel in [7, 8, 9] and not self.isArbitre:
                return
            player = self.server.players.get(playerName)
            if player != None:
                self.client.sendServerMessageOthers(f"{player.playerName} has been roomkicked from [{str.lower(player.room.name)}] by {self.client.playerName}.")
                self.client.sendClientMessage(f"{player.playerName} got kicked from the room.", 1)
                player.startBulle(self.server.recommendRoom(player.langue))
            else:
                self.client.playerException.Invoke("unknownuser")

        @self.command(level=7, arb=True, args=1, alies=['deban'])
        async def unban(self, playerName):
            result = self.server.checkBanUser(playerName)
            if result == 1:
                self.server.removeTempBan(playerName)
                if playerName in self.server.reports:
                    self.server.reports[playerName]['bannedby'] = ""
                    self.server.reports[playerName]['banhours'] = 0
                    self.server.reports[playerName]['banreason'] = ""
                    self.server.reports[playerName]['state'] = "disconnected"
                self.client.sendClientMessage(f"The player {playerName} got unbanned.", 1)
                self.client.sendServerMessageOthers(f"{self.client.playerName} unbanned the player {playerName}.")
                self.server.saveCasier(playerName, "UNBAN", self.client.playerName, "", "")
            elif result == -1:
                self.client.playerException.Invoke("usernotbanned", playerName)
            else:
                self.client.playerException.Invoke("unknownuser")

        @self.command(level=9, args=1, alies=['debanip'])
        async def unbanip(self, ipAddress):
            decip = Utils.DecodeIP(ip)
            if decip in self.server.IPTempBanCache:
                self.server.removeTempBanIP(decip)
                self.client.sendServerMessageOthers(f"{self.client.playerName} unbanned the ip address {ip}.")
                self.client.sendClientMessage(f"The ip address {ip} got unbanned.", 1)
            else:
                self.client.sendClientMessage("The IP is invalid or not banned.", 1)

        @self.command(level=7, arb=True, args=1, alies=['demute'])
        async def unmute(self, playerName):
            if self.server.checkExistingUser(playerName):
                if self.server.checkTempMute(playerName):
                    self.client.sendServerMessageOthers(f"{self.client.playerName} unmuted the player {playerName}.")
                    self.client.sendClientMessage(f"The player {playerName} got unmuted.", 1)
                    self.server.removeModMute(playerName)
                    self.client.isMute = False
                    self.server.saveCasier(playerName, "UNMUTE", self.client.playerName, "", "")
                    if playerName in self.server.reports:
                        self.server.reports[playerName]['isMuted'] = False
                        self.server.reports[playerName]['muteHours'] = 0
                        self.server.reports[playerName]['muteReason'] = ""
                        self.server.reports[playerName]['mutedBy'] = ""
                else:
                    self.client.playerException.Invoke("usernotmuted", playerName)
            else:
                self.client.playerException.Invoke("unknownuser")


# Modo Commands
        @self.command(level=8)
        async def clearchat(self):
            self.client.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("\n" * 10000).toByteArray())

        @self.command(level=8)
        async def mm(self, *args):
            self.client.room.sendAll(Identifiers.send.Staff_Chat, ByteArray().writeByte(0).writeUTF("").writeUTF(self.argsNotSplited).writeShort(0).writeByte(0).toByteArray())

        @self.command(level=8, args=2)
        async def moveplayer(self, playerName, roomName):
            player = self.server.players.get(playerName)
            if player != None:
                newRoom = player.room.name
                player.startBulle(roomName)
                self.client.sendServerMessageOthers(f"{player.playerName} has been moved from ({str.lower(newRoom)}) to ({str.lower(player.room.name)}) by {self.client.playerName}.")
                self.client.sendClientMessage(f"{player.playerName} has been moved from {str.lower(newRoom)} to {str.lower(player.room.name)} ", 1)
            else:
                self.client.playerException.Invoke("unknownuser")

        @self.command(level=8, args=1)
        async def removeplayerrecords(self, playerName):
            t = self.server.fastRacingRecords
            if playerName in t["records"]:
                s = [playerName,len(t["records"][playerName])]
                if s in t["sequentialrecords"]:
                    index = t["sequentialrecords"].index(s)
                    t["sequentialrecords"].pop(index)
                for mapcode in t["records"][playerName]:
                    if mapcode in t["recordmap"]:
                        del t["recordmap"][mapcode]
                del t["records"][playerName]
                await self.client.room.CursorMaps.execute("update Maps set Time = ?, Player = ?, RecDate = ? where Player = ?", [0, "", 0, playerName])
                self.client.sendServerMessageOthers(f"The records of {playerName} were removed by {self.client.playerName}.")
                self.client.sendClientMessage(f"{playerName}'s records got removed.", 1)
            else:
                self.client.playerException.Invoke("norecordsfound")

# Admin Commands
        @self.command(level=9, args=3) #######
        async def addcode(self, name, type, amount):
            data = json.loads(open('./include/json/codes.json','r').read())
            if type == "fraises" or type == "cheeses":
                data['codes'].append({'name': name.upper(), 'type': type, 'amount': amount, 'havegot': 0})
                with open('./include/json/codes.json', 'w') as F:
                    json.dump(data, F)
                self.server.gameCodes['codes'] = data['codes']
                self.client.sendClientMessage(f"Successfull added code [<N>{name}</N>].", 1)
            else:
                self.client.sendClientMessage("The type of code is invalid.", 1)

        @self.command(level=9, args=1)
        async def baniperm(self, ip):
            decip = Utils.DecodeIP(ip)
            if decip not in self.server.IPPermaBanCache:
                self.server.IPPermaBanCache.append(decip)
                self.Cursor['ippermaban'].insert_one({'Ip':decip})
                for player in self.server.players.copy().values():
                    if player.ipAddress == decip:
                        player.transport.close()
                self.client.sendServerMessageOthers(f"{self.client.playerName} permanently banned the IP address {ip}.")
                self.client.sendClientMessage(f"The ip address {ip} got blacklisted.", 1)
            else:
                self.client.sendClientMessage("The IP is already banned.", 1)

        @self.command(level=9, args=2)
        async def changepassword(self, playerName, newPassword):
            player = self.server.players.get(playerName)
            if player != None:
                salt = b'\xf7\x1a\xa6\xde\x8f\x17v\xa8\x03\x9d2\xb8\xa1V\xb2\xa9>\xddC\x9d\xc5\xdd\xceV\xd3\xb7\xa4\x05J\r\x08\xb0'
                hashtext = base64.b64encode(hashlib.sha256(hashlib.sha256(newPassword.encode()).hexdigest().encode() + salt).digest()).decode()
                self.Cursor['users'].update_one({'Username':playerName},{'$set':{'Password': hashtext}})
                player.updateDatabase()
                player.room.removeClient(player)
                player.transport.close()
            else:
                self.client.playerException.Invoke("unknownuser")

        @self.command(level=9, args=1)
        async def commandlog(self, playerName):
            r = self.Cursor['commandlog'].find({'Username':playerName})
            message = "<p align='center'>Command Log of (<V>"+playerName+"</V>)\n</p>"
            for rs in r:
                d = str(datetime.fromtimestamp(float(int(rs['Time']))))
                message += "<p align='left'><V>[%s]</V> <FC> - </FC><VP>use command:</VP> <V>/%s</V> <FC> ~> </FC><VP>[%s]\n" % (playerName,rs['Command'],d)
            self.client.sendLogMessage(message)

        @self.command(level=9, args=1, alies=['deluser', 'deleteaccount'])
        async def deleteuser(self, playerName):
            if playerName == self.client.playerName:
                self.client.sendClientMessage("You cannot delete yourself, idiot!", 1)
            elif self.server.checkExistingUser(playerName):
                self.Cursor['users'].delete_one({'Username':playerName})
                self.client.sendServerMessageAdminOthers(f"The account {playerName} was deleted by {self.client.playerName}")
                self.client.sendClientMessage(f"The account {playerName} got deleted.", 1)
            else:
                self.client.playerException.Invoke("unknownuser")

        @self.command(level=9)
        async def move(self, roomName):
            for player in [*self.client.room.clients.copy().values()]:
                player.enterRoom(self.argsNotSplited)

        @self.command(level=9, args=1)
        async def resetprofile(self, playerName):
            player = self.server.players.get(playerName)
            if player != None:
                self.Cursor['users'].update_one({'Username':playerName}, {'$set':{"PrivLevel":1,"TitleNumber":0,"FirstCount":0,"CheeseCount":0,"ShamanCheeses":0,"ShopCheeses":0,"ShopFraises":0,"ShamanSaves":0,"ShamanSavesNoSkill":0,"HardModeSaves":0,"HardModeSavesNoSkill":0,"DivineModeSaves":0,"DivineModeSavesNoSkill":0,"BootcampCount":0,"ShamanType":0,"ShopItems":"","ShamanItems":"","Clothes":"","Look":"1;0,0,0,0,0,0,0,0,0,0,0","ShamanLook":"0,0,0,0,0,0,0,0,0,0","MouseColor":"78583a","ShamanColor":"95d9d6","RegDate":Utils.getTime(),"Badges":"","CheeseTitleList":"","FirstTitleList":"","ShamanTitleList":"","ShopTitleList":"","BootcampTitleList":"","HardModeTitleList":"","DivineModeTitleList":"","SpecialTitleList":"","BanHours":0,"ShamanLevel":0,"ShamanExp":0,"ShamanExpNext":0,"Skills":"","LastOn":32,"FriendsList":"","IgnoredsList":"","Gender":0,"LastDivorceTimer":0,"Marriage":"","TribeCode":0,"TribeRank":0,"TribeJoined":0,"Gifts":"","Messages":"","SurvivorStats":"0,0,0,0","RacingStats":"0,0,0,0","DefilanteStats":"0,0,0","Consumables":"","EquipedConsumables":"","Pet":0,"PetEnd":0,"Fur":0,"FurEnd":0,"ShamanBadges":"","EquipedShamanBadge":0,"totemitemcount":0,"totem":"","VisuDone":"","customitems":"","AventureCounts":"","AventurePoints":"24:0","AventureSaves":0,"Letters":"","Time":0,"Karma":0,"Roles":"{}"}})
                self.client.sendServerMessageAdminOthers(f"The account {playerName} was reset by {self.client.playerName}")
                self.client.sendClientMessage(f"The account {playerName} got reset.", 1)
                player.updateDatabase()
                player.room.removeClient(player)
                player.transport.close()
            else:
                self.client.playerException.Invoke("unknownuser")

        @self.command(level=9, alies=['deleterecords'])
        async def resetrecords(self):
            await self.client.room.CursorMaps.execute("update Maps set Time = ?, Player = ?, RecDate = ?", [0, "", 0])
            self.client.sendClientMessage("Records got deleted.", 1)
            self.client.sendServerMessageAdminOthers("All records of fastracing were deleted by %s."%(self.client.playerName))

        @self.command(level=9, args=1, alies=['re', 'revive'])
        async def respawn(self, playerName):
            if playerName in self.client.room.clients:
                self.client.room.respawnSpecific(playerName)
                self.client.sendClientMessage(f"Successfull respawned {playerName}.", 1)

        @self.command(level=9, args=1, alies=['setroundtime'])
        async def settime(self, time):
            time = int(time)
            time = 5 if time < 1 else (32767 if time > 32767 else time)
            for player in self.client.room.clients.copy().values():
                player.sendRoundTime(time)
            self.client.room.changeMapTimers(time)
            self.client.sendClientMessage(f"Successfull added {time} seconds to current round.", 1)

        @self.command(level=9)
        async def updatesql(self):
            self.server.updateServer()
            self.client.sendServerMessageAdminOthers(f"The database was updated by {self.client.playerName}.")
            self.client.sendClientMessage("The database got updated.", 1)

        @self.command(level=9, args=1, alies=['removepermmap', 'harddel'])
        async def removemap(self, mapCode):
            mapCode = mapCode.replace('@', '')
            await self.client.room.CursorMaps.execute("delete from Maps where Code = ?", [mapCode])
            self.client.sendClientMessage(f"Successfull deleted the map: @{mapCode} from database.", 1)
       
        @self.command(level=9)
        async def smc(self, *args):
            for room in self.server.rooms.values():
                room.sendAll(Identifiers.send.Staff_Chat, ByteArray().writeByte(6).writeUTF(self.client.langue.lower() + " " + self.client.playerName).writeUTF(self.argsNotSplited).writeShort(0).writeByte(0).toByteArray())

        @self.command(level=9, args=1, alies=['debaniperm'])
        async def unbaniperm(self, ipAddress):
            decip = Utils.DecodeIP(ip)
            if decip in self.server.IPPermaBanCache:
                self.server.IPPermaBanCache.remove(decip)
                self.Cursor['ippermaban'].delete_one({'Ip':decip})
                self.client.sendServerMessageAdminOthers(f"{self.client.playerName} unbanned the ip address {ip}.")
                self.client.sendClientMessage(f"The ip address {ip} got unbanned.", 1)
            else:
                self.client.sendClientMessage("The IP is invalid or not banned.", 1)

# Owner Commands
        @self.command(owner=True, args=1)
        async def clearlogs(self, type_log):
            if type_log == "reports":
                self.server.reports = {}
                self.client.sendClientMessage("Successfull.", 1)
                self.client.sendServerMessageAdminOthers("The player %s cleared all reports from modopwet." %(self.client.playerName))
            elif type_log == "ippermacache":
                self.server.IPPermaBanCache = []
                self.client.sendClientMessage("Successfull.", 1)
                self.client.sendServerMessageAdminOthers("The player %s clear the cache of the server." %(self.client.playerName))
            elif type_log == "iptempcache":
                self.server.IPTempBanCache = []
                self.client.sendClientMessage("Successfull.", 1)
                self.client.sendServerMessageAdminOthers("The player %s cleared all IP bans." %(self.client.playerName))
            elif type_log == "banlog":
                Cursor['casierlog'].delete_many({})
                Cursor['ippermaban'].delete_many({})
                Cursor['usertempban'].delete_many({})
                self.client.sendClientMessage("Successfull.", 1)
                self.client.sendServerMessageAdminOthers("The player %s cleared casier database." %(self.client.playerName))
            elif type_log == "loginlog":
                Cursor['loginlogs'].delete_many({})
                self.client.sendClientMessage("Successfull.", 1)
                self.client.sendServerMessageAdminOthers("The player %s cleared loginlog database." %(self.client.playerName))
            elif type_log == "commandlog":
                Cursor['commandlog'].delete_many({})
                self.client.sendClientMessage("Successfull.", 1)
                self.client.sendServerMessageAdminOthers("The player %s cleared commandlog database." %(self.client.playerName))
            else:
                self.client.sendClientMessage("Available options are: reports, ippermacache, iptempcache, banlog, loginlog and commandlog.", 1)

        @self.command(owner=True)
        async def luaadmin(self):
            self.client.isLuaAdmin = not self.client.isLuaAdmin
            self.client.sendClientMessage("You can run lua programming as administrator." if self.client.isLuaAdmin else "You can't run lua programming as administrator.", 1)

        @self.command(owner=True, alies=['restart'])
        async def reboot(self):
            self.server.sendServerRestart()

        @self.command(owner=True)
        async def reload(self):
            if self.client.playerName in self.owners:
                try:
                    await self.server.reloadServer()
                    self.client.sendClientMessage("Successfull reloaded all modules.", 1)
                except Exception as e:
                    self.client.sendClientMessage(f"Failed reload all modules. Error: {e}", 1)

        @self.command(owner=True)
        async def serverconfigs(self):
            with open("./include/configs.properties", 'r') as File:
                Log = File.read()
                File.close()
            self.client.sendLogMessage(Log.replace("<", "&amp;lt;").replace("\x0D\x0A", "\x0A"))

        @self.command(owner=True, args=1)
        async def viewlog(self, log_type):
            if log_type == "errors":
                errors = ["Tribulle.log", "Commands.log", "Server.log"]
                for error in errors:
                    with open(f"./include/logs/Errors/{error}", 'r') as File:
                        Log = File.read()
                        File.close()
                    self.client.sendLogMessage(Log.replace("<", "&amp;lt;").replace("\x0D\x0A", "\x0A"))
                    Log = ""
            elif log_type == "cache":
                message = ""
                for ip in self.server.IPPermaBanCache:
                    message += ip
                self.client.sendLogMessage(message)
                
            elif log_type == "iptemp":
                message = ""
                for ip in self.server.IPTempBanCache:
                    message += ip
                self.client.sendLogMessage(message)
                
            elif log_type == "debug":
                with open(f"./include/logs/Errors/Debug.log", 'r') as File:
                    Log = File.read()
                    File.close()
                self.client.sendLogMessage(Log.replace("<", "&amp;lt;").replace("\x0D\x0A", "\x0A"))
                
            elif log_type == "promotions":
                message = ""
                for promotion in self.server.shopPromotions:
                    message += str(promotion) + ", "
                self.client.sendLogMessage(message[:-1])
                
            elif log_type == "shopoutfits":
                message = ""
                for promotion in self.server.shopOutfits:
                    message += str(promotion) + ", "
                self.client.sendLogMessage(message[:-1])
            else:
                self.client.sendClientMessage("Available options are: cache, iptemp, debug, promotions, and shopoutfits.", 1)



# Predefined Commands in swf.
        @self.command(level=1, args=1) ###########
        async def codecadeau(self, code):
            xd = None
            for i in self.server.gameCodes['codes']:
                if code.upper() == i['name'] and i['havegot'] == 0:
                    r1 = i['type']
                    r2 = i["amount"]
                    if r1 == "cheeses":
                        self.client.sendPacket(Identifiers.send.Gain_Give, ByteArray().writeInt(r2).writeInt(0).toByteArray())
                        self.client.sendPacket(Identifiers.send.Anim_Donation, ByteArray().writeByte(0).writeInt(r2).toByteArray())
                        self.client.shopCheeses += int(r2)
                        i['havegot'] = 1
                        break
                    elif r1 == "fraises":
                        self.client.sendPacket(Identifiers.send.Gain_Give, ByteArray().writeInt(0).writeInt(r2).toByteArray())
                        self.client.sendPacket(Identifiers.send.Anim_Donation, ByteArray().writeByte(1).writeInt(r2).toByteArray())
                        self.client.shopFraises += int(r2)
                        i['havegot'] = 1
                        break

        @self.command(level=7)
        async def sonar(self, playerName, end=''): ############
            player = self.server.players.get(playerName)
            if player:
                self.client.sendPacket(Identifiers.send.Minibox_1, ByteArray().writeShort(200).writeUTF("Sonar "+playerName).writeUTF('\n'.join(self.server.sonar[playerName]) if playerName in self.server.sonar else "\n").toByteArray())
                self.server.sonar[playerName] = []
                if end == 'end':
                    import time as _time
                    if not int(_time.time() - self.lastsonar) > 2: 
                        self.currentArgsCount = 1
                    self.lastsonar = _time.time()
                if self.currentArgsCount == 1:
                    player.sendPacket(Identifiers.send.Init_Sonar, ByteArray().writeInt(player.playerCode).writeBoolean(True).writeShort(1).toByteArray())
                else:
                    player.sendPacket(Identifiers.send.End_Sonar, ByteArray().writeInt(player.playerCode).toByteArray())


        @self.command(level=1)
        async def test(self):
            self.client.sendPacket([28, 41], ByteArray().writeShort(2).toByteArray())


    def FunCorpPlayerCommands(self):
        message = "FunCorp Commands: \n\n"
        message += "<J>/changesize</J> <V>[playerNames|*] [size|off]</V> : <BL> Temporarily changes the size (between 0.1x and 5x) of players.</BL>\n"
        message += "<J>/colormouse </J> <V>[playerNames|*] [color|off]</V> : <BL> Temporarily gives a colorized fur.</BL>\n"
        message += "<J>/colornick</J> <V>[playerNames|*] [color|off]</V> : <BL> Temporarily changes the color of player nicknames.</BL>\n"
        message += "<J>/funcorp</J> <G>[on|off|help]</G> : <BL> Enable/disable the funcorp mode, or show the list of funcorp-related commands.</BL>\n"
        message += "<J>/linkmice</J> <V>[playerNames|*]</V> <G>[off]</G> : <BL> Temporarily links players.</BL>\n"
        message += "<J>/meep</J> <V>[playerNames|*]</V> <G>[off]</G> : <BL> Give meep to players.</BL>\n"
        message += "<J>/transformation</J> <V>[playerNames|*]</V> <G>[off]</G> : <BL> Temporarily gives the ability to transform.</BL>\n"
        return message
        
    def FunCorpMemberCommands(self):
        message = "FunCorp Commands: \n\n"
        message += "<J>/changenick</J> <V>[playerName] [newNickname|off]</V> : <BL> Temporarily changes a player's nickname.</BL>\n"
        message += "<J>/changesize</J> <V>[playerNames|*] [size|off]</V> : <BL> Temporarily changes the size (between 0.1x and 5x) of players.</BL>\n"
        message += "<J>/closeroom</J> : <BL>Close the current room.</BL>\n"
        #message += "<J>/colormouse </J> <V>[playerNames|*] [color|off]</V> : <BL> Temporarily gives a colorized fur.</BL>\n"
        #message += "<J>/colornick</J> <V>[playerNames|*] [color|off]</V> : <BL> Temporarily changes the color of player nicknames.</BL>\n"
        message += "<J>/commu</J> <V>[code]</V> : <BL>Lets you change your community. Ex: /commu fr</BL>\n"
        message += "<J>/funcorp</J> <G>[on|off|help]</G> : <BL> Enable/disable the funcorp mode, or show the list of funcorp-related commands.</BL>\n"
        message += "<J>/ignore</J> <V>[playerPartName]<V> : <BL> Ignore selected player. (aliases: /negeer, /ignorieren)\n"
        message += "<J>/linkmice</J> <V>[playerNames|*]</V> <G>[off]</G> : <BL> Temporarily links players.</BL>\n"
        message += "<J>/lsfc</J> : <BL> List of online funcorps.</BL>\n"
        message += "<J>/meep</J> <V>[playerNames|*]</V> <G>[off]</G> : <BL> Give meep to players.</BL>\n"
        message += "<J>/profil</J> <V>[playerPartName]</V> : <BL> Display player's info. (aliases: /profile, /perfil, /profiel)</BL>\n"
        message += "<J>/room*</J> <V>[roomName]</V> : <BL> Allows you to entyer into any room. (aliases: /salon*, /sala*)</BL>\n"
        message += "<J>/roomevent</J> <G>[on|off]</G> : <BL> Highlights the current room in the room list.</BL>\n"
        message += "<J>/roomkick</J> <V>[playerName]</V> : <BL> Kicks a player from a room.</BL>\n"
        message += "<J>/transformation</J> <V>[playerNames|*]</V> <G>[off]</G> : <BL> Temporarily gives the ability to transform.</BL>\n"
        message += "<J>/tropplein</J> <V>[maxPlayers]</V> : <BL> Setting a limit for the number of players in a room.</BL>\n"
        message += "<J>/music</J> <V>[MP3_URL]</V> : <BL> Start playing music in the room.</BL>\n"
        return message