#coding: utf-8
import re, sys, json, os, base64, hashlib, time, random, traceback
"""
9 Admin, 8 Mod, 7 Arb, 6 MC, 5 FC, 4 LC, 3 - FS, 2 Sentinel, 1 PPL
Commands: /relation, /harddel, /sondage, /arb, /resign
"""
# Modules
from time import gmtime, strftime
from langues import Langues
from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers

# Library
from datetime import datetime

class Commands:
    def __init__(self, client, server):
        self.client = client
        self.server = client.server
        self.Cursor = client.Cursor
        self.currentArgsCount = 0
        self.owners = []

    def requireTribe(self, canUse=False, tribePerm = 8):
        if (not(not self.client.tribeName == "" and self.client.room.isTribeHouse and tribePerm != -1 and self.client.tribeRanks[self.client.tribeRank].split("|")[2].split(",") [tribePerm] == "1")):
            canUse = True
    
    def requireArguments(self, arguments):
        if self.currentArgsCount < arguments:
            self.client.sendMessage("<V>[•]</V> You need more arguments to use this command.")
            return False
        elif self.currentArgsCount == arguments:
            return True
        else:
            return False
    
    def requireArgumentsUpper(self, arguments):
        if self.currentArgsCount < arguments:
            self.client.sendMessage("<V>[•]</V> You need more arguments to use this command.")
            return False
        elif self.currentArgsCount == arguments:
            return True
        else:
            return True
    
    def parseCommand(self, command):                
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
            if command in ["profile", "profil"]:
                if self.client.privLevel >= 1:
                    self.client.sendProfile(Utils.parsePlayerName(args[0]) if len(args) >= 1 else self.client.playerName)
			
            elif command in ["editeur", "editor"]:
                if self.client.privLevel >= 1:
                    self.client.sendPacket(Identifiers.send.Room_Type, 1)
                    self.client.enterRoom("\x03[Editeur] %s" %(self.client.playerName))
                    self.client.sendPacket(Identifiers.old.send.Map_Editor, [])

            elif command in ["totem"]:
                if self.client.privLevel >= 1:
                    if self.client.shamanSaves >= 100:
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
                        if player.privLevel in [8] and not player.privLevel in [2,3,4,5,6,7,9]:
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
                        if player.privLevel in [6] or player.isMapCrew == True and not player.privLevel in [2,3,4,5,8,7,9]:
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
                    if self.client.room.roomName.startswith("*") or self.client.room.roomName.startswith(self.client.playerName):
                        if len(args) == 0:
                            self.client.room.roomPassword = ""
                            self.client.sendLangueMessage("", "$MDP_Desactive")
                        else:
                            password = args[0]
                            self.client.room.roomPassword = password
                            self.client.sendLangueMessage("", "$Mot_De_Passe : %s" %(password))

            elif command in ["lb"]:
                if self.client.room.isSpeedRace and self.client.privLevel >= 1:
                    self.client.sendLeaderBoard()

            elif command in ["ds"]:
                if self.client.room.isDeathmatch and self.client.privLevel >= 1:
                    self.client.sendDeathBoard()
            
            elif command in ["title", "titulo", "titre"]:
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
                    self.client.Packets.packets = []

            elif command in ["skip"]:
                if self.client.privLevel >= 1 and self.client.canSkipMusic and self.client.room.isMusic and self.client.room.isPlayingMusic:
                    self.client.room.musicSkipVotes += 1
                    self.client.checkMusicSkip()
                    self.client.sendBanConsideration()

            elif command in ["mjj"]:
                roomName = args[0]
                if roomName.startswith("#"):
                    if roomName.startswith("#utility"):
                        self.client.enterRoom(roomName)
                    else:
                        self.client.enterRoom(roomName + "1")
                else:
                    self.client.enterRoom(({0:"", 1:"", 3:"vanilla", 8:"survivor", 9:"racing", 11:"music", 2:"bootcamp", 10:"defilante", 16:"village"}[self.client.lastGameMode]) + roomName)
                self.client.Packets.packets = []
                
            elif command in ["bootcamp", "vanilla", "survivor", "racing", "defilante", "tutorial"]:
                self.client.enterRoom("bootcamp1" if command == "bootcamp" else "vanilla1" if command == "vanilla" else "survivor1" if command == "survivor" else "racing1" if command == "racing" else "defilante1" if command == "defilante" else (chr(3) + "[Tutorial] " + self.client.playerName) if command == "tutorial" else "Sourimenta" + self.client.playerName)

            elif command in ["ping"]:
                if self.client.privLevel >= 1:
                    self.client.sendMessage("<V>[•]</V> %s" % (str(self.client.PInfo[2])))

            elif command in ["defrecs"]:
                if self.client.privLevel >= 1 and self.client.room.isBigdefilante:
                    mapList = ""
                    records = 0
                    self.client.room.CursorMaps.execute("select * from Maps where BDTimeNick = ?", [self.client.playerName])
                    for rs in self.client.room.CursorMaps.fetchall():
                        bestTime = rs["BDTime"]
                        records += 1
                        rec = bestTime * 0.01
                        mapList += "\n<font color='#F272A5'>%s</font> - <font color='#9a9a9a'>@%s</font> - <font color='#F272A5'>%s</font><font color='#9a9a9a'>%s</font>" %(rs["BDTimeNick"], rs["Code"], rec, "s")
                    try: self.client.sendLogMessage("<p align='center'><font color='#F272A5'>Records</font><BV>:</BV> <font color='#9a9a9a'>%s</font>\n%s</p>" %(records, mapList))
                    except: self.client.sendLogMessage("<R>So much records.</R>")

            elif command in ["pink"]:
                if self.client.privLevel >= 1:
                    self.client.room.sendAll(Identifiers.send.Player_Damanged, ByteArray().writeInt(self.client.playerCode).toByteArray()) 

# Tribe Commands:
            elif command in ["inv"]:
                if self.client.privLevel >= 1 and self.requireArguments(1):
                    if self.client.room.isTribeHouse:
                        playerName = Utils.parsePlayerName(args[0])
                        if self.server.checkConnectedAccount(playerName) and not playerName in self.client.tribulle.getTribeMembers(self.client.tribeCode):
                            player = self.server.players.get(playerName)
                            player.invitedTribeHouses.append(self.client.tribeName)
                            player.sendPacket(Identifiers.send.Tribe_Invite, ByteArray().writeUTF(self.client.playerName).writeUTF(self.client.tribeName).toByteArray())
                            self.client.sendLangueMessage("", "$InvTribu_InvitationEnvoyee", "<V>" + player.playerName + "</V>")
                        else:
                            self.client.sendMessage("<V>[•]</V> The username isn't online or you can't invite member from your own tribe.")
                    else:
                        self.client.sendMessage("<V>[•]</V> You need go to in your tribe for use this command.")

            elif command in ["invkick"]:
                if self.client.privLevel >= 1 and self.requireArguments(1):
                    if self.client.room.isTribeHouse:
                        playerName = Utils.parsePlayerName(args[0])
                        if self.server.checkConnectedAccount(playerName) and not playerName in self.client.tribulle.getTribeMembers(self.client.tribeCode):
                            player = self.server.players.get(playerName)
                            if self.client.tribeName in player.invitedTribeHouses:
                                player.invitedTribeHouses.remove(self.client.tribeName)
                                self.client.sendLangueMessage("", "$InvTribu_AnnulationEnvoyee", "<V>" + player.playerName + "</V>")
                                player.sendLangueMessage("", "$InvTribu_AnnulationRecue", "<V>" + self.client.playerName + "</V>")
                                if player.roomName == "*" + chr(3) + self.client.tribeName:
                                    player.enterRoom(self.server.recommendRoom(self.client.langue))
                        else:
                            self.client.sendMessage("<V>[•]</V> The username isn't online or you can't invite member from your own tribe.")
                    else:
                        self.client.sendMessage("<V>[•]</V> You need go to in your tribe for use this command.")

            elif command in ["neige"]:
                if self.client.privLevel >= 1 and self.client.room.isTribeHouse:
                    if self.client.room.isSnowing:
                        self.client.room.startSnow(0, 0, not self.client.room.isSnowing)
                        self.client.room.isSnowing = False
                    else:
                        self.client.room.startSnow(1000, 60, not self.client.room.isSnowing)
                        self.client.room.isSnowing = True

# Lua Commands
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
                        if "LuaCrew" in player.roles and not player.playerName.startswith('*') or player.isLuaCrew:
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
                    for player in self.server.players.values(): # if player has role LuaCrew
                        if "FashionSquad" in player.roles and not player.playerName.startswith('*') or player.isFashionSquad:
                            FS += "<font color='#ffb6c1'>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </font><br>"
                    if FS != "":
                        FS = FS.rstrip("\n")
                        self.client.sendMessage(FS)
                    else:
                        self.client.sendMessage("<V>[•]</V> Don't have any online Fashion Squads at moment.")

# Funcorp Commands:
            elif command in ["lsfc"]:
                if (self.client.privLevel in [5, 9] or self.client.isFuncorpPlayer == True):
                    FunCorps = ""
                    self.Cursor.execute("select Username from Users where PrivLevel = %s", [5])
                    r = self.Cursor.fetchall()
                    for rs in r:
                        player = self.server.players.get(rs[0])
                        if player != None:
                            FunCorps += "<FC>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </FC><br>"
                    for player in self.server.players.values(): # if player has role LuaCrew
                        if "FunCorp" in player.roles and not player.playerName.startswith('*') or player.isFuncorpPlayer:
                            FunCorps += "<FC>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </FC><br>"
                    if FunCorps != "":
                        FunCorps = FunCorps.rstrip("\n")
                        self.client.sendMessage(FunCorps)
                    else:
                        self.client.sendMessage("<V>[•]</V> Don't have any online Fun Corps at moment.")

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
                                self.client.sendMessage("<V>[•]</V> The following player has changed his nickname to default: <BV>"+ str(player.playerName) +"</BV>")
                            else:
                                player.mouseName = newName
                                self.client.room.funcorpNames[player.playerName] = newName
                                self.client.sendMessage("<V>[•]</V> The following player has changed his nickname: <BV>"+ str(player.playerName) +"</BV>")
                    else:
                        self.client.sendMessage("<V>[•]</V> FunCorp commands only work when the room is in FunCorp mode.")
                        
            elif command in ["changesize"]:
                if (self.client.privLevel in [5, 9] or self.client.room.roomName == "*strm_" + self.client.playerName.lower() or self.client.isFuncorpPlayer == True) and self.requireArguments(2):
                    if self.client.room.isFuncorp:
                        playerName = Utils.parsePlayerName(args[0])
                        self.client.playerSize = 1.0 if args[1] == "off" else (99999.0 if float(args[1]) > 9999.0 else float(args[1]))
                        if args[1] == "off":
                            if playerName == "*":
                                for player in self.client.room.clients.values():
                                    self.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(int(self.client.playerSize * 100)).writeBoolean(False).toByteArray())
                                self.client.sendMessage("<V>[•]</V> All players now have their regular size.")
                            else:
                                player = self.server.players.get(playerName)
                                if player != None:
                                    self.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(int(self.client.playerSize * 100)).writeBoolean(False).toByteArray())
                                    self.client.sendMessage("<V>[•]</V> The following player now have the regular size: <BV>" + str(player.playerName) + "</BV>")
                        elif self.client.playerSize >= float(0.1) or self.client.playerSize <= float(5.0):
                            if playerName == "*":
                                for player in self.client.room.clients.values():
                                    self.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(int(self.client.playerSize * 100)).writeBoolean(False).toByteArray())
                                self.client.sendMessage("<V>[•]</V> All players now have the same size: <BV>" + str(self.client.playerSize) + "</BV>.")
                            else:
                                player = self.server.players.get(playerName)
                                if player != None:
                                    self.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(int(self.client.playerSize * 100)).writeBoolean(False).toByteArray())
                                    self.client.sendMessage("<V>[•]</V> The following player have the new size " + str(self.client.playerSize) + ": <BV>" + str(player.playerName) + "</BV>")
                    else:
                        self.client.sendMessage("<V>[•]</V> FunCorp commands only work when the room is in FunCorp mode.")

            elif command in ["funcorp"]:
                if (self.client.privLevel in [5, 9] or self.client.room.roomName == "*strm_" + self.client.playerName.lower() or self.client.isFuncorpPlayer == True):
                    if len(args) == 0:
                        if self.client.room.isFuncorp:
                            for player in self.client.room.clients.values():
                                player.sendLangueMessage("", "<FC>$FunCorpDesactive</FC>")
                                self.client.room.isFuncorp = False
                                player.mouseName = ""
                                player.nickColor = "#95d9d6"
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
                   
            elif command in ["transformation"]:
                if(self.client.privLevel in [5, 9] or self.client.room.roomName == "*strm_" + self.client.playerName.lower()) and self.requireArguments(1):
                    if self.client.room.isFuncorp:
                        playerName = Utils.parsePlayerName(args[0])
                        if playerName == "*":
                            for player in self.client.room.clients.values():
                                player.sendPacket([27, 10], 1)
                        else:
                            player = self.server.players.get(playerName)
                            if player != None:
                                player.sendPacket([27, 10], 1)
                    else:
                        self.client.sendMessage("<V>[•]</V> FunCorp commands only work when the room is in FunCorp mode.")

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
                            self.client.sendMessage("<V>[•]</V> The number of Maximum players is invalid.")

            elif command in ["meep"]:
                if (self.client.privLevel in [5, 9] or self.client.room.roomName == "*strm_" + self.client.playerName.lower() or self.client.isFuncorpPlayer == True):
                    if self.client.room.isFuncorp:
                        playerName = Utils.parsePlayerName(args[0])
                        if playerName == "*":
                            for player in self.client.room.clients.values():
                                player.sendPacket(Identifiers.send.Can_Meep, 1)
                                self.client.sendMessage("<V>[•]</V> Successfull given the ability meep to all players.")
                        else:
                            player = self.server.players.get(playerName)
                            if player != None:
                                player.sendPacket(Identifiers.send.Can_Meep, 1)
                                self.client.sendMessage("<V>[•]</V> Successfull given the ability meep to following player: <BV>"+ str(player.playerName) +"</BV>")
                    
                        if args[1] == "off":
                            if playerName == "*":
                                for player in self.client.room.clients.values():
                                    player.sendPacket(Identifiers.send.Can_Meep, 0)
                                    self.client.sendMessage("<V>[•]</V> Successfull revoked the ability meep to all players.")
                            else:
                                player = self.server.players.get(playerName)
                                if player != None:
                                    player.sendPacket(Identifiers.send.Can_Meep, 0)
                                    self.client.sendMessage("<V>[•]</V> Successfull revoked the ability meep to following player: <BV>"+ str(player.playerName) +"</BV>")
                                
                    else:
                        self.client.sendMessage("<V>[•]</V> FunCorp commands only work when the room is in FunCorp mode.")

            elif command in ["linkmice"]: 
                if (self.client.privLevel in [5, 9] or self.client.room.roomName == "*strm_" + self.client.playerName.lower() or self.client.isFuncorpPlayer == True) and self.requireArguments(2):
                    if self.client.room.isFuncorp:
                        playerName = Utils.parsePlayerName(args[0])
                        playerName2 = Utils.parsePlayerName(args[1])
                        if args[1] == "off":
                            player = self.client.room.clients.get(playerName)
                            if player != None:
                                self.client.room.sendAll(Identifiers.send.Soulmate, ByteArray().writeBoolean(False).writeInt(player.playerCode).toByteArray())
                                self.client.sendMessage('<V>[•]</V> The links involving the following players have been removed: <MC>'+player+'</MC>')
                        else:
                            player = self.client.room.clients.get(playerName)
                            if player != None:
                                if playerName2 == "*":
                                    for player2 in self.client.room.clientsvalues():
                                        self.client.room.sendAll(Identifiers.send.Soulmate, ByteArray().writeBoolean(True).writeInt(player.playerCode).writeInt(player2.playerCode).toByteArray())
                                        self.client.sendMessage("<V>[•]</V> The following players are now linked: <MC>"+player+', *</MC>')
                                else:
                                    player2 = self.client.room.clients.get(playerName2)
                                    if player2 != None:
                                        self.client.room.sendAll(Identifiers.send.Soulmate, ByteArray().writeBoolean(True).writeInt(player.playerCode).writeInt(player2.playerCode).toByteArray())
                                        self.client.sendMessage("<V>[•]</V> The following players are now linked: <MC>"+player+', '+player2+'</MC>')
                    else:
                        self.client.sendMessage("<V>[•]</V> FunCorp commands only work when the room is in FunCorp mode.")

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
                        self.client.sendMessage("<V>[•]</V> FunCorp commands only work when the room is in FunCorp mode.")

            elif command in ["image"]:
                if (self.client.privLevel in [5, 9] or self.client.room.roomName == "*strm_" + self.client.playerName.lower() or self.client.isFuncorpPlayer == True) and self.requireArguments(4):
                    if self.client.room.isFuncorp:
                        imageName = args[0]
                        target = Utils.parsePlayerName(args[1])
                        xPosition = int(args[2]) if args[2].isdigit() else 0
                        yPosition = int(args[3]) if args[3].isdigit() else 0

                        if target.lower() in ["$all", "%all"]:
                            for player in self.client.room.clientsvalues():
                                self.client.room.addImage(imageName, target[0] + player.playerName, xPosition, yPosition, "")
                        else:
                            self.client.room.addImage(imageName, target, xPosition, yPosition, "")
                    else:
                        self.client.sendMessage("<V>[•]</V> FunCorp commands only work when the room is in FunCorp mode.")

            elif command in ["playmusic", "musique", "music"]:
                if (self.client.privLevel in [5, 9] or self.client.isFuncorpPlayer == True) or self.client.room.isTribeHouse:
                    if len(args) == 0:
                        self.client.room.sendAll(Identifiers.old.send.Music, [])
                    else:
                        self.client.room.sendAll(Identifiers.old.send.Music, [args[0]])

            elif command in ["changepoke"]:
                if(self.client.privLevel in [5, 9] or self.client.room.roomName == "*strm_" + self.client.playerName.lower() or self.client.isFuncorpPlayer == True) and self.requireArguments(2):
                    if self.client.room.isFuncorp:
                        playerName = Utils.parsePlayerName(args[0])
                        player = self.server.players.get(playerName)
                        skins = {0: '1534bfe985e.png', 1: '1507b2e4abb.png', 2: '1507bca2275.png', 3: '1507be4b53c.png', 4: '157f845d5fa.png', 5: '1507bc62345.png', 6: '1507bc98358.png', 7: '157edce286a.png', 8: '157f844c999.png', 9: '157de248597.png', 10: '1507b944d89.png', 11: '1507bcaf32c.png', 12: '1507be41e49.png', 13: '1507bbe8fe3.png', 14: '1507b8952d3.png', 15: '1507b9e3cb6.png', 16: '1507bcb5d04.png', 17: '1507c03fdcf.png', 18: '1507bee9b88.png', 19: '1507b31213d.png', 20: '1507b4f8b8f.png', 21: '1507bf9015d.png', 22: '1507bbf43bc.png', 23: '1507ba020d2.png', 24: '1507b540b04.png', 25: '157d3be98bd.png', 26: '1507b75279e.png', 27: '1507b921391.png', 28: '1507ba14321.png', 29: '1507b8eb323.png', 30: '1507bf3b131.png', 31: '1507ba11258.png', 32: '1507b8c6e2e.png', 33: '1507b9ea1b4.png', 34: '1507ba08166.png', 35: '1507b9bb220.png', 36: '1507b2f1946.png', 37: '1507b31ae1f.png', 38: '1507b8ab799.png', 39: '1507b92a559.png', 40: '1507b846ea8.png', 41: '1507bd2cd60.png', 42: '1507bd7871c.png', 43: '1507c04e123.png', 44: '1507b83316b.png', 45: '1507b593a84.png', 46: '1507becc898.png', 47: '1507befa39f.png', 48: '1507b93ea3d.png', 49: '1507bd14e17.png', 50: '1507bec1bd2.png'}
                        number = float(args[1])
                        if args[1] == "off":
                            self.client.sendMessage("<V>[•]</V> All players back to normal size.")
                            skin = skins[int(number)]
                            p = ByteArray()
                            p.writeInt(0)
                            p.writeUTF(skin)
                            p.writeByte(3)
                            p.writeInt(player.playerCode)
                            p.writeShort(-30)
                            p.writeShort(-35)
                            self.client.room.sendAll([29, 19], p.toByteArray())
                            self.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(float(1)).writeBoolean(False).toByteArray())
                        elif number >= 0:
                            if playerName == "*":
                                for player in self.client.room.clients.values():
                                    skins = {0: '1534bfe985e.png', 1: '1507b2e4abb.png', 2: '1507bca2275.png', 3: '1507be4b53c.png', 4: '157f845d5fa.png', 5: '1507bc62345.png', 6: '1507bc98358.png', 7: '157edce286a.png', 8: '157f844c999.png', 9: '157de248597.png', 10: '1507b944d89.png', 11: '1507bcaf32c.png', 12: '1507be41e49.png', 13: '1507bbe8fe3.png', 14: '1507b8952d3.png', 15: '1507b9e3cb6.png', 16: '1507bcb5d04.png', 17: '1507c03fdcf.png', 18: '1507bee9b88.png', 19: '1507b31213d.png', 20: '1507b4f8b8f.png', 21: '1507bf9015d.png', 22: '1507bbf43bc.png', 23: '1507ba020d2.png', 24: '1507b540b04.png', 25: '157d3be98bd.png', 26: '1507b75279e.png', 27: '1507b921391.png', 28: '1507ba14321.png', 29: '1507b8eb323.png', 30: '1507bf3b131.png', 31: '1507ba11258.png', 32: '1507b8c6e2e.png', 33: '1507b9ea1b4.png', 34: '1507ba08166.png', 35: '1507b9bb220.png', 36: '1507b2f1946.png', 37: '1507b31ae1f.png', 38: '1507b8ab799.png', 39: '1507b92a559.png', 40: '1507b846ea8.png', 41: '1507bd2cd60.png', 42: '1507bd7871c.png', 43: '1507c04e123.png', 44: '1507b83316b.png', 45: '1507b593a84.png', 46: '1507becc898.png', 47: '1507befa39f.png', 48: '1507b93ea3d.png', 49: '1507bd14e17.png', 50: '1507bec1bd2.png'}
                                    number = args[1]
                                    
                                    if int(number) in skins:
                                        #self.client.useAnime += 1
                                        skin = skins[int(number)]
                                        p = ByteArray()
                                        p.writeInt(0)
                                        p.writeUTF(skin)
                                        p.writeByte(3)
                                        p.writeInt(player.playerCode)
                                        p.writeShort(-30)
                                        p.writeShort(-35)
                                        self.client.room.sendAll([29, 19], p.toByteArray())
##                                        self.client.sendMessage("All players skin: " + str(skin) + ".")
                                    #self.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(int(self.client.playerSize * 100)).writeBoolean(False).toByteArray())
                            else:
                                player = self.server.players.get(playerName)
                                if player != None:
                                    skins = {0: '1534bfe985e.png', 1: '1507b2e4abb.png', 2: '1507bca2275.png', 3: '1507be4b53c.png', 4: '157f845d5fa.png', 5: '1507bc62345.png', 6: '1507bc98358.png', 7: '157edce286a.png', 8: '157f844c999.png', 9: '157de248597.png', 10: '1507b944d89.png', 11: '1507bcaf32c.png', 12: '1507be41e49.png', 13: '1507bbe8fe3.png', 14: '1507b8952d3.png', 15: '1507b9e3cb6.png', 16: '1507bcb5d04.png', 17: '1507c03fdcf.png', 18: '1507bee9b88.png', 19: '1507b31213d.png', 20: '1507b4f8b8f.png', 21: '1507bf9015d.png', 22: '1507bbf43bc.png', 23: '1507ba020d2.png', 24: '1507b540b04.png', 25: '157d3be98bd.png', 26: '1507b75279e.png', 27: '1507b921391.png', 28: '1507ba14321.png', 29: '1507b8eb323.png', 30: '1507bf3b131.png', 31: '1507ba11258.png', 32: '1507b8c6e2e.png', 33: '1507b9ea1b4.png', 34: '1507ba08166.png', 35: '1507b9bb220.png', 36: '1507b2f1946.png', 37: '1507b31ae1f.png', 38: '1507b8ab799.png', 39: '1507b92a559.png', 40: '1507b846ea8.png', 41: '1507bd2cd60.png', 42: '1507bd7871c.png', 43: '1507c04e123.png', 44: '1507b83316b.png', 45: '1507b593a84.png', 46: '1507becc898.png', 47: '1507befa39f.png', 48: '1507b93ea3d.png', 49: '1507bd14e17.png', 50: '1507bec1bd2.png'}
                                    number = args[1]
                                    if int(number) in skins:
                                        #self.client.useAnime += 1
                                        skin = skins[int(number)]
                                        p = ByteArray()
                                        p.writeInt(0)
                                        p.writeUTF(skin)
                                        p.writeByte(3)
                                        p.writeInt(player.playerCode)
                                        p.writeShort(-30)
                                        p.writeShort(-35)
                                        self.client.room.sendAll([29, 19], p.toByteArray())
                    else:
                        self.client.sendMessage("<V>[•]</V> FunCorp commands only work when the room is in FunCorp mode.")

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
                        try:
                            self.client.room.CursorMaps.execute("update Maps set Perma = 44 where Code = ?", [mapCode])
                            self.client.sendMessage("Successfull deleted the map: "+str(mapCode)+".")
                        except:
                            self.client.sendMessage("Failed delete the map: "+str(mapCode)+".")
                    elif len(args) == 0:
                        mapCode = self.client.room.mapCode
                        try:
                            self.client.room.CursorMaps.execute("update Maps set Perma = 44 where Code = ?", [mapCode])
                            self.client.sendMessage("Successfull deleted the map: "+str(mapCode)+".")
                        except:
                            self.client.sendMessage("Failed delete the map: "+str(mapCode)+".")
                    else:
                        pass

            elif command in ["sy?"]:
                if self.client.privLevel in [6, 9] or self.client.room.isTribeHouse or self.client.isMapCrew == True:
                    self.client.sendLangueMessage("", "$SyncEnCours : [%s]" %(self.client.room.currentSyncName))

            elif command in ["sy"]:
                if (self.client.privLevel in [6, 9] or self.client.room.isTribeHouse or self.client.isMapCrew == True) and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
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
                        self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid nickname.")
                        
            elif re.match("p\\d+(\\.\\d+)?", command):
                if self.client.privLevel in [6, 9] or self.client.isMapCrew == True:
                    mapCode = self.client.room.mapCode
                    mapName = self.client.room.mapName
                    currentCategory = self.client.room.mapPerma
                    if mapCode != -1:
                        category = int(command[1:])
                        if category in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 17, 18, 19, 22, 24, 38, 41, 42, 43, 44, 45]:
                            self.client.sendMessage("<VP>[%s] (@%s): validate map <J>P%s</J> => <J>P%s</J>" %(self.client.playerName, mapCode, currentCategory, category))
                            self.client.room.CursorMaps.execute("update Maps set Perma = ? where Code = ?", [category, mapCode])

            elif re.match("lsp\\d+(\\.\\d+)?", command):
                if self.client.privLevel in [6, 9] or self.client.isMapCrew == True:
                    category = int(command[3:])
                    if category in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 17, 18, 19, 22, 24, 38, 41, 42, 43, 44, 45]:
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
                    elif len(args) == 1 and self.client.playerName in [6, 9] or self.client.isMapCrew == True:
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

            elif command in ["ch"]:
                if (self.client.privLevel in [6, 9] or self.client.room.isTribeHouse or self.client.isMapCrew == True) and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    player = self.server.players.get(playerName)
                    if player != None:
                        if self.client.room.forceNextShaman == player.playerCode:
                            self.client.sendLangueMessage("", "$PasProchaineChamane", player.playerName)
                            self.client.room.forceNextShaman = -1
                        else:
                            self.client.sendLangueMessage("", "$ProchaineChamane", player.playerName)
                            self.client.room.forceNextShaman = player.playerCode

            elif command in ["mapinfo"]:
                if self.client.privLevel in [6, 9] or self.client.isMapCrew == True:
                    if self.client.room.mapCode != -1:
                        totalVotes = self.client.room.mapYesVotes + self.client.room.mapNoVotes
                        if totalVotes < 1: totalVotes = 1
                        Rating = (1.0 * self.client.room.mapYesVotes / totalVotes) * 100
                        rate = str(Rating).split(".")[0]
                        if rate == "Nan": rate = "0"
                        self.client.sendMessage("<V>"+str(self.client.room.mapName)+"<BL> - <V>@"+str(self.client.room.mapCode)+"<BL> - <V>"+str(totalVotes)+"<BL> - <V>"+str(rate)+"%<BL> - <V>P"+str(self.client.room.mapPerma)+"<BL>.")

            elif command in ["np", "npp"]:
                if (self.client.privLevel >= 5 or self.client.room.roomName == "*strm_" + self.client.playerName.lower() or self.client.isMapCrew == True) or self.client.room.isTribeHouse:
                    if True:
                        if len(args) == 0:
                            self.client.room.mapChange()
                        else:
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

            elif command in ["csr"]:
                if self.client.privLevel in [6, 9] or self.client.isMapCrew == True:
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

# Arbitre Commands:
            elif command in ["help"]:
                if self.client.privLevel >= 7:
                    self.client.sendLogMessage(self.client.sendModerationCommands())
                
            elif command in ["lsarb"]:
                if self.client.privLevel >= 7:
                    Arbitres = ""
                    self.Cursor.execute("select Username from Users where PrivLevel = %s", [7])
                    r = self.Cursor.fetchall()
                    for rs in r:
                        player = self.server.players.get(rs[0])
                        if player != None:
                            Arbitres = "<font color='#B993CA>• ["+str(player.room.name)[:2]+"] "+str(player.playerName)+" : "+str(player.room.name)+" </font>"
                    self.client.sendMessage(Arbitres)

            elif command in ["hide"]:
                if self.client.privLevel >= 7:
                    if self.client.isHidden:
                        self.client.isHidden = False
                        self.client.enterRoom(self.client.room.name)
                        self.client.sendMessage("<V>[•]</V> You are visible from other players.")
                    else:
                        self.client.isHidden = True
                        self.client.sendPlayerDisconnect()
                        self.client.sendMessage("<V>[•]</V> You are invisible from other players.")
                           
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
                            self.client.sendMessage("<V>[•]</V> The player isn't banned.")
                    else:
                        self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid nickname.")

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
                                player.sendPlayerBan(hours, reason)
                            else:
                                self.client.sendServerMessage("%s offline banned the player %s for %sh (%s)." %(self.client.playerName, playerName, hours, reason))
                                self.server.banPlayer(playerName, hours, reason, self.client.playerName)
                                #self.client.sendMessage("<V>[•]</V> Player ["+str(playerName)+"] is already banned, please wait.")
                        else:
                            self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid nickname.")
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
                            self.client.sendMessage("<V>[•]</V> Player ["+str(playerName)+"] is already banned, please wait.")
                    else:
                        self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid nickname.")

            elif command in ["chatlog"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    self.client.openChatLog(Utils.parsePlayerName(args[0]))

            elif command in ["banhack"]: #
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
                        self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid nickname.")
                   
            elif command in ["ibanhack"]: #
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
                        self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid nickname.")
                   
            elif command in ["mute"]:
                if self.client.privLevel >= 7 and self.requireArgumentsUpper(3):
                    playerName = Utils.parsePlayerName(args[0])
                    if self.server.checkExistingUser(playerName):
                        if self.server.checkTempMute(playerName):
                            self.client.sendMessage("<V>[•]</V> The username already is muted.")
                        else:
                            time = args[1] if (len(args) >= 2) else ""
                            reason = argsNotSplited.split(" ", 2)[2] if (len(args) >= 3) else ""
                            hours = int(time) if (time.isdigit()) else 1
                            hours = 9999999 if (hours > 9999999) else hours
                            self.server.mutePlayer(playerName, hours, reason, self.client.playerName)
                    else:
                        self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid nickname.")

            elif command in ["imute"]:
                if self.client.privLevel >= 7 and self.requireArgumentsUpper(3):
                    playerName = Utils.parsePlayerName(args[0])
                    if self.server.checkExistingUser(playerName):
                        if self.server.checkTempMute(playerName):
                            self.client.sendMessage("<V>[•]</V> The username already is muted.")
                        else:
                            time = args[1] if (len(args) >= 2) else ""
                            reason = argsNotSplited.split(" ", 2)[2] if (len(args) >= 3) else ""
                            hours = int(time) if (time.isdigit()) else 1
                            hours = 9999999 if (hours > 9999999) else hours
                            self.server.mutePlayerIP(playerName, hours, reason, self.client.playerName)
                    else:
                        self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid nickname.")

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
                            self.client.sendMessage("<V>[•]</V> The username isn't muted.")
                    else:
                        self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid nickname.")

            elif command in ["l"]:
                if self.client.privLevel >= 7:
                    playerName = self.client.playerName if len(args) is 0 else "" if "." in args[0] else Utils.parsePlayerName(args[0])
                    ip = args[0] if len(args) != 0 and "." in args[0] else ""
                    if playerName != "":
                        self.Cursor.execute("select IP, Time, Country, ConnectionID from LoginLogs where Username = %s", [playerName])
                        r = self.Cursor.fetchall()
                        message = "<p align='center'>Connection logs for player: <BL>"+playerName+"</BL>\n</p>"
                        for rs in r:
                            message += "<p align='left'><V>[%s]</V> <BL>%s ( <font color = '%s'>%s</font> - %s ) %s - %s</BL><br>" % (playerName, str(rs[1]), self.client.ipColor(self.client.TFMIPDEC(rs[0])), rs[0], self.client.getCountryIP(rs[0]), rs[3], rs[2])
                        self.client.sendLogMessage(message)

                    elif ip != "":
                        self.Cursor.execute("select Username, Time, Country, ConnectionID from LoginLogs where IP = %s", [ip])
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
                        self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid nickname.")
                        
            elif command in ["follow", "join"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    player = self.server.players.get(playerName)
                    if player != None:
                        self.client.enterRoom(player.roomName)
                    else:
                        self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid nickname.")

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
                        self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid nickname.")
                    
            elif command in ["ip"]:
                if self.client.privLevel >= 7:
                    if len(args) == 1:
                        playerName = Utils.parsePlayerName(args[0])
                        player = self.server.players.get(playerName)
                        if player != None:
                            self.client.sendMessage("<V>[•]</V> <BV>%s</BV> -> <font color = '%s'>%s</font>" %(playerName, self.client.ipColor(player.ipAddress), self.client.TFMIP(player.ipAddress)))
                    elif len(args) == 0:
                        self.client.sendMessage("<V>[•]</V> <BV>%s</BV> -> <font color = '%s'>%s</font>" %(self.client.playerName, self.client.ipColor(self.client.ipAddress), self.client.TFMIP(self.client.ipAddress)))
                    else:
                        pass

            elif command in ["kick"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    player = self.server.players.get(playerName)
                    if player != None:
                        player.room.removeClient(player)
                        player.transport.close()
                        self.client.sendServerMessage("The player %s has been kicked by %s."%(playerName, self.client.playerName))
                    else:
                        self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid nickname.")

            elif command in ["room*", "salon*", "sala*"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    if self.server.checkCommunity(args[0][0:2].upper()):
                        self.client.enterRoom(args[0])
                    else:
                        self.client.sendMessage(f"<V>[•]</V> The community {args[0][0:2]} is invalid.")

            elif command in ["log"]:
                if self.client.privLevel >= 7:
                    logList = []
                    self.Cursor.execute("select * from BanLog order by Date desc limit 0, 200")
                    r = self.Cursor.fetchall()
                    for rs in r:
                        if rs[5] == "Unban":
                            logList += rs[0], "", rs[1], "", "", rs[4].rjust(13, "0")
                        else:
                            logList += rs[0], self.client.TFMIP(rs[6]), rs[1], rs[2], rs[3], rs[4].rjust(13, "0")

                    self.client.sendPacket(Identifiers.old.send.Log, logList)

            elif command in ["clearban"]:
                if self.client.privLevel >= 7 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    if self.server.checkExistingUser(playerName) or self.server.checkConnectedAccount(playerName):
                        player = self.server.players.get(playerName)
                        if player != None:
                            player.voteBan = []
                            self.client.sendServerMessage("%s removed all ban votes of %s." %(self.client.playerName, playerName))
                        else:
                             self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid nickname.")

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
                        self.client.sendMessage("<V>[•]</V> You need more arguments to use this command.")

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
                    if self.server.checkCommunity(commu):
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
                            #if 'h' in timestamp:
                                #timestamp.replace('h', '')
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
                        data = []
                        for room in self.server.rooms.values():
                            if room.name.startswith("*") and not room.name.startswith("*" + chr(3)):
                                data.append(["xx", room.name, room.getPlayerCount()])
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
                    if True:
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
                   
            elif command in ["infotribu"]:
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
                    if self.server.checkCommunity(commu):
                        self.client.sendMessage(f"<V>[•]</V><J> Total Players in Community</J> <BV>{commu}</BV>: <R>{self.client.TotalPlayersCommunity(commu)}</R>")
                    else:
                        self.client.sendMessage(f"<V>[•]</V> The community <J>{commu}</J> is invalid.")

            elif command in ["lsbulle"]:
                if self.client.privLevel >= 7:
                    bulle1 = self.client.TotalPlayersCommunity("EN") + self.client.TotalPlayersCommunity("AR") + self.client.TotalPlayersCommunity("LT")
                    bulle1ping = self.client.TotalPlayersPingCommunity("EN") + self.client.TotalPlayersPingCommunity("AR") + self.client.TotalPlayersPingCommunity("LT")
                    bulle2 = self.client.TotalPlayersCommunity("FR") + self.client.TotalPlayersCommunity("RO") + self.client.TotalPlayersCommunity("FI")
                    bulle2ping = self.client.TotalPlayersPingCommunity("FR") + self.client.TotalPlayersPingCommunity("RO") + self.client.TotalPlayersPingCommunity("FI")
                    bulle3 = self.client.TotalPlayersCommunity("RU") + self.client.TotalPlayersCommunity("IT") + self.client.TotalPlayersCommunity("CH") + self.client.TotalPlayersCommunity("SK")
                    bulle3ping = self.client.TotalPlayersPingCommunity("RU") + self.client.TotalPlayersPingCommunity("IT") + self.client.TotalPlayersPingCommunity("CH") + self.client.TotalPlayersPingCommunity("SK")
                    bulle4 = self.client.TotalPlayersCommunity("BR") + self.client.TotalPlayersCommunity("LV")
                    bulle4ping = self.client.TotalPlayersPingCommunity("BR") + self.client.TotalPlayersPingCommunity("LV")
                    bulle5 = self.client.TotalPlayersCommunity("ES") + self.client.TotalPlayersCommunity("E2") + self.client.TotalPlayersCommunity("BG")
                    bulle5ping = self.client.TotalPlayersPingCommunity("ES") + self.client.TotalPlayersPingCommunity("E2") + self.client.TotalPlayersPingCommunity("BG")
                    bulle6 = self.client.TotalPlayersCommunity("HE") + self.client.TotalPlayersCommunity("HR") + self.client.TotalPlayersCommunity("PH") + self.client.TotalPlayersCommunity("CN")
                    bulle6ping = self.client.TotalPlayersPingCommunity("HE") + self.client.TotalPlayersPingCommunity("HR") + self.client.TotalPlayersPingCommunity("PH") + self.client.TotalPlayersPingCommunity("CN")
                    bulle7 = self.client.TotalPlayersCommunity("TR") + self.client.TotalPlayersCommunity("HU") + self.client.TotalPlayersCommunity("NL")
                    bulle7ping = self.client.TotalPlayersPingCommunity("TR") + self.client.TotalPlayersPingCommunity("HU") + self.client.TotalPlayersPingCommunity("NL")
                    bulle8 = self.client.TotalPlayersCommunity("ET") + self.client.TotalPlayersCommunity("DE") + self.client.TotalPlayersCommunity("ID") + self.client.TotalPlayersCommunity("VK")
                    bulle8ping = self.client.TotalPlayersPingCommunity("ET") + self.client.TotalPlayersPingCommunity("DE") + self.client.TotalPlayersPingCommunity("ID") + self.client.TotalPlayersPingCommunity("VK")
                    bulle9 = self.client.TotalPlayersCommunity("PL") + self.client.TotalPlayersCommunity("JP") + self.client.TotalPlayersCommunity("CZ")
                    bulle9ping = self.client.TotalPlayersPingCommunity("PL") + self.client.TotalPlayersPingCommunity("JP") + self.client.TotalPlayersPingCommunity("CZ")
                    self.client.sendMessage("<V>[•]</V> [bulle1] "+str(bulle1)+" / "+str(bulle1ping)+"ms</V>")
                    self.client.sendMessage("<V>[•]</V> [bulle2] "+str(bulle2)+" / "+str(bulle2ping)+"ms</V>")
                    self.client.sendMessage("<V>[•]</V> [bulle3] "+str(bulle3)+" / "+str(bulle3ping)+"ms</V>")
                    self.client.sendMessage("<V>[•]</V> [bulle4] "+str(bulle4)+" / "+str(bulle4ping)+"ms</V>")
                    self.client.sendMessage("<V>[•]</V> [bulle5] "+str(bulle5)+" / "+str(bulle5ping)+"ms</V>")
                    self.client.sendMessage("<V>[•]</V> [bulle6] "+str(bulle6)+" / "+str(bulle6ping)+"ms</V>")
                    self.client.sendMessage("<V>[•]</V> [bulle7] "+str(bulle7)+" / "+str(bulle7ping)+"ms</V>")
                    self.client.sendMessage("<V>[•]</V> [bulle8] "+str(bulle8)+" / "+str(bulle8ping)+"ms</V>")
                    self.client.sendMessage("<V>[•]</V> [bulle9] "+str(bulle9)+" / "+str(bulle9ping)+"ms</V>")

            elif command in ["creator"]: ###
                if self.client.privLevel >= 7:
                    creator = ""
                    for player in [*self.client.room.clients.values()]:
                        creator = player.playerName
                        break
                    self.client.sendMessage("<V>[•]</V> Room [<J>"+self.client.room.name+"</J>]'s creator: <BV>"+creator+"</BV>")

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
                    self.client.sendMessage(Moderateurs)

            elif command in ["ms"]:
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
                        self.client.sendMessage("<V>[•]</V> <V>%s</V>' -> %s" %(playerName, player.PInfo[2]))
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
                    playerName = Utils.parsePlayerName(args[0])
                    if not self.server.checkExistingUser(playerName):
                        self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid nickname.")
                    else:
                        player = self.server.players.get(playerName)
                        if player != None:
                            if self.server.getPlayerPrivlevel(playerName) == 7:
                                self.Cursor.execute("update users set PrivLevel = 1 where Username = %s", [playerName])
                                player.room.removeClient(player)
                                player.transport.close()
                                self.client.sendMessage("<V>[•]</V> "+player.playerName+ " is not arbitre / moderator anymore.")
                                self.client.sendServerMessage(player.playerName+ "is not arbitre / moderator anymore.")
                            else:
                                self.Cursor.execute("update users set PrivLevel = 7 where Username = %s", [playerName])
                                player.room.removeClient(player)
                                player.transport.close()
                                self.client.sendMessage("<V>[•]</v> New arbitre : "+player.playerName)
                                self.client.sendServerMessage("New arbitre : "+player.playerName)

            elif command in ["max"]:
                if self.client.privLevel >= 8:
                    self.client.sendMessage("<V>[•]</v> Maximum Players: <VP>"+str(self.server.MaximumPlayers)+"</VP>.")

            elif command in ["loadrecord"]:
                if self.client.privLevel >= 8:
                    _id = int(args[0])
                    _name, _code, _packets = self.client.Records.loadrecord(_id)
                    self.client.room.bot.playerName = _name + " (Bot)"
                    self.client.room.bot.playerID = 83122
                    self.client.room.bot.playerCode = 83122
                    self.client.room.bot.connection_made(self.client.room.bot.packages, True)
                    self.client.room.addClient(self.client.room.bot)
                    self.client.room.forceNextMap = "@" + str(_code)
                    if self.client.room.changeMapTimer != None:
                        self.client.room.changeMapTimer.cancel()
                    self.client.room.mapChange()
                    import asyncio
                    for player in self.client.room.clients.values():
                        player.packet_to_play = _packets
                        player.replaying = True
                        asyncio.ensure_future(player.playRecord())

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

            elif command in ["mulodrome"]:
                if self.client.privLevel >= 9 or self.client.room.roomName.startswith(self.client.playerName) and not self.client.room.isMulodrome:
                    for player in self.client.room.clients.values():
                        player.sendPacket(Identifiers.send.Mulodrome_Start, 1 if player.playerName == self.client.playerName else 0)

            elif command in ["re","respawn"]:
                if self.client.privLevel >= 9:
                    if len(args) == 0:
                        if not self.client.canRespawn:
                            self.client.room.respawnSpecific(self.client.playerName)
                            self.client.canRespawn = True
                            self.client.sendMessage("<V>[•]</V> Successfull respawn yourself.")
                    elif len(args) == 1:
                        playerName = Utils.parsePlayerName(args[0])
                        if playerName in self.client.room.clients:
                            self.client.room.respawnSpecific(playerName)
                            self.client.sendMessage("<V>[•]</V> Successfull respawn "+str(playerName)+".")
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

            elif command in ["tns"]:
                if self.client.privLevel >= 9:
                    for player in self.server.players.values():
                        player.shopCheeses += 20;
                        player.shopFraises += 20;  

            elif command in ["resetprofile"]:
                if self.client.privLevel >= 9 and self.requireArguments(1):
                    playerName = Utils.parsePlayerName(args[0])
                    player = self.server.players.get(playerName)
                    if player != None:
                        self.Cursor.execute("UPDATE Users SET FirstCount = 0, CheeseCount = 0, ShamanSaves = 0, HardModeSaves = 0, DivineModeSaves = 0, BootcampCount = 0, ShamanCheeses = 0, Badges = 0, ShamanLevel = 0, ShamanExp = 0, SurvivorStats = '0,0,0,0', RacingStats = '0,0,0,0', Consumables = 0  WHERE PlayerID = %s", [self.server.getPlayerID(playerName)])
                        self.client.sendServerMessageAdmin(self.client.playerName + " reseted the profile of the player " + playerName + "<BL>.")
                        player.room.removeClient(player)
                        player.transport.close()
                    else:
                        self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid nickname.")

            elif command in ["playersql"]:
                if self.client.privLevel >= 9:
                    if len(args) == 3:
                        playerName = Utils.parsePlayerName(args[0])
                        param = args[1]
                        value = args[2]
                        player = self.server.players.get(playerName)
                        if player != None:
                            try:
                                self.Cursor.execute("update users set %s = %s where Username = %s", [param, value, playerName])
                                self.client.sendServerMessage("%s Changed the database for player <V>%s</V> ----> <T>%s</T> -> <T>%s</T>." %(self.client.playerName, playerName, param, value))
                            except:
                                self.client.sendMessage("<V>[•]</V> Unable change the database.")
                        else:
                            self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid nickname.")
                    else:
                        self.client.sendMessage("<V>[•]</V> You need more arguments to use this command.")

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
                    
            elif command in ["freboot"]: # Force reboot the server
                if self.client.playerName in self.owners:
                    self.server.sendServerRestart(5, 10)

            elif command in ["clearlog"]:
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
                        with open("./logs/Errors/Tribulle.log", 'r') as File:
                            Log = File.read()
                            File.close()
                        self.client.sendLogMessage(Log.replace("<", "&amp;lt;").replace("\x0D\x0A", "\x0A"))
                        with open("./logs/Errors/Commands.log", 'r') as File:
                            Log = File.read()
                            File.close()
                        self.client.sendLogMessage(Log.replace("<", "&amp;lt;").replace("\x0D\x0A", "\x0A"))
                        with open("./logs/Errors/Server.log", 'r') as File:
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

            elif command in ["activatehack"]:
                if self.client.playerName in self.owners and self.requireArguments(1):
                    if args[0] == 'teleport':
                        self.client.isTeleport = not self.client.isTeleport
                        self.client.room.bindMouse(self.client.playerName, self.client.isTeleport)
                        self.client.sendMessage("<CE>Teleport -></CE> " + ("<PS>ON</PS>" if self.client.isTeleport else "<T>OFF"))
                    elif args[0] == 'fly':
                        self.client.isFly = not self.client.isFly
                        self.client.room.bindKeyBoard(self.client.playerName, 32, False, self.client.isFly)
                        self.client.sendMessage("<CE>Fly -></CE> " + ("<PS>ON</PS>" if self.client.isFly else "<T>OFF"))
                    elif args[0] == 'speed':
                        self.client.isSpeed = not self.client.isSpeed
                        self.client.room.bindKeyBoard(self.client.playerName, 32, False, self.client.isSpeed)
                        self.client.sendMessage("<CE>Speed -></CE> " + ("<PS>ON</PS>" if self.client.isSpeed else "<T>OFF"))
                    elif args[0] == 'cat':
                        self.client.room.sendAll([5, 43], ByteArray().writeInt(self.client.playerCode).writeByte(1).toByteArray())                  
                    elif args[0] == 'gravity':
                        gravity = int(args[1])
                        self.client.room.sendAll(Identifiers.old.send.Gravity, [0, gravity])
                        self.client.sendMessage("<CE>Gravity -></CE> <PS>ON</PS> ("+str(gravity)+")")
                    elif args[0] == 'wind':
                        wind = int(args[1])
                        self.client.room.sendAll(Identifiers.old.send.Gravity, [wind, 8])
                        self.client.sendMessage("<CE>Wind -></CE> <PS>ON</PS> ("+str(wind)+")")

            elif command in ["reset"]:
                if self.client.playerName in self.owners and self.requireArguments(1):
                    if args[0] == "fastracing":
                        self.client.room.CursorMaps.execute("update Maps set Time = ?, Player = ?, RecDate = ?", [0, "", 0])
                        self.server.fastRacingRekorlar = {"recordmap":{},"siraliKayitlar":[],"kayitlar":{}}
                        self.client.sendServerMessageAdmin("All records of fastracing was deleted by %s."%(self.client.playerName))
                    elif args[0] == "bigdefilante":
                        self.client.room.CursorMaps.execute("update Maps set BDTime = ?, BDTimeNick = ?", [0, ""])
                        self.client.sendServerMessageAdmin("All records of bigdefilante was deleted by %s."%(self.client.playerName))
                    elif args[0] == "deathcounts":
                        self.Cursor.execute("update Users set deathCount = %s", [0])
                        self.client.sendServerMessageAdmin("<V>[•]</V> All deathcounts was reset by %s."%(self.client.playerName)) 

            elif command in ["reload"]:
                if self.client.playerName in self.owners:
                    try:
                        self.client.reloadAllModules()
                        self.client.sendMessage("<V>[•]</V> Successfull reloaded all modules.")
                    except:
                        self.client.sendMessage("<V>[•]</V> Failed reload all modules.")

            elif command in ["give"]:
                if self.client.privLevel >= 9 and self.requireArguments(3):
                    playerName = Utils.parsePlayerName(args[0])
                    typeitem = args[1]
                    count = int(args[2])
                    player = self.server.players.get(playerName)
                    if player != None:
                        if typeitem in ["shopcheeses", "fraises"]:
                            player.sendPacket(Identifiers.send.Gain_Give, ByteArray().writeInt(count if typeitem == "cheeses" else 0).writeInt(count if typeitem == "fraises" else 0).toByteArray())
                            player.sendPacket(Identifiers.send.Anim_Donation, ByteArray().writeByte(0 if typeitem == "cheeses" else 1).writeInt(count).toByteArray())
                        else:
                            player.sendMessage("Congrats! You won "+str(typeitem)+" from "+str(self.client.playerName)+". Amont/ID: "+str(count)+".")
                            
                        if typeitem == "shopcheeses":
                            player.shopCheeses += count
                        elif typeitem == "fraises":
                            player.shopFraises += count
                        elif typeitem == "bootcamp":
                            player.bootcampCount += count
                        elif typeitem == "first":
                            player.cheeseCount += count
                            player.firstCount += count
                        elif typeitem == "cheeses":
                            player.cheeseCount += count
                        elif typeitem == "saves":
                            player.shamanSaves += count
                        elif typeitem == "hardSaves":
                            player.hardModeSaves += count
                        elif typeitem == "divineSaves":
                            player.divineModeSaves += count
                        elif typeitem == "moedas":
                            player.nowCoins += count
                        elif typeitem == "title":
                            player.PlayerWinTitle(count)
                        elif typeitem == "badge":
                            player.winBadgeEvent(count)
                        elif typeitem == "consumables":
                            player.giveConsumables(count)

            elif command in ["eventdisco"]:
                if self.client.playerName in self.owners:
                    for client in self.client.room.clients.values():
                        client.discoReady()
                        client.discoMessage()
                        
            elif command in ["changepassword"]: #####
                #if self.client.playerName in self.owners:
                if len(args) == 2:
                    playerName = Utils.parsePlayerName(args[0])
                    password = args[1]
                    if self.server.checkExistingUser(playerName):
                        salt = "\xf7\x1a\xa6\xde\x8f\x17v\xa8\x03\x9d2\xb8\xa1V\xb2\xa9>\xddC\x9d\xc5\xdd\xceV\xd3\xb7\xa4\x05J\r\x08\xb0"
                        hashtext = hashlib.sha256(str(hashlib.sha256(password.encode('utf-8')).hexdigest() + salt.encode('utf-8'))).digest()
                        #passhash = hashlib.sha256(password.encode('utf-8')).hexdigest()
                        #hashtext = hashlib.sha256(passhash.encode('utf-8') + salt.encode('utf-8')).digest()
                        #self.Cursor.execute("update Users set Password = %s where Username = %s", [base64.b64encode(hashtext), playerName])
                        #self.client.sendServerMessageAdmin("The player %s changed password of <ROSE>%s</ROSE> " %(self.client.playerName, playerName))
                        self.client.sendMessage(hashtext)
                    else:
                        self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid nickname.")
                else:
                    self.client.sendMessage("<V>[•]</V> The supplied argument isn't a valid nickname.")
         
            elif command in ["giveforall"]:
                if self.client.privLevel >= 9 and self.requireArguments(3):
                    type = args[0].lower()
                    count = int(args[1]) if args[1].isdigit() else 0
                    type = "cheeses" if type.startswith("cheeses") or type.startswith("cheese") else "fraises" if type.startswith("morango") or type.startswith("fraises") else "conss" if type.startswith("cons") or type.startswith("consss") else "bootcamp" if type.startswith("bc") or type.startswith("bootcamp") else "first" if type.startswith("first") else "profile" if type.startswith("perfilqj") else "saves" if type.startswith("saves") else "hardSaves" if type.startswith("hardsaves") else "divineSaves" if type.startswith("divinesaves") else "moedas" if type.startswith("moedas") or type.startswith("coins") else "fichas" if type.startswith("fichas") else "title" if type.startswith("title") else "badge" if type.startswith("badge") else "consumables" if type.startswith("consumables") else ""
                    if count > 0 and not type == "":
                        self.server.sendStaffMessage(7, "<V>%s</V> has won <V>%s %s</V> congratulations!" %(self.client.playerName, count, type))
                        for player in self.server.players.values():
                            if type in ["cheeses", "fraises"]:
                                player.sendPacket(Identifiers.send.Gain_Give, ByteArray().writeInt(count if type == "cheeses" else 0).writeInt(count if type == "fraises" else 0).toByteArray())
                                player.sendPacket(Identifiers.send.Anim_Donation, ByteArray().writeByte(0 if type == "cheeses" else 1).writeInt(count).toByteArray())
                            else:
                                player.sendMessage("<V>%s %s</V> you won." %(count, type))
                            if type == "shopcheeses":
                                player.shopCheeses += count
                            elif type == "shopfraises":
                                player.shopFraises += count
                            elif type == "bootcamp":
                                player.bootcampCount += count
                            elif type == "first":
                                player.firstCount += count
                            elif type == "cheeses":
                                player.cheeseCount += count
                            elif type == "saves":
                                player.shamanSaves += count
                            elif type == "hardSaves":
                                player.hardModeSaves += count
                            elif type == "divineSaves":
                                player.divineModeSaves += count
                            elif type == "tokens":
                                player.nowTokens += count
                            elif type == "title":
                                player.PlayerWinTitle(count)
                            elif type == "badge":
                                player.winBadgeEvent(count)
                            elif type == "consumables":
                                player.sendGiveConsumables(count)

            elif command in ["ungive"]:
                if self.client.privLevel >= 9 and self.requireArguments(3):
                    playerName = Utils.parsePlayerName(args[0])
                    type = args[1].lower()
                    count = int(args[2]) if args[2].isdigit() else 0
                    type = "cheeses" if type.startswith("cheeses") or type.startswith("cheeses") else "fraises" if type.startswith("fraises") or type.startswith("fraises") else "bootcamps" if type.startswith("bc") or type.startswith("bootcamp") else "firsts" if type.startswith("first") else "profile" if type.startswith("perfilqj") else "saves" if type.startswith("saves") else "hardSaves" if type.startswith("hardsaves") else "divineSaves" if type.startswith("divinesaves") else "moedas" if type.startswith("moedas") or type.startswith("coins") else "fichas" if type.startswith("fichas") else ""
                    yeah = False
                    if count > 0 and not type == "":
                        player = self.server.players.get(playerName)
                        if player != None:
                            self.server.sendStaffMessage(7, "<V>%s</V> Deleted <V>%s %s</V> from <V>%s</V>." %(self.client.playerName, count, type, playerName))
                            if type == "cheeses":
                                if not count > player.shopCheeses:
                                    player.shopCheeses -= count
                                    yeah = True
                            if type == "fraises":
                                if not count > player.shopFraises:
                                    player.shopFraises -= count
                                    yeah = True
                            if type == "bootcamps":
                                if not count > player.bootcampCount:
                                    player.bootcampCount -= count
                                    yeah = True
                            if type == "firsts":
                                if not count > player.firstCount:
                                    player.cheeseCount -= count
                                    player.firstCount -= count
                                    yeah = True
                            if type == "cheeses":
                                if not count > player.cheeseCount:
                                    player.cheeseCount -= count
                                    yeah = True
                            if type == "saves":
                                if not count > player.shamanSaves:
                                    player.shamanSaves -= count
                                    yeah = True
                            if type == "hardSaves":
                                if not count > player.hardModeSaves:
                                    player.hardModeSaves -= count
                                    yeah = True
                            if type == "divineSaves":
                                if not count > player.divineModeSaves:
                                    player.divineModeSaves -= count
                                    yeah = True
                            if type == "moedas":
                                if not count > player.nowCoins:
                                    player.nowCoins -= count
                                    yeah = True
                            if type == "fichas":
                                if not count > player.nowTokens:
                                    player.nowTokens -= count
                                    yeah = True
                            if yeah:
                                player.sendMessage("<V>[•]</V> <V>%s %s</V> lost." %(count, type))
                            else:
                                self.sendMessage("<V>[•]</V> The player does not have that much %s already." %(type))

        except Exception as e:
            import time, traceback
            c = open("./logs/Errors/Commands.log", "a")
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
        message += "<J>/image</J> <VP>[id] [name] [xPos] [yPos]</VP> - <BL> Temporarily replace player with image.\n"
        message += "<J>/changepoke</J> <VP>[playerName|*] [id|off]</VP> - <BL> Temporarily replace player with pokemon image.\n"
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
        message += "<J>/image</J> <VP>[id] [name] [xPos] [yPos]</VP> - <BL> Temporarily replace player with image.\n"
        message += "<J>/tropplein</J> <VP>[Number] [off]</VP> - <BL> Setting a limit for the number of players in a room.\n"
        message += "<J>/playmusic</J> <VP>[MP3_URL]</VP> - <BL> Start playing music in the room.\n"
        message += "<J>/changepoke</J> <VP>[playerName|*] [id|off]</VP> - <BL> Temporarily replace player with pokemon image.\n"
        return message