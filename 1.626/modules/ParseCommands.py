#coding: utf-8
import re, sys, json, os, base64, hashlib, time, random, traceback, asyncio, ast
"""
9 Admin, 8 Mod, 7 Arb, 6 MC, 5 FC, 4 LC, 3 - FS, 2 Sentinel, 1 PPL
Commands: /relation, /arb, /resign, /sondage
"""
# Modules
from time import gmtime, strftime
from langues import Langues
from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers
from modules import Lua

# Library
from datetime import datetime

class Exceptions:
    def __init__(self, client, server):
        self.client = client
        self.server = client.server
        self.Cursor = client.Cursor
        self.name = ""
    def Invoke(self, name):
        if name == "unknownuser":
            self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid nickname.")
        elif name == "moreargs":
            self.client.sendMessage("<V>[•]</V> You need more arguments to use this command.")
        elif name == "requireFC":
            self.client.sendMessage("<V>[•]</V> FunCorp commands only work when the room is in FunCorp mode.")
    def to_int(self, s):
        try:
            return ast.literal_eval(s)
        except ValueError:
            return 999999999


class Commands:
    def __init__(self, client, server):
        self.client = client
        self.server = client.server
        self.Cursor = client.Cursor
        self.currentArgsCount = 0
        self.owners = ["Chatta#7646", "Chatta#4845"]
        self.Ex = Exceptions(client, server)

    def requireTribePerm(self):
        if not self.client.tribeName == "" and self.client.room.isTribeHouse:
            rankInfo = self.client.tribeRanks.split(";")
            rankName = rankInfo[self.client.tribeRank].split("|")
            if rankName[2] in ["512"]:
                return True
        return False
    
    def requireArguments(self, arguments):
        if self.currentArgsCount < arguments:
            self.Ex.Invoke("moreargs")
            return False
        elif self.currentArgsCount == arguments:
            return True
        else:
            return False
    
    def requireArgumentsUpper(self, arguments):
        if self.currentArgsCount < arguments:
            self.Ex.Invoke("moreargs")
            return False
        else:
            return True
    
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
                    staff = {}
                    staffList = "$ModoPasEnLigne"
                    for player in self.server.players.values():
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
                    staff = {}
                    staffList = "$MapcrewPasEnLigne"
                    for player in self.server.players.values():
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
                    if (self.client.room.roomName.startswith("*") and self.client.room.roomCreator == self.client.playerName) or self.client.room.roomName.startswith(self.client.playerName):
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
                if not self.client.isDead:
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
                lang = langue.lower()
                if roomName.startswith("#"):
                    self.client.enterRoom(f"{lang}-{roomName}" + "1")
                else:
                    self.client.enterRoom(({0:"", 1:"", 3:"vanilla", 8:"survivor", 9:"racing", 11:"music", 2:"bootcamp", 10:"defilante", 16:"village"}[self.client.lastGameMode]) + roomName)

            elif command in ["bootcamp", "vanilla", "survivor", "racing", "defilante", "tutorial", "fastracing", "village"]: ###############
                self.client.enterRoom("bootcamp1" if command == "bootcamp" else "vanilla1" if command == "vanilla" else "survivor1" if command == "survivor" else "racing1" if command == "racing" else "defilante1" if command == "defilante" else (chr(3) + "[Tutorial] " + self.client.playerName) if command == "tutorial" else "#fastracing1" if command == "fastracing" else "village1" if command == "village" else "")

            elif command in ["ping"]:
                if self.client.privLevel >= 1:
                    self.client.sendMessage("ping ~%s" % str(self.client.PInfo[2]))

            elif command in ["mulodrome"]:
                if (self.client.privLevel >= 9 or self.client.room.roomName.startswith(self.client.playerName) or (self.client.room.roomName.startswith("*") and self.client.room.roomCreator == self.client.playerName)) and not self.client.room.isMulodrome:
                    for player in self.client.room.clients.values():
                        player.sendPacket(Identifiers.send.Mulodrome_Start, 1 if player.playerName == self.client.playerName else 0)

            elif command in ["x_eneko"]:
                self.client.enterRoom(self.client.sendLangueMessage("", "$Entrainement") + self.client.playerName)

            elif command in ["time", "temps"]:
                if self.client.privLevel >= 1:
                    self.client.playerTime += abs(Utils.getSecondsDiff(self.client.loginTime))
                    self.client.loginTime = Utils.getTime()
                    temps = map(int, [self.client.playerTime // 86400, self.client.playerTime // 3600 % 24, self.client.playerTime // 60 % 60, self.client.playerTime % 60])
                    self.client.sendLangueMessage("", "$TempsDeJeu", *temps)

# Tribe Commands:
            elif command in ["inv"]:
                if self.client.privLevel >= 1 and self.requireArguments(1) and self.requireTribePerm():
                    playerName = Utils.parsePlayerName(args[0])
                    if self.server.checkConnectedAccount(playerName) and not playerName in self.client.tribulle.getTribeMembers(self.client.tribeCode):
                        player = self.server.players.get(playerName)
                        player.invitedTribeHouses.append(self.client.tribeName)
                        player.sendPacket(Identifiers.send.Tribe_Invite, ByteArray().writeUTF(self.client.playerName).writeUTF(self.client.tribeName).toByteArray())
                        self.client.sendLangueMessage("", "$InvTribu_InvitationEnvoyee", "<V>" + player.playerName + "</V>")

            elif command in ["invkick"]:
                if self.client.privLevel >= 1 and self.requireArguments(1) and self.requireTribePerm():
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
                if self.client.privLevel >= 1 and self.client.room.isTribeHouse:
                    if self.client.room.isSnowing:
                        self.client.room.startSnow(0, 0, not self.client.room.isSnowing)
                        self.client.room.isSnowing = False
                    else:
                        self.client.room.startSnow(1000, 60, not self.client.room.isSnowing)
                        self.client.room.isSnowing = True

            elif command in ["module"]:
                if self.client.privLevel >= 1 and self.requireTribePerm():
                    if len(args) == 0:
                        self.client.sendMessage("<V>[•]</V> Module list:")
                        for key in self.server.officialminigames:
                            self.client.sendMessage(f"<VP>#{key}</VP> : {self.client.room.getPlayersCountbyRoom('#'+key)}")
                    else:
                        moduleid = args[0]
                        if moduleid[:1] == "stop":
                            if self.client.room.luaRuntime != None:
                                self.client.room.luaRuntime.stopModule()
                        else:
                            module = self.server.minigames.get(moduleid[:1])
                            if module != None:
                                self.client.room.luaRuntime = Lua(self.client.room, self.server)
                                self.client.room.luaRuntime.owner = self.client.playerName
                                #self.luaRuntime.owner = ""
                                self.client.room.luaRuntime.RunCode(module)
            
            elif command in ["sy?"]:
                if(self.client.privLevel in [6, 9] or self.client.isMapCrew == True) or self.client.room.isTribeHouse:
                    self.client.sendLangueMessage("", "<V>[•]</V> $SyncEnCours : [%s]" %(self.client.room.currentSyncName))

            elif command in ["sy"]:
                if((self.client.privLevel in [6, 9] or self.client.isMapCrew == True) or self.client.room.isTribeHouse) and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    player = self.server.players.get(playerName)
                    if player != None:
                        player.isSync = True
                        self.client.room.currentSyncCode = player.playerCode
                        self.client.room.currentSyncName = player.playerName
                        if self.client.room.mapCode != -1 or self.client.room.EMapCode != 0:
                            self.client.sendPacket(Identifiers.old.send.Sync, [player.playerCode, ""])
                            self.client.sendLangueMessage("", "<V>[•]</V> $NouveauSync <V> %s" %(player.playerName))
                        else:
                            self.client.sendPacket(Identifiers.old.send.Sync, [player.playerCode])
                            self.client.sendLangueMessage("", "<V>[•]</V> $NouveauSync <V> %s" %(player.playerName))
                    else:
                        self.Ex.Invoke("unknownuser")
            
            elif command in ["ch"]:
                if (self.client.privLevel in [6, 9] or self.client.room.isTribeHouse or self.client.isMapCrew == True or self.client.room.roomName == "*strm_" + self.client.playerName.lower()) and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    player = self.server.players.get(playerName)
                    if player != None:
                        if self.client.room.forceNextShaman == player.playerCode:
                            self.client.sendLangueMessage("", "<V>[•]</V> $PasProchaineChamane", player.playerName)
                            self.client.room.forceNextShaman = -1
                        else:
                            self.client.sendLangueMessage("", "<V>[•]</V> $ProchaineChamane", player.playerName)
                            self.client.room.forceNextShaman = player.playerCode
                    else:
                        self.Ex.Invoke("unknownuser")
            
            elif command in ["csr"]:
                if (self.client.privLevel in [6, 9] or self.client.isMapCrew == True) and self.client.room.isTribeHouse:
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
            
            
            #elif command in ["playmusic", "musique", "music"]:
                #if (self.client.privLevel >= 1 and self.client.room.isTribeHouse) or self.client.privLevel >= 9:
                    #if len(args) == 0:
                        #self.client.room.sendAll(Identifiers.old.send.Music, [])
                    #else:
                        #self.client.room.sendAll(Identifiers.old.send.Music, [args[0]])


# Lua and Fashion Squad Commands
            elif command in ["lslua"]:
                if self.client.privLevel in [4, 9] or self.client.isLuaCrew == True:
                    LuaCrews = ""
                    self.Cursor.execute("select Username from Users where PrivLevel = %s", [4])
                    r = self.Cursor.fetchall()
                    for rs in r:
                        player = self.server.players.get(rs[0])
                        if player != None:
                            LuaCrews += "<font color='#79bbac'>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </font><br>"
                    for player in self.server.players.values(): # if player has role LuaCrew
                        if ("LuaCrew" in player.roles and not player.playerName.startswith('*')) or player.isLuaCrew:
                            LuaCrews += "<font color='#79bbac'>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </font><br>"
                    if LuaCrews != "":
                        LuaCrews = LuaCrews.rstrip("\n")
                        self.client.sendMessage(LuaCrews)
                    else:
                        self.client.sendMessage("<V>[•]</V> Don't have any online Lua Crews at moment.")

            elif command in ["lsfs"]:
                if self.client.privLevel in [3, 9] or self.client.isFashionSquad == True:
                    FS = ""
                    self.Cursor.execute("select Username from Users where PrivLevel = %s", [3])
                    r = self.Cursor.fetchall()
                    for rs in r:
                        player = self.server.players.get(rs[0])
                        if player != None:
                            FS += "<font color='#ffb6c1'>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </font><br>"
                    for player in self.server.players.values(): # if player has role Fashion Squad
                        if "FashionSquad" in player.roles and not player.playerName.startswith('*') or player.isFashionSquad:
                            FS += "<font color='#ffb6c1'>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </font><br>"
                    if FS != "":
                        FS = FS.rstrip("\n")
                        self.client.sendMessage(FS)
                    else:
                        self.client.sendMessage("<V>[•]</V> Don't have any online Fashion Squads at moment.")

# Funcorp Commands:
            elif command in ["lsfc"]:
                if (self.client.privLevel in [5, 9] or self.client.isFunCorpPlayer == True):
                    FunCorps = ""
                    self.Cursor.execute("select Username from Users where PrivLevel = %s", [5])
                    r = self.Cursor.fetchall()
                    for rs in r:
                        player = self.server.players.get(rs[0])
                        if player != None:
                            FunCorps += "<FC>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </FC><br>"
                    for player in self.server.players.values(): # if player has role LuaCrew
                        if "FunCorp" in player.roles and not player.playerName.startswith('*') or player.isFunCorpPlayer:
                            FunCorps += "<FC>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </FC><br>"
                    if FunCorps != "":
                        FunCorps = FunCorps.rstrip("\n")
                        self.client.sendMessage(FunCorps)
                    else:
                        self.client.sendMessage("<V>[•]</V> Don't have any online Fun Corps at moment.")

            elif command in ["funcorp"]:
                if (self.client.privLevel in [5, 9] or self.client.room.roomName == "*strm_" + self.client.playerName.lower() or self.client.isFuncorpPlayer == True):
                    if len(args) == 0:
                        if self.client.room.isFuncorp:
                            for player in self.client.room.clients.values():
                                player.sendLangueMessage("", "<FC>$FunCorpDesactive</FC>")
                                self.client.room.isFuncorp = False
                                player.mouseName = ""
                                player.funcorpcolornick = ""
                                player.tempMouseColor = ""
                                self.client.room.funcorpNames.clear()
                        else:
                            for player in self.client.room.clients.values():
                                player.sendLangueMessage("", "<FC>$FunCorpActive</FC>")
                                self.client.room.isFuncorp = True
                    else:
                        if args[0] == "help":
                            if self.client.room.roomName == "*strm_" + self.client.playerName.lower() and not self.client.privLevel in [5, 9] and self.client.isFuncorpPlayer == False:
                                self.client.sendLogMessage(self.FunCorpPlayerCommands()) # strm_
                            else:
                                self.client.sendLogMessage(self.FunCorpMemberCommands()) # FC member
                   
            elif command in ["tropplein"]:
                if (self.client.privLevel in [5, 8, 9] or self.client.isFuncorpPlayer == True):
                    if len(args) == 0:
                        self.client.sendMessage("<V>[•]</V> The current maximum number of players is: "+str(self.client.room.maxPlayers))
                    elif self.requireArguments(1):
                        try:
                            maxPlayers = int(args[0])
                            if maxPlayers == 0:
                                self.client.room.maxPlayers = 200
                            else:
                                if maxPlayers < 1: maxPlayers = 1
                                self.client.room.maxPlayers = maxPlayers
                                self.client.sendMessage("<V>[•]</V> Maximum number of players in the room is set to: <BV>" +str(maxPlayers))
                        except:
                            pass

            elif command in ["roomevent"]:
                if (self.client.privLevel in [5, 9] or self.client.isFuncorpPlayer == True):
                    if self.client.room.isFuncorp: 
                        if self.client.room.isFuncorpRoomName:
                            self.client.room.isFuncorpRoomName = False
                            self.client.sendMessage('<V>[•]</V> Sucessfull disabled the room color.')
                        else:
                            self.client.sendMessage('<V>[•]</V> Sucessfull enabled the room color.')
                            self.client.room.isFuncorpRoomName = True
                    else:
                        self.Ex.Invoke("requireFC")

            elif command in ["transformation"]:
                if(self.client.privLevel in [5, 9] or self.client.room.roomName == "*strm_" + self.client.playerName.lower() or self.client.isFuncorpPlayer == True) and self.requireArgumentsUpper(1):
                    if self.client.room.isFuncorp:
                        if len(args) == 2 and args[0] == "*" and args[1] == "off":
                            for player in self.client.room.clients.values():
                                player.sendPacket([27, 10], 0)
                            self.client.sendMessage("<V>[•]</V> All the transformations powers have been removed.")
                        elif len(args) == 1 and args[0] == "*":
                            for player in self.client.room.clients.values():
                                player.sendPacket([27, 10], 1)
                            self.client.sendMessage("<V>[•]</V> Transformations powers given to all players in the room.")
                        else:
                            dump = []
                            for arg in args:
                                dump.append(arg)
                            if dump[-1] != "off":
                                for x in dump:
                                    player = self.server.players.get(x)
                                    if player != None:
                                        player.sendPacket([27, 10], 1)
                                res = ", ".join(dump)
                                self.client.sendMessage("<V>[•]</V> Transformations powers given to players: <BV>"+res+"</BV>")
                            else:
                                for x in dump[:-1]:
                                    player = self.server.players.get(x)
                                    if player != None:
                                        player.sendPacket([27, 10], 0)
                                dump.pop()
                                res = ", ".join(dump)
                                self.client.sendMessage("<V>[•]</V> Transformations powers removed to players: <BV>"+res+"</BV>")
                    else:
                        self.Ex.Invoke("requireFC")

            elif command in ["changesize"]:
                if (self.client.privLevel in [5, 9] or self.client.room.roomName == "*strm_" + self.client.playerName.lower() or self.client.isFuncorpPlayer == True) and self.requireArgumentsUpper(1):
                    if self.client.room.isFuncorp:
                        r1 = 0
                        if len(args) == 2 and args[0] == "*":
                            if args[1] == "off":
                                for player in self.client.room.clients.values():
                                    self.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(100).writeBoolean(False).toByteArray())
                                self.client.sendMessage("<V>[•]</V> All players now have their regular size.")
                            else:
                                r1 = self.Ex.to_int(args[1])
                                if r1 == 999999999: r1 = 100
                                for player in self.client.room.clients.values():
                                    self.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(r1).writeBoolean(False).toByteArray())
                                self.client.sendMessage("<V>[•]</V> All players now have the same size: <BV>" + str(r1) + "</BV>.")
                        else:
                            dump = []
                            for arg in args:
                                dump.append(arg)
                            if dump[-1] != "off":
                                r1 = self.Ex.to_int(dump[-1])
                                if r1 != 999999999:
                                    for x in dump[:-1]:
                                        player = self.server.players.get(x)
                                        if player != None:
                                            self.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(dump[-1]).writeBoolean(False).toByteArray())
                                res = ", ".join(dump)
                                self.client.sendMessage("<V>[•]</V> The following players now have the size "+str(r1)+": <BV>"+res+"</BV>")
                            else:
                                for x in dump[:-1]:
                                    player = self.server.players.get(x)
                                    if player != None:
                                        self.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(100).writeBoolean(False).toByteArray())
                                dump.pop()
                                res = ", ".join(dump)
                                self.client.sendMessage("<V>[•]</V> The following players now have their regular size: <BV>"+res+"</BV>")

                    else:
                        self.Ex.Invoke("requireFC")

            elif command in ["meep"]:
                if (self.client.privLevel in [5, 9] or self.client.room.roomName == "*strm_" + self.client.playerName.lower() or self.client.isFuncorpPlayer == True) and self.requireArgumentsUpper(1):
                    if self.client.room.isFuncorp:
                        if len(args) == 2 and args[0] == "*" and args[1] == "off":
                            for player in self.client.room.clients.values():
                                player.sendPacket(Identifiers.send.Can_Meep, 0)
                            self.client.sendMessage("<V>[•]</V> All the meep powers have been removed.")
                            
                        elif len(args) == 1 and args[0] == "*":
                            for player in self.client.room.clients.values():
                                player.sendPacket(Identifiers.send.Can_Meep, 1)
                            self.client.sendMessage("<V>[•]</V> Meep powers given to all players in the room.")
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
                                self.client.sendMessage("<V>[•]</V> Meep powers given to players: <BV>"+res+"</BV>")
                            else:
                                for x in dump[:-1]:
                                    player = self.server.players.get(x)
                                    if player != None:
                                        player.sendPacket(Identifiers.send.Can_Meep, 0)
                                dump.pop()
                                res = ", ".join(dump)
                                self.client.sendMessage("<V>[•]</V> Meep powers removed from players: <BV>"+res+"</BV>")
                    else:
                        self.Ex.Invoke("requireFC")
      
            elif command in ["changenick", "changename"]:
                if(self.client.privLevel in [5, 9] or self.client.isFuncorpPlayer == True) and self.requireArguments(2):
                    if self.client.room.isFuncorp:
                        playerName = Utils.parsePlayerName(args[0])
                        newName = argsNotSplited.split(" ", 1)[1]
                        player = self.server.players.get(playerName)
                        if player != None:
                            if newName == "off":
                                player.mouseName = ""
                                self.client.room.funcorpNames[player.playerName] = ""
                                self.client.sendMessage("<V>[•]</V> The following player has changed his nickname to default: <BV>"+ str(player.playerName) +"</BV>")
                            else:
                                player.mouseName = newName
                                self.client.room.funcorpNames[player.playerName] = newName
                                self.client.sendMessage("<V>[•]</V> The following player has changed his nickname: <BV>"+ str(player.playerName) +"</BV>")
                    else:
                        self.Ex.Invoke("requireFC")
              
            elif command in ["linkmice"]: 
                if (self.client.privLevel in [5, 9] or self.client.room.roomName == "*strm_" + self.client.playerName.lower() or self.client.isFuncorpPlayer == True) and self.requireArgumentsUpper(2):
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
                        self.Ex.Invoke("requireFC")
              
# MapCrew Commands:
            elif command in ["lsmc"]:
                if self.client.privLevel in [6, 9] or self.client.isMapCrew == True:
                    Mapcrews = ""
                    self.Cursor.execute("select Username from Users where PrivLevel = %s", [6])
                    r = self.Cursor.fetchall()
                    for rs in r:
                        player = self.server.players.get(rs[0])
                        if player != None:
                            Mapcrews += "<BV>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </BV><br>"
                    for player in self.server.players.values(): # if player has role MapCrew
                        if "MapCrew" in player.roles and not player.playerName.startswith('*') or player.isMapCrew:
                            Mapcrews += "<BV>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </BV><br>"
                    if Mapcrews != "":
                        Mapcrews = Mapcrews.rstrip("\n")
                        self.client.sendMessage(Mapcrews)
                    else:
                        self.client.sendMessage("<V>[•]</V> Don't have any online Map Crews at moment.")
                    
            elif command in ["del"]:
                if self.client.privLevel in [6, 9] or self.client.isMapCrew == True:
                    if len(args) == 1:
                        mapCode = args[0]
                        mapCode = mapCode.replace('@', '')
                        if mapCode != -1:
                            self.client.room.CursorMaps.execute("update Maps set Perma = ? where Code = ?", ["44", mapCode])
                            self.client.sendMessage("<V>[•]</V> Successfull deleted the map: @"+str(mapCode)+".")
                    elif len(args) == 0:
                        mapCode = self.client.room.mapCode
                        if mapCode != -1:
                            self.client.room.CursorMaps.execute("update Maps set Perma = ? where Code = ?", [44, mapCode])
                            self.client.sendMessage("<V>[•]</V> Successfull deleted the map: @"+str(mapCode)+".")
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
                            self.client.sendMessage("<VP>[%s] (@%s): validate map <J>P%s</J> => <J>P%s</J>" %(self.client.playerName, mapCode, currentCategory, category))
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
                            
                        try: self.client.sendLogMessage("<font size=\"12\"><N>Total Maps </N> <BV>%s</BV> <N>with category: </N> <V>p%s %s</V></font>" %(mapCount, category, mapList))
                        except: self.client.sendMessage("<R><V>[•]</V> There are too many maps and it can not be opened.</R>")

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

                    try: self.client.sendLogMessage("<font size= \"12\"><V>%s<N>'s maps: <BV>%s %s</font>" %(playerName, mapCount, mapList))
                    except: self.client.sendMessage("<R><V>[•]</V> There are too many maps and it can not be opened.</R>")

            elif command in ["mapinfo"]:
                if self.client.privLevel in [6, 9] or self.client.isMapCrew == True:
                    if self.client.room.mapCode != -1:
                        totalVotes = self.client.room.mapYesVotes + self.client.room.mapNoVotes
                        if totalVotes < 1: totalVotes = 1
                        Rating = (1.0 * self.client.room.mapYesVotes / totalVotes) * 100
                        rate = str(Rating).split(".")[0]
                        if rate == "Nan": rate = "0"
                        self.client.sendMessage("[•] <V>"+str(self.client.room.mapName)+"<BL> - <V>@"+str(self.client.room.mapCode)+"<BL> - <V>"+str(totalVotes)+"<BL> - <V>"+str(rate)+"%<BL> - <V>P"+str(self.client.room.mapPerma)+"<BL>.")

            elif command in ["np", "npp"]: ########
                if (self.client.privLevel >= 5 or self.client.room.roomName == "*strm_" + self.client.playerName.lower() or self.client.isMapCrew == True) or self.client.room.isTribeHouse:
                    if len(args) == 0:
                        self.client.room.mapChange()
                    elif len(args) == 1:
                        if not self.client.room.isVotingMode:
                            code = args[0]
                            if code.startswith("@"):
                                mapInfo = self.client.room.getMapInfo(int(code[1:]))
                                if mapInfo[0] == None:
                                    self.client.sendLangueMessage("", "$CarteIntrouvable")
                                else:
                                    self.client.room.forceNextMap = code
                                    if command == "np":
                                        if self.client.room.changeMapTimer != None:
                                            self.client.room.changeMapTimer.cancel()
                                        self.client.room.mapChange()
                                    else:
                                        self.client.sendLangueMessage("", "$ProchaineCarte %s" %(code))

                            elif code.isdigit():
                                self.client.room.forceNextMap = code
                                if command == "np":
                                    if self.client.room.changeMapTimer != None:
                                        self.client.room.changeMapTimer.cancel()
                                    self.client.room.mapChange()
                                else:
                                    self.client.sendLangueMessage("", "$ProchaineCarte %s" %(code))

# Arbitre Commands:           

            elif command in ["lsarb"]:
                if self.client.privLevel >= 7 or self.client.isArbitre:
                    Arbitres = ""
                    self.Cursor.execute("select Username from Users where PrivLevel = %s", [7])
                    r = self.Cursor.fetchall()
                    for rs in r:
                        player = self.server.players.get(rs[0])
                        if player != None:
                            Arbitres = "<font color='#B993CA>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </font>"
                    if Arbitres != "":
                        Arbitres = Arbitres.rstrip("\n")
                        self.client.sendMessage(Arbitres)
                    else:
                        self.client.sendMessage("<V>[•]</V> Don't have any online Arbitres at moment.")

            elif command in ["unban", "deban"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    modName = self.client.playerName
                    found = False
                    player = self.server.players.get(playerName)
                    if player != None or self.server.checkExistingUser(playerName):
                        if self.server.checkTempBan(playerName):
                            self.server.removeTempBan(playerName)
                            found = True
                        if self.server.checkPermaBan(playerName):
                            self.server.removePermaBan(playerName)
                            found = True
                        if found:
                            import time
                            self.Cursor.execute("insert into BanLog values (%s, %s, '', '', %s, 'Unban', '')", [playerName, self.client.playerName, int(str(time.time())[:9])])
                            self.client.sendServerMessage("%s unbanned the player %s." %(self.client.playerName, playerName))
                            self.server.saveCasier(playerName, "UNBAN", modName, "", "")
                        else:
                            self.Ex.Invoke("usernotbanned")
                    else:
                        self.Ex.Invoke("unknownuser")

            elif command in ["ban"]:
                if self.client.privLevel >= 7 or self.client.room.roomName == "*strm_" + self.client.playerName.lower():
                    if self.client.room.roomName == "*strm_" + self.client.playerName.lower() and self.requireArguments(1): # STRM support
                        playerName = Utils.parsePlayerName(args[0])
                        player = self.server.players.get(playerName)
                        if player != None:
                            player.enterRoom('1')
                            
                    elif self.client.privLevel >= 7 and self.requireArgumentsUpper(3):
                        playerName = Utils.parsePlayerName(args[0])
                        player = self.server.players.get(playerName)
                        if player != None:
                            hours = int(args[1])
                            reason = argsNotSplited.split(" ", 2)[2]
                            if self.server.checkConnectedAccount(playerName):
                                self.client.sendServerMessage("%s banned the player %s for %sh (%s)." %(self.client.playerName, playerName, hours, reason))
                                self.server.banPlayer(playerName, hours, reason, self.client.playerName)
                            else:
                                self.client.sendServerMessage("%s offline banned the player %s for %sh (%s)." %(self.client.playerName, playerName, hours, reason))
                                self.server.banPlayer(playerName, hours, reason, self.client.playerName)
                                #self.Ex.Invoke("useralreadybanned")
                        else:
                            self.Ex.Invoke("unknownuser")
                    else:
                        pass

            elif command in ["iban"]:
                if self.client.privLevel >= 7 and self.requireArgumentsUpper(3):
                    playerName = Utils.parsePlayerName(args[0])
                    player = self.server.players.get(playerName)
                    if player != None:
                        hours = int(args[1])
                        reason = argsNotSplited.split(" ", 2)[2]
                        if not player.isBanned:
                            if self.server.checkConnectedAccount(playerName):
                                self.client.sendServerMessage("%s banned the player %s for %sh (%s)." %(self.client.playerName, playerName, hours, reason))
                                self.server.banPlayer(playerName, hours, reason, self.client.playerName)
                            else:
                                self.client.sendServerMessage("%s offline banned the player %s for %sh (%s)." %(self.client.playerName, playerName, hours, reason))
                                self.server.banPlayer(playerName, hours, reason, self.client.playerName)
                        else:
                            self.Ex.Invoke("useralreadybanned")
                            #self.client.sendMessage("<V>[•]</V> Player ["+str(playerName)+"] is already banned, please wait.")
                    else:
                        self.Ex.Invoke("unknownuser")

            elif command in ["chatlog"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    self.client.modoPwet.openChatLog(Utils.parsePlayerName(args[0]))

            elif command in ["banhack"]: ########
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    player = self.server.players.get(playerName)
                    if player != None:
                        hours = 360
                        reason = "Hack. Your account will be permanently banned if you continue to violate the rules!"
                        player.sendPlayerBan(hours, reason)
                        self.server.banPlayer(player.playerName, hours, reason, self.client.playerName)
                        self.client.sendServerMessage("%s banned the player %s for %sh (%s)" %(self.client.playerName, playerName, hours, reason))
                    else:
                        self.Ex.Invoke("unknownuser")
                   
            elif command in ["ibanhack"]: ########
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    player = self.server.players.get(playerName)
                    if player != None:
                        hours = 360
                        reason = "Hack. Your account will be permanently banned if you continue to violate the rules!"
                        player.sendPacket(Identifiers.old.send.Player_Ban, [3600000 * hours, reason])
                        self.server.banPlayer(player.playerName, hours, reason, self.client.playerName)
                        self.client.sendServerMessage("%s banned the player %s for %sh (%s)" %(self.client.playerName, playerName, hours, reason))
                    else:
                        self.Ex.Invoke("unknownuser")
                   
            elif command in ["mute"]:
                if self.client.privLevel >= 7 and self.requireArgumentsUpper(3):
                    playerName = Utils.parsePlayerName(args[0])
                    if self.server.checkExistingUser(playerName):
                        if self.server.checkTempMute(playerName):
                            self.Ex.Invoke("useralreadymuted")
                        else:
                            time = args[1] if (len(args) >= 2) else ""
                            reason = argsNotSplited.split(" ", 2)[2] if (len(args) >= 3) else ""
                            hours = int(time) if (time.isdigit()) else 1
                            hours = 9999999 if (hours > 9999999) else hours
                            self.server.mutePlayer(playerName, hours, reason, self.client.playerName)
                    else:
                        self.Ex.Invoke("unknownuser")

            elif command in ["imute"]:
                if self.client.privLevel >= 7 and self.requireArgumentsUpper(3):
                    playerName = Utils.parsePlayerName(args[0])
                    if self.server.checkExistingUser(playerName):
                        if self.server.checkTempMute(playerName):
                            self.Ex.Invoke("useralreadymuted")
                        else:
                            time = args[1] if (len(args) >= 2) else ""
                            reason = argsNotSplited.split(" ", 2)[2] if (len(args) >= 3) else ""
                            hours = int(time) if (time.isdigit()) else 1
                            hours = 9999999 if (hours > 9999999) else hours
                            self.server.mutePlayerIP(playerName, hours, reason, self.client.playerName)
                    else:
                        self.Ex.Invoke("unknownuser")

            elif command in ["unmute", "demute"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    if self.server.checkExistingUser(playerName):
                        if self.server.checkTempMute(playerName):
                            modName = self.client.playerName
                            self.client.sendServerMessage("%s unmuted the player %s." %(self.client.playerName, playerName))
                            self.server.removeModMute(playerName)
                            self.client.isMute = False
                            self.server.saveCasier(playerName, "UNMUTE", modName, "", "")
                        else:
                            self.Ex.Invoke("usernotmuted")
                    else:
                        self.Ex.Invoke("unknownuser")

            elif command in ["l"]:
                if self.client.privLevel >= 7:
                    playerName = self.client.playerName if len(args) == 0 else "" if "." in args[0] else Utils.parsePlayerName(args[0])
                    ip = args[0] if len(args) != 0 and "." in args[0] else ""
                    if playerName != "":
                        self.Cursor.execute("select DISTINCT IP, Time, Country, ConnectionID from LoginLogs where Username = %s", [playerName])
                        r = self.Cursor.fetchall()
                        message = "<p align='center'>Connection logs for player: <BL>"+playerName+"</BL>\n</p>"
                        for rs in r:
                            message += "<p align='left'><V>[%s]</V> <BL>%s ( <font color = '%s'>%s</font> - %s ) %s - %s</BL><br>" % (playerName, str(rs[1]), self.client.ipColor(self.client.TFMIPDEC(rs[0])), rs[0], self.client.getCountryIP(rs[0]), rs[3], rs[2])
                        self.client.sendLogMessage(message)

                    elif ip != "":
                        self.Cursor.execute("select DISTINCT Username, Time, Country, ConnectionID from LoginLogs where IP = %s", [ip])
                        r = self.Cursor.fetchall()
                        message = "<p align='center'>Connection logs for ip: <V>"+ip+"</V>\n</p>"
                        for rs in r:
                            message += "<p align='left'><V>[%s]</V> <BL>%s ( <font color = '%s'>%s</font> - %s ) %s - %s</BL><br>" % (str(rs[0]), str(rs[1]), self.client.ipColor(self.client.TFMIPDEC(ip)), ip, self.client.getCountryIP(ip), rs[3], rs[2])
                        self.client.sendLogMessage(message)
            
            elif command in ["roomkick"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    player = self.server.players.get(playerName)
                    if player != None:
                        self.client.sendServerMessage(player.playerName+" has been roomkicked from ["+str.lower(player.room.name)+"] by "+self.client.playerName+".")
                        player.enterRoom('1')
                    else:
                        self.Ex.Invoke("unknownuser")
                        
            elif command in ["follow", "join"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    player = self.server.players.get(playerName)
                    if player != None:
                        self.client.enterRoom(player.roomName)
                    else:
                        self.Ex.Invoke("unknownuser")

            elif command in ["ninja"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    player = self.server.players.get(playerName)
                    if player != None:
                        if not self.client.playerName == player.playerName:
                            roomName = player.room.name
                            if not roomName in ["[Editeur]", "[Totem]"]:
                                self.client.isHidden = True
                                self.client.sendPlayerDisconnect()
                                self.client.startBulle(roomName)
                                self.client.sendPacket(Identifiers.send.Watch, ByteArray().writeUTF(playerName).toByteArray())
                    else:
                        self.Ex.Invoke("unknownuser")
                    
            elif command in ["ip"]:
                if self.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    player = self.server.players.get(playerName)
                    if player != None:
                        self.client.sendMessage("<V>[•]</V> <BV>%s</BV> -> <font color = '%s'>%s</font>" %(playerName, self.client.ipColor(player.ipAddress), self.client.TFMIP(player.ipAddress)))
                    else:
                        self.Ex.Invoke("unknownuser")
            
            
            elif command in ["kick"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    player = self.server.players.get(playerName)
                    if player != None:
                        player.room.removeClient(player)
                        player.transport.close()
                        self.client.sendServerMessage("The player %s has been kicked by %s."%(playerName, self.client.playerName))
                    else:
                        self.Ex.Invoke("unknownuser")

            elif command in ["room*", "salon*", "sala*"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    if args[0][0:2] in self.server.langs:
                        self.client.enterRoom(args[0])
                    else:
                        self.client.sendMessage(f"<V>[•]</V> The community {args[0][0:2]} is invalid.")

            elif command in ["clearban"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    if self.server.checkExistingUser(playerName) or self.server.checkConnectedAccount(playerName):
                        player = self.server.players.get(playerName)
                        if player != None:
                            player.voteBan = []
                            self.client.sendServerMessage("%s removed all ban votes of %s." %(self.client.playerName, playerName))
                        else:
                             self.Ex.Invoke("unknownuser")

            elif command in ["chatfilter"]:
                if self.client.privLevel >= 7:
                    try:
                        if args[0] == "list" and self.requireArguments(1):
                            msg = " "*60 + "Filter List (" + self.server.miceName + ")"
                            msg += "\n<V>"
                            for message in self.server.serverList:
                                msg += message + "\n"
                            self.client.sendLogMessage(msg)
                        elif args[0] == "del" and self.requireArgumentsUpper(2):
                            name = args[1].replace("http://www.", "").replace("https://www.", "").replace("http://", "").replace("https://", "").replace("www.", "")
                            if not name in self.server.serverList:
                                self.client.sendMessage("<V>[•]</V> The string <N>[%s]</N> is not in the filter." %(name))
                            else:
                                self.server.serverList.remove(name)
                                self.server.updateBlackList()
                                self.client.sendMessage("<V>[•]</V> The string <N>[%s]</N> has been removed from the filter." %(name))
                        elif self.requireArgumentsUpper(1):
                            name = args[0].replace("http://www.", "").replace("https://www.", "").replace("http://", "").replace("https://", "").replace("www.", "")
                            if name in self.server.serverList:
                                self.client.sendMessage("<V>[•]</V> The string <N>[%s]</N> is already on the filter." %(name))
                            else:
                                self.server.serverList.append(name)
                                self.server.updateBlackList()
                                self.client.sendMessage("<V>[•]</V> The string <N>[%s]</N> has been added to the filter." %(name))
                    except:
                        self.Ex.Invoke("moreargs")

            elif command in ["mumute"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    if self.server.checkConnectedAccount(playerName):
                        self.server.sendMumute(playerName, self.client.playerName)
                        self.client.sendMessage("<V>[•]</V> "+ playerName + " got mumuted.")

            elif command in ["lsc"]:
                if self.client.privLevel >= 7:
                    result = {}
                    for room in self.server.rooms.values():
                        if room.community in result:
                            result[room.community] = result[room.community] + room.getPlayerCount()
                        else:
                            result[room.community] = room.getPlayerCount()

                    message = "\n"
                    for community in result.items():
                        message += "<BL>%s<BL> : <J>%s\n" %(community[0].upper(), community[1])
                    message += "<BL>ALL<BL> : <J>%s" %(sum(result.values()))
                    self.client.sendLogMessage(message)

            elif command in ["find", "chercher", "search"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    Text = args[0]
                    result = ""
                    for player in self.server.players.values():
                        if player.playerName.startswith(Text):
                            result += "<BV>%s</BV> -> <V>%s</V>\n" %(player.playerName, player.room.name)
                    result = result.rstrip("\n")
                    self.client.sendMessage("<V>[•]</V>\n "+result)

            elif command in ["nomip"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    player = self.server.players.get(playerName)
                    if player != None:
                        ipList="<V>[•]</V> "+playerName+"'s last known IP addresses:"
                        self.Cursor.execute("select distinct IP from LoginLogs where Username = %s", [playerName])
                        for rs in self.Cursor.fetchall():
                            ipList += "<br>" + rs[0]
                        self.client.sendMessage(ipList)
                    else:
                        self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid nickname.")

            elif command in ["ipnom"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    ip = args[0]
                    List = "<V>[•]</V> Logs for the IP address ["+ip+"]:"
                    self.Cursor.execute("select distinct Username from LoginLogs where IP = %s", [ip])
                    r = self.Cursor.fetchall()
                    for rs in r:
                        if self.server.checkConnectedAccount(rs[0]):
                            List += "<br>" + rs[0] + " <G>(online)</G>"
                        else:
                            List += "<br>" + rs[0]
                    self.client.sendMessage(List)

            elif command in ["delrecord"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    mapCode = args[0]
                    if self.server.checkRecordMap(mapCode):
                        self.client.room.CursorMaps.execute("update Maps set Time = ? and Player = ? and RecDate = ? where Code = ?", [0, "", 0, str(mapCode)])
                        self.client.sendServerMessage("The map's record: @"+str(mapCode)+" was removed by <BV>"+str(self.client.playerName)+"</BV>.")
                    else:
                        self.client.sendMessage("<V>[•]</V> The map isn't have a record.")

            elif command in ["roompw"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    roomName = argsNotSplited.split(" ", 0)[0]
                    try:
                        for client in self.server.rooms[roomName].clients.values():
                            if client != None:
                                password = client.room.roomPassword
                        if len(password) != 0:
                            self.client.sendMessage("<V>[•] Password -> </V>" + password)
                        else:
                            self.client.sendMessage("<V>[•]</V> The room [<J>"+roomName+"</J>] doesn't have password.")
                    except KeyError:
                        self.client.sendMessage("<V>[•]</V> The room [<J>"+roomName+"</J>] doesn't exists.")

            elif command in ["prison"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    player = self.server.players.get(playerName)
                    if player != None:
                        if player.isPrisoned:
                            player.isPrisoned = False
                            self.client.sendServerMessage(player.playerName+" unprisoned by "+self.client.playerName+".")
                            player.enterRoom("1")
                        else:
                            player.enterRoom("*Bad Girls")
                            player.isPrisoned = True
                            self.client.sendServerMessage(player.playerName+" prisoned by "+self.client.playerName+".")
                    else:
                        self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid nickname.")

            elif command in ["commu"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    commu = args[0]
                    if commu in self.server.langs:
                        self.client.langue = commu
                        self.client.langueID = Langues.getLangues().index(commu)
                        self.client.startBulle(self.server.recommendRoom(commu))
                        self.client.sendMessage(f"<V>[•]</V> Successfull changed your community to <J>{commu}</J>.")
                    else:
                        self.client.sendMessage(f"<V>[•]</V> The community <J>{commu}</J> is invalid.")

            elif command in ["casier"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    player = self.server.players.get(playerName)
                    if player != None:
                        message = "<p align='center'><N>Sanction Logs for <V>"+playerName+"</V></N>\n</p><p align='left'>Currently running sanctions: </p><br>"
                        self.Cursor.execute("select * from bmlog where Name = %s order by Timestamp desc limit 0, 200", [playerName])
                        for rs in self.Cursor.fetchall():
                            name,state,timestamp,modName,time,reason = rs[0],rs[1],rs[2],rs[3],rs[4],rs[5]
                            fromtime = str(datetime.fromtimestamp(float(int(timestamp))))
                            ip = self.client.TFMIP(player.ipAddress)
                            if time == '': time = 0
                            sanctime = (int(time)*60*60)
                            totime = str(datetime.fromtimestamp(float(int(timestamp) + sanctime)))
                            if state == "UNMUTE" or state == "UNBAN":
                                message = message + "<G><font size='12'><p align='left'> - </G><G><b>" + state + "</b> (" + str(ip) + ") by " + modName + "</font></G>\n"
                                message = message + "<G><p align='left'><font size='9'>    " + fromtime + "</font></G>\n\n"
                            elif state == "MUMUTE":
                                message = message + "<N><font size='12'><p align='left'> - <b><V></N>" + state + " " + str(time) + "h</V></b><N> (" + str(ip) + ") by " + modName + " : <BL>" + reason + "</BL>\n"
                                message = message + "<p align='left'><font size='9'>    " + fromtime + "</font>\n\n"
                            else:
                                message = message + "<N><font size='12'><p align='left'> - <b><V></N>" + state + " " + str(time) + "h</V></b><N> (" + str(ip) + ") by " + modName + " : <BL>" + reason + "</BL>\n"
                                message = message + "<p align='left'><font size='9'><N2>    " + fromtime + " -> "+ str(totime) + "</N2>\n\n"
                        self.client.sendLogMessage(message)
                    else:
                        self.client.sendMessage("<V>[•]</V> There has been an error when retrieving the list of sanctions of the player "+playerName+" : PARAMETRE_INVALIDE.")

            elif command in ["closeroom"]:
                if self.client.privLevel >= 7:
                    if len(args) == 0:
                        roomName = self.client.room.name
                        for player in [*self.client.room.clients.values()]:
                            player.enterRoom('1')
                        self.client.sendMessage("<V>[•]</V> "+str(self.client.playerName)+" closed the room ["+roomName+"].")
                    elif len(args) == 1:
                        roomName = argsNotSplited.split(" ", 0)[0]
                        try:
                            for client in [*self.server.rooms[roomName].clients.values()]:
                                client.enterRoom('1')
                            self.client.sendMessage("<V>[•]</V> "+str(self.client.playerName)+" closed the room ["+roomName+"].")
                        except KeyError:
                            self.client.sendMessage("<V>[•]</V> The room [<J>"+roomName+"</J>] doesn't exists.")
                    else:
                        pass
                                    
            elif command in ["lsroom"]:
                if self.client.privLevel >= 7:
                    if len(args) == 0:
                        Message = "<V>[•]</V> Players in room ["+str(self.client.roomName[:2].lower() + self.client.roomName[2:])+"]: "+str(self.client.room.getPlayerCount())+"\n"
                        for player in [*self.client.room.clients.values()]:
                            if not player.isHidden:
                                Message += "<BL>%s / </BL><font color = '%s'>%s</font> <G>(%s)</G>\n" % (player.playerName, self.client.ipColor(player.ipAddress), self.client.TFMIP(player.ipAddress), self.client.getCountryIP(player.ipAddress))
                            else:
                                Message += "<BL>%s / </BL><font color = '%s'>%s</font> <G>(%s)</G> <BL>(invisible)</BL>\n" % (player.playerName, self.client.ipColor(player.ipAddress), self.client.TFMIP(player.ipAddress), self.client.getCountryIP(player.ipAddress))
                        Message = Message.rstrip("\n")
                        self.client.sendMessage(Message)
                    elif len(args) == 1:
                        roomName = argsNotSplited.split(" ", 0)[0]
                        try:
                            players = 0
                            for player in [*self.server.rooms[roomName].clients.values()]:
                                players = players + 1
                            Message = "<V>[•]</V> Players in room ["+roomName+"]: "+str(players)+"\n"
                            for player in [*self.server.rooms[roomName].clients.values()]:
                                if not player.isHidden:
                                    Message += "<BL>%s / </BL><font color = '%s'>%s</font> <G>(%s)</G>\n" % (player.playerName, self.client.ipColor(player.ipAddress), self.client.TFMIP(player.ipAddress), self.client.getCountryIP(player.ipAddress))
                                else:
                                    Message += "<BL>%s / </BL><font color = '%s'>%s</font> <G>(%s)</G> <BL>(invisible)</BL>\n" % (player.playerName, self.client.ipColor(player.ipAddress), self.client.TFMIP(player.ipAddress), self.client.getCountryIP(player.ipAddress))
                            Message = Message.rstrip("\n")
                            self.client.sendMessage(Message)
                        except KeyError:
                            self.client.sendMessage("<V>[•]</V> The room [<J>"+roomName+"</J>] doesn't exists.")
                    else:
                        pass
                            
            elif command in ["unbanip"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    ip = args[0]
                    decip = self.client.TFMIPDEC(ip)
                    if decip in self.server.IPPermaBanCache:
                        self.server.IPPermaBanCache.remove(decip)
                        self.Cursor.execute("delete from IPPermaBan where IP = %s", [decip])
                        self.client.sendServerMessage("%s unbanned the ip address %s." %(self.client.playerName, ip))
                    else:
                        self.client.sendMessage("<V>[•]</V> The IP isn't banned.")
                            
            elif command in ["ls"]:
                if self.client.privLevel >= 7:
                    if len(args) >= 1:
                        roomNAME = argsNotSplited.split(" ", 0)[0] if (len(args) >= 1) else ""
                        totalusers = 0
                        users, rooms, message = 0, [], ""
                        for room in self.server.rooms.values():
                            if room.name.find(roomNAME) != -1 or room.name.startswith(roomNAME):
                                rooms.append([room.name, room.community, room.getPlayerCount()])
                                
                        message += "<N>List of rooms matching [%s]:</N>" % (roomNAME)
                        for roomInfo in rooms:
                            message += "\n"
                            message += "<BL>%s <G>(%s / %s)</G> : <V>%s</V>" % (str.lower(roomInfo[0]), str.lower(roomInfo[1]), self.client.BulleServer(str.upper(roomInfo[1])), roomInfo[2])
                            totalusers = totalusers + roomInfo[2]
                        message += "\n<J>Total players:</J> <R>%s</R>" % (totalusers)
                        self.client.sendLogMessage(message)
                    else:
                        bulle = ""
                        data = []
                        for room in self.server.rooms.values():
                            if room.name.startswith("*") and not room.name.startswith("*" + chr(3)):
                                data.append(["xx", room.name, room.getPlayerCount()])
                                bulle = "bulle0"
                            elif room.name.startswith(str(chr(3))) or room.name.startswith("*" + chr(3)):
                                if room.name.startswith(("*" + chr(3))):
                                    data.append(["xx", room.name, room.getPlayerCount()])
                                    bulle = "maison"
                                else:
                                    data.append(["*", room.name, room.getPlayerCount()])
                                    bulle = self.client.BulleServer("*")
                            else:
                                data.append([room.community, room.roomName, room.getPlayerCount()])
                                bulle = self.client.BulleServer(str.upper(room.community))
                        result = "<N>List of rooms:</N>"
                        for roomInfo in data:
                            if bulle == "maison":
                                result += "\n<BL>%s</BL> <G>(%s / %s) :</G> <V>%s</V>" % (roomInfo[1] ,str.lower(roomInfo[0]), bulle, roomInfo[2])
                            else:
                                result += "\n<BL>%s-%s</BL> <G>(%s / %s) :</G> <V>%s</V>" % (str.lower(roomInfo[0]), roomInfo[1] ,str.lower(roomInfo[0]), bulle, roomInfo[2])
                        result += "\n<J>Total players:</J> <R>%s</R>" %(len(self.server.players))
                        self.client.sendLogMessage(result)

            elif command in ["relation"]: ########
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    playerName = args[0]
                    player = self.server.players.get(playerName)
                    if player != None:
                        r1 = []
                        displayed = []
                        List = "<V>[•]</V> The player <BV>"+str(playerName)+"</BV> has the following relations:"
                        if player == None:
                            self.Cursor.execute("select distinct IP from LoginLogs where Username = %s", [playerName])
                            try:
                                ip35 = self.client.TFMIPDEC(self.Cursor.fetchall()[0][0])
                            except:
                                self.client.sendMessage("<V>[•]</V> The player <BV>"+str(playerName)+"</BV> does not exist")
                                return
                        else:
                            ip35 = player.ipAddress
                        self.Cursor.execute("select distinct Username from LoginLogs where IP = %s", [self.client.TFMIP(ip35)])
                        ip2 = f"<font color='{self.client.ipColor(ip35)}'>{self.client.TFMIP(ip35)}</font>"
                        for rs in self.Cursor.fetchall():
                            if rs[0] in displayed: continue
                            if self.server.players.get(str(rs[0])) == None:
                                d = self.Cursor.execute("select distinct IP from LoginLogs where Username = %s", [str(rs[0])])
                                d = self.Cursor.fetchall()
                                ips = []
                                ips2 = []
                                for i in d:
                                    if i[0] in ips2: continue
                                    ips.append(f"<font color='{self.client.ipColor(self.client.TFMIPDEC(i[0]))}'>{i[0]}</font>")
                                    ips2.append(i[0])
                                toshow = ", ".join(ips)
                                
                                List += f"<br>- <BV>{rs[0]}</BV> : {toshow}"
                            else:
                                ip31 = self.server.players.get(str(rs[0])).ipAddress
                                List += f"<br>- <BV>{rs[0]}</BV> : <font color='{self.client.ipColor(ip31)}'>{self.client.TFMIP(ip31)}</font> (Current ip)"
                            displayed.append(rs[0])

                        self.client.sendMessage(List)
                   
            elif command in ["infotribu"]: ########
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
                                    message += "<N>-<N> <V>"+str(playerName)+"</V> : <BL>"+str(tribeRank)+"</BL> <N>(</N><font color = '"+str(self.client.ipColor(pl1.ipAddress))+"'>"+str(self.client.TFMIP(pl1.ipAddress))+"</font><N> / "+str(pl1.roomName)+")</N>\n"
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

            elif command in ["infocommu"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    commu = args[0]
                    if commu in self.server.langs:
                        self.client.sendMessage(f"<V>[•]</V><J> Total Players in Community</J> <BV>{commu}</BV>: <R>{self.client.TotalPlayersCommunity(commu)}</R>")
                    else:
                        self.client.sendMessage(f"<V>[•]</V> The community <J>{commu}</J> is invalid.")

            elif command in ["creator"]:
                if self.client.privLevel >= 7:
                    self.client.sendMessage("<V>[•]</V> Room [<J>"+self.client.room.name+"</J>]'s creator: <BV>"+self.client.room.roomCreator+"</BV>")

# Moderator Commands

            elif command in ["lsmodo"]:
                if self.client.privLevel in [7, 8, 9]:
                    Moderateurs = ""
                    self.Cursor.execute("select Username from Users where PrivLevel = %s", [8])
                    r = self.Cursor.fetchall()
                    for rs in r:
                        player = self.server.players.get(rs[0])
                        if player != None:
                            Moderateurs = "<font color='#C565FE'>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </font>"
                    if Moderateurs != "":
                        Moderateurs = Moderateurs.rstrip("\n")
                        self.client.sendMessage(Moderateurs)
                    else:
                        self.client.sendMessage("<V>[•]</V> Don't have any online Moderators at moment.")

            elif command in ["mm"]:
                if self.client.privLevel >= 8:
                    self.client.room.sendAll(Identifiers.send.Staff_Chat, ByteArray().writeByte(0).writeUTF("").writeUTF(argsNotSplited).writeShort(0).writeByte(0).toByteArray())
            
            elif command in ["clearchat"]:
                if self.client.privLevel >= 8:
                    self.client.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("\n" * 10000).toByteArray())

            elif command in ["playerping"]:
                if self.client.privLevel >= 8 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    player = self.server.players.get(playerName)
                    if player != None:
                        self.client.sendMessage("<V>[•]</V> <V>%s</V> -> %s" %(playerName, self.client.getPing(player.ipAddress)))
                    else:
                        self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid nickname.")

            elif command in ["moveplayer"]:
                if self.client.privLevel >= 8 and self.requireArguments(2):
                    playerName = Utils.parsePlayerName(args[0])
                    roomName = argsNotSplited.split(" ", 1)[1]
                    player = self.server.players.get(playerName)
                    if player != None:
                        newRoom = player.room.name
                        player.enterRoom(roomName)
                        self.client.sendServerMessage(player.playerName+" has been moved from ("+str.lower(newRoom)+") to ("+str.lower(player.room.name)+")  by "+self.client.playerName+".")
                    else:
                        self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid nickname.")

            elif command in ["removeplayerrecords"]:
                if self.client.privLevel >= 8 and self.requireArguments(1):
                    try:
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
                            self.client.sendServerMessage("The %s's records were removed by %s." %(playerName, self.client.playerName))
                    except:
                        pass

            elif command in ["arb"]:
                if self.client.privLevel >= 8 and self.requireArguments(1):
                    player = self.server.players.get(Utils.parsePlayerName(args[0]))
                    if player != None:
                        if self.server.getPlayerPrivlevel(player.playerName) == 7:
                            self.Cursor.execute("UPDATE users SET PrivLevel = 1 WHERE Username = '%s' " % (player.playerName))
                            player.privLevel = 1
                            player.updateDatabase()
                            self.client.sendServerMessage(player.playerName+" is not arbitre / moderator anymore.")
                            
                        else:
                            self.Cursor.execute("UPDATE users SET PrivLevel = 7 WHERE Username = '%s' " % (player.playerName))
                            player.privLevel = 7
                            player.updateDatabase()
                            self.client.sendServerMessage("New arbitre : "+player.playerName)

            elif command in ["max"]:
                if self.client.privLevel >= 8:
                    self.client.sendMessage("<V>[•]</v> Maximum Players: <VP>"+str(self.server.MaximumPlayers)+"</VP>.")

# Admins Commands

            elif command in ["move"]:
                if self.client.privLevel >= 9:
                    for player in [*self.client.room.clients.values()]:
                        player.enterRoom(argsNotSplited)

            elif command in ["updatesql"]:
                if self.client.privLevel >= 9:
                    for player in self.server.players.values():
                        player.updateDatabase()
                    self.client.sendServerMessageAdmin("The database was updated by %s."%(self.client.playerName))

            elif command in ["smc"]:
                if self.client.privLevel >= 9:
                    for player in self.server.players.values():
                        player.sendMessage("<font color = '#12DA8A'>• [%s] %s</font>" % (self.client.playerName, argsNotSplited))

            elif command in ["re","respawn"]:
                if self.client.privLevel >= 9:
                    if len(args) == 0:
                        if not self.client.canRespawn:
                            self.client.room.respawnSpecific(self.client.playerName)
                            self.client.canRespawn = True
                            self.client.sendMessage("<V>[•]</V> Successfull respawned yourself.")
                    elif len(args) == 1:
                        playerName = Utils.parsePlayerName(args[0])
                        if playerName in self.client.room.clients:
                            self.client.room.respawnSpecific(playerName)
                            self.client.sendMessage("<V>[•]</V> Successfull respawned "+str(playerName)+".")
                    else:
                        pass

            elif command in ["settime"]:
                if self.client.privLevel >= 9 and self.requireArguments(1):
                    time = args[0]
                    iTime = int(time)
                    iTime = 5 if iTime < 5 else (32767 if iTime > 32767 else iTime)
                    for player in self.client.room.clients.values():
                        player.sendRoundTime(iTime)
                    self.client.room.changeMapTimers(iTime)
                    self.client.sendMessage("<V>[•]</V> Successfull added "+str(iTime)+" seconds to current round.")

            elif command in ["changemapname"]:
                if self.client.privLevel >= 9 and self.requireArguments(2):
                    playerName = Utils.parsePlayerName(args[0])
                    code = args[1]
                    if code.isdigit():
                        mapInfo = self.client.room.getMapInfo(int(code[1:]))
                        if mapInfo[0] == None:
                            self.client.sendLangueMessage("", "$CarteIntrouvable")
                        else:
                            self.client.room.CursorMaps.execute("update Maps set Name = ? where Code = ?", [playerName, code])
                            self.client.sendServerMessageAdmin("The map <J>@"+code+"</J>'s name was changed to <V>"+playerName+"</V>.")
                    else:
                        self.client.sendMessage("<V>[•]</V> The code must be integer.")

            elif command in ["commandlog"]:
                if self.client.privLevel >= 9 and self.requireArguments(1):
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

            elif command in ["anim"]:
                if self.client.privLevel >= 9 and self.requireArguments(3):
                    playerName = Utils.parsePlayerName(args[0])
                    anim = args[1]
                    frame = int(args[2])
                    player = self.client.room.clients.get(playerName)
                    if player != None:
                        self.client.room.sendAll(Identifiers.send.Add_Anim, ByteArray().writeInt(player.playerCode).writeUTF(anim).writeShort(frame).toByteArray())

            elif command in ["frame"]:
                if self.client.privLevel >= 9 and self.requireArguments(4):
                    playerName = Utils.parsePlayerName(args[0])
                    frame = args[1]
                    xPosition = int(args[2])
                    yPosition = int(args[3])
                    player = self.client.room.clients.get(playerName)
                    if player != None:
                        self.client.room.sendAll(Identifiers.send.Add_Frame, ByteArray().writeInt(player.playerCode).writeUTF(frame).writeInt(xPosition).writeInt(yPosition).toByteArray())

            elif command in ["resetprofile"]:
                if self.client.privLevel >= 9 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    player = self.server.players.get(playerName)
                    if player != None:
                        self.Cursor.execute(f"UPDATE Users SET FirstCount = 0, CheeseCount = 0, ShamanSaves = 0, HardModeSaves = 0, DivineModeSaves = 0, BootcampCount = 0, ShamanCheeses = 0, Badges = 0, ShamanLevel = 0, ShamanExp = 0, Consumables = '', Pet = '', ShamanBadges = '', Badges = '{'{}'}', Karma = 0, ShopCheeses = 0, ShopFraises = 0  WHERE PlayerID = {self.server.getPlayerID(player.playerName)}")
                        self.client.sendServerMessageAdmin(self.client.playerName + " reseted the profile of the player " + playerName + "<BL>.")
                        #player.updateDatabase()
                        player.room.removeClient(player)
                        player.transport.close()
                    else:
                        self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid nickname.")

            elif command in ["harddel"]:
                if self.client.privLevel >= 9:
                    if len(args) == 1:
                        mapCode = args[0]
                        mapCode = mapCode.replace('@', '')
                        if mapCode != -1:
                            self.client.room.CursorMaps.execute("delete from Maps where Code = ?", [mapCode])
                            self.client.sendMessage("<V>[•]</V> Successfull deleted the map: @"+str(mapCode)+" from database.")
                    elif len(args) == 0:
                        mapCode = self.client.room.mapCode
                        if mapCode != -1:
                            self.client.room.CursorMaps.execute("delete from Maps where Code = ?", [mapCode])
                            self.client.sendMessage("<V>[•]</V> Successfull deleted the map: @"+str(mapCode)+" from database.")
                    else:
                        pass

            elif command in ["addcode"]:
                if self.client.privLevel >= 9 and self.requireArguments(3):
                    data = json.loads(open('./include/json/codes.json','r').read())
                    name = args[0]
                    T = args[1]
                    amount = int(args[2])
                    if T == "fraises" or T == "cheeses":
                        if isinstance(amount, int) == True:
                            data['codes'].append({'name': name, 'type': T, 'amount': amount, 'havegot': 0})
                            with open('./include/json/codes.json', 'w') as F:
                                json.dump(data, F)
                        else:
                            self.client.sendMessage("<V>[•]</V> The amount must be integer.")
                    else:
                        self.client.sendMessage("<V>[•]</V> The type of code is invalid.")

# Owner Commands:
            elif command in ["luaadmin"]:
                if self.client.playerName in self.owners:
                    self.client.isLuaAdmin = not self.client.isLuaAdmin
                    self.client.sendMessage("<V>[•]</V> You can run lua programming as administrator." if self.client.isLuaAdmin else "<V>[•]</V> You can't run lua programming as administrator.")

            elif command in ["serverconfigs"]:
                if self.client.playerName in self.owners:
                    with open("./include/configs.properties", 'r') as File:
                        Log = File.read()
                        File.close()
                    self.client.sendLogMessage(Log.replace("<", "&amp;lt;").replace("\x0D\x0A", "\x0A"))

            elif command in ["reboot"]:
                if self.client.playerName in self.owners:
                    self.server.sendServerRestart(0, 0)
                    
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
                        self.Cursor.execute("DELETE FROM bmlog")
                        self.Cursor.execute("DELETE FROM banlog")
                        self.Cursor.execute("DELETE FROM ippermaban")
                        self.Cursor.execute("DELETE FROM userpermaban")
                        self.Cursor.execute("DELETE FROM usertempban")
                        self.client.sendServerMessageAdmin("The player %s cleared casier database." %(self.client.playerName))
                    elif args[0] == "loginlog":
                        self.Cursor.execute("DELETE FROM loginlog")
                        self.Cursor.execute("DELETE FROM loginlogs")
                        self.client.sendServerMessageAdmin("The player %s cleared loginlog database." %(self.client.playerName))
                    elif args[0] == "commandlog":
                        self.Cursor.execute("DELETE FROM commandlog")
                        self.client.sendServerMessageAdmin("The player %s cleared commandlog database." %(self.client.playerName))

            elif command in ["shutdown"]:
                if self.client.playerName in self.owners:
                    self.server.closeServer()

            elif command in ["viewlog"]:
                if self.client.playerName in self.owners and self.requireArguments(1):
                    if args[0] == "errors":
                        with open("./include/logs/Errors/Tribulle.log", 'r') as File:
                            Log = File.read()
                            File.close()
                        self.client.sendLogMessage(Log.replace("<", "&amp;lt;").replace("\x0D\x0A", "\x0A"))
                        with open("./include/logs/Errors/Commands.log", 'r') as File:
                            Log = File.read()
                            File.close()
                        self.client.sendLogMessage(Log.replace("<", "&amp;lt;").replace("\x0D\x0A", "\x0A"))
                        with open("./include/logs/Errors/Server.log", 'r') as File:
                            Log = File.read()
                            File.close()
                        self.client.sendLogMessage(Log.replace("<", "&amp;lt;").replace("\x0D\x0A", "\x0A"))
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

            elif command in ["delete"]:
                if self.client.playerName in self.owners and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])        
                    if self.server.checkExistingUser(playerName):
                        self.Cursor.execute("delete from Users where Username = %s", [playerName])
                        self.client.sendServerMessageAdmin("The account %s is deleted by %s" % (playerName, self.client.playerName))
                    else:
                        self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid nickname.")

            elif command in ["reset"]:
                if self.client.playerName in self.owners and self.requireArguments(1):
                    if args[0] == "fastracing":
                        self.client.room.CursorMaps.execute("update Maps set Time = ?, Player = ?, RecDate = ?", [0, "", 0])
                        self.client.sendServerMessageAdmin("All records of fastracing was deleted by %s."%(self.client.playerName))
                    elif args[0] == "deathcounts":
                        self.Cursor.execute("update Users set deathCount = %s", [0])
                        self.client.sendServerMessageAdmin("<V>[•]</V> All deathcounts was reset by %s."%(self.client.playerName)) 

            elif command in ["reload"]:
                #if self.client.playerName in self.owners:
                try:
                    self.server.reloadServer()
                    self.client.sendMessage("<V>[•]</V> Successfull reloaded all modules.")
                except:
                    self.client.sendMessage("<V>[•]</V> Failed reload all modules.")
                        
            elif command in ["changepassword"]:
                if self.client.playerName in self.owners and self.requireArguments(2):
                    playerName = Utils.parsePlayerName(args[0])
                    password = args[1]
                    player = self.server.players.get(playerName)
                    if player != None:
                        salt = b'\xf7\x1a\xa6\xde\x8f\x17v\xa8\x03\x9d2\xb8\xa1V\xb2\xa9>\xddC\x9d\xc5\xdd\xceV\xd3\xb7\xa4\x05J\r\x08\xb0'
                        hashtext = base64.b64encode(hashlib.sha256(hashlib.sha256(password.encode()).hexdigest().encode() + salt).digest()).decode()
                        player.updateDatabase()
                        self.Cursor.execute(f"UPDATE Users SET Password = '{hashtext}' WHERE Username = '{playerName}'")
                        player.room.removeClient(player)
                        player.transport.close()
                    else:
                        self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid nickname.")
         
            elif command in ["colornick"]:
                if(self.client.privLevel in [5, 9] or self.client.room.roomName == "*strm_" + self.client.playerName.lower() or self.client.isFuncorpPlayer == True) and self.requireArguments(2):
                    if self.client.room.isFuncorp:
                        playerName = Utils.parsePlayerName(args[0])
                        if len(args) == 1:
                            if playerName != "*":
                                player = self.server.players.get(playerName)
                                if player != None:
                                    self.client.room.showColorPicker(10000, player.playerName, int(player.mouseColor, 16), "Select a color for your name.")
                        else:
                            color = args[1]
                            if playerName != "*":
                                player = self.server.players.get(playerName)
                                if player != None:
                                    player.funcorpcolornick = color
                                    self.client.room.setNameColor(player.playerName, color)
                    else:
                        self.client.sendMessage("<V>[•]</V> FunCorp commands only work when the room is in FunCorp mode.")

# Predefined Commands in swf.
            elif command in ["codecadeau"]: #It executes when player use /code. 
                if self.client.privLevel >= 1 and self.requireArguments(1):
                    d = json.loads(open('./include/json/codes.json','r').read())
                    try:
                        for i in d['codes']:
                            if args[0].lower() == i['name'] and i['havegot'] == 0:
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
                        self.client.updateDatabase()
                        with open('./include/json/codes.json', 'w') as F:
                            json.dump(d, F)
                    except:
                        pass
                        
        except Exception as e:
            import time, traceback
            c = open("./include/logs/Errors/Commands.log", "a")
            c.write("\n" + "=" * 60 + "\n- Time: %s\n- Name: %s\n- Error Command: \n" %(time.strftime("%d/%m/%Y - %H:%M:%S"), self.client.playerName))
            traceback.print_exc(file=c)
            c.close()
            self.client.sendServerMessageAdmin("<BL>[<R>ERROR<BL>] The user <R>%s</R> used error command [%s]." %(self.client.playerName, time.strftime("%d/%m/%Y - %H:%M:%S")))
            
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
        message += "<J>/playmusic</J> <VP>[MP3_URL]</VP> - <BL> Start playing music in the room.\n"
        return message