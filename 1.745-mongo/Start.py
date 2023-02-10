#coding: utf-8
import sys
sys.dont_write_bytecode = True
import requests, re, os, json, time, random, aiosqlite, pymongo, traceback, zlib, asyncio, urllib.request, binascii, configparser, socket, base64
import time as _time
import modules as _module

from time import gmtime, strftime
from datetime import datetime, date, timedelta
from utils import *
from modules import *
from colorconsole  import win
from importlib import reload
from lupa import LuaRuntime

loop = asyncio.get_event_loop()

# Others
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))

class Client:
    def __init__(self, _server):
        self.loop = asyncio.new_event_loop()
        self.packages = ByteArray()
        self.server = _server

        # String
        self.computerLanguage = "EN"
        self.computerOS = ""
        self.computerOSVersion = ""
        self.currentCaptcha = ""
        self.emailAddress = ""
        self.ipColor = ""
        self.ipCountry = ""
        self.isReportedType = ""
        self.langue = ""
        self.lastMessage = ""
        self.lastNpc = ""
        self.lastroom = ""
        self.marriage = ""
        self.modoPwetLangue = "ALL"
        self.mouseColor = "78583a"
        self.mouseName = ""
        self.nickColor = "#95d9d6"
        self.playerLook = "1;0,0,0,0,0,0,0,0,0,0,0"
        self.playerName = ""
        self.roles = ""
        self.roomName = ""
        self.shamanColor = "95d9d6"
        self.shamanItems = ""
        self.shamanLook = "0,0,0,0,0,0,0,0,0,0"
        self.shopItems = ""
        self.silenceMessage = ""
        self.tempMouseColor = ""
        self.tradeName = ""
        self.tribeMessage = ""
        self.tribeName = ""
        self.tribeRanks = ""
        self.shopGifts = ""
        self.playerLetters = ""
        self.shopMessages = ""
        
        # Integer
        self.sayfasayi = 0
        self.lbsayfa = 0
        self.ambulanceCount = 0
        self.banHours = 0
        self.bootcampCount = 0
        self.bootcampRounds = 0
        self.bubblesCount = 0
        self.cheeseCount = 0
        self.currentPlace = 0
        self.defilantePoints = 0
        self.defilanteRounds = 0
        self.divineModeSaves = 0
        self.divineModeSavesNoSkill = 0
        self.drawingColor = 0
        self.equipedShamanBadge = 0
        self.firstCount = 0
        self.fur = 0
        self.furEnd = 0
        self.gender = 0
        self.hardModeSaves = 0
        self.hardModeSavesNoSkill = 0
        self.iceCount = 0
        self.langueID = 0
        self.lastDivorceTimer = 0
        self.lastGameMode = 0
        self.lastOn = 0
        self.lastPacketID = random.randint(0, 99)
        self.lastReportID = 0
        self.loginTime = 0
        self.pet = 0
        self.petEnd = 0
        self.pingTime = 0
        self.playerCode = 0
        self.playerID = 0
        self.playerKarma = 0
        self.playerScore = 0
        self.playerStartTimeMillis = 0
        self.playerTime = 0
        self.posX = 0
        self.posY = 0
        self.priceDoneVisu = 0
        self.privLevel = 0
        self.racingRounds = 0
        self.regDate = 0
        self.shamanCheeses = 0
        self.shamanExp = 0
        self.shamanExpNext = 32
        self.shamanLevel = 0
        self.shamanSaves = 0
        self.shamanSavesNoSkill = 0
        self.shamanType = 0
        self.shopCheeses = 0
        self.shopFraises = 0
        self.silenceType = 0
        self.survivorDeath = 0
        self.titleNumber = 0
        self.titleStars = 0
        self.tribeChat = 0
        self.tribeCode = 0
        self.tribeHouse = 0
        self.tribeJoined = 0
        self.tribeRank = 0
        self.tribulleID = 0
        self.velX = 0
        self.velY = 0
        self.verifycoder = -1
        self.isNoShamanSkills = 0
        
        self.aventureSaves = 0
        self.hasArtefact = 0
        self.artefactID = 0
        self.cheeseCounter = 0

        # Bool
        self.canRedistributeSkills = False
        self.canRespawn = False
        self.canShamanRespawn = False
        self.canSkipMusic = False
        self.desintegration = False
        self.hasCheese = False
        self.hasEnter = False
        self.hasLuaTransformations = False
        self.isAfk = False
        self.isCafe = False
        self.isClosed = False
        self.isDead = False
        self.isEnterRoom = False
        self.isFashionSquad = False
        self.isFunCorpPlayer = False
        self.isGuest = False
        self.isHidden = False
        self.isJumping = False
        self.isLuaAdmin = False
        self.isLuaCrew = False
        self.isMapCrew = False
        self.isModoPwet = False
        self.isModoPwetNotifications = False
        self.isMovingLeft = False
        self.isMovingRight = False
        self.isMumute = False
        self.isMute = False
        self.isNewPlayer = False
        self.isOpportunist = False
        self.isPrisoned = False
        self.isReloadCafe = False
        self.isShaman = False
        self.isSkill = False
        self.isTrade = False
        self.isTribeOpen = False
        self.isVampire = False
        self.lastping = False
        self.openingFriendList = False
        self.resetTotem = False
        self.tradeConfirm = False
        self.useTotem = False
        self.validatingVersion = False
        self.canChangeMission = True

        # Others
        self.Cursor = Cursor
        self.CursorCafe = CursorCafe
        self.CMDTime = time.time()
        self.CRTTime = time.time()
        self.MessageTime = time.time()

        # Nonetype
        self.room = None
        self.awakeTimer = None
        self.skipMusicTimer = None
        self.resSkillsTimer = None
        self.followed = None
        self.killafktimer = None
        self.playerException = None
        
        # List
        self.records = []
        self.totem = [0, ""]
        self.PInfo = [0, 0, 0]
        self.tempTotem = [0, ""]
        self.racingStats = [0] * 4
        self.survivorStats = [0] * 4
        self.defilanteStats = [0] * 3
        self.invitedTribeHouses = []
        self.voteBan = []
        self.clothes = []
        self.titleList = []
        self.friendsList = []
        self.tribeInvite = []
        self.shamanBadges = []
        self.ignoredsList = []
        self.mulodromePos = []
        self.shopTitleList = []
        self.marriageInvite = []
        self.firstTitleList = []
        self.cheeseTitleList = []
        self.shamanTitleList = []
        self.specialTitleList = []
        self.Notifications = []
        self.bootcampTitleList = []
        self.hardModeTitleList = []
        self.equipedConsumables = []
        self.ignoredTribeInvites = []
        self.divineModeTitleList = []
        self.ignoredMarriageInvites = []
        self.custom = []
        self.visuDone = []
        self.canLogin = [False, False, False, False]

        # Dict
        self.playerConsumables = {}
        self.playerSkills = {}
        self.shopBadges = {}
        self.tradeConsumables = {}
        self.aventureCounts = {}
        self.aventurePoints = {}
        self.tribeInfo = ["", "", 0, "", ""]
    
# Packets
    
    def eof_received(self):
        pass

    def getnewlen(self, b):
        var_2068 = 0
        var_2053 = 0
        var_176 = b
        while var_2053 < 10:
            var_56 = var_176.readByte() & 0xFF
            var_2068 = var_2068 | (var_56 & 0x7F) << 7 * var_2053
            var_2053 += 1
            if not ((var_56 & 0x80) == 0x80 and var_2053 < 10): #5
                return var_2068+1, var_2053

    def data_received(self, data):
        if data == b'<policy-file-request/>\x00':
            self.transport.write(b'<cross-domain-policy><allow-access-from domain=\"*\" to-ports=\"*\"/></cross-domain-policy>\x00')
            self.transport.close()
            return

        self.packages.write(data)
        oldpacket = self.packages.copy()
        while self.packages.getLength() > 0:
            length, lenlen = self.getnewlen(self.packages)
            if self.packages.getLength() >= length:
                read = ByteArray(self.packages.bytes[:length])
                oldpacket.bytes = oldpacket.bytes[length:]
                self.packages.bytes = self.packages.bytes[length:]
                loop.create_task(self.parseString(read))
            else:
                self.packages = oldpacket
                break

    def connection_made(self, transport):
        self.transport = transport
        self.ipAddress = transport.get_extra_info("peername")[0]
        self.modoPwet = ModoPwet(self, self.server)
        self.tribulle = Tribulle(self, self.server)
        self.Shop = Shop(self, self.server)
        self.Skills = Skills(self, self.server)
        self.Packets = Packets(self, self.server)
        self.Commands = Commands(self, self.server)
        self.playerException = GameException(self)
        self.missions = Missions(self, self.server)
        self.AntiCheat = AntiCheat(self, self.server)
        self.Cafe = Cafe(self, self.server)
        if self.ipAddress in self.server.connectedCounts:
            self.server.connectedCounts[self.ipAddress] += 1
        else:
            self.server.connectedCounts[self.ipAddress] = 1
        
        if self.server.connectedCounts[self.ipAddress] >= 100 or self.ipAddress in self.server.IPPermaBanCache or self.ipAddress in self.server.IPTempBanCache or self.ipAddress in self.server.badIPS:
            self.transport.close()
            self.server.IPTempBanCache.append(self.ipAddress)

    def connection_lost(self, args):
        self.isClosed = True
        if self.ipAddress in self.server.connectedCounts:
            count = self.server.connectedCounts[self.ipAddress] - 1
            if count < 1:
                del self.server.connectedCounts[self.ipAddress]
            else:
                self.server.connectedCounts[self.ipAddress] = count

        if self.playerName in self.server.players:
            if self.server.players[self.playerName].followed != None:
                self.isHidden = False
                self.sendPacket(Identifiers.send.Watch, ByteArray().writeUTF("").writeBoolean(False).toByteArray())
                self.enterRoom(self.lastroom)
                self.server.players[self.playerName].followed = None
            del self.server.players[self.playerName]
                
            if self.isTrade:
                self.cancelTrade(self.tradeName)

            if self.playerName in self.server.reports:
                if not self.server.reports[self.playerName]["state"] in ["banned", "deleted"]:
                    self.server.reports[self.playerName]["state"] = "disconnected"

            if self.playerName in self.server.chatMessages:
                self.server.chatMessages[self.playerName] = {}
                del self.server.chatMessages[self.playerName]

            for player in self.server.players.copy().values():
                if self.playerName and player.playerName in self.friendsList and player.friendsList:
                    player.tribulle.sendFriendDisconnected(self.playerName)

            if self.tribeCode != 0:
                self.tribulle.sendTribeMemberDisconnected()

            if self.room != None:
                self.room.removeClient(self)

            if not self.playerName == "":
                if not self.isGuest:
                    self.updateDatabase()
                    self.sendModInfo(0)
                                                    
    def sendPacket(self, identifiers, data=b""):
        loop.create_task(self._sendPacket(identifiers, data))

    async def _sendPacket(self, identifiers, data=b""):
        if self.isClosed:
            return

        if isinstance(data, list):
            data = ByteArray().writeUTF(chr(1).join(map(str, ["".join(map(chr, identifiers))] + data))).toByteArray()
            identifiers = [1, 1]

        elif isinstance(data, int):
            data = chr(data)

        if isinstance(data, str):
            data = data.encode()

        self.lastPacketID = (self.lastPacketID + 1) % 255
        packet = ByteArray()
        length = len(data) + 2
        packet2 = ByteArray()
        calc1 = length >> 7
        while calc1 != 0:
            packet2.writeByte(((length & 127) | 128))
            length = calc1
            calc1 = calc1 >> 7
        packet2.writeByte((length & 127))
        
        packet.writeBytes(packet2.toByteArray()).writeByte(identifiers[0]).writeByte(identifiers[1]).writeBytes(data)
        self.transport.write(packet.toByteArray())
        
    async def parseString(self, packet):
        if self.isClosed:
            return  
        packetID, C, CC = packet.readByte(), packet.readByte(), packet.readByte()       
        if not self.validatingVersion:
            if ((C,CC) == Identifiers.recv.Correct_Version):
                version, lang, ckey, stand = packet.readShort(), packet.readUTF(), packet.readUTF(), packet.readUTF()
                if stand == "StandAlone" and self.server.activateAntiCheat:
                    self.sendServerMessage("[Anti-Cheat] The ip <font color='"+self.ipColor+"'>"+Utils.EncodeIP(self.ipAddress)+"</font> is connected with standalone.")

                if not ckey == self.server.CKEY and version != self.server.Version:
                    print("[%s] [WARN] Invalid version or CKey (%s, %s)" %(time.strftime("%H:%M:%S"), version, ckey))
                    self.transport.close()
                else:
                    self.validatingVersion = True
                    self.sendCorrectVersion(lang)
        else:
            try:
                self.lastPacketID = packetID
                if C != 0 and CC != 0:
                    if self.server.activateAntiCheat:
                        self.AntiCheat.readPacket(C + CC)
                await self.Packets.parsePacket(packetID, C, CC, packet)
            except Exception as e:
                sex = ServerException(e)
                sex.SaveException("Server.log", self.client, "servererreur")

# Functions

    def buyNPCItem(self, itemID):
        item = self.server.npcs["Shop"][self.lastNpc][itemID]
        type, id, amount, four, priceItem, priceAmount = item
        if priceItem in self.playerConsumables and self.playerConsumables[priceItem] >= priceAmount:
            count = self.playerConsumables[priceItem] - priceAmount
            if count <= 0:
                del self.playerConsumables[priceItem]
            else:
                self.playerConsumables[priceItem] = count
                
            self.sendUpdateInventoryConsumable(priceItem, count)
            
            if type == 1:
                self.sendAnimZelda(3, id)
                self.Shop.sendUnlockedBadge(id)
                self.shopBadges.append(id)

            elif type == 2:
                self.sendAnimZelda(6, id)
                self.shamanBadges.append(id)
                    
            elif type == 3:
                self.titleList.append(id + 0.1)
                self.changeTitle(id)
                    
            elif type == 4:
                self.giveConsumable(id, amount)
            self.openNpcShop(self.lastNpc)

    def cancelTrade(self, playerName):
        player = self.room.clients.get(playerName)
        if player != None:
            self.tradeName = ""
            self.isTrade = False
            self.tradeConsumables = {}
            self.tradeConfirm = False
            player.tradeName = ""
            player.isTrade = False
            player.tradeConsumables = {}
            player.tradeConfirm = False
            player.sendTradeResult(self.playerName, 2)

    def changeTitle(self, id):
        self.titleStars = 1
        self.titleNumber = id
        self.sendUnlockedTitle(id, 1)
        self.sendPacket(Identifiers.send.Change_Title, ByteArray().writeByte(self.gender).writeShort(self.titleNumber).toByteArray())

    def checkAndRebuildTitleList(self, type):
        titlesLists = [self.cheeseTitleList, self.firstTitleList, self.shamanTitleList, self.shopTitleList, self.bootcampTitleList, self.hardModeTitleList, self.divineModeTitleList]
        titles = [self.server.cheeseTitleList, self.server.firstTitleList, self.server.shamanTitleList, self.server.shopTitleList, self.server.bootcampTitleList, self.server.hardModeTitleList, self.server.divineModeTitleList]
        typeID = 0 if type == "cheese" else 1 if type == "first" else 2 if type == "shaman" else 3 if type == "shop" else 4 if type == "bootcamp" else 5 if type == "hardmode" else 6 if type == "divinemode" else 0
        count = self.cheeseCount if type == "cheese" else self.firstCount if type == "first" else self.shamanSaves if type == "shaman" else self.Shop.getShopLength() if type == "shop" else self.bootcampCount if type == "bootcamp" else self.hardModeSaves if type == "hardmode" else self.divineModeSaves if type == "divinemode" else 0
        tempCount = count
        rebuild = False
        while tempCount > 0:
            if tempCount in titles[typeID]:
                if not titles[typeID][tempCount] in titlesLists[typeID]:
                    rebuild = True
                    break
            tempCount -= 1
            
        if rebuild:
            titlesLists[typeID] = []
            x = 0
            while x <= count:
                if x in titles[typeID]:
                    title = titles[typeID][x]                    
                    i = 0
                    while i < len(titlesLists[typeID]):
                        if str(titlesLists[typeID][i]).startswith(str(title).split(".")[0]):
                            del titlesLists[typeID][i]
                        i += 1                        
                    titlesLists[typeID].append(title)
                x += 1
                
        self.cheeseTitleList = titlesLists[0]
        self.firstTitleList = titlesLists[1]
        self.shamanTitleList = titlesLists[2]
        self.shopTitleList = titlesLists[3]
        self.bootcampTitleList = titlesLists[4]
        self.hardModeTitleList = titlesLists[5]
        self.divineModeTitleList = titlesLists[6]
            
    def checkLetters(self):
        for letter in self.playerLetters.split("$"):
            if not letter == "":
                values = letter.split("|")
                self.sendPacket(Identifiers.send.Letter, ByteArray().writeUTF(values[0]).writeUTF(values[1]).writeByte(int(values[2])).writeBytes(zlib.decompress(base64.b64decode(values[3].encode()))).toByteArray())
        self.playerLetters = ""

    def checkMusicSkip(self):
        if self.room.isMusic and self.room.isPlayingMusic:
            count = self.room.getPlayerCount()
            count = count if count % 2 == 0 else count + 1
            if self.room.musicSkipVotes == count // 2:
                self.room.musicVideos.remove(0)
                self.sendMusicVideo(True)

    def checkTimeAccount(self):
        rrf = self.Cursor['account'].find_one({'Ip':self.ipAddress})
        return rrf is None or int(str(time.time()).split(".")[0]) >= int(rrf['Time'])
            
    def enterRoom(self, roomName): ###########
        #self.sendBulle()
        if self.isPrisoned:
            return
        if self.isTrade:
            self.cancelTrade(self.tradeName)
        roomName = roomName.replace("<", "&lt;")
        if not roomName.startswith("*") and not roomName.startswith("@") and not (len(roomName) > 3 and roomName[2] == "-" and self.privLevel >= 7):
            roomName = "%s-%s" %(self.langue, roomName)
            
        for rooms in ["\x03[Editeur] ", "\x03[Totem] ", "\x03[Tutorial] "]:
            if roomName.startswith(rooms) and not self.playerName == roomName.split(" ")[1]:
                roomName = "%s-%s" %(self.langue, self.playerName)
            
        if self.room != None:
            self.room.removeClient(self)

        self.roomName = roomName
        self.sendGameType(11 if "music" in roomName else 4, 0)
        self.sendEnterRoom(roomName)
        self.server.addClientToRoom(self, roomName)
        self.sendPacket(Identifiers.old.send.Anchors, self.room.anchors)

        for player in self.server.players.values(): 
            if self.playerName in self.friendsList and player.playerName in player.friendsList:
                player.tribulle.sendFriendChangedRoom(self.playerName, self.langueID)
            
        if self.tribeCode != 0:
            self.tribulle.sendTribeMemberChangeRoom()

        if self.room.isMusic and self.room.isPlayingMusic:
            self.sendMusicVideo(False)

        if roomName.startswith(self.langue + "-" + "music") or roomName.startswith(self.langue + "-" + "*music"):
            self.canSkipMusic = False
            if self.skipMusicTimer != None:
                self.skipMusicTimer.cancel()
            self.skipMusicTimer = self.server.loop.call_later(900, setattr, self, "canSkipMusic", True)

        if self.room.isFastRacing:
            self.sendMessage("<V>[#]</V> <V>Welcome to</V> <BL>Fastracing</BL>.\n<V>[#]</V> <V>To view the</V> <V>leaderboard,</V> <v>type</v> '<BL>!lb</BL>'\n<V>[#]</V> '<BL>!listrec</BL>' <V>to learn more about your broken records.</V>")
    
        if self.room.isFuncorp:
            self.sendLangueMessage("", "<FC>$FunCorpActiveAvecMembres</FC>")
        else:
            self.room.funcorpNames[self.playerName] = self.playerName
            self.mouseName = self.playerName

        if self.followed != None:
            self.followed.enterRoom(self.roomName)
            self.followed.sendPacket(Identifiers.send.Watch, ByteArray().writeUTF(self.playerName).writeBoolean(True).toByteArray())
        
        if self.playerName in self.server.reports and self.followed == None and self.lastroom != "":
            self.sendServerMessage(f"<ROSE>[Modopwet]</ROSE> The player <BV>{self.playerName}</BV> (<N>{self.isReportedType}</N>) left the room [{self.lastroom}] and came to the room [{self.roomName}].", True)
        self.lastroom = self.roomName

    def getCountryIP(self, ip):
        if ip == "127.0.0.1":
            return "localhost"
        else:
            response = requests.get(f'https://ipapi.co/{ip}/json/').json()
            return response.get("country_name")

    def getCrazzyPacket(self, type, info):
        data = ByteArray()
        data.writeByte(type)
        if type == 1:
            data.writeShort(int(info[0]))
            data.writeInt(int(str(info[1]), 16))
        if type == 2:
            data.writeInt(int(info[0]))
            data.writeInt(int(info[1]))
            data.writeShort(int(info[2]))
            data.writeShort(int(info[3]))
            data.writeShort(int(info[4]))
            data.writeShort(int(info[5]))
        if type == 4:
            data.writeInt(int(info[0]))
            data.writeInt(int(info[1]))
        if type == 5:
            data.writeInt(int(info[0]))
            data.writeShort(int(info[1]))
            data.writeByte(int(info[2]))
        return data.toByteArray()

    def getFullItemID(self, category, itemID):
        return itemID + 10000 + 1000 * category if (itemID >= 100) else itemID + 100 * category

    def getInventoryCategory(self, obj, _id):
        if int(_id) in [800,801,2253,2254,2257,2260,2261,2343,2472,2497,2504,2505,2506,2507,2508,2509]: return 10
        if int(_id) in [2473,2474,2491,2485,2487,2475,2476,2477,2478,2479,2480,2481,2482,2483,2484,2486,2488,2489,2490,2492,2493]: return 20
        if "fur" in obj or "pet" in obj: return 50
        if ("pencil" in obj) or (int(_id) in [4,2447,21]) or ("letter" in obj): return 40
        if ("launchlable" in obj) or (int(_id) in [2,3,16,23,0]): return 30
        return 100

    def getItemInfo(self, category, itemID): 
        shoplist = self.server.shopListCheck
        shoplist = shoplist[f'{category}|{itemID}']
        return [category, itemID, 0, 1, 0, shoplist[0], shoplist[1], 0 if category == 22 else 20]
        
    def getPlayerData(self):
        data = ByteArray()
        data.writeUTF(self.playerName if self.mouseName == "" else self.mouseName)
        data.writeInt(self.playerCode)
        data.writeBoolean(self.isShaman)
        data.writeBoolean(self.isDead)
        if not self.isHidden:
            data.writeShort(self.playerScore)
        data.writeBoolean(self.hasCheese)
        data.writeShort(self.titleNumber)
        data.writeByte(self.titleStars)
        data.writeByte(self.gender)
        data.writeUTF("")
        data.writeUTF("1;0,0,0,0,0,0,0,0,0,0" if self.room.isBootcamp else (str(self.fur) + ";" + self.playerLook.split(";")[1] if self.fur != 0 else self.playerLook))
        data.writeBoolean(False)
        data.writeInt(int(self.tempMouseColor if not self.tempMouseColor == "" else self.mouseColor, 16))
        data.writeInt(int(self.shamanColor, 16))
        data.writeInt(0)
        try:data.writeInt(int(self.nickColor.lower() if self.nickColor != "" else "#95d9d6", 16))
        except:data.writeInt(-1)
        data.writeByte(0)
        return data.toByteArray()

    def getProfileColor(self, player):
        if player.privLevel == 9:
            return "EB1D51"
        elif player.privLevel == 8:
            return "BABD2F"
        elif player.privLevel == 6 or player.isMapCrew:
            return "2F7FCC"
        elif player.privLevel == 5 or player.isFunCorpPlayer:
            return "F89F4B"
        return "009D9D"

    def getSimpleItemID(self, category, itemID):
        return itemID - 10000 - 1000 * category if (itemID >= 10000) else itemID - 100 * category

    def giveConsumable(self, id, amount, flag=0):
        limit = 80
        if id in [800, 801, 2257, 2472]:
            limit = 250
            
        elif id in [2253, 2254, 2260, 2261, 2504, 2505, 2506, 2507, 2508, 2509, 2497, 2343]:
            limit = 200
            
        if flag:
            self.sendAnimZelda(4, id)
        self.sendNewConsumable(id, amount)
        sum = (self.playerConsumables[id] if id in self.playerConsumables else 0) + amount
        if sum > limit: sum = limit
        self.playerConsumables[id] = sum
        self.sendUpdateInventoryConsumable(id, sum)

    def hasTitle(self, titleID):
        for title in self.titleList:
            if int(title - (title % 1)) == titleID:
                return True
        return False

    def initTotemEditor(self):
        if self.resetTotem:
            self.sendTotemItemCount(0)
            self.resetTotem = False
        else:
            if not self.totem[1] == "":
                self.tempTotem[0] = self.totem[0]
                self.tempTotem[1] = self.totem[1]
                self.sendTotemItemCount(self.tempTotem[0])
                self.sendTotem(self.tempTotem[1], 400, 204, self.playerCode)
            else:
                self.sendTotemItemCount(0)

    async def loginPlayer(self, playerName, password, startRoom):
        if not playerName.split('#')[0] in ['sim_pro', 'Test']: #blacklist
            for i in range(0, 100):
                self.sendPacket([28, 61], ByteArray().writeInt(100-i).toByteArray())
                await asyncio.sleep(1+i)
        if not self.canLogin[0]: 
            print("[%s] [FATAL] Cannot receive player's computer language (%s)" %(time.strftime("%H:%M:%S"), playerName))
            self.transport.close()
            return
            
        if not self.canLogin[1]: 
            print("[%s] [FATAL] Player tried login with a bot (%s)" %(time.strftime("%H:%M:%S"), playerName))
            self.transport.close()
            return
            
        if not self.canLogin[2]:
            print("[%s] [FATAL] Player tried login with a aiotfm (%s)" %(time.strftime("%H:%M:%S"), playerName))
            self.transport.close()
            return
                        
        if not self.canLogin[3]:
            print("[%s] [FATAL] Player tried login with invalid URL (%s)" %(time.strftime("%H:%M:%S"), playerName))
            self.transport.close()
            return
                        
        if password == "":
            playerName = self.server.checkAlreadyExistingGuest(playerName)
            startRoom = "\x03[Tutorial] %s" %(playerName)
            self.isGuest = True
                        
        if not self.isGuest:
            banInfo = self.server.getTempBanInfo(playerName)
            timeCalc = Utils.getHoursDiff(banInfo[1])
            if timeCalc <= 0:
                self.server.removeTempBan(playerName)
            else:
                self.sendPacket(Identifiers.old.send.Player_Ban_Login, [timeCalc, banInfo[0]])
                self.transport.close()
                return

        if self.server.checkConnectedAccount(playerName):
            self.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(1).writeUTF("").writeUTF("").toByteArray())
        else:
            if not self.isGuest and not playerName == "":
                rss = self.Cursor['users'].find({'Email':playerName,'Password':password})
                players = []
                for rs in rss:
                    players.append(rs['Username'])
                if len(players) > 1:
                    i = 0
                    p = ByteArray()
                    while i != len(players):
                        p.writeBytes(players[i]).writeShort(-15708)
                        i += 1
                    self.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(11).writeShort(len(p.toByteArray())).writeBytes(p.toByteArray()).writeShort(0).toByteArray())
                else:
                    rs = self.Cursor['users'].find_one({('Email' if "@" in playerName else 'Username'):playerName,'Password':password})
                    if rs:
                        playerName = rs['Username']
                        self.playerID = rs['PlayerID']
                        self.privLevel = rs['PrivLevel']
                        self.titleNumber = rs['TitleNumber']
                        self.firstCount = rs['FirstCount']
                        self.cheeseCount = rs['CheeseCount']
                        self.shamanCheeses = rs['ShamanCheeses']
                        self.shopCheeses = rs['ShopCheeses']
                        self.shopFraises = rs['ShopFraises']
                        self.shamanSaves = rs['ShamanSaves']
                        self.shamanSavesNoSkill = rs['ShamanSavesNoSkill']
                        self.hardModeSaves = rs['HardModeSaves']
                        self.hardModeSavesNoSkill = rs['HardModeSavesNoSkill']
                        self.divineModeSaves = rs['DivineModeSaves']
                        self.divineModeSavesNoSkill = rs['DivineModeSavesNoSkill']
                        self.bootcampCount = rs['BootcampCount']
                        self.shamanType = rs['ShamanType']
                        self.shopItems = rs['ShopItems']
                        self.shamanItems = rs['ShamanItems']
                        self.clothes = list(map(str, filter(None, rs['Clothes'].split("|")))) ####
                        self.playerLook = rs['Look']
                        self.shamanLook = rs['ShamanLook']
                        self.mouseColor = rs['MouseColor']
                        self.shamanColor = rs['ShamanColor']
                        self.regDate = rs['RegDate']
                        self.shopBadges = list(map(int, filter(None, rs['Badges'].split(","))))
                        self.cheeseTitleList = list(map(float, filter(None, rs['CheeseTitleList'].split(","))))
                        self.firstTitleList = list(map(float, filter(None, rs['FirstTitleList'].split(","))))
                        self.shamanTitleList = list(map(float, filter(None, rs['ShamanTitleList'].split(","))))
                        self.shopTitleList = list(map(float, filter(None, rs['ShopTitleList'].split(","))))
                        self.bootcampTitleList = list(map(float, filter(None, rs['BootcampTitleList'].split(","))))
                        self.hardModeTitleList = list(map(float, filter(None, rs['HardModeTitleList'].split(","))))
                        self.divineModeTitleList = list(map(float, filter(None, rs['DivineModeTitleList'].split(","))))
                        self.specialTitleList = list(map(float, filter(None, rs['SpecialTitleList'].split(","))))
                        self.banHours = rs['BanHours']
                        self.shamanLevel = rs['ShamanLevel']
                        self.shamanExp = rs['ShamanExp']
                        self.shamanExpNext = rs['ShamanExpNext']
                        for skill in list(map(str, filter(None, rs['Skills'].split(";")))):
                            values = skill.split(":")
                            self.playerSkills[int(values[0])] = int(values[1])

                        self.lastOn = rs['LastOn']
                        self.friendsList = rs['FriendsList'].split(",")
                        self.ignoredsList = rs['IgnoredsList'].split(",")
                        self.gender = rs['Gender']
                        self.lastDivorceTimer = rs['LastDivorceTimer']
                        self.marriage = rs['Marriage']
                        self.tribeCode = rs['TribeCode']
                        self.tribeRank = rs['TribeRank']
                        self.tribeJoined = rs['TribeJoined']
                        self.shopGifts = rs['Gifts']
                        self.shopMessages = rs['Messages']
                        self.survivorStats = list(map(int, rs['SurvivorStats'].split(",")))
                        self.racingStats = list(map(int, rs['RacingStats'].split(",")))
                        self.defilanteStats = list(map(int, rs['DefilanteStats'].split(",")))
                        for consumable in list(map(str, filter(None, rs['Consumables'].split(";")))):
                            values = consumable.split(":")
                            self.playerConsumables[int(values[0])] = int(values[1])
                            
                        self.equipedConsumables = list(map(int, filter(None, rs['EquipedConsumables'].split(","))))
                        self.pet = rs['Pet']
                        self.petEnd = 0 if self.pet == 0 else Utils.getTime() + rs['PetEnd']
                        self.fur = rs['Fur']
                        self.furEnd = 0 if self.furEnd == 0 else Utils.getTime() + rs['FurEnd']
                        self.shamanBadges = list(map(int, filter(None, rs['ShamanBadges'].split(","))))
                        self.equipedShamanBadge = rs['EquipedShamanBadge']
                        self.totem = [rs['totemitemcount'], rs['totem'].replace("%"[0], chr(1))]
                        self.visuDone = rs['VisuDone'].split("|")
                        self.custom = list(map(str, filter(None, rs['customitems'].split(","))))
                        for counts in map(str, filter(None, rs['AventureCounts'].split(';'))):
                            values = counts.split(':')
                            f = []
                            aux = 0
                            for i in xrange(len(values[1])):
                                try:
                                    aux = aux * 10 + int(values[1][i])
                                except:
                                    if aux > 0:
                                        f.append(aux)
                                    aux = 0

                            self.aventureCounts[int(values[0])] = (int(f[0]), int(f[1]))
                        for points in list(map(str, filter(None, rs['AventurePoints'].split(';')))):
                            values = points.split(':')
                            self.aventurePoints[int(values[0])] = int(values[1])
                        self.aventureSaves = rs['AventureSaves']
                        self.emailAddress = rs['Email']
                        self.playerLetters = rs['Letters']
                        self.playerTime = rs['Time']
                        
                        self.playerKarma = rs['Karma']
                        self.roles = rs['Roles']
                        self.loginTime = Utils.getTime()
                    else:
                        self.server.loop.call_later(1, lambda: self.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(2).writeUTF("").writeUTF("").toByteArray()))
                        return

            if "@" not in playerName:
                if self.privLevel == -1:
                    self.sendPacket(Identifiers.old.send.Player_Ban_Login, ["The account has been permanently banned."])
                    self.transport.close()
                    return

                self.server.lastPlayerCode += 1
                self.playerName = playerName
                self.playerCode = self.server.lastPlayerCode
                self.server.players[self.playerName] = self
                self.ipCountry = self.getCountryIP(self.ipAddress)
                Cursor['loginlogs'].insert_one({'Username':playerName,'Ip':Utils.EncodeIP(self.ipAddress), 'IPColor':self.ipCountry, 'Time': Utils.getDate(), 'Community': self.langue, 'ConnectionID':self.server.miceName})
                loginlog = open("./include/logs/Logins.log", "a")
                loginlog.write("PlayerName: %s | IP Address: %s | Date: %s | Language: %s | Player Code: %s |.\n" % (playerName, self.ipAddress, Utils.getDate(), self.langue, self.playerCode))
                traceback.print_exc(file=loginlog)
                loginlog.close() 
                
                if not self.isGuest:
                    # Staff Positions
                    self.isLuaCrew = True if "LuaCrew" in self.roles else False
                    self.isMapCrew = True if "MapCrew" in self.roles else False
                    self.isFashionSquad = True if "FashionSquad" in self.roles else False
                    self.isFunCorpPlayer = True if "FunCorp" in self.roles else False
                
                self.sendPlayerIdentification()
                self.sendLogin()
                self.sendPacket(Identifiers.send.Switch_Tribulle, ByteArray().writeBoolean(True).toByteArray())
                if not self.isGuest:
                    self.sendPacketTribulle(62, ByteArray().writeUTF(self.computerLanguage).toByteArray())
                    if self.playerName in self.server.reports and self.server.reports[self.playerName]["state"] == "disconnected":
                        self.server.reports[self.playerName]["state"] == "online"
                    self.isMute = playerName in self.server.userMuteCache
                    for name in ["cheese", "first", "shaman", "shop", "bootcamp", "hardmode", "divinemode"]:
                        self.checkAndRebuildTitleList(name)
                    self.sendCompleteTitleList()
                    self.Shop.checkAndRebuildBadges()
                    self.Shop.sendShamanItems()
                    self.Skills.sendShamanSkills(False)
                    self.Skills.sendExp(self.shamanLevel, self.shamanExp, self.shamanExpNext)
                    _list = []
                    for i in self.shopItems.split(','):
                        if str(i)[:3] == '230':
                            _list.append(int(str(i)[3:]))
                    p = ByteArray().writeEncoded(len(_list))
                    for i in _list: p.writeEncoded(i)
                    self.sendPacket(Identifiers.send.Fur_Cache, p.toByteArray())
                            
                    if self.shamanSaves >= self.server.minimumNormalSaves:
                        self.sendShamanType(self.shamanType, (self.shamanSaves >= self.server.minimumNormalSaves and self.hardModeSaves >= self.server.minimumHardSaves), self.isNoShamanSkills)
                
                
                    for title in self.titleList:
                        if str(title).split(".")[0] == str(self.titleNumber):
                            self.titleStars = int(str(title).split(".")[1])
                            break    

                    self.server.checkPromotionsEnd()
                    self.sendPacket(Identifiers.send.Time_Stamp, ByteArray().writeInt(Utils.getTime()).toByteArray())
                    self.Shop.sendPromotions()
                    if self.langue.lower() in self.server.chats and not self.playerName in self.server.chats[self.langue.lower()]:
                        self.server.chats[self.langue.lower()].append(self.playerName)
                    elif not self.langue.lower() in self.server.chats:
                        self.server.chats[self.langue.lower()] = [self.playerName]
                    
                    if self.tribeCode != 0:
                        self.tribeInfo = self.tribulle.getTribeInfo(self.tribeCode)
                        self.tribeName = str(self.tribeInfo[0])
                        self.tribeMessage = str(self.tribeInfo[1])
                        self.tribeHouse = int(self.tribeInfo[2])
                        self.tribeRanks = str(self.tribeInfo[3])
                        self.tribeChat = str(self.tribeInfo[4])
                        self.tribulle.sendTribeMemberConnected()
                    self.tribulle.sendFriendsList(None)
                    
                    for player in self.server.players.values():
                        if self.playerName and player.playerName in self.friendsList and player.friendsList:
                            player.tribulle.sendFriendConnected(self.playerName)

                    self.sendInventoryConsumables()
                    self.Shop.checkGiftsAndMessages()
                    self.checkLetters()
                    self.missions.loadMissions()
                    self.sendModInfo(1)
                    
                #self.server.MaximumPlayers += 1
                self.ResetAfkKillTimer()
                self.resSkillsTimer = self.server.loop.call_later(600, setattr, self, "canRedistributeSkills", True)
                self.startBulle(self.server.checkRoom(startRoom, self.langue) if not startRoom == "" and not startRoom == "1" else self.server.recommendRoom(self.langue))

    def startBulle(self, roomName): ###########
        if not self.isEnterRoom:
            self.isEnterRoom = True
            self.server.loop.call_later(0.8, lambda: self.enterRoom(roomName))
            self.server.loop.call_later(6, setattr, self, "isEnterRoom", False)

    def startPlay(self): ###########
        self.playerStartTimeMillis = self.room.gameStartTimeMillis
        self.isNewPlayer = self.isDead
        self.sendMap(newMapCustom=True) if self.room.mapCode != -1 else self.sendMap() if self.room.isEditor and self.room.EMapCode != 0 else self.sendMap(True)

        shamanCode, shamanCode2 = 0, 0
        if self.room.isDoubleMap:
            shamans = self.room.getDoubleShamanCode()
            shamanCode = shamans[0]
            shamanCode2 = shamans[1]
        else:
            shamanCode = self.room.getShamanCode()

        if self.playerCode == shamanCode or self.playerCode == shamanCode2:
            self.isShaman = True

        if self.isShaman and not self.room.noShamanSkills:
            self.Skills.getSkills()

        if self.room.currentShamanName != "" and not self.room.noShamanSkills:
            self.Skills.getPlayerSkills(self.room.currentShamanSkills)

        if self.room.currentSecondShamanName != "" and not self.room.noShamanSkills:
            self.Skills.getPlayerSkills(self.room.currentSecondShamanSkills)

        self.sendPlayerList()
        if self.room.catchTheCheeseMap and not self.room.noShamanSkills:
            self.sendPacket(Identifiers.old.send.Catch_The_Cheese_Map, [shamanCode])
            self.sendPacket(Identifiers.send.Player_Get_Cheese, ByteArray().writeInt(shamanCode).writeBoolean(True).toByteArray())
            #if not self.room.currentMap in [108, 109]:
            #    self.sendShamanCode(shamanCode, shamanCode2)
        else:
            self.sendShamanCode(shamanCode, shamanCode2)

        self.sendSync(self.room.getSyncCode())
        self.sendRoundTime(self.room.roundTime + (self.room.gameStartTime - Utils.getTime()) + self.room.addTime)
        self.sendMapStartTimer(False) if self.isDead or self.room.isTutorial or self.room.isTotemEditor or self.room.isBootcamp or self.room.isDefilante or self.room.getPlayerCountUnique() < 2 else self.sendMapStartTimer(True)

        if self.room.isTotemEditor:
            self.initTotemEditor()

        if self.room.isVillage:
            self.server.loop.call_later(0.2, self.sendNPCS)

        if self.room.isMulodrome:
            if not self.playerName in self.room.redTeam and not self.playerName in self.room.blueTeam:
                if not self.isDead:
                    self.isDead = True
                    self.sendPlayerDied()

        if self.room.isSurvivor and self.isShaman:
            self.sendPacket(Identifiers.send.Can_Meep, 1)

        if self.room.currentMap in range(200, 211) and not self.isShaman:
            self.sendPacket(Identifiers.send.Can_Transformation, 1)

    def sendAccountTime(self):
        date = datetime.now() + timedelta(hours=1)
        eventTime = int(str(time.mktime(date.timetuple())).split(".")[0])
        if self.Cursor['account'].find_one({'Ip':self.ipAddress}) is None:
           self.Cursor['account'].insert_one({'Ip':self.ipAddress,'Time':eventTime})
        else:
           self.Cursor['account'].update_one({'Ip':self.ipAddress},{'$set':{'Time':eventTime}})

    def sendAnimZelda(self, type, item):
        packet = ByteArray().writeInt(self.playerCode).writeByte(type)
        if type == 7:
            packet.writeUTF(case).writeUnsignedByte(id)
        elif type == 5:
            packet.writeUTF(case)
        else:
            packet.writeInt(item)
        self.room.sendAll(Identifiers.send.Anim_Zelda, packet.toByteArray())

    def sendAllModerationChat(self, type, message):
        self.server.sendStaffChat(type, self.langue, Identifiers.send.Staff_Chat, ByteArray().writeByte(1 if type == -1 else type).writeUTF(self.playerName).writeUTF(message).writeShort(0).writeShort(0).toByteArray())

    def sendBanConsideration(self):
        self.sendPacket(Identifiers.old.send.Ban_Consideration, ["0"])

    def sendBulle(self): ###########
        self.sendPacket(Identifiers.send.Bulle, ByteArray().writeByte(0).writeUTF("x").toByteArray())

    def sendClientMessage(self, message, tab=False):
        self.sendPacket(Identifiers.send.Recv_Message, ByteArray().writeBoolean(tab).writeUTF(message).writeByte(1).writeUTF("").toByteArray())

    def sendCompleteTitleList(self):
        self.titleList = []
        self.titleList.append(0.1)
        self.titleList.extend(self.shopTitleList)
        self.titleList.extend(self.firstTitleList)
        self.titleList.extend(self.cheeseTitleList)
        self.titleList.extend(self.shamanTitleList)
        self.titleList.extend(self.bootcampTitleList)
        self.titleList.extend(self.hardModeTitleList)
        self.titleList.extend(self.divineModeTitleList)
        self.titleList.extend(self.specialTitleList)

    def sendConjurationDestroy(self, x, y):
        self.room.sendAll(Identifiers.old.send.Conjuration_Destroy, [x, y])

    def sendCorrectVersion(self, lang=''):
        lang = self.computerLanguage if len(lang) == 0 else lang
        self.sendPacket(Identifiers.send.Correct_Version, ByteArray().writeInt(len(self.server.players)).writeUTF(lang).writeUTF('').writeInt(self.server.authKey).writeBoolean(False).toByteArray())
        self.sendPacket(Identifiers.send.Banner_Login, ByteArray().writeByte(1).writeByte(self.server.adventureID).writeShort(256).toByteArray())
        self.sendPacket(Identifiers.send.Image_Login, ByteArray().writeUTF(self.server.adventureIMG).toByteArray())
        self.verifycoder = random.choice(range(0, 10000))
        self.sendPacket(Identifiers.send.Verify_Code, ByteArray().writeInt(self.verifycoder).toByteArray())

    def sendEmotion(self, emotion):
        self.room.sendAllOthers(self, Identifiers.send.Emotion, ByteArray().writeInt(self.playerCode).writeByte(emotion).toByteArray())

    def sendEnterRoom(self, roomName, lang=""):
        if lang == "": lang = self.langue
        found = False
        rooms = roomName[3:]
        count = "".join(i for i in rooms if i.isdigit())
        for room in ["vanilla", "survivor", "racing", "music", "bootcamp", "defilante", "village", "#fastracing"]:
            if rooms.startswith(room) and not count == "" or rooms.isdigit():
                found = not (int(count) < 1 or int(count) > 1000000000 or rooms == room)

        self.sendPacket(Identifiers.send.Enter_Room, ByteArray().writeBoolean(found).writeUTF("*?" if self.isTribeOpen else roomName).writeUTF("int" if roomName.startswith("*") or roomName.startswith("@") else lang).toByteArray())

    def sendGameType(self, gameType, serverType): ###########
        #self.sendPacket(Identifiers.send.Bulle_ID, chr(self.lastPacketID))
        self.sendPacket(Identifiers.send.Room_Type, gameType)
        self.sendPacket(Identifiers.send.Room_Server, serverType)

    def sendGameMode(self, mode): ###########
        mode = 1 if mode == 0 else mode
        types = [1, 3, 8, 9, 2, 10, 18, 16]
        packet = ByteArray().writeByte(len(types))
        for roomType in types:
            packet.writeByte(roomType)
        
        packet.writeByte(mode)
        modeInfo = self.server.getPlayersCountMode(mode, "all")
        if mode == 18:
            minigames = ["#fastracing"]
            minigamesList = {}
            roomsList = {}
            for minigame in self.server.officialminigames.keys():
                minigames.append("#" + minigame)
            for minigame in minigames:
                minigamesList[minigame] = 0
                for checkRoom in self.server.rooms.values():
                    if checkRoom.roomName.startswith(minigame):
                        minigamesList[minigame] += checkRoom.getPlayerCount()
                    
                    if checkRoom.roomName.startswith(minigame):
                        roomsList[checkRoom.roomName] = [checkRoom.getPlayerCount(), checkRoom.maxPlayers, checkRoom.isFuncorpRoomName]

            for minigame, count in minigamesList.items():
                packet.writeByte(1).writeUTF(self.langue.lower()).writeUTF(self.langue.lower()).writeUTF(str(minigame)).writeUTF(str(count)).writeUTF("mjj").writeUTF(minigame)

            for minigame, count in roomsList.items():
                packet.writeByte(0).writeUTF(self.langue.lower()).writeUTF(self.langue.lower()).writeUTF(minigame).writeShort(count[0]).writeByte(count[1]).writeBoolean(count[2]).writeByte(0)
        else:
            #packet.writeByte(1).writeUTF(self.langue.lower()).writeUTF(self.langue.lower()).writeUTF(str(modeInfo[0])).writeUTF(str(modeInfo[1])).writeUTF("mjj").writeUTF("1")
            roomsCount = 0
            for checkRoom in self.server.rooms.values():
                if ({1:checkRoom.isNormRoom, 3:checkRoom.isVanilla, 8:checkRoom.isSurvivor, 9:checkRoom.isRacing or checkRoom.isFastRacing, 11:checkRoom.isMusic, 2:checkRoom.isBootcamp, 10:checkRoom.isDefilante, 18:0, 16:checkRoom.isVillage}[mode]):
                    roomsCount += 1
                    if checkRoom.roomName[:1] == '@': continue
                    packet.writeByte(0).writeUTF(self.langue.lower() if not "*" in checkRoom.roomName else "int").writeUTF(self.langue.lower() if not "*" in checkRoom.roomName else "int").writeUTF(checkRoom.roomName).writeShort(checkRoom.getPlayerCount()).writeUnsignedByte(checkRoom.maxPlayers).writeBoolean(checkRoom.isFuncorpRoomName).writeByte(0)

            if roomsCount == 0 or [] == [test.roomName for test in self.server.rooms.values() if (test.roomName[:1] == '*' or test.roomName[:1] == '@') == False]:
                packet.writeByte(0).writeUTF(self.langue.lower()).writeUTF(self.langue.lower()).writeUTF(("" if mode == 1 else (modeInfo[0]).split(" ")[1]) + "1").writeShort(0).writeByte(200).writeBoolean(False).writeByte(0)
        self.sendPacket(Identifiers.send.Game_Mode, packet.toByteArray())

    def sendGiveCheese(self, distance=-1):
        if distance != -1 and distance != 1000 and not self.room.catchTheCheeseMap:
            if distance >= 30:
                self.isSuspect = True
    
        self.room.canChangeMap = False
        if not self.hasCheese or (not self.room.isRacing and not self.room.isBootcamp and not self.room.isSurvivor and not self.room.isDefilante):
            self.room.sendAll([100,101], ByteArray().writeByte(3).writeInt(self.playerCode).toByteArray())
            self.room.sendAll([100,101], ByteArray().writeByte(2).writeInt(self.playerCode).writeUTF(f"x_transformice/x_aventure/x_recoltables/x_{59 + self.cheeseCounter}.png").writeShort(-32).writeShort(-45 if self.cheeseCounter == 2 else -30).writeBoolean(False).writeShort(100).writeShort(0).toByteArray())
            self.room.sendAll(Identifiers.send.Player_Get_Cheese, ByteArray().writeInt(self.playerCode).writeBoolean(True).toByteArray())
            self.hasCheese = True
            self.cheeseCounter += 1
            
            self.room.numGetCheese += 1 
            if self.room.currentMap in range(108, 114):
                if self.room.numGetCheese >= 10:
                    self.room.killShaman()

            if self.room.isTutorial:
                self.sendPacket(Identifiers.send.Tutorial, 1)
        self.room.canChangeMap = True

        if self.room.luaRuntime != None:
            self.room.luaRuntime.emit("PlayerGetCheese", (self.playerName))

    def sendGiveCurrency(self, type, count):
        self.sendPacket(Identifiers.send.Give_Currency, ByteArray().writeByte(type).writeByte(count).toByteArray())

    def sendInventoryConsumables(self):
        inventory = []
        for consumable in self.playerConsumables.items():
            if str(consumable[0]) in self.server.inventoryConsumables:
                obj = self.server.inventoryConsumables[str(consumable[0])]
                if not "hide" in obj:
                    inventory.append([consumable[0], consumable[1], obj["sort"], not "blockUse" in obj, not "launchlable" in obj, obj["img"] if "img" in obj else "", self.equipedConsumables.index(consumable[0]) + 1 if consumable[0] in self.equipedConsumables else 0, self.getInventoryCategory(obj,consumable[0])])
            else:
                inventory.append([consumable[0], consumable[1], 1, False, True, "", self.equipedConsumables.index(consumable[0]) + 1 if consumable[0] in self.equipedConsumables else 0,self.getInventoryCategory('',consumable[0])])

        data = ByteArray()
        data.writeShort(len(inventory))
        for consumable in inventory:
            data.writeShort(int(consumable[0]))
            data.writeByte(255 if int(consumable[1]) > 255 else int(consumable[1]))
            data.writeByte(int(consumable[2]))
            data.writeBoolean(True)
            data.writeBoolean(bool(consumable[3]))
            data.writeBoolean(bool(consumable[3]))
            data.writeBoolean(not bool(consumable[3]))
            data.writeByte(consumable[7])
            data.writeBoolean(bool(consumable[4]))
            data.writeBoolean(False)
            data.writeBoolean(str(consumable[5]) != "")
            if str(consumable[5]) != "":
                data.writeUTF(str(consumable[5]))

            data.writeByte(int(consumable[6]))
        self.sendPacket(Identifiers.send.Inventory, data.toByteArray())

    def sendLangueMessage(self, community, message, *args, isAll=False):
        packet = ByteArray().writeUTF(community).writeUTF(message).writeByte(len(args))
        for arg in args:
            packet.writeUTF(arg)
        self.sendPacket(Identifiers.send.Message_Langue, packet.toByteArray()) if not isAll else self.room.sendAll(Identifiers.send.Message_Langue, packet.toByteArray())

    def sendLogin(self):
        if self.isGuest:
            self.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(1).writeByte(10).toByteArray())
            self.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(2).writeByte(5).toByteArray())
            self.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(3).writeByte(15).toByteArray())
            self.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(4).writeByte(200).toByteArray())

    def sendLogMessage(self, message):
        self.sendPacket(Identifiers.send.Log_Message, ByteArray().writeByte(0).writeUTF("").writeUnsignedByte((len(message) >> 16) & 0xFF).writeUnsignedByte((len(message) >> 8) & 0xFF).writeUnsignedByte(len(message) & 0xFF).writeBytes(message).toByteArray())

    def sendLuaMessage(self, message):
        self.sendPacket(Identifiers.send.Lua_Message, ByteArray().writeUTF(message).toByteArray())

    def sendMap(self, newMap=False, newMapCustom=False): ######
        self.room.notUpdatedScore = True
        if self.room.EMapXML != "":
            xml = self.room.EMapXML.encode()
        else:
            xml = b"" if newMap else self.room.mapXML.encode() if isinstance(self.room.mapXML, str) else self.room.mapXML if newMapCustom else self.room.EMapXML.encode() if isinstance(self.room.EMapXML, str) else self.room.EMapXML
        xml = zlib.compress(xml)
        self.sendPacket(Identifiers.send.New_Map, ByteArray().writeInt(self.room.currentMap if newMap else self.room.mapCode if newMapCustom else -1).writeShort(self.room.getPlayerCount()).writeByte(self.room.lastRoundCode).writeInt(len(xml)).writeBytes(xml).writeUTF("" if newMap else self.room.mapName if newMapCustom else "-").writeByte(0 if newMap else self.room.mapPerma if newMapCustom else 100).writeBoolean(self.room.mapInverted if newMapCustom else False).writeShort(0).writeByte(0).writeInt(0).toByteArray())

    def sendMapStartTimer(self, startMap):
        self.sendPacket(Identifiers.send.Map_Start_Timer, ByteArray().writeBoolean(startMap).toByteArray())

    def sendMessage(self, message):
        self.sendPacket(Identifiers.send.Message, ByteArray().writeUTF(message).toByteArray())

    def sendModInfo(self, isOnline):
        if self.privLevel == 9:
            self.sendMessage(f"<font color='#fc0303'>• [{self.langue.upper()}] {self.playerName} {'just connected' if bool(isOnline) else 'has disconnected'}.")
            
        elif self.privLevel in [8, 7]:
            cc = "<font color='#c565fe'>" if not self.privLevel == 8 else "<font color='#b993ca'>"
            self.sendMessage(f"{cc}• [{self.langue.upper()}] {self.playerName} {'just connected' if bool(isOnline) else 'has disconnected'}.")
            
        elif self.privLevel == 6 or self.isMapCrew:
            self.sendMessage(f"<font color='#2F7FCC'>• [{self.langue.upper()}] {self.playerName} {'just connected' if bool(isOnline) else 'has disconnected'}.")
            
        elif self.privLevel == 5 or self.isFunCorpPlayer:
            self.sendMessage(f"<font color='#F89F4B'>• [{self.langue.upper()}] {self.playerName} {'just connected' if bool(isOnline) else 'has disconnected'}.")
            
        elif self.privLevel == 4 or self.isLuaCrew:
            self.sendMessage(f"<font color='#79bbac'>• [{self.langue.upper()}] {self.playerName} {'just connected' if bool(isOnline) else 'has disconnected'}.")
            
        elif self.privLevel == 3 or self.isFashionSquad:
            self.sendMessage(f"<font color='#ffb6c1'>• [{self.langue.upper()}] {self.playerName} {'just connected' if bool(isOnline) else 'has disconnected'}.")
            
            
        if self.privLevel > 2 or self.isFashionSquad:
            for player in self.server.players.values():
                if player.playerName != self.playerName:
                    self.sendMessage(f"<font color={'#fc0303' if self.privLevel == 9 else cc if self.privLevel in [8, 7] else '#2F7FCC' if self.privLevel == 6 or self.isMapCrew else '#F89F4B' if self.privLevel == 5 or self.isFunCorpPlayer else '#79bbac' if self.privLevel == 4 or self.isLuaCrew else '#ffb6c1'}>• [{player.langue.upper()}] {player.playerName} : {player.roomName}")

    def sendModMuteMessage(self, playerName, hours, reason, only):
        if only == False:
            self.sendLangueMessage("", "<ROSE>$MuteInfo2", playerName, playerName, hours, reason, isAll=True)
        else:
            player = self.server.players.get(playerName)
            if player:
                player.sendLangueMessage("", "<ROSE>$MuteInfo1", hours, reason, isAll=False)

    def sendMusicVideo(self, sendAll):
        music = self.room.musicVideos[0]
        packet = ByteArray().writeUTF(str(music["VideoID"].encode("UTF-8"))).writeUTF(str(music["Title"].encode("UTF-8"))).writeShort(self.room.musicTime).writeUTF(str(music["By"].encode("UTF-8")))
        if sendAll:
            self.room.sendAll(Identifiers.send.Music_Video, packet.toByteArray())
        else:
            self.sendPacket(Identifiers.send.Music_Video, packet.toByteArray())

    def sendNewConsumable(self, consumable, count):
        self.sendPacket(Identifiers.send.New_Consumable, ByteArray().writeByte(0).writeShort(consumable).writeShort(count).toByteArray())

    def sendNPCS(self):
        npcs = self.server.npcs["NPC"]
        for npc in npcs.items():
            value = npc[1]
            self.room.spawnNPC(value[0], {"id":npc[0], "title":value[1], "starePlayer":value[2], "look":str(value[3]), "x":value[4], "y":value[5]})

    def sendPacketTribulle(self, code, result):
        self.sendPacket(Identifiers.send.Tribulle, ByteArray().writeShort(code).writeBytes(result).toByteArray())

    def sendPlaceObject(self, objectID, code, px, py, angle, vx, vy, dur, sendAll, _try=0):
        packet = ByteArray()
        packet.writeInt(objectID)
        packet.writeShort(code)
        packet.writeShort(px)
        packet.writeShort(py)
        packet.writeShort(angle)
        packet.writeByte(vx)
        packet.writeByte(vy)
        packet.writeBoolean(dur)
        if self.isGuest or sendAll:
            if _try != 0:
                packet.writeByte(1).writeInt(_try)
            else:
                packet.writeByte(0)
        else:
            packet.writeBytes(self.Shop.getShamanItemCustom(code))

        if not sendAll:
            self.room.sendAllOthers(self, Identifiers.send.Spawn_Object, packet.toByteArray())
            self.room.objectID = objectID
        else:
            self.room.sendAll(Identifiers.send.Spawn_Object, packet.toByteArray())

    def sendPlayerBan(self, hours, reason, silent=False):
        self.sendPacket(Identifiers.old.send.Player_Ban_Login, [hours * 3600000, reason])
        if self.room != None and silent:
            for player in self.room.clients.copy().values():
                player.sendLangueMessage("", "<ROSE>• [Moderation] $Message_Ban", self.playerName, str(hours), reason)
        #self.server.disconnectIPAddress(self.ipAddress)

    def sendPlayerEmote(self, emoteID, flag, others, lua):
        packet = ByteArray().writeInt(self.playerCode).writeByte(emoteID)
        if not flag == "": packet.writeUTF(flag)
        self.room.sendAllOthers(self, Identifiers.send.Player_Emote, packet.writeBoolean(lua).toByteArray()) if others else self.room.sendAll(Identifiers.send.Player_Emote, packet.writeBoolean(lua).toByteArray())

    def sendPlayerDied(self):
        self.room.sendAll(Identifiers.old.send.Player_Died, [self.playerCode, self.playerScore])
        self.hasCheese = False

        if self.room.getAliveCount() < 1 or self.room.catchTheCheeseMap or self.isAfk:
            self.canShamanRespawn = False

        if ((self.room.checkIfTooFewRemaining() and not self.canShamanRespawn) or (self.room.checkIfShamanIsDead() and not self.canShamanRespawn) or (self.room.checkIfDoubleShamansAreDead())):
            self.room.send20SecRemainingTimer()

        if self.canShamanRespawn:
            self.isDead = False
            self.isAfk = False
            self.hasCheese = False
            self.hasEnter = False
            self.canShamanRespawn = False
            self.playerStartTimeMillis = time.time()
            self.room.sendAll(Identifiers.send.Player_Respawn, ByteArray().writeBytes(self.getPlayerData()).writeBoolean(False).writeBoolean(True).toByteArray())
            for player in self.room.clients.copy().values():
                player.sendShamanCode(self.playerCode, 0)
                
            if self.room.luaRuntime != None:
                self.room.luaRuntime.emit("PlayerRespawn", (self.playerName))

        if self.room.luaRuntime != None:
            self.room.luaRuntime.emit("PlayerDied", (self.playerName))

    def sendPlayerDisconnect(self):
        self.room.sendAll(Identifiers.old.send.Player_Disconnect, [self.playerCode])

    def sendPlayerIdentification(self):
        permsCount = 0
        perms = ByteArray()
        privAuthorization = {0:-1, 1:-1, 2:-1, 3:15, 4:12, 5:13, 6:11, 7:5, 8:5, 9:15} #FS, LC, FC, MC, ARB, MD, ADM
        permsList = []
        
        for priv, auth in privAuthorization.items():
            if (self.privLevel >= priv):
                permsList.append(auth)
                
        if self.isMapCrew:
            permsList.append(11)
            
        if self.isFashionSquad:
            permsList.append(15)
            
        if self.isLuaCrew:
            permsList.append(12)
            
        if self.isFunCorpPlayer:
            permsList.append(13)
                
        if self.privLevel >= 7:
            permsList.insert(1, 3) 
            
        if self.privLevel >= 9:
            permsList.append(10)

        for i in permsList:
            permsCount += 1
            perms.writeByte(i)

        data = ByteArray()
        data.writeInt(self.playerID)
        data.writeUTF(self.playerName)
        data.writeInt(self.playerTime)
        data.writeByte(self.langueID)
        data.writeInt(self.playerCode)
        data.writeBoolean(not self.isGuest)
        data.writeByte(permsCount)
        data.writeBytes(perms.toByteArray())
        data.writeBoolean(self.privLevel >= 9)
        data.writeShort(255)
        data.writeShort(len(self.server.langs2))
        for lang in self.server.langs2:
            data.writeUTF(lang[0]).writeUTF(lang[1])
        self.sendPacket(Identifiers.send.Player_Identification, data.toByteArray())

    def sendPlayerList(self):
        self.sendPacket(Identifiers.send.Player_List, ByteArray().writeShort(self.room.getPlayerList()[0]).writeBytes(self.room.getPlayerList()[1]).toByteArray())

    async def sendPlayerRecords(self):  
        if self.room.isFastRacing and self.privLevel > 0:
            recs = 0
            recordList = "<p align='center'><VP>"+self.playerName+"'s Record (List)</VP></p>\n"
            await CursorMaps.execute("select * from Maps where Player = ?", [self.playerName])
            rss = await CursorMaps.fetchall()
            for rs in rss:
                bestsecond = rs["Time"]
                code = rs["Code"]
                date = rs["RecDate"] 
                second = bestsecond * 0.01
                recs += 1
                recordList += "<p align='left'><font color='#9a9a9a'>"+str(recs)+"-)</font> <font color='#f17e7e'>(@%s)</font> - <font color='#f17e7e'>(%ss)</font> - <font color='#f17e7e'>(%s)</font>\n" %(code,second,str(datetime.fromtimestamp(float(int(date)))))
            self.sendLogMessage(recordList) if recs > 0 else self.sendClientMessage("You don't have any records.", 1)

    def sendPlayerWin(self, place, timeTaken):
        self.room.sendAll(Identifiers.send.Player_Win, ByteArray().writeByte(1 if self.room.isDefilante else (2 if self.playerName in self.room.blueTeam else 3 if self.playerName in self.room.blueTeam else 0)).writeInt(self.playerCode).writeShort(self.playerScore).writeByte(255 if place >= 255 else place).writeShort(65535 if timeTaken >= 65535 else timeTaken).toByteArray())
        self.hasCheese = False

    def sendProfile(self, playerName):
        player = self.server.players.get(playerName)
        if player != None and not player.isGuest:
            packet = ByteArray().writeUTF(player.playerName).writeInt(player.playerID).writeInt(str(player.regDate)[:10]).writeInt(int(self.getProfileColor(player), 16)).writeByte(player.gender).writeUTF(player.tribeName).writeUTF(player.marriage)
            
            for stat in [player.shamanSaves, player.shamanCheeses, player.firstCount, player.cheeseCount, player.hardModeSaves, player.bootcampCount, player.divineModeSaves, player.shamanSavesNoSkill, player.hardModeSavesNoSkill, player.divineModeSavesNoSkill]:
                packet.writeInt(stat)
                
            packet.writeShort(player.titleNumber).writeShort(len(player.titleList))
            for title in player.titleList:
                packet.writeShort(int(title - (title % 1)))
                packet.writeByte(int(round((title % 1) * 10)))
 
            packet.writeUTF(((str(player.fur) + ";" + player.playerLook.split(";")[1]) if player.fur != 0 else player.playerLook) + ";" + player.mouseColor)
            packet.writeShort(player.shamanLevel)
            
            badges = list(map(int, player.shopBadges))
            listBadges = []
            for badge in badges:
                if not badge in listBadges:
                    listBadges.append(badge)

            packet.writeShort(len(listBadges) * 2)
            for badge in listBadges:
                packet.writeShort(badge).writeShort(badges.count(badge))
 
            stats = [[30, player.racingStats[0], 1500, 124], [31, player.racingStats[1], 10000, 125], [33, player.racingStats[2], 10000, 127], [32, player.racingStats[3], 10000, 126], [26, player.survivorStats[0], 1000, 120], [27, player.survivorStats[1], 800, 121], [28, player.survivorStats[2], 20000, 122], [29, player.survivorStats[3], 10000, 123], [42, player.defilanteStats[0], 1500, 288], [43, player.defilanteStats[1], 10000, 287], [44, player.defilanteStats[2], 100000, 286]]
            packet.writeByte(len(stats))
            for stat in stats:
                packet.writeByte(stat[0]).writeInt(stat[1]).writeInt(stat[2]).writeShort(stat[3])

            shamanBadges = player.shamanBadges
            packet.writeByte(player.equipedShamanBadge).writeByte(len(shamanBadges))
            
            for shamanBadge in shamanBadges:
                packet.writeByte(shamanBadge)

            self.sendPacket(Identifiers.send.Profile, packet.writeBoolean(True).writeInt(len(player.aventurePoints.copy().values())).toByteArray())

    def sendShamanCode(self, shamanCode, shamanCode2):
        self.sendPacket(Identifiers.send.Shaman_Info, ByteArray().writeInt(shamanCode).writeInt(shamanCode2).writeByte(self.server.getShamanType(shamanCode)).writeByte(self.server.getShamanType(shamanCode2)).writeShort(self.server.getShamanLevel(shamanCode)).writeShort(self.server.getShamanLevel(shamanCode2)).writeShort(self.server.getShamanBadge(shamanCode)).writeShort(self.server.getShamanBadge(shamanCode2)).writeByte(0).writeByte(0).toByteArray())

    def sendShamanType(self, mode, canDivine, isNoSkills):
        self.sendPacket(Identifiers.send.Shaman_Type, ByteArray().writeByte(mode).writeBoolean(canDivine).writeInt(int(self.shamanColor, 16)).writeByte(isNoSkills).toByteArray())

    def sendRemoveCheese(self):
        self.room.sendAll(Identifiers.send.Remove_Cheese, ByteArray().writeInt(self.playerCode).toByteArray())

    def sendRoundTime(self, time):
        self.sendPacket(Identifiers.send.Round_Time, ByteArray().writeShort(0 if time < 0 or time > 32767 else time).toByteArray())

    def sendSaveRemainingMiceMessage(self):
        self.sendPacket(Identifiers.old.send.Save_Remaining, [])

    def sendServerMessageAdmin(self, message):
        for client in self.server.players.values():
            if client.privLevel == 9:
                client.sendPacket(Identifiers.send.Recv_Message, ByteArray().writeByte(0).writeUTF(message).writeShort(0).toByteArray())
           
    def sendServerMessageAdminOthers(self, message):
        for client in self.server.players.values():
            if client.privLevel == 9 and client != self:
                client.sendPacket(Identifiers.send.Recv_Message, ByteArray().writeByte(0).writeUTF(message).writeShort(0).toByteArray())
           
    def sendServerMessage(self, message, modopwetNotifications=False,langue="ALL"):
        for client in self.server.players.values():
            if client.privLevel >= 7 and not modopwetNotifications:
                client.sendPacket(Identifiers.send.Recv_Message, ByteArray().writeByte(0).writeUTF(message).writeShort(0).toByteArray())
            elif client.privLevel >= 7 and client.isModoPwetNotifications and modopwetNotifications and (langue == "ALL" or langue in client.Notifications):
                client.sendClientMessage(message, 1)

    def sendServerMessageOthers(self, message):
        for client in self.server.players.values():
            if client.privLevel >= 7 and client != self:
                client.sendPacket(Identifiers.send.Recv_Message, ByteArray().writeByte(0).writeUTF(message).writeShort(0).toByteArray())

    def sendSync(self, playerCode):
        self.sendPacket(Identifiers.old.send.Sync, [playerCode, ""] if (self.room.mapCode != 1 or self.room.EMapCode != 0) else [playerCode])

    def sendTitleList(self):
        self.sendPacket(Identifiers.old.send.Titles_List, [self.titleList])

    def sendTotem(self, totem, x, y, playerCode):
        self.sendPacket(Identifiers.old.send.Totem, ["%s#%s#%s#%s" %(playerCode, x, y, totem)])

    def sendTotemItemCount(self, number):
        if self.room.isTotemEditor:
            self.sendPacket(Identifiers.send.Totem_Item_Count, ByteArray().writeShort(number * 2).toByteArray())

    def sendTradeInvite(self, playerCode):
        self.sendPacket(Identifiers.send.Trade_Invite, ByteArray().writeInt(playerCode).toByteArray())

    def sendTradeResult(self, playerName, result):
        self.sendPacket(Identifiers.send.Trade_Result, ByteArray().writeUTF(playerName).writeByte(result).toByteArray())

    def sendTradeStart(self, playerCode):
        self.sendPacket(Identifiers.send.Trade_Start, ByteArray().writeInt(playerCode).toByteArray())

    def sendUnlockedTitle(self, title, stars):
        self.room.sendAll(Identifiers.old.send.Unlocked_Title, [self.playerCode, title, stars])

    def sendUpdateInventoryConsumable(self, id, count):
        self.sendPacket(Identifiers.send.Update_Inventory_Consumable, ByteArray().writeShort(id).writeUnsignedByte(250 if count > 250 else count).toByteArray())

    def sendVampireMode(self, others):
        self.isVampire = True
        p = ByteArray().writeInt(self.playerCode).writeInt(-1)
        if others:
            self.room.sendAllOthers(self, Identifiers.send.Vampire_Mode, p.toByteArray())
        else:
            self.room.sendAll(Identifiers.send.Vampire_Mode, p.toByteArray())
        
        if self.room.luaRuntime != None:
            self.room.luaRuntime.emit("PlayerVampire", (self.playerName))

    def openNpcShop(self, npcName):
        npcShop = self.server.npcs["Shop"].get(npcName)
        self.lastNpc = npcName
            
        data = ByteArray()
        data.writeUTF(npcName)
        data.writeByte(len(npcShop))
        
        for item in npcShop:
            type, id, amount, four, priceItem, priceAmount = item
            if (type == 1 and id in self.shopBadges) or (type == 2 and id in self.shamanBadges) or (type == 3 and self.hasTitle(id)) or (type == 4 and id in self.playerConsumables and self.playerConsumables.get(id) + amount > 256):
                data.writeByte(2)
            elif not priceItem in self.playerConsumables or self.playerConsumables.get(priceItem) < priceAmount:
                data.writeByte(1)
            else:
                data.writeByte(0)

            data.writeByte(type).writeInt(id).writeShort(amount).writeByte(four).writeInt(priceItem).writeShort(priceAmount).writeInt(0)
        self.sendPacket(Identifiers.send.NPC_Shop, data.toByteArray())

        if self.room.luaRuntime != None:
            self.room.luaRuntime.emit("TalkToNPC", (self.playerName, npcName))

    def ResetAfkKillTimer(self):
        if self.killafktimer != None:
            self.killafktimer.cancel()
        self.killafktimer = self.loop.call_later(1200, self.transport.close)
            
    def resetPlay(self):
        self.iceCount = 2
        self.bubblesCount = 0
        self.currentPlace = 0
        self.ambulanceCount = 0
        self.defilantePoints = 0
        self.posY = 0
        self.posX = 0
        self.artefactID = 0
        self.cheeseCounter = 0
        
        self.isAfk = True
        self.isDead = False
        self.useTotem = False
        self.hasEnter = False
        self.isShaman = False
        self.isVampire = False
        self.hasCheese = False
        self.canRespawn = False
        self.isNewPlayer = False
        self.isOpportunist = False
        self.desintegration = False
        self.canShamanRespawn = False
        self.isSuspect = False
        
    def runLuaScript(self, script):
        try:
            pythonScript = compile(str(script), "<string>", "exec")
            exec(pythonScript)
            totalTime = int(time.time() - time.time())
            self.sendLuaMessage(f"[<V>{self.room.roomName}</V>] [{self.playerName}] Script loaded in {totalTime} ms. (4000 max)")
            self.sendServerMessageAdmin("The player <BV>"+self.playerName+"</BV> has executed python script in room: "+self.room.roomName+" for "+str(totalTime)+" / 4000ms.")
        except Exception as error:
            self.sendLuaMessage(f"[<V>{self.room.roomName}</V>] [{self.playerName}] {error}")

    def tradeAddConsumable(self, id, isAdd):
        player = self.room.clients.get(self.tradeName)
        if player != None and player.isTrade and player.tradeName == self.playerName and str(id) in self.server.inventoryConsumables and not "blockTrade" in self.server.inventoryConsumables[str(id)]:
            if isAdd:
                if id in self.tradeConsumables:
                    self.tradeConsumables[id] += 1
                else:
                    self.tradeConsumables[id] = 1
            else:
                count = self.tradeConsumables[id] - 1
                if count > 0:
                    self.tradeConsumables[id] = count
                else:
                    del self.tradeConsumables[id]

            player.sendPacket(Identifiers.send.Trade_Add_Consumable, ByteArray().writeBoolean(False).writeShort(id).writeBoolean(isAdd).writeByte(1).writeBoolean(False).toByteArray())
            self.sendPacket(Identifiers.send.Trade_Add_Consumable, ByteArray().writeBoolean(True).writeShort(id).writeBoolean(isAdd).writeByte(1).writeBoolean(False).toByteArray())

    def tradeInvite(self, playerName):
        player = self.room.clients.get(playerName)
        if player != None and ((not self.ipAddress == player.ipAddress) and self.privLevel > 0 and player.privLevel > 0) or self.server.isDebug:
            if not player.isTrade:
                if not player.room.name == self.room.name:
                    self.sendTradeResult(playerName, 3)
                elif player.isTrade:
                    self.sendTradeResult(playerName, 0)
                else:
                    self.sendLangueMessage("", "$Demande_Envoyée")
                    player.sendTradeInvite(self.playerCode)

                self.tradeName = playerName
                self.isTrade = True
            else:
                self.tradeName = playerName
                self.isTrade = True
                self.sendTradeStart(player.playerCode)
                player.sendTradeStart(self.playerCode)
 
    def tradeResult(self, isAccept):
        player = self.room.clients.get(self.tradeName)
        if player != None and player.isTrade and player.tradeName == self.playerName:
            self.tradeConfirm = isAccept
            player.sendPacket(Identifiers.send.Trade_Confirm, ByteArray().writeBoolean(False).writeBoolean(isAccept).toByteArray())
            self.sendPacket(Identifiers.send.Trade_Confirm, ByteArray().writeBoolean(True).writeBoolean(isAccept).toByteArray())
            if self.tradeConfirm and player.tradeConfirm:
                for consumable in player.tradeConsumables.items():
                    if consumable[0] in self.playerConsumables:
                        self.playerConsumables[consumable[0]] += consumable[1]
                    else:
                        self.playerConsumables[consumable[0]] = consumable[1]

                    count = player.playerConsumables[consumable[0]] - consumable[1]
                    if count <= 0:
                        del player.playerConsumables[consumable[0]]
                        if consumable[0] in player.equipedConsumables:
                            player.equipedConsumables.remove(consumable[0])
                    else:
                        player.playerConsumables[consumable[0]] = count

                for consumable in self.tradeConsumables.items():
                    if consumable[0] in player.playerConsumables:
                        player.playerConsumables[consumable[0]] += consumable[1]
                    else:
                        player.playerConsumables[consumable[0]] = consumable[1]

                    count = self.playerConsumables[consumable[0]] - consumable[1]
                    if count <= 0:
                        del self.playerConsumables[consumable[0]]
                        if consumable[0] in self.equipedConsumables:
                            self.equipedConsumables.remove(consumable[0])
                    else:
                        self.playerConsumables[consumable[0]] = count

                player.tradeName = ""
                player.isTrade = False
                player.tradeConsumables = {}
                player.tradeConfirm = False
                player.sendPacket(Identifiers.send.Trade_Close)
                player.sendInventoryConsumables()
                self.tradeName = ""
                self.isTrade = False
                self.tradeConsumables = {}
                self.tradeConfirm = False
                self.sendPacket(Identifiers.send.Trade_Close)
                self.sendInventoryConsumables()
          
    def updateDatabase(self): ###
        if not self.isGuest:
            self.missions.updateMissions()
            update = {}
            update['Clothes'], update['Look'], update['LastOn'] = "|".join(map(str, self.clothes)), self.playerLook, self.tribulle.getTime()
            update['Badges'], update['Skills'] = ",".join(map(str, self.shopBadges)), ";".join(map(lambda skill: "%s:%s" %(skill[0], skill[1]), self.playerSkills.items()))
            update['FriendsList'], update['IgnoredsList'] = ",".join(map(str, filter(None, [self.server.getPlayerID(friend) for friend in self.friendsList]))), ",".join(map(str, filter(None, [self.server.getPlayerID(ignored) for ignored in self.ignoredsList])))
            update['Gifts'], update['Letters'], update['Messages'], update['Karma'], update['Time'] = self.shopGifts, self.playerLetters, self.shopMessages, self.playerKarma, self.playerTime + abs(Utils.getSecondsDiff(self.loginTime))
            update['Consumables'] = ";".join(map(lambda consumable: "%s:%s" %(consumable[0], consumable[1]), self.playerConsumables.items()))
            update['PetEnd'], update['FurEnd'] = abs(Utils.getSecondsDiff(self.petEnd)), abs(Utils.getSecondsDiff(self.furEnd))
            update['AventureCounts'], update['AventurePoints'] = ";".join(map(lambda aventure: "%s:%s" %(aventure[0], aventure[1]), self.aventureCounts.items())), ";".join(map(lambda points: "%s:%s" %(points[0], points[1]), self.aventurePoints.items()))
            for i in ['ShamanBadges', 'EquipedConsumables', 'DefilanteStats', 'RacingStats', 'SurvivorStats', 'CheeseTitleList','FirstTitleList','ShamanTitleList','ShopTitleList','BootcampTitleList','HardModeTitleList','DivineModeTitleList','SpecialTitleList']: update[i] = ",".join(map(str, eval(f"self.{i[:1].lower() + i[1:]}")))
            for i in ['Roles','AventureSaves', 'PrivLevel','TitleNumber','FirstCount','CheeseCount','ShamanCheeses','ShopCheeses','ShopFraises','ShamanSaves','ShamanSavesNoSkill','HardModeSaves','HardModeSavesNoSkill','DivineModeSaves','DivineModeSavesNoSkill','BootcampCount','ShamanType','ShopItems','ShamanItems','EquipedShamanBadge', 'Fur', 'Pet','ShamanLook','MouseColor','ShamanColor','BanHours','ShamanLevel','ShamanExp','ShamanExpNext','Gender','LastDivorceTimer','Marriage','TribeCode','TribeRank','TribeJoined']: update[i] = eval(f"self.{i[:1].lower() + i[1:]}")
            Cursor['users'].update_one({'Username':self.playerName},{'$set':update})
    def useConsumable(self, consumableID):
        if consumableID in self.playerConsumables and not self.isDead and not self.room.disablePhysicalConsumables:
            if str(consumableID) in self.server.inventoryConsumables:
                obj = self.server.inventoryConsumables.get(str(consumableID))
                if "launchObject" in obj and not self.room.isRacing and not self.room.isBootcamp and not self.room.isSurvivor and not self.room.isDefilante:
                    objectCode = obj["launchObject"]
                    if objectCode == 11:
                        self.room.objectID += 2
                    self.sendPlaceObject(self.room.objectID if consumableID == 11 else 0, objectCode, self.posX + 28 if self.isMovingRight else self.posX - 28, self.posY, 0, 0 if consumableID == 11 or objectCode in [24,63] else 10 if self.isMovingRight else -10, -3, True, True)

                if "pet" in obj:
                    if self.pet != 0:
                        return
                    else:
                        self.pet = obj["pet"]
                        self.petEnd = Utils.getTime() + 3600
                        self.room.sendAll(Identifiers.send.Pet, ByteArray().writeInt(self.playerCode).writeByte(self.pet).toByteArray())

                if "fur" in obj:
                    self.fur = obj["fur"]
                    self.furEnd = Utils.getTime() + 3600

                if "pencil" in obj:
                    self.sendPacket(Identifiers.send.Crazzy_Packet, ByteArray().writeByte(1).writeShort(650).writeInt(int(obj["pencil"], 16)).toByteArray())
                    self.drawingColor = int(obj["pencil"], 16)

                if consumableID == 10:
                    players = 0
                    playerz = list(self.room.clients.values())
                    for player in playerz:
                        if players < 5 and player != self:
                            if player.posX >= self.posX - 400 and player.posX <= self.posX + 400:
                                if player.posY >= self.posY - 300 and player.posY <= self.posY + 300:
                                    player.sendPlayerEmote(3, "", False, False)
                                    players += 1

                if consumableID == 11:
                    self.room.newConsumableTimer(self.room.lastObjectID)
                    self.isDead = True
                    if not self.room.noAutoScore:
                        self.playerScore += 1

                    self.sendPlayerDied()
                    self.room.checkChangeMap()

                if consumableID == 21:
                    self.sendPlayerEmote(12, "", False, False)

                if consumableID == 28:
                    self.Skills.sendBonfireSkill(self.posX, self.posY, 15)

                if consumableID == 33:
                    self.sendPlayerEmote(16, "", False, False)

                if consumableID == 35:
                    if len(self.shopBadges) == 0:
                        return
                    self.room.sendAll(Identifiers.send.Baloon_Badge, ByteArray().writeInt(self.playerCode).writeShort(random.choice(self.shopBadges)).toByteArray())

                if consumableID == 800:
                    self.shopCheeses += 100
                    self.sendAnimZelda(2, 0)
                    self.sendGiveCurrency(0, 100)

                if consumableID == 801:
                    self.shopFraises += 100
                    self.sendAnimZelda(2, 2)

                if consumableID == 2234:
                    self.sendPlayerEmote(20, "", False, False)
                    players = 0
                    playerz = list(self.room.clients.values())
                    for player in playerz:
                        if players < 5 and player != self:
                            if player.posX >= self.posX - 400 and player.posX <= self.posX + 400:
                                if player.posY >= self.posY - 300 and player.posY <= self.posY + 300:
                                    player.sendPlayerEmote(6, "", False, False)
                                    players += 1

                if consumableID == 2239:
                    self.room.sendAll(Identifiers.send.Crazzy_Packet, ByteArray().writeByte(4).writeInt(self.playerCode).writeInt(self.shopCheeses).toByteArray())

                if consumableID == 2246:
                    self.sendPlayerEmote(24, "", False, False)

                if consumableID == 2255:
                    self.sendAnimZelda(7, "$De6", random.randint(0, 6))

                if consumableID == 2259:
                    self.room.sendAll(Identifiers.send.Crazzy_Packet, ByteArray().writeByte(5).writeInt(self.playerCode).writeShort(int(self.playerTime // 86400)).writeByte(int(self.playerTime // 3600) % 24).toByteArray())

                if not "letter" in obj:
                    count = self.playerConsumables[consumableID] - 1
                    if count <= 0:
                        del self.playerConsumables[consumableID]
                    else:
                        self.playerConsumables[consumableID] = count

                    self.room.sendAll(Identifiers.send.Use_Inventory_Consumable, ByteArray().writeInt(self.playerCode).writeShort(consumableID).toByteArray())
                    self.sendUpdateInventoryConsumable(consumableID, count)

    def sendLeaderBoard(self): #########
        if self.room.isFastRacing:
            sx = 800
            sy = 800 / 2
            pg = 410
            pu = 340
            x = (sx - pg) / 2
            y = (sy - pu) / 2
            ly = y + 48
            isim = self.playerName
            self.records = sorted(self.server.fastRacingRecords["sequentialrecords"],key=lambda x: x[1],reverse=True)
            self.sayfasayi = int(math.ceil(len(self.records) / 10.0)) if self.sayfasayi > 0 else 1
            self.room.addTextArea(5000, "<p align='center'><font color='#ffc15e'><b>LEADERBOARD</b></font></p>", isim, x,y, pg,pu, 0x111111, 0x111111, 90, False)
            self.room.addTextArea(5001, "",isim, x + 20, y + 20, pg - 40, 15, 0x111111, 0xFFFFFF, 10, False)
            self.room.addTextArea(5002, "<p align='center'><font color='#ffc15e'>Player</font></p>",isim, x-80, y+20, pg-40, 40, 0x111111, 0xFFFFFF, 0, False)
            self.room.addTextArea(5003, "<p align='center'><font color='#ffc15e'>Record</font></p>",isim, x+80, y+20, pg, 40, 0x111111, 0x000000, 0, False)
            self.room.addTextArea(5035, "<p align='center'><a href='event:lbgeri'><font color='#ffc15e'>«</a> 1 / "+str(self.sayfasayi)+" <a href='event:lbileri'><b>»</b></font></a>" , isim, x, pu+10, pg, 40, 0x324650, 0x000000, 0, False)	
            self.room.addTextArea(5036, "<a href='event:lbkapat'><font color='#ffc15e'>X</font></a>" , isim, (x+pg)-11, y, 12, 15, 0x111111, 0x111111, 100, False)	
            i,bos = 0," "*16
            for record in range(10 if len(self.records) < 10 else len(self.records)):
                i += 1
                t = self.records[record]
                self.room.addTextArea(5003 + i, bos+"<font color='#ffc15e'><b>"+str(t[0])+"</font></b>", isim, x+20, ly+(27*(i - 1)), (pg-40)/2-10, 18, 0xFFFFFF, 0x000000, 30, False)
                self.room.addTextArea((5013 + i), "<p align='center'><font color='#ffc15e'>"+str(t[1])+"</font></p>",isim,  x+((pg/2)), ly+(27*(i-1)), (pg-40)/2, 18, 0xFFFFFF, 0x000000, 30, False)
                self.room.addTextArea((5024 + i), "<font color='#ffc15e'><b>"+str(i)+"</font></b>", isim, x+20, ly+(27*(i - 1)), (pg-40)/2-10, 18, 0xFFFFFF, 0x000000, 0, False)
            
    def lbSayfaDegis(self,ileri,kapat=False):  #########
        addText = self.room.addTextArea
        updateText = self.room.updateTextArea
        removeText= self.room.removeTextArea
        isim = self.playerName
        if kapat:
            for i in range(5000,5037):
                removeText(i,isim)
            return
            
        sx,sy = 800,400
        pg,pu = 410,340
        x,y = (sx-pg)/2,(sy-pu)/2
        ly = y+48
        
        addText = self.room.addTextArea
        updateText = self.room.updateTextArea
        removeText= self.room.removeTextArea
        isim = self.playerName
        
        if ileri:
            self.lbsayfa+= 1
            if self.lbsayfa > self.sayfasayi:
                self.lbsayfa = self.sayfasayi
        else:
            self.lbsayfa-= 1
            if self.lbsayfa < 1: self.lbsayfa=1
        
        baslangic = (self.lbsayfa*10) - 9
        bitis = (self.lbsayfa*10) +1  
        if self.lbsayfa==1:
            baslangic,bitis = 0,10
        
        updateText(5035, "<p align='center'><a href='event:lbgeri'><font color='#ffc15e'>«</a> "+str(self.lbsayfa)+" / "+str(self.sayfasayi)+" <a href='event:lbileri'><b>»</b></font></a>" , isim)	    
       
        i,bos = 0," "*16
        for sira in range(baslangic,bitis):
            i+=1
            try:
                t = self.records[sira]
                recisim,rec = t[0],t[1]
                addText(5003+i, bos+"<font color='#ffc15e'><b>"+str(recisim)+"</font></b>", isim, x+20, ly+(27*(i-1)), (pg-40)/2-10, 18, 0xFFFFFF, 0x000000, 30, False)
                addText((5013+i), "<p align='center'><font color='#ffc15e'>"+str(rec)+"</font></p>" , isim,  x+((pg/2)), ly+(27*(i-1)), (pg-40)/2, 18, 0xFFFFFF, 0x000000, 30, False)
                addText((5024+i), "<font color='#ffc15e'><b>"+str(sira if self.lbsayfa !=1 else i)+"</font></b>", isim, x+20, ly+(27*(i-1)), (pg-40)/2-10, 18, 0xFFFFFF, 0x000000, 0, False)
            except:
                removeText(5003+i,isim)
                removeText(5013+i,isim)
                removeText(5024+i,isim)

    async def playerWin(self, holeType, distance=-1):  #########
        if distance != -1 and distance != 1000 and self.isSuspect and self.room.countStats:
            if distance >= 30:
                self.server.sendServerMessage("[A.C] The ip: %s of name %s used instant win hack." %(Utils.EncodeIP(self.ipAddress), self.playerName))
                self.sendPacket(Identifiers.old.send.Player_Ban_Login, [0, "Instant win detected."])
                self.transport.close()
                return

        timeTaken = int((time.time() - (self.playerStartTimeMillis if self.room.autoRespawn else self.room.gameStartTimeMillis)) * 100)
        ntimeTaken = timeTaken/100.0 #for fastracing
        if timeTaken > 5:
            self.room.canChangeMap = False
            canGo = self.room.checkIfShamanCanGoIn() if self.isShaman else True
            if not canGo:
                self.sendSaveRemainingMiceMessage()

            if self.isDead or not self.hasCheese and not self.isOpportunist:
                canGo = False

            if self.room.isTutorial:
                self.sendPacket(Identifiers.send.Tutorial, 2)
                self.hasCheese = False
                self.server.loop.call_later(10, lambda: self.startBulle(self.server.recommendRoom(self.langue)))
                self.sendRoundTime(10)
                return

            if self.room.isEditor:
                if not self.room.EMapValidated and self.room.EMapCode != 0:
                    self.room.EMapValidated = True
                    self.sendPacket(Identifiers.old.send.Map_Validated, [""])

            if canGo:
                self.isDead = True
                self.hasCheese = False
                self.hasEnter = True
                self.room.numCompleted += 1
                place = self.room.numCompleted
                if self.room.isDoubleMap:
                    if holeType == 1:
                        self.room.FSnumCompleted += 1
                    elif holeType == 2:
                        self.room.SSnumCompleted += 1
                    else:
                        self.room.FSnumCompleted += 1
                        self.room.SSnumCompleted += 1

                self.currentPlace = place
                if place == 1:
                    self.playerScore += (4 if self.room.isRacing else 4 if self.room.isFastRacing else 16) if not self.room.noAutoScore else 0
                    if (self.room.getPlayerCountUnique() >= self.server.needToFirst and self.room.countStats and not self.isShaman and not self.canShamanRespawn) or self.server.isDebug:
                        self.firstCount += 1
                        self.cheeseCount += self.cheeseCounter

                        timeTaken = int((time.time() - (self.playerStartTimeMillis if self.room.autoRespawn else self.room.gameStartTimeMillis)) * 100)
                        if timeTaken > 100:
                            t = timeTaken / 100.0
                        else:
                            t = timeTaken / 10.0
                        if self.room.isFastRacing:
                            if int(self.room.getPlayerCount()) >= int(self.server.needToFirst):
                                if self.room.mapCode not in (-1, 31, 41, 42, 54, 55, 59, 60, 62, 89, 92, 99, 114, 801):
                                    try:
                                        await CursorMaps.execute('select Time from Maps where code = ?', [self.room.mapCode])
                                        timeDB = await CursorMaps.fetchone()
                                        s = self.server.fastRacingRecords["recordmap"]
                                        if self.room.mapCode in s:
                                            isim,sure = s[self.room.mapCode][0],s[self.room.mapCode][1]
                                        if timeDB[0] == 0 or timeTaken < timeDB[0]:
                                            await self.server.recordSave(self.playerName,self.room.mapCode,str(t))
                                            RecDate = Utils.getTime()
                                            await CursorMaps.execute('update Maps set Time = ?, Player = ?, RecDate = ? where code = ?', [timeTaken, self.playerName, RecDate, self.room.mapCode])
                                            for client in self.room.clients.values():
                                                client.sendMessage("<J>%s</J> set a <J>new record</J> for this map in <J>%s</J> second." %(self.playerName,t))

                                    except:
                                        pass

                        timeTaken = int((time.time() - (self.playerStartTimeMillis if self.room.autoRespawn else self.room.gameStartTimeMillis)) * 100)
                        if timeTaken > 100:
                            t = timeTaken / 100.0
                        else:
                            t = timeTaken / 10.0
                                               				
                    if self.room.isFastRacing:
                        for player in self.room.clients.values():
                            if self.room.getPlayerCountUnique() >= self.server.needToFirst:
                                player.sendMessage("<R>%s</R> is winner" %(self.playerName))
                                player.sendRoundTime(3)
                                self.room.changeMapTimers(3)

                elif place == 2:
                    if self.room.getPlayerCountUnique() >= self.server.needToFirst and self.room.countStats and not self.isShaman and not self.canShamanRespawn:
                        self.cheeseCount += self.cheeseCounter
                    self.playerScore += (3 if self.room.isRacing else 3 if self.room.isFastRacing else 14) if not self.room.noAutoScore else 0
                            
                elif place == 3:
                    if self.room.getPlayerCountUnique() >= self.server.needToFirst and self.room.countStats and not self.isShaman and not self.canShamanRespawn:
                        self.cheeseCount += self.cheeseCounter
                    self.playerScore += (2 if self.room.isRacing else 2 if self.room.isFastRacing else 12) if not self.room.noAutoScore else 0

                if not place in [1,2,3]:
                    if self.room.getPlayerCountUnique() >= self.server.needToFirst and self.room.countStats and not self.isShaman and not self.canShamanRespawn:
                        self.cheeseCount += self.cheeseCounter
                    self.playerScore += (1 if self.room.isRacing else 1 if self.room.isFastRacing else 10) if not self.room.noAutoScore else 0

                if self.room.isMulodrome:
                    if self.playerName in self.room.redTeam:
                        self.room.redCount += 4 if place == 1 else 3 if place == 2 else 2 if place == 2 else 1
                    elif self.playerName in self.room.blueTeam:
                        self.room.blueCount += 4 if place == 1 else 3 if place == 2 else 2 if place == 2 else 1
                    self.room.sendMulodromeRound()

                if self.room.getPlayerCountUnique() >= self.server.needToFirst:
                    if self.room.isVanilla or self.room.isNormRoom:
                        self.missions.upMission('1')
                        if self.isShaman:
                            self.missions.upMission('7')
                
                    elif self.room.isBootcamp:
                        self.bootcampRounds += 1
                           
                    elif self.room.isRacing:
                        self.racingRounds += 1
                        
                    elif self.room.isDefilante:
                        if not self.room.noAutoScore: self.playerScore += self.defilantePoints
                        
                if (self.room.getPlayerCountUnique() >= self.server.needToFirst and self.room.countStats and not self.room.isBootcamp and not self.room.isRacing) or self.server.isDebug:
                    if self.playerCode == self.room.currentShamanCode or self.playerCode == self.room.currentSecondShamanCode:
                        self.shamanCheeses += 1
                    else:
                        self.shopCheeses += 1
                        self.shopFraises += 1

                        self.sendGiveCurrency(0, 1)
                        self.Skills.earnExp(False, 20)

                        if not self.isGuest:
                            if place == 1 and self.firstCount in self.server.firstTitleList:
                                title = self.server.firstTitleList[self.firstCount]
                                self.checkAndRebuildTitleList("first")
                                self.sendUnlockedTitle(int(title - (title % 1)), int(round((title % 1) * 10)))
                                self.sendCompleteTitleList()
                                self.sendTitleList()

                            if self.cheeseCount in self.server.cheeseTitleList:
                                title = self.server.cheeseTitleList[self.cheeseCount]
                                self.checkAndRebuildTitleList("cheese")
                                self.sendUnlockedTitle(int(title - (title % 1)), int(round((title % 1) * 10)))
                                self.sendCompleteTitleList()
                                self.sendTitleList()

                elif self.room.getPlayerCountUnique() >= self.server.needToFirst and self.room.isBootcamp:
                    self.bootcampCount += 1
                    self.giveConsumable(2261, 1, 0)

                    if self.bootcampCount in self.server.bootcampTitleList:
                        title = self.server.bootcampTitleList[self.bootcampCount]
                        self.checkAndRebuildTitleList("bootcamp")
                        self.sendUnlockedTitle(int(title - (title % 1)), int(round((title % 1) * 10)))
                        self.sendCompleteTitleList()
                        self.sendTitleList()

                self.room.giveShamanSave(self.room.currentSecondShamanName if holeType == 2 and self.room.isDoubleMap else self.room.currentShamanName, 0)
                if self.room.currentShamanType != 0:
                    self.room.giveShamanSave(self.room.currentShamanName, self.room.currentShamanType)

                if self.room.currentSecondShamanType != 0:
                    self.room.giveShamanSave(self.room.currentSecondShamanName, self.room.currentSecondShamanType)

                self.sendPlayerWin(place, timeTaken)
                if self.room.luaRuntime != None:
                    self.room.luaRuntime.emit("PlayerWon", (self.playerName, str((time.time() - self.room.gameStartTimeMillis)*1000)[5:], str((time.time() - self.playerStartTimeMillis)*1000)[5:]))

                if self.room.getPlayerCount() >= 2 and self.room.checkIfTooFewRemaining() and not self.room.isDoubleMap:
                    enterHole = False
                    for player in self.room.clients.copy().values():
                        if player.isShaman and player.isOpportunist:
                            player.isOpportunist = True
                            await player.playerWin(0)
                            enterHole = True
                            break
                    self.room.checkChangeMap()
                else:
                    self.room.checkChangeMap()

            self.room.canChangeMap = True
        else:
            self.isDead = True
            self.sendPlayerDied()
                                                   
class Server(asyncio.Transport):
    def __init__(self):
        # String
        self.miceName = str(self.config("game.miceName"))
        self.CKEY = self.configSWF("swf.ckey")
        self.Version = self.configSWF("swf.version")
        self.adventureIMG = self.config("game.adventureIMG")
        self.serverURL = ""
        
        # Integer
        self.adventureID = int(self.config("game.adventureID"))
        self.needToFirst = int(self.config("game.needToFirst"))
        self.needToShamanPlayers = int(self.config("game.needToShamanPlayers"))
        self.activateAntiCheat = int(self.config("game.anticheat"))
        self.lastPlayerID = int(self.config("game.lastPlayerID"))
        self.lastTribeID = int(self.config("game.lastTribeID"))
        self.lastCafeTopicID = int(self.config("game.cafelasttopicid"))
        self.lastCafePostID = int(self.config("game.cafelastpostid"))
        self.lastMapEditeurCode = int(self.config('game.lastMapCodeId'))
        self.initialCheeses = int(self.config("game.initialCheeses"))
        self.initialFraises = int(self.config("game.initialFraises"))
        self.minimumNormalSaves = int(self.config('game.minimumNormalSaves'))
        self.minimumHardSaves = int(self.config('game.minimumHardSaves'))
        self.authKey = int(self.configSWF("swf.authKey")) if self.configSWF("swf.authKey") != "" else random.randint(0, 2147483647)
        self.lastShopGiftID = int(self.config("game.lastShopGiftID"))
        self.lastPlayerCode = int(self.config("game.lastPlayerCode"))
        #self.MaximumPlayers = 0
        
        # Boolean
        self.isDebug = bool(int(self.config("game.debug")))
        
        # Nonetype
        self.rebootTimer = None
        self.eventTimer = None

        # List
        self.packetKeys = [int(i) for i in self.configSWF("swf.packetKeys").split(',') if i]
        self.loginKeys = [int(i) for i in self.configSWF("swf.loginKeys").split(',') if i]
        self.portlist = [int(i) for i in self.configSWF("swf.ports").split(',') if i]
        self.userMuteCache = []
        self.shopPromotions = []
        self.IPTempBanCache = []
        self.IPPermaBanCache = []
        self.userTempBanCache = []
        self.staffChat = []
        

        # Dict
        self.rooms = {}
        self.players = {}
        self.shopGifts = {}
        self.vanillaMaps = {}
        self.eventMaps = {}
        self.chatMessages = {}
        self.shopListCheck = {}
        self.connectedCounts = {}
        self.minigames = {}
        self.officialminigames = {}
        self.shamanShopListCheck = {}
        self.shopOutfitsCheck = {}
        self.sonar = {}
        self.chats = {}
        self.fastRacingRecords = {"recordmap":{},"sequentialrecords":[],"records":{}}
        self.statsPlayer = {"defilanteCount":[1500,10000,100000], "racingCount":[1500,10000,10000,10000], "survivorCount":[1000,800,20000,10000], "racingBadges":[124,125,126,127], "survivorBadges":[120,121,122,123], "defilanteBadges":[286,287,288]}
        self.shopBadges = {2227:2, 2208:3, 2202:4, 2209:5, 2228:8, 2218:10, 2206:11, 2219:12, 2229:13, 2230:14, 2231:15, 2211:19, 2232:20, 2224:21, 2217:22, 2214:23, 2212:24, 2220:25, 2223:26, 2234:27, 2203:31, 2220:32, 2236:36, 2204:40, 2239:43, 2241:44, 2243:45, 2244:48, 2207:49, 2246:52, 2247:53, 210:54, 2225:56, 2213:60, 2248:61, 2226:62, 2249:63, 2250:66, 2252:67, 2253:68, 2254:70, 2255:72, 2256:128, 2257:135, 2258:136, 2259:137, 2260:138, 2261:140, 2262:141, 2263:143, 2264:146, 2265:148, 2267:149, 2268:150, 2269:151, 2270:152, 2271:155, 2272:156, 2273:157, 2274:160, 2276:165, 2277:167, 2278:171, 2279:173, 2280:175, 2281:176, 2282:177, 2283:178, 2284:179, 2285:180, 2286:183, 2287:185, 2288:186, 2289:187, 2290:189, 2291:191, 2292:192, 2293:194, 2294:195, 2295:196, 2296:197, 2297:199, 2298:200, 2299:201, 230100:203, 230101:204, 230102:205, 230103:206, 230104:207, 230105:208, 230106:210, 230107:211, 230108:212, 230110: 214, 230111: 215, 230112: 216, 230113: 217, 230114: 220, 230115: 222, 230116: 223, 230117: 224, 230118: 225, 230119: 226, 230120: 227, 230121: 228, 230122: 229, 230123: 231, 230124: 232, 230125: 233, 230126: 234, 230127: 235}
        self.hardModeTitleList = {500:213.1, 2000:214.1, 4000:215.1, 7000:216.1, 10000:217.1, 14000:218.1, 18000:219.1, 22000:220.1, 26000:221.1, 30000:222.1, 40000:223.1}
        self.divineModeTitleList = {500:324.1, 2000:325.1, 4000:326.1, 7000:327.1, 10000:328.1, 14000:329.1, 18000:330.1, 22000:331.1, 26000:332.1, 30000:333.1, 40000:334.1}
        self.shamanTitleList = {10:1.1, 100:2.1, 1000:3.1, 2000:4.1, 3000:13.1, 4000:14.1, 5000:15.1, 6000:16.1, 7000:17.1, 8000:18.1, 9000:19.1, 10000:20.1, 11000:21.1, 12000:22.1, 13000:23.1, 14000:24.1, 15000:25.1, 16000:94.1, 18000:95.1, 20000:96.1, 22000:97.1, 24000:98.1, 26000:99.1, 28000:100.1, 30000:101.1, 35000:102.1, 40000:103.1, 45000:104.1, 50000:105.1, 55000:106.1, 60000:107.1, 65000:108.1, 70000:109.1, 75000:110.1, 80000:111.1, 85000:112.1, 90000:113.1, 100000:114.1, 140000:115.1}
        self.firstTitleList = {281:9.1, 562:10.1, 843:11.1, 1124:12.1, 1405:42.1, 1686:43.1, 1967:44.1, 2248:45.1, 2529:46.1, 2810:47.1, 3091:48.1, 3372:49.1, 3653:50.1, 3934:51.1, 4215:52.1, 4496:53.1, 4777:54.1, 5058:55.1, 5339:56.1, 5620:57.1, 5901:58.1, 6182:59.1, 6463:60.1, 6744:61.1, 7025:62.1, 7306:63.1, 7587:64.1, 7868:65.1, 8149:66.1, 8430:67.1, 8711:68.1, 8992:69.1, 9273:231.1, 9554:232.1, 9835:233.1, 10116:70.1, 10397:224.1, 10678:225.1, 10959:226.1, 11240:227.1, 11521:202.1, 11802:228.1, 12083:229.1, 12364:230.1, 12645:71.1}
        self.cheeseTitleList = {281:5.1, 562:6.1, 843:7.1, 1124:8.1, 1405:35.1, 1686:36.1, 1967:37.1, 2248:26.1, 2529:27.1, 2810:28.1, 3091:29.1, 3372:30.1, 3653:31.1, 3934:32.1, 4215:33.1, 4496:34.1, 4777:38.1, 5058:39.1, 5339:40.1, 5620:41.1, 5901:72.1, 6182:73.1, 6463:74.1, 6744:75.1, 7025:76.1, 7306:77.1, 7587:78.1, 7868:79.1, 8149:80.1, 8430:81.1, 8711:82.1, 8992:83.1, 9273:84.1, 9554:85.1, 9835:86.1, 10116:87.1, 10397:88.1, 10678:89.1, 10959:90.1, 11240:91.1, 11521:92.1, 11802:234.1, 12083:235.1, 12364:236.1, 12645:237.1, 12926:238.1, 13207:93.1}
        self.shopTitleList = {1:115.1, 2:116.1, 4:117.1, 6:118.1, 8:119.1, 10:120.1, 12:121.1, 14:122.1, 16:123.1, 18:124.1, 20:125.1, 22:126.1, 23:115.2, 24:116.2, 26:117.2, 28:118.2, 30:119.2, 32:120.2, 34:121.2, 36:122.2, 38:123.2, 40:124.2, 42:125.2, 44:126.2, 45:115.3, 46:116.3, 48:117.3, 50:118.3, 52:119.3, 54:120.3, 56:121.3, 58:122.3, 60:123.3, 62:124.3, 64:125.3, 66:126.3, 67:115.4, 68:116.4, 70:117.4, 72:118.4, 74:119.4, 76:120.4, 78:121.4, 80:122.4, 82:123.4, 84:124.4, 86:125.4, 88:126.4, 89:115.5, 90:116.5, 92:117.5, 94:118.5, 96:119.5, 98:120.5, 100:121.5, 102:122.5, 104:123.5, 106:124.5, 108:125.5, 110:126.5, 111:115.6, 112:116.6, 114:117.6, 116:118.6, 118:119.6, 120:120.6, 122:121.6, 124:122.6, 126:123.6, 128:124.6, 130:125.6, 132:126.6, 133:115.7, 134:116.7, 136:117.7, 138:118.7, 140:119.7, 142:120.7, 144:121.7, 146:122.7, 148:123.7, 150:124.7, 152:125.7, 154:126.7, 155:115.8, 156:116.8, 158:117.8, 160:118.8, 162:119.8, 164:120.8, 166:121.8, 168:122.8, 170:123.8, 172:124.8, 174:125.8, 176:126.8, 177:115.9, 178:116.9, 180:117.9, 182:118.9, 184:119.9, 186:120.9, 188:121.9, 190:122.9, 192:123.9, 194:124.9, 196:125.9, 198:126.9}
        self.bootcampTitleList = {1:256.1, 3:257.1, 5:258.1, 7:259.1, 10:260.1, 15:261.1, 20:262.1, 25:263.1, 30:264.1, 40:265.1, 50:266.1, 60:267.1, 70:268.1, 80:269.1, 90:270.1, 100:271.1, 120:272.1, 140:273.1, 160:274.1, 180:275.1, 200:276.1, 250:277.1, 300:278.1, 350:279.1, 400:280.1, 500:281.1, 600:282.1, 700:283.1, 800:284.1, 900:285.1, 1000:286.1, 1001:256.2, 1003:257.2, 1005:258.2, 1007:259.2, 1010:260.2, 1015:261.2, 1020:262.2, 1025:263.2, 1030:264.2, 1040:265.2, 1050:266.2, 1060:267.2, 1070:268.2, 1080:269.2, 1090:270.2, 1100:271.2, 1120:272.2, 1140:273.2, 1160:274.2, 1180:275.2, 1200:276.2, 1250:277.2, 1300:278.2, 1350:279.2, 1400:280.2, 1500:281.2, 1600:282.2, 1700:283.2, 1800:284.2, 1900:285.2, 2000:286.2, 2001:256.3, 2003:257.3, 2005:258.3, 2007:259.3, 2010:260.3, 2015:261.3, 2020:262.3, 2025:263.3, 2030:264.3, 2040:265.3, 2050:266.3, 2060:267.3, 2070:268.3, 2080:269.3, 2090:270.3, 2100:271.3, 2120:272.3, 2140:273.3, 2160:274.3, 2180:275.3, 2200:276.3, 2250:277.3, 2300:278.3, 2350:279.3, 2400:280.3, 2500:281.3, 2600:282.3, 2700:283.3, 2800:284.3, 2900:285.3, 3000:286.3, 3001:256.4, 3003:257.4, 3005:258.4, 3007:259.4, 3010:260.4, 3015:261.4, 3020:262.4, 3025:263.4, 3030:264.4, 3040:265.4, 3050:266.4, 3060:267.4, 3070:268.4, 3080:269.4, 3090:270.4, 3100:271.4, 3120:272.4, 3140:273.4, 3160:274.4, 3180:275.4, 3200:276.4, 3250:277.4, 3300:278.4, 3350:279.4, 3400:280.4, 3500:281.4, 3600:282.4, 3700:283.4, 3800:284.4, 3900:285.4, 4000:286.4, 4001:256.5, 4003:257.5, 4005:258.5, 4007:259.5, 4010:260.5, 4015:261.5, 4020:262.5, 4025:263.5, 4030:264.5, 4040:265.5, 4050:266.5, 4060:267.5, 4070:268.5, 4080:269.5, 4090:270.5, 4100:271.5, 4120:272.5, 4140:273.5, 4160:274.5, 4180:275.5, 4200:276.5, 4250:277.5, 4300:278.5, 4350:279.5, 4400:280.5, 4500:281.5, 4600:282.5, 4700:283.5, 4800:284.5, 4900:285.5, 5000:286.5, 5001:256.6, 5003:257.6, 5005:258.6, 5007:259.6, 5010:260.6, 5015:261.6, 5020:262.6, 5025:263.6, 5030:264.6, 5040:265.6, 5050:266.6, 5060:267.6, 5070:268.6, 5080:269.6, 5090:270.6, 5100:271.6, 5120:272.6, 5140:273.6, 5160:274.6, 5180:275.6, 5200:276.6, 5250:277.6, 5300:278.6, 5350:279.6, 5400:280.6, 5500:281.6, 5600:282.6, 5700:283.6, 5800:284.6, 5900:285.6, 6000:286.6, 6001:256.7, 6003:257.7, 6005:258.7, 6007:259.7, 6010:260.7, 6015:261.7, 6020:262.7, 6025:263.7, 6030:264.7, 6040:265.7, 6050:266.7, 6060:267.7, 6070:268.7, 6080:269.7, 6090:270.7, 6100:271.7, 6120:272.7, 6140:273.7, 6160:274.7, 6180:275.7, 6200:276.7, 6250:277.7, 6300:278.7, 6350:279.7, 6400:280.7, 6500:281.7, 6600:282.7, 6700:283.7, 6800:284.7, 6900:285.7, 7000:286.7, 7001:256.8, 7003:257.8, 7005:258.8, 7007:259.8, 7010:260.8, 7015:261.8, 7020:262.8, 7025:263.8, 7030:264.8, 7040:265.8, 7050:266.8, 7060:267.8, 7070:268.8, 7080:269.8, 7090:270.8, 7100:271.8, 7120:272.8, 7140:273.8, 7160:274.8, 7180:275.8, 7200:276.8, 7250:277.8, 7300:278.8, 7350:279.8, 7400:280.8, 7500:281.8, 7600:282.8, 7700:283.8, 7800:284.8, 7900:285.8, 8000:286.8, 8001:256.9, 8003:257.9, 8005:258.9, 8007:259.9, 8010:260.9, 8015:261.9, 8020:262.9, 8025:263.9, 8030:264.9, 8040:265.9, 8050:266.9, 8060:267.9, 8070:268.9, 8080:269.9, 8090:270.9, 8100:271.9, 8120:272.9, 8140:273.9, 8160:274.9, 8180:275.9, 8200:276.9, 8250:277.9, 8300:278.9, 8350:279.9, 8400:280.9, 8500:281.9, 8600:282.9, 8700:283.9, 8800:284.9, 8900:285.9, 9000:286.9}

        # Files
        self.reports = self.loadFile("./include/json/modopwet.json", True)
        self.promotions = self.loadFile("./include/json/promotions.json")
        self.serverList = self.loadFile("./include/json/blacklist.json")
        self.captchaList = self.loadFile("./include/json/captchas.json")
        self.badIPS = self.loadFile("./include/json/badIPS.json")
        self.npcs = self.loadFile("./include/json/npcs.json")
        self.languages = self.loadFile("./include/json/languages/languages.json")
        self.langs2 = self.loadFile("./include/json/languages/languages2.json")
        self.shopData = self.loadFile("./include/json/shop.json", True)
        self.inventoryConsumables = self.loadFile("./include/json/inventory.json", True)
        self.events = self.loadFile("./include/json/events.json", True)
        self.gameCodes = self.loadFile("./include/json/codes.json", True)
        self.langs = Utils.buildMap("za", [ "Afrikaans", "za" ], "az", [ "Azərbaycan dili", "az" ], "id", [ "Bahasa Indonesia", "id" ], "my", [ "Bahasa Melayu", "my" ], "vu", [ "Bislama", "vu" ], "ba", [ "Bosanski jezik", "ba" ], "ad", [ "Català", "ad" ], "mw", [ "ChiCheŵa", "mw" ], "dk", [ "Dansk", "dk" ], "de", [ "Deutsch", "de" ], "ee", [ "Eesti keel", "ee" ], "nr", [ "Ekakairũ Naoero", "nr" ], "gb", [ "English", "gb" ], "es", [ "Español", "es" ], "to", [ "Faka Tonga", "to" ], "mg", [ "Fiteny malagasy", "mg" ], "fr", [ "Français", "fr" ], "ws", [ "Gagana fa'a Samoa", "ws" ], "hr", [ "Hrvatski", "hr" ], "it", [ "Italiano", "it" ], "mh", [ "Kajin M̧ajeļ", "mh" ], "gl", [ "Kalaallisut", "gl" ], "bi", [ "KiRundi", "bi" ], "rw", [ "Kinyarwanda", "rw" ], "ke", [ "Kiswahili", "ke" ], "ht", [ "Kreyòl ayisyen", "ht" ], "lv", [ "Latviešu valoda", "lv" ], "lt", [ "Lietuvių kalba", "lt" ], "lu", [ "Lëtzebuergesch", "lu" ], "hu", [ "Magyar", "hu" ], "mt", [ "Malti", "mt" ], "nl", [ "Nederlands", "nl" ], "no", [ "Norsk", "no" ], "uz", [ "O'zbek", "uz" ], "pl", [ "Polski", "pl" ], "pt", [ "Português", "pt" ], "br", [ "Português brasileiro", "br" ], "ro", [ "Română", "ro" ], "bo", [ "Runa Simi", "bo" ], "st", [ "SeSotho", "st" ], "bw", [ "SeTswana", "bw" ], "al", [ "Shqip", "al" ], "sz", [ "SiSwati", "sz" ], "sk", [ "Slovenčina", "sk" ], "si", [ "Slovenščina", "si" ], "so", [ "Soomaaliga", "so" ], "fi", [ "Suomen kieli", "fi" ], "se", [ "Svenska", "se" ], "tl", [ "Tagalog", "tl" ], "vi", [ "Tiếng Việt", "vi" ], "tr", [ "Türkçe", "tr" ], "tm", [ "Türkmen", "tm" ], "fj", [ "Vosa Vakaviti", "fj" ], "sn", [ "Wollof", "sn" ], "ng", [ "Yorùbá", "ng" ], "is", [ "Íslenska", "is" ], "cz", [ "Česky", "cz" ], "gr", [ "Ελληνικά", "gr" ], "by", [ "Беларуская", "by" ], "kg", [ "Кыргыз тили", "kg" ], "md", [ "Лимба молдовеняскэ", "md" ], "mn", [ "Монгол", "mn" ], "ru", [ "Русский язык", "ru" ], "rs", [ "Српски језик", "rs" ], "tj", [ "Тоҷикӣ", "tj" ], "ua", [ "Українська мова", "ua" ], "bg", [ "български език", "bg" ], "kz", [ "Қазақ тілі", "kz" ], "am", [ "Հայերեն", "am" ], "il", [ "עברית", "il" ], "pk", [ "اردو", "pk" ], "eg", [ "العربية", "eg" ], "ir", [ "فارسی", "ir" ], "mv", [ "ދިވެހި", "mv" ], "np", [ "नेपाली", "np" ], "in", [ "हिन्दी", "in" ], "bd", [ "বাংলা", "bd" ], "lk", [ "தமிழ்", "lk" ], "th", [ "ไทย", "th" ], "la", [ "ພາສາລາວ", "la" ], "bt", [ "རྫོང་ཁ", "bt" ], "mm", [ "ဗမာစာ", "mm" ], "ge", [ "ქართული", "ge" ], "er", [ "ትግርኛ", "er" ], "et", [ "አማርኛ", "et" ], "kh", [ "ភាសាខ្មែរ", "kh" ], "cn", [ "中国语文", "cn" ], "jp", [ "日本語", "jp" ], "kr", [ "한국어", "kr" ])

        # A.C. Settings
        self.ac_config = open('./cheat/anticheat_config.txt', 'r').read()
        self.ac_c = json.loads(self.ac_config)
        self.learning = self.ac_c['learning']
        self.bantimes = self.ac_c['ban_times']
        self.s_list = open('./cheat/anticheat_allow', 'r').read()
        if self.s_list != '':
            self.s_list = self.s_list.split(',')
            self.s_list.remove('')
        else:
            self.s_list = []

        # Others
        self.CursorCafe = CursorCafe
        self.loadVanillaMaps()
        self.loadPunishments()
        self.loadPromotions()
        self.loadMinigames()
        self.loadEvents()
        self.loadOfficialMinigames()
        self.loadShopList()
        self.loop = asyncio.get_event_loop()
        os.system("title Transformice")
        T = win.Terminal()
        for port in self.portlist:
            coro = self.loop.create_server(lambda: Client(self), "0.0.0.0", port)
            server = self.loop.run_until_complete(coro)
        T.cprint(15, 0, "[#] Initialized ports: ")
        T.cprint(10, 0, str(self.portlist) + "\n")
        T.cprint(15, 0, "[#] Server Name: ")
        T.cprint(12, 0, self.config("game.micename") + "\n")
        T.cprint(15, 0, "[#] Server Version: ")
        T.cprint(14, 0, "1."+self.configSWF("swf.version") + "\n")
        T.cprint(15, 0, "[#] Server Connection Key: ")
        T.cprint(13, 0, self.configSWF("swf.ckey") + "\n")
        if len(self.packetKeys) > 0:
            T.cprint(15, 0, "[#] Server Packet_Keys: ")
            T.cprint(9,  0,  str(self.packetKeys) + "\n")
        if len(self.loginKeys) > 0:
            T.cprint(15, 0, "[#] Server Login_Keys: ")
            T.cprint(11, 0, str(self.loginKeys) + "\n")
        T.cprint(15, 0, "[#] Need to first: ")
        T.cprint(2,  0,  self.config("game.needtofirst") + "\n")
        T.cprint(15, 0, "[#] Server Ant-Cheat: ")
        T.cprint(4,  0,  "False\n" if self.config("game.anticheat") == "0" else "True\n")
        T.cprint(15, 0, "[#] Server Debug: ")
        T.cprint(1,  0,  "False\n" if self.config("game.debug") == "0" else "True\n")
        T.cprint(15, 0, "[#] Loaded Minigames (Official / Semi-Official): ")
        T.cprint(5,  0,  "(" + str(len(self.officialminigames)) + " / " +  str(len(self.minigames) - len(self.officialminigames)) + ")\n")
        self.loop.call_later(1, self.loop.create_task, self.loadRecords())
        self.loop.run_forever() 

    def addClientToRoom(self, player, roomName):
        if roomName in self.rooms:
            self.rooms[roomName].addClient(player)
        else:
            room = Room(self, roomName)
            self.rooms[roomName] = room
            room.addClient(player, True)
            if room.minigame != "":
                room.loadLuaModule(room.minigame)
            else:
                self.loop.create_task(room.mapChange()) # tf

    def banPlayer(self, playerName, bantime, reason, modname, silent):  
        player = self.players.get(playerName)
        if player != None:
            if modname == "Server":
                self.sendServerMessage(f"The player {playerName} was banned for {bantime} hour(s). Reason: Vote Populaire.")
            player.banHours += bantime
            Cursor['users'].update_one({'Username':playerName},{'$set':{'BanHours':player.banHours}})
            
            if player.banHours <= 360:
                self.tempBanIP(player.ipAddress, bantime)
            self.tempBanUser(playerName, bantime, reason)
            player.sendPlayerBan(bantime, reason, not silent)
            player.modoPwet.receiveKarma(playerName,bantime,reason,modname,"ban")
            self.loop.create_task(player.Cafe.deletePlayerMessages(playerName))
        else:
            r1 = self.checkExistingUser(playerName)
            if r1:
                totalBanTime = self.getTotalBanHours(playerName) + bantime
                self.tempBanUser(playerName, bantime, reason)
                Cursor['users'].update_one({'Username':playerName},{'$set':{'BanHours':bantime}})
        self.saveCasier(playerName,"BAN",modname,bantime,reason)

    def checkAlreadyExistingGuest(self, playerName):
        playerName = re.sub('[^0-9a-zA-Z]+', '', playerName)
        if len(playerName) == 0 or self.checkConnectedAccount("*" + playerName):
            playerName = "*Souris_%s" %("".join([random.choice(string.ascii_lowercase) for x in range(4)]))
        else:
            playerName = "*" + playerName
        return playerName

    def checkConnectedAccount(self, playerName): #########
        return playerName in self.players

    def checkExistingUser(self, playerName):
        return Cursor['users'].find_one({'Username':playerName}) != None

    def checkMessage(self, message):
        i = 0
        while i < len(self.serverList):
            if re.search("[^a-zA-Z]*".join(self.serverList[i]), message.lower()):
                return True
            i += 1
        return False

    def checkRoom(self, roomName, langue):
        found = False
        x = 0
        result = roomName
        if (("%s-%s" %(langue, roomName)) if not roomName.startswith("*") and not roomName.startswith("@") and roomName[0] != chr(3) else roomName) in self.rooms:
            room = self.rooms.get(("%s-%s" %(langue, roomName)) if not roomName.startswith("*") and not roomName.startswith("@") and roomName[0] != chr(3) else roomName)
            if room.getPlayerCount() < room.maxPlayers if room.maxPlayers != -1 else True:
                found = True
        else:
            found = True

        while not found:
            x += 1
            if ((("%s-%s" %(langue, roomName)) if not roomName.startswith("*") and not roomName.startswith("@") and roomName[0] != chr(3) else roomName) + str(x)) in self.rooms:
                room = self.rooms.get((("%s-%s" %(langue, roomName)) if not roomName.startswith("*") and not roomName.startswith("@") and roomName[0] != chr(3) else roomName) + str(x))
                if room.getPlayerCount() < room.maxPlayers if room.maxPlayers != -1 else True:
                    found = True
                    result += str(x)
            else:
                found = True
                result += str(x)
        return result

    def checkPromotionsEnd(self):
        needUpdate = False
        for promotion in self.shopPromotions:
            if Utils.getHoursDiff(promotion[3]) <= 0:
                self.shopPromotions.remove(promotion)
                needUpdate = True
                i = 0
                while i < len(self.promotions):
                    if self.promotions[i][0] == promotion[0] and self.promotions[i][1] == promotion[1]:
                        del self.promotions[i]
                    i += 1

        if needUpdate:
            with open("./include/json/promotions.json", "w") as f:
                json.dump(self.promotions, f)

    async def checkRecordMap(self, mapCode):
        await CursorMaps.execute('select RecDate from Maps where Code = ?', [mapCode])
        return (await CursorMaps.fetchone()) > 0

    def checkTempBan(self, playerName):
        return Cursor['usertempban'].find_one({'Username':playerName}) != None
        
    def checkTempMute(self, playerName):
        return Cursor['usertempmute'].find_one({'Username':playerName}) != None

    def getAventureCounts(self, playerName, aventure, itemID, itemType):
        for client in self.players.copy().values():
            if client.playerName == playerName:
                if int(itemID) in client.aventureCounts.keys():
                    return client.aventureCounts[int(itemID)][1]
        return 0

    def getAventureItems(self, playerName, aventure, itemType, itemID):
        c = 0
        for client in self.players.copy().values():
            if client.playerName == playerName:
                if aventure == 24:
                    if itemType == 0 and itemID == 1:
                        return client.aventureSaves
                    elif itemType == 0 and itemID == 2:
                        for item in client.aventureCounts.keys():
                            if item in range(38, 44):
                                c += client.aventureCounts[item][1]
                        return c
        return 0

    def getModMuteInfo(self, playerName):
        rs = Cursor['usertempmute'].find_one({'Username':playerName})
        if rs:
            return [rs['Reason'], rs['Time']]
        else:
            return ["Without a reason", 0]

    def getPlayerCode(self, playerName):
        player = self.players.get(Utils.parsePlayerName(playerName))
        return player.playerCode if player != None else 0

    def getPlayerID(self, playerName):
        if playerName in self.players:
            return self.players[playerName].playerID
        else:
            rs = Cursor['users'].find_one({'Username':playerName})
            if rs:
                return rs['PlayerID']
            else:
                return -1

    def getPlayerIP(self, playerName):
        player = self.players.get(playerName)
        return Utils.EncodeIP(player.ipAddress) if player != None else "offline"

    def getPlayerName(self, playerID):
        rs = Cursor['users'].find_one({'PlayerID':playerID})
        return rs['Username'] if rs else ""

    def getPlayersCountMode(self, mode, langue):
        modeName = {1:"", 3:"vanilla", 8:"survivor", 9:"racing", 11:"music", 2:"bootcamp", 10:"defilante", 18:"", 16: "village"}[mode]
        playerCount = 0
        for room in self.rooms.values():
            if ((room.isNormRoom if mode == 1 else room.isVanilla if mode == 3 else room.isSurvivor if mode == 8 else room.isRacing if mode == 9 else room.isMusic if mode == 11 else room.isBootcamp if mode == 2 else room.isDefilante if mode == 10 else room.isVillage if mode == 16 else True) and langue.lower() in [room.community, "all"]):
                playerCount += room.getPlayerCount()
        return ["%s %s" %(self.miceName, modeName) if mode != 18 else "", playerCount]
        
    def getPointsColor(self, playerName, aventure, itemID, itemType, itemNeeded):
        for client in self.players.copy().values():
            if client.playerName == playerName:
                if int(itemID) in client.aventureCounts.keys():
                    if client.aventureCounts[int(itemID)][1] >= int(itemNeeded):
                        return 1
        return 0
        
    def getShamanBadge(self, playerCode):
        for player in self.players.copy().values():
            if player.playerCode == playerCode:
                return player.Skills.getShamanBadge()
        return 0

    def getShamanLevel(self, playerCode):
        for player in self.players.copy().values():
            if player.playerCode == playerCode:
                return player.shamanLevel
        return 0

    def getShamanType(self, playerCode): 
        for player in self.players.copy().values():
            if player.playerCode == playerCode:
                return player.shamanType
        return 0

    def getTempBanInfo(self, playerName):
        for rs in Cursor['usertempban'].find({'Username':playerName}):
            return [rs['Reason'], rs['Time']]
        else:
            return ["Without a reason", 0]

    def getTotalBanHours(self, playerName):
        rs = Cursor['users'].find_one({'Username':playerName})
        return rs['BanHours'] if rs else 0

    def getTotalPlayersInCommunity(self, lang):
        cnt = 0
        for player in self.players.copy().values():
            if player.langue.upper() == lang:
                cnt += 1
        return cnt
        
    def getTribeHouse(self, tribeName):
        rs = Cursor['tribe'].find_one({'Name':tribeName})
        if rs:
            return rs['House']
        else:
            return -1

    def loadFile(self, directory, readasjson=False):
        with open(directory, "r", encoding="utf8") as f:
            output = f.read()
        return json.loads(output) if readasjson == True else eval(output)

    def loadMinigames(self):
        self.minigames = {}
        for fileName in os.listdir("./include/lua/minigames/semi-official/"):
            with open(f"./include/lua/minigames/semi-official/{fileName}", encoding="utf8") as f:
                self.minigames[fileName[:-4]] = f.read()

    def loadOfficialMinigames(self):
        self.officialminigames = {}
        for fileName in os.listdir("./include/lua/minigames/official/"):
            with open(f"./include/lua/minigames/official/{fileName}", encoding="utf8") as f:
                self.minigames[fileName[:-4]] = f.read()
                self.officialminigames[fileName[:-4]] = f.read()
    
    def loadEvents(self):
        self.event = ""
        for fileName in os.listdir("./include/lua/events/"):
            with open(f"./include/lua/events/{fileName}", encoding="utf8") as f:
                self.event = f.read()
                break #read only 1 event
        room = Room(self, "en-event")
        room.luaRuntime = Lua(room, self)
        room.luaRuntime.RunCode(self.event) 
        for timer in [room.autoRespawnTimer, room.changeMapTimer, room.endSnowTimer, room.killAfkTimer, room.voteCloseTimer]:
            if timer != None:
                timer.cancel()
    
    def runEvent(self):
        for room in self.rooms:
            self.rooms[room].nextEvent = True

    def loadPromotions(self):
        i = 0
        self.shopPromotions = []
        while i < len(self.promotions):
            item = self.promotions[i]                
            try:
                if item[4] > int(time.time()):
                    i +=1
                    continue
            except: i = i
            self.shopPromotions.append([item[0], item[1], item[2], item[3]])
            i += 1
        
        self.checkPromotionsEnd()

    def loadPunishments(self):
        for rs in Cursor['usertempban'].find():
            self.userTempBanCache.append(rs['Username'])
            
        for rs in Cursor['usertempmute'].find():
            self.userMuteCache.append(rs['Username'])

    async def loadRecords(self, showConsole = 1):
        await CursorMaps.execute("select Code, Time, Player from Maps where not Player = ''")
        recs = await CursorMaps.fetchall()
        t = self.fastRacingRecords
        for rs in recs:
            mapCode, name, recordtime = rs["Code"], rs["Player"], rs["Time"]
            t["recordmap"][mapCode] = [name,recordtime]
            if not name in t["records"]:
                t["records"][name] = {}
            t["records"][name][mapCode] = [mapCode, recordtime]    
        
        for name in t["records"]:
            t["sequentialrecords"].append([name,len(t["records"][name])])	
        if showConsole:
            T = win.Terminal()
            T.cprint(15, 0, "[#] Loaded Records: ")
            T.cprint(6, 0, str(len(recs)) + "\n")

    def loadShopList(self):
        self.shopList = self.shopData["shopItems"]
        self.shamanShopList = self.shopData["shamanItems"]
        self.shopOutfits = self.shopData["fullLooks"]
        self.shopListChecker = []
        self.shopListCheck = {}

        for item in self.shopList:
            self.shopListCheck[f'{item["category"]}|{item["id"]}'] = [item["cheese"], item["fraise"]]
            self.shopListChecker.append(f'{int(item["category"])},{int(item["id"])},0,1,0,{int(item["cheese"])},{int(item["fraise"])}')

        for item in self.shamanShopList:
            self.shamanShopListCheck[str(item["id"])] = [item["cheese"], item["fraise"]]
        
        for item in self.shopOutfits:
            self.shopOutfitsCheck[str(item["id"])] = [item["look"], item["bg"],item["discount"],item["name"],item["start"],item["perm"]]

    def loadVanillaMaps(self):
        for fileName in os.listdir("./include/maps/vanilla/"):
            with open("./include/maps/vanilla/"+fileName) as f:
                self.vanillaMaps[int(fileName[:-4])] = f.read()



    def mutePlayer(self, playerName, hours, reason, modName, isOriginal=False, isSilent=False):
        player = self.players.get(playerName)
        player2 = self.players.get(modName)
        if player != None:
            if isOriginal == True and player2 != None:
                player2.sendServerMessageOthers(f"{modName} muted the player {playerName} for {hours}h ({reason})")
            if playerName in self.userMuteCache:
                self.removeModMute(playerName)
            player.isMute = True
            if isOriginal == True:
                player.sendModMuteMessage(playerName, hours, reason, isSilent)
            self.userMuteCache.append(playerName)
            Cursor['usertempmute'].insert_one({'Username':playerName,'Time':int(Utils.getTime() + (hours * 60 * 60)),'Reason':reason})
            self.saveCasier(playerName,"MUTE",modName,hours,reason)
            player.modoPwet.receiveKarma(playerName,hours,reason,modName,"mute")

    def mutePlayerIP(self, playerName, hours, reason, modName):
        player = self.players.get(playerName)
        if player != None:
            self.mutePlayer(player.playerName, hours, reason, modName, True)
            for player1 in self.players.copy().values():
                if player1.ipAddress == player.ipAddress and player1 != player:
                    self.mutePlayer(player1.playerName, hours, reason, modName, False)

    def saveCasier(self, playerName, state, bannedby, time, reason=""):   
        Cursor['casierlog'].insert_one({'Name':playerName,'IP':self.getPlayerIP(playerName),'State':state,'Timestamp':Utils.getTime(),'Moderator':bannedby,'Time':time,'Reason':reason})

    def sendMumute(self, playerName, modName):
        player = self.players.get(playerName)
        if player != None:
            player.sendServerMessageOthers("%s mumuted %s." %(modName, playerName))
            self.saveCasier(playerName,"MUMUTE", modName, "", "")
            player.isMumute = True

    def sendServerRestartSEC(self, seconds):
        for player in self.players.copy().values():
            player.sendPacket(Identifiers.send.Server_Restart, ByteArray().writeInt(seconds * 1000).toByteArray())
        if seconds <= 1:
            Cursor['loginlogs'].delete_many({})
            Cursor['commandlog'].delete_many({})
            self.updateServer(True)
            os._exit(5)

    def sendStaffChat(self, type, langue, identifiers, packet):
        for client in self.players.copy().values():
            if(type == 3):
                if(client.privLevel >= 7 and client.langue == langue):
                    client.sendPacket(identifiers, packet)
                    
            elif(type == 4):
                if(client.privLevel >= 7):
                    client.sendPacket(identifiers, packet)
                    
            elif(type == 2):
                if(client.privLevel >= 7 and client.langue == langue):
                    client.sendPacket(identifiers, packet)
                    
            elif(type == 5):
                if(client.privLevel >= 7):
                    client.sendPacket(identifiers, packet)
                    
            elif(type == 9):
                if(client.privLevel in [5, 9] or client.isFunCorpPlayer == True):
                    client.sendPacket(identifiers, packet)
                    
            elif(type == 8):
                if(client.privLevel in [4, 9] or client.isLuaCrew == True):
                    client.sendPacket(identifiers, packet)
                    
            elif(type == 10):
                if(client.privLevel in [3, 9] or client.isFashionSquad == True):
                    client.sendPacket(identifiers, packet)
                    
            elif(type == 7):
                if(client.privLevel in [6, 9] or client.isMapCrew == True):
                    client.sendPacket(identifiers, packet)

    def recommendRoom(self, langue, prefix=""):
        count = 0
        result = ""
        while result == "":
            count += 1
            if ("%s-%s" %(langue, count) if prefix == "" else "%s-%s%s" %(langue, prefix, count)) in self.rooms:
                if self.rooms["%s-%s" %(langue, count) if prefix == "" else "%s-%s%s" %(langue, prefix, count)].getPlayerCount() < 25:
                    result = str(count)
            else:
                result = str(count)
        return result

    async def recordSave(self, name, mapCode, time):
        oldname = ""
        if mapCode in self.fastRacingRecords["recordmap"]:
            oldname = self.fastRacingRecords["recordmap"][mapCode][0]
            time = self.fastRacingRecords["recordmap"][mapCode][1]
            if oldname in self.fastRacingRecords["records"] and mapCode in self.fastRacingRecords["records"][oldname]:
                del self.fastRacingRecords["records"][oldname][mapCode]
   
        self.fastRacingRecords["recordmap"][mapCode] = [name, time]
        if not name in self.fastRacingRecords["records"]:
                self.fastRacingRecords["records"][name] = {}
        self.fastRacingRecords["records"][name][mapCode] = [mapCode, time]  
        
        self.fastRacingRecords["sequentialrecords"] = []
        for name in self.fastRacingRecords["records"]:
            self.fastRacingRecords["sequentialrecords"].append([name,len(self.fastRacingRecords["records"][name])])
        await CursorMaps.execute("update maps set Time = ?, Player = ? where Code = ?", [time, name, mapCode])

    async def reloadServer(self):
        reload(_module)
        self.updateServer()
        await self.loadRecords(0)
        self.loadMinigames()
        self.loadEvents()
        self.loadOfficialMinigames()
        self.loadPromotions()
        self.loadShopList()
        for player in self.players.copy().values():
            player.AntiCheat = _module.AntiCheat(player, self)
            player.Cafe = _module.Cafe(player, self)
            player.modoPwet = _module.ModoPwet(player, self)
            player.tribulle = _module.Tribulle(player, self)
            player.Shop = _module.Shop(player, self)
            player.Skills = _module.Skills(player, self)
            player.Packets = _module.Packets(player, self)
            player.Commands = _module.Commands(player, self)
            player.playerException = _module.GameException(player)
            player.missions = _module.Missions(player, self)

    def removeModMute(self, playerName): 
        if playerName in self.userMuteCache:
            self.userMuteCache.remove(playerName)
        Cursor['usertempmute'].delete_one({'Username':playerName})

    def removeTempBan(self, playerName):
        if playerName in self.userTempBanCache:
            self.userTempBanCache.remove(playerName)
        Cursor['usertempban'].delete_one({'Username':playerName})

    def tempBanUser(self, playerName, bantime, reason):
        if self.checkTempBan(playerName):
            self.removeTempBan(playerName)
        self.userTempBanCache.append(playerName)
        Cursor['usertempban'].insert_one({'Username':playerName,'Reason':reason,'Time':int(Utils.getTime() + (bantime * 60 * 60))})

    def tempBanIP(self, ip, time):
        if not ip in self.IPTempBanCache:
            self.IPTempBanCache.append(ip)
            if ip in self.IPTempBanCache:
                self.loop.call_later(time, lambda: self.IPTempBanCache.remove(ip))

    def updateBlackList(self):
        with open("./include/json/blacklist.json", "w") as f: 
            json.dump(self.serverList, f)

    def updateConfig(self):
        config.set("configGame", "game.lastShopGiftID", str(self.lastShopGiftID))
        config.set("configGame", "game.lastPlayerCode", str(self.lastPlayerCode))
        config.set("configGame", "game.lastMapCodeId", str(self.lastMapEditeurCode))
        config.set("configGame", "game.lastPlayerID", str(self.lastPlayerID))
        config.set("configGame", "game.lastTribeID", str(self.lastTribeID))
        config.set("configGame", "game.cafelasttopicid", str(self.lastCafeTopicID))
        config.set("configGame", "game.cafelastpostid", str(self.lastCafePostID))
        with open("./include/configs.properties", "w") as f:
            config.write(f)

    def updateModopwet(self):
        with open("./include/json/modopwet.json",'w') as F:
            F.write(json.dumps(self.reports))
                
    def updatePromotions(self):
        with open("./include/json/promotions.json", "w") as f:
            json.dump(self.promotions, f)
                
    def updateShop(self):
        with open("./include/json/shop.json",'w') as f:
            f.write(json.dumps(self.shopData))
        self.loadShopList()

    def updateServer(self, isRestarting=False):
        self.updateBlackList()
        self.updateConfig()
        self.updateModopwet()
        self.updatePromotions()
        self.updateShop()
        if isRestarting:
            for player in self.players.copy().values():
                player.updateDatabase()
                player.transport.close()
                del self.players[player.playerName]
        else:
            for player in self.players.copy().values():
                player.updateDatabase()

    def voteBanPopulaire(self, playerName, playerVoted, ip):
        player = self.players.get(playerName)
        if player != None and player.privLevel >= 1 and not ip in player.voteBan:
            player.voteBan.append(ip)
            if len(player.voteBan) == 20:
                self.banPlayer(playerName, 1, "Vote Populaire", "Server", False)
            player.sendServerMessage(f"The player {playerVoted} voted to ban {playerName} ({len(player.voteBan)} / 20 votes)")

    def checkBanUser(self, playerName):
        if self.checkExistingUser(playerName):
            if self.checkTempBan(playerName):
                return 1
            else:
                return -1
        return 0

    def configSWF(self, setting):
        return config.get("configSWF", setting)
        
    def configServeur(self, setting):
        return config.get("configServeur", setting)
                        
    def config(self, setting):
        return config.get("configGame", setting)

    def lastoutfitid(self):
        if len(self.shopData["fullLooks"]) == 0: 
            return 0
        highestid = 0
        for i in self.shopData["fullLooks"]:
            if int(i["id"]) > highestid: highestid = int(i["id"])
           
        return highestid + 1


    def sendServerRestart(self, no=0, sec=1):
        if sec > 0 or no != 5:
            self.sendServerRestartSEC(120 if no == 0 else (60 if no == 1 else (30 if no == 2 else (20 if no == 3 else (10 if no == 4 else sec)))))
            if self.rebootTimer != None:
                self.rebootTimer.cancel()
            self.rebootTimer = self.loop.call_later(60 if no == 0 else 30 if no == 1 else 10 if no == 2 or no == 3 else 1, lambda: self.sendServerRestart(no if no == 5 else no + 1, 9 if no == 4 else sec - 1 if no == 5 else 0))
        return

class Room:
    def __init__(self, server, name):

        # String
        self.mapXML = ""
        self.mapName = ""
        self.EMapXML = ""
        self.minigame = ""
        self.roomPassword = ""
        self.forceNextMap = "-1"
        self.currentSyncName = ""
        self.currentShamanName = ""
        self.currentSecondShamanName = ""
        self.bulle = "bulle1"

        # Integer
        self.lastImageID = 0
        self.addTime = 0
        self.mapCode = -1
        self.cloudID = -1
        self.EMapCode = 0
        self.objectID = 0
        self.redCount = 0
        self.mapPerma = -1
        self.blueCount = 0
        self.musicTime = 0
        self.mapStatus = -1
        self.mapNoVotes = 0
        self.currentMap = 0
        self.receivedNo = 0
        self.EMapLoaded = 0
        self.roundTime = 120
        self.mapYesVotes = 0
        self.receivedYes = 0
        self.roundsCount = -1
        self.maxPlayers = 200
        self.numCompleted = 0
        self.numGetCheese = 0
        self.companionBox = -1
        self.gameStartTime = 0
        self.lastRoundCode = 0
        self.FSnumCompleted = 0
        self.SSnumCompleted = 0
        self.musicSkipVotes = 0
        self.forceNextShaman = -1
        self.currentSyncCode = -1
        self.changeMapAttemps = 0
        self.currentShamanCode = -1
        self.currentShamanType = -1
        self.mulodromeRoundCount = 0
        self.gameStartTimeMillis = 0
        self.currentSecondShamanCode = -1
        self.currentSecondShamanType = -1

        # Bool
        self.isMusic = False
        self.isClosed = False
        self.noShaman = False
        self.isEditor = False
        self.isRacing = False
        self.isSnowing = False
        self.isVillage = False
        self.isVanilla = False
        self.countStats = False
        self.isFixedMap = False
        self.isNormRoom = False
        self.isTutorial = False
        self.isBootcamp = False
        self.isSurvivor = False
        self.isVotingBox = False
        self.autoRespawn = False
        self.noAutoScore = False
        self.isDoubleMap = False
        self.specificMap = False
        self.mapInverted = False
        self.isDefilante = False
        self.isMulodrome = False
        self.canChangeMap = True
        self.isVotingMode = False
        self.isTribeHouse = False
        self.isNoShamanMap = False
        self.EMapValidated = False
        self.isTotemEditor = False
        self.canChangeMusic = True
        self.initVotingMode = True
        self.disableAfkKill = False
        self.isPlayingMusic = False
        self.noShamanSkills = False
        self.never20secTimer = False
        self.isTribeHouseMap = False
        self.changed20secTimer = False
        self.catchTheCheeseMap = False
        self.disableDebugCommand = False
        self.disableMinimalistMode = False
        self.disableWatchCommand = False
        self.isFastRacing = False
        self.isFuncorp = False
        self.isFuncorpRoomName = False
        self.autoMapFlipMode = True
        self.disableMortCommand = False
        self.disablePhysicalConsumables = False
        self.notUpdatedScore = False
        self.nextEvent = False
        self.isEvent = False
        
        # Nonetype
        self.killAfkTimer = None
        self.endSnowTimer = None
        self.changeMapTimer = None
        self.voteCloseTimer = None
        self.startTimerLeft = None
        self.autoRespawnTimer = None
        self.luaRuntime = None
        self.roomCreator = None

        # List Arguments
        self.anchors = []
        self.redTeam = []
        self.blueTeam = []
        self.roomTimers = []
        self.musicVideos = []
        self.lastHandymouse = [-1, -1]
        
        self.noShamanMaps = [7, 8, 10, 14, 22, 23, 28, 29, 33, 42, 55, 57, 58, 61, 70, 77, 78, 87, 88, 122, 123, 124, 125, 126, 148, 149, 150, 151, 172, 173, 174, 175, 178, 179, 180, 188, 189, 190, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 218, 219, 220, 221, 222, 224, 225]
        self.mapList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 136, 137, 138, 139, 140, 141, 142, 143, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227]
        self.mapEvents = []
        self.catchCheeseMaps = [108, 109, 110, 111, 112, 113, 144, 170, 171, 214, 215]
        self.doubleShamanMaps = [44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 138, 139, 140, 141, 142, 143, 223, 227]
        self.transformationMaps = [200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210]
        #self.bombMaps = [8, 14, 28, 33, 117, 118, 120]
        
        # Dict
        self.clients = {}
        self.funcorpNames = {}
        self.currentTimers = {}
        self.currentShamanSkills = {}
        self.currentSecondShamanSkills = {}

        # Others
        self.name = name
        self.server = server
        self.CursorMaps = CursorMaps

        if self.name.startswith("*") or self.name.startswith("@"):
            self.community = "xx"
            self.roomName = self.name
        else:
            self.community = self.name.split("-")[0].lower()
            self.roomName = self.name.split("-")[1]

        roomNameCheck = self.roomName[1:] if self.roomName.startswith("*") or self.roomName.startswith("@") else self.roomName
        if self.roomName.startswith("\x03[Editeur] "):
            self.countStats = False
            self.isEditor = True
            self.never20secTimer = True

        elif self.roomName.startswith("\x03[Tutorial] "):
            self.countStats = False
            self.currentMap = 900
            self.specificMap = True
            self.noShaman = True
            self.never20secTimer = True
            self.isTutorial = True

        elif self.roomName.startswith("\x03[Totem] "):
            self.countStats = False
            self.specificMap = True
            self.currentMap = 444
            self.isTotemEditor = True
            self.never20secTimer = True

        elif self.roomName.startswith("*\x03"):
            self.countStats = False
            self.isTribeHouse = True
            self.autoRespawn = True
            self.never20secTimer = True
            self.noShaman = True
            self.disableAfkKill = True
            self.isFixedMap = True
            self.roundTime = 0

        elif roomNameCheck.startswith("801") or roomNameCheck.startswith("village"):
            self.isVillage = True
            self.roundTime = 0
            self.never20secTimer = True
            self.autoRespawn = True
            self.countStats = False
            self.noShaman = True
            self.isFixedMap = True
            self.disableAfkKill = True

        elif roomNameCheck.startswith("#fastracing"):
            self.isFastRacing = True
            self.roundTime = 63
            self.noShaman = True
            self.countStats = True
                
        elif roomNameCheck.startswith("#") or roomNameCheck.startswith("*#") or roomNameCheck.startswith("@#"):
            for name in self.server.minigames:
                if(name in self.roomName[1:]):
                    self.minigame = name
            for name in self.server.officialminigames:
                if(name in self.roomName[1:]):
                    self.minigame = name
                    self.countStats = True

        elif "music" in self.roomName.lower():
            self.isMusic = True
            self.countStats = True

        elif "racing" in self.roomName.lower():
            self.isRacing = True
            self.noShaman = True
            self.countStats = True
            self.roundTime = 63

        elif "bootcamp" in self.roomName.lower():
            self.isBootcamp = True
            self.countStats = True
            self.roundTime = 360
            self.never20secTimer = True
            self.autoRespawn = True
            self.noShaman = True
            self.server.loop.call_later(2, lambda: self.bindKeyBoard("",71,True))

        elif "vanilla" in self.roomName.lower():
            self.isVanilla = True
            self.countStats = True

        elif "survivor" in self.roomName.lower():
            self.isSurvivor = True
            self.countStats = True
            self.roundTime = 90

        elif "defilante" in self.roomName.lower():
            self.isDefilante = True
            self.noShaman = True
            self.countStats = False
        else:
            self.isNormRoom = True

    def startTimer(self):
        for player in self.clients.copy().values():
            player.sendMapStartTimer(False)

    async def mapChange(self, force=False):
        if self.changeMapTimer != None: self.changeMapTimer.cancel()
        
        if not self.canChangeMap:
            self.changeMapAttemps += 1
            if self.changeMapAttemps < 5:
                self.changeMapTimer = self.server.loop.call_later(1, self.server.loop.create_task, self.mapChange())
                return

        for timer in self.roomTimers:
            timer.cancel()

        self.roomTimers = []

        for timer in [self.voteCloseTimer, self.killAfkTimer, self.autoRespawnTimer, self.startTimerLeft]:
            if timer != None:
                timer.cancel()

        if self.initVotingMode:
            if not self.isVotingBox and (self.mapPerma == 0 and self.mapCode != -1) and self.getPlayerCount() >= 2:
                self.isVotingMode = True
                self.isVotingBox = True
                self.voteCloseTimer = self.server.loop.call_later(8, self.server.loop.create_task, self.closeVoting())
                for player in self.clients.copy().values():
                    player.sendPacket(Identifiers.old.send.Vote_Box, [self.mapName, self.mapYesVotes, self.mapNoVotes])
            else:
                self.votingMode = False
                return await self.closeVoting()

        elif self.isTribeHouse and self.isTribeHouseMap:
            pass
        else:
            if self.isVotingMode:
                TotalYes = self.mapYesVotes + self.receivedYes
                TotalNo = self.mapNoVotes + self.receivedNo
                isDel = False

                if TotalYes + TotalNo >= 100:
                    TotalVotes = TotalYes + TotalNo
                    Rating = (1.0 * TotalYes / TotalNo) * 100
                    rate = str(Rating).split(".")
                    if int(rate[0]) < 50:
                        isDel = True
                await CursorMaps.execute("update Maps set YesVotes = ?, NoVotes = ?, Perma = 44 where Code = ?" if isDel else "update Maps set YesVotes = ?, NoVotes = ? where Code = ?", [TotalYes, TotalNo, self.mapCode])
                self.isVotingMode = False
                self.receivedNo = 0
                self.receivedYes = 0

            self.initVotingMode = True
            self.lastRoundCode = (self.lastRoundCode + 1) % 127

            if self.isSurvivor:
                cnt = 0
                for player in self.clients.copy().values():
                    if not player.isDead and (not player.isVampire if self.mapStatus == 0 else not player.isShaman):
                        if not self.noAutoScore: 
                            player.playerScore += 10

            if self.catchTheCheeseMap:
                self.catchTheCheeseMap = False
            else:
                numCom = self.FSnumCompleted - 1 if self.isDoubleMap else self.numCompleted - 1
                numCom2 = self.SSnumCompleted - 1 if self.isDoubleMap else 0
                if numCom < 0: numCom = 0
                if numCom2 < 0: numCom2 = 0

                player = self.clients.get(self.currentShamanName)
                if player != None:
                    self.sendAll(Identifiers.old.send.Shaman_Perfomance, [self.currentShamanName, numCom])
                    if not self.noAutoScore: player.playerScore = numCom
                    if numCom > 0:
                        player.Skills.earnExp(True, numCom)

                player2 = self.clients.get(self.currentSecondShamanName)
                if player2 != None:
                    self.sendAll(Identifiers.old.send.Shaman_Perfomance, [self.currentSecondShamanName, numCom2])
                    if not self.noAutoScore: player2.playerScore = numCom2
                    if numCom2 > 0:
                        player2.Skills.earnExp(True, numCom2)

            if self.getPlayerCount() >= self.server.needToFirst:
                if self.isSurvivor:
                    self.giveSurvivorStats() 
                elif self.isRacing:
                    self.giveRacingStats()
                elif self.isDefilante:
                    self.giveDefilanteStats()

            self.currentSyncCode = -1
            self.currentShamanCode = -1
            self.currentShamanType = -1
            self.currentSecondShamanCode = -1
            self.currentSecondShamanType = -1

            self.currentSyncName = ""
            self.currentShamanName = ""
            self.currentSecondShamanName = ""
            
            self.currentShamanSkills = {}
            self.currentSecondShamanSkills = {}
            
            self.changed20secTimer = False
            self.isDoubleMap = False
            self.isNoShamanMap = False
            self.FSnumCompleted = 0
            self.SSnumCompleted = 0
            self.objectID = 0
            self.numGetCheese = 0
            self.addTime = 0
            self.cloudID = -1
            self.companionBox = -1
            self.lastHandymouse = [-1, -1]
            self.isTribeHouseMap = False
            self.canChangeMusic = True
            self.canChangeMap = True
            self.changeMapAttemps = 0
            
            self.getSyncCode()
            self.anchors = []
            self.mapStatus = (self.mapStatus + 1) % 10

            self.numCompleted = 0
                   
            if self.nextEvent:
                self.nextEvent = False
                self.isEvent = True
                if self.luaRuntime == None:
                    self.luaRuntime = Lua(self, self.server)
                self.luaRuntime.RunCode(self.server.event)
                return
                
            self.currentMap = await self.selectMap()
            self.checkMapXML()
     
            if self.currentMap in self.doubleShamanMaps or self.mapPerma == 8 and self.getPlayerCount() >= 3:
                self.isDoubleMap = True

            if self.mapPerma in [7, 17, 42] or (self.isSurvivor and self.mapStatus == 0) or self.currentMap in self.noShamanMaps:
                self.isNoShamanMap = True

            if self.currentMap in self.catchCheeseMaps:
                self.catchTheCheeseMap = True

            self.gameStartTime = Utils.getTime()
            self.gameStartTimeMillis = time.time()

            for player in self.clients.copy().values():
                player.resetPlay()

            for player in self.clients.copy().values():
                player.startPlay()
                
                if player.isHidden:
                    player.isDead = True
                    player.sendPlayerDied()
            
            if self.isFastRacing:
                await CursorMaps.execute('select Time,Player from Maps where code = ?', [self.mapCode])
                rs = await CursorMaps.fetchone()
                if rs[0] > 0:
                    t = rs[0] / 100.0 if rs[0] > 0 else rs[0] / 10.0
                    for player in self.clients.copy().values():
                        if player.langueID >= 0:
                            player.sendMessage("<bl>Best record by <J>"+str(rs[1])+"</J> <bl>with second</font> (<v>"+str(t)+"</v>s)")
                else:
                    for player in self.clients.copy().values():
                        player.sendMessage("<R>(@%s)</R> <bl>map has not broken record</font>"% (self.mapCode))

            for player in self.clients.copy().values():
                if player.pet != 0:
                    if Utils.getSecondsDiff(player.petEnd) >= 0:
                        player.pet = 0
                        player.petEnd = 0
                    else:
                        self.sendAll(Identifiers.send.Pet, ByteArray().writeInt(player.playerCode).writeUnsignedByte(player.pet).toByteArray())
                if player.fur != 0:
                    if Utils.getSecondsDiff(player.furEnd) >= 0:
                        player.fur = 0
                        player.furEnd = 0

            if self.isSurvivor and self.mapStatus == 0:
                self.server.loop.call_later(5, self.sendVampireMode)

            if self.isMulodrome:
                self.mulodromeRoundCount += 1
                self.sendMulodromeRound()
                if self.mulodromeRoundCount <= 10:
                    for player in self.clients.copy().values():
                        if player.playerName in self.blueTeam:
                            self.setNameColor(player.playerName, 0x979EFF)
                        elif player.playerName in self.redTeam:
                            self.setNameColor(player.playerName, 0xFF9396)
                else:
                    self.sendAll(Identifiers.send.Mulodrome_End)

            if (self.isRacing or self.isDefilante or self.isFastRacing) and self.notUpdatedScore:
                self.roundsCount = (self.roundsCount + 1) % 10
                self.notUpdatedScore = False
                self.sendAll(Identifiers.send.Rounds_Count, ByteArray().writeByte(self.roundsCount).writeInt(self.getHighestScore()).toByteArray())
                        
            self.startTimerLeft = self.server.loop.call_later(3, self.startTimer)
            if not self.isFixedMap and not self.isTribeHouse and not self.isTribeHouseMap:
                self.changeMapTimer = self.server.loop.call_later(self.roundTime + self.addTime, self.server.loop.create_task, self.mapChange())
            
            self.killAfkTimer = self.server.loop.call_later(30, self.killAfk)
            if self.autoRespawn or self.isTribeHouseMap:
                self.autoRespawnTimer = self.server.loop.call_later(2, self.respawnMice)
                
        if self.luaRuntime != None:
            self.luaRuntime.emit("NewGame", self.currentMap)

    def getPlayersCountbyRoom(self, roomName):
        cnt = 0
        roomName = roomName.replace('*', '')
        for player in self.clients.copy().values():
            if player.room.name[3:].startswith(roomName):
                cnt += 1
        return cnt

    def addClient(self, player, newRoom=False):
        self.clients[player.playerName] = player

        player.room = self
        if not newRoom:
            player.isDead = True
            self.sendAllOthers(player, Identifiers.send.Player_Respawn, ByteArray().writeBytes(player.getPlayerData()).writeBoolean(False).writeBoolean(True).toByteArray())
            player.startPlay()
        else:
            player.room.roomCreator = player.playerName
        
        if self.luaRuntime != None:
            self.luaRuntime.emit("NewPlayer", (player.playerName))

    async def selectMap(self):
        if self.forceNextMap == "-1" and self.isEvent: return -1
        if not self.forceNextMap == "-1":
            force = self.forceNextMap
            self.forceNextMap = "-1"
            self.mapCode = -1

            if force.isdigit():
                return await self.selectMapSpecificic(force, "Vanilla")
            elif force.startswith("@"):
                return await self.selectMapSpecificic(force[1:], "Custom")
            elif force.startswith("#"):
                return await self.selectMapSpecificic(force[1:], "Perm")
            elif force.startswith("<"):
                return await self.selectMapSpecificic(force, "Xml")
            else:
                return 0

        elif self.specificMap:
            self.mapCode = -1
            return self.currentMap
        else:
            if self.isEditor:
                return self.EMapCode

            elif self.isTribeHouse:
                tribeName = self.roomName[2:]
                runMap = self.server.getTribeHouse(tribeName)

                if runMap == 0:
                    self.mapCode = 0
                    self.mapName = "Mice Master"
                    self.mapXML = "<C><P /><Z><S><S Y=\"360\" T=\"0\" P=\"0,0,0.3,0.2,0,0,0,0\" L=\"800\" H=\"80\" X=\"400\" /></S><D><P Y=\"0\" T=\"34\" P=\"0,0\" X=\"0\" C=\"719b9f\" /><T Y=\"320\" X=\"49\" /><P Y=\"320\" T=\"16\" X=\"224\" P=\"0,0\" /><P Y=\"319\" T=\"17\" X=\"311\" P=\"0,0\" /><P Y=\"284\" T=\"18\" P=\"1,0\" X=\"337\" C=\"57703e,e7c3d6\" /><P Y=\"284\" T=\"21\" X=\"294\" P=\"0,0\" /><P Y=\"134\" T=\"23\" X=\"135\" P=\"0,0\" /><P Y=\"320\" T=\"24\" P=\"0,1\" X=\"677\" C=\"46788e\" /><P Y=\"320\" T=\"26\" X=\"588\" P=\"1,0\" /><P Y=\"193\" T=\"14\" P=\"0,0\" X=\"562\" C=\"95311e,bde8f3,faf1b3\" /></D><O /></Z></C>"
                    self.mapYesVotes = 0
                    self.mapNoVotes = 0
                    self.mapPerma = 22
                    self.mapInverted = False
                else:
                    run = await self.selectMapSpecificic(runMap, "Custom")
                    if run != -1:
                        self.mapCode = 0
                        self.mapName = self.server.micename
                        self.mapXML = "<C><P /><Z><S><S Y=\"360\" T=\"0\" P=\"0,0,0.3,0.2,0,0,0,0\" L=\"800\" H=\"80\" X=\"400\" /></S><D><P Y=\"0\" T=\"34\" P=\"0,0\" X=\"0\" C=\"719b9f\" /><T Y=\"320\" X=\"49\" /><P Y=\"320\" T=\"16\" X=\"224\" P=\"0,0\" /><P Y=\"319\" T=\"17\" X=\"311\" P=\"0,0\" /><P Y=\"284\" T=\"18\" P=\"1,0\" X=\"337\" C=\"57703e,e7c3d6\" /><P Y=\"284\" T=\"21\" X=\"294\" P=\"0,0\" /><P Y=\"134\" T=\"23\" X=\"135\" P=\"0,0\" /><P Y=\"320\" T=\"24\" P=\"0,1\" X=\"677\" C=\"46788e\" /><P Y=\"320\" T=\"26\" X=\"588\" P=\"1,0\" /><P Y=\"193\" T=\"14\" P=\"0,0\" X=\"562\" C=\"95311e,bde8f3,faf1b3\" /></D><O /></Z></C>"
                        self.mapYesVotes = 0
                        self.mapNoVotes = 0
                        self.mapPerma = 22
                        self.mapInverted = False

            elif self.isVillage:
                return 801

            elif self.isVanilla:
                self.mapCode = -1
                self.mapName = "Invalid";
                self.mapXML = "<C><P /><Z><S /><D /><O /></Z></C>"
                self.mapYesVotes = 0
                self.mapNoVotes = 0
                self.mapPerma = -1
                self.mapInverted = False
                map = random.choice(self.mapList)
                while map == self.currentMap:
                    map = random.choice(self.mapList)
                return map
                
            else:
                self.mapCode = -1
                self.mapName = "Invalid";
                self.mapXML = "<C><P /><Z><S /><D /><O /></Z></C>"
                self.mapYesVotes = 0
                self.mapNoVotes = 0
                self.mapPerma = -1
                self.mapInverted = False
                return await self.selectMapStatus()
        return -1

    async def selectMapStatus(self):
        maps = [0, -1, 4, 9, 5, 0, -1, 8, 6, 7]
        selectPerma = (17 if self.mapStatus % 2 == 0 else 7) if self.isRacing or self.isFastRacing else (13 if self.mapStatus % 2 == 0 else 3) if self.isBootcamp else 18 if self.isDefilante else (11 if self.mapStatus == 0 else 10) if self.isSurvivor else 19 if self.isMusic and self.mapStatus % 2 == 0 else 0
        isMultiple = False

        if self.isNormRoom:
            if self.mapStatus < len(maps) and maps[self.mapStatus] != -1:
                isMultiple = maps[self.mapStatus] == 0
                selectPerma = maps[self.mapStatus]
            else:
                map = random.choice(self.mapList)
                while map == self.currentMap:
                    map = random.choice(self.mapList)
                return map

        elif self.isVanilla or (self.isMusic and self.mapStatus % 2 != 0):
            map = random.choice(self.mapList)
            while map == self.currentMap:
                map = random.choice(self.mapList)
            return map

        await CursorMaps.execute("select * FROM maps WHERE Perma = ? ORDER BY RANDOM() LIMIT 1", [random.choice([0, 1]) if isMultiple else selectPerma])
        rs = await CursorMaps.fetchone()
        if rs:
           self.mapCode = rs["Code"]
           self.mapName = rs["Name"]
           self.mapXML = rs["XML"]
           self.mapYesVotes = rs["YesVotes"]
           self.mapNoVotes = rs["NoVotes"]
           self.mapPerma = rs["Perma"]
           self.mapInverted = self.autoMapFlipMode and random.randint(0, 100) > 85
        else:
           map = random.choice(self.mapList)
           while map == self.currentMap:
               map = random.choice(self.mapList)
           return map
        return -1
        
    async def selectMapSpecificic(self, code, type):
        if type == "Vanilla":
            return int(code)

        elif type == "Custom":
            mapInfo = await self.getMapInfo(int(code))
            if mapInfo[0] == None:
                return 0
            else:
                self.mapCode = code
                self.mapName = mapInfo[0]
                self.mapXML = mapInfo[1]
                self.mapYesVotes = mapInfo[2]
                self.mapNoVotes = mapInfo[3]
                self.mapPerma = mapInfo[4]
                self.mapInverted = False
                return -1

        elif type == "Perm":
            mapList = []
            await CursorMaps.execute("select Code from Maps where Perma = ? and Code != ? order by random() limit 1", [code, self.currentMap])
            runMap = await CursorMaps.fetchone()
            runMap = 0 if runMap == None else runMap[0]

            if runMap == 0:
                map = random.choice(self.MapList)
                while map == self.currentMap:
                    map = random.choice(self.MapList)
                return map
            else:
                mapInfo = await self.getMapInfo(runMap)
                self.mapCode = runMap
                self.mapName = mapInfo[0]
                self.mapXML = mapInfo[1]
                self.mapYesVotes = mapInfo[2]
                self.mapNoVotes = mapInfo[3]
                self.mapPerma = mapInfo[4]
                self.mapInverted = False
                return -1

        elif type == "Xml":
            self.mapCode = 0
            self.mapName = "#Module"
            self.mapXML = str(code)
            self.mapYesVotes = 0
            self.mapNoVotes = 0
            self.mapPerma = 22
            self.mapInverted = False
            return -1

    def changeMapTimers(self, seconds):
        if self.changeMapTimer != None: self.changeMapTimer.cancel()
        self.changeMapTimer = self.server.loop.call_later(seconds, self.server.loop.create_task, self.mapChange())

    def checkChangeMap(self):
        if (not (self.isBootcamp or self.autoRespawn or self.isTribeHouse and self.isTribeHouseMap or self.isFixedMap)):
            alivePeople = list(filter(lambda player: not player.isDead, self.clients.copy().values()))
            if not alivePeople:
                self.server.loop.create_task(self.mapChange())

    def checkMapXML(self):
        if int(self.currentMap) in self.server.vanillaMaps or int(self.currentMap) in self.server.eventMaps:
            self.mapCode = int(self.currentMap) if self.currentMap in self.mapList or self.currentMap in self.server.eventMaps else 801
            self.mapName = "_Atelier 801" if self.mapCode == 801 else self.server.miceName
            self.mapXML = str(self.server.vanillaMaps[int(self.currentMap)])
            self.mapYesVotes = 0
            self.mapNoVotes = 0
            self.mapPerma = -1
            self.currentMap = int(self.currentMap)
            self.mapInverted = False

    def checkIfDoubleShamansAreDead(self):
        player1 = self.clients.get(self.currentShamanName)
        player2 = self.clients.get(self.currentSecondShamanName)
        return (False if player1 == None else player1.isDead) and (False if player2 == None else player2.isDead)

    def checkIfShamanIsDead(self):
        player = self.clients.get(self.currentShamanName)
        return False if player == None else player.isDead

    def checkIfShamanCanGoIn(self):
        for player in self.clients.copy().values():
            if player.playerCode != self.currentShamanCode and player.playerCode != self.currentSecondShamanCode and not player.isDead:
                return False
        return True

    def checkIfTooFewRemaining(self):
        return len(list(filter(lambda player: not player.isDead, self.clients.copy().values()))) <= 2

    async def closeVoting(self):
        self.initVotingMode = False
        self.isVotingBox = False
        if self.voteCloseTimer != None: self.voteCloseTimer.cancel()
        await self.mapChange()

    def getAliveCount(self):
        return len(list(filter(lambda player: not player.isDead, self.clients.copy().values())))

    def getDeathCountNoShaman(self):
        return len(list(filter(lambda player: not player.isShaman and not player.isDead and not player.isNewPlayer, self.clients.copy().values())))

    def getDoubleShamanCode(self):
        if self.currentShamanCode == -1 and self.currentSecondShamanCode == -1:
            if self.forceNextShaman > 0:
                self.currentShamanCode = self.forceNextShaman
                self.forceNextShaman = 0
            else:
                self.currentShamanCode = self.getHighestScore()

            if self.currentSecondShamanCode == -1:
                self.currentSecondShamanCode = self.getSecondHighestScore()

            if self.currentSecondShamanCode == self.currentShamanCode:
                tempClient = random.choice(list(self.clients.copy().values()))
                self.currentSecondShamanCode = tempClient.playerCode

            for player in self.clients.copy().values():
                if player.playerCode == self.currentShamanCode:
                    self.currentShamanName = player.playerName
                    self.currentShamanType = player.shamanType
                    self.currentShamanSkills = player.playerSkills
                    break

                if player.playerCode == self.currentSecondShamanCode:
                    self.currentSecondShamanName = player.playerName
                    self.currentSecondShamanType = player.shamanType
                    self.currentSecondShamanSkills = player.playerSkills
                    break

        return [self.currentShamanCode, self.currentSecondShamanCode]

    def getHighestScore(self):
        playerScores = []
        playerID = 0
        for player in self.clients.copy().values():
            playerScores.append(player.playerScore)
                    
        for player in self.clients.copy().values():
            if player.playerScore == max(playerScores):
                playerID = player.playerCode
        return playerID

    async def getMapInfo(self, mapCode):
        mapInfo = ["", "", 0, 0, 0]
        await CursorMaps.execute("SELECT * from Maps where Code = ?", [mapCode])
        rs = await CursorMaps.fetchone()
        if rs:
            mapInfo = rs["Name"], rs["XML"], rs["YesVotes"], rs["NoVotes"], rs["Perma"]
        return mapInfo

    def getPlayerCount(self):
        return len(list(filter(lambda player: not player.isHidden, self.clients.copy().values())))

    def getPlayerCountUnique(self):
        ipList = []
        for player in self.clients.copy().values():
            if not player.ipAddress in ipList:
                ipList.append(player.ipAddress)
        return len(ipList)

    def getPlayerList(self):
        result, i = b"", 0
        for player in self.clients.copy().values():
            if not player.isHidden:
                result += player.getPlayerData()
                i += 1

        return [i, result]

    def getSecondHighestScore(self):
        playerScores = []
        playerID = 0
        for player in self.clients.copy().values():
            playerScores.append(player.playerScore)
        playerScores.remove(max(playerScores))

        if len(playerScores) >= 1:
            for player in self.clients.copy().values():
                if player.playerScore == max(playerScores):
                    playerID = player.playerCode
        return playerID

    def getShamanCode(self):
        if self.currentShamanCode == -1:
            if self.isNoShamanMap or self.noShaman or self.currentMap in self.noShamanMaps:
                pass
            else:
                if self.forceNextShaman > 0:
                    self.currentShamanCode = self.forceNextShaman
                    self.forceNextShaman = 0
                else:
                    self.currentShamanCode = self.getHighestScore()

            if self.currentShamanCode == -1:
                self.currentShamanName = ""
            else:
                for player in self.clients.copy().values():
                    if player.playerCode == self.currentShamanCode:
                        self.currentShamanName = player.playerName
                        self.currentShamanType = player.shamanType
                        self.currentShamanSkills = player.playerSkills
                        break
        return self.currentShamanCode

    def getSourisCount(self):
        return len(list(filter(lambda player: player.isGuest, self.clients.copy().values())))

    def getSyncCode(self):
        if self.getPlayerCount() > 0:
            if self.currentSyncCode == -1:
                player = random.choice(list(self.clients.copy().values()))
                self.currentSyncCode = player.playerCode
                self.currentSyncName = player.playerName
        else:
            if self.currentSyncCode == -1:
                self.currentSyncCode = 0
                self.currentSyncName = ""
        return self.currentSyncCode

    def giveDefilanteStats(self, increment=1):
        for player in self.clients.copy().values():
            if not player.isNewPlayer:
                player.defilanteStats[0] += increment
                if player.hasEnter:
                    if player.defilanteRounds % 3 == 0:
                        player.giveConsumable(2504, 1, 0)
                    player.defilanteStats[1] += increment
                    player.missions.upMission("5")
                player.defilanteStats[2] += player.defilantePoints
                i = 0
                while i < 2:
                    playerStat = player.defilanteStats[i]
                    serverStat = self.server.statsPlayer["defilanteCount"][i]
                    if playerStat % serverStat > (playerStat + increment) % serverStat:
                        player.Shop.sendUnlockedBadge(self.server.statsPlayer["defilanteBadges"][i])
                        player.shopBadges.append(self.server.statsPlayer["defilanteBadges"][i])
                        player.Shop.checkAndRebuildBadges()
                    i += 1

    def giveRacingStats(self, increment=1):
        for player in self.clients.copy().values():
            if not player.isNewPlayer:
                player.racingStats[0] += increment
                if player.hasEnter:
                    player.racingStats[1] += increment
                    player.missions.upMission("4")
                    player.giveConsumable(2254, increment, 0)
                    if player.currentPlace <= 3:
                        player.racingStats[2] += increment
                    if player.currentPlace == 1:
                        player.racingStats[3] += increment

                i = 0
                while i < 3:
                    playerStat = player.racingStats[i]
                    serverStat = self.server.statsPlayer["racingCount"][i]
                    if playerStat % serverStat > (playerStat + increment) % serverStat:
                        player.Shop.sendUnlockedBadge(self.server.statsPlayer["racingBadges"][i])
                        player.shopBadges.append(self.server.statsPlayer["racingBadges"][i])
                        player.Shop.checkAndRebuildBadges()
                    i += increment

    def giveShamanSave(self, shamanName, type):
        if not self.countStats:
            return
        player = self.clients.get(shamanName)
        if player != None and (self.getPlayerCountUnique() >= self.server.needToShamanPlayers or self.server.isDebug):
            if type == 0:
                player.missions.upMission('2_1')
                player.shamanSaves += 1 if not player.isNoShamanSkills else player.shamanSavesNoSkill
                player.giveConsumable(2253, 1, 0)
            elif type == 1:
                player.missions.upMission('2_2')
                player.hardModeSaves += 1 if not player.isNoShamanSkills else player.hardModeSavesNoSkill
                player.giveConsumable(2253, 1, 0)
            elif type == 2:
                player.missions.upMission('2_3')
                player.divineModeSaves += 1 if not player.isNoShamanSkills else player.divineModeSavesNoSkill
                player.giveConsumable(2253, 1, 0)
            if not self.isGuest:
                counts = [player.shamanSaves, player.hardModeSaves, player.divineModeSaves]
                titles = [self.server.shamanTitleList, self.server.hardModeTitleList, self.server.divineModeTitleList]
                rebuilds = ["shaman", "hardmode", "divinemode"]
                if counts[type] in titles[type]:
                    title = titles[type][counts[type]]
                    player.checkAndRebuildTitleList(rebuilds[type])
                    player.sendUnlockedTitle(int(title - (title % 1)), int(round((title % 1) * 10)))
                    player.sendCompleteTitleList()
                    player.sendTitleList()

    def giveSurvivorStats(self, increment=1):
        for player in self.clients.copy().values():
            if not player.isNewPlayer:
                player.survivorStats[0] += increment
                if player.isShaman:
                    cnt = self.getDeathCountNoShaman()
                    player.survivorStats[1] += increment
                    if cnt > 0:
                        player.survivorStats[2] += cnt
                elif not player.isDead:
                    player.survivorStats[3] += increment

                i = 0
                while i < 3:
                    playerStat = player.survivorStats[i]
                    serverStat = self.server.statsPlayer["survivorCount"][i]
                    if playerStat % serverStat > (playerStat + increment) % serverStat:
                        player.Shop.sendUnlockedBadge(self.server.statsPlayer["survivorBadges"][i])
                        player.shopBadges.append(self.server.statsPlayer["survivorBadges"][i])
                        player.Shop.checkAndRebuildBadges()
                    i += 1

    def loadLuaModule(self, minigame):
        module = self.server.minigames.get(minigame)
        if module != None:
            self.luaRuntime = Lua(self, self.server)
            self.luaRuntime.RunCode(module)      

    def killAfk(self):
        if self.isEditor or self.isTotemEditor or self.isBootcamp or self.isTribeHouseMap or self.disableAfkKill:
            return
            
        if ((Utils.getTime() - self.gameStartTime) < 32 and (Utils.getTime() - self.gameStartTime) > 28):
            for player in self.clients.copy().values():
                if not player.isDead and player.isAfk:
                    player.isDead = True
                    if not self.noAutoScore: player.playerScore += 1
                    player.sendPlayerDied()
            self.checkChangeMap()

    def killShaman(self):
        for player in self.clients.copy().values():
            if player.playerCode == self.currentShamanCode:
                player.isDead = True
                player.sendPlayerDied()
        self.checkChangeMap()

    def newConsumableTimer(self, code):
        self.roomTimers.append(self.server.loop.call_later(10, lambda: self.sendAll(Identifiers.send.Remove_Object, ByteArray().writeInt(code).writeBoolean(False).toByteArray())))

    def removeClient(self, player):
        if player.playerName in self.clients:
            del self.clients[player.playerName]
            player.resetPlay()
            player.isDead = True
            player.playerScore = 0
            player.sendPlayerDisconnect()

            if self.isMulodrome:
                if player.playerName in self.redTeam: self.redTeam.remove(player.playerName)
                if player.playerName in self.blueTeam: self.blueTeam.remove(player.playerName)

                if len(self.redTeam) == 0 and len(self.blueTeam) == 0:
                    self.mulodromeRoundCount = 10
                    self.sendMulodromeRound()

            if len(self.clients) == 0:
                for timer in [self.autoRespawnTimer, self.changeMapTimer, self.endSnowTimer, self.killAfkTimer, self.voteCloseTimer]:
                    if timer != None:
                        timer.cancel()
                        
                del self.server.rooms[self.name]
            else:
                if player.playerCode == self.currentSyncCode:
                    self.currentSyncCode = -1
                    self.currentSyncName = ""
                    self.getSyncCode()
                self.checkChangeMap()
            if self.luaRuntime != None:
                self.luaRuntime.emit("PlayerLeft", (player.playerName))

    def respawnMice(self):
        for player in self.clients.copy().values():
            if player.isDead:
                player.isDead = False
                player.playerStartTimeMillis = time.time()
                self.sendAll(Identifiers.send.Player_Respawn, ByteArray().writeBytes(player.getPlayerData()).writeBoolean(False).writeBoolean(True).toByteArray())
                if self.luaRuntime != None:
                    self.luaRuntime.emit("PlayerRespawn", (player.playerName))
                    
        if self.autoRespawn or self.isTribeHouseMap:
            self.autoRespawnTimer = self.server.loop.call_later(2, self.respawnMice)

    def respawnSpecific(self, playerName):
        player = self.clients.get(playerName)
        if player != None and player.isDead:
            player.resetPlay()
            player.isAfk = False
            player.playerStartTimeMillis = time.time()
            self.sendAll(Identifiers.send.Player_Respawn, ByteArray().writeBytes(player.getPlayerData()).writeBoolean(False).writeBoolean(True).toByteArray())
            if self.luaRuntime != None:
                self.luaRuntime.emit("PlayerRespawn", (player.playerName))

    def sendAll(self, identifiers, packet=""):
        for player in self.clients.copy().values():
            player.sendPacket(identifiers, packet)
                
    def sendAllChat(self, playerName, message, isOnly):
        p = ByteArray().writeUTF(playerName).writeUTF(message).writeBoolean(True)
        if not isOnly:
            for client in self.clients.copy().values():
                client.sendPacket(Identifiers.send.Chat_Message, p.toByteArray())
        elif isOnly == 1:
            player = self.clients.get(playerName)
            if player != None:
                player.sendPacket(Identifiers.send.Chat_Message, p.toByteArray())
                player.sendServerMessage("The player <BV>"+player.playerName+"</BV> has sent a filtered text: [<J>" + str(message) + "</J>].")
        else: #mumute
            player = self.clients.get(playerName)
            if player != None:
                player.sendPacket(Identifiers.send.Chat_Message, p.toByteArray())

    def sendAllOthers(self, senderClient, identifiers, packet=""):
        for player in self.clients.copy().values():
            if player != senderClient:
                player.sendPacket(identifiers, packet)

    def sendMulodromeRound(self):
        self.sendAll(Identifiers.send.Mulodrome_Result, ByteArray().writeByte(self.mulodromeRoundCount).writeShort(self.blueCount).writeShort(self.redCount).toByteArray())
        if self.mulodromeRoundCount > 10:
            self.sendAll(Identifiers.send.Mulodrome_End)
            self.sendAll(Identifiers.send.Mulodrome_Winner, ByteArray().writeByte(2 if self.blueCount == self.redCount else (1 if self.blueCount < self.redCount else 0)).writeShort(self.blueCount).writeShort(self.redCount).toByteArray())
            self.isMulodrome = False
            self.mulodromeRoundCount = 0
            self.redCount = 0
            self.blueCount = 0
            self.redTeam = []
            self.blueTeam = []
            self.isRacing = False
            self.never20secTimer = False
            self.noShaman = False

    def sendVampireMode(self):
        player = self.clients.get(self.currentSyncName)
        if player != None:
            player.sendVampireMode(False)

    def send20SecRemainingTimer(self):
        if not self.changed20secTimer:
            if not self.never20secTimer and self.roundTime + (self.gameStartTime - Utils.getTime()) > 21:
                self.changed20secTimer = True
                self.changeMapTimers(20)
                for player in self.clients.copy().values():
                    player.sendRoundTime(20)

    def startSnowSchedule(self, power):
        if self.isSnowing:
            self.startSnow(0, power, False)

    def startSnow(self, millis, power, enabled):
        self.isSnowing = enabled
        self.sendAll(Identifiers.send.Snow, ByteArray().writeBoolean(enabled).writeShort(power).toByteArray())
        if enabled:
            self.endSnowTimer = self.server.loop.call_later(millis, lambda: self.startSnowSchedule(power))


# Lua

    def addPhysicObject(self, id, x, y, bodyDef):
        self.sendAll(Identifiers.send.Add_Physic_Object, ByteArray().writeShort(id).writeBoolean(bool(bodyDef["dynamic"]) if "dynamic" in bodyDef else False).writeByte(int(bodyDef["type"]) if "type" in bodyDef else 0).writeShort(x).writeShort(y).writeShort(int(bodyDef["width"]) if "width" in bodyDef else 0).writeShort(int(bodyDef["height"]) if "height" in bodyDef else 0).writeBoolean(bool(bodyDef["foreground"]) if "foreground" in bodyDef else False).writeShort(int(bodyDef["friction"]) if "friction" in bodyDef else 0).writeShort(int(bodyDef["restitution"]) if "restitution" in bodyDef else 0).writeShort(int(bodyDef["angle"]) if "angle" in bodyDef else 0).writeBoolean("color" in bodyDef).writeInt(int(bodyDef["color"]) if "color" in bodyDef else 0).writeBoolean(bool(bodyDef["miceCollision"]) if "miceCollision" in bodyDef else True).writeBoolean(bool(bodyDef["groundCollision"]) if "groundCollision" in bodyDef else True).writeBoolean(bool(bodyDef["fixedRotation"]) if "fixedRotation" in bodyDef else False).writeShort(int(bodyDef["mass"]) if "mass" in bodyDef else 0).writeShort(int(bodyDef["linearDamping"]) if "linearDamping" in bodyDef else 0).writeShort(int(bodyDef["angularDamping"]) if "angularDamping" in bodyDef else 0).writeBoolean(False).writeUTF("").writeBoolean(False).toByteArray())

    def addPopup(self, id, type, text, targetPlayer, x=50, y=50, width=0, fixedPos=False):
        p = ByteArray().writeInt(id).writeByte(type).writeUTF(text).writeShort(x).writeShort(y).writeShort(width).writeBoolean(fixedPos)
        if targetPlayer == "":
            self.sendAll(Identifiers.send.Add_Popup, p.toByteArray())
        else:
            player = self.clients.get(targetPlayer)
            if player != None:
                player.sendPacket(Identifiers.send.Add_Popup, p.toByteArray())

    def addQuestanoablePopup(self, question="", popupID=0, targetPlayer="", _class="", small=True, big=False):
        if small:
            p = ByteArray().writeByte(1).writeUTF(_class).writeInt(popupID).writeBoolean(big).writeBoolean(big).writeUTF(question).toByteArray()
        else:
            p = ByteArray().writeByte(2).writeInt(popupID).writeByte(int(big)).writeInt(popupID).writeUTF(question).writeUTF(question).toByteArray()
        if targetPlayer == "":
            self.sendAll(Identifiers.send.Questionable_Popup, p)
        else:
            player = self.clients.get(targetPlayer)
            if player != None:
                player.sendPacket(Identifiers.send.Questionable_Popup, p)

    def addTextArea(self, id, text, targetPlayer="", x=50, y=50, width=0, height=0, backgroundColor=0x324650, borderColor=0, backgroundAlpha=1, fixedPos=False):
        p = ByteArray().writeInt(id).writeUTF(text).writeShort(x).writeShort(y).writeShort(width).writeShort(height).writeInt(backgroundColor).writeInt(borderColor).writeByte(100 if backgroundAlpha > 100 else backgroundAlpha).writeBoolean(fixedPos)
        if targetPlayer == "":
            self.sendAll(Identifiers.send.Add_Text_Area, p.toByteArray())
        else:
            client = self.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Add_Text_Area, p.toByteArray())

    def bindKeyBoard(self, playerName, key, down, yes = True):
        if playerName == "":
            self.sendAll(Identifiers.send.Bind_Key_Board, ByteArray().writeShort(key).writeBoolean(down).writeBoolean(yes).toByteArray())
            return
        player = self.clients.get(playerName)
        if player != None:
            player.sendPacket(Identifiers.send.Bind_Key_Board, ByteArray().writeShort(key).writeBoolean(down).writeBoolean(yes).toByteArray())

    def bindMouse(self, playerName, yes = True):
        player = self.clients.get(playerName)
        if player != None:
            player.sendPacket(Identifiers.send.Bind_Mouse, ByteArray().writeBoolean(yes).toByteArray())

    def movePlayer(self, playerName, xPosition, yPosition, pOffSet=False, xSpeed=0, ySpeed=0, sOffSet=False, angle=0, angleOffset=False):
        player = self.clients.get(playerName)
        if player != None:
            player.sendPacket(Identifiers.send.Move_Player, ByteArray().writeShort(xPosition).writeShort(yPosition).writeBoolean(pOffSet).writeShort(xSpeed).writeShort(ySpeed).writeBoolean(sOffSet).writeShort(angle).writeBoolean(angleOffset).toByteArray())

    def removeObject(self, objectId):
        if objectId == None: objectId = 0
        self.sendAll(Identifiers.send.Remove_Object, ByteArray().writeInt(objectId).writeBoolean(True).toByteArray())
        if self.luaRuntime != None:
            del self.luaRuntime.RoomObjects[int(objectId)]
            self.luaRuntime.RefreshTFMGet()

    def removeTextArea(self, id, targetPlayer=""):
        p = ByteArray().writeInt(id)
        if targetPlayer == "":
            self.sendAll(Identifiers.send.Remove_Text_Area, p.toByteArray())
        else:
            client = self.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Remove_Text_Area, p.toByteArray())

    def setNameColor(self, playerName, color):
        if playerName in self.clients:
            self.sendAll(Identifiers.send.Set_Name_Color, ByteArray().writeInt(self.clients.get(playerName).playerCode).writeInt(color).toByteArray())
    
    def showColorPicker(self, id, targetPlayer, defaultColor, title):
        packet = ByteArray().writeInt(id).writeInt(defaultColor).writeUTF(title)
        if targetPlayer == "":
            self.sendAll(Identifiers.send.Show_Color_Picker, packet.toByteArray())
        else:
            player = self.clients.get(targetPlayer)
            if player != None:
                player.sendPacket(Identifiers.send.Show_Color_Picker, packet.toByteArray())

    def spawnNPC(self, npcName, data={}): ####################
        self.sendAll(Identifiers.send.NPC, ByteArray().writeInt(int(data["id"]) if "id" in data else 0).writeUTF(npcName).writeShort(int(data["title"]) if "title" in data else 0).writeBoolean(bool(data["starePlayer"]) if "starePlayer" in data else False).writeUTF(data["look"] if "look" in data else "").writeShort(int(data["x"]) if "x" in data else 0).writeShort(int(data["y"]) if "y" in data else 0).writeShort(1).writeByte(11).writeShort(0).toByteArray())
        

    def updateTextArea(self, id, text, targetPlayer):
        p = ByteArray().writeInt(id).writeUTF(text)
        if targetPlayer == "":
            self.sendAll(Identifiers.send.Update_Text_Area, p.toByteArray())
        else:
            client = self.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Update_Text_Area, p.toByteArray())

        
async def setup(db):
    db = await aiosqlite.connect(db)
    db.text_factory = str
    db.isolation_level = None
    db.row_factory = aiosqlite.Row
    cursor = await db.cursor()
    return db, cursor

if __name__ == "__main__":
    # Connection Settings
    config = configparser.ConfigParser()
    config.read("./include/configs.properties")

    # Transformice
    Database, Cursor = None, None
    Database = pymongo.MongoClient('mongodb://localhost:27017')['transformice1']
    Cursor = Database
    
    # Maps
    DatabaseMaps, CursorMaps = asyncio.get_event_loop().run_until_complete(setup('./database/Maps.db'))

    # Cafe
    DatabaseCafe, CursorCafe = asyncio.get_event_loop().run_until_complete(setup('./database/Cafe.db'))

    # Connection Server
    _Server = Server()
