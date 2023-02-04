#coding: utf-8
import re, sys, json, os, base64, hashlib, time, random, asyncio, ast
"""
9 Admin, 8 Mod, 7 Arb, 6 MC, 5 FC, 4 LC, 3 - FS, 2 Sentinel, 1 PPL
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
        self.owners = ["Chatta"]

    def requireTribePerm(self, permId):
        if self.client.room.isTribeHouse:
            rankInfo = self.client.tribeRanks.split(";")
            rankName = rankInfo[self.client.tribeRank].split("|")
            if rankName[2] in str(permId):
                return True
        return False
    
    def requireArguments(self, arguments, flag=False):
        if self.currentArgsCount < arguments:
            self.client.playerException.Invoke("moreargs")
            return False
        elif self.currentArgsCount == arguments:
            return True
        else:
            return flag

    async def parseCommand(self, command):                
        values = command.split(" ")
        command = values[0].lower()
        args = values[1:]
        argsCount = len(args)
        argsNotSplited = " ".join(args)
        self.currentArgsCount = argsCount
        self.Cursor.execute("insert into commandlog values (%s, %s, %s)", [Utils.getTime(), self.client.playerName, command])
        self.client.sendServerMessageAdmin("<J>[%s]</J> <BV>%s</BV> used command ----> <CH2>%s</CH2>" %(Utils.getTime(), self.client.playerName, command))
# Player Commands
        try:            
            if command in ["profile", "profil", "perfil", "profiel"]:
                if self.client.privLevel >= 1:
                    self.client.sendProfile(Utils.parsePlayerName(args[0]) if len(args) >= 1 else self.client.playerName)
			
            elif command in ["editeur", "editor"]:
                if self.client.privLevel >= 1:
                    self.client.sendPacket(Identifiers.send.Room_Type, 1)
                    self.client.enterRoom("\x03[Editeur] %s" %(self.client.playerName))
                    self.client.sendPacket(Identifiers.old.send.Map_Editor, [])

            elif command in ["totem"]:
                if self.client.privLevel >= 1 and self.client.shamanSaves >= self.server.minimumNormalSaves:
                    self.client.enterRoom("\x03[Totem] %s" %(self.client.playerName))
                                                                               
            elif command in ["sauvertotem"]:
                if self.client.room.isTotemEditor:
                    self.client.totem[0] = self.client.tempTotem[0]
                    self.client.totem[1] = self.client.tempTotem[1]
                    self.client.sendPlayerDied()
                    self.client.enterRoom(self.server.recommendRoom(self.client.langue))

            elif command in ["resettotem"]:
                if self.client.room.isTotemEditor:
                    self.client.totem = [0 , ""]
                    self.client.tempTotem = [0 , ""]
                    self.client.resetTotem = True
                    self.client.isDead = True
                    self.client.sendPlayerDied()
                    self.client.room.checkChangeMap()

            elif command in ["mod", "mods"]:
                if self.client.privLevel >= 1:
                    staffList, staff = "$ModoPasEnLigne", {}
                    for player in self.server.players.copy().values():
                        if player.privLevel == 8:
                            if player.langue.lower() in staff:
                                names = staff[player.langue.lower()]
                                names.append(player.playerName)
                                staff[player.langue.lower()] = names
                            else:
                                names = []
                                names.append(player.playerName)
                                staff[player.langue.lower()] = names
                    if len(staff) >= 1:
                        staffList = "$ModoEnLigne"
                        for list in staff.items():
                            staffList += "<br>[%s] <BV>%s</BV>" %(list[0], ("<BV>, <BV>").join(list[1]))
                    self.client.sendLangueMessage("", staffList)
                        
            elif command in ["mapcrew"]:
                if self.client.privLevel >= 1:
                    staffList, staff = "$MapcrewPasEnLigne", {}
                    for player in self.server.players.copy().values():
                        if player.privLevel == 6:
                            if player.langue.lower() in staff:
                                names = staff[player.langue.lower()]
                                names.append(player.playerName)
                                staff[player.langue.lower()] = names
                            else:
                                names = []
                                names.append(player.playerName)
                                staff[player.langue.lower()] = names
                    if len(staff) >= 1:
                        staffList = "$MapcrewEnLigne"
                        for list in staff.items():
                            staffList += "<br>[%s] <BV>%s</BV>" %(list[0], ("<BV>, </BV>").join(list[1]))
                    self.client.sendLangueMessage("", staffList)

            elif command in ["pw"]:
                if self.client.privLevel >= 1:
                    if self.client.room.roomCreator == self.client.playerName:
                        if len(args) == 0:
                            self.client.room.roomPassword = ""
                            self.client.sendLangueMessage("", "$MDP_Desactive")
                        else:
                            password = args[0]
                            self.client.room.roomPassword = password
                            self.client.sendLangueMessage("", "$Mot_De_Passe : %s" %(password))

            elif command in ["title", "titre", "titulo", "titel"]:
                if self.client.privLevel >= 1:
                    if len(args) == 0:
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
                        titleID = args[0]
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

            elif command in ["mort", "die", "kill"]:
                if not self.client.isDead and not self.client.room.disableMortCommand:
                    self.client.isDead = True
                    if not self.client.room.noAutoScore: self.client.playerScore += 1
                    self.client.sendPlayerDied()
                    self.client.room.checkChangeMap()

            elif command in ["skip"]:
                if self.client.privLevel >= 1 and self.client.canSkipMusic and self.client.room.isMusic and self.client.room.isPlayingMusic:
                    self.client.room.musicSkipVotes += 1
                    self.client.checkMusicSkip()

            elif command in ["mjj"]:
                roomName = args[0]
                if roomName.startswith("#"):
                    if roomName[1:] in self.server.minigames:
                        self.client.enterRoom(f"{self.client.langue.lower()}-{roomName}" + "1")
                else:
                    self.client.enterRoom(({0:"", 3:"vanilla", 8:"survivor", 9:"racing", 11:"music", 2:"bootcamp", 10:"defilante", 16:"village"}[self.client.lastGameMode]) + roomName)

            elif command in ["ping"]:
                if self.client.privLevel >= 1:
                    self.client.sendClientMessage("ping ~%s" % str(self.client.PInfo[2]), 1)

            elif command in ["mulodrome"]:
                if (self.client.privLevel >= 9 or self.client.room.roomCreator == self.client.playerName and (not self.client.room.isMulodrome)):
                    for player in self.client.room.clients.copy().values():
                        player.sendPacket(Identifiers.send.Mulodrome_Start, 1 if player.playerName == self.client.playerName else 0)

            elif command in ["time", "temps"]:
                if self.client.privLevel >= 1:
                    self.client.playerTime += abs(Utils.getSecondsDiff(self.client.loginTime))
                    self.client.loginTime = Utils.getTime()
                    temps = map(int, [self.client.playerTime // 86400, self.client.playerTime // 3600 % 24, self.client.playerTime // 60 % 60, self.client.playerTime % 60])
                    self.client.sendLangueMessage("", "$TempsDeJeu", *temps)

            elif command in ["tutorial"]:
                self.client.enterRoom("\x03[Tutorial] %s" %(self.client.playerName))

            elif command in ["facebook"]:
                if self.client.privLevel >= 1:
                    self.client.sendPacket(Identifiers.old.send.Facebook_URL, [""])
                    self.client.shopCheeses += 20

# Tribe Commands:
            elif command in ["inv"]:
                if self.client.privLevel >= 1 and self.requireArguments(1) and self.requireTribePerm(2046):
                    playerName = Utils.parsePlayerName(args[0])
                    if self.server.checkConnectedAccount(playerName) and not playerName in self.client.tribulle.getTribeMembers(self.client.tribeCode):
                        player = self.server.players.get(playerName)
                        player.invitedTribeHouses.append(self.client.tribeName)
                        player.sendPacket(Identifiers.send.Tribe_Invite, ByteArray().writeUTF(self.client.playerName).writeUTF(self.client.tribeName).toByteArray())
                        self.client.sendLangueMessage("", "$InvTribu_InvitationEnvoyee", "<V>"+player.playerName+"</V>")

            elif command in ["invkick"]:
                if self.client.privLevel >= 1 and self.requireArguments(1) and self.requireTribePerm(2046):
                    playerName = Utils.parsePlayerName(args[0])
                    if self.server.checkConnectedAccount(playerName) and not playerName in self.client.tribulle.getTribeMembers(self.client.tribeCode):
                        player = self.server.players.get(playerName)
                        if self.client.tribeName in player.invitedTribeHouses:
                            player.invitedTribeHouses.remove(self.client.tribeName)
                            self.client.sendLangueMessage("", "$InvTribu_AnnulationEnvoyee", "<V>" + player.playerName + "</V>")
                            player.sendLangueMessage("", "$InvTribu_AnnulationRecue", "<V>" + self.client.playerName + "</V>")
                            if player.roomName == "*" + chr(3) + self.client.tribeName:
                                player.enterRoom(self.server.recommendRoom(self.client.langue))

            elif command in ["neige"]:
                if self.client.privLevel >= 1 and self.requireTribePerm(2046):
                    if self.client.room.isSnowing:
                        self.client.room.startSnow(0, 0, not self.client.room.isSnowing)
                        self.client.room.isSnowing = False
                    else:
                        self.client.room.startSnow(1000, 60, not self.client.room.isSnowing)
                        self.client.room.isSnowing = True

            elif command in ["module"]: ###########
                if self.client.privLevel >= 1:
                    if len(args) == 0:
                        self.client.sendClientMessage("Module list:", 1)
                        for key in self.server.officialminigames:
                            self.client.sendMessage(f"<VP>#{key}</VP> : {self.client.room.getPlayersCountbyRoom('#'+key)}")
                    elif self.requireTribePerm(2046) and len(args) == 1:
                        if moduleid[:1] == "stop":
                            if self.client.room.luaRuntime != None:
                                self.client.room.luaRuntime.stopModule()
                        else:
                            module = self.server.minigames.get(moduleid[:1])
                            if module != None:
                                self.client.room.luaRuntime = Lua(self.client.room, self.server)
                                self.client.room.luaRuntime.owner = self.client.playerName
                                self.client.room.luaRuntime.RunCode(module)
            
            elif command in ["sy?"]:
                if(self.client.privLevel in [6, 9] or self.client.isMapCrew == True) or self.requireTribePerm(2046):
                    self.client.sendLangueMessage("", "$SyncEnCours : [%s]" %(self.client.room.currentSyncName))

            elif command in ["sy"]:
                if((self.client.privLevel in [6, 9] or self.client.isMapCrew == True) or self.requireTribePerm(2046)) and self.requireArguments(1):
                    player = self.server.players.get(Utils.parsePlayerName(args[0]))
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
            
            elif command in ["ch"]:
                if (self.client.privLevel in [6, 9] or self.client.requireTribePerm(2046) or self.client.isMapCrew == True or self.client.room.roomName == "*strm_" + self.client.playerName.lower()) and self.requireArguments(1):
                    player = self.server.players.get(Utils.parsePlayerName(args[0]))
                    if player != None:
                        if self.client.room.forceNextShaman == player.playerCode:
                            self.client.sendLangueMessage("", "$PasProchaineChamane", player.playerName)
                            self.client.room.forceNextShaman = -1
                        else:
                            self.client.sendLangueMessage("", "$ProchaineChamane", player.playerName)
                            self.client.room.forceNextShaman = player.playerCode
                    else:
                        self.client.playerException.Invoke("unknownuser")
            
            elif command in ["csr"]:
                if (self.client.privLevel in [6, 9] or self.client.isMapCrew == True) and self.requireTribePerm(2046):
                    ml = []
                    for room in self.server.rooms.values():
                        for playerCode, client in room.clients.items():
                            ml.append(client.playerName)
                    randomplayer = random.choice(ml)
                    player = self.server.players.get(randomplayer)
                    if player != None:
                        player.isSync = True
                        self.client.room.currentSyncCode = player.playerCode
                        self.client.room.currentSyncName = player.playerName
                        self.client.sendLangueMessage("", "$NouveauSync <V> %s" %(player))
            

            elif command in ["playmusic", "musique", "music"]:
                if (self.client.privLevel in [5, 9] or self.client.room.roomName == "*strm_" + self.client.playerName or self.client.isFuncorpPlayer == True) or self.requireTribePerm(2046):
                    self.client.room.sendAll(Identifiers.old.send.Music, []) if len(args) == 0 else self.client.room.sendAll(Identifiers.old.send.Music, [args[0]])

# Lua and Fashion Squad Commands
            elif command in ["lslua"]:
                if self.client.privLevel in [4, 9] or self.client.isLuaCrew == True:
                    LuaCrews = ""
                    for player in self.server.players.copy().values():
                        if player.isLuaCrew or player.privLevel == 4:
                            LuaCrews += "<font color='#79bbac'>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </font><br>"
                    if LuaCrews != "":
                        self.client.sendMessage(LuaCrews.rstrip("\n"))
                    else:
                        self.client.sendClientMessage("Don't have any online Lua Crews at moment.", 1)

            elif command in ["lsfs"]:
                if self.client.privLevel in [3, 9] or self.client.isFashionSquad == True:
                    FS = ""
                    for player in self.server.players.copy().values():
                        if player.isFashionSquad or player.privLevel == 3:
                            FS += "<font color='#ffb6c1'>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </font><br>"
                    if FS != "":
                        self.client.sendMessage(FS.rstrip("\n"))
                    else:
                        self.client.sendClientMessage("Don't have any online Fashion Squads at moment.", 1)

# Funcorp Commands:
            elif command in ["lsfc"]:
                if (self.client.privLevel in [5, 9] or self.client.isFunCorpPlayer == True):
                    FunCorps = ""
                    for player in self.server.players.copy().values(): # if player has role LuaCrew
                        if player.isFunCorpPlayer or player.privLevel == 5:
                            FunCorps += "<FC>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </FC><br>"
                    if FunCorps != "":
                        self.client.sendMessage(FunCorps.rstrip("\n"))
                    else:
                        self.client.sendClientMessage("Don't have any online Fun Corps at moment.", 1)

            elif command in ["funcorp"]:
                if (self.client.privLevel in [5, 9] or self.client.room.roomName == "*strm_" + self.client.playerName or self.client.isFuncorpPlayer == True):
                    if len(args) == 0:
                        if self.client.room.isFuncorp:
                            for player in self.client.room.clients.copy().values():
                                player.sendLangueMessage("", "<FC>$FunCorpDesactive</FC>")
                                self.client.room.isFuncorp = False
                                player.mouseName = ""
                                player.tempMouseColor = ""
                                self.client.room.funcorpNames.clear()
                        else:
                            for player in self.client.room.clients.copy().values():
                                player.sendLangueMessage("", "<FC>$FunCorpActive</FC>")
                                self.client.room.isFuncorp = True
                    else:
                        if args[0] == "help":
                            if self.client.room.roomName == "*strm_" + self.client.playerName and not (self.client.privLevel in [5, 9] or self.client.isFuncorpPlayer):
                                self.client.sendLogMessage(self.FunCorpPlayerCommands()) # strm_
                            else:
                                self.client.sendLogMessage(self.FunCorpMemberCommands()) # FC member
                   
            elif command in ["tropplein"]:
                if (self.client.privLevel in [5, 8, 9] or self.client.isFuncorpPlayer == True):
                    if len(args) == 0:
                        self.client.sendClientMessage("The current maximum number of players is: "+str(self.client.room.maxPlayers), 1)
                    elif self.requireArguments(1):
                        maxPlayers = 0 if int(args[0]) > 200 or int(args[0]) < 1 else int(args[0])
                        self.client.room.maxPlayers = maxPlayers
                        self.client.sendClientMessage("Maximum number of players in the room is set to: <BV>" +str(maxPlayers), 1)

            elif command in ["roomevent"]:
                if (self.client.privLevel in [5, 9] or self.client.isFuncorpPlayer == True):
                    if self.client.room.isFuncorp:
                        self.client.room.isFuncorpRoomName = not self.client.room.isFuncorpRoomName
                        self.client.sendClientMessage('Sucessfull disabled the room color.' if self.client.room.isFuncorpRoomName else 'Sucessfull enabled the room color.', 1)
                    else:
                        self.client.playerException.Invoke("requireFC")

            elif command in ["transformation"]: 
                if(self.client.privLevel in [5, 9] or self.client.room.roomName == "*strm_" + self.client.playerName or self.client.isFuncorpPlayer == True) and self.requireArguments(1, True):
                    if self.client.room.isFuncorp:
                        if len(args) == 2 and args[0] == "*":
                            if args[1] == "off":
                                for player in self.client.room.clients.copy().values():
                                    player.sendPacket(Identifiers.send.Can_Transformation, 0)
                                self.client.sendClientMessage("All the transformations powers have been removed.", 1)
                            else:
                                for player in self.client.room.clients.copy().values():
                                    player.sendPacket(Identifiers.send.Can_Transformation, 1)
                                self.client.sendClientMessage("Transformations powers given to all players in the room.", 1)
                        else:
                            dump = []
                            for arg in args:
                                dump.append(arg)
                            if dump[-1] != "off":
                                for x in dump:
                                    player = self.server.players.get(x)
                                    if player != None:
                                        player.sendPacket(Identifiers.send.Can_Transformation, 1)
                                res = ", ".join(dump)
                                self.client.sendClientMessage("Transformations powers given to players: <BV>"+res+"</BV>", 1)
                            else:
                                for x in dump[:-1]:
                                    player = self.server.players.get(x)
                                    if player != None:
                                        player.sendPacket(Identifiers.send.Can_Transformation, 0)
                                dump.pop()
                                res = ", ".join(dump)
                                self.client.sendClientMessage("Transformations powers removed to players: <BV>"+res+"</BV>", 1)
                    else:
                        self.client.playerException.Invoke("requireFC")

            elif command in ["changesize"]:
                if (self.client.privLevel in [5, 9] or self.client.room.roomName == "*strm_" + self.client.playerName or self.client.isFuncorpPlayer == True) and self.requireArguments(1, True):
                    if self.client.room.isFuncorp:
                        r1 = 0
                        if len(args) == 2 and args[0] == "*":
                            if args[1] == "off":
                                for player in self.client.room.clients.copy().values():
                                    self.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(100).writeBoolean(False).toByteArray())
                                self.client.sendClientMessage("All players now have their regular size.", 1)
                            else:
                                r1 = int(args[1])
                                if r1 >= 999999999: r1 = 100
                                for player in self.client.room.clients.copy().values():
                                    self.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(r1).writeBoolean(False).toByteArray())
                                self.client.sendClientMessage("All players now have the same size: <BV>" + str(r1) + "</BV>.", 1)
                        else:
                            dump = []
                            for arg in args:
                                dump.append(arg)
                            if dump[-1] != "off":
                                r1 = int(args[1])
                                if r1 != 999999999:
                                    for x in dump[:-1]:
                                        player = self.server.players.get(x)
                                        if player != None:
                                            self.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(dump[-1]).writeBoolean(False).toByteArray())
                                res = ", ".join(dump)
                                self.client.sendClientMessage("The following players now have the size "+str(r1)+": <BV>"+res+"</BV>", 1)
                            else:
                                for x in dump[:-1]:
                                    player = self.server.players.get(x)
                                    if player != None:
                                        self.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(100).writeBoolean(False).toByteArray())
                                dump.pop()
                                res = ", ".join(dump)
                                self.client.sendClientMessage("The following players now have their regular size: <BV>"+res+"</BV>", 1)

                    else:
                        self.client.playerException.Invoke("requireFC")

            elif command in ["meep"]:
                if (self.client.privLevel in [5, 9] or self.client.room.roomName == "*strm_" + self.client.playerName or self.client.isFuncorpPlayer == True) and self.requireArguments(1, True):
                    if self.client.room.isFuncorp:
                        if len(args) == 2 and args[0] == "*" and args[1] == "off":
                            for player in self.client.room.clients.copy().values():
                                player.sendPacket(Identifiers.send.Can_Meep, 0)
                            self.client.sendClientMessage("All the meep powers have been removed.", 1)
                            
                        elif len(args) == 1 and args[0] == "*":
                            for player in self.client.room.clients.copy().values():
                                player.sendPacket(Identifiers.send.Can_Meep, 1)
                            self.client.sendClientMessage("Meep powers given to all players in the room.", 1)
                        else:
                            dump = []
                            for arg in args:
                                dump.append(arg)
                            if dump[-1] != "off":
                                for x in dump:
                                    player = self.server.players.get(x)
                                    if player != None:
                                        player.sendPacket(Identifiers.send.Can_Meep, 1)
                                res = ", ".join(dump)
                                self.client.sendClientMessage("Meep powers given to players: <BV>"+res+"</BV>", 1)
                            else:
                                for x in dump[:-1]:
                                    player = self.server.players.get(x)
                                    if player != None:
                                        player.sendPacket(Identifiers.send.Can_Meep, 0)
                                dump.pop()
                                res = ", ".join(dump)
                                self.client.sendClientMessage("Meep powers removed from players: <BV>"+res+"</BV>", 1)
                    else:
                        self.client.playerException.Invoke("requireFC")
      
            elif command in ["changenick"]: 
                if(self.client.privLevel in [5, 9] or self.client.isFuncorpPlayer == True) and self.requireArguments(2):
                    if self.client.room.isFuncorp:
                        playerName = Utils.parsePlayerName(args[0])
                        newName = argsNotSplited.split(" ", 1)[1]
                        player = self.server.players.get(playerName)
                        if player != None:
                            if newName == "off":
                                player.mouseName = ""
                                self.client.room.funcorpNames[player.playerName] = ""
                                self.client.sendClientMessage("The following player has changed his nickname to default: <BV>"+ str(player.playerName) +"</BV>", 1)
                            else:
                                player.mouseName = newName
                                self.client.room.funcorpNames[player.playerName] = newName
                                self.client.sendClientMessage("The following player has changed his nickname: <BV>"+ str(player.playerName) +"</BV>", 1)
                    else:
                        self.client.playerException.Invoke("requireFC")
              
            elif command in ["linkmice"]:
                if (self.client.privLevel in [5, 9] or self.client.room.roomName == "*strm_" + self.client.playerName or self.client.isFuncorpPlayer == True) and self.requireArguments(2, True):
                    if self.client.room.isFuncorp:
                        dump = []
                        for arg in args:
                            dump.append(arg)
                        
                        if dump[-1] == "off":
                            player = self.client.room.clients.get(dump[-2])
                            for x in dump[:-2]:
                                player2 = self.client.room.clients.get(x)
                                if player2 != None:
                                    self.client.room.sendAll(Identifiers.send.Soulmate, ByteArray().writeBoolean(False).writeInt(player.playerCode).writeInt(player2.playerCode).toByteArray())
                        else:
                            player = self.client.room.clients.get(dump[-1])
                            for x in dump[:-1]:
                                player2 = self.client.room.clients.get(x)
                                if player2 != None:
                                    self.client.room.sendAll(Identifiers.send.Soulmate, ByteArray().writeBoolean(True).writeInt(player.playerCode).writeInt(player2.playerCode).toByteArray())
                    else:
                        self.client.playerException.Invoke("requireFC")
              
# MapCrew Commands:
            elif command in ["lsmc"]:
                if self.client.privLevel in [6, 9] or self.client.isMapCrew == True:
                    Mapcrews = ""
                    for player in self.server.players.copy().values():
                        if player.isMapCrew or player.privLevel == 6:
                            Mapcrews += "<BV>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </BV><br>"
                    if Mapcrews != "":
                        self.client.sendMessage(Mapcrews.rstrip("\n"))
                    else:
                        self.client.sendClientMessage("Don't have any online Map Crews at moment.", 1)
                    
            elif command in ["del"]:
                if self.client.privLevel in [6, 9] or self.client.isMapCrew == True:
                    if len(args) == 1:
                        mapCode = args[0]
                        mapCode = mapCode.replace('@', '')
                        if mapCode != -1:
                            self.client.room.CursorMaps.execute("update Maps set Perma = ? where Code = ?", ["44", mapCode])
                            self.client.sendClientMessage("Successfull deleted the map: @"+str(mapCode)+".", 1)
                    elif len(args) == 0:
                        mapCode = self.client.room.mapCode
                        if mapCode != -1:
                            self.client.room.CursorMaps.execute("update Maps set Perma = ? where Code = ?", [44, mapCode])
                            self.client.sendClientMessage("Successfull deleted the map: @"+str(mapCode)+".", 1)
                    else:
                        pass

            elif re.match("p\\d+(\\.\\d+)?", command):
                if self.client.privLevel in [6, 9] or self.client.isMapCrew == True:
                    mapCode = self.client.room.mapCode
                    mapName = self.client.room.mapName
                    currentCategory = self.client.room.mapPerma
                    if mapCode != -1:
                        category = int(command[1:])
                        if category in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 17, 18, 19, 20, 21, 22, 23, 24, 32, 34, 38, 41, 42, 43, 44, 45, 66]:
                            self.client.sendClientMessage("<VP>[%s] (@%s): validate map <J>P%s</J> => <J>P%s</J>" %(self.client.playerName, mapCode, currentCategory, category), 1)
                            self.client.room.CursorMaps.execute("update Maps set Perma = ? where Code = ?", [category, mapCode])

            elif re.match("lsp\\d+(\\.\\d+)?", command):
                if self.client.privLevel in [6, 9] or self.client.isMapCrew == True:
                    category = int(command[3:])
                    if category in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 17, 18, 19, 20, 21, 22, 23, 24, 32, 34, 38, 41, 42, 43, 44, 45, 66]:
                        mapList = ""
                        mapCount = 0
                        self.client.room.CursorMaps.execute("select * from Maps where Perma = ?", [category])
                        for rs in self.client.room.CursorMaps.fetchall():
                            mapCount += 1
                            yesVotes = rs["YesVotes"]
                            noVotes = rs["NoVotes"]
                            totalVotes = yesVotes + noVotes
                            if totalVotes < 1: totalVotes = 1
                            rating = (1.0 * yesVotes / totalVotes) * 100
                            mapList += "\n<N>%s</N> - @%s - %s - %s%s - P%s" %(rs["Name"], rs["Code"], totalVotes, str(rating).split(".")[0], "%", rs["Perma"])
                            
                        self.client.sendLogMessage("<font size=\"12\"><N>Total Maps </N> <BV>%s</BV> <N>with category: </N> <V>p%s %s</V></font>" %(mapCount, category, mapList))

            elif command in ["lsmap"]:
                if self.client.privLevel >= 1:
                    if len(args) == 0:
                        playerName = self.client.playerName
                    elif len(args) == 1 and (self.client.playerName in [6, 9] or self.client.isMapCrew == True):
                        playerName = Utils.parsePlayerName(args[0])
                    mapList = ""
                    mapCount = 0

                    self.client.room.CursorMaps.execute("select * from Maps where Name = ?", [playerName])
                    for rs in self.client.room.CursorMaps.fetchall():
                        mapCount += 1
                        yesVotes = rs["YesVotes"]
                        noVotes = rs["NoVotes"]
                        totalVotes = yesVotes + noVotes
                        if totalVotes < 1: totalVotes = 1
                        rating = (1.0 * yesVotes / totalVotes) * 100
                        mapList += "\n<N>%s</N> - @%s - %s - %s%s - P%s" %(rs["Name"], rs["Code"], totalVotes, str(rating).split(".")[0], "%", rs["Perma"])

                    self.client.sendLogMessage("<font size= \"12\"><V>%s<N>'s maps: <BV>%s %s</font>" %(playerName, mapCount, mapList))

            elif command in ["info"]:
                if self.client.privLevel >= 1:
                    if self.client.room.mapCode != -1:
                        totalVotes = self.client.room.mapYesVotes + self.client.room.mapNoVotes
                        if totalVotes < 1: totalVotes = 1
                        Rating = (1.0 * self.client.room.mapYesVotes / totalVotes) * 100
                        rate = str(Rating).split(".")[0]
                        if rate == "Nan": rate = "0"
                        self.client.sendClientMessage("<BL>"+self.client.room.mapName+" - @"+str(self.client.room.mapCode)+" - "+str(totalVotes)+" - "+rate+"% - P"+str(self.client.room.mapPerma)+".</BL>")

            elif command in ["np", "npp"]: ########
                if (self.client.privLevel >= 5 or self.client.room.roomName == "*strm_" + self.client.playerName.lower() or self.client.isMapCrew == True) or self.client.room.isTribeHouse:
                    if argsCount == 0:
                        self.client.room.mapChange()
                        return

                    if self.client.room.isVotingMode:
                        return

                    code = args[0]
                    if code.startswith("@"):
                        if len(code[1:]) < 1 or not code[1:].isdigit():
                            self.client.sendLangueMessage("", "$CarteIntrouvable")
                            return
                        mapInfo = self.client.room.getMapInfo(int(code[1:]))
                        if mapInfo[0] == None:
                            self.client.sendLangueMessage("", "$CarteIntrouvable")
                            return

                        self.client.room.forceNextMap = code
                        if command == "np":
                            if self.client.room.changeMapTimer != None:
                                try:self.client.room.changeMapTimer.cancel()
                                except:self.client.room.changeMapTimer = None
                            self.client.room.mapChange()
                            return
                        self.client.sendLangueMessage("", f"$ProchaineCarte {code}")
                        return

                    elif code.isdigit():
                        self.client.room.forceNextMap = f"{code}"
                        if command == "np":
                            if self.client.room.changeMapTimer != None:
                                try:self.client.room.changeMapTimer.cancel()
                                except:self.client.room.changeMapTimer = None
                            self.client.room.mapChange()
                            return
                        self.client.sendLangueMessage("", f"$ProchaineCarte {code}")

# Arbitre Commands:           

            elif command in ["lsarb"]:
                if self.client.privLevel >= 7 or self.client.isArbitre:
                    Arbitres = ""
                    for player in self.server.players.copy().values():
                        if player.isArbitre or player.privLevel == 7:
                            Arbitres += "<font color='#B993CA'>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </font><br>"
                    if Arbitres != "":
                        self.client.sendMessage(Arbitres.rstrip("\n"))
                    else:
                        self.client.sendClientMessage("Don't have any online Arbitres at moment.", 1)

            elif command in ["unban", "deban"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
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

            elif command in ["ban"]:
                if self.client.privLevel >= 1 or self.client.room.roomName == "*strm_" + self.client.playerName.lower() and self.requireArguments(1, True):
                    playerName = Utils.parsePlayerName(args[0])
                    if self.client.room.roomName == "*strm_" + self.client.playerName: # STRM support
                        player = self.server.players.get(playerName)
                        if player != None and player.roomName == self.client.roomName:
                            player.enterRoom('1')
                    elif len(args) == 1: # Vote Populaire Support
                        self.server.voteBanPopulaire(playerName, self.client.playerName, self.client.ipAddress)
                    else:
                        if self.client.privLevel >= 7:
                            result = self.server.checkBanUser(playerName)
                            if result == -1:
                                hours = int(args[1])
                                reason = argsNotSplited.split(" ", 2)[2]
                                if self.server.checkConnectedAccount(playerName):
                                    self.client.sendClientMessage(f"The player {playerName} got banned for {hours}h ({reason})", 1)
                                    self.client.sendServerMessageOthers(f"{self.client.playerName} banned the player {playerName} for {hours}h ({reason}).")
                                    self.server.banPlayer(playerName, hours, reason, self.client.playerName, False)
                                else:
                                    self.client.sendClientMessage(f"The player {playerName} got banned for {hours}h ({reason})", 1)
                                    self.client.sendServerMessageOthers(f"{self.client.playerName} offline banned the player {playerName} for {hours}h ({reason}).")
                                    self.server.banPlayer(playerName, hours, reason, self.client.playerName, False)
                            elif result == 1:
                                self.client.playerException.Invoke("useralreadybanned", playerName)
                            else:
                                self.client.playerException.Invoke("unknownuser")

            elif command in ["iban"]:
                if self.client.privLevel >= 7 and self.requireArguments(3, True):
                    playerName = Utils.parsePlayerName(args[0])
                    result = self.server.checkBanUser(playerName)
                    if result == -1:
                        hours = int(args[1])
                        reason = argsNotSplited.split(" ", 2)[2]
                        if self.server.checkConnectedAccount(playerName):
                            self.client.sendClientMessage(f"The player {playerName} got banned for {hours}h ({reason})", 1)
                            self.client.sendServerMessageOthers(f"{self.client.playerName} banned the player {playerName} for {hours}h ({reason}).")
                            self.server.banPlayer(playerName, hours, reason, self.client.playerName, True)
                        else:
                            self.client.sendClientMessage(f"The player {playerName} got banned for {hours}h ({reason})", 1)
                            self.client.sendServerMessageOthers(f"{self.client.playerName} offline banned the player {playerName} for {hours}h ({reason}).")
                            self.server.banPlayer(playerName, hours, reason, self.client.playerName, True)
                    elif result == 1:
                        self.client.playerException.Invoke("useralreadybanned", playerName)
                    else:
                        self.client.playerException.Invoke("unknownuser")

            elif command in ["chatlog"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    self.client.modoPwet.openChatLog(Utils.parsePlayerName(args[0]))

            elif command in ["banhack"]: ################
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    player = self.server.players.get(playerName)
                    if player != None:
                        hours = 360
                        reason = "Hack. Your account will be permanently banned if you continue to violate the rules!"
                        player.sendPlayerBan(hours, reason)
                        self.server.banPlayer(player.playerName, hours, reason, self.client.playerName, False)
                        self.client.sendServerMessageOthers("%s banned the player %s for %sh (%s)" %(self.client.playerName, playerName, hours, reason))
                    else:
                        self.client.playerException.Invoke("unknownuser")
                   
            elif command in ["ibanhack"]: ##############
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    player = self.server.players.get(playerName)
                    if player != None:
                        hours = 360
                        reason = "Hack. Your account will be permanently banned if you continue to violate the rules!"
                        player.sendPacket(Identifiers.old.send.Player_Ban, [3600000 * hours, reason])
                        self.server.banPlayer(player.playerName, hours, reason, self.client.playerName, True)
                        self.client.sendServerMessageOthers("%s banned the player %s for %sh (%s)" %(self.client.playerName, playerName, hours, reason))
                    else:
                        self.client.playerException.Invoke("unknownuser")
                   
            elif command in ["mute", "imute"]:
                if self.client.privLevel >= 7 and self.requireArguments(3, True):
                    playerName = Utils.parsePlayerName(args[0])
                    if self.server.checkExistingUser(playerName):
                        if self.server.checkTempMute(playerName):
                            self.client.playerException.Invoke("useralreadymuted", playerName)
                        else:
                            time = args[1] if (len(args) >= 2) else ""
                            reason = argsNotSplited.split(" ", 2)[2] if (len(args) >= 3) else ""
                            hours = int(time) if (time.isdigit()) else 1
                            hours = 9999999 if (hours > 9999999) else hours
                            self.server.mutePlayer(playerName, hours, reason, self.client.playerName, True, bool(command == "imute"))
                            self.client.sendClientMessage(f"The player {playerName} got muted", 1)
                    else:
                        self.client.playerException.Invoke("unknownuser")

            elif command in ["unmute", "demute"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
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
                            self.client.playerException.Invoke("usernotmuted")
                    else:
                        self.client.playerException.Invoke("unknownuser")

            elif command in ["l"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    if "." not in args[0]:
                        self.Cursor.execute("select DISTINCT(IP), Time, IPColor, Country, Community, ConnectionID from LoginLogs where Username = %s order by Time desc limit 0, 200", [args[0]])
                        r = self.Cursor.fetchall()
                        if r == None:
                            self.client.playerException.Invoke("notloggedin", args[0])
                        else:
                            message = "<p align='center'>Connection logs for player: <BL>"+args[0]+"</BL>\n</p>"
                            for rs in r:
                                message += f"<p align='left'><V>[ {args[0]} ]</V> <BL>{rs[1]}</BL><G> ( <font color = '{rs[2]}'>{rs[0]}</font> - {rs[3]} ) {rs[5]} - {rs[4]}</G><br>"
                            self.client.sendLogMessage(message)
                    else:
                        self.Cursor.execute("select DISTINCT(Username), Time, IPColor, Country, Community, ConnectionID from LoginLogs where IP = %s order by Time desc limit 0, 200", [args[0]])
                        r = self.Cursor.fetchall()
                        if r == None:
                            pass
                        else:
                            message = "<p align='center'>Connection logs for IP Address: <V>"+args[0].upper()+"</V>\n</p>"
                            for rs in r:
                                message += f"<p align='left'><V>[ {rs[0]} ]</V> <BL>{rs[1]}</BL><G> ( <font color = '{rs[2]}'>{args[0].upper()}</font> - {rs[3]} ) {rs[5]} - {rs[4]}</BL><br>"
                            self.client.sendLogMessage(message)
            
            elif command in ["roomkick"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    player = self.server.players.get(Utils.parsePlayerName(args[0]))
                    if player != None:
                        self.client.sendServerMessageOthers(f" {player.playerName} has been roomkicked from [{str.lower(player.room.name)}] by {self.client.playerName}.")
                        self.client.sendClientMessage(f"{player.playerName} got kicked from the room.", 1)
                        player.startBulle(self.server.recommendRoom(player.langue))
                    else:
                        self.client.playerException.Invoke("unknownuser")
                        
            elif command in ["follow", "join"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    player = self.server.players.get(Utils.parsePlayerName(args[0]))
                    if player != None:
                        self.client.enterRoom(player.roomName)
                    else:
                        self.client.playerException.Invoke("unknownuser")

            elif command in ["ninja"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    player = self.server.players.get(Utils.parsePlayerName(args[0]))
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
                    
            elif command in ["ip"]:
                if self.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    player = self.server.players.get(playerName)
                    if player != None:
                        self.client.sendClientMessage(f"<BV>{playerName}</BV> -> {Utils.EncodeIP(player.ipAddress)} ({player.ipCountry})", 1)
                    else:
                        self.client.playerException.Invoke("unknownuser")
            
            elif command in ["kick"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    player = self.server.players.get(playerName)
                    if player != None:
                        player.room.removeClient(player)
                        player.transport.close()
                        self.client.sendServerMessageOthers("The player {playerName} has been kicked by {self.client.playerName}.")
                        self.client.sendClientMessage(f"The player {playerName} got kicked", 1)
                    else:
                        self.client.playerException.Invoke("unknownuser")

            elif command in ["room*", "salon*", "sala*", "commu"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    community = args[0][0:2].upper()
                    try:
                        self.client.langue = community
                        self.client.langueID = Langues.getLangues().index(community)
                        self.client.enterRoom(args[0] if command != "commu" else self.server.recommendRoom(community))
                    except:
                        self.client.sendClientMessage(f"The community {community} is invalid.", 1)

            elif command in ["clearban"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    if self.server.checkExistingUser(playerName) or self.server.checkConnectedAccount(playerName):
                        player = self.server.players.get(playerName)
                        if player != None:
                            player.voteBan = []
                            self.client.sendServerMessageOthers(f"{self.client.playerName} removed all ban votes of {playerName}.")
                            self.client.sendClientMessage(f"Successfully removed all ban votes of {playerName}", 1)
                        else:
                             self.client.playerException.Invoke("unknownuser")

            elif command in ["chatfilter"]:
                if self.client.privLevel >= 7:
                    try:
                        if args[0] == "list" and self.requireArguments(1):
                            msg = " "*60 + "Filter List (" + self.server.miceName + ")"
                            msg += "\n<V>"
                            for message in self.server.serverList:
                                msg += message + "\n"
                            self.client.sendLogMessage(msg)
                        elif args[0] == "del" and self.requireArguments(2, True):
                            name = args[1].replace("http://www.", "").replace("https://www.", "").replace("http://", "").replace("https://", "").replace("www.", "")
                            if not name in self.server.serverList:
                                self.client.sendClientMessage(f"The string <N>[{name}]</N> is not in the filter.", 1)
                            else:
                                self.server.serverList.remove(name)
                                self.client.sendClientMessage(f"The string <N>[{name}]</N> has been removed from the filter.", 1)
                        elif self.requireArguments(1, True):
                            name = args[0].replace("http://www.", "").replace("https://www.", "").replace("http://", "").replace("https://", "").replace("www.", "")
                            if name in self.server.serverList:
                                self.client.sendClientMessage(f"The string <N>[{name}]</N> is already on the filter.", 1)
                            else:
                                self.server.serverList.append(name)
                                self.client.sendClientMessage(f"The string <N>[{name}]</N> has been added to the filter.", 1)
                    except:
                        self.client.playerException.Invoke("moreargs")

            elif command in ["mumute"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    if self.server.checkConnectedAccount(playerName):
                        self.server.sendMumute(playerName, self.client.playerName)
                        self.client.sendClientMessage(""+ playerName + " got mumuted.", 1)

            elif command in ["lsc"]:
                if self.client.privLevel >= 7:
                    result = {}
                    for room in self.server.rooms.values():
                        if room.community in result:
                            result[room.community] = result[room.community] + room.getSourisCount()
                        else:
                            result[room.community] = room.getSourisCount()
                    message = ""
                    for community in result.items():
                        if community[1] > 0:
                            message += "<BL>%s:<BL> <V>%s</V>\n" %(community[0].upper(), community[1])
                    message += "<J>Total players:</J> <R>%s</R>" %(sum(result.values()))
                    self.client.sendLogMessage(message)

            elif command in ["find", "chercher", "search"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    Text = args[0]
                    result = ""
                    for player in self.server.players.copy().values():
                        if player.playerName.startswith(Text):
                            result += "<BV>%s</BV> -> %s\n" %(player.playerName, player.room.name)
                    result = result.rstrip("\n")
                    self.client.sendClientMessage(result, 1) if result != "" else self.client.sendClientMessage("No results were found.", 1)

            elif command in ["nomip"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    player = self.server.players.get(playerName)
                    if player != None:
                        ipList=playerName+"'s last known IP addresses:"
                        self.Cursor.execute("select distinct IP from LoginLogs where Username = %s", [playerName])
                        for rs in self.Cursor.fetchall():
                            ipList += "<br>" + rs[0]
                        self.client.sendClientMessage(ipList, 1)
                    else:
                        self.client.playerException.Invoke("unknownuser")

            elif command in ["ipnom"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    ip = args[0]
                    List = "Logs for the IP address ["+ip+"]:"
                    self.Cursor.execute("select distinct Username from LoginLogs where IP = %s", [ip])
                    r = self.Cursor.fetchall()
                    for rs in r:
                        if self.server.checkConnectedAccount(rs[0]):
                            List += "<br>" + rs[0] + " <G>(online)</G>"
                        else:
                            List += "<br>" + rs[0]
                    self.client.sendClientMessage(List, 1)

            elif command in ["delrecord"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    mapCode = args[0]
                    if self.server.checkRecordMap(mapCode):
                        self.client.room.CursorMaps.execute("update Maps set Time = ? and Player = ? and RecDate = ? where Code = ?", [0, "", 0, str(mapCode)])
                        self.client.sendServerMessage("The map's record: @"+str(mapCode)+" was removed by <BV>"+str(self.client.playerName)+"</BV>.")
                    else:
                        self.client.sendClientMessage("The map isn't have a record.")

            elif command in ["prison"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    player = self.server.players.get(playerName)
                    if player != None:
                        if player.isPrisoned:
                            player.isPrisoned = False
                            self.client.sendServerMessageOthers(f"{player.playerName} unprisoned by {self.client.playerName}.")
                            self.client.sendClientMessage(f"{player.playerName} got unprisoned.", 1)
                            player.enterRoom("1")
                        else:
                            player.enterRoom("*Bad Girls")
                            player.isPrisoned = True
                            self.client.sendServerMessageOthers(f"{player.playerName} prisoned by {self.client.playerName}.")
                            self.client.sendClientMessage(f"{player.playerName} got prisoned.", 1)
                    else:
                        self.client.playerException.Invoke("unknownuser")

            elif command in ["casier"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    player = self.server.players.get(Utils.parsePlayerName(args[0]))
                    if player != None:
                        try:
                            message = "<p align='center'><N>Sanction Logs for <V>"+player.playerName+"</V></N>\n</p><p align='left'>Currently running sanctions: </p><br>"
                            self.Cursor.execute("select * from casierlog where Name = %s order by Timestamp desc limit 0, 200", [player.playerName])
                            for rs in self.Cursor.fetchall():
                                name,ip,state,timestamp,modName,time,reason = rs[0],rs[1],rs[2],rs[3],rs[4],rs[5],rs[6]
                                fromtime = str(datetime.fromtimestamp(float(int(timestamp))))
                                ip = Utils.EncodeIP(player.ipAddress)
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
                            self.client.sendLogMessage(message)
                        except:
                            self.client.sendClientMessage("There has been an error when retrieving the list of sanctions of the player "+player.playerName+" : PARAMETRE_INVALIDE.", 1)
                    else:
                        self.client.playerException.Invoke("unknownuser")

            elif command in ["closeroom"]:
                if self.client.privLevel >= 7:
                    if len(args) == 0:
                        roomName = self.client.room.name
                        for player in [*self.client.room.clients.copy().values()]:
                            player.enterRoom('1')
                        self.client.sendServerMessageOthers(str(self.client.playerName)+" closed the room ["+roomName+"].")
                        self.client.sendClientMessage(f"The room {roomName} got closed.", 1)
                    elif len(args) == 1:
                        roomName = argsNotSplited.split(" ", 0)[0]
                        try:
                            for client in [*self.server.rooms[roomName].clients.values()]:
                                client.enterRoom('1')
                            self.client.sendServerMessageOthers(str(self.client.playerName)+" closed the room ["+roomName+"].")
                            self.client.sendClientMessage(f"The room {roomName} got closed.", 1)
                        except KeyError:
                            self.client.sendClientMessage("The room [<J>"+roomName+"</J>] doesn't exists.", 1)
                    else:
                        pass
                                    
            elif command in ["lsroom"]:
                if self.client.privLevel >= 7:
                    if len(args) == 0:
                        Message = "Players in room ["+str(self.client.roomName[:2].lower() + self.client.roomName[2:])+"]: "+str(self.client.room.getPlayerCount())+"\n"
                        for player in [*self.client.room.clients.copy().values()]:
                            if not player.isHidden:
                                Message += "<BL>%s / </BL><font color = '%s'>%s</font> <G>(%s)</G>\n" % (player.playerName, player.ipColor, Utils.EncodeIP(player.ipAddress), player.ipCountry)
                            else:
                                Message += "<BL>%s / </BL><font color = '%s'>%s</font> <G>(%s)</G> <BL>(invisible)</BL>\n" % (player.playerName, player.ipColor, Utils.EncodeIP(player.ipAddress), player.ipCountry)
                        Message = Message.rstrip("\n")
                        self.client.sendClientMessage(Message, 1)
                    elif len(args) == 1:
                        roomName = argsNotSplited.split(" ", 0)[0]
                        try:
                            players = 0
                            for player in [*self.server.rooms[roomName].clients.values()]:
                                players = players + 1
                            Message = "<V>[•]</V> Players in room ["+roomName+"]: "+str(players)+"\n"
                            for player in [*self.server.rooms[roomName].clients.values()]:
                                if not player.isHidden:
                                    Message += "<BL>%s / </BL><font color = '%s'>%s</font> <G>(%s)</G>\n" % (player.playerName, player.ipColor, Utils.EncodeIP(player.ipAddress), player.ipCountry)
                                else:
                                    Message += "<BL>%s / </BL><font color = '%s'>%s</font> <G>(%s)</G> <BL>(invisible)</BL>\n" % (player.playerName, player.ipColor, Utils.EncodeIP(player.ipAddress), player.ipCountry)
                            Message = Message.rstrip("\n")
                            self.client.sendClientMessage(Message, 1)
                        except KeyError:
                            self.client.sendClientMessage("The room [<J>"+roomName+"</J>] doesn't exists.", 1)
                    else:
                        pass
                            
            elif command in ["unbanip", "debanip"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    ip = args[0]
                    decip = Utils.DecodeIP(ip)
                    if decip in self.server.IPPermaBanCache:
                        self.server.IPPermaBanCache.remove(decip)
                        self.Cursor.execute("delete from IPPermaBan where IP = %s", [decip])
                        self.client.sendServerMessageOthers(f"{self.client.playerName} unbanned the ip address {ip}.")
                        self.client.sendClientMessage(f"The ip address {ip} got unbanned.", 1)
                    else:
                        self.client.sendClientMessage("The IP isn't banned.", 1)
                            
            elif command in ["ls"]:
                if self.client.privLevel >= 7:
                    if len(args) >= 1:
                        roomNAME = argsNotSplited.split(" ", 0)[0] if (len(args) >= 1) else ""
                        totalusers = 0
                        users, rooms, message = 0, [], ""
                        for room in self.server.rooms.values():
                            if room.name.find(roomNAME) != -1 or room.name.startswith(roomNAME):
                                rooms.append([room.name, room.community, room.getPlayerCount(), "bulle0"])
                                
                        message += "<N>List of rooms matching [%s]:</N>" % (roomNAME)
                        for roomInfo in rooms:
                            message += "\n"
                            message += "<BL>%s <G>(%s / %s)</G> : <V>%s</V>" % (str.lower(roomInfo[0]), str.lower(roomInfo[1]), roomInfo[3], roomInfo[2])
                            totalusers = totalusers + roomInfo[2]
                        message += "\n<J>Total players:</J> <R>%s</R>" % (totalusers)
                        self.client.sendLogMessage(message)
                    else:
                        data = []
                        for room in self.server.rooms.values():
                            if room.name.startswith("*") and not room.name.startswith("*" + chr(3)):
                                data.append(["xx", room.name, room.getPlayerCount(), "bulle0"])
                            elif room.name.startswith(str(chr(3))) or room.name.startswith("*" + chr(3)):
                                if room.name.startswith(("*" + chr(3))):
                                    data.append(["xx", room.name, room.getPlayerCount(), "bulle0"])
                                else:
                                    data.append(["*", room.name, room.getPlayerCount(), "bulle0"])
                            else:
                                data.append([room.community, room.roomName, room.getPlayerCount(), "bulle0"])
                        result = "<N>List of rooms:</N>"
                        for roomInfo in data:
                            if roomInfo[3] == "maison":
                                result += "\n<BL>%s</BL> <G>(%s / %s) :</G> <V>%s</V>" % (roomInfo[1] ,str.lower(roomInfo[0]), roomInfo[3], roomInfo[2])
                            else:
                                result += "\n<BL>%s-%s</BL> <G>(%s / %s) :</G> <V>%s</V>" % (str.lower(roomInfo[0]), roomInfo[1] ,str.lower(roomInfo[0]), roomInfo[3], roomInfo[2])
                        result += "\n<J>Total players:</J> <R>%s</R>" %(len(self.server.players))
                        self.client.sendLogMessage(result)

            elif command in ["relation"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    player = self.server.players.get(Utils.parsePlayerName(args[0]))
                    if player != None:
                        r1 = []
                        displayed = []
                        List = "The player <BV>"+str(player.playerName)+"</BV> has the following relations:"
                        self.Cursor.execute("select distinct Username from LoginLogs where IP = %s", [Utils.EncodeIP(player.ipAddress)])
                        ip2 = f"<font color='{player.ipColor}'>{Utils.EncodeIP(player.ipAddress)}</font>"
                        for rs in self.Cursor.fetchall():
                            if rs[0] in displayed: continue
                            if self.server.players.get(str(rs[0])) == None:
                                d = self.Cursor.execute("select distinct IP from LoginLogs where Username = %s", [str(rs[0])])
                                d = self.Cursor.fetchall()
                                ips = []
                                ips2 = []
                                for i in d:
                                    if i[0] in ips2: continue
                                    ips.append(f"<font color='{Utils.DecodeIP(i[0])}'>{i[0]}</font>")
                                    ips2.append(i[0])
                                toshow = ", ".join(ips)
                                List += f"<br>- <BV>{rs[0]}</BV> : {toshow}"
                            else:
                                ip31 = self.server.players.get(str(rs[0]))
                                List += f"<br>- <BV>{rs[0]}</BV> : <font color='{ip31.ipColor}'>{Utils.EncodeIP(ip31.ipAddress)}</font> (current IP)"
                            displayed.append(rs[0])
                        self.client.sendClientMessage(List, 1)
                    else:
                        self.client.playerException.Invoke("unknownuser")
                   
            elif command in ["infotribu"]: #########
                if self.client.privLevel >= 7:
                    if len(args) >= 1:
                        name = args[0]
                        message = "<p align='center'>Tribe: <J>%s</J><BR>" % name
                        self.Cursor.execute("select Code, Message, House, Ranks, Historique, Members from tribe where Name = %s", [name])
                        r = self.Cursor.fetchall()
                        try:
                            r1 = iter(r)
                            r2 = next(r1)
                            totalmembers = len(self.client.tribulle.getTribeMembers(r2[0]))
                            message += "<p align='left'><N>Id:</N> : <R>%s</R><BR><N>Tribehouse map : @%s</N><BR><BR><N>Members: %s</N><BR>" % (str(r2[0]), str(r2[2]), totalmembers)
                            for playerName in self.client.tribulle.getTribeMembers(r2[0]):
                                tribeRank = self.client.tribulle.getPlayerTribeRank(playerName)
                                pl1 = self.server.players.get(playerName)
                                if pl1 != None:
                                    message += "<N>-<N> <V>"+str(playerName)+"</V> : <BL>"+str(tribeRank)+"</BL> <N>(</N><font color = '"+str(pl1.ipColor)+"'>"+str(Utils.EncodeIP(pl1.ipAddress))+"</font><N> / "+str(pl1.roomName)+")</N>\n"
                                else:
                                    message += "<N>-<N> <V>"+str(playerName)+"</V> : <BL>"+str(tribeRank)+"</BL>\n"
                            ranks = str(r2[3])
                            ranks = ranks.replace("|", "<BR><N>-</N> ")
                            #ranks = ranks.split("|")[2].split(",")
                            message += "<BR><N>Ranks:</N><BR> <N>-</N> <V>"+ranks+"</V>\n"
                            self.client.sendLogMessage(message)
                        except:
                            self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid tribe name.")
                    elif len(args) == 0:
                        self.client.sendMessage("<V>[•]</V> You need more arguments to use this command.")
                    else:
                        pass

            elif command in ["infocommu"]:  ########
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    commu = args[0]
                    if commu in self.server.langs:
                        self.client.sendClientMessage(f"Total Players in Community</J> <BV>{commu}</BV>: <R>{self.server.getTotalPlayersInCommunity(commu)}</R>", 1)
                    else:
                        self.client.sendClientMessage(f"The community <J>{commu}</J> is invalid.", 1)

            elif command in ["creator"]:
                if self.client.privLevel >= 7:
                    self.client.sendClientMessage("Room [<J>"+self.client.room.name+"</J>]'s creator: <BV>"+self.client.room.roomCreator+"</BV>", 1)

# Moderator Commands

            elif command in ["lsmodo"]:
                if self.client.privLevel in [7, 8, 9]:
                    Moderateurs = ""
                    for player in self.server.players.copy().values():
                        if player.privLevel == 8:
                            Moderateurs += "<font color='#C565FE'>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </font><br>"
                    if Moderateurs != "":
                        self.client.sendMessage(Moderateurs.rstrip("\n"))
                    else:
                        self.client.sendClientMessage("<V>[•]</V> Don't have any online Moderators at moment.", 1)

            elif command in ["mm"]:
                if self.client.privLevel >= 8:
                    self.client.room.sendAll(Identifiers.send.Staff_Chat, ByteArray().writeByte(0).writeUTF("").writeUTF(argsNotSplited).writeShort(0).writeByte(0).toByteArray())
            
            elif command in ["clearchat"]:
                if self.client.privLevel >= 8:
                    self.client.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("\n" * 10000).toByteArray())

            elif command in ["moveplayer"]:
                if self.client.privLevel >= 8 and self.requireArguments(2):
                    playerName = Utils.parsePlayerName(args[0])
                    roomName = argsNotSplited.split(" ", 1)[1]
                    player = self.server.players.get(playerName)
                    if player != None:
                        newRoom = player.room.name
                        player.enterRoom(roomName)
                        self.client.sendServerMessageOthers(f"{player.playerName} has been moved from ({str.lower(newRoom)}) to ({str.lower(player.room.name)})  by {self.client.playerName}.")
                        self.client.sendClientMessage(f"{player.playerName} has been moved from {str.lower(newRoom)} to {str.lower(player.room.name)} ", 1)
                    else:
                        self.client.playerException.Invoke("unknownuser")

            elif command in ["removeplayerrecords"]:
                if self.client.privLevel >= 8 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
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
                        self.client.room.CursorMaps.execute("update Maps set Time = ?, Player = ?, RecDate = ? where Player = ?", [0, "", 0, playerName])
                        self.client.sendServerMessageOthers(f"The records of {playerName} were removed by {self.client.playerName}.")
                        self.client.sendClientMessage(f"{playerName}'s records got removed.", 1)
                    else:
                        self.client.playerException.Invoke("norecordsfound")

            elif command in ["arb"]:
                if self.client.privLevel >= 8 and self.requireArguments(1):
                    player = self.server.players.get(Utils.parsePlayerName(args[0]))
                    if player != None and not player.isGuest:
                        if player.privLevel == 7:
                            self.Cursor.execute("UPDATE users SET PrivLevel = 1 WHERE Username = '%s' " % (player.playerName))
                            player.privLevel = 1
                            self.client.sendClientMessage(player.playerName+" is not arbitre / moderator anymore.", 1)
                            player.room.removeClient(player)
                            player.transport.close()
                            
                        else:
                            self.Cursor.execute("UPDATE users SET PrivLevel = 7 WHERE Username = '%s' " % (player.playerName))
                            player.privLevel = 7
                            self.client.sendClientMessage("New arbitre : "+player.playerName, 1)
                            player.room.removeClient(player)
                            player.transport.close()

            #elif command in ["max"]:
                #if self.client.privLevel >= 8:
                    #self.client.sendClientMessage("Maximum Players: <VP>"+str(self.server.MaximumPlayers)+"</VP>.", 1)

            elif command in ["log"]:
                if self.client.privLevel >= 8:
                    logList = []
                    self.Cursor.execute("select * from casierlog order by Time desc limit 0, 200")
                    r = self.Cursor.fetchall()
                    for rs in r:
                        if rs[2] in ["UNBAN", "BAN"]:
                            if rs[2] == "UNBAN":
                                logList += rs[0], "", rs[6], "", "", rs[3].rjust(13, "0")
                            else:
                                logList += rs[0], rs[1], rs[6], rs[5], rs[4], rs[3].rjust(13, "0")
                    self.client.sendPacket(Identifiers.old.send.Log, logList)

# Admins Commands

            elif command in ["move"]:
                if self.client.privLevel >= 9:
                    for player in [*self.client.room.clients.copy().values()]:
                        player.enterRoom(argsNotSplited)

            elif command in ["updatesql"]:
                if self.client.privLevel >= 9:
                    self.server.updateServer()
                    self.client.sendServerMessageAdminOthers(f"The database was updated by {self.client.playerName}.")
                    self.client.sendClientMessage("The database got updated.", 1)

            elif command in ["smc"]:
                if self.client.privLevel >= 9:
                    for player in self.server.players.copy().values():
                        player.sendMessage(f"<font color = '#12DA8A'>• [{self.client.playerName}] {argsNotSplited}</font>")

            elif command in ["re","respawn"]:
                if self.client.privLevel >= 9:
                    playerName = Utils.parsePlayerName(args[0])
                    if playerName in self.client.room.clients:
                        self.client.room.respawnSpecific(playerName)
                        self.client.sendClientMessage(f"Successfull respawned {playerName}.", 1)

            elif command in ["settime"]:
                if self.client.privLevel >= 9 and self.requireArguments(1):
                    time = int(args[0])
                    time = 5 if time < 1 else (32767 if time > 32767 else time)
                    for player in self.client.room.clients.copy().values():
                        player.sendRoundTime(time)
                    self.client.room.changeMapTimers(time)
                    self.client.sendClientMessage(f"Successfull added {time} seconds to current round.", 1)

            elif command in ["commandlog"]:
                if self.client.privLevel >= 9:
                    playerName = Utils.parsePlayerName(args[0])
                    self.Cursor.execute("select Username, Time, Command from Commandlog where Username = %s", [playerName])
                    r = self.Cursor.fetchall()
                    message = "<p align='center'>Command Log of (<V>"+playerName+"</V>)\n</p>"
                    for rs in r:
                        nick = rs[0]
                        date = rs[1]
                        command = rs[2]
                        d = str(datetime.fromtimestamp(float(int(date))))
                        message += "<p align='left'><V>[%s]</V> <FC> - </FC><VP>use command:</VP> <V>/%s</V> <FC> ~> </FC><VP>[%s]\n" % (nick,command,d)
                    self.client.sendLogMessage(message)
                else:
                    self.Cursor.execute("select Username, Time, Command from Commandlog") 
                    r = self.Cursor.fetchall()
                    message = "<p align='center'>Command Log of Server\n</p>"
                    for rs in r:
                        nick = rs[0]
                        date = rs[1]
                        command = rs[2]
                        d = str(datetime.fromtimestamp(float(int(date))))
                        message += "<p align='left'><V>[%s]</V> <FC> - </FC><VP>use command:</VP> <V>/%s</V> <FC> ~> </FC><VP>[%s]\n" % (nick,command,d)
                    self.client.sendLogMessage(message)

            elif command in ["resetprofile"]: #########
                if self.client.privLevel >= 9 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    player = self.server.players.get(playerName)
                    if player != None:
                        self.Cursor.execute(f"UPDATE Users SET FirstCount = 0, CheeseCount = 0, ShamanSaves = 0, HardModeSaves = 0, DivineModeSaves = 0, BootcampCount = 0, ShamanCheeses = 0, Badges = 0, ShamanLevel = 0, ShamanExp = 0, Consumables = '', Pet = '', ShamanBadges = '', Badges = '{'{}'}', Karma = 0, ShopCheeses = 0, ShopFraises = 0  WHERE PlayerID = {self.server.getPlayerID(player.playerName)}")
                        self.client.sendServerMessageAdminOthers(f"The account {playerName} was reset by {self.client.playerName}")
                        self.client.sendClientMessage(f"The account {playerName} got reset.", 1)
                        player.room.removeClient(player)
                        player.transport.close()
                    else:
                        self.client.playerException.Invoke("unknownuser")

            elif command in ["harddel"]:
                if self.client.privLevel >= 9:
                    mapCode = args[0] if len(args) else self.client.room.mapCode
                    mapCode = mapCode.replace('@', '')
                    if mapCode != -1:
                        self.client.room.CursorMaps.execute("delete from Maps where Code = ?", [mapCode])
                        self.client.sendClientMessage(f"Successfull deleted the map: @{mapCode} from database.", 1)

            elif command in ["addcode"]:
                if self.client.privLevel >= 9 and self.requireArguments(3):
                    data = json.loads(open('./include/json/codes.json','r').read())
                    name = args[0]
                    T = args[1]
                    amount = int(args[2])
                    if T == "fraises" or T == "cheeses":
                        data['codes'].append({'name': str(name), 'type': str(T), 'amount': amount, 'havegot': 0})
                        with open('./include/json/codes.json', 'w') as F:
                            json.dump(data, F)
                    else:
                        self.client.sendClientMessage("The type of code is invalid.", 1)


# Owner Commands:
            elif command in ["luaadmin"]:
                if self.client.playerName in self.owners:
                    self.client.isLuaAdmin = not self.client.isLuaAdmin
                    self.client.sendClientMessage("You can run lua programming as administrator." if self.client.isLuaAdmin else "You can't run lua programming as administrator.", 1)

            elif command in ["serverconfigs"]:
                if self.client.playerName in self.owners:
                    with open("./include/configs.properties", 'r') as File:
                        Log = File.read()
                        File.close()
                    self.client.sendLogMessage(Log.replace("<", "&amp;lt;").replace("\x0D\x0A", "\x0A"))

            elif command in ["reboot"]:
                if self.client.playerName in self.owners:
                    self.server.sendServerRestart()
                    
            elif command in ["clearlogs"]:
                if self.client.playerName in self.owners and self.requireArguments(1):
                    if args[0] == "reports":
                        self.server.reports = {}
                        self.client.sendServerMessageAdmin("The player %s cleared all reports from modopwet." %(self.client.playerName))
                    elif args[0] == "ippermacache":
                        self.server.IPPermaBanCache = []
                        self.client.sendServerMessageAdmin("The player %s clear the cache of the server." %(self.client.playerName))
                    elif args[0] == "iptempcache":
                        self.server.IPTempBanCache = []
                        self.client.sendServerMessageAdmin("The player %s cleared all IP bans." %(self.client.playerName))
                    elif args[0] == "banlog":
                        self.Cursor.execute("DELETE FROM casierlog")
                        self.Cursor.execute("DELETE FROM ippermaban")
                        self.Cursor.execute("DELETE FROM usertempban")
                        self.client.sendServerMessageAdmin("The player %s cleared casier database." %(self.client.playerName))
                    elif args[0] == "loginlog":
                        self.Cursor.execute("DELETE FROM loginlog")
                        self.Cursor.execute("DELETE FROM loginlogs")
                        self.client.sendServerMessageAdmin("The player %s cleared loginlog database." %(self.client.playerName))
                    elif args[0] == "commandlog":
                        self.Cursor.execute("DELETE FROM commandlog")
                        self.client.sendServerMessageAdmin("The player %s cleared commandlog database." %(self.client.playerName))

            elif command in ["viewlog"]:
                if self.client.playerName in self.owners and self.requireArguments(1):
                    if args[0] == "errors":
                        errors = ["Tribulle.log", "Commands.log", "Server.log"]
                        for error in errors:
                            with open(f"./include/logs/Errors/{error}", 'r') as File:
                                Log = File.read()
                                File.close()
                            self.client.sendLogMessage(Log.replace("<", "&amp;lt;").replace("\x0D\x0A", "\x0A"))
                            Log = ""
                    elif args[0] == "cache":
                        message = ""
                        for ip in self.server.IPPermaBanCache:
                            message += ip
                        self.client.sendLogMessage(message)
                        
                    elif args[0] == "iptemp":
                        message = ""
                        for ip in self.server.IPTempBanCache:
                            message += ip
                        self.client.sendLogMessage(message)
                        
                    elif args[0] == "debug":
                        with open(f"./include/logs/Errors/Debug.log", 'r') as File:
                            Log = File.read()
                            File.close()
                        self.client.sendLogMessage(Log.replace("<", "&amp;lt;").replace("\x0D\x0A", "\x0A"))
                        
                    elif args[0] == "promotions":
                        message = ""
                        for promotion in self.server.shopPromotions:
                            message += str(promotion) + ", "
                        self.client.sendLogMessage(message[:-1])

            elif command in ["delete"]:
                if self.client.playerName in self.owners and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])        
                    if self.server.checkExistingUser(playerName):
                        self.Cursor.execute("delete from Users where Username = %s", [playerName])
                        self.client.sendServerMessageAdminOthers(f"The account {playerName} was deleted by {self.client.playerName}")
                        self.client.sendClientMessage(f"The account {playerName} got deleted.", 1)
                    else:
                        self.client.playerException.Invoke("unknownuser")

            elif command in ["resetmaps"]:
                if self.client.playerName in self.owners and self.requireArguments(1):
                    self.client.room.CursorMaps.execute("update Maps set Time = ?, Player = ?, RecDate = ?", [0, "", 0])
                    self.client.sendServerMessageAdmin("All records of fastracing was deleted by %s."%(self.client.playerName))

            elif command in ["reload"]:
                if self.client.playerName in self.owners:
                    try:
                        self.server.reloadServer()
                        self.client.sendClientMessage("Successfull reloaded all modules.", 1)
                    except Exception as e:
                        self.client.sendClientMessage(f"Failed reload all modules. Error: {e}", 1)
                        
            elif command in ["changepassword"]:
                if self.client.playerName in self.owners and self.requireArguments(2):
                    playerName = Utils.parsePlayerName(args[0])
                    password = args[1]
                    player = self.server.players.get(playerName)
                    if player != None:
                        salt = b'\xf7\x1a\xa6\xde\x8f\x17v\xa8\x03\x9d2\xb8\xa1V\xb2\xa9>\xddC\x9d\xc5\xdd\xceV\xd3\xb7\xa4\x05J\r\x08\xb0'
                        hashtext = base64.b64encode(hashlib.sha256(hashlib.sha256(password.encode()).hexdigest().encode() + salt).digest()).decode()
                        self.Cursor.execute(f"UPDATE Users SET Password = '{hashtext}' WHERE Username = '{playerName}'")
                        player.updateDatabase()
                        player.room.removeClient(player)
                        player.transport.close()
                    else:
                        self.client.playerException.Invoke("unknownuser")

         
# Predefined Commands in swf.
            elif command in ["codecadeau"]:
                if self.client.privLevel >= 1 and self.requireArguments(1):
                    d = json.loads(open('./include/json/codes.json','r').read())
                    for i in d['codes']:
                        if args[0].upper() == i['name'] and i['havegot'] == 0:
                            r1 = i['type']
                            r2 = i["amount"]
                            if r1 == "cheeses":
                                self.client.sendPacket(Identifiers.send.Gain_Give, ByteArray().writeInt(r2).writeInt(0).toByteArray())
                                self.client.sendPacket(Identifiers.send.Anim_Donation, ByteArray().writeByte(0).writeInt(r2).toByteArray())
                                self.client.shopCheeses += r2
                                i['havegot'] = 1
                            elif r1 == "fraises":
                                self.client.sendPacket(Identifiers.send.Gain_Give, ByteArray().writeInt(0).writeInt(r2).toByteArray())
                                self.client.sendPacket(Identifiers.send.Anim_Donation, ByteArray().writeByte(1).writeInt(r2).toByteArray())
                                self.client.shopFraises += r2
                                i['havegot'] = 1
                    #self.client.updateDatabase()
                    with open('./include/json/codes.json', 'w') as F:
                        json.dump(d, F)
                        
            elif command in ["sonar"]:
                if self.client.privLevel >= 7 and self.requireArguments(1, True):
                    playerName = Utils.parsePlayerName(args[0])
                    try:
                        arg2 = args[1]
                    except:
                        arg2 = "start"
                    player = self.server.players.get(playerName)
                    if player:
                        self.client.sendPacket(Identifiers.send.Minibox_1, ByteArray().writeShort(200).writeUTF("Sonar "+args[0]).writeUTF('\n'.join(self.server.sonar[playerName]) if playerName in self.server.sonar else "\n").toByteArray())
                        self.server.sonar[playerName] = []
                        if arg2 != "fin":
                            player.sendPacket(Identifiers.send.Init_Sonar, ByteArray().writeInt(8).writeBoolean(True).writeShort(1).toByteArray())
                        else:
                            player.sendPacket(Identifiers.send.End_Sonar, ByteArray().writeInt(8).toByteArray())

        except Exception as e:
            sex = ServerException(e)
            sex.SaveException("Commands.log", self.client, "commanderreur")
            
    def FunCorpPlayerCommands(self):
        message = "FunCorp Commands: \n"
        message += "<J>/changesize</J> <VP>[playerName|*] [size/off]</VP> - <BL> Temporarily changes the size (between 0.1x and 5x) of players.\n"
        message += "<J>/colormouse </J> <VP>[playerName|*] [color/off]</VP> - <BL> Temporarily gives a colorized fur.\n"
        message += "<J>/colornick</J> <VP>[playerName|*] [color/off]</VP> - <BL> Temporarily changes the color of player nicknames.\n"
        message += "<J>/funcorp</J> <VP>[help]</VP> - <BL> Enables/disables FunCorp or Displays all the commands available in the FunCorp mode.\n"
        message += "<J>/linkmice</J><VP>[playerName|*] [off]</VP>  - <BL> Temporarily links players.\n"
        message += "<J>/meep</J> <VP>[playerName|*] [off]</VP> - <BL> 	Give meep to players.\n"
        message += "<J>/transformation</J> <VP>[playerName|*] [off]</VP> - <BL> Temporarily gives the ability to transform.\n"
        return message
        
    def FunCorpMemberCommands(self):
        message = "FunCorp Commands: \n"
        message += "<J>/changenick</J> <VP>[playerName] [newNickname/off]</VP> - <BL> Temporarily changes a player's nickname.\n"
        message += "<J>/changesize</J> <VP>[playerName|*] [size/off]</VP> - <BL> Temporarily changes the size (between 0.1x and 5x) of players.\n"
        message += "<J>/colormouse </J> <VP>[playerName|*] [color/off]</VP> - <BL> Temporarily gives a colorized fur.\n"
        message += "<J>/colornick</J> <VP>[playerName|*] [color/off]</VP> - <BL> Temporarily changes the color of player nicknames.\n"
        message += "<J>/funcorp</J> <VP>[help]</VP> - <BL> Enables/disables FunCorp or Displays all the commands available in the FunCorp mode.\n"
        message += "<J>/linkmice</J> <VP>[playerName|*] [off]</VP>  - <BL> Temporarily links players.\n"
        message += "<J>/meep</J> <VP>[playerName|*] [off]</VP> - <BL> Give meep to players.\n"
        message += "<J>/roomevent</J> <VP>[on|off]</VP> - <BL> Highlights the current room in the room list.\n"
        message += "<J>/lsfc</J> - <BL> List of online funcorps.\n"
        message += "<J>/transformation</J> <VP>[playerName|*] [off]</VP> - <BL> Temporarily gives the ability to transform.\n"
        message += "<J>/tropplein</J> <VP>[Number] [off]</VP> - <BL> Setting a limit for the number of players in a room.\n"
        #message += "<J>/playmusic</J> <VP>[MP3_URL]</VP> - <BL> Start playing music in the room.\n"
        return message