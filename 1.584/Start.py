#coding: utf-8
import requests, re, os, sys, json, time, random, sqlite3, pymysql, traceback, zlib, asyncio, urllib.request, binascii, configparser
import time as _time
from time import gmtime, strftime
from datetime import datetime, date, timedelta

# Utils and Modules
from utils import *
from modules import *
from colorconsole  import win
from importlib import reload

class Reactor1:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
    def callLater(self, *args, **kwargs):
        return self.loop.call_later(*args, **kwargs)
    def callFromThread(self, func):
        return func()
reactor = Reactor1()

# Others
sys.dont_write_bytecode = True
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))

def InfinityLoop():
    time.sleep(10000)
    InfinityLoop()

class Client:
    def __init__(self, _server):

        # String
        self.langue = ""
        self.server = _server
        self.packages = ByteArray()
        self.realLangue = json.load(urllib.request.urlopen("http://ipinfo.io/json"))["country"].lower()
        self.nickColor = "#95d9d6"
        self.mouseName = ""
        self.roomName = ""
        self.emailAddress = ""
        self.marriage = ""
        self.lastroom = "1"
        self.shopItems = ""
        self.tribeName = ""
        self.nameColor = ""
        self.chatColor = ""
        self.tradeName = ""
        self.playerName = ""
        self.shamanItems = ""
        self.lastMessage = ""
        self.tribeMessage = ""
        self.tempMouseColor = ""
        self.silenceMessage = ""
        self.currentCaptcha = ""
        self.mouseColor = "78583a"
        self.shamanColor = "95d9d6"
        self.modoPwetLangue = "ALL"
        self.playerLook = "1;0,0,0,0,0,0,0,0,0,0,0"
        self.shamanLook = "0,0,0,0,0,0,0,0,0,0"
        self.fur = ""
        self.botVillage = ""
        self.lastNpc = ""
        self.roles = ""
        
        # Integer
        self.lastReportID = 0
        self.playerKarma = 0
        self.pingTime = 0
        self.flypoints = 0
        self.pet = 0
        self.activeArtefact = 0
        self.posX = 0
        self.ClientGotHole = 1
        self.posY = 0
        self.velX = 0
        self.velY = 0
        self.gender = 0
        self.playerTime = 0
        self.loginTime = 0
        self.petEnd = 0
        self.viewMessage = 0
        self.priceDoneVisu = 0
        self.lastOn = 0
        self.regDate = 0
        self.langueID = 0
        self.useAnime = 0
        self.playerID = 0
        self.banHours = 0
        self.iceCount = 0 #2
        self.privLevel = 0
        self.nowTokens = 0
        self.nowCoins = 0
        self.shamanExp = 0
        self.tribeCode = 0
        self.tribeRank = 0
        self.tribeChat = 0
        self.titleStars = 0
        self.firstCount = 0
        self.playerCode = 0
        self.shamanType = 0
        self.tribeHouse = 0
        self.tribeJoined = 0
        self.silenceType = 0
        self.playerScore = 0
        self.titleNumber = 0
        self.cheeseCount = 0
        self.shopFraises = 0
        self.shamanSaves = 0
        self.shamanLevel = 1
        self.lastGameMode = 0
        self.bubblesCount = 0
        self.currentPlace = 0
        self.shamanCheeses = 0
        self.hardModeSaves = 0
        self.bootcampCount = 0
        self.shopCheeses = 0
        self.shamanExpNext = 32
        self.ambulanceCount = 0
        self.defilantePoints = 0
        self.divineModeSaves = 0
        self.lastDivorceTimer = 0
        self.TimeGiro = 0
        self.equipedShamanBadge = 0
        self.playerStartTimeMillis = 0
        self.racingRounds = 0
        self.defilanteRounds = 0
        self.fastracingRounds = 0
        self.bootcampRounds = 0
        self.survivorDeath = 0
        self.countTime = 1
        self.countP = 0
        self.cannonX = 2
        self.cannonY = 8
        self.cXpos = 189
        self.cYpos = 133
        self.cnCustom = 0
        self.page = 1
        self.lastPacketID = random.randint(0, 99)
        self.authKey = random.randint(0, 2147483647)
        self.TFMUtils = Utils
        self.tribulleID = 0
        self.artefactID = 0
        self.drawingColor = 0
        self.lastTopicID = 0
        self.currentPost = 0

        # Bool
        self.isLuaAdmin = False
        self.isReloadCafe = False
        self.isAfk = False
        self.isDead = False
        self.isMute = False
        self.isMumute = False
        self.isCafe = False
        self.isGuest = False
        self.isVoted = False
        self.isTrade = False
        self.useTotem = False
        self.openStaffChat = False
        self.isHidden = False
        self.isClosed = False
        self.isShaman = False
        self.hasEnter = False
        self.isSkill = False
        self.isSuspect = False
        self.isVampire = False
        self.hasCheese = False
        self.hasBolo = False
        self.hasBolo2 = False
        self.selfGet = False
        self.isJumping = False
        self.resetTotem = False
        self.isModoPwet = False
        self.isModoPwetNotifications = False
        self.canRespawn = False
        self.enabledLua = False
        self.isNewPlayer = False
        self.isEnterRoom = False
        self.tradeConfirm = False
        self.canUseConsumable = True
        self.canSkipMusic = False
        self.isReloadCafe = False
        self.isMovingLeft = False
        self.isMovingRight = False
        self.isOpportunist = False
        self.qualifiedVoted = False
        self.desintegration = False
        self.canShamanRespawn = False
        self.validatingVersion = False
        self.canRedistributeSkills = False
        self.libCn = False
        self.canCN = False
        self.isFly = False
        self.isFlyMod = False
        self.isSpeed = False
        self.isFFA = False
        self.canSpawnCN = True
        self.isTeleport = False
        self.chatdisabled = False
        self.canKiss = True
        self.openingFriendList = False
        self.isTribeOpen = False
        self.hasArtefact = False
        self.porno = False
        self.showButtons = True
        self.isBlockAttack = True
        self.isPrisoned = False
        self.hasLuaTransformations = False
        self.lastping = False
        
        # Staff Positions
        self.isLuaCrew = False
        self.isMapCrew = False
        self.isFashionSquad = False
        self.isFunCorpPlayer = False

        # Others
        self.Cursor = Cursor
        self.CursorCafe = CursorCafe
        self.CMDTime = time.time()
        self.CAPTime = time.time()
        self.CTBTime = time.time()
        self.CRTTime = time.time()

        # Nonetype
        self.room = None
        self.awakeTimer = None
        self.skipMusicTimer = None
        self.resSkillsTimer = None
        self.followed = None
        
        # List
        self.totem = [0, ""]
        self.PInfo = [0, 0, 400]
        self.tempTotem = [0, ""]
        self.racingStats = [0] * 4
        self.survivorStats = [0] * 4

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
        self.bootcampTitleList = []
        self.hardModeTitleList = []
        self.equipedConsumables = []
        self.ignoredTribeInvites = []
        self.divineModeTitleList = []
        self.ignoredMarriageInvites = []
        self.ModoWatchedPlayers = []
        self.custom = []
        self.dailyMissions = [0, 0, 0, 0]
        self.deathStats = []
        self.visuDone = []
        self.visusRemove = []

        # Dict
        self.ipInfo = eval(urllib.request.urlopen("https://extreme-ip-lookup.com/json/").read())
        self.shopBadges = {}
        self.tribeRanks = ""
        self.playerSkills = {}
        self.tradeConsumables = {}
        self.playerConsumables = {}
        self.playerMissions = {}
        self.itensBots = {"Papaille": [(4, 800, 50, 4, 2253, 50), (4, 800, 50, 4, 2254, 50), (4, 800, 50, 4, 2257, 50), (4, 800, 50, 4, 2260, 50), (4, 800, 50, 4, 2261, 50)], "Santa Claus": [(1, 34, 1, 4, 2254, 100), (1, 174, 1, 4, 2254, 100), (4, 6, 50, 4, 2253, 50), (3, 312, 1, 4, 2253, 50)], "Easter Chappie": [(1, 65, 1, 4, 2254, 100), (1, 64, 1, 4, 2254, 100), (1, 170, 1, 4, 2254, 100), (4, 6, 50, 4, 2254, 100), (3, 426, 1, 4, 2254, 100)], "Buffy": [(1, 147, 1, 4, 2254, 200), (2, 17, 1, 4, 2254, 150), (2, 18, 1, 4, 2254, 150), (2, 19, 1, 4, 2254, 150), (3, 398, 1, 4, 2254, 150), (3, 392, 1, 4, 2254, 50)], "Indiana Mouse": [(3, 255, 1, 4, 2257, 50), (3, 394, 1, 4, 2257, 50), (3, 395, 1, 4, 2257, 50), (3, 320, 1, 4, 2257, 50), (3, 393, 1, 4, 2257, 50), (3, 402, 1, 4, 2257, 50), (3, 397, 1, 4, 2257, 50), (3, 341, 1, 4, 2257, 50), (3, 335, 1, 4, 2257, 25), (3, 403, 1, 4, 2257, 50), (1, 6, 1, 4, 2257, 50), (1, 17, 1, 4, 2257, 50)], "Elise": [(4, 31, 2, 4, 2261, 5), (4, 2256, 2, 4, 2261, 5), (4, 2232, 2, 4, 2253, 1), (4, 21, 5, 4, 2253, 1), (4, 33, 2, 4, 2260, 1), (4, 33, 2, 4, 2254, 1)], "Oracle": [(1, 145, 1, 4, 2253, 200), (2, 16, 1, 4, 2253, 150), (2, 21, 1, 4, 2253, 150), (2, 24, 1, 4, 2253, 150), (2, 20, 1, 4, 2253, 150), (3, 390, 1, 4, 2253, 50), (3, 391, 1, 4, 2253, 200), (3, 399, 1, 4, 2253, 150)], "Prof": [(4, 800, 20, 4, 2257, 10), (4, 19, 2, 4, 2257, 5), (4, 2258, 2, 4, 2257, 4), (4, 2262, 5, 4, 2257, 2), (4, 2259, 10, 4, 2257, 1), (4, 20, 1, 4, 2257, 2)], "Cassidy": [(1, 154, 1, 4, 2261, 200), (2, 23, 1, 4, 2261, 150), (3, 400, 1, 4, 2261, 100)], "Von Drekkemouse": [(2, 22, 1, 4, 2260, 150), (1, 153, 1, 4, 2260, 200), (3, 401, 1, 4, 2260, 100)], "Tod": [(4, 2259, 10, 4, 2257, 1), (4, 2258, 10, 4, 2254, 230), (3, 401, 1, 4, 2260, 100)], "Fishing2017": [(1, 184, 1, 4, 2257, 200), (2, 24, 1, 4, 2257, 150), (2, 29, 1, 4, 2257, 150), (3, 422, 1, 4, 2257, 200)]}
        self.aventureCounts = {}
        self.aventurePoints = {}
    
    def eof_received(self):
        pass

    def getnewlen(self,b):
        var_2068 = 0
        var_2053 = 0
        var_176 = b
        while var_2053 < 10:
            var_56 = var_176.readByte() & 255
            var_2068 = var_2068 | (var_56 & 127) << 7 * var_2053
            var_2053 += 1
            if not ((var_56 & 128) == 128 and var_2053 < 5):
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
                self.parseString(read)
            else:
                self.packages = oldpacket
                break


    def getText(self, object, *params):
        keys = object.split(".")
        json = self.server.menu["texts"][self.langue]
        i = 0
        while i < len(keys):
            key = keys[i]
            if i == len(keys) - 1:
                text = json[key]
                count = 0
                while count < len(params):
                    text = text.replace("%" + str(count + 1), str(params[count]))
                    count += 1
                return text
            else: json = json[key]
            i += 1
        return ""
        
    def close(self):
        i = 10002
        while i <= 10500:
            self.room.removeTextArea(i, self.playerName)
            i += 1

    def sendAddPopupText(self, id, x, y, l, a, fur1, fur2, opcit, Message):
        bg = int(fur1, 16)
        bd = int(fur2, 16)
        data = struct.pack("!i", id)
        data = data + struct.pack("!h", len(Message))
        data = data + Message + struct.pack("!hhhhiibb", int(x), int(y), int(l), int(a), int(bg), int(bd), int(opcit), 0)
        self.sendPacket([29, 20], data)

    
    def connection_made(self, transport):
        self.transport = transport
        self.ipAddress = transport.get_extra_info("peername")[0]
        self.modoPwet = ModoPwet(self, self.server)
        self.tribulle = Tribulle(self, self.server)
        self.Shop = Shop(self, self.server)
        self.Skills = Skills(self, self.server)
        self.Packets = Packets(self, self.server)
        self.Commands = Commands(self, self.server)
        self.ModoCommands = ModoCommands(self, self.server) # Modo
        self.missions = Missions(self, self.server)
        self.AntiCheat = AntiCheat(self, self.server)
        if self.ipAddress in self.server.connectedCounts:
            self.server.connectedCounts[self.ipAddress] += 1
        else:
            self.server.connectedCounts[self.ipAddress] = 1
        if self.server.connectedCounts[self.ipAddress] >= 9999999999999999999999999 or self.ipAddress in self.server.IPPermaBanCache or self.ipAddress in self.server.IPTempBanCache:
            self.transport.close()
            self.server.IPTempBanCache.append(self.ipAddress)

    def checkReport(self, array, playerName):
        return playerName in array

    def connection_lost(self, args):
        self.isClosed = True
        if self.ipAddress in self.server.connectedCounts:
            count = self.server.connectedCounts[self.ipAddress] - 1
            if count <= 0:
                del self.server.connectedCounts[self.ipAddress]
            else:
                self.server.connectedCounts[self.ipAddress] = count

        if self.playerName in self.server.players:
            del self.server.players[self.playerName]
                
            if self.isTrade:
                self.cancelTrade(self.tradeName)

            if self.playerName in self.server.reports:
                if not self.server.reports[self.playerName]["state"] == "banned":
                    self.server.reports[self.playerName]["state"] = "disconnected"
                    self.modoPwet.updateModoPwet()
                    if self.privLevel >= 7 and self.isModoPwetNotifications:
                        self.sendmodServerMessage("<ROSE>[Modopwet]</ROSE><BL> The reported player <BV>"+self.playerName+"</BV> has disconnected from game.</BL>")

            if self.playerName in self.server.chatMessages:
                self.server.chatMessages[self.playerName] = {}
                del self.server.chatMessages[self.playerName]

            for player in self.server.players.values():
                if self.playerName and player.playerName in self.friendsList and player.friendsList:
                    player.tribulle.sendFriendDisconnected(self.playerName)

            if self.tribeCode != 0:
                self.tribulle.sendTribeMemberDisconnected()

            if not self.playerName == "":
                if not self.isGuest:
                    self.updateDatabase()
            reactor.callFromThread(self.updateDatabase)            

        if self.room != None:
            self.room.removeClient(self)
            
        self.sendModInfo(0)
        

    def sendPacket(self, identifiers, data=b""):
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
        
    def sendPacketTribulle(self, code, result):
        self.sendPacket([60, 3], ByteArray().writeShort(code).writeBytes(result).toByteArray())

    def parseString(self, packet):
        if self.isClosed:
            return
             
        packetID, C, CC = packet.readByte(), packet.readByte(), packet.readByte()        
        if not self.validatingVersion:
            if (C == Identifiers.recv.Informations.C and CC == Identifiers.recv.Informations.Correct_Version) and not (self.isClosed):
                version = packet.readShort()
                ckey = packet.readUTF()

                if not ckey == self.server.CKEY and version != self.server.Version:
                    print("[%s] [WARN] Invalid version or CKey (%s, %s)" %(time.strftime("%H:%M:%S"), version, ckey))
                    self.transport.close()
                # if "StandAlone" in packet.toByteArray():
                    # print "[%s] [%s] Someone tried to log in the game with standalone." % (time.strftime("%H:%M:%S"), this.transport.getPeer().host)
                else:
                    self.validatingVersion = True
                    self.sendCorrectVersion()

                    
        else:
            try:
                self.lastPacketID = (self.lastPacketID + 1) % 100
                self.lastPacketID = packetID
                self.Packets.parsePacket(packetID, C, CC, packet)
            except:
                with open("./logs/Errors/Server.log", "a") as f:
                    traceback.print_exc(file=f)
                    f.write("\n")

    def isValidIP(self, ip):
        m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
        return bool(m) and all(map(lambda n: 0 <= int(n) <= 255, m.groups()))

    def TFMIP(self, ip):
        ip = '.'.join([hex(int(x)+256)[3:].upper() for x in ip.split('.')])
        return '#' + ip

    def TFMIPDEC(self, ip):
        ip = ip[1:]
        result = []
        for i in ip.split('.'):
            if int(i, 16):
                result.append(int(i, 16))
            else:
                result.append(int(i))
        result = [str(i) for i in result]
        return '.'.join(result)

    def ipColor(self, ip):
        if self.isValidIP(ip):
            country = self.getCountryIP(ip)
            if country == "localhost": return "#FFFFFF"
            elif country == "AF": return "#C58EB5"
            elif country == "AX": return "#6B1C72"
            elif country == "AL": return "#AEEAD4"
            elif country == "DZ": return "#DB7B27"
            elif country == "AS": return "#D1C58B"
            elif country == "AD": return "#E3796A"
            elif country == "AO": return "#CC1BA7"
            elif country == "AI": return "#6BF8DC"
            elif country == "AQ": return "#6F4B48"
            elif country == "AG": return "#6CF1B2"
            elif country == "AR": return "#83F8ED"
            elif country == "AM": return "#334870"
            elif country == "AW": return "#49DE03"
            elif country == "AU": return "#1D7592"
            elif country == "AT": return "#8B1A61"
            elif country == "AZ": return "#0707A8"
            elif country == "BS": return "#ED8E8A"
            elif country == "BH": return "#12AB7C"
            elif country == "BD": return "#D474DF"
            elif country == "BB": return "#B1E53B"
            elif country == "BY": return "#44F7A7"
            elif country == "BE": return "#17408E"
            elif country == "BZ": return "#D0A339"
            elif country == "BJ": return "#D22745"
            elif country == "BM": return "#6B7337"
            elif country == "BT": return "#411046"
            elif country == "BO": return "#07F95D"
            elif country == "BA": return "#38499C"
            elif country == "BW": return "#FC764B"
            elif country == "BV": return "#460519"
            elif country == "BR": return "#F646AD"
            elif country == "VG": return "#6151C4"
            elif country == "IO": return "#EEF99A"
            elif country == "BN": return "#488456"
            elif country == "BG": return "#86923F"
            elif country == "BF": return "#A2E99B"
            elif country == "BI": return "#628875"
            elif country == "KH": return "#63815C"
            elif country == "CM": return "#D1D9A7"
            elif country == "CA": return "#F4350A"
            elif country == "CV": return "#1D90CB"
            elif country == "KY": return "#A763B4"
            elif country == "CF": return "#1C2CD5"
            elif country == "TD": return "#1CB2E4"
            elif country == "CL": return "#DA02D0"
            elif country == "CN": return "#C2B913"
            elif country == "HK": return "#153DC6"
            elif country == "MO": return "#1916D9"
            elif country == "CX": return "#7091CA"
            elif country == "CC": return "#0BF7CB"
            elif country == "CO": return "#679F99"
            elif country == "KM": return "#B4B3D4"
            elif country == "CG": return "#041EFE"
            elif country == "CD": return "#7BEE02"
            elif country == "CK": return "#54F6F2"
            elif country == "CR": return "#D77285"
            elif country == "CI": return "#581652"
            elif country == "HR": return "#65630A"
            elif country == "CU": return "#78191F"
            elif country == "CY": return "#19A49C"
            elif country == "CZ": return "#4CCC23"
            elif country == "DK": return "#43B03A"
            elif country == "DJ": return "#FBA09A"
            elif country == "DM": return "#B15CA7"
            elif country == "DO": return "#FB444D"
            elif country == "EC": return "#FED520"
            elif country == "EG": return "#83DD1F"
            elif country == "SV": return "#12CA78"
            elif country == "GQ": return "#54692D"
            elif country == "ER": return "#EAE0BC"
            elif country == "EE": return "#A0E0DF"
            elif country == "ET": return "#852757"
            elif country == "FK": return "#5C2929"
            elif country == "FO": return "#DE6375"
            elif country == "FJ": return "#342172"
            elif country == "FI": return "#7CD3B0"
            elif country == "FR": return "#F52252"
            elif country == "GF": return "#8E7700"
            elif country == "PT": return "#1DE162"
            elif country == "TF": return "#BE4FAA"
            elif country == "GM": return "#95B846"
            elif country == "GE": return "#EC8BE1"
            elif country == "DE": return "#16B55A"
            elif country == "GH": return "#7A5029"
            elif country == "GI": return "#A02D37"
            elif country == "GR": return "#2903CD"
            elif country == "GL": return "#B8263A"
            elif country == "GD": return "#0EFD9A"
            elif country == "GP": return "#CD74D1"
            elif country == "GU": return "#BDA9CC"
            elif country == "GT": return "#8C2EA1"
            elif country == "GG": return "#DE0008"
            elif country == "GN": return "#3542EB"
            elif country == "GW": return "#74E6F6"
            elif country == "GY": return "#3AA6CD"
            elif country == "HT": return "#819DDC"
            elif country == "HM": return "#D1D405"
            elif country == "VA": return "#E6B3BF"
            elif country == "HN": return "#5CD452"
            elif country == "HU": return "#E8CD6B"
            elif country == "IS": return "#F0AAE8"
            elif country == "IN": return "#09A527"
            elif country == "ID": return "#C7EBBF"
            elif country == "IR": return "#C9B81B"
            elif country == "IQ": return "#D53FA7"
            elif country == "IE": return "#894798"
            elif country == "IM": return "#25136B"
            elif country == "IL": return "#3FF8F6"
            elif country == "IT": return "#0F431B"
            elif country == "JM": return "#565122"
            elif country == "JP": return "#BCCF48"
            elif country == "JE": return "#10955F"
            elif country == "JO": return "#075E7B"
            elif country == "KZ": return "#492100"
            elif country == "KE": return "#3C5FCC"
            elif country == "KI": return "#ECBF23"
            elif country == "KP": return "#975EEA"
            elif country == "KR": return "#59B7F2"
            elif country == "KW": return "#1B6B53"
            elif country == "KG": return "#511DC9"
            elif country == "LA": return "#E5776F"
            elif country == "LV": return "#6B41A3"
            elif country == "LB": return "#4C5A3B"
            elif country == "LS": return "#57F3BD"
            elif country == "LR": return "#505C34"
            elif country == "LY": return "#540596"
            elif country == "LI": return "#67BAC7"
            elif country == "LT": return "#F734A4"
            elif country == "LU": return "#D77A35"
            elif country == "MK": return "#4B9F2F"
            elif country == "MG": return "#720D8E"
            elif country == "MW": return "#8F4A99"
            elif country == "MY": return "#94187D"
            elif country == "MV": return "#C65430"
            elif country == "ML": return "#E39F70"
            elif country == "MT": return "#1EB6B3"
            elif country == "MH": return "#C6A041"
            elif country == "MQ": return "#40ECD7"
            elif country == "MR": return "#B017B3"
            elif country == "MU": return "#06053B"
            elif country == "YT": return "#6FEF9E"
            elif country == "MX": return "#B9D253"
            elif country == "FM": return "#AA14F5"
            elif country == "MD": return "#306225"
            elif country == "MC": return "#653C54"
            elif country == "MN": return "#F6F6DC"
            elif country == "ME": return "#B04D86"
            elif country == "MS": return "#C886BD"
            elif country == "MA": return "#7D818E"
            elif country == "MZ": return "#04003D"
            elif country == "MM": return "#3244B4"
            elif country == "NR": return "#CD510E"
            elif country == "NP": return "#94C9C8"
            elif country == "NL": return "#BB22BA"
            elif country == "AN": return "#9BD247"
            elif country == "NC": return "#E8E08E"
            elif country == "NZ": return "#A36396"
            elif country == "NI": return "#94D546"
            elif country == "NE": return "#636A56"
            elif country == "NG": return "#818654"
            elif country == "NU": return "#3CE240"
            elif country == "NF": return "#F46BC9"
            elif country == "NP": return "#620542"
            elif country == "NO": return "#20687F"
            elif country == "OM": return "#38394D"
            elif country == "PK": return "#7F346A"
            elif country == "PW": return "#8CDDEB"
            elif country == "PS": return "#D67666"
            elif country == "PA": return "#2E31B2"
            elif country == "US": return "#2E31B2"
            # 	Papua New Guinea	
        else:
            return "#A1EBD9"

    def getCountryIP(self, ip):
        if ip == "127.0.0.1" or ip == "::1":
            return "localhost"
        elif self.isValidIP(ip):
            r = urllib.request.urlopen(f"https://freegeoip.app/json/{ip}")
            d = json.loads(r.read())
            r.close()
            return d["country_code"]
        else:
            ip1 = self.TFMIPDEC(ip)
            self.getCountryIP(ip1)
            
    def BulleServer(self, commu):
        if commu == '*': return "bulle4"
        elif commu == 'EN': return "bulle1"
        elif commu == 'FR': return "bulle2"
        elif commu == 'RU': return "bulle3"
        elif commu == 'BR': return "bulle4"
        elif commu == 'ES': return "bulle5"
        elif commu == 'CN': return "bulle6"
        elif commu == 'TR': return "bulle7"
        elif commu == 'VK': return "bulle8"
        elif commu == 'PL': return "bulle9"
        elif commu == 'HU': return "bulle7"
        elif commu == 'NL': return "bulle7"
        elif commu == 'RO': return "bulle2"
        elif commu == 'ID': return "bulle8"
        elif commu == 'IT': return "bulle3"
        elif commu == 'DE': return "bulle8"
        elif commu == 'E2': return "bulle5"
        elif commu == 'AR': return "bulle1"
        elif commu == 'PH': return "bulle6"
        elif commu == 'LT': return "bulle1"
        elif commu == 'JP': return "bulle9"
        elif commu == 'FI': return "bulle2"
        elif commu == 'CH': return "bulle3"
        elif commu == 'CZ': return "bulle9"
        elif commu == 'SK': return "bulle3"
        elif commu == 'HR': return "bulle6"
        elif commu == 'BG': return "bulle5"
        elif commu == 'LV': return "bulle4"
        elif commu == 'HE': return "bulle6"
        elif commu == 'ET': return "bulle8"
        else: return "bulle2"

    def sendDeathBoard(self):
        position = 1
        shown = "<V><p align='center'><FC>DeathCount Leaderboard</font></p>\n"
        shown += "<p align='center'><font size='12'>"
        self.Cursor.execute("select Username, deathCount from users where PrivLevel < 200 ORDER By deathCount DESC LIMIT 100")
        for rrf in self.Cursor.fetchall():
            playerName = str(rrf[0])
            deathCount = rrf[1]
            shown += "<font color='#E96D84'>"+str(position)+"</font> <font color='#3C5064'>-</font> <font color='#B7E96D'>"+str(playerName)+"</font> <font color='#3C5064'>-</font> <font color='#6DB5E9'>"+str(deathCount)+"</font>"
            shown += "<br />"
            position += 1

        self.sendLogMessage(shown + "</font></p>")

    def sendModerationCommands(self):
        message = "Moderation Commands: [] - required | () - optional \n"
        if self.privLevel >= 7:
            message += "<VP>Commands for 'Naughty Mice'</VP>:\n"
            message += "<J>/ban</J> <VP>[PlayerName] [Duration] [Reason]</VP> - <BL> Bans the player for the defined duration.\n"
            message += "<J>/iban</J> <VP>[PlayerName] [Duration] [Reason]</VP> - <BL> Bans the player for the defined duration, but the pink text doesn't show.\n"
            message += "<J>/banhack</J> <VP>[PlayerName]</VP> - <BL> Special ban command for cheaters, ban them for 360/720/1080... hours.\n"
            message += "<J>/ibanhack</J> <VP>[PlayerName]</VP> - <BL> same as /banhack, but the pink text doesn't show.\n"
            message += "<J>/unban</J> <VP>[PlayerName]</VP> - <BL> Removes the last ban from a player's account.\n"
            message += "<J>/unbanip</J> <VP>[IP]</VP> - <BL> Removes the last ban from the selected IP address.\n"
            message += "<J>/clearban</J> <VP>[PlayerName]</VP> - <BL> Removes the vote ban on a player's account.\n"
            message += "<J>/mute</J> <VP>[PlayerName] [Duration] [Reason]</VP> - <BL> Prevents the player from speaking for the set amount of time.\n"
            message += "<J>/imute</J> <VP>[PlayerName] [Duration] [Reason]</VP> - <BL> Prevents the player's IP address from speaking for the set amount of time.\n"
            message += "<J>/unmute</J> <VP>[PlayerName]</VP> - <BL> Removes a player's mute.\n"
            message += "<J>/mumute</J> <VP>[PlayerName]</VP> - <BL> Prevents the player from speaking without knowing it, just for the duration of the connection.\n"
            message += "<J>/kick</J> <VP>[PlayerName]</VP> - <BL> Disconnects the player from the server.\n"
            message += "<J>/prison</J> <VP>[PlayerName]</VP> - <BL> Teleports the player to 'Bad Girls' room and does not let them leave (use again to return them to a normal room).\n"
        if self.privLevel >= 8:
            message += "<J>/removeplayerrecords</J> <VP>[PlayerName]</VP> - <BL> Remove all records from player's account.\n"
        if self.privLevel >= 7:
            message += "<VP><br><N>Chats & Staff Chats Commands:<N></VP>\n"
            message += "<J>/m</J> <VP>[Message]</VP> - <BL> Send message in your community in #Modo.\n"
            message += "<J>/m*</J> <VP>[Message]</VP> - <BL> Send international message in #Modo.\n"
            message += "<J>/lsmodo</J> - <BL> Lists the moderators and administrators connected as well as their language.\n"
            message += "<J>/a</J> <VP>[Message]</VP> - <BL> Send message in your community in #Arbitre.\n"
            message += "<J>/a*</J> <VP>[Message]</VP> - <BL> Send international message in #Arbitre.\n"
            message += "<J>/lsarb</J> - <BL> Lists the arbitres connected as well as their language.\n"
        if self.privLevel >= 8:
            message += "<J>/ms</J> <VP>[Message]</VP> - <BL> Speak in pinktext in the room.\n"
            message += "<J>/clearchat</J> - <BL> Clear the chat.\n"
        if self.privLevel >= 7:
            message += "<br><N><VP>IP Commands:<VP><N>\n"
            message += "<J>/ip</J> <VP>(PlayerName)</VP> - <BL> Get the IP on player's Account.\n"
            message += "<J>/nomip</J> <VP>[PlayerName]</VP> - <BL> Gives the IPs connecting to an account since the last server restart.\n"
            message += "<J>/ipnom</J> <VP>[IP]</VP> - <BL> Gives the accounts a specific IP has connected to since the last server restart.\n"
            message += "<J>/l</J> <VP>[PlayerName|IP]</VP> - <BL> Gives the last 200 connections to an account (IP/time/country) / specific IP.\n"
            message += "<J>/relation</J> <VP>[PlayerName]</VP> - <BL> Gives list of related accounts since the last reboot.\n"
            message += "<br><N><VP>Room Commands:<VP><N>\n"
            message += "<J>/room*</J> <VP>[RoomName]</VP> - <BL> Joins the specified room on the specified community. (eg. /room* en-1 would join 1 on EN community).\n"
            message += "<J>/follow</J> <VP>[PlayerName]</VP> - <BL> Joins the room of a specific player.\n"
            message += "<J>/ninja</J> <VP>[PlayerName]</VP> - <BL> Same as [watch] in modopwet.\n"
            message += "<J>/search</J> <VP>[playerPartName]</VP> - <BL> Give the name of the room where a player is located.\n"
            message += "<J>/roomkick</J> <VP>[PlayerName]</VP> - <BL> Kick the player from the room (Move him to 1).\n"
            message += "<J>/closeroom</J> <VP>(RoomName)</VP> - <BL> Kicks everyone from the room.\n"
            message += "<J>/ls</J> <VP>(Text)</VP> - <BL> Give the number of mice in a living room.\n"
            message += "<J>/lsc</J> - <BL> Give the number of mice per community.\n"
            message += "<J>/lsroom</J> <VP>(RoomName)</VP> - <BL> List the names of the mice in a living room and their IP address.\n"
            message += "<J>/roompw</J> <VP>[RoomName]</VP> - <BL> Gets the room password if have.\n"
            message += "<J>/creator</J> - <BL> Displays the creator of the room you are in.\n"
        if self.privLevel >= 8:
            message += "<J>/moveplayer</J> <VP>[PlayerName] [RoomName]</VP> - <BL> Move the player in specific room.\n"
        if self.privLevel >= 9:
            message += "<J>/move</J> <VP>[RoomName]</VP> - <BL> Move all players in specific room.\n"
        if self.privLevel >= 7:
            message += "<br><N><VP>Misc:<VP><N>\n"
            message += "<J>/casier</J> <VP>[PlayerName]</VP> - <BL> Gets sanction logs of playerName.\n"
            message += "<J>/chatlog</J> <VP>[PlayerName]</VP> - <BL> Get the chat messages on player's account.\n"
            message += "<J>/hide</J> - <BL> Makes you invisible, use this command again for make you visible.\n"
            message += "<J>/chatfilter</J> <VP>[string|del string|list]</VP> - <BL> Get list of blacklisted words / Add or Delete a string from chat filter.\n"
            message += "<J>/commu </J> <VP>[Community]</VP> <BL> - Changes your community in-game.\n"
            message += "<J>/log</J> <BL> - Show the list the last 200 bans put into play.\n"
            message += "<J>/delrecord</J> <VP>[mapCode]</VP> <BL> - Delete the record on map.\n"
            message += "<J>/infotribu</J> <VP>[Tribe Name]</VP> <BL> - Get information about a tribe.\n"
            message += "<J>/infocommu</J> <VP>[Community]</VP> <BL> - Get the list of players in the community.\n"
            message += "<J>/lsbulle</J> <BL> - Get information about the servers.\n"
        if self.privLevel >= 8:
            message += "<J>/playerping</J> <VP>[PlayerName]</VP> <BL> - Get a player's ping.\n"
            message += "<J>/arb</J> <VP>[PlayerName]</VP> <BL> - Add/Remove arbitre powers on player's account.\n"
            message += "<J>/max</J>  <BL> - Gives the maximum number of connected players since the last reboot.\n"
            #message += "<J>/resign</J> <BL> - Removes all powers from your character, this is a resignation order.\n"
        if self.privLevel >= 7:
            message += "<br><N><VP>#Modo Commands:<N><VP>\n"
            message += "<J>.avatar</J> <VP>[PlayerName]</VP> <BL> - Gives the link to a player's avatar.\n"
            message += "<J>.profile</J> <VP>[PlayerName]</VP> <BL> - Gives the profile of a player.\n"
            #message += "<J>.bulleinfo</J> <VP>[BulleID]</VP> <BL> - Gets information about the bulle.\n"
        if self.privLevel >= 9:
            message += "<br><N>Administration Commands:<N>\n"
            message += "<J>/updatesql</J> - <BL> Update the database in the game.\n"
            message += "<J>/smc</J> <VP>[Message]</VP> - <BL> Send message to all players.\n"
            message += "<J>/settime</J> <VP>[Time]</VP> - <BL> Set a time in current round (seconds).\n"
            message += "<J>/changemapname</J> <VP>[MapCode] [PlayerName]</VP> - <BL> Changes the map author.\n"
            message += "<J>/commandlog</J> <VP>[PlayerName]</VP> - <BL> Gets command log of playerName.\n"
            message += "<J>/anim</J> <VP>[PlayerName] [Anim_ID] [Frame_ID] </VP> - <BL> Adds animation to player.\n"
            message += "<J>/frame</J> <VP>[PlayerName] [Frame_ID] [X] [Y] </VP> - <BL> Adds frame to player.\n"
            #message += "<J>/resetprofile</J> <VP>[PlayerName]</VP> - <BL> Resets playerName's profile.\n"
            message += "<J>/tns</J> - <BL> Gives 20 cheeses and fraises to all players.\n"
            message += "<J>/re</J> <VP>(PlayerName)</VP> - <BL> Respawn someone or yourself.\n"
            message += "<J>/playersql</J> <VP>[Name] [ID] [Value]</VP> - <BL> Change a player's something with specific value in database.\n"
            message += "<J>/luaadmin</J> - <BL> Execute scripts as administrator.\n"
            message += "<J>/reboot</J> - <BL> Reboot the server (2 minutes).\n"
            message += "<J>/shutdown</J> - <BL> Shutdown the server (2 minutes).\n"
            message += "<J>/fshutdown</J> - <BL> Shutdown the server (10 seconds).\n"
            message += "<J>/serverconfigs</J> - <BL> Open and shows the configs.properties file.\n"
            message += "<J>/clearlog</J> <VP>[records|reports|loginlog|commandlog|banlog|ippermacache|iptempcache]</VP> - <BL> Resets the specific log from the server.\n"
            message += "<J>/viewlog</J> <VP>[iptemp|errors|cache]</VP> - <BL> View the specific log from the server.\n"
            message += "<J>/delete</J> <VP>[playerName]</VP> - <BL> Delete a playerName from database.\n"
            message += "<J>/reload</J> - <BL> Reload all modules.\n"
        return message

    def blockAttack(self):
        reactor.callLater(1.5, self.sendBlockAttack)
        
    def sendBlockAttack(self):
        self.isBlockAttack = True

    def loginPlayer(self, playerName, password, startRoom):
        playerName = "Souris" if playerName == "" else playerName
        if password == "":
            playerName = self.server.checkAlreadyExistingGuest("*" + (playerName[0].isdigit() or str(playerName) > 12 or str(playerName) < 3 or "Souris" if "+" in playerName else playerName))
            startRoom = "\x03[Tutorial] %s" %(playerName)
            self.isGuest = True
            
        if not self.isGuest and playerName in self.server.userPermaBanCache:
            self.sendPacket(Identifiers.old.send.Player_Ban_Login, [self.server.getPermBanInfo(playerName)])
            self.transport.close()
            return

        if not self.isGuest:
            banInfo = self.server.getTempBanInfo(playerName)
            timeCalc = Utils.getHoursDiff(banInfo[1])
            if timeCalc <= 0:
                self.server.removeTempBan(playerName)
            else:
                self.sendPacket(Identifiers.old.send.Player_Ban_Login, [timeCalc, banInfo[0]])
                self.transport.close()
                return

        if self.getConnectedPlayerCount() > self.server.MaximumPlayers:
            self.sendPacket(Identifiers.old.send.Player_Ban_Login, [0, "The server has limit."])
            self.transport.close()

        if self.server.checkConnectedAccount(playerName):
            self.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(1).writeUTF("").writeUTF("").toByteArray())
        else:
            letters, selfs, messages = "", "", ""
            if not self.isGuest and not playerName == "":
                Cursor.execute("select * from Users where Email = %s and Password = %s", [playerName, password])
                players = []
                for rs in Cursor.fetchall():
                    players.append(rs[0])
                if len(players) > 1:
                    i = 0
                    p = ByteArray()
                    while i != len(players):
                        p.writeBytes(players[i]).writeShort(-15708)
                        i += 1
                    self.sendPacket([26, 12], ByteArray().writeByte(11).writeShort(len(p.toByteArray())).writeBytes(p.toByteArray()).writeShort(0).toByteArray())
                else:
                    self.Cursor.execute("select * from Users where "+("Email" if "@" in playerName else "Username")+" = %s and Password = %s", [playerName, password])
                    rs = self.Cursor.fetchone()
                    if rs:
                        playerName = rs[0]
                        self.playerID = rs[2]
                        self.privLevel = rs[3]
                        self.titleNumber = rs[4]
                        self.firstCount = rs[5]
                        self.cheeseCount = rs[6]
                        self.shamanCheeses = rs[7]
                        self.shopCheeses = rs[8]
                        self.shopFraises = rs[9]
                        self.shamanSaves = rs[10]
                        self.hardModeSaves = rs[11]
                        self.divineModeSaves = rs[12]
                        self.bootcampCount = rs[13]
                        self.shamanType = rs[14]
                        self.shopItems = rs[15]
                        self.shamanItems = rs[16]
                        self.clothes = list(map(str, filter(None, rs[17].split("|"))))
                        self.playerLook = rs[18]
                        self.shamanLook = rs[19]
                        self.mouseColor = rs[20]
                        self.shamanColor = rs[21]
                        self.regDate = rs[22]
                        self.shopBadges = eval(rs[23])
                        self.firstTitleList = list(map(float, filter(None, rs[25].split(","))))
                        self.shamanTitleList = list(map(float, filter(None, rs[26].split(","))))
                        self.shopTitleList = list(map(float, filter(None, rs[27].split(","))))
                        self.bootcampTitleList = list(map(float, filter(None, rs[28].split(","))))
                        self.hardModeTitleList = list(map(float, filter(None, rs[29].split(","))))
                        self.divineModeTitleList = list(map(float, filter(None, rs[30].split(","))))
                        self.specialTitleList = list(map(float, filter(None, rs[31].split(","))))
                        self.banHours = rs[32]
                        self.shamanLevel = rs[33]
                        self.shamanExp = rs[34]
                        self.shamanExpNext = rs[35]

                        for skill in list(map(str, filter(None, rs[36].split(";")))):
                            values = skill.split(":")
                            self.playerSkills[int(values[0])] = int(values[1])

                        self.lastOn = rs[37]
                        self.friendsList = rs[38].split(",")
                        self.ignoredsList = rs[39].split(",")
                        self.gender = rs[40]
                        self.lastDivorceTimer = rs[41]
                        self.marriage = rs[42]
                        self.tribeCode = rs[43]
                        self.tribeRank = rs[44]
                        self.tribeJoined = rs[45]
                        selfs = rs[46]
                        message = rs[47]
                        self.visuDone = rs[59].split("|")
                        self.custom = list(map(str, filter(None, rs[60].split(","))))
                        self.survivorStats = list(map(int, rs[48].split(",")))
                        self.racingStats = list(map(int, rs[49].split(",")))
                        
                        for consumable in list(map(str, filter(None, rs[50].split(";")))):
                            values = consumable.split(":")
                            self.playerConsumables[int(values[0])] = int(values[1])

                        self.equipedConsumables = []
                        self.pet = rs[52]
                        self.petEnd = 0 if self.pet == 0 else Utils.getTime() + rs[53]
                        self.shamanBadges = list(map(int, filter(None, rs[54].split(","))))
                        self.equipedShamanBadge = rs[55]
                        self.totem = [rs[57], rs[58].replace("%"[0], chr(1))]
                        self.nowCoins = rs[61]
                        self.nowTokens = rs[62]
                        self.deathStats = list(map(int, rs[63].split(",")))
                        vipTime = rs[64]
                        self.langueStaff = rs[65]
                        self.votemayor, self.candidatar, self.isMayor, self.isPresidente, self.votepresidente, self.addpresidente=map(int, rs[66].split("#"))
                        for counts in list(map(str, filter(None, rs[69].split(";")))):
                            values = counts.split(":")
                            f = []
                            aux = 0
                            for i in xrange(len(values[1])):
                                try:
                                    aux = aux * 10 + int(values[1][i])
                                except:
                                    if aux > 0:
                                        f.append(aux)
                                    aux = 0
                                    pass
                            self.aventureCounts[int(values[0])] = int(f[0]), int(f[1])
                        for points in list(map(str, filter(None, rs[70].split(";")))):
                            values = points.split(":")
                            self.aventurePoints[int(values[0])] = int(values[1])
                        self.aventureSaves = rs[71]
                        self.emailAddress = rs[82]
                        letters = rs[83]
                        self.playerTime = rs[84]
                        self.playerKarma = int(rs[85]) if rs[85] != None else 0
                        self.roles = rs[86]
                        self.loginTime = Utils.getTime()
                    else:
                        reactor.callLater(1, lambda: self.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(2).writeUTF("").writeUTF("").toByteArray()))
                        return

            if "@" not in playerName:
                if self.privLevel == -1:
                    self.sendPacket(Identifiers.old.send.Player_Ban_Login, ["The account has been permanently banned."])
                    self.transport.close()
                    return

                self.server.lastPlayerCode += 1
                self.playerName = playerName
                self.playerCode = self.server.lastPlayerCode

                for name in ["cheese", "first", "shaman", "shop", "bootcamp", "hardmode", "divinemode"]:
                    self.checkAndRebuildTitleList(name)

                self.sendCompleteTitleList()
                self.Shop.checkAndRebuildBadges()
                Cursor.execute("insert into loginlogs values (%s, %s, %s, %s, %s)", [playerName, self.TFMIP(self.ipAddress), Utils.getDate(), self.langue, self.server.miceName])
                loginlog = open("./logs/Logins.log", "a")
                loginlog.write("PlayerName: %s | IP Address: %s | Date: %s | Language: %s | Player Code: %s |.\n" % (playerName, self.ipAddress, Utils.getDate(), self.langue, self.playerCode))
                traceback.print_exc(file=loginlog)
                loginlog.close() 
                self.server.players[self.playerName] = self
                
                for player in self.server.players.values():
                    if "LuaCrew" in player.roles and not player.playerName.startswith('*'):
                        player.isLuaCrew = True
                    if "MapCrew" in player.roles and not player.playerName.startswith('*'):
                        player.isMapCrew = True
                    if "FashionSquad" in player.roles and not player.playerName.startswith('*'):
                        player.isFashionSquad = True
                    if "FunCorp" in player.roles and not player.playerName.startswith('*'):
                        player.isFunCorpPlayer = True
                
                for title in self.titleList:
                    if str(title).split(".")[0] == str(self.titleNumber):
                        self.titleStars = int(str(title).split(".")[1])
                        break
                self.isMute = playerName in self.server.userMuteCache
                #self.server.players[self.playerName] = self
                self.sendPlayerIdentification()
                self.sendLogin()
                self.Shop.sendShamanItems()
                self.sendPacket([60, 4], chr(1))
                self.Skills.sendShamanSkills(False)
                self.Skills.sendExp(self.shamanLevel, self.shamanExp, self.shamanExpNext)
                if self.shamanSaves >= 1500:
                    self.sendShamanType(self.shamanType, (self.shamanSaves >= 1500 and self.hardModeSaves >= 1500))

                self.server.checkPromotionsEnd()
                self.sendTimeStamp()
                self.sendPromotions()

                if self.tribeCode != 0:
                    tribeInfo = self.tribulle.getTribeInfo(self.tribeCode)
                    self.tribeName = tribeInfo[0]
                    self.tribeMessage = tribeInfo[1]
                    self.tribeHouse = tribeInfo[2]
                    self.tribeRanks = tribeInfo[3]
                    self.tribeChat = tribeInfo[4]
                #self.sendPacket([60, 4], chr(1))
                self.tribulle.sendFriendsList(None)
                self.sendPacketTribulle(62, ByteArray().writeUTF(self.langue.lower()).toByteArray())
                self.missions.loadMissions()

                for player in self.server.players.values():
                    if self.playerName and player.playerName in self.friendsList and player.friendsList:
                        player.tribulle.sendFriendConnected(self.playerName)
                     
                if self.tribeCode != 0:
                    self.tribulle.sendTribeMemberConnected()
                self.sendInventoryConsumables()
                self.Shop.checkselfsAndMessages(selfs, messages)
                self.checkLetters(letters)
                self.resSkillsTimer = reactor.callLater(10, setattr, self, "canRedistributeSkills", True)
                self.startBulle(self.server.checkRoom(startRoom, self.langue) if not startRoom == "" and not startRoom == "1" else self.server.recommendRoom(self.langue))
                self.langueStaff = self.langue
                self.sendModInfo(1)
                
    def sendPlayerIdentification(self):
        permsCount = 0
        perms = ByteArray()
        privAuthorization = {0:-1, 1:-1, 2:-1, 3:15, 4:12, 5:13, 6:11, 7:5, 8:5, 9:15} #FC, MC, ARB, MD, ADM
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
        self.sendPacket(Identifiers.send.Player_Identification, data.toByteArray())

    def winBadgeEvent(self, badge):
        if not badge in self.shopBadges:
            self.sendAnimZelda(3, badge)
            try: self.shopBadges[badge] += 1;
            except:self.shopBadges[badge] = 1
            self.Shop.checkAndRebuildBadges()
            self.Shop.sendUnlockedBadge(badge)
            
    def PlayerWinTitle(self, title):
        if not title in self.specialTitleList:
            self.specialTitleList.append(title + 0.1)
            self.sendUnlockedTitle(title, 1)
            self.sendCompleteTitleList()
            self.sendTitleList()


    def sendStaffCM(self, byte, username, message, all=True):
        if all:
            for client in self.server.players.values():
                if client.privLevel >= 2:
                    client.sendPacket([6, 10], ByteArray().writeByte(byte).writeUTF(username).writeUTF(message).writeShort(0).writeShort(0).toByteArray())
        else:
            self.sendPacket([6, 10], ByteArray().writeByte(byte).writeUTF(username).writeUTF(message).writeShort(0).writeShort(0).toByteArray())

    def sendAllModerationChat(self, type, message):
        if type == 3 or type == 4: # Modo commands. 
            self.ModoCommands.parseCommand(message)
            self.server.sendStaffChat(type, self.langue, Identifiers.send.Staff_Chat, ByteArray().writeByte(type).writeUTF(self.playerName).writeUTF(message).writeShort(0).writeShort(0).toByteArray())
        else:
            self.server.sendStaffChat(type, self.langue, Identifiers.send.Staff_Chat, ByteArray().writeByte(1 if type == -1 else type).writeUTF(self.playerName).writeUTF(message).writeShort(0).writeShort(0).toByteArray())

    def TotalPlayersCommunity(self, lang):
        cnt = 0
        for player in self.server.players.values():
            if player.langue.upper() == lang:
                cnt += 1
        return cnt

    def TotalPlayersPingCommunity(self, lang):
        cnt = 0
        for player in self.server.players.values():
            if player.langue.upper() == lang:
                cnt += player.PInfo[2]
        return cnt

    def sendTotalRec(self):
        if self.room.isSpeedRace:
            if self.privLevel != 0:
                totalrecs = 0
                CursorMaps.execute("select * from Maps where Player = ?", [self.playerName])
                for rs in CursorMaps.fetchall():
                    totalrecs += 1
                try: self.sendMessage("<bl>Total records</font><BV>:</BV> <font color='#9a9a9a'>%s</font>" %(totalrecs))
                except: self.sendMessage("<R>So much records.</R>") 

    def sendListRec(self):
        if self.room.isSpeedRace:
            if self.privLevel != 0:
                    no = 0
            recordList = "<p align='center'><VP>"+self.playerName+"'s Record (List)</VP></p>\n"
            CursorMaps.execute("select * from Maps where Player = ?", [self.playerName])
            for rs in CursorMaps.fetchall():
                bestsecond = rs["Time"]
                code = rs["Code"]
                date = rs["RecDate"] 
                second = bestsecond * 0.01
                no += 1
                recordList += "<p align='left'><font color='#9a9a9a'>"+str(no)+"-)</font> <font color='#f17e7e'>(@%s)</font> - <font color='#f17e7e'>(%ss)</font> - <font color='#f17e7e'>(%s)</font>\n" %(code,second,str(datetime.fromtimestamp(float(int(date)))))
            try: self.sendLogMessage(recordList)
            except: self.sendMessage("Problem for admin with contact")

    def sendLeaderBoard(self):
        if self.room.isSpeedRace:
                sx,sy = 800,400
                pg,pu = 410,340
                x,y = (sx-pg)/2,(sy-pu)/2
                ly = y+48
                
                addText = self.room.addTextArea
                isim = self.playerName
                self.lbsayfa,sinir = 1,10
                self.records = sorted(self.server.fastRacingRecords["sequentialrecords"],key=lambda x: x[1],reverse=True)
                if len(self.records) < 10: sinir=len(self.records)
                self.sayfasayi = int(math.ceil(len(self.records)/10.0))
                if self.sayfasayi < 1: self.sayfasayi = 1
                
                addText(5000, "<p align='center'><font color='#ffc15e'><b>LEADER BOARD</b></font></p>", isim, x,y, pg,pu, 0x111111, 0x111111, 90, False)
                addText(5001, "" , isim, x+20, y+20, pg-40, 15, 0x111111, 0xFFFFFF, 10, False)
                addText(5002, "<p align='center'><font color='#ffc15e'>Player</font></p>" , isim, x-80, y+20, pg-40, 40, 0x111111, 0xFFFFFF, 0, False)
                addText(5003, "<p align='center'><font color='#ffc15e'>Record</font></p>" , isim, x+80, y+20, pg, 40, 0x111111, 0x000000, 0, False)
                addText(5035, "<p align='center'><a href='event:lbgeri'><font color='#ffc15e'>«</a> 1 / "+str(self.sayfasayi)+" <a href='event:lbileri'><b>»</b></font></a>" , isim, x, pu+10, pg, 40, 0x324650, 0x000000, 0, False)	
                addText(5036, "<a href='event:lbkapat'><font color='#ffc15e'>X</font></a>" , isim, (x+pg)-11, y, 12, 15, 0x111111, 0x111111, 100, False)	
                
                i,bos = 0," "*16
                for sira in range(sinir):
                    i+=1
                    t = self.records[sira]
                    recisim,rec = t[0],t[1]
                    addText(5003+i, bos+"<font color='#ffc15e'><b>"+str(recisim)+"</font></b>", isim, x+20, ly+(27*(i-1)), (pg-40)/2-10, 18, 0xFFFFFF, 0x000000, 30, False)
                    addText((5013+i), "<p align='center'><font color='#ffc15e'>"+str(rec)+"</font></p>" , isim,  x+((pg/2)), ly+(27*(i-1)), (pg-40)/2, 18, 0xFFFFFF, 0x000000, 30, False)
                    addText((5024+i), "<font color='#ffc15e'><b>"+str(i)+"</font></b>", isim, x+20, ly+(27*(i-1)), (pg-40)/2-10, 18, 0xFFFFFF, 0x000000, 0, False)
                
    def lbSayfaDegis(self,ileri,kapat=False):
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

    def discoColors(self):
        colors = ["000000", "FF0000", "17B700", "F2FF00", "FFB900", "00C0D9", "F600A8", "850000", "62532B", "EFEAE1", "201E1C"]
        sColor = random.choice(colors)                
        data = struct.pack("!i", self.playerCode)
        data += struct.pack("!i", int(sColor, 16))
        self.room.sendAll([29, 4], data)
        self.discoReady()

    def sendTitleMessage(self, message):
        for client in self.room.clients.values():
            info = struct.pack('!h', len(message)) + message + '\n'
            client.room.sendPacket([29, 25], info)    

    def discoMessage(self):
        self.sendMessage("<font color='#E9A144'>Disco time begins to entertaining namecolor.</font>")

    def discoReady(self):
        reactor.callLater(4, self.discoColors)
            
    def getConnectedPlayerCount(self):
        return len(self.server.players)

    def updateDatabase(self):
        if not self.isGuest:
            Cursor.execute("update Users set PrivLevel = %s, TitleNumber = %s, FirstCount = %s, CheeseCount = %s, ShamanCheeses = %s, ShopCheeses = %s, ShopFraises = %s, ShamanSaves = %s, HardModeSaves = %s, DivineModeSaves = %s, BootcampCount = %s, ShamanType = %s, ShopItems = %s, ShamanItems = %s, Clothes = %s, Look = %s, ShamanLook = %s, mouseColor = %s, shamanColor = %s, RegDate = %s, Badges = %s, CheeseTitleList = %s, FirstTitleList = %s, ShamanTitleList = %s, ShopTitleList = %s, BootcampTitleList = %s, HardModeTitleList = %s, DivineModeTitleList = %s, SpecialTitleList = %s, BanHours = %s, ShamanLevel = %s, ShamanExp = %s, ShamanExpNext = %s, Skills = %s, LastOn = %s, FriendsList = %s, IgnoredsList = %s, Gender = %s, LastDivorceTimer = %s, Marriage = %s, TribeCode = %s, TribeRank = %s, TribeJoined = %s, SurvivorStats = %s, RacingStats = %s, Consumables = %s, EquipedConsumables = %s, Pet = %s, PetEnd = %s, ShamanBadges = %s, EquipedShamanBadge = %s, VisuDone = %s, CustomItems = %s, Coins = %s, Tokens = %s, DeathStats = %s, Langue = %s, Mayor = %s, AventureCounts = %s, AventurePoints = %s, SavesAventure = %s, Time = %s, Karma = %s, user_line_status = 1  where Username = %s", [self.privLevel, self.titleNumber, self.firstCount, self.cheeseCount, self.shamanCheeses, self.shopCheeses, self.shopFraises, self.shamanSaves, self.hardModeSaves, self.divineModeSaves, self.bootcampCount, self.shamanType, self.shopItems, self.shamanItems, "|".join(map(str, self.clothes)), self.playerLook, self.shamanLook, self.mouseColor, self.shamanColor, self.regDate, str(self.shopBadges), ",".join(map(str, self.cheeseTitleList)), ",".join(map(str, self.firstTitleList)), ",".join(map(str, self.shamanTitleList)), ",".join(map(str, self.shopTitleList)), ",".join(map(str, self.bootcampTitleList)), ",".join(map(str, self.hardModeTitleList)), ",".join(map(str, self.divineModeTitleList)), ",".join(map(str, self.specialTitleList)), self.banHours, self.shamanLevel, self.shamanExp, self.shamanExpNext, ";".join(map(lambda skill: "%s:%s" %(skill[0], skill[1]), self.playerSkills.items())), self.tribulle.getTime(), ",".join(map(str, filter(None, self.friendsList))), ",".join(map(str, filter(None, self.ignoredsList))), self.gender, self.lastDivorceTimer, self.marriage, self.tribeCode, self.tribeRank, self.tribeJoined, ",".join(map(str, self.survivorStats)), ",".join(map(str, self.racingStats)), ";".join(map(lambda consumable: "%s:%s" %(consumable[0], 250 if consumable[1] > 250 else consumable[1]), self.playerConsumables.items())), ",".join(map(str, self.equipedConsumables)), self.pet, abs(Utils.getSecondsDiff(self.petEnd)), ",".join(map(str, self.shamanBadges)), self.equipedShamanBadge, "|".join(map(str, self.visuDone)), ",".join(map(str, self.custom)), self.nowCoins, self.nowTokens, ",".join(map(str, self.deathStats)), self.langueStaff, "#".join([str(self.votemayor), str(self.candidatar), str(self.isMayor), str(self.isPresidente), str(self.votepresidente), str(self.addpresidente)]), ";".join(map(lambda aventure: "%s:%s" %(aventure[0], aventure[1]), self.aventureCounts.items())), ";".join(map(lambda points: "%s:%s" %(points[0], points[1]), self.aventurePoints.items())), self.aventureSaves, (self.playerTime+Utils.getSecondsDiff(self.loginTime)), self.playerKarma, self.playerName])

    def startBulle(self, roomName):
        #self.sendBulle()
        reactor.callLater(0.4, lambda: self.enterRoom(roomName))

    def enterRoom(self, roomName):
        if self.isTrade:
            self.cancelTrade(self.tradeName)
        roomName = roomName.replace("<", "&lt;")
        if not roomName.startswith("*") and not (len(roomName) > 3 and roomName[2] == "-" and self.privLevel >= 7):
            roomName = "%s-%s" %(self.langue, roomName)
            
        for rooms in ["\x03[Editeur] ", "\x03[Totem] ", "\x03[Tutorial] "]:
            if roomName.startswith(rooms) and not self.playerName == roomName.split(" ")[1]:
                roomName = "%s-%s" %(self.langue, self.playerName)

        player = self.server.players.get(self.playerName)
        if player != None:
            r1 = player.isPrisoned
            
        if self.room != None:
            self.room.removeClient(self)

        self.roomName = roomName
        self.sendGameType(11 if "music" in roomName else 4, 0)
        try:
            if r1 == False:
                self.sendEnterRoom(roomName)
                self.server.addClientToRoom(self, roomName)
                self.sendPacket(Identifiers.old.send.Anchors, self.room.anchors)
                self.sendPacket([29, 1], "")
        except UnboundLocalError:
            pass

        for player in self.server.players.values(): 
            if self.playerName and player.playerName in self.friendsList and player.friendsList:
                player.tribulle.sendFriendChangedRoom(self.playerName, self.langueID)
            
        if self.tribeCode != 0:
            self.tribulle.sendTribeMemberChangeRoom()

        if self.room.isMusic and self.room.isPlayingMusic:
            self.sendMusicVideo(False)

        if self.room.isTribeHouse and self.room.isPlayingMusic:
            self.sendMusicdeo(False)

#        if not self.room.isTotemEditor and not self.room.isEditor and not self.room.isRacing and not self.room.isBootcamp and not self.room.isSurvivor and not self.room.isVillage and not self.room.isDefilante:

        if roomName.startswith(self.langue + "-" + "music") or roomName.startswith(self.langue + "-" + "*music"):
            self.canSkipMusic = False
            if self.skipMusicTimer != None:
                self.skipMusicTimer.cancel()
            self.skipMusicTimer = reactor.callLater(15, setattr, self, "canSkipMusic", True)

        if self.room.isDeathmatch:
            self.room.bindKeyBoard(self.playerName, 3, False, self.room.isDeathmatch)
            self.room.bindKeyBoard(self.playerName, 32, False, self.room.isDeathmatch)
            self.room.bindKeyBoard(self.playerName, 79, False, self.room.isDeathmatch)
            self.room.bindKeyBoard(self.playerName, 80, False, self.room.isDeathmatch)
            self.sendMessage("<CH><ROSE>#deathmatch <CH>welcome to your module.", True)
            self.sendMessage("<V><ROSE>Down ↓<V>or <ROSE>SPACE <V>you can throw the cannon by pressing the key.", True)
            self.sendMessage("<V><ROSE>'P'<V> Press the key to profile, <ROSE>'O' <V>you can look at the inventory by pressing.", True)
            self.sendMessage("<V><ROSE>#Deathmatch<V> in the room to play for, <ROSE>3 <V>room need player.", True)
            self.sendMessage("<V><ROSE>#Deathmatch<ROSE> ranking showing for <V>/ds <ROSE>write.", True)

        if self.room.isFFARace:
            self.room.bindKeyBoard(self.playerName, 3, False, self.room.isFFARace)
            self.room.bindKeyBoard(self.playerName, 32, False, self.room.isFFARace)
            self.canCannon = True
            self.sendMessage("<N>Welcome to <J>#ffarace")
            self.sendMessage("<N>Press <R>down <N>or <R>space <N>to launch cannons.")
            self.sendMessage("<N>Try to be the <R><b>first</b> <N>and the <R><b>survivor</b> <N>!")
            self.sendMessage("<font color='#E56CA3'>Welcome to fastracing</font>\n<font color='#e6b31e'>Leaderboard '!lb'</font>")#\n<font color='#e6b31e'>Kırılan kayıtlarınız '!lsrec'</font>") 
        if self.room.isSpeedRace:
            self.sendMessage("<V>[#]</V> <V>Welcome to</V> <BL>Fastracing</BL>.\n<V>[#]</V> <V>To view the</V> <V>leaderboard,</V> <v>type</v> '<BL>!lb</BL>'\n<V>[#]</V> '<BL>!listrec</BL>' <V>&</V> '<BL>!lsrec</BL>' <V>to learn more about your broken records.</V>")
    
        if self.room.isFlyMod:
            self.room.bindKeyBoard(self.playerName, 32, False, self.room.isFly)
            self.sendLangueMessage("", "<V>Press space on the keyboard to use the flights.")
            
        if self.room.isFuncorp:
            self.sendLangueMessage("", "<FC>$FunCorpActive</FC>")
        else:
            player = self.server.players.get(self.playerName)
            if player != None:
                player.mouseName = player.playerName
                self.room.funcorpNames[player.playerName] = player.playerName

        if self.followed != None:
            if self.followed.isHidden == False:
                self.followed = None
            else:
                #self.followed.sendMessage(f"<ROSE>[Follow]</ROSE> Moving to room [{self.roomName}]")
                self.followed.startBulle(self.roomName)
                self.followed.sendPacket(Identifiers.send.Watch, ByteArray().writeUTF(self.playerName).writeBoolean(True).toByteArray())
        
        if self.playerName in self.server.reportedUsers and self.followed == None:
            self.sendmodServerMessage(f"<ROSE>[Modopwet]</ROSE> The player <BV>{self.playerName}</BV> (<N>{self.modoPwet.getReportType(self.playerName)}</N>) left the room [{self.lastroom}] and went to the room [{self.roomName}] (<a href='event:modopwetfollow#{self.playerName}'><FC>Follow</FC></a>).")
            
        self.lastroom = self.roomName
            
    def resetPlay(self):
        self.iceCount = 2
        self.bubblesCount = 0
        self.currentPlace = 0
        self.ambulanceCount = 0
        self.defilantePoints = 0
        self.bootcampRounds = 0
        self.artefactID = 0
        
        self.isAfk = True
        self.isDead = False
        self.useTotem = False
        self.hasEnter = False
        self.isShaman = False
        self.isVampire = False
        self.hasCheese = False
        self.isSuspect = False
        self.hasBolo = False
        self.hasBolo2 = False
        self.canRespawn = False
        self.selfGet = False
        self.isNewPlayer = False
        self.isOpportunist = False
        self.desintegration = False
        self.canShamanRespawn = False
        self.canKiss = True
        self.hasArtefact = False
        self.room.isFly = False

        self.a = []
        self.i = []
        self.s = []
        
    def sendAccountTime(self):
        eventTime = 1
        date = datetime.now() + timedelta(hours=int(eventTime))
        timetuple = date.timetuple()
        eventTime_ = int(str(thetime.mktime(timetuple)).split(".")[0])
        self.Cursor.execute('select IP from Account where IP = %s', [self.ipAddress])
        rrf = self.Cursor.fetchone()
        if rrf is None:
           self.Cursor.execute('insert into Account values (%s, %s)', [self.ipAddress, eventTime_])
        else:
           self.Cursor.execute('update Account set Time = %s where IP = %s', [eventTime_, self.ipAddress])

    def checkTimeAccount(self):
        #return
#        self.Cursor.execute('SELECT Time FROM Account WHERE IP = %s', [self.ipAddress])
        rrf = self.Cursor.fetchone()
        if rrf is None:
            return True
        else:
            if (int(str(thetime.time()).split(".")[0]) >= int(rrf[0])):
                return True
            else:
                return False

    def startFrogEvent(self):
        self.sendPacket([5, 51], "\t\x00,\x07\x00i\x07\xb2")
        self.sendPacket([5, 51], "\t\x00-\x07\x00\xc3\x07\xb2")
        self.sendPacket([5, 51], "\t\x00.\x07\x00\xcd\x07\xb2")
        self.sendPacket([5, 51], "\t\x00/\x08\x011\x07\xb2")
        self.sendPacket([5, 51], "\t\x000\x08\x01\x8b\x07\xb2")
        self.sendPacket([5, 51], "\t\x001\x08\x01\x90\x07\xc1")
        self.sendPacket([5, 51], "\t\x002\x08\x01\x95\x07\xb2")
        self.sendPacket([5, 51], "\t\x003\x08\x01\xf9\x07\xb2")
        self.sendPacket([5, 51], "\t\x004\x07\x02S\x07\xb2")
        self.sendPacket([5, 51], "\t\x005\x07\x02]\x07\xb2")
        self.sendPacket([5, 51], "\t\x006\x07\x02\xc1\x07\xb2")
        reactor.callLater(13, self.travarRatos)

    def travarRatos(self):
        self.room.sendAll([100, 66], "\x01")

    def enableKey(self, key, onKeyPress = True, onKeyLeave = True):
        if not self.isDead:
            self.sendPacket([29, 2], struct.pack('!hbb', int(key), onKeyPress, onKeyLeave))

    def disableKey(self, key, onKeyPress = False, onKeyLeave = False):
        self.sendPacket([29, 2], struct.pack('!hbb', int(key), onKeyPress, onKeyLeave))

    def sendSaintConsumables(self):
        id = 2236
        if not id in self.playerConsumables:
            self.playerConsumables[id] = 50
        else:
            count = self.playerConsumables[id] + 50
            self.playerConsumables[id] = count
            self.sendAnimZeldaInventory(4, id, 50)

    def sendSaintBadge(self):
        self.sendAnimZelda(3, 132)
        self.Shop.sendUnlockedBadge(132)
        try: self.shopBadges[132] += 1
        except: self.shopBadges[132] = 1


    def sendSaintMessage(self):
        self.sendMessage("<font color='#EA489E'>[Master Valentine] Happy Valentine's Day ^^</font>")

    def sendSaintTitle(self):
        self.specialTitleList.append(649.1)
        self.sendUnlockedTitle(649, 1)
        self.sendCompleteTitleList()
        self.sendTitleList()

    def sendSaintEvent(self):
        self.sendSaintMessage()
        reactor.callLater(40, self.sendSaintTitle)
        reactor.callLater(60, self.sendSaintBadge)
        reactor.callLater(80, self.sendSaintConsumables)


    
    def startPlay(self):
        self.playerStartTimeMillis = self.room.gameStartTimeMillis
        self.isNewPlayer = self.isDead
        self.sendMap(newMapCustom=True) if self.room.mapCode != -1 else self.sendMap() if self.room.isEditor and self.room.EMapCode != 0 else self.sendMap(True)

        if self.room.mapCode == 2809 or self.room.mapCode == 2810:
            self.sendPacket([8, 30], ByteArray().writeInt(-20).writeUTF("Fish Man").writeShort(563).writeBoolean(True).writeUTF("7;0,6,0,34_004BA2,0,53_006C87+396278+000000,33_007294+007294+000000,0,0,0,0").writeShort(2145).writeShort(635).writeShort(1).writeByte(11).writeShort(0).toByteArray())
            
        if self.room.porno:
            self.room.sendAll(Identifiers.old.send.Music, ["https://youtu.be/ALZHF5UqnU4"])
            

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
            self.Skills.getkills()

        if self.room.currentShamanName != "" and not self.room.noShamanSkills:
            self.Skills.getPlayerSkills(self.room.currentShamanSkills)

        if self.room.currentSecondShamanName != "" and not self.room.noShamanSkills:
            self.Skills.getPlayerSkills(self.room.currentSecondShamanSkills)

        self.sendPlayerList()
        if self.room.catchTheCheeseMap and not self.room.noShamanSkills:
            self.sendPacket(Identifiers.old.send.Catch_The_Cheese_Map, [shamanCode])
            self.sendPacket(Identifiers.send.Player_Get_Cheese, ByteArray().writeInt(shamanCode).writeBoolean(True).toByteArray())
            if not self.room.currentMap in [108, 109]:
                self.sendShamanCode(shamanCode, shamanCode2)
        else:
            self.sendShamanCode(shamanCode, shamanCode2)

        self.sendSync(self.room.getSyncCode())
        self.sendRoundTime(self.room.roundTime + (self.room.gameStartTime - Utils.getTime()) + self.room.addTime)
        self.sendMapStartTimer(False) if self.isDead or self.room.isTutorial or self.room.isTotemEditor or self.room.isBootcamp or self.room.isDefilante or self.room.getPlayerCountUnique() < 2 else self.sendMapStartTimer(True)

        if self.room.isTotemEditor:
            self.initTotemEditor()

            
        if self.room.mapCode == 2811:
            self.sendPacket([8, 30], ByteArray().writeInt(-20).writeUTF("Gwen").writeShort(116).writeBoolean(True).writeUTF("122;174_FFB0AF+FFBCBB+FFC3C2,0,0,66_FFC3C2,0,3_D49F9E,0,9_F6A1A0+F1BDA9+FFD0DA,10_FFC9C8+FFD2D2+FF6461+FFC6C5,0,0").writeShort(600).writeShort(359).writeShort(1).writeByte(11).writeShort(0).toByteArray())
            self.sendSaintEvent()
            

       
    
##        if self.room.isSpeedRace:
##            self.sendPacket([29, 25], struct.pack('!h', len('<font color="#E2E05A">Fastracing')) + '<font color="#E2E05A">Fastracing')

        if self.useAnime >= 1:
            self.useAnime = 0

        if self.room.isMeepRace:
            self.sendPacket(Identifiers.send.Can_Meep, 1)

        if self.room.isMulodrome:
            if not self.playerName in self.room.redTeam and not self.playerName in self.room.blueTeam:
                if not self.isDead:
                    self.isDead = True
                    self.sendPlayerDied()

        if self.room.isSurvivor and self.isShaman:
            self.sendPacket(Identifiers.send.Can_Meep, 1)

        if self.room.isOldSurvivor and self.isShaman:
            self.sendPacket(Identifiers.send.Can_Meep, 0)

        self.isEvent = True
        self.room.bindKeyBoard(self.playerName, 32, False, self.isEvent)

        self.isPositioncmd = True
        self.room.bindKeyBoard(self.playerName, 78, False, self.isPositioncmd)
        
        if self.room.mapCode == 2809 or self.room.mapCode == 2810:
            self.sendLangueMessage("", "<font color='#95CAD9'>[Fish Man] Go to <ROSE>water</ROSE> <font color='#95CAD9'>parts and press space key.")

        if self.room.currentMap in range(200, 211) and not self.isShaman:
            self.sendPacket(Identifiers.send.Can_Transformation, 1)

        if self.room.isVillage:
            reactor.callLater(0.1, self.sendBotsVillage)

        elif self.room.isFFARace:
            reactor.callLater(1.3, self.enableSpawnCN)


    def sendFishingCount(self):
        self.sendPlayerEmote(14, "", False, False)
        item = ["30", "1", "5", "21", "22", "23", "24", "25", "28", "32", "33", "407", "35", "2349", "2252", "2240", "2247", "14", "15", "16", "20", "2", "3", "4", "6", "8", "800", "29", "2234", "2246", "2256", "2330", "11", "31", "34", "26", "2305", "2447", "2273", "2295", "2306", "2375", "1511", "800", "801", "2247", "2253", "2254",]
        id = random.choice(item)
        if not id in self.playerConsumables:
            self.playerConsumables[id] = 7
        else:
            count = self.playerConsumables[id] + 7
            self.playerConsumables[id] = count
        self.sendAnimZeldaInventoryx(4, id, 7)    
        id2 = 2305
        if not id2 in self.playerConsumables:
            self.playerConsumables[id2] = 3
        else:
            count = self.playerConsumables[id2] + 3
            self.playerConsumables[id2] = count
        self.sendAnimZeldaInventoryx(4, id2, 3)

    def sendBotsVillage(self):
        self.sendPacket([8, 30], "\xff\xff\xff\xff\x00\x06Oracle\x01+\x01\x00*61;0,0,0,0,0,19_3d100f+1fa896+ffe15b,0,0,0\x08\x8b\x01}\x00\x01\x0b\x00\x00")
        self.sendPacket([8, 30], "\xff\xff\xff\xfe\x00\x08Papaille\x01*\x01\x00\x134;2,0,2,2,0,0,0,0,1\tZ\x00\xd1\x00\x01\x0b\x00\x00")
        self.sendPacket([8, 30], "\xff\xff\xff\xfd\x00\x05Elise\x01]\x01\x00\x143;10,0,1,0,1,0,0,1,0\t\x19\x00\xd1\x01\x01\x0b\x00\x00")
        self.sendPacket([8, 30], "\xff\xff\xff\xfc\x00\x05Buffy\x01[\x01\x00\x06$Buffy\x07t\x01\xf3\x00\x01\x0b\x00\x00")
        self.sendPacket([8, 30], "\xff\xff\xff\xfb\x00\rIndiana Mouse\x01(\x00\x00\x1445;0,0,0,0,0,0,0,0,0\x00\xae\x02\xca\x00\x01\x0b\x00\x00")
        self.sendPacket([8, 30], "\xff\xff\xff\xfa\x00\x04Prof\x01G\x00\x00\n$Proviseur\x01!\x02\xcb\x00\x01\x0b\x00\x00")
        self.sendPacket([8, 30], "\xff\xff\xff\xf9\x00\x07Cassidy\x01\x18\x00\x00\x07$Barman\n\xd2\x02%\x00\x01\x0b\x00\x00")
        self.sendPacket([8, 30], "\xff\xff\xff\xf8\x00\x0fVon Drkkemouse\x01\x1f\x00\x00\n$Halloween\x06\x88\x01z\x00\x01\x0b\x00\x00")
       ## self.sendPacket([8, 30], ByteArray().writeInt(-20).writeUTF("Title man").writeShort(1).writeBoolean(True).writeUTF("113;173,5,0,63,38,0,29,0,0,0,0").writeShort(1574).writeShort(643).writeShort(1).writeByte(11).writeShort(0).toByteArray())
        self.sendPacket([8, 30], ByteArray().writeInt(-20).writeUTF("Scofield").writeShort(1).writeBoolean(True).writeUTF("13;89_54593B+C98307,0,0,4_676877+78583B,0,0,0,0,0,0,0").writeShort(2166).writeShort(749).writeShort(1).writeByte(11).writeShort(0).toByteArray())
        self.sendPacket([8, 30], ByteArray().writeInt(-20).writeUTF("Tigeress").writeShort(1).writeBoolean(True).writeUTF("21;151_D39F63+000000+D39F63+D39F63,0,0,0,0,37,0,0,0,0,0").writeShort(1700).writeShort(520).writeShort(1).writeByte(11).writeShort(0).toByteArray())
      ##  self.sendPacket([8, 30], ByteArray().writeInt(-20).writeUTF("Teddi").writeShort(1).writeBoolean(True).writeUTF("117;172,24,0,0,0,0,0,0,0,0,0").writeShort(2214).writeShort(112).writeShort(1).writeByte(11).writeShort(0).toByteArray())
      ##  self.sendPacket([8, 30], ByteArray().writeInt(-20).writeUTF("Father").writeShort(1).writeBoolean(True).writeUTF("13;6_FFFFFF+000000,28,0,0,3,0,0,0,0,0,0").writeShort(2400).writeShort(102).writeShort(1).writeByte(11).writeShort(0).toByteArray())
        self.sendPacket([8, 30], ByteArray().writeInt(-20).writeUTF("Mother").writeShort(1).writeBoolean(True).writeUTF("65;161,0,35,50,0,0,0,0,0,0,0").writeShort(1027).writeShort(682).writeShort(1).writeByte(11).writeShort(0).toByteArray())
        self.sendPacket([8, 30], ByteArray().writeInt(-20).writeUTF("Pets Man").writeShort(1).writeBoolean(True).writeUTF("128;150,0,0,0,0,4_FFFFFF,0,0,0,0,0").writeShort(1674).writeShort(373).writeShort(1).writeByte(11).writeShort(0).toByteArray())
        self.sendPacket([8, 30], ByteArray().writeInt(-20).writeUTF("Not Scofield").writeShort(1).writeBoolean(True).writeUTF("13;89_54593B+C98307,0,0,4_676877+78583B,0,0,0,0,0,0,0").writeShort(1737).writeShort(751).writeShort(1).writeByte(11).writeShort(0).toByteArray())

    def sendNPC(self, id, id2, name, title, look, px, py, mode, end):
        self.sendPacket([8, 30], ByteArray().writeShort(id).writeShort(id2).writeUTF(name).writeShort(title).writeByte(0).writeUTF(look).writeShort(px).writeShort(py).writeShort(mode).writeByte(5).writeShort(end).toByteArray()) 

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
        data.writeUTF("71;0,0,0,0,0,0,0,0,0,0,0" if self.room.isBootcamp else (self.fur if self.fur != "" else self.playerLook))
        data.writeBoolean(False)
        data.writeInt(int(self.tempMouseColor if not self.tempMouseColor == "" else self.mouseColor, 16))
        data.writeInt(int(self.shamanColor, 16))
        data.writeInt(0)
        try:data.writeInt(int(self.nickColor.lower() if self.nickColor != "" else "#95d9d6", 16))
        except:data.writeInt(-1)
        return data.toByteArray()


    def sendShamanCode(self, shamanCode, shamanCode2):
        self.sendShaman(shamanCode, shamanCode2, self.server.getShamanType(shamanCode), self.server.getShamanType(shamanCode2), self.server.getShamanLevel(shamanCode), self.server.getShamanLevel(shamanCode2), self.server.getShamanBadge(shamanCode), self.server.getShamanBadge(shamanCode2))

    def sendCorrectVersion(self, lang='en'):
        self.sendPacket(Identifiers.send.Correct_Version, ByteArray().writeInt(self.getConnectedPlayerCount()).writeUTF('').writeUTF(lang).writeUTF('').writeInt(self.authKey).writeBoolean(False).toByteArray())
        self.sendPacket(Identifiers.send.Banner_Login, ByteArray().writeByte(1).writeByte(self.server.adventureID).writeByte(1).writeBoolean(False).toByteArray())
        self.sendPacket(Identifiers.send.Image_Login, ByteArray().writeUTF(self.server.adventureIMG).toByteArray())
        self.awakeTimer = reactor.callLater(999999, self.transport.close)

    def sendLogin(self):
        self.sendPacket(Identifiers.old.send.Login, [self.playerName, self.playerCode, self.privLevel, 30, 1 if self.isGuest else 0, 0, 0, 0])
        if self.isGuest:
            self.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(1).writeByte(10).toByteArray())
            self.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(2).writeByte(5).toByteArray())
            self.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(3).writeByte(15).toByteArray())
            self.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(4).writeByte(200).toByteArray())

    def sendTimeStamp(self):
        self.sendPacket(Identifiers.send.Time_Stamp, ByteArray().writeInt(Utils.getTime()).toByteArray())

    def enableSpawnCN(self):
        self.canSpawnCN = True

    def getCrazzyPacket(self,type,info): 
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

    def sendPromotions(self):
        for promotion in []:
            self.sendPacket(Identifiers.send.Promotion, ByteArray().writeBoolean(False).writeBoolean(True).writeInt(promotion[0] * (10000 if promotion[1] > 99 else 100) + promotion[1] + (10000 if promotion[1] > 99 else 0)).writeBoolean(True).writeInt(promotion[2]).writeByte(0).toByteArray())

    def sendGameType(self, gameType, serverType):
        self.sendPacket(Identifiers.send.Room_Type, gameType)
        self.sendPacket(Identifiers.send.Room_Server, serverType)

    def sendEnterRoom(self, roomName):
        found = False
        rooms = roomName[3:]
        count = "".join(i for i in rooms if i.isdigit())
        for room in ["vanilla", "survivor", "racing", "music", "bootcamp", "defilante", "village", "#deathmatch"]:
            if rooms.startswith(room) and not count == "" or rooms.isdigit():
                found = not (int(count) < 1 or int(count) > 1000000000 or rooms == room)
                
        self.sendPacket(Identifiers.send.Enter_Room, ByteArray().writeBoolean(found).writeUTF(roomName).toByteArray())

    def sendMap(self, newMap=False, newMapCustom=False):
        xml = b"" if newMap else self.room.mapXML if newMapCustom else self.room.EMapXML
        try:
            xml = zlib.compress(xml)
        except:
            xml = zlib.compress(xml.encode())
        self.sendPacket(Identifiers.send.New_Map, ByteArray().writeInt(self.room.currentMap if newMap else self.room.mapCode if newMapCustom else -1).writeShort(self.room.getPlayerCount()).writeByte(self.room.lastRoundCode).writeShort(0).writeUTF(xml).writeUTF("" if newMap else self.room.mapName if newMapCustom else "-").writeByte(0 if newMap else self.room.mapPerma if newMapCustom else 100).writeBoolean(self.room.mapInverted if newMapCustom else False).toByteArray())

    def sendPlayerList(self):
        players = self.room.getPlayerList()
        data = ByteArray().writeShort(len(players))
        for player in players:
            data.writeBytes(player)
        
        self.sendPacket([144, 1], data.toByteArray())

    def sendSync(self, playerCode):
        self.sendPacket(Identifiers.old.send.Sync, [playerCode, ""] if (self.room.mapCode != 1 or self.room.EMapCode != 0) else [playerCode])

    def sendRoundTime(self, time):
        self.sendPacket(Identifiers.send.Round_Time, ByteArray().writeShort(0 if time < 0 or time > 32767 else time).toByteArray())

    def sendMapStartTimer(self, startMap):
        self.sendPacket(Identifiers.send.Map_Start_Timer, ByteArray().writeBoolean(startMap).toByteArray())

    def sendPlayerDisconnect(self):
        self.room.sendAll(Identifiers.old.send.Player_Disconnect, [self.playerCode])

    def sendChangeMap(self, time):
       self.room.sendAll([5, 22], ByteArray().writeShort(time).toByteArray())
       if self.room.changeMapTimer:
               try:
                       self.room.changeMapTimer.cancel()
               except:
                       self.room.changeMapTimer=None
       self.room.changeMapTimer = reactor.callLater(time, self.room.mapChange)

    def getPing(self, ip):
        ping = os.popen("ping -n 1 %s"%(ip)).readlines()[-1]
        ping = str(ping.split("= ")[-1]).strip().replace('ms', '')
        return ping

    def sendPlayerDied(self):
        self.room.sendAll(Identifiers.old.send.Player_Died, [self.playerCode, self.playerScore])
        self.hasCheese = False

        if self.room.getAliveCount() < 1 or self.room.catchTheCheeseMap or self.isAfk:
            self.canShamanRespawn = False

        if ((self.room.checkIfTooFewRemaining() and not self.canShamanRespawn) or (self.room.checkIfShamanIsDead() and not self.canShamanRespawn) or (self.room.checkIfDoubleShamansAreDead())):
            self.room.send20SecRemainingTimer()
         
        if self.room.isDeathmatch:
            if self.room.checkIfDeathMouse():
                if self.room.getPlayerCount() >= 4:
                   self.sendChangeMap(5)
                for client in self.room.clients.values():
                     if not client.isDead:
                         #client.firstCount += 1
                         self.Cursor.execute("update users set deathCount = deathCount + 1 where Username = %s", [client.playerName])
                         client.cheeseCount += 1

        if self.room.isRacing:
            self.racingRounds = 0
        if self.room.isDefilante:
            self.defilanteRounds = 0
        if self.room.isSpeedRace:
            self.fastracingRounds = 0
        if self.room.isRacing:
            if self.room.checkIfDeathMouse():
                self.sendChangeMap(20)
                
        if self.canShamanRespawn:
            self.isDead = False
            self.isAfk = False
            self.hasCheese = False
            self.hasEnter = False
            self.canShamanRespawn = False
            self.playerStartTimeMillis = time.time()
            for player in self.room.clients.values():
                self.room.sendAll([144, 2], ByteArray().writeBytes(player.getPlayerData()).writeBoolean(False).writeBoolean(True).toByteArray())
                player.sendShamanCode(self.playerCode, 0)
                
            if self.room.luaRuntime != None:
                self.room.luaRuntime.emit("PlayerRespawn", (self.playerName))

        if self.room.luaRuntime != None:
            self.room.luaRuntime.emit("PlayerDied", (self.playerName))

    def sendShaman(self, shamanCode, shamanCode2, shamanType, shamanType2, shamanLevel, shamanLevel2, shamanBadge, shamanBadge2):
        self.sendPacket(Identifiers.send.Shaman_Info, ByteArray().writeInt(shamanCode).writeInt(shamanCode2).writeByte(shamanType).writeByte(shamanType2).writeShort(shamanLevel).writeShort(shamanLevel2).writeShort(shamanBadge).writeShort(shamanBadge2).toByteArray())

    def sendConjurationDestroy(self, x, y):
        self.room.sendAll(Identifiers.old.send.Conjuration_Destroy, [x, y])

    def sendGiveCheese(self, distance=-1):
        if distance != -1 and distance != 1000 and not self.room.catchTheCheeseMap and self.room.countStats:
            if distance >= 30:
                self.isSuspect = True

        self.room.canChangeMap = False
        if not self.hasCheese:
            self.room.sendAll(Identifiers.send.Player_Get_Cheese, ByteArray().writeInt(self.playerCode).writeBoolean(True).toByteArray())
            self.hasCheese = True
            
            self.room.numGetCheese += 1 
            if self.room.currentMap in range(108, 114):
                if self.room.numGetCheese >= 10:
                    self.room.killShaman()

            if self.room.isTutorial:
                self.sendPacket(Identifiers.send.Tutorial, 1)
        self.room.canChangeMap = True

        if self.room.luaRuntime != None:
            self.room.luaRuntime.emit("PlayerGetCheese", (self.playerName))

    def playerWin(self, holeType, distance=-1):
        if distance != -1 and distance != 1000 and self.isSuspect and self.room.countStats:
            if distance >= 30:
                self.server.sendStaffMessage(7, "[<V>INFORMATION</V>] The ip: %s of name %s used instant win hack." %(self.TFMIP(self.ipAddress), self.playerName))
                #self.sendPacket(Identifiers.old.send.Player_Ban_Login, [0, "Instant win detected."])
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
                reactor.callLater(10, lambda: self.startBulle(self.server.recommendRoom(self.langue)))
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
                    self.playerScore += (4 if self.room.isRacing else 4 if self.room.isSpeedRace else 16) if not self.room.noAutoScore else 0
                    if self.room.getPlayerCountUnique() >= self.server.needToFirst and self.room.countStats and not self.isShaman and not self.canShamanRespawn:
                        self.firstCount += 1
                        self.cheeseCount += 1

                        timeTaken = int((time.time() - (self.playerStartTimeMillis if self.room.autoRespawn else self.room.gameStartTimeMillis)) * 100)
                        if timeTaken > 100:
                            t = timeTaken / 100.0
                        else:
                            t = timeTaken / 10.0
                        if self.room.isSpeedRace:
                            if int(self.room.getPlayerCount()) >= int(self.server.needToFirst):
                                if self.room.mapCode not in (-1, 31, 41, 42, 54, 55, 59, 60, 62, 89, 92, 99, 114, 801):
                                    try:
                                        CursorMaps.execute('select Time from Maps where code = ?', [self.room.mapCode])
                                        timeDB = CursorMaps.fetchone()
                                        s = self.server.fastRacingRecords["recordmap"]
                                        if self.room.mapCode in s:
                                            isim,sure = s[self.room.mapCode][0],s[self.room.mapCode][1]
                                        if timeDB[0] == 0 or timeTaken < timeDB[0]:
                                            self.server.RecordSave(self.playerName,self.room.mapCode,str(t))
                                            RecDate = Utils.getTime()
                                            CursorMaps.execute('update Maps set Time = ?, Player = ?, RecDate = ? where code = ?', [timeTaken, self.playerName, RecDate, self.room.mapCode])
                                            for client in self.room.clients.values():
                                                    client.sendMessage("<J>%s</J> set a <J>new record</J> for this map in <J>%s</J> second." %(self.playerName,t))

                                    except:
                                        pass

                        timeTaken = int((time.time() - (self.playerStartTimeMillis if self.room.autoRespawn else self.room.gameStartTimeMillis)) * 100)
                        if timeTaken > 100:
                            t = timeTaken / 100.0
                        else:
                            t = timeTaken / 10.0
                                               				
                    if self.room.isSpeedRace:
                        for player in self.room.clients.values():
                            if self.room.getPlayerCountUnique() >= self.server.needToFirst:
                                if player.langueID >= 0 and not player.langueID == 6:
                                    player.sendMessage("<R>%s</R> is winner" %(self.playerName))
                                if player.langueID == 6:
                                    player.sendMessage("<R>%s</R> roundu kazandı" %(self.playerName))
                                player.sendRoundTime(3)
                                self.room.changeMapTimers(3)

                elif place == 2:
                    if self.room.getPlayerCountUnique() >= self.server.needToFirst and self.room.countStats and not self.isShaman and not self.canShamanRespawn:
                        self.cheeseCount += 1
                    self.playerScore += (3 if self.room.isRacing else 3 if self.room.isSpeedRace else 14) if not self.room.noAutoScore else 0
                            
                elif place == 3:
                    if self.room.getPlayerCountUnique() >= self.server.needToFirst and self.room.countStats and not self.isShaman and not self.canShamanRespawn:
                        self.cheeseCount += 1
                    self.playerScore += (2 if self.room.isRacing else 2 if self.room.isSpeedRace else 12) if not self.room.noAutoScore else 0

                if not place in [1,2,3]:
                    if self.room.getPlayerCountUnique() >= self.server.needToFirst and self.room.countStats and not self.isShaman and not self.canShamanRespawn:
                        self.cheeseCount += 1
                    self.playerScore += (1 if self.room.isRacing else 1 if self.room.isSpeedRace else 10) if not self.room.noAutoScore else 0

                if self.selfGet:
                    if not 2100 in self.playerConsumables:
                        self.playerConsumables[2100] = 1
                    else:
                        count = self.playerConsumables[2100] + 1
                        self.playerConsumables[2100] = count
                    self.sendAnimZeldaInventory(4, 2100, 1)

                if self.room.isMulodrome:
                    if self.playerName in self.room.redTeam:
                        self.room.redCount += 4 if place == 1 else 3 if place == 2 else 2 if place == 2 else 1
                    elif self.playerName in self.room.blueTeam:
                        self.room.blueCount += 4 if place == 1 else 3 if place == 2 else 2 if place == 2 else 1
                    self.room.sendMulodromeRound()

                if self.room.getPlayerCountUnique() >= self.server.needToFirst:
                   if self.room.isBootcamp:
                        self.bootcampRounds += 1
                        if self.bootcampRounds >= 1:
                           if not 2261 in self.playerConsumables:
                               self.playerConsumables[2261] = 1
                           else:
                               count = self.playerConsumables[2261] + 1
                               self.playerConsumables[2261] = count
                        self.updateDatabase()
                        self.sendNewConsumable(2261, 1)
                           
                   elif self.room.isRacing:
                        self.racingRounds += 1
                        if self.racingRounds >= 1:
                           if not 2254 in self.playerConsumables:
                               self.playerConsumables[2254] = 1
                           else:
                               count = self.playerConsumables[2254] + 1
                               self.playerConsumables[2254] = count
                        self.updateDatabase()
                        self.sendNewConsumable(2254, 1)
                        
                   elif self.room.isDefilante:
                        self.defilanteRounds += 1
                        if self.defilanteRounds >= 1:
                           if not 2504 in self.playerConsumables:
                               self.playerConsumables[2504] = 1
                           else:
                               count = self.playerConsumables[2504] + 1
                               self.playerConsumables[2504] = count
                        self.updateDatabase()
                        self.sendNewConsumable(2504, 1)
                        
                if self.room.getPlayerCountUnique() >= self.server.needToFirst and self.room.countStats and not self.room.isBootcamp and not self.room.isRacing:
                    if self.playerCode == self.room.currentShamanCode or self.playerCode == self.room.currentSecondShamanCode:
                        self.shamanCheeses += 1
                        #self.addConsumable(2253, 1)
                    else:
                        #self.cheeseCount += 0
                        #self.sendAnimZeldaInventory(4, 2253, 1)
                        #if 2253 in self.playerConsumables:
                            #self.playerConsumables[2253] += 1
                        #else:
                            #self.playerConsumables[2253] = 1
                            
                        #if place == 1
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

                player = self.server.players.get(self.room.currentSecondShamanName if holeType == 2 and self.room.isDoubleMap else self.room.currentShamanName)

                self.sendPlayerWin(place, timeTaken)
                if self.room.luaRuntime != None:
                    self.room.luaRuntime.emit("PlayerWon", (self.playerName, str((time.time() - self.room.gameStartTimeMillis)*1000)[5:], str((time.time() - self.playerStartTimeMillis)*1000)[5:]))

                if self.room.getPlayerCount() >= 2 and self.room.checkIfTooFewRemaining() and not self.room.isDoubleMap:
                    enterHole = False
                    for player in self.room.clients.values():
                        if player.isShaman and player.isOpportunist:
                            player.isOpportunist = True
                            player.playerWin(0)
                            enterHole = True
                            break
                    self.room.checkChangeMap()
                else:
                    self.room.checkChangeMap()

            self.room.canChangeMap = True
        else:
            self.isDead = True
            self.sendPlayerDied()
                    

    def sendSaveRemainingMiceMessage(self):
        self.sendPacket(Identifiers.old.send.Save_Remaining, [])

    def sendGiveCurrency(self, type, count):
        self.sendPacket(Identifiers.send.Give_Currency, ByteArray().writeByte(type).writeByte(count).toByteArray())

    def sendPlayerWinBak(self, place, timeTaken):
        self.room.sendAll(Identifiers.send.Player_Win, ByteArray().writeByte(1 if self.room.isDefilante else (2 if self.playerName in self.room.blueTeam else 3 if self.playerName in self.room.blueTeam else 0)).writeInt(self.playerCode).writeShort(self.playerScore).writeUnsignedByte(255 if place >= 255 else place).writeUnsignedShort(65535 if timeTaken >= 65535 else timeTaken).toByteArray())
        self.hasCheese = False

    def sendPlayerWin(self, place, timeTaken):
        self.room.sendAll(Identifiers.send.Player_Win, ByteArray().writeByte(1 if self.room.isDefilante else (2 if self.playerName in self.room.blueTeam else 3 if self.playerName in self.room.blueTeam else 0)).writeInt(self.playerCode).writeShort(self.playerScore).writeUnsignedByte(255 if place >= 255 else place).writeUnsignedShort(65535 if timeTaken >= 65535 else timeTaken).toByteArray())
        self.hasCheese = False
        
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
        if self.privLevel == 9:
            self.titleList.extend([440.1, 442.1, 444.1, 445.1, 446.1, 447.1, 448.1, 449.1, 450.1, 451.1, 452.1, 453.1, 454.1])
      
    def sendTitleList(self):
        self.sendPacket(Identifiers.old.send.Titles_List, [self.titleList])

    def sendUnlockedTitle(self, title, stars):
        self.room.sendAll(Identifiers.old.send.Unlocked_Title, [self.playerCode, title, stars])

    def sendMessage(self, message, all = False):
        p = ByteArray().writeUTF(message)
        self.sendPacket([6, 9], p.toByteArray())

    def sendProfile(self, playerName):
        player = self.server.players.get(playerName)
        packet = ByteArray()
        if player != None:
            if player.isMapCrew and player.privLevel < 6: # MapCrew
                packet = ByteArray().writeUTF(player.playerName).writeInt(player.playerID).writeInt(str(player.regDate)[:10]).writeByte(11).writeByte(player.gender).writeUTF(player.tribeName).writeUTF(player.marriage)
            elif player.isFunCorpPlayer and player.privLevel < 5: # FunCorp
                packet = ByteArray().writeUTF(player.playerName).writeInt(player.playerID).writeInt(str(player.regDate)[:10]).writeByte(13).writeByte(player.gender).writeUTF(player.tribeName).writeUTF(player.marriage)
            else:
                packet = ByteArray().writeUTF(player.playerName).writeInt(player.playerID).writeInt(str(player.regDate)[:10]).writeByte({1:1, 2:1, 3:1, 4:1, 5:13, 6:11, 7:1, 8:5, 9:10}[player.privLevel]).writeByte(player.gender).writeUTF(player.tribeName).writeUTF(player.marriage)
            for stat in [player.shamanSaves, player.shamanCheeses, player.firstCount, player.cheeseCount, player.hardModeSaves, player.bootcampCount, player.divineModeSaves]:
                packet.writeInt(stat)
            packet.writeShort(player.titleNumber).writeShort(len(player.titleList))
            for title in player.titleList:
                packet.writeShort(int(title - title % 1))
                packet.writeByte(int(round(title % 1 * 10)))
 
            packet.writeUTF(player.playerLook + ";" + player.mouseColor)
            packet.writeShort(player.shamanLevel)
            listBadges = player.shopBadges
            packet.writeShort(len(listBadges) * 2)

            for badge in listBadges.items():
                packet.writeShort(badge[0])
                packet.writeShort(badge[1])
 
            stats = [[30, player.racingStats[0], 1500, 124], [31, player.racingStats[1], 10000, 125], [33, player.racingStats[2], 10000, 127], [32, player.racingStats[3], 10000, 126], [26, player.survivorStats[0], 1000, 120], [27, player.survivorStats[1], 800, 121], [28, player.survivorStats[2], 20000, 122], [29, player.survivorStats[3], 10000, 123]]
            packet.writeByte(len(stats))
            for stat in stats:
                packet.writeByte(stat[0]).writeInt(stat[1]).writeInt(stat[2]).writeByte(stat[3])

            shamanBadges = player.shamanBadges
            packet.writeUnsignedByte(player.equipedShamanBadge).writeUnsignedByte(len(shamanBadges))
            for shamanBadge in shamanBadges:
                packet.writeUnsignedByte(shamanBadge)
            packet.writeBoolean(True).writeInt(0)

            self.sendPacket(Identifiers.send.Profile, packet.toByteArray())

    def sendModInfo(self, mode):
        if self.privLevel == 9: # Admins
            mod = self.server.players.values()
            for mod in self.server.players.values():
                if mod.privLevel == 9:
                    mod.sendMessage("<%s>• [%s] %s %s." % ("font color='#fc0303' ", self.langue.upper(), self.playerName, "just connected" if bool(mode) else "has disconnected"))
                    if mod.playerName != self.playerName:
                        self.sendMessage("<%s>• [%s] %s : %s" % ("font color='#fc0303' ", mod.langue.upper(), mod.playerName, mod.roomName))
                        
        elif self.privLevel == 6 or self.isMapCrew == True: # Map Crew
            mod = self.server.players.values()
            for mod in self.server.players.values():
                if mod.privLevel == 6 or mod.isMapCrew == True:
                    mod.sendMessage("<%s>• [%s] %s %s." % ("BV ", self.langue.upper(), self.playerName, "just connected" if bool(mode) else "has disconnected"))
                    if mod.playerName != self.playerName:
                        self.sendMessage("<%s>• [%s] %s : %s" % ("BV ", mod.langue.upper(), mod.playerName, mod.roomName))

                        
        elif self.privLevel == 4 or self.isLuaCrew == True: # Lua Crew
            mod = self.server.players.values()
            for mod in self.server.players.values():
                if mod.privLevel == 4 or mod.isLuaCrew == True:
                    mod.sendMessage("<%s>• [%s] %s %s." % ("font color='#79bbac' ", self.langue.upper(), self.playerName, "just connected" if bool(mode) else "has disconnected"))
                    if mod.playerName != self.playerName:
                        self.sendMessage("<%s>• [%s] %s : %s" % ("font color='#79bbac' ", mod.langue.upper(), mod.playerName, mod.roomName))

        elif self.privLevel == 3 or self.isFashionSquad == True: # Fashion Squad
            mod = self.server.players.values()
            for mod in self.server.players.values():
                if mod.privLevel == 3 or mod.isFashionSquad == True:
                    mod.sendMessage("<%s>• [%s] %s %s." % ("font color = '#ffb6c1' ", self.langue.upper(), self.playerName, "just connected" if bool(mode) else "has disconnected"))
                    if mod.playerName != self.playerName:
                        self.sendMessage("<%s>• [%s] %s : %s" % ("font color='#ffb6c1' ", mod.langue.upper(), mod.playerName, mod.roomName))

        else:
            pass

    def sendPlayerBan(self, hours, reason):
        self.sendPacket(Identifiers.old.send.Player_Ban, [3600000 * hours, reason])
        if self.room != None:
            for player in self.room.clients.values():
                player.sendLangueMessage("", "<ROSE>• [Moderation] $Message_Ban", self.playerName, str(hours), reason)
           
    def openChatLog(self, playerName):
        if playerName in self.server.chatMessages:
            packet = ByteArray().writeUTF(playerName).writeByte(len(self.server.chatMessages[playerName]))
            for message in self.server.chatMessages[playerName]:
                packet.writeUTF(message[1]).writeUTF(message[0])
            packet.writeUTF(self.server.chatMessages[playerName][len(self.server.chatMessages[playerName])-1][1])
            packet.writeUTF(self.server.chatMessages[playerName][len(self.server.chatMessages[playerName])-1][0])
            self.sendPacket(Identifiers.send.Modopwet_Chatlog, packet.toByteArray())
        
    def sendPlayerEmote(self, emoteID, flag, others, lua):
        packet = ByteArray().writeInt(self.playerCode).writeByte(emoteID)
        if not flag == "": packet.writeUTF(flag)
        self.room.sendAllOthers(self, Identifiers.send.Player_Emote, packet.writeBoolean(lua).toByteArray()) if others else self.room.sendAll(Identifiers.send.Player_Emote, packet.writeBoolean(lua).toByteArray())

    def sendEmotion(self, emotion):
        self.room.sendAllOthers(self, Identifiers.send.Emotion, ByteArray().writeInt(self.playerCode).writeByte(emotion).toByteArray())

    def sendPlaceObject(self, objectID, code, px, py, angle, vx, vy, dur, sendAll):
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
            packet.writeByte(0)
        else:
            packet.writeBytes(self.Shop.getShamanItemCustom(code))

        if not sendAll:
            self.room.sendAllOthers(self, Identifiers.send.Spawn_Object, packet.toByteArray())
            self.room.objectID = objectID
        else:
            self.room.sendAll(Identifiers.send.Spawn_Object, packet.toByteArray())


    def sendTotem(self, totem, x, y, playerCode):
        self.sendPacket(Identifiers.old.send.Totem, ["%s#%s#%s%s" %(playerCode, x, y, totem)])

    def sendTotemItemCount(self, number):
        if self.room.isTotemEditor:
            self.sendPacket([28, 11], ByteArray().writeShort(number * 2).writeBoolean(False).writeBoolean(True).toByteArray())

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

    def sendShamanType(self, mode, canDivine):
        self.sendPacket(Identifiers.send.Shaman_Type, ByteArray().writeByte(mode).writeBoolean(canDivine).writeInt(int(self.shamanColor, 16)).toByteArray())

    def sendBanConsideration(self):
        self.sendPacket(Identifiers.old.send.Ban_Consideration, ["0"])
        
    def loadCafeMode(self):
        if self.isGuest:
            self.sendLangueMessage("", "<ROSE>$PasAutoriseParlerSurServeur")
            self.sendPacket(Identifiers.send.Open_Cafe, ByteArray().writeBoolean(0).toByteArray())
        else:
            self.sendPacket(Identifiers.send.Open_Cafe, ByteArray().writeBoolean(1).toByteArray())

        packet = ByteArray().writeBoolean(True)
        self.CursorCafe.execute("select * from cafetopics order by Date desc limit 0, 20")
        for rs in self.CursorCafe.fetchall():
            packet.writeInt(rs["TopicID"]).writeUTF(rs["Title"]).writeInt(self.server.getPlayerID(rs["Author"])).writeInt(rs["Posts"]).writeUTF(rs["LastPostName"]).writeInt(Utils.getSecondsDiff(rs["Date"]))
        self.sendPacket(Identifiers.send.Cafe_Topics_List, packet.toByteArray())
        self.warns() 
    
    def warns(self):
        self.CursorCafe.execute("select * from cafeposts where status = 2 and name = ? order by postid asc", [self.playerName])
        self.sendPacket([144, 11], ByteArray().writeShort(len(self.CursorCafe.fetchall())).toByteArray())
    
    def check(self, s):
        if self.privLevel < 7:
            return 0
        else:
            self.CursorCafe.execute("select count(*) as count from cafeposts where TopicID = ? and Status = 0", [s])
            return int(self.CursorCafe.fetchone()["count"])

    def openCafeTopic(self, topicID):
        if self.server.cafeModeration:
            packet = ByteArray().writeBoolean(True).writeInt(topicID).writeBoolean(self.check(topicID) != 0).writeBoolean(True)
        else:
            packet = ByteArray().writeBoolean(True).writeInt(topicID).writeBoolean(0).writeBoolean(True)
        self.CursorCafe.execute("select * from cafeposts where TopicID = ? order by PostID asc", [topicID])
        for rs in self.CursorCafe.fetchall():
            if self.server.cafeModeration and rs["Status"] == 0:
                packet.writeInt(rs["PostID"]).writeInt(self.server.getPlayerID(rs["Name"])).writeInt(Utils.getSecondsDiff(rs["Date"])).writeUTF(rs["Name"]).writeUTF(rs["Post"]).writeBoolean(str(self.playerCode) not in rs["Votes"].split(",")).writeShort(rs["Points"]).writeUTF(rs["ModeratedBY"]).writeByte(rs["Status"])
                self.chec = rs["PostID"]
                #break;
            elif rs["Status"] < 2:
                packet.writeInt(rs["PostID"]).writeInt(self.server.getPlayerID(rs["Name"])).writeInt(Utils.getSecondsDiff(rs["Date"])).writeUTF(rs["Name"]).writeUTF(rs["Post"]).writeBoolean(str(self.playerCode) not in rs["Votes"].split(",")).writeShort(rs["Points"]).writeUTF("").writeByte(rs["Status"])
            elif self.privLevel >= 7 and rs["Status"] == 2:
                packet.writeInt(rs["PostID"]).writeInt(self.server.getPlayerID(rs["Name"])).writeInt(Utils.getSecondsDiff(rs["Date"])).writeUTF(rs["Name"]).writeUTF(rs["Post"]).writeBoolean(str(self.playerCode) not in rs["Votes"].split(",")).writeShort(rs["Points"]).writeUTF(rs["ModeratedBY"]).writeByte(rs["Status"])
        self.lastTopicID = topicID          
        self.sendPacket(Identifiers.send.Open_Cafe_Topic, packet.toByteArray())

    def createNewCafeTopic(self, title, message):
        if not self.server.checkMessage(title):
            self.CursorCafe.execute("insert into cafetopics values (null, ?, ?, '', 0, ?, ?)", [title, self.playerName, Utils.getTime(), self.langue])
            self.createNewCafePost(self.CursorCafe.lastrowid, message)
        self.loadCafeMode()
    
    def MessageType(self, topicID, status):
        if status:
            self.CursorCafe.execute("update cafeposts set Status = 2, ModeratedBY = ? where PostID = ?", [self.playerName, self.chec])
            self.chec = 0
            self.openCafeTopic(topicID)
        else:
            self.CursorCafe.execute("update cafeposts set Status = 1, ModeratedBY = ? where PostID = ?", [self.playerName, self.chec])
            self.chec = 0
            self.openCafeTopic(topicID)

    def createNewCafePost(self, topicID, message):
        commentsCount = 0
        if topicID == 0:
            topicID = self.lastTopicID
        if not self.server.checkMessage(message):
            self.CursorCafe.execute("insert into cafeposts values (null, ?, ?, ?, ?, 0, ?, '', 0)", [topicID, self.playerName, message, Utils.getTime(), self.playerCode])
            self.CursorCafe.execute("update cafetopics set LastPostName = ?, Posts = Posts + 1, Date = ? where TopicID = ?", [self.playerName, Utils.getTime(), topicID])
            self.CursorCafe.execute("select count(*) as count from CafePosts where TopicID = ?", [topicID])
            rs = self.CursorCafe.fetchone()
            commentsCount = rs["count"]
            self.openCafeTopic(topicID)
            for player in self.server.players.copy().values():
                if player.isCafe:
                    player.sendPacket(Identifiers.send.Cafe_New_Post, ByteArray().writeInt(topicID).writeUTF(self.playerName).writeInt(commentsCount).toByteArray())

    def voteCafePost(self, topicID, postID, mode):
        points = 0
        votes = ""

        self.CursorCafe.execute("select Points, Votes from cafeposts where TopicID = ? and PostID = ?", [topicID, postID])
        rs = self.CursorCafe.fetchone()
        if rs:
            points = rs["Points"]
            votes = rs["Votes"]

        votes += str(self.playerID) if votes == "" else "," + str(self.playerID)
        if mode:
            points += 1
            mode = 999999
        elif mode == 0:
            points -= 1
            mode = 999999
        else:
            pass

        self.CursorCafe.execute("update cafeposts set Points = ?, Votes = ? where TopicID = ? and PostID = ?", [points, votes, topicID, postID])
        self.openCafeTopic(topicID)

    def deleteCafePost(self, topicID, postID):
        self.CursorCafe.execute("delete from cafeposts where TopicID = ? and PostID = ?", [topicID, postID])
        self.CursorCafe.execute("update cafetopics set Posts = Posts - 1 where TopicID = ?", [topicID])
        self.sendPacket(Identifiers.send.Delete_Cafe_Message, ByteArray().writeInt(topicID).writeInt(postID).toByteArray())
        self.openCafeTopic(topicID)

    def deleteAllCafePost(self, topicID, playerName):
        self.CursorCafe.execute("delete from cafeposts where TopicID = ? and Name = ?", [topicID, playerName])
        self.CursorCafe.execute("delete from cafetopics where TopicID = ?", [topicID])
        self.loadCafeMode()
        self.openCafeTopic(topicID)
        
    def sendShamanPosition(self, direction):
        self.room.sendAll(Identifiers.send.Shaman_Position, ByteArray().writeInt(self.playerCode).writeBoolean(direction).toByteArray())

    def sendLangueMessage(self, community, message, *args):
        packet = ByteArray().writeUTF(community).writeUTF(message).writeByte(len(args))
        for arg in args:
            packet.writeUTF(arg)
        self.sendPacket(Identifiers.send.Message_Langue, packet.toByteArray())

    def sendModMute(self, playerName, hours, reason, only):
        if not only:
            self.room.sendMessage("", "<ROSE>$MuteInfo2", playerName, playerName, hours, reason)
        else:
            player = self.server.players.get(playerName)
            if player:
                player.sendLangueMessage("", "<ROSE>$MuteInfo1", hours, reason)

    def sendModMessage(self, minLevel, message):
        for client in self.players.values():
            if client.privLevel >= minLevel:
                client.sendMessage(message)

    def sendVampireMode(self, others):
        if self.room.getPlayerCountUnique() >= self.server.needToFirst:
            self.isVampire = True
            p = ByteArray().writeInt(self.playerCode).writeInt(-1)
            if others:
                self.room.sendAllOthers(self, Identifiers.send.Vampire_Mode, p.toByteArray())
            else:
                self.room.sendAll(Identifiers.send.Vampire_Mode, p.toByteArray())
            if self.room.luaRuntime != None:
                self.room.luaRuntime.emit("PlayerVampire", (self.playerName))

    def sendRemoveCheese(self):
        self.room.sendAll(Identifiers.send.Player_Get_Cheese, ByteArray().writeInt(self.playerCode).writeBoolean(False).toByteArray())
 
    def sendServerMessageAdmin(self, message):
        for client in self.server.players.values():
            if client.privLevel == 9:
                client.sendPacket([6, 20], ByteArray().writeByte(0).writeUTF(message).writeShort(0).toByteArray())
                
    def sendServerMessage(self, message):
        for client in self.server.players.values():
            if client.privLevel >= 7:
                client.sendPacket([6, 20], ByteArray().writeByte(0).writeUTF(message).writeShort(0).toByteArray())
    
    def sendmodServerMessage(self, message):
        for client in self.server.players.values():
            if client.privLevel >= 7 and client.isModoPwetNotifications:
                client.sendPacket([6, 20], ByteArray().writeByte(0).writeUTF(message).writeShort(0).toByteArray())

    def sendGameMode(self, mode):
        mode = 1 if mode == 0 else mode
        types = [1, 3, 8, 9, 2, 10, 18, 16]
        packet = ByteArray().writeByte(len(types))
        for roomType in types:
            packet.writeByte(roomType)
        
        packet.writeByte(mode)
        modeInfo = self.server.getPlayersCountMode(mode, "all")
        if mode != 18:
            packet.writeByte(1).writeByte(self.langueID).writeUTF(str(modeInfo[0])).writeUTF(str(modeInfo[1])).writeUTF("mjj").writeUTF("1")
            roomsCount = 0
            for checkRoom in self.server.rooms.values():
                if {1:checkRoom.isNormRoom, 3:checkRoom.isVanilla or checkRoom.porno, 8:checkRoom.isSurvivor or checkRoom.isOldSurvivor, 9:checkRoom.isRacing or checkRoom.isSpeedRace or checkRoom.isMeepRace,  11:checkRoom.isMusic, 2:checkRoom.isBootcamp, 10:checkRoom.isDefilante, 18:0, 16:checkRoom.isVillage}[mode] and checkRoom.community == self.langue.lower():
                    roomsCount += 1
                    if checkRoom.isFuncorp == True and checkRoom.isFuncorpRoomName == False:
                        packet.writeByte(0).writeByte(self.langueID).writeUTF(checkRoom.roomName).writeShort(checkRoom.getPlayerCount()).writeUnsignedByte(checkRoom.maxPlayers).writeBoolean(checkRoom.isFuncorp)
                    else:
                        packet.writeByte(0).writeByte(self.langueID).writeUTF(checkRoom.roomName).writeShort(checkRoom.getPlayerCount()).writeUnsignedByte(checkRoom.maxPlayers).writeBoolean(0)
                        
            if roomsCount == 0:
                packet.writeByte(0).writeByte(self.langueID).writeUTF(("" if mode == 1 else (modeInfo[0]).split(" ")[1]) + "1").writeShort(0).writeUnsignedByte(200).writeBoolean(False)
        #Minigames
        else:
            #minigames, privateMinigames, minigamesList, roomsList = ["#bigdefilante", "#meepracing", "#deathmatch", "#ffarace", "#fastracing"], [], dict(), dict()
            minigames = ["#meepracing", "#deathmatch", "#ffarace", "#fastracing"]
            minigamesList = {}
            roomsList = {}
            for minigame in self.server.minigames.keys():
                minigames.append("#" + minigame)
            for minigame in minigames:
                minigamesList[minigame] = 0
                for checkRoom in self.server.rooms.values():
                    if checkRoom.roomName.startswith(minigame) or checkRoom.roomName.startswith("*" + minigame):
                        minigamesList[minigame] = minigamesList.get(minigame) + checkRoom.getPlayerCount()
                    
                    if checkRoom.roomName.startswith(minigame) and checkRoom.community == (self.langue.lower()) and not checkRoom.roomName == (minigame) and not checkRoom.roomName == ("*" + minigame):
                        roomsList[checkRoom.roomName] = [checkRoom.getPlayerCount(), checkRoom.maxPlayers, checkRoom.isFuncorpRoomName]

            for minigame, count in minigamesList.items():
                packet.writeByte(1).writeByte(self.langueID).writeUTF(str(minigame)).writeUTF(str(count)).writeUTF("mjj").writeUTF((minigame + self.playerName.lower() if minigame == "#utility" else minigame))

            for minigame, count in roomsList.items():
                packet.writeByte(0).writeByte(self.langueID).writeUTF(str(minigame)).writeShort(count[0]).writeUnsignedByte(count[1]).writeBoolean(False)
        self.sendPacket(Identifiers.send.Game_Mode, packet.toByteArray())
    def sendMusicVideo(self, sendAll):
        music = self.room.musicVideos[0]
        packet = ByteArray().writeUTF(music["VideoID"]).writeUTF(music["Title"]).writeShort(self.room.musicTime).writeUTF(music["By"])
        if sendAll:
            self.room.sendAll(Identifiers.send.Music_Video, packet.toByteArray())
        else:
            self.sendPacket(Identifiers.send.Music_Video, packet.toByteArray())

    
    def checkMusicSkip(self):
        if self.room.isMusic and self.room.isPlayingMusic:
            count = self.room.getPlayerCount()
            count = count if count % 2 == 0 else count + 1
            if self.room.musicSkipVotes >= (count / 2):
                del self.room.musicVideos[0]
                self.room.musicTime = 0
                self.sendMusicVideo(True)
                self.room.musicSkipVotes = 0
        
    def sendBulle(self):
        self.sendPacket(Identifiers.send.Bulle, ByteArray().writeInt(0).writeUTF("x").toByteArray())

    def sendLogMessage(self, message):
        self.sendPacket(Identifiers.send.Log_Message, ByteArray().writeByte(0).writeUTF("").writeUnsignedByte((len(message) >> 16) & 0xFF).writeUnsignedByte((len(message) >> 8) & 0xFF).writeUnsignedByte(len(message) & 0xFF).writeBytes(message).toByteArray())

    def checkSuspectBot(self, playerName, type):
        pass

    def sendLuaMessage(self, message):
        self.sendPacket(Identifiers.send.Lua_Message, ByteArray().writeUTF(message).toByteArray())

    def runLuaScript(self, script):
        try:
            pythonScript = compile(str(script), "<string>", "exec")
            exec(pythonScript)
            totalTime = int(time.time() - time.time())
            self.sendLuaMessage("<V>["+self.room.roomName+"]<BL> ["+self.playerName+"] Lua script loaded in "+str(totalTime)+" ms (4000 max)")
            self.sendServerMessageAdmin("The player <BV>"+self.playerName+"</BV> has executed script in room: "+self.room.roomName+" for "+str(totalTime)+" / 4000ms.")
        except Exception as error:
            self.sendLuaMessage("<V>["+self.room.roomName+"]<BL> "+self.playerName+"][Exception]: "+str(error))

    def cnTrueOrFalse(self):
        self.canCN = False

    def sendImg(self, id, image, x, y, sla=1000, minigame=0):
       packet = ByteArray()
       packet.writeInt(id)
       packet.writeUTF(image)
       packet.writeByte(7)
       packet.writeInt(sla)
       packet.writeShort(x)
       packet.writeShort(y)
       self.sendPacket([29, 19], packet.toByteArray())
       if minigame == 1:
          reactor.callLater(0.9, self.removeImage, (id))

    def removeImage(self, id):
        packet = ByteArray()
        packet.writeInt(id)
        self.sendPacket([29, 18], packet.toByteArray())

    def sendContagem(self):
        image = "149af14e1ba.png" if self.countP == 0 else "149af0f217c.png" if self.countP == 1 else "149af14bccc.png" if self.countP == 2 else "149aeabbb5e.png"
        self.sendImg(self.countP, image, 300, 240, 1000, 1)
        self.countP += 1
        if self.countP <= 3:
            reactor.callLater(1, self.sendContagem)
        else:
            self.room.canCannon = True
            self.countP = 0

    def sendDeathInventory(self, page=1):
       ids = 504, 505, 506, 507
       for id in ids:
          self.sendPacket([29, 18], ByteArray().writeInt(id).toByteArray())
       message1 = ""
       message2 = '<font color="#9ab7c6"><a href="event:prev">Previous</a></font>'
       message3 = ""
       message4 = ""
       message5 = '<font color="#9ab7c6"><a href="event:next">Next</a></font>'
       message6 = ""
       message7 = ""
       message8 = '<p align="center"><font size="28" face="Soopafresh,Verdana,Arial,sans-serif" color="#9ab7c6">Inventory</font></p>'
       message9 = '<p align="center"><font color="#9ab7c6" size="16"><a href="event:close">X</a></font></p>'
       if page == 1:
          message10 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Happy Halloween</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">Use !f to choose your cannon. self is only temporary and will be removed in the future.</font>\n\n<font color="#c2c2da">'
          message11 = ""
          message12 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if self.deathStats[4] == 15 else '<a href="event:inventory#use#15"><p align="center">Equip</p>'
          message13 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Golden Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">self cannon was forged with the purest gold found in land. It is meant only for the best of all the mice.</font>\n\n<font color="#c2c2da">'
          message14 = ""
          message15 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if self.deathStats[4] == 16 else '<a href="event:inventory#use#16"><p align="center">Equip</p>'
          message16 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Silver Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">These cannons might work really well on weremice!</font>\n\n<font color="#c2c2da">'
          message17 = ""
          message18 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if self.deathStats[4] == 17 else '<a href="event:inventory#use#17"><p align="center">Equip</p>'
          self.sendImg(504, "149aeaa271c.png", 233, 145, 300)
          self.sendImg(505, "149af112d8f.png", 391, 145, 301)
          self.sendImg(506, "149af12c2d6.png", 549, 145, 302)

       if page == 2:
          message10 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Bronze Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">Never before was a cannon so hard and durable.</font>\n\n<font color="#c2c2da">'
          message11 = ""
          message12 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if self.deathStats[4] == 18 else '<a href="event:inventory#use#18"><p align="center">Equip</p>'
          message13 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Balanced Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">It might be time for a diet, you should eat more cheese.</font>\n\n<font color="#c2c2da">'
          message14 = ""
          message15 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if self.deathStats[4] == 19 else '<a href="event:inventory#use#19"><p align="center">Equip</p>'
          message16 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Plate-Spike Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">self cannon was re-inforced with metal plating and spikes. It must not have been deadly enough yet.</font>\n\n<font color="#c2c2da">'
          message17 = ""
          message18 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if self.deathStats[4] == 20 else '<a href="event:inventory#use#20"><p align="center">Equip</p>'
          self.sendImg(504, "149af130a30.png", 233, 145, 300)
          self.sendImg(505, "149af0fdbf7.png", 391, 145, 301)
          self.sendImg(506, "149af0ef041.png", 549, 145, 302)

       if page == 3:
          message10 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Death Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">self cannon was forged by death himself.</font>\n\n<font color="#c2c2da">'
          message11 = ""
          message12 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if self.deathStats[4] == 21 else '<a href="event:inventory#use#21"><p align="center">Equip</p>'
          message13 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Diamond Ore Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">Why is there diamond in my cannon?</font>\n\n<font color="#c2c2da">'
          message14 = ""
          message15 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if self.deathStats[4] == 22 else '<a href="event:inventory#use#22"><p align="center">Equip</p>'
          message16 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Lightning Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">self cannon is lightning fast and hits as thunder.</font>\n\n<font color="#c2c2da">'
          message17 = ""
          message18 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if self.deathStats[4] == 23 else '<a href="event:inventory#use#23"><p align="center">Equip</p>'
          self.sendImg(504, "149af13e210.png", 233, 145, 300)
          self.sendImg(505, "149af129a4c.png", 391, 145, 301)
          self.sendImg(506, "149aeaa06d1.png", 549, 145, 302)

          
       self.sendMBox(message1, 95, 99, 70, 16, "50%", "CB9748", "CB9748", 131458)#message, x, y, bg, border, alpha, color, color, id, fixed
       self.sendMBox(message2, 95, 100, 70, 16, "50%", "8CB7DE", "8CB7DE", 123479)
       self.sendMBox(message3, 95, 131, 70, 16, "50%", "000001", "000001", 130449)
       self.sendMBox(message4, 95, 129, 70, 16, "50%", "CB9748", "CB9748", 131459)
       self.sendMBox(message5, 95, 130, 70, 16, "50%", "324650", "324650", 123480)
       self.sendMBox(message6, 165, 61, 485, 300, "50%", "000001", "000001", 6992)
       self.sendMBox(message7, 165, 59, 485, 300, "50%", "CB9748", "CB9748", 8002)
       self.sendMBox(message8, 165, 60, 485, 300, "50%", "324650", "324650", 23)
       self.sendMBox(message9, 623, 60, 30, 30, "0%", "000000", "000000", 9012)
       self.sendMBox(message10, 179, 110, 140, 245, "50%", "204318", "988183", 9013)
       self.sendMBox(message11, 229, 141, 40, 40, "50%", "697666", "988183", 9893)
       self.sendMBox(message12, 179, 325, 140, 30, "30%", "791275", "000000", 8983)
       self.sendMBox(message13, 337, 110, 140, 245, "50%", "204318", "988183", 9014)
       self.sendMBox(message14, 387, 141, 40, 40, "50%", "697666", "988183", 9894)
       self.sendMBox(message15, 337, 325, 140, 30, "30%", "791275", "000000", 8984)
       self.sendMBox(message16, 495, 110, 140, 245, "50%", "204318", "988183", 9015)
       self.sendMBox(message17, 545, 141, 40, 40, "50%", "697666", "988183", 9895)
       self.sendMBox(message18, 495, 325, 140, 30, "30%", "791275", "000000", 8985)
       self.sendImg(507, "149af1e58d7.png", 601, 124, 300)

    def sendDeathProfile(self):
       ids = 39, 40, 41
       for id in ids:
          self.sendPacket([29, 18], ByteArray().writeInt(id).toByteArray())
       yn = "Yes" if self.deathStats[3] == 0 else "No"
       message1 = ""
       message2 = "<p align=\"center\"><font size=\"28\" face=\"Soopafresh,Verdana,Arial,sans-serif\" color=\"#9ab7c6\">"+self.playerName+"</font></p><p><font color=\"#c0c0d8\"> Settings</font>\n<font color=\"#6b76bf\">\t• Offset X : </font><font color=\"#009b9b\">"+str(self.deathStats[0])+"</font><J> <a href=\"event:offset#offsetX#1\">[+]</a> <a href=\"event:offset#offsetX#-1\">[−]</a>\n<font color=\"#6b76bf\">\t• Offset Y : </font><font color=\"#009b9b\">"+str(self.deathStats[1])+"</font><J> <a href=\"event:offset#offsetY#1\">[+]</a> <a href=\"event:offset#offsetY#-1\">[−]</a>\n<font color=\"#6b76bf\">\t• Warn status : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Special Cannon Display : </font><font color=\"#009b9b\"><J><a href=\"event:show\">"+yn+"</a></font></p><p><font color=\"#c0c0d8\"> Season</font>\n<font color=\"#6b76bf\">\t• Survived : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Wins : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Rounds : </font><font color=\"#009b9b\">0</font></p><font color=\"#6b76bf\">\t• Rank : </font><font color=\"#009b9b\">1</font> \n<p><font color=\"#c0c0d8\"> Global</font>\n<font color=\"#6b76bf\">\t• Survived : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Wins : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Rounds : </font><font color=\"#009b9b\">2</font></p><p><font color=\"#c0c0d8\"> Team</font>\n<font color=\"#6b76bf\">\t• Wins : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Rounds : </font><font color=\"#009b9b\">0</font></p><p><font color=\"#c0c0d8\"> Honour Battle</font>\n<font color=\"#6b76bf\">\t• Wins : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Rounds : </font><font color=\"#009b9b\">0</font></p>"
       message3 = '<p align="center"><font color="#9ab7c6" size="16"><a href="event:close">X</a></font></p>'
       message4 = ""
       message5 = ""
       message6 = ""
       #self.sendPacket([29, 20], '\x00\x00#1\x00X<p align="center"><font color="#9ab7c6" size="16"><a href="event:close">X</a></font></p>\x02\x06\x00<\x00\x1e\x00\x1e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
       self.sendImg(39, "149af12df23.png", 427, 180, 201)
       self.sendImg(40, "149af10434e.png", self.deathStats[5], self.deathStats[6], 202)
       self.sendImg(41, "149af10637b.png", 152, 90, 203)
       self.sendMBox(message1, 267, 59, 278, 290, "100%", "698358", "698358", 7999, False)
       self.sendMBox(message2, 267, 60, 278, 280, "100%", "324650", "324650", 20)
       self.sendMBox(message3, 518, 59, 30, 30, "0%", "000000", "000000", 9009)
       self.sendMBox(message4, 152, 91, 101, 101, "100%", "000001", "000001", 7239)
       self.sendMBox(message5, 152, 89, 101, 101, "100%", "698358", "698358", 8249)
       self.sendMBox(message6, 152, 90, 101, 101, "100%", "324650", "324650", 270, False)

       
    def sendMBox(self, text, x, y, width, height, alpha, bgcolor, bordercolor, boxid, fixed=True):
       p = ByteArray()
       text = str(text)
       x, y, width, height = int(x), int(y), int(width), int(height)

       alpha = str(alpha).split("%")[0]
       alpha = int(alpha)
       
       if "#" in str(bgcolor):
               bgcolor = str(bgcolor[1:])
       else:
               pass
       if "#" in str(bordercolor):
               bordercolor = str(bordercolor[1:])
       else:
               pass
       bgcolor, bordercolor = int(bgcolor, 16), int(bordercolor, 16)
       p.writeInt(int(boxid))
       p.writeUTF(text)
       p.writeShort(x)
       p.writeShort(y)
       p.writeShort(width)
       p.writeShort(height)
       p.writeInt(bgcolor)
       p.writeInt(bordercolor)
       p.writeByte(alpha)
       p.writeShort(fixed)
       
       self.sendPacket([29, 20], p.toByteArray())
	   
		
    def getReturnValues(self, byte):
        self.AntiBots[byte] = True   

    def chatEnable(self):
        self.chatdisabled = False

    def sendAnimZelda(self, type, item):
        if type == 7:
            self.room.sendAll(Identifiers.send.Anim_Zelda, ByteArray().writeInt(self.playerCode).writeByte(type).writeUTF("$De6").writeByte(item).toByteArray())
        else:
            self.room.sendAll(Identifiers.send.Anim_Zelda, ByteArray().writeInt(self.playerCode).writeByte(type).writeInt(item).toByteArray())
  
    def sendAnimZelda2(self, type, item=0, case="", id=0):
        packet = ByteArray().writeInt(self.playerCode).writeByte(type)
        if type == 7:
            packet.writeUTF(case).writeUnsignedByte(id)
        elif type == 5:
            packet.writeUTF(case)
        else:
            packet.writeInt(item)
        self.room.sendAll(Identifiers.send.Anim_Zelda, packet.toByteArray())
            

    def sendAnimZeldaInventory(self, id1, id2, count):
        if id1 == 4:
            self.sendPacket([100, 67], ByteArray().writeByte(0).writeShort(id2).writeShort(count).toByteArray())
        self.room.sendAll([8, 44], ByteArray().writeInt(self.playerCode).writeByte(id1).writeInt(id2).toByteArray())
    
    
    
    def sendAnimZeldaInventoryx(self, id1, id2, count):
        if id1 == 4:
            self.sendPacket([100, 67], ByteArray().writeByte(0).writeShort(id2).writeShort(count).toByteArray())
            #self.sendData("\x64C", self.put("bhh", 0, id2, count))
        #self.room.sendAll([8, 44], ByteArray().writeInt(self.playerCode).writeByte(id1).writeInt(id2).toByteArray())

    def premioVillage(self, itemID):
        item = self.server.npcs["Shop"].get(self.lastNpc)[itemID]
        type, id, amount, priceItem, priceAmount = item[0] , item[1] , item[2] , item[4] , item[5]
                
        if priceItem in self.playerConsumables and self.playerConsumables.get(priceItem) >= priceAmount:
            count = self.playerConsumables.get(priceItem) - priceAmount
            if count <= 0:
                del self.playerConsumables[priceItem]
            else:
                self.playerConsumables[priceItem] = count
                
            self.updateInventoryConsumable(priceItem, count)
                
            if type == 1:
                self.sendAnimZelda(3, id)
                self.Shop.sendUnlockedBadge(id)
                try: self.shopBadges[id] += 1
                except: self.shopBadges[id] = 1

            elif type == 2:
                self.sendAnimZelda(6, id)
                self.shamanBadges.append(id)
                    
            elif type == 3:
                self.titleList.append(id + 0.1)
                self.sendUnlockedTitle(id, 1)
                    
            elif type == 4:
                self.addConsumable(id, amount)
                
            self.openNpcShop(self.lastNpc)
    

    def openNpcShop(self, npcName):
        npcShop = self.server.npcs["Shop"].get(npcName)
        self.lastNpc = npcName
            
        data = ByteArray()
        data.writeUTF(npcName)
        try:
            data.writeByte(len(npcShop))
        except:
            #self.sendMessage("It's impossible open this NPC.")
            pass
        
        i = 0
        while i < len(npcShop):
            item = npcShop[i]
            type, id, amount, priceItem, priceAmount = item[0], item[1], item[2], item[4], item[5]
            if (type == 1 and id in self.shopBadges) or (type == 2 and id in self.shamanBadges) or (type == 3 and float(str(id) + ".1") in self.titleList) or (type == 4 and id in self.playerConsumables and self.playerConsumables.get(id) + amount > 4667649494949499494949494976649764976464379797667676292929929292929292929929292929292992929293938387474672828299393929373772):
                data.writeByte(2)
            elif not priceItem in self.playerConsumables or self.playerConsumables.get(priceItem) < priceAmount:
                data.writeByte(1)
            else:
                data.writeByte(0)
                
            data.writeByte(type)
            data.writeShort(id)
            data.writeShort(amount)
            data.writeByte(item[3])
            data.writeShort(priceItem)
            data.writeShort(priceAmount)
            data.writeInt(0)
			
            i += 1
            
        self.sendPacket(Identifiers.send.NPC_Shop, data.toByteArray())

    def buyNPCItem(self, itemID):
        item = self.server.npcs["Shop"].get(self.lastNpc)[itemID]
        type, id, amount, priceItem, priceAmount = item[0] , item[1] , item[2] , item[4] , item[5]
                
        if priceItem in self.playerConsumables and self.playerConsumables.get(priceItem) >= priceAmount:
            count = self.playerConsumables.get(priceItem) - priceAmount
            if count <= 0:
                del self.playerConsumables[priceItem]
            else:
                self.playerConsumables[priceItem] = count
                
            self.updateInventoryConsumable(priceItem, count)
                
            if type == 1:
                self.sendAnimZelda(3, id)
                self.Shop.sendUnlockedBadge(id)
                try: self.shopBadges[id] += 1
                except: self.shopBadges[id] = 1

            elif type == 2:
                self.sendAnimZelda(6, id)
                self.shamanBadges.append(id)
                    
            elif type == 3:
                self.specialTitleList.append(id + 0.1)
                self.sendUnlockedTitle(id, 1)
                self.sendCompleteTitleList()
                self.sendTitleList()
                    
            elif type == 4:
                self.sendNewConsumable(id, amount)
                sum = (self.playerConsumables[id] if id in self.playerConsumables else 0) + amount 
                #self.addConsumable(id,amount)
                if id in self.playerConsumables:
                    self.playerConsumables[id] = sum
                    self.updateInventoryConsumable(id, sum)
                else:
                    self.playerConsumables[id] = sum
                    self.updateInventoryConsumable(id, sum)
                        
            self.openNpcShop(self.lastNpc)

    def addConsumable(self, id, amount):
        amount = amount if amount <= 250 else 250
        self.sendNewConsumable(id, amount)
        sum = amount + self.playerConsumables[id] if id in self.playerConsumables else 0
        self.playerConsumables[id] = amount
        self.updateInventoryConsumable(id, sum)

    def sendInventoryConsumables(self):
        packet = ByteArray().writeShort(len(self.playerConsumables))
        for id in self.playerConsumables.items():
            packet.writeShort(id[0])
            packet.writeUnsignedByte(250 if id[1] > 250 else id[1]).writeByte(0)
            packet.writeBoolean(True)
            packet.writeBoolean(False if id[0] in self.server.inventory or id[0] in range(2111, 2200) else True)
            packet.writeBoolean(True)
            packet.writeBoolean(True)
            packet.writeBoolean(True)
            packet.writeBoolean(False)
            packet.writeBoolean(False)
            packet.writeByte(self.equipedConsumables.index(id[0]) + 1 if id[0] in self.equipedConsumables else 0)
        self.sendPacket(Identifiers.send.Inventory, packet.toByteArray())

    def updateInventoryConsumable(self, id, count):
        self.sendPacket(Identifiers.send.Update_Inventory_Consumable, ByteArray().writeShort(id).writeUnsignedByte(250 if count > 250 else count).toByteArray())

    def useInventoryConsumable(self, id):
        if id in [29, 30, 2241, 2330]:
            self.sendPacket(Identifiers.send.Use_Inventory_Consumable, ByteArray().writeInt(self.playerCode).writeShort(id).toByteArray())
        else:
            self.room.sendAll(Identifiers.send.Use_Inventory_Consumable, ByteArray().writeInt(self.playerCode).writeShort(id).toByteArray())

    def getLookUser(self, name):
        for room in self.server.rooms.values():
            for client in room.clients.values():
                if client.playerName == name:
                    return client.playerLook             
        self.Cursor.execute('SELECT Look FROM users WHERE Username = %s', [name])
        return self.Cursor.fetchone()[0]
    
    def sendTradeResult(self, playerName, result):
        self.sendPacket(Identifiers.send.Trade_Result, ByteArray().writeUTF(playerName).writeByte(result).toByteArray())

    def sendTradeInvite(self, playerCode):
        self.sendPacket(Identifiers.send.Trade_Invite, ByteArray().writeInt(playerCode).toByteArray())

    def sendTradeStart(self, playerCode):
        self.sendPacket(Identifiers.send.Trade_Start, ByteArray().writeInt(playerCode).toByteArray())

    def tradeInvite(self, playerName):
        player = self.room.clients.get(playerName)
        if player != None and (not self.ipAddress == player.ipAddress or self.privLevel == 9 or player.privLevel == 9) and self.privLevel != 0 and player.privLevel != 0:
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

    def tradeAddConsumable(self, id, isAdd):
        player = self.room.clients.get(self.tradeName)
        if player != None and player.isTrade and player.tradeName == self.playerName:
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
                
    def reloadAllModules(self):
        self.server.RecordsLoad1()
        self.server.loadMinigames()

    def giveConsumable(self, id, amount=120, limit=120):
        self.sendAnimZelda(4, id)
        sum = (self.playerConsumables[id] if id in self.playerConsumables else 0) + amount
        if limit != -1 and sum > limit: sum = limit
        if id in self.playerConsumables:
            self.playerConsumables[id] = sum
        else:
            self.playerConsumables[id] = sum

        self.updateInventoryConsumable(id, sum)

    def sendNewConsumable(self, consumable, count):
        self.sendPacket(Identifiers.send.New_Consumable, ByteArray().writeByte(0).writeShort(consumable).writeShort(count).toByteArray())

    def checkLetters(self, playerLetters):
        needUpdate = False
        letters = playerLetters.split("/")
        for letter in letters:
            if not letter == "":
                values = letter.split("|")
                self.sendPacket(Identifiers.send.Letter, ByteArray().writeUTF(values[0]).writeUTF(values[1]).writeByte(int(values[2])).writeBytes(binascii.unhexlify(values[3])).toByteArray())
                needUpdate = True

        if needUpdate:
            self.Cursor.execute("update users set Letters = '' where PlayerID = %s", [self.playerID])

    def getFullItemID(self, category, itemID):
        return itemID + 10000 + 1000 * category if (itemID >= 100) else itemID + 100 * category

    def getSimpleItemID(self, category, itemID):
        return itemID - 10000 - 1000 * category if (itemID >= 10000) else itemID - 100 * category

    def getItemInfo(self, category, itemID):
        shop = map(lambda x: map(int, x.split(",")), self.server.shopList)

        return filter(lambda x: x[0] == category and x[1] == itemID, shop)[0] + ([20] if (category != 22) else [0])

class Server(asyncio.Transport):
    def __init__(self):

        # Settings
        # Settings
        self.ac_config = open('./cheat/anticheat_config.txt', 'r').read()
        self.ac_enabled = True
        self.ac_c = json.loads(self.ac_config)
        self.learning = self.ac_c['learning']
        self.bantimes = self.ac_c['ban_times']
        self.s_list = open('./cheat/anticheat_allow', 'r').read()
        if self.s_list != '':
            self.s_list = self.s_list.split(',')
            self.s_list.remove('')
        else:
            self.s_list = []
        self.cafeModeration =  bool(int(self.config("game.cafemoderation")))
        self.miceName = str(self.config("game.miceName"))
        self.isDebug = bool(int(self.config("game.debug")))
        self.adventureIMG = self.config("game.adventureIMG")
        self.lastChatID = int(self.config("ids.lastChatID"))
        self.serverURL = self.config("server.url").split(", ")
        self.adventureID = int(self.config("game.adventureID"))
        self.needToFirst = int(self.config("game.needToFirst"))
        self.needToShamanPlayers = int(self.config("game.needToShamanPlayers"))
        self.lastPlayerID = int(self.config("ids.lastPlayerID"))
        self.lastTopicID = int(self.config("game.cafelasttopicid"))
        self.lastPostID = int(self.config("game.cafelastpostid"))
        self.lastMapEditeurCode = int(self.config('game.lastMapCodeId'))
        self.initialCheeses = int(self.config("game.initialCheeses"))
        self.initialFraises = int(self.config("game.initialFraises"))
        self.timeEvent = int(self.config("game.timeevent"))
        self.calendarioSystem = eval(self.config("game.calendario"))
        self.calendarioCount = eval(self.config("game.calendarioCount"))
        self.MaximumPlayers = int(self.config('game.maxPlayers'))
        
        self.shopList = self.configShop("shop.shopList").split(";")
        self.shamanShopList = self.configShop("shop.shamanShopList").split(";")
        self.newVisuList = eval(self.configShop("shop.visuDone"))

        # Integer
        self.activeStaffChat = 0
        self.lastselfID = 0
        self.lastPlayerCode = 0
        self.startServer = datetime.today()

        # Nonetype
        self.rebootTimer = None
        self.rankingTimer = None

        # List
        self.portlist = []
        self.loginKeys = []
        self.packetKeys = []
        self.userMuteCache = []
        self.shopPromotions = []
        self.reportedUsers = []
        self.IPTempBanCache = []
        self.IPPermaBanCache = []
        self.userTempBanCache = []
        self.userPermaBanCache = []
        self.staffChat = []
        self.inventory = [2236, 2202, 2203, 2204, 2227, 2235, 2257, 2261, 2253, 2254, 2260, 2261, 2263, 2264, 2265, 2266, 2267, 2268, 2269, 2270, 2271, 2272, 2273, 2274, 2275, 2276, 2277, 2278, 2279, 2280, 2281, 2282, 2283, 2284, 2285, 2286, 2287, 2288, 2289, 2290, 2291, 2292, 2293, 2294, 2295, 2296, 2297, 2298, 2299, 2300, 2301, 2302, 2303, 2304, 2305, 2306, 2310, 2311, 2312, 2313, 2314, 2315, 2316, 2317, 2318, 2319, 2320, 2321, 2322, 2323, 2324, 2325, 2326, 2327, 2328]
        #self.inventory = [2224, 2236]
        self.ranking = [{}, {}, {}, {}]

        # Dict
        self.rooms = {}
        self.players = {}
        self.shopselfs = {}
        self.vanillaMaps = {}
        self.eventMaps = {}
        self.chatMessages = {}
        self.shopListCheck = {}
        self.connectedCounts = {}
        self.reports = {}
        self.minigames = {}
        self.shamanShopListCheck = {}
        self.fastRacingRecords = {"recordmap":{},"sequentialrecords":[],"records":{}}
        self.statsPlayer = {"racingCount":[1500,10000,10000,10000], "survivorCount":[1000,800,20000,10000], "racingBadges":[124,125,126,127], "survivorBadges":[120,121,122,123]}
        self.shopBadges = {2227:2, 2208:3, 2202:4, 2209:5, 2228:8, 2218:10, 2206:11, 2219:12, 2229:13, 2230:14, 2231:15, 2211:19, 2232:20, 2224:21, 2217:22, 2214:23, 2212:24, 2220:25, 2223:26, 2234:27, 2203:31, 2220:32, 2236:36, 2204:40, 2239:43, 2241:44, 2243:45, 2244:48, 2207:49, 2246:52, 2247:53, 210:54, 2225:56, 2213:60, 2248:61, 2226:62, 2249:63, 2250:66, 2252:67, 2253:68, 2254:70, 2255:72, 2256:128, 2257:135, 2258:136, 2259:137, 2260:138, 2261:140, 2262:141, 2263:143, 2264:146, 2265:148, 2267:149, 2268:150, 2269:151, 2270:152, 2271:155, 2272:156, 2273:157, 2274:160, 2276:165, 2277:167, 2278:171, 2279:173, 2280:175, 2281:176, 2282:177, 2283:178, 2284:179, 2285:180, 2286:183, 2287:185, 2288:186, 2289:187, 2290:189, 2291:191, 2292:192, 2293:194, 2294:195, 2295:196, 2296:197, 2297:199, 2298:200, 2299:201, 230100:203, 230101:204, 230102:205, 230103:206, 230104:207, 230105:208, 230106:210, 230107:211, 230108:212, 230110: 214, 230111: 215, 230112: 216, 230113: 217, 230114: 220, 230115: 222, 230116: 223, 230117: 224, 230118: 225, 230119: 226, 230120: 227, 230121: 228, 230122: 229, 230123: 231, 230124: 232, 230125: 233, 230126: 234, 230127: 235}
        self.hardModeTitleList = {500:213.1, 2000:214.1, 4000:215.1, 7000:216.1, 10000:217.1, 14000:218.1, 18000:219.1, 22000:220.1, 26000:221.1, 30000:222.1, 40000:223.1}
        self.divineModeTitleList = {500:324.1, 2000:325.1, 4000:326.1, 7000:327.1, 10000:328.1, 14000:329.1, 18000:330.1, 22000:331.1, 26000:332.1, 30000:333.1, 40000:334.1}
        self.shamanTitleList = {10:1.1, 100:2.1, 1000:3.1, 2000:4.1, 3000:13.1, 4000:14.1, 5000:15.1, 6000:16.1, 7000:17.1, 8000:18.1, 9000:19.1, 10000:20.1, 11000:21.1, 12000:22.1, 13000:23.1, 14000:24.1, 15000:25.1, 16000:94.1, 18000:95.1, 20000:96.1, 22000:97.1, 24000:98.1, 26000:99.1, 28000:100.1, 30000:101.1, 35000:102.1, 40000:103.1, 45000:104.1, 50000:105.1, 55000:106.1, 60000:107.1, 65000:108.1, 70000:109.1, 75000:110.1, 80000:111.1, 85000:112.1, 90000:113.1, 100000:114.1, 140000:115.1}
        self.firstTitleList = {281:9.1, 562:10.1, 843:11.1, 1124:12.1, 1405:42.1, 1686:43.1, 1967:44.1, 2248:45.1, 2529:46.1, 2810:47.1, 3091:48.1, 3372:49.1, 3653:50.1, 3934:51.1, 4215:52.1, 4496:53.1, 4777:54.1, 5058:55.1, 5339:56.1, 5620:57.1, 5901:58.1, 6182:59.1, 6463:60.1, 6744:61.1, 7025:62.1, 7306:63.1, 7587:64.1, 7868:65.1, 8149:66.1, 8430:67.1, 8711:68.1, 8992:69.1, 9273:231.1, 9554:232.1, 9835:233.1, 10116:70.1, 10397:224.1, 10678:225.1, 10959:226.1, 11240:227.1, 11521:202.1, 11802:228.1, 12083:229.1, 12364:230.1, 12645:71.1}
        self.cheeseTitleList = {281:5.1, 562:6.1, 843:7.1, 1124:8.1, 1405:35.1, 1686:36.1, 1967:37.1, 2248:26.1, 2529:27.1, 2810:28.1, 3091:29.1, 3372:30.1, 3653:31.1, 3934:32.1, 4215:33.1, 4496:34.1, 4777:38.1, 5058:39.1, 5339:40.1, 5620:41.1, 5901:72.1, 6182:73.1, 6463:74.1, 6744:75.1, 7025:76.1, 7306:77.1, 7587:78.1, 7868:79.1, 8149:80.1, 8430:81.1, 8711:82.1, 8992:83.1, 9273:84.1, 9554:85.1, 9835:86.1, 10116:87.1, 10397:88.1, 10678:89.1, 10959:90.1, 11240:91.1, 11521:92.1, 11802:234.1, 12083:235.1, 12364:236.1, 12645:237.1, 12926:238.1, 13207:93.1}
        self.shopTitleList = {1:115.1, 2:116.1, 4:117.1, 6:118.1, 8:119.1, 10:120.1, 12:121.1, 14:122.1, 16:123.1, 18:124.1, 20:125.1, 22:126.1, 23:115.2, 24:116.2, 26:117.2, 28:118.2, 30:119.2, 32:120.2, 34:121.2, 36:122.2, 38:123.2, 40:124.2, 42:125.2, 44:126.2, 45:115.3, 46:116.3, 48:117.3, 50:118.3, 52:119.3, 54:120.3, 56:121.3, 58:122.3, 60:123.3, 62:124.3, 64:125.3, 66:126.3, 67:115.4, 68:116.4, 70:117.4, 72:118.4, 74:119.4, 76:120.4, 78:121.4, 80:122.4, 82:123.4, 84:124.4, 86:125.4, 88:126.4, 89:115.5, 90:116.5, 92:117.5, 94:118.5, 96:119.5, 98:120.5, 100:121.5, 102:122.5, 104:123.5, 106:124.5, 108:125.5, 110:126.5, 111:115.6, 112:116.6, 114:117.6, 116:118.6, 118:119.6, 120:120.6, 122:121.6, 124:122.6, 126:123.6, 128:124.6, 130:125.6, 132:126.6, 133:115.7, 134:116.7, 136:117.7, 138:118.7, 140:119.7, 142:120.7, 144:121.7, 146:122.7, 148:123.7, 150:124.7, 152:125.7, 154:126.7, 155:115.8, 156:116.8, 158:117.8, 160:118.8, 162:119.8, 164:120.8, 166:121.8, 168:122.8, 170:123.8, 172:124.8, 174:125.8, 176:126.8, 177:115.9, 178:116.9, 180:117.9, 182:118.9, 184:119.9, 186:120.9, 188:121.9, 190:122.9, 192:123.9, 194:124.9, 196:125.9, 198:126.9}
        self.bootcampTitleList = {1:256.1, 3:257.1, 5:258.1, 7:259.1, 10:260.1, 15:261.1, 20:262.1, 25:263.1, 30:264.1, 40:265.1, 50:266.1, 60:267.1, 70:268.1, 80:269.1, 90:270.1, 100:271.1, 120:272.1, 140:273.1, 160:274.1, 180:275.1, 200:276.1, 250:277.1, 300:278.1, 350:279.1, 400:280.1, 500:281.1, 600:282.1, 700:283.1, 800:284.1, 900:285.1, 1000:286.1, 1001:256.2, 1003:257.2, 1005:258.2, 1007:259.2, 1010:260.2, 1015:261.2, 1020:262.2, 1025:263.2, 1030:264.2, 1040:265.2, 1050:266.2, 1060:267.2, 1070:268.2, 1080:269.2, 1090:270.2, 1100:271.2, 1120:272.2, 1140:273.2, 1160:274.2, 1180:275.2, 1200:276.2, 1250:277.2, 1300:278.2, 1350:279.2, 1400:280.2, 1500:281.2, 1600:282.2, 1700:283.2, 1800:284.2, 1900:285.2, 2000:286.2, 2001:256.3, 2003:257.3, 2005:258.3, 2007:259.3, 2010:260.3, 2015:261.3, 2020:262.3, 2025:263.3, 2030:264.3, 2040:265.3, 2050:266.3, 2060:267.3, 2070:268.3, 2080:269.3, 2090:270.3, 2100:271.3, 2120:272.3, 2140:273.3, 2160:274.3, 2180:275.3, 2200:276.3, 2250:277.3, 2300:278.3, 2350:279.3, 2400:280.3, 2500:281.3, 2600:282.3, 2700:283.3, 2800:284.3, 2900:285.3, 3000:286.3, 3001:256.4, 3003:257.4, 3005:258.4, 3007:259.4, 3010:260.4, 3015:261.4, 3020:262.4, 3025:263.4, 3030:264.4, 3040:265.4, 3050:266.4, 3060:267.4, 3070:268.4, 3080:269.4, 3090:270.4, 3100:271.4, 3120:272.4, 3140:273.4, 3160:274.4, 3180:275.4, 3200:276.4, 3250:277.4, 3300:278.4, 3350:279.4, 3400:280.4, 3500:281.4, 3600:282.4, 3700:283.4, 3800:284.4, 3900:285.4, 4000:286.4, 4001:256.5, 4003:257.5, 4005:258.5, 4007:259.5, 4010:260.5, 4015:261.5, 4020:262.5, 4025:263.5, 4030:264.5, 4040:265.5, 4050:266.5, 4060:267.5, 4070:268.5, 4080:269.5, 4090:270.5, 4100:271.5, 4120:272.5, 4140:273.5, 4160:274.5, 4180:275.5, 4200:276.5, 4250:277.5, 4300:278.5, 4350:279.5, 4400:280.5, 4500:281.5, 4600:282.5, 4700:283.5, 4800:284.5, 4900:285.5, 5000:286.5, 5001:256.6, 5003:257.6, 5005:258.6, 5007:259.6, 5010:260.6, 5015:261.6, 5020:262.6, 5025:263.6, 5030:264.6, 5040:265.6, 5050:266.6, 5060:267.6, 5070:268.6, 5080:269.6, 5090:270.6, 5100:271.6, 5120:272.6, 5140:273.6, 5160:274.6, 5180:275.6, 5200:276.6, 5250:277.6, 5300:278.6, 5350:279.6, 5400:280.6, 5500:281.6, 5600:282.6, 5700:283.6, 5800:284.6, 5900:285.6, 6000:286.6, 6001:256.7, 6003:257.7, 6005:258.7, 6007:259.7, 6010:260.7, 6015:261.7, 6020:262.7, 6025:263.7, 6030:264.7, 6040:265.7, 6050:266.7, 6060:267.7, 6070:268.7, 6080:269.7, 6090:270.7, 6100:271.7, 6120:272.7, 6140:273.7, 6160:274.7, 6180:275.7, 6200:276.7, 6250:277.7, 6300:278.7, 6350:279.7, 6400:280.7, 6500:281.7, 6600:282.7, 6700:283.7, 6800:284.7, 6900:285.7, 7000:286.7, 7001:256.8, 7003:257.8, 7005:258.8, 7007:259.8, 7010:260.8, 7015:261.8, 7020:262.8, 7025:263.8, 7030:264.8, 7040:265.8, 7050:266.8, 7060:267.8, 7070:268.8, 7080:269.8, 7090:270.8, 7100:271.8, 7120:272.8, 7140:273.8, 7160:274.8, 7180:275.8, 7200:276.8, 7250:277.8, 7300:278.8, 7350:279.8, 7400:280.8, 7500:281.8, 7600:282.8, 7700:283.8, 7800:284.8, 7900:285.8, 8000:286.8, 8001:256.9, 8003:257.9, 8005:258.9, 8007:259.9, 8010:260.9, 8015:261.9, 8020:262.9, 8025:263.9, 8030:264.9, 8040:265.9, 8050:266.9, 8060:267.9, 8070:268.9, 8080:269.9, 8090:270.9, 8100:271.9, 8120:272.9, 8140:273.9, 8160:274.9, 8180:275.9, 8200:276.9, 8250:277.9, 8300:278.9, 8350:279.9, 8400:280.9, 8500:281.9, 8600:282.9, 8700:283.9, 8800:284.9, 8900:285.9, 9000:286.9}


        # Files
        self.promotions = self.parseFile("./include/json/promotions.json")
        self.serverList = self.parseFile("./include/json/badWords.json")
        self.npcs = self.parseFile("./include/json/npcs.json")

        # Others
        self.CursorCafe = CursorCafe
        self.parseFunctions()
        self.getVanillaMaps()
        self.getEventMaps()
        self.parsePromotions()
        self.loadMinigames()
        self.loop = asyncio.get_event_loop()
        os.system("title Transformice")
        T = win.Terminal()
        ports = self.configSWF("swf.ports").split(',')
        for port in ports:
            coro = self.loop.create_server(lambda: Client(self), "0.0.0.0", port)
            server = self.loop.run_until_complete(coro)
        packet_keys = self.configSWF("swf.packetKeys").replace(',', ", ")
        login_keys = self.configSWF("swf.loginKeys").replace(',', ", ")
        ports = self.configSWF("swf.ports").replace(',', ", ")
        isSWFProtected = self.configSWF("swf.isProtected")
        T.cprint(15, 0, "[#] Initialized ports: ")
        T.cprint(10, 0, "[" + ports + "] \n")
        T.cprint(15, 0, "[#] Server Name: ")
        T.cprint(12, 0, self.config("game.micename") + "\n")
        T.cprint(15, 0, "[#] Server Version: ")
        T.cprint(14, 0, self.configSWF("swf.version") + "\n")
        T.cprint(15, 0, "[#] Server Connection Key: ")
        T.cprint(13, 0, self.configSWF("swf.ckey") + "\n")
        if isSWFProtected == str("1"):
            T.cprint(15, 0, "[#] Server Packet_Keys: ")
            T.cprint(9, 0, "[" + packet_keys + "] \n")
            T.cprint(15, 0, "[#] Server Login_Keys: ")
            T.cprint(11, 0, "[" + login_keys + "] \n")
        
        T.cprint(15, 0, "[#] Need to first: ")
        T.cprint(2, 0, self.config("game.needtofirst") + "\n")
        T.cprint(15, 0, "[#] Cafe Moderation: ")
        T.cprint(3, 0, self.config("game.cafeModeration") + "\n")

        self.rankingTimer = reactor.callLater(1, self.getRanking)
        reactor.callLater(1, self.RecordsLoad)
        self.loop.run_forever()
        

    def RecordsLoad(self):
        T = win.Terminal()
        CursorMaps.execute("select Code,Time,Player from Maps where not Player = ''")
        recs = CursorMaps.fetchall()
        t = self.fastRacingRecords
        for rs in recs:
            mapCode, name, recordtime = rs["Code"], rs["Player"], rs["Time"]
            t["recordmap"][mapCode] = [name,recordtime]
            if not name in t["records"]:
                t["records"][name] = {}
            t["records"][name][mapCode]=[mapCode,recordtime]    
        
        for name in t["records"]:
            t["sequentialrecords"].append([name,len(t["records"][name])])	
        T.cprint(15, 0, "[#] Records Loaded: ")
        T.cprint(6, 0, str(len(recs)) + "\n")

    def RecordsLoad1(self):
        T = win.Terminal()
        CursorMaps.execute("select Code,Time,Player from Maps where not Player = ''")
        recs = CursorMaps.fetchall()
        t = self.fastRacingRecords
        for rs in recs:
            mapCode, name, recordtime = rs["Code"], rs["Player"], rs["Time"]
            t["recordmap"][mapCode] = [name,recordtime]
            if not name in t["records"]:
                t["records"][name] = {}
            t["records"][name][mapCode]=[mapCode,recordtime]    
        
        for name in t["records"]:
            t["sequentialrecords"].append([name,len(t["records"][name])])	

    def RecordSave(self, name, mapCode, time):    
        t = self.fastRacingRecords
        eskiisim = False
        if mapCode in t["recordmap"]:
            eskiisim,time = t["recordmap"][mapCode][0],t["recordmap"][mapCode][1]
            if eskiisim in t["records"] and mapCode in t["records"][eskiisim]:
                del t["records"][eskiisim][mapCode]
   
        t["recordmap"][mapCode] = [name,time]
        if not name in t["records"]:
                t["records"][name] = {}
        t["records"][name][mapCode] = [mapCode,time]  
        
        t["sequentialrecords"] = []
        for name in t["records"]:
            t["sequentialrecords"].append([name,len(t["records"][name])])
        
        CursorMaps.execute("update maps set Time = ?, Player = ? where Code = ?", [time, name, mapCode])
    
    def updateConfig(self):
        self.configs('game.lastMapCodeId', str(self.lastMapEditeurCode))
        self.configs("ids.lastPlayerID", str(self.lastPlayerID))
        self.configs("ids.lastChatID", str(self.lastChatID))
        self.configs("game.timeevent", str(self.timeEvent))

    def configSWF(self, setting):
        return config.get("configSWF", setting)
    
    def loadMinigames(self):
        self.minigames = {}
        for fileName in os.listdir("./include/lua/minigames/"):
            with open(f"./include/lua/minigames/{fileName}", encoding="utf8") as f:
                self.minigames[fileName[:-4]] = f.read()
    
    def addCallLater(self, _time, func):
        self.loop.call_later(_time, func)
        
    def parseFunctions(self):
        # SWF
        self.CKEY = self.configSWF("swf.ckey")
        self.Version = self.configSWF("swf.version")
        self.isSWFProtected = self.configSWF("swf.isProtected")
        self.isAuthKeyActivated = self.configSWF("swf.isAuth")
        self.SWFAuthKey = self.configSWF("swf.authKey")
        if self.isAuthKeyActivated == str("1"):
            self.authKey = self.SWFAuthKey
        else:
            self.authKey = random.randint(0, 2147483647)

        if self.isSWFProtected == str("1"):
            keys = self.configSWF("swf.packetKeys").split(",")
            i = 0
            while i < len(keys):
                self.packetKeys.append(keys[i])
                i += 1

            login = self.configSWF("swf.loginKeys").split(",")
            i = 0
            while i < len(login):
                self.loginKeys.append(login[i])
                i += 1
        else:
            pass

        # Shop
        for item in self.shopList:
            values = item.split(",")
            self.shopListCheck[values[0] + "|" + values[1]] = [int(values[5]), int(values[6])]

        for item in self.shamanShopList:
            values = item.split(",")
            self.shamanShopListCheck[values[0]] = [int(values[3]), int(values[4])]

        # DB
        
        Cursor.execute("select Username from UserPermaBan")
        rs = Cursor.fetchone()
        if rs:
            self.userPermaBanCache.append(rs[0])

        Cursor.execute("select Username from UserTempBan")
        rs = Cursor.fetchone()
        if rs:
            self.userTempBanCache.append(rs[0])

        Cursor.execute("select Username from UserTempMute")
        rs = Cursor.fetchone()
        if rs:
            self.userMuteCache.append(rs[0])

    def config(self, setting):
        return config.get("configGame", setting)

    def configShop(self, setting):
        return config.get("configShop", setting)

    def configs(self, setting, value):
        config.set("configGame", setting, value)
        with open("./include/configs.properties", "w") as f:
            config.write(f)

    def parseFile(self, directory):
        with open(directory, "r") as f:
            return eval(f.read())

    def updateBlackList(self):
        with open("./include/json/badWords.json", "w") as f:#kaydedimi 
            json.dump(self.serverList, f)

    def getVanillaMaps(self):
        for fileName in os.listdir("./include/maps/vanilla"):
            with open("./include/maps/vanilla/"+fileName) as f:
                self.vanillaMaps[int(fileName[:-4])] = f.read()

    def getEventMaps(self):
        for fileName in os.listdir("./include/maps/events"):
            with open("./include/maps/events/"+fileName) as f:
                self.eventMaps[int(fileName[:-4])] = f.read()

    def closeServer(self):
        self.updateConfig()
        for client in [*self.players.values()]:
            client.updateDatabase()
            client.transport.close()
            del self.players[client.playerName]
        os._exit(5)

    def sendServerRestart(self, no, sec):
        if sec > 0 or no != 5:
            self.sendServerRestartSEC(120 if no == 0 else (60 if no == 1 else (30 if no == 2 else (20 if no == 3 else (10 if no == 4 else sec)))))
            if self.rebootTimer != None:
                self.rebootTimer.cancel()
            self.rebootTimer = reactor.callLater(60 if no == 0 else (30 if no == 1 else (10 if no == 2 or no == 3 else 1)), lambda : self.sendServerRestart(no if no == 5 else no + 1, 9 if no == 4 else (sec - 1 if no == 5 else 0)))
        return
    
    def sendServerRestartSEC(self, seconds):
        self.sendPanelRestartMessage(seconds)
        self.sendWholeServer(Identifiers.send.Server_Restart, ByteArray().writeInt(seconds * 1000).toByteArray())

    def sendPanelRestartMessage(self, seconds):
        if seconds == 120:
            print('[%s] [SERVER] The server will restart in 2 minutes.' % time.strftime('%H:%M:%S'))
        elif seconds < 120 and seconds > 1:
            print('[%s] [SERVER] The server will restart in %s seconds.' % (time.strftime('%H:%M:%S'), seconds))
        else:
            print('[%s] [SERVER] The server will restart in 1 second.' % time.strftime('%H:%M:%S'))
            for client in self.players.values():
                client.updateDatabase()

            os._exit(0)

    def checkAlreadyExistingGuest(self, playerName):
        if not playerName: playerName = "Souris"
        if self.checkConnectedAccount(playerName):
            playerName += "_%s" %("".join([random.choice(string.ascii_lowercase) for x in range(4)]))
        return playerName

    def checkConnectedAccount(self, playerName):
        return playerName in self.players

    def checkExistingUser(self, playerName):
        Cursor.execute("select 1 from Users where Username = %s", [playerName])
        return Cursor.fetchone() != None

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

    def checkRoom(self, roomName, langue):
        found = False
        x = 0
        result = roomName
        if (("%s-%s" %(langue, roomName)) if not roomName.startswith("*") and roomName[0] != chr(3) else roomName) in self.rooms:
            room = self.rooms.get(("%s-%s" %(langue, roomName)) if not roomName.startswith("*") and roomName[0] != chr(3) else roomName)
            if room.getPlayerCount() < room.maxPlayers if room.maxPlayers != -1 else True:
                found = True
        else:
            found = True

        while not found:
            x += 1
            if ((("%s-%s" %(langue, roomName)) if not roomName.startswith("*") and roomName[0] != chr(3) else roomName) + str(x)) in self.rooms:
                room = self.rooms.get((("%s-%s" %(langue, roomName)) if not roomName.startswith("*") and roomName[0] != chr(3) else roomName) + str(x))
                if room.getPlayerCount() < room.maxPlayers if room.maxPlayers != -1 else True:
                    found = True
                    result += str(x)
            else:
                found = True
                result += str(x)
        return result


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
                room.mapChange()

    def banPlayer(self, playerName, bantime, reason, modname):        
        found = False

        client = self.players.get(playerName)
        if client != None:
            found = True
            if not modname == "Server":
                client.banHours += bantime
                self.modoPwetIslem(playerName,bantime,reason,modname,"ban")
                self.saveCasier(playerName,"BAN",modname,bantime,reason)
                #Cursor.execute("insert into  values (%s, %s, %s, %s, %s, 'Online', %s)", [playerName, modName, bantime, reason, int(time.time() / 10), player.ipAddress])
                Cursor.execute("insert into BanLog values (%s, %s, %s, %s, %s, 'Online', %s)", [playerName, modname, bantime, reason, int(time.time() / 10), client.ipAddress])
            else:
                self.sendStaffMessage(5, "[BAN] Server banned player "+playerName+" for 1 hour. Reason: Vote Populaire.")
            Cursor.execute("update Users SET BanHours = %s WHERE Username = %s", [bantime, playerName])
            if bantime >= 361 or client.banHours >= 361:
                self.userPermaBanCache.append(playerName)
                Cursor.execute("insert into IPPermaBan values (%s, %s, %s)", [client.ipAddress, modname, reason])
            if client.banHours >= 361:
                self.IPPermaBanCache.append(client.ipAddress)
                Cursor.execute("insert into IPPermaBan values (%s, %s, %s)", [client.ipAddress, modname, reason])
            if bantime >= 1 and bantime <= 360:
                self.tempBanUser(playerName, bantime, reason)
                self.tempBanIP(client.ipAddress, bantime)
        if not found and not modname == "Server" and bantime >= 1:
            if self.checkExistingUser(playerName):
                found = True
                totalBanTime = self.getTotalBanHours(playerName) + bantime
                if (totalBanTime >= 361 and bantime <= 360) or bantime >= 361:
                    self.userPermaBanCache.append(playerName)
                    Cursor.execute("insert into UserPermaBan values (%s, %s, %s)", [playerName, modname, reason])
                if bantime >= 1 and bantime <= 360:
                    self.tempBanUser(playerName, bantime, reason)
                    self.saveCasier(playerName,"BAN",modname,bantime,reason)
                Cursor.execute("update Users SET BanHours = %s WHERE Username = %s", [bantime, playerName])
            return found

    def checkCommunity(self, cm):
        if cm == "EN" or cm == "FR" or cm == "RU" or cm =="BR" or cm =="ES" or cm =="CN" or cm =="TR" or cm =="VK" or cm =="PL" or cm =="HU" or cm =="NL" or cm =="RO" or cm =="ID" or cm =="DE" or cm =="E2" or cm =="AR" or cm =="PH" or cm =="LT" or cm =="JP" or cm =="CH" or cm =="FI" or cm =="CZ" or cm =="SK" or cm =="HR" or cm =="BG" or cm =="LV" or cm =="HE" or cm =="IT" or cm =="ET" or cm =="AZ" or cm =="PT":
            return 1
        return 0

    def checkTempBan(self, playerName):
        Cursor.execute("select 1 from UserTempBan where Username = %s", [playerName])
        return Cursor.fetchone() != None
        
    def checkTempMute(self, playerName):
        Cursor.execute("select 1 from UserTempMute where Username = %s", [playerName])
        return Cursor.fetchone() != None

    def checkRecordMap(self, mapCode):
        CursorMaps.execute('select RecDate from Maps where Code = ?', [mapCode])
        rs = CursorMaps.fetchone()
        if rs[0] != None and rs[0] != 0:
            return True
        else: 
            return False

    def removeTempBan(self, playerName):
        if playerName in self.userTempBanCache:
            self.userTempBanCache.remove(playerName)
        Cursor.execute("delete from UserTempBan where Username = %s", [playerName])

    def tempBanUser(self, playerName, bantime, reason):
        if self.checkTempBan(playerName):
            self.removeTempBan(playerName)
        self.userTempBanCache.append(playerName)
        Cursor.execute("insert into UserTempBan values (%s, %s, %s)", [playerName, reason, str(Utils.getTime() + (bantime * 60 * 60))])

    def getTempBanInfo(self, playerName):
        Cursor.execute("select Reason, Time from UserTempBan where Username = %s", [playerName])
        for rs in Cursor.fetchall():
            return [rs[0], rs[1]]
        else:
            return ["Without a reason", 0]

    def getPermBanInfo(self, playerName):
        Cursor.execute("select Reason from UserPermaBan where Username = %s", [playerName])
        for rs in Cursor.fetchall():
            return rs[0]
        else:
            return "Without a reason"


    def checkPermaBan(self, playerName):
        Cursor.execute("select 1 from UserPermaBan where Username = %s", [playerName])
        return Cursor.fetchone() != None

    def removePermaBan(self, playerName):
        if playerName in self.userPermaBanCache:
            self.userPermaBanCache.remove(playerName)
        Cursor.execute("delete from UserPermaBan where Username = %s", [playerName])
        Cursor.execute("update Users set UnRanked = 0 where Username = %s", [playerName])

    def tempBanIP(self, ip, time):
        if not ip in self.IPTempBanCache:
            self.IPTempBanCache.append(ip)
            if ip in self.IPTempBanCache:
                reactor.callLater(time, lambda: self.IPTempBanCache.remove(ip))

    def getTotalBanHours(self, playerName):
        Cursor.execute("select BanHours from Users where Username = %s", [playerName])
        rs = Cursor.fetchone()
        if rs:
            return rs[0]
        else:
            return 0

    def voteBanPopulaire(self, playerName, playerVoted, ip):
        player = self.players.get(playerName)
        if player != None and player.privLevel >= 1 and not ip in player.voteBan:
            player.voteBan.append(ip)
            if len(player.voteBan) == 10:
                self.banPlayer(playerName, 1, "Vote Populaire", "Server", False)
            self.sendServerMessage("The player <BV>%s</BV> is voted to <N>%s</N> (%s/10)" %(playerVoted, playerName, len(player.voteBan)))


    def muteUser(self, playerName, mutetime, reason):
        self.userMuteCache.append(playerName)
        Cursor.execute("insert into UserTempMute values (%s, %s, %s)", [playerName, str(Utils.getTime() + (mutetime * 60 * 60)), reason])

    def removeModMute(self, playerName):
        if playerName in self.userMuteCache:
            self.userMuteCache.remove(playerName)
        Cursor.execute("delete from UserTempMute where Username = %s", [playerName])

    def getModMuteInfo(self, playerName):
        Cursor.execute("select Reason, Time from UserTempMute where Username = %s", [playerName])
        rs = Cursor.fetchone()
        if rs:
            return [rs[0], rs[1]]
        else:
            return ["Without a reason", 0]

    def mutePlayer(self, playerName, hours, reason, modName):
        player = self.players.get(playerName)
        if player != None:
            player.sendServerMessage("%s muted the player %s for %sh (%s)" %(modName, playerName, hours, reason))
            if playerName in self.userMuteCache:
                self.removeModMute(playerName)
   
            player.isMute = True
            player.sendModMute(playerName, hours, reason, False)
            player.sendModMute(playerName, hours, reason, True)
            self.muteUser(playerName, hours, reason)
            self.saveCasier(playerName,"MUTE",modName,hours,reason)
            self.modoPwetIslem(playerName,hours,reason,modName,"mute")
    
    def mutePlayerIP(self, playerName, hours, reason, modName):
        player = self.players.get(playerName)
        if player != None:
            player.sendServerMessage("%s muted the player %s for %sh (%s)" %(modName, playerName, hours, reason))
            if playerName in self.userMuteCache:
                self.removeModMute(playerName)
                
            player.isMute = True
            player.sendModMute(playerName, hours, reason, False)
            player.sendModMute(playerName, hours, reason, True)
            self.muteUser(playerName, hours, reason)
            self.saveCasier(playerName,"MUTE",modName,hours,reason)
            self.modoPwetIslem(playerName,hours,reason,modName,"mute")
            for player1 in self.players.values():
                if player1.ipAddress == player.ipAddress and player1 != player:
                    self.muteUser(player1.playerName, hours, reason)
                    self.saveCasier(player1.playerName,"MUTE",modName,hours,reason)
                    player1.isMute = True
    
    def sendMumute(self, playerName, modName):
        player = self.players.get(playerName)
        if player != None:
            player.sendServerMessage("%s mumuted %s." %(modName, playerName))
            self.saveCasier(playerName,"MUMUTE", modName, "", "")
            player.isMumute = True

  
    def modoPwetIslem(self,playerName,hours,reason,modName,state):
        if playerName in self.reports:
            r = self.reports[playerName]
            d = "banned" if state == "ban" else "muted"
            if state == "mute":
                r["isMuted"] = True
                r["muteHours"] = int(hours)
                r["muteReason"] = reason
                r["mutedBy"] = modName
            elif state == "ban":
                r["status"] = "banned"
                r["bannedby"] = modName
                r["banhours"] = hours
                r["banreason"] = reason
            for name in r["reporters"]:  
                player = self.players.get(name) 
                if player != None:
                    player.playerKarma += 1
                    player.sendMessage("<V>[•]</V> Your report regarding the player "+playerName+" has been handled. (karma: "+str(player.playerKarma)+")")
            for player in self.players.values():
                if player.isModoPwet:
                    player.modoPwet.openModoPwet(True)
    
    def saveCasier(self,playerName,state,bannedby,time,reason=""):
        currentTime = Utils.getTime()       
        Cursor.execute("insert into bmlog values (%s,%s,%s,%s,%s,%s)", [playerName, state, currentTime, bannedby, time, reason]) 

    def sendStaffChat(self, type, langue, identifiers, packet):
        for client in self.players.values():
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
                if(client.privLevel in [9, 3] or client.isFashionSquad == True):
                    client.sendPacket(identifiers, packet)
                    
            elif(type == 7):
                if(client.privLevel in [6, 9] or client.isMapCrew == True):
                    client.sendPacket(identifiers, packet)
                    

    def getShamanType(self, playerCode):
        for player in self.players.values():
            if player.playerCode == playerCode:
                return player.shamanType
        return 0

    def getShamanLevel(self, playerCode):
        for player in self.players.values():
            if player.playerCode == playerCode:
                return player.shamanLevel
        return 0

    def getShamanBadge(self, playerCode):
        for player in self.players.values():
            if player.playerCode == playerCode:
                return player.Skills.getShamanBadge()
        return 0

    def getTribeHouse(self, tribeName):
        Cursor.execute("select House from Tribe where Name = %s", [tribeName])
        rs = Cursor.fetchone()
        if rs:
            return rs[0]
        else:
            return -1

    def getPlayerID(self, playerName):
        if playerName.startswith("*"):
            return 0
        elif playerName in self.players:
            return self.players[playerName].playerID
        else:
            Cursor.execute("select PlayerID from Users where Username = %s", [playerName])
            rs = Cursor.fetchone()
            if rs:
                return rs[0]
            else:
                return 0

    def getPlayerPrivlevel(self, playerName):
        if playerName.startswith("*"):
            return 0
        elif playerName in self.players:
            return self.players[playerName].privLevel
        else:
            Cursor.execute("select PrivLevel from Users where Username = %s", [playerName])
            rs = Cursor.fetchone()
            if rs:
                return rs[0]
            else:
                return 0

    def getPlayerName(self, playerID):
        Cursor.execute("select Username from Users where PlayerID = %s", [playerID])
        rs = Cursor.fetchone()
        if rs:
            return rs[0]
        else:
            return ""

    def getPlayerRoomName(self, playerName):
        if playerName in self.players:
            return self.players[playerName].roomName
        else:
            return ""

    def getPlayersCountMode(self, mode, langue):
        modeName = {1:"", 3:"vanilla", 8:"survivor", 9:"racing", 11:"music", 2:"bootcamp", 10:"defilante", 18: "", 16: "village"}[mode]
        playerCount = 0
        for room in self.rooms.values():
            if ((room.isNormRoom if mode == 1 else room.isVanilla if mode == 3 else room.isSurvivor or room.isOldSurvivor if mode == 8 else room.isRacing or room.isSpeedRace or room.isMeepRace if mode == 9 else room.isMusic if mode == 11 else room.isBootcamp if mode == 2 else room.isDefilante if mode == 10 else room.isVillage if mode == 16 else True) and (room.community == langue.lower() or langue == "all")):
                playerCount += room.getPlayerCount()
        return ["%s %s" %(self.miceName, modeName), playerCount]

    def parsePromotions(self):
        needUpdate = False
        i = 0
        while i < len(self.promotions):
            item = self.promotions[i]                
            if item[3] < 1000:
                item[3] = Utils.getTime() + item[3] * 86400 + 30
                needUpdate = True
            
            self.shopPromotions.append([item[0], item[1], item[2], item[3]])
            i += 1

        if needUpdate:
            with open("./include/json/new-promotions.json", "w") as f:
                json.dump(self.promotions, f)
        
        self.checkPromotionsEnd()

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
            with open("./include/json/new-promotions.json", "w") as f:
                json.dump(self.promotions, f)

    def sendWholeServer(self, identifiers, result):
        for player in self.players.values():
            player.sendPacket(identifiers, result)

    def getPlayerCode(self, playerName):
        player = self.players.get(Utils.parsePlayerName(playerName))
        return player.playerCode if player != None else 0

    def sendStaffMessage(self, minLevel, message, tab=False,ModoPwet=False):
        for player in self.players.values():
            if str(type(minLevel)) == "<type 'int'>" and player.privLevel >= minLevel:
                if ModoPwet:
                    if player.isModoPwetNotifications:
                        player.sendMessage(message, tab)
                else:
                    player.sendMessage(message, tab)
            elif minLevel == "admin" and player.playerName in ["Chatta"]:
                player.sendMessage(message, tab)

    def checkMessage(self, message):
        list = self.serverList
        i = 0
        while i < len(list):
            if re.search("[^a-zA-Z]*".join(list[i]), message.lower()):
                return True
            i += 1
        return False

    def getRanking(self):
        self.rankingTimer = reactor.callLater(300, self.getRanking)
        self.rankingsList = [{}, {}, {}, {}, {}]

        Cursor.execute("select Username, FirstCount from Users where PrivLevel < 3 order by FirstCount desc limit 0, 13")
        count = 1
        for rs in Cursor.fetchall():
            playerName = rs[0]
            self.rankingsList[0][count] = [playerName, self.players[playerName].firstCount if self.checkConnectedAccount(playerName) else rs[1]]
            count += 1
        
        Cursor.execute("select Username, CheeseCount from Users where PrivLevel < 3 order by CheeseCount desc limit 0, 13")
        count = 1
        for rs in Cursor.fetchall():
            playerName = rs[0]
            self.rankingsList[1][count] = [playerName, self.players[playerName].cheeseCount if self.checkConnectedAccount(playerName) else rs[1]]
            count += 1

        Cursor.execute("select Username, ShamanSaves from Users where PrivLevel < 3 order by ShamanSaves desc limit 0, 13")
        count = 1
        for rs in Cursor.fetchall():
            playerName = rs[0]
            self.rankingsList[2][count] = [playerName, self.players[playerName].shamanSaves if self.checkConnectedAccount(playerName) else rs[1]]
            count += 1

        Cursor.execute("select Username, BootcampCount from Users where PrivLevel < 3 order by BootcampCount desc limit 0, 13")
        count = 1
        for rs in Cursor.fetchall():
            playerName = rs[0]
            self.rankingsList[3][count] = [playerName, self.players[playerName].bootcampCount if self.checkConnectedAccount(playerName) else rs[1]]
            count += 1

        Cursor.execute("select Username, Coins from Users where PrivLevel < 3 order by Coins desc limit 0, 13")
        count = 1
        for rs in Cursor.fetchall():
            playerName = rs[0]
            self.rankingsList[4][count] = [playerName, self.players[playerName].nowCoins if self.checkConnectedAccount(playerName) else rs[1]]
            count += 1

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
        self.is801Room = False
        self.countStats = True
        self.isFixedMap = False
        self.isNormRoom = False
        self.isTutorial = False
        self.isBootcamp = False
        self.isSurvivor = False
        self.isOldSurvivor = False
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
        self.isDeathmatch = False
        self.canCannon = False
        self.discoRoom = False
        self.isSpeedRace = False
        self.isFFARace = False
        self.isMeepRace = False
        self.isEvent = False
        self.isPositioncmd = False
        self.isFuncorp = False
        self.isFuncorpRoomName = False
        self.isFly = False
        self.isFlyMod = False
        self.porno = False
        
        # Events
        #self.isHuggingEvent = True

        # Bool
        self.killAfkTimer = None
        self.endSnowTimer = None
        self.changeMapTimer = None
        self.voteCloseTimer = None
        self.startTimerLeft = None
        self.autoRespawnTimer = None
        self.contagemDeath = None
        self.luaRuntime = None
        self.roomCreator = None

        # List Arguments
        self.anchors = []
        self.redTeam = []
        self.blueTeam = []
        self.roomTimers = []
        self.musicVideos = []
        self.lastHandymouse = [-1, -1]
        self.noShamanMaps = [7, 8, 14, 22, 23, 28, 29, 54, 55, 57, 58, 59, 60, 61, 70, 77, 78, 87, 88, 92, 122, 123, 124, 125, 126, 148, 149, 150, 151, 169, 172, 173, 174, 175, 178, 179, 180, 190, 1007, 888, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210]
        self.mapList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 136, 137, 138, 139, 140, 141, 142, 143, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 190, 191, 192, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210]
        self.playersBan = []
        self.blacklistcommands = []
        
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


        #if self.isHuggingEvent:
            #self.noShamanself.noShaman = True
            #self.disableAfkKill = True
            
        if self.name.startswith("*"):
            self.community = "xx"
            self.roomName = self.name
        else:
            self.community = self.name.split("-")[0].lower()
            self.roomName = self.name.split("-")[1]

        roomNameCheck = self.roomName[1:] if self.roomName.startswith("*") else self.roomName
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

        elif roomNameCheck.startswith("music"):
            self.isMusic = True

        elif roomNameCheck.startswith("racing"):
            self.isRacing = True
            self.noShaman = True
            self.noAutoScore = False
            self.never20secTimer = True
            self.roundTime = 63

        elif roomNameCheck.startswith("bootcamp"):
            self.isBootcamp = True
            self.countStats = False
            self.roundTime = 360
            self.never20secTimer = True
            self.autoRespawn = True
            self.noShaman = True

        elif roomNameCheck.startswith("vanilla"):
            self.isVanilla = True

        elif roomNameCheck.startswith("survivor"):
            self.isSurvivor = True
            self.roundTime = 90

        elif roomNameCheck.startswith("#meepracing"):
            self.isMeepRace = True
            self.roundTime = 63
            self.noShaman = True
                    
        elif self.roomName.startswith("#fastracing"):
            self.isSpeedRace = True
            self.roundTime = 63
            self.noShaman = True
                
        elif self.roomName.startswith("#ffarace"):
            self.isFFARace = True
            self.roundTime = 63
            self.noShaman = True
            
        elif self.roomName.startswith("#deathmatch"):
            self.isDeathmatch = True
            self.roundTime = 90
            self.noShaman = True
            
        elif roomNameCheck.startswith("#fly"):
            self.isFlyMod = True
            self.isVanilla = True
            self.roundTime = 120
            self.noShaman = True

        elif roomNameCheck.startswith("#") and not roomNameCheck.startswith in ["#meepracing", "#fastracing", "#ffarace", "#deathmatch", "#fly"]:
            minigame = roomNameCheck[1:]
            if minigame in self.server.minigames:
                self.minigame = minigame
            elif minigame.split('0')[0] in self.server.minigames:
                self.minigame = minigame.split('0')[0]
            elif minigame.split(' ')[0] in self.server.minigames:
                self.minigame = minigame.split(' ')[0]
            
        elif roomNameCheck.startswith("defilante"):
            self.isDefilante = True
            self.noShaman = True
            self.countStats = False
            self.noAutoScore = False

        elif roomNameCheck.startswith("801") or roomNameCheck.startswith("village"):
            if roomNameCheck.startswith("village"):
                self.isVillage = True
            else:
                self.is801Room = True
            self.roundTime = 2700
            self.never20secTimer = True
            self.autoRespawn = True
            self.countStats = False
            self.noShaman = True
            self.isFixedMap = True
            self.disableAfkKill = True
        else:
            self.isNormRoom = True
        self.mapChange()

    def addTextPopUpStaff(self, id, type, text, targetPlayer, x, y, width):
        p = ByteArray().writeInt(id).writeByte(type).writeUTF(text).writeShort(x).writeShort(y).writeShort(width).writeByte(4)
        if targetPlayer == '':
            self.sendAll([29, 23], p.toByteArray())
        else:
            player = self.clients.get(targetPlayer)
            if player != None:
                player.sendPacket([29, 23], p.toByteArray())
        return

    def loadLuaModule(self, minigame):
        module = self.server.minigames.get(minigame)
        print('g2')
        if module != None:
            print('g3')
            self.luaRuntime = Lua(self, self.server)
            #self.luaRuntime.owner = self.clients.get("Chatta#3388")
            #self.luaRuntime.owner = ""
            self.luaRuntime.RunCode(module)

    def startTimer(self):
        for player in self.clients.values():
            player.sendMapStartTimer(False)

    def displayParticle(self, particleType=0, xPosition=0, yPosition=0, xSpeed=0, ySpeed=0, xAcceleration=0, yAcceleration=0, targetPlayer=""):
        packet = ByteArray()
        packet.writeByte(particleType)
        packet.writeShort(xPosition)
        packet.writeShort(yPosition)
        packet.writeShort(xSpeed)
        packet.writeShort(ySpeed)
        packet.writeShort(xAcceleration)
        packet.writeShort(yAcceleration)
        if targetPlayer == "":
            self.sendAll(Identifiers.send.Display_Particle, packet.toByteArray())
        else:
            player = self.players.get(Utils.parsePlayerName(targetPlayer))
            if player != None:
                player.sendPacket(Identifiers.send.Display_Particle, packet.toByteArray())

    def mapChange(self):
        if self.changeMapTimer != None: self.changeMapTimer.cancel()
        for client in self.clients.values(): client.activeArtefact = 0

        for room in self.server.rooms.values():
            for playerCode, client in room.clients.items():
                if self.isDeathmatch:
                    if not self.contagemDeath is None:
                        self.contagemDeath.cancel()
        
        if not self.canChangeMap:
            self.changeMapAttemps += 1
            if self.changeMapAttemps < 5:
                self.changeMapTimer = reactor.callLater(1, self.mapChange)
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
                self.voteCloseTimer = reactor.callLater(8, self.closeVoting)
                for player in self.clients.values():
                    player.sendPacket(Identifiers.old.send.Vote_Box, [self.mapName, self.mapYesVotes, self.mapNoVotes])
            else:
                self.votingMode = False
                self.closeVoting()

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
                CursorMaps.execute("update Maps set YesVotes = ?, NoVotes = ?, Perma = 44 where Code = ?" if isDel else "update Maps set YesVotes = ?, NoVotes = ? where Code = ?", [TotalYes, TotalNo, self.mapCode])
                self.isVotingMode = False
                self.receivedNo = 0
                self.receivedYes = 0
                for player in self.clients.values():
                    player.qualifiedVoted = False
                    player.isVoted = False

            self.initVotingMode = True
            self.lastRoundCode = (self.lastRoundCode + 1) % 127

            if self.isSurvivor:
                cnt = 0
                for player in self.clients.values():
                    if not player.isDead and (not player.isVampire if self.mapStatus == 0 else not player.isShaman):
                        if not self.noAutoScore: 
                            player.playerScore += 10
                    elif player.isDead and not player.isAfk and not player.isShaman:
                        cnt += 1
                if cnt != 0 and self.getPlayerCountUnique() >= self.server.needToShamanPlayers:
                    for player in self.clients.values():
                        if player.isShaman:
                            if not 2260 in player.playerConsumables:
                                player.playerConsumables[2260] = cnt
                            else:
                                count = player.playerConsumables[2260] + cnt
                                player.playerConsumables[2260] = count
                            player.updateDatabase()
                            player.sendNewConsumable(2260, cnt)
                

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
                self.giveSurvivorStats() if self.isSurvivor else self.giveRacingStats() if self.isSpeedRace or self.isRacing else None

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
                
            self.currentMap = self.selectMap()
            self.checkMapXML()
            

            if self.currentMap in [range(44, 54), range(138, 144)] or self.mapPerma == 8 and self.getPlayerCount() >= 3:
                self.isDoubleMap = True

            if self.mapPerma in [7, 17, 42, 11]:
                self.isNoShamanMap = True

            if self.isSurvivor and self.mapPerma in [11]:
                reactor.callLater(5, self.sendVampireMode)

            if self.currentMap in [108, 109, 110, 111, 112, 113, 170, 171]:
                self.catchTheCheeseMap = True

            self.gameStartTime = Utils.getTime()
            self.gameStartTimeMillis = time.time()

            for player in self.clients.values():
                player.resetPlay()

            for player in self.clients.values():
                player.startPlay()

                if player.isHidden:
                    player.sendPlayerDisconnect()
                    player.isDead = True

            if self.isSpeedRace:
                CursorMaps.execute('select Time,Player from Maps where code = ?', [self.mapCode])
                rs = CursorMaps.fetchone()
                if rs[0] > 0:
                    if rs[0] > 100:
                        t = rs[0] / 100.0
                    else:
                        t = rs[0] / 10.0
                    for player in self.clients.values():
                        if player.langueID >= 0:
                            player.sendMessage("<bl>Best record by <J>"+str(rs[1])+"</J> <bl>with second</font> (<v>"+str(t)+"</v>s)")
                else:
                        for player in self.clients.values():
                            if player.langueID >= 0:
                                player.sendMessage("<R>(@%s)</R> <bl>map has not broken record</font>"% (self.mapCode))

           # if self.getPlayerCount() >= self.server.needToFirst:
                   #if not self.isEditor and not self.isVillage and not self.isTribeHouse and not self.isSurvivor and not self.isMusic:
                      # for player in self.clients.values():
                            #player.sendPacket([5, 51], ByteArray().writeByte(52).writeByte(1).writeShort(1).writeShort(random.randint(0, 30)).writeShort(-100).toByteArray())
                           # player.sendPacket([100, 101], "\x01\x01")



            if player in self.clients.values():
                if player.pet != 0:
                    if Utils.getSecondsDiff(player.petEnd) >= 0:
                        player.pet = 0
                        player.petEnd = 0
                    else:
                        self.sendAll(Identifiers.send.Pet, ByteArray().writeInt(player.playerCode).writeUnsignedByte(player.pet).toByteArray())

            if self.isMulodrome:
                self.mulodromeRoundCount += 1
                self.sendMulodromeRound()

                if self.mulodromeRoundCount <= 10:
                    for player in self.clients.values():
                        if player.playerName in self.blueTeam:
                            self.setNameColor(player.playerName, 0x979EFF)
                        elif player.playerName in self.redTeam:
                            self.setNameColor(player.playerName, 0xFF9396)
                else:
                    self.sendAll(Identifiers.send.Mulodrome_End)

            if self.isDeathmatch:
               self.canCannon = False
               for client in self.clients.values():
                  reactor.callLater(3, client.sendContagem)

            if self.isRacing or self.isDefilante or self.isSpeedRace or self.isMeepRace:
                self.roundsCount = (self.roundsCount + 1) % 10
                player = self.clients.get(self.getHighestScore())
                self.sendAll(Identifiers.send.Rounds_Count, ByteArray().writeByte(self.roundsCount).writeInt(player.playerCode if player != None else 0).toByteArray())
                if self.roundsCount == 9:
                    for client in self.clients.values():
                        client.playerScore = 0
                        
            self.startTimerLeft = reactor.callLater(3, self.startTimer)
            if not self.isFixedMap and not self.isTribeHouse and not self.isTribeHouseMap:
                self.changeMapTimer = reactor.callLater(self.roundTime + self.addTime, self.mapChange)
            
            self.killAfkTimer = reactor.callLater(30, self.killAfk)
            if self.autoRespawn or self.isTribeHouseMap:
                self.autoRespawnTimer = reactor.callLater(2, self.respawnMice)

    def getPlayerCount(self):
        return len(list(filter(lambda player: not player.isHidden, self.clients.values())))

    def getPlayerCountUnique(self):
        ipList = []
        for player in self.clients.values():
            if not player.ipAddress in ipList:
                ipList.append(player.ipAddress)
        return len(ipList)

    def getPlayerList(self):
        result = []
        for player in self.clients.values():
            if not player.isHidden:
                result.append(player.getPlayerData())
        return result

    def addClient(self, player, newRoom=False):
        self.clients[player.playerName] = player

        player.room = self
        if not newRoom:
            player.isDead = True
            self.sendAllOthers(player, [144, 2], ByteArray().writeBytes(player.getPlayerData()).writeBoolean(False).writeBoolean(True).toByteArray())
            player.startPlay()

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

    def checkChangeMap(self):
        if (not (self.isBootcamp or self.autoRespawn or self.isTribeHouse and self.isTribeHouseMap or self.isFixedMap)):
            alivePeople = list(filter(lambda player: not player.isDead, self.clients.values()))
            if not alivePeople:
                self.mapChange()

    def sendMessage(self, message1, message2, AP, *args):
        for player in self.clients.values():
            if player.playerName != AP:
                player.sendLangueMessage(message1, message2, *args)

    def sendAll(self, identifiers, packet=""):
        for player in self.clients.values():
            player.sendPacket(identifiers, packet)

    def sendAllOthers(self, senderClient, identifiers, packet=""):
        for player in self.clients.values():
            if not player == senderClient:
                player.sendPacket(identifiers, packet)
                
    def sendAllChat(self, playerCode, playerName, message, langueID, isOnly):
        p = ByteArray().writeInt(playerCode).writeUTF(playerName).writeByte(langueID).writeUTF(message)
        if isOnly == 0:
            for client in self.clients.values():
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

    def getSyncCode(self):
        if self.getPlayerCount() > 0:
            if self.currentSyncCode == -1:
                player = random.choice(list(self.clients.values()))
                self.currentSyncCode = player.playerCode
                self.currentSyncName = player.playerName
        else:
            if self.currentSyncCode == -1:
                self.currentSyncCode = 0
                self.currentSyncName = ""
        return self.currentSyncCode

    def selectMap(self):
        if not self.forceNextMap == "-1":
            force = self.forceNextMap
            self.forceNextMap = "-1"
            self.mapCode = -1

            if force.isdigit():
                return self.selectMapSpecificic(force, "Vanilla")
            elif force.startswith("@"):
                return self.selectMapSpecificic(force[1:], "Custom")
            elif force.startswith("#"):
                return self.selectMapSpecificic(force[1:], "Perm")
            elif force.startswith("<"):
                return self.selectMapSpecificic(force, "Xml")
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
                    run = self.selectMapSpecificic(runMap, "Custom")
                    if run != -1:
                        self.mapCode = 0
                        self.mapName = "Mice Master"
                        self.mapXML = "<C><P /><Z><S><S Y=\"360\" T=\"0\" P=\"0,0,0.3,0.2,0,0,0,0\" L=\"800\" H=\"80\" X=\"400\" /></S><D><P Y=\"0\" T=\"34\" P=\"0,0\" X=\"0\" C=\"719b9f\" /><T Y=\"320\" X=\"49\" /><P Y=\"320\" T=\"16\" X=\"224\" P=\"0,0\" /><P Y=\"319\" T=\"17\" X=\"311\" P=\"0,0\" /><P Y=\"284\" T=\"18\" P=\"1,0\" X=\"337\" C=\"57703e,e7c3d6\" /><P Y=\"284\" T=\"21\" X=\"294\" P=\"0,0\" /><P Y=\"134\" T=\"23\" X=\"135\" P=\"0,0\" /><P Y=\"320\" T=\"24\" P=\"0,1\" X=\"677\" C=\"46788e\" /><P Y=\"320\" T=\"26\" X=\"588\" P=\"1,0\" /><P Y=\"193\" T=\"14\" P=\"0,0\" X=\"562\" C=\"95311e,bde8f3,faf1b3\" /></D><O /></Z></C>"
                        self.mapYesVotes = 0
                        self.mapNoVotes = 0
                        self.mapPerma = 22
                        self.mapInverted = False

            elif self.is801Room:
                return 1234567890
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
                return self.selectMapStatus()
        return -1

    def selectMapStatus(self):
        maps = [0, -1, 4, 9, 5, 0, -1, 8, 6, 7]
        selectPerma = (17 if self.mapStatus % 2 == 0 else 17) if self.isRacing or self.isFFARace or self.isMeepRace or self.isSpeedRace else (13 if self.mapStatus % 2 == 0 else 3) if self.isBootcamp else 18 if self.isDefilante else (11 if self.mapStatus == 0 else 10) if self.isSurvivor else 10 if self.isOldSurvivor else 19 if self.isMusic and self.mapStatus % 2 == 0 else 41 if self.isDeathmatch else 45
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

        CursorMaps.execute("select * from Maps where Code != "+ str(self.currentMap) +" and Perma = 0 or Perma = 1 order by random() limit 1" if isMultiple else "select * from Maps where Code != "+ str(self.currentMap) + " and Perma = "+ str(selectPerma) +" order by random() limit 1")
        rs = CursorMaps.fetchone()
        if rs:
           self.mapCode = rs["Code"]
           self.mapName = rs["Name"]
           self.mapXML = rs["XML"]
           self.mapYesVotes = rs["YesVotes"]
           self.mapNoVotes = rs["NoVotes"]
           self.mapPerma = rs["Perma"]
           self.mapInverted = random.randint(0, 100) > 85
        else:
           map = random.choice(self.mapList)
           while map == self.currentMap:
               map = random.choice(self.mapList)
           return map
            
        return -1
        
    def selectMapSpecificic(self, code, type):
        if type == "Vanilla":
            return int(code)

        elif type == "Custom":
            mapInfo = self.getMapInfo(int(code))
            if mapInfo[0] == None:
                return 0
            else:
                self.mapCode = int(code)
                self.mapName = str(mapInfo[0])
                self.mapXML = str(mapInfo[1])
                self.mapYesVotes = int(mapInfo[2])
                self.mapNoVotes = int(mapInfo[3])
                self.mapPerma = int(mapInfo[4])
                self.mapInverted = False
                return -1

        elif type == "Perm":
            mapList = []
            CursorMaps.execute("select Code from Maps where Perma = ?", [int(str(code))])
            for rs in CursorMaps.fetchall():
                mapList.append(rs["Code"])

            if len(mapList) >= 1:
                runMap = random.choice(mapList)
            else:
                runMap = 0

            if len(mapList) >= 2:
                while runMap == self.currentMap:
                    runMap = random.choice(mapList)

            if runMap == 0:
                map = random.choice(self.MapList)
                while map == self.currentMap:
                    map = random.choice(self.MapList)
                return map
            else:
                mapInfo = self.getMapInfo(runMap)
                self.mapCode = runMap
                self.mapName = str(mapInfo[0])
                self.mapXML = str(mapInfo[1])
                self.mapYesVotes = int(mapInfo[2])
                self.mapNoVotes = int(mapInfo[3])
                self.mapPerma = int(mapInfo[4])
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

    def getMapInfo(self, mapCode):
        mapInfo = ["", "", 0, 0, 0]
        CursorMaps.execute("select Name, XML, YesVotes, NoVotes, Perma from Maps where Code = ?", [mapCode])
        rs = CursorMaps.fetchone()
        if rs:
            mapInfo = rs["Name"], rs["XML"], rs["YesVotes"], rs["NoVotes"], rs["Perma"]
        return mapInfo

    def checkIfDeathMouse(self):
        return len(list(filter(lambda player: not player.isDead, self.clients.values()))) <= 1

    def checkIfTooFewRemaining(self):
        return len(list(filter(lambda player: not player.isDead, self.clients.values()))) <= 2

    def getAliveCount(self):
        return len(list(filter(lambda player: not player.isDead, self.clients.values())))

    def getDeathCountNoShaman(self):
        return len(list(filter(lambda player: not player.isShaman and not player.isDead and not player.isNewPlayer, self.clients.values())))

    def getHighestScore(self):
        playerScores = []
        playerID = 0
        for player in self.clients.values():
            playerScores.append(player.playerScore)
                    
        for player in self.clients.values():
            if player.playerScore == max(playerScores):
                playerID = player.playerCode
        return playerID

    def getSecondHighestScore(self):
        playerScores = []
        playerID = 0
        for player in self.clients.values():
            playerScores.append(player.playerScore)
        playerScores.remove(max(playerScores))

        if len(playerScores) >= 1:
            for player in self.clients.values():
                if player.playerScore == max(playerScores):
                    playerID = player.playerCode
        return playerID

    def getShamanCode(self):
        if self.currentShamanCode == -1:
            if (self.currentMap in self.noShamanMaps) or self.isNoShamanMap or self.noShaman or (self.mapCode in self.noShamanMaps):
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
                for player in self.clients.values():
                    if player.playerCode == self.currentShamanCode:
                        self.currentShamanName = player.playerName
                        self.currentShamanType = player.shamanType
                        self.currentShamanSkills = player.playerSkills
                        break
        return self.currentShamanCode

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
                tempClient = random.choice(self.clients.values())
                self.currentSecondShamanCode = tempClient.playerCode

            for player in self.clients.values():
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

    def closeVoting(self):
        self.initVotingMode = False
        self.isVotingBox = False
        if self.voteCloseTimer != None: self.voteCloseTimer.cancel()
        self.mapChange()

    def killShaman(self):
        for player in self.clients.values():
            if player.playerCode == self.currentShamanCode:
                player.isDead = True
                player.sendPlayerDied()
        self.checkChangeMap()

    def killAfk(self):
        if self.isEditor or self.isTotemEditor or self.isBootcamp or self.isTribeHouseMap or self.disableAfkKill:
            return
            
        if ((Utils.getTime() - self.gameStartTime) < 32 and (Utils.getTime() - self.gameStartTime) > 28):
            for player in self.clients.values():
                if not player.isDead and player.isAfk:
                    player.isDead = True
                    if not self.noAutoScore: player.playerScore += 1
                    player.sendPlayerDied()
            self.checkChangeMap()

    def checkIfDoubleShamansAreDead(self):
        player1 = self.clients.get(self.currentShamanName)
        player2 = self.clients.get(self.currentSecondShamanName)
        return (False if player1 == None else player1.isDead) and (False if player2 == None else player2.isDead)

    def checkIfShamanIsDead(self):
        player = self.clients.get(self.currentShamanName)
        return False if player == None else player.isDead

    def checkIfShamanCanGoIn(self):
        for player in self.clients.values():
            if player.playerCode != self.currentShamanCode and player.playerCode != self.currentSecondShamanCode and not player.isDead:
                return False
        return True

    def giveShamanSave(self, shamanName, type):
        if not self.countStats:
            return
        player = self.clients.get(shamanName)
        if player != None and self.getPlayerCountUnique() >= self.server.needToShamanPlayers:
            if type == 0:
                player.shamanSaves += 1
                if not 2253 in player.playerConsumables:
                    player.playerConsumables[2253] = 1
                else:
                    count = player.playerConsumables[2253] + 1
                    player.playerConsumables[2253] = count
                player.updateDatabase()
                player.sendNewConsumable(2253, 1)
            elif type == 1:
                player.hardModeSaves += 1
                if not 2253 in player.playerConsumables:
                    player.playerConsumables[2253] = 1
                else:
                    count = player.playerConsumables[2253] + 1
                    player.playerConsumables[2253] = count
                player.updateDatabase()
                player.sendNewConsumable(2253, 1)
            elif type == 2:
                player.divineModeSaves += 1
                if not 2253 in player.playerConsumables:
                    player.playerConsumables[2253] = 1
                else:
                    count = player.playerConsumables[2253] + 1
                    player.playerConsumables[2253] = count
                player.updateDatabase()
                player.sendNewConsumable(2253, 1)
            if player.privLevel != 0:
                counts = [player.shamanSaves, player.hardModeSaves, player.divineModeSaves]
                titles = [self.server.shamanTitleList, self.server.hardModeTitleList, self.server.divineModeTitleList]
                rebuilds = ["shaman", "hardmode", "divinemode"]
                if counts[type] in titles[type]:
                    title = titles[type][counts[type]]
                    player.checkAndRebuildTitleList(rebuilds[type])
                    player.sendUnlockedTitle(int(title - (title % 1)), int(round((title % 1) * 10)))
                    player.sendCompleteTitleList()
                    player.sendTitleList()

    def respawnMice(self):
        for player in self.clients.values():
            if player.isDead:
                player.isDead = False
                player.playerStartTimeMillis = time.time()
                self.sendAll([144, 2], ByteArray().writeBytes(player.getPlayerData()).writeBoolean(False).writeBoolean(True).toByteArray())

        if self.autoRespawn or self.isTribeHouseMap:
            self.autoRespawnTimer = reactor.callLater(2, self.respawnMice)

    def respawnSpecific(self, playerName):
        player = self.clients.get(playerName)
        if player != None and player.isDead:
            player.resetPlay()
            player.isAfk = False
            player.playerStartTimeMillis = time.time()
            self.sendAll([144, 2], ByteArray().writeBytes(player.getPlayerData()).writeBoolean(False).writeBoolean(True).toByteArray())

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

    def checkMapXML(self):
        if int(self.currentMap) in self.server.vanillaMaps:
            self.mapCode = int(self.currentMap)
            self.mapName = "_Village" if self.mapCode == 801 else self.server.miceName
            self.mapXML = str(self.server.vanillaMaps[int(self.currentMap)])
            self.mapYesVotes = 0
            self.mapNoVotes = 0
            self.mapPerma = 41
            self.currentMap = -1
            self.mapInverted = False
        if int(self.currentMap) in self.server.eventMaps:
            self.mapCode = int(self.currentMap)
            self.mapName = "Event"
            self.mapXML = str(self.server.eventMaps[int(self.currentMap)])
            self.mapYesVotes = 0
            self.mapNoVotes = 0
            self.mapPerma = 92
            self.currentMap = -1
            self.mapInverted = False

    def sendVampireMode(self):
        player = self.clients.get(self.currentSyncName)
        if player != None:
            player.sendVampireMode(False)

    def bindKeyBoard(self, playerName, key, down, yes):
        player = self.clients.get(playerName)
        if player != None:
            player.sendPacket(Identifiers.send.Bind_Key_Board, ByteArray().writeShort(key).writeBoolean(down).writeBoolean(yes).toByteArray())

    def addPhysicObject(self, id, x, y, bodyDef):
        self.sendAll(Identifiers.send.Add_Physic_Object, ByteArray().writeShort(id).writeBoolean(bool(bodyDef["dynamic"]) if "dynamic" in bodyDef else False).writeByte(int(bodyDef["type"]) if "type" in bodyDef else 0).writeShort(x).writeShort(y).writeShort(int(bodyDef["width"]) if "width" in bodyDef else 0).writeShort(int(bodyDef["height"]) if "height" in bodyDef else 0).writeBoolean(bool(bodyDef["foreground"]) if "foreground" in bodyDef else False).writeShort(float(bodyDef["friction"]) if "friction" in bodyDef else 0).writeShort(float(bodyDef["restitution"]) if "restitution" in bodyDef else 0).writeShort(int(bodyDef["angle"]) if "angle" in bodyDef else 0).writeBoolean("color" in bodyDef).writeInt(int(bodyDef["color"]) if "color" in bodyDef else 0).writeBoolean(bool(bodyDef["miceCollision"]) if "miceCollision" in bodyDef else True).writeBoolean(bool(bodyDef["groundCollision"]) if "groundCollision" in bodyDef else True).writeBoolean(bool(bodyDef["fixedRotation"]) if "fixedRotation" in bodyDef else False).writeShort(int(bodyDef["mass"]) if "mass" in bodyDef else 0).writeShort(float(bodyDef["linearDamping"]) if "linearDamping" in bodyDef else 0).writeShort(float(bodyDef["angularDamping"]) if "angularDamping" in bodyDef else 0).writeBoolean(False).writeUTF("").toByteArray())
    
    def removeObject(self, objectId):
        self.sendAll(Identifiers.send.Remove_Object, ByteArray().writeInt(objectId).writeBoolean(True).toByteArray())

    def movePlayer(self, playerName, xPosition, yPosition, pOffSet, xSpeed, ySpeed, sOffSet):
        player = self.clients.get(playerName)
        if player != None:
            player.sendPacket(Identifiers.send.Move_Player, ByteArray().writeShort(xPosition).writeShort(yPosition).writeBoolean(pOffSet).writeShort(xSpeed).writeShort(ySpeed).writeBoolean(sOffSet).toByteArray())

    def setNameColor(self, playerName, color):
        if playerName in self.clients:
            self.sendAll(Identifiers.send.Set_Name_Color, ByteArray().writeInt(self.clients.get(playerName).playerCode).writeInt(color).toByteArray())

    def addPopup(self, id, type, text, targetPlayer, x, y, width, fixedPos):
        p = ByteArray().writeInt(id).writeByte(type).writeUTF(text).writeShort(x).writeShort(y).writeShort(width).writeBoolean(fixedPos)
        if targetPlayer == "":
            self.sendAll(Identifiers.send.Add_Popup, p.toByteArray())
        else:
            player = self.clients.get(targetPlayer)
            if player != None:
                player.sendPacket(Identifiers.send.Add_Popup, p.toByteArray())
    
    def addTextArea(self, id, text, targetPlayer, x, y, width, height, backgroundColor, borderColor, backgroundAlpha, fixedPos):
        p = ByteArray().writeInt(id).writeUTF(text).writeShort(x).writeShort(y).writeShort(width).writeShort(height).writeInt(backgroundColor).writeInt(borderColor).writeByte(100 if backgroundAlpha > 100 else backgroundAlpha).writeBoolean(fixedPos)
        if targetPlayer == "":
            self.sendAll(Identifiers.send.Add_Text_Area, p.toByteArray())
        else:
            player = self.clients.get(targetPlayer)
            if player != None:
                player.sendPacket(Identifiers.send.Add_Text_Area, p.toByteArray())

    def removeTextArea(self, id, targetPlayer):
        p = ByteArray().writeInt(id)
        if targetPlayer == "":
            self.sendAll(Identifiers.send.Remove_Text_Area, p.toByteArray())
        else:
            player = self.clients.get(targetPlayer)
            if player != None:
                player.sendPacket(Identifiers.send.Remove_Text_Area, p.toByteArray())

    def updateTextArea(self, id, text, targetPlayer):
        p = ByteArray().writeInt(id).writeUTF(text)
        if targetPlayer == "":
            self.sendAll(Identifiers.send.Update_Text_Area, p.toByteArray())
        else:
            client = self.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Update_Text_Area, p.toByteArray())

    def bindMouse(self, playerName, yes):
        player = self.clients.get(playerName)
        if player != None:
            player.sendPacket(Identifiers.send.Bind_Mouse, ByteArray().writeBoolean(yes).toByteArray())
			
    def showColorPicker(self, id, targetPlayer, defaultColor, title):
        packet = ByteArray().writeInt(id).writeInt(defaultColor).writeUTF(title)
        if targetPlayer == "":
            self.sendAll(Identifiers.send.Show_Color_Picker, packet.toByteArray())
        else:
            player = self.clients.get(targetPlayer)
            if player != None:
                player.sendPacket(Identifiers.send.Show_Color_Picker, packet.toByteArray())

    def startSnowSchedule(self, power):
        if self.isSnowing:
            self.startSnow(0, power, False)

    def startSnow(self, millis, power, enabled):
        self.isSnowing = enabled
        self.sendAll(Identifiers.send.Snow, ByteArray().writeBoolean(enabled).writeShort(power).toByteArray())
        if enabled:
            self.endSnowTimer = reactor.callLater(millis, lambda: self.startSnowSchedule(power))

    def addImage(self, imageName = "", target = "", xPosition = 50, yPosition = 50, targetPlayer = ""):
        if imageName == None:
            imageName = ""
        if target == None:
            target = ""
        if xPosition == None:
            xPosition == 50
        if yPosition == None:
            yPosition = 50
        if targetPlayer == None:
            targetPlayer = ""
        packet = ByteArray()
        self.lastImageID += 1
        packet.writeInt(self.lastImageID)
        packet.writeUTF(imageName)
        packet.writeByte(1 if target.startswith("#") else 2 if target.startswith("$") else 3 if target.startswith("%") else 4 if target.startswith("?") else 5 if target.startswith("_") else 6 if target.startswith("!") else 7 if target.startswith("&") else 0)
        target = target[1:]
        packet.writeInt(int(target) if target.isdigit() else self.server.getPlayerCode(Utils.parsePlayerName(target)))
        packet.writeShort(xPosition)
        packet.writeShort(yPosition)
        if targetPlayer == "":
            self.sendAll(Identifiers.send.Add_Image, packet.toByteArray())
        else:
            player = self.clients.get(Utils.parsePlayerName(targetPlayer))
            if player != None:
                player.sendPacket(Identifiers.send.Add_Image, packet.toByteArray())

    def giveSurvivorStats(self):
        for player in self.clients.values():
            if not player.isNewPlayer:
                player.survivorStats[0] += 1
                if player.isShaman:
                    player.survivorStats[1] += 1
                    player.survivorStats[2] += self.getDeathCountNoShaman()
                elif not player.isDead:
                    player.survivorStats[3] += 1

                i = 0
                while i < 3:
                    if player.survivorStats[i] >= self.server.statsPlayer["survivorCount"][i] and not self.server.statsPlayer["survivorBadges"][i] in player.shopBadges:
                        player.Shop.sendUnlockedBadge(self.server.statsPlayer["survivorBadges"][i])
                        try: player.shopBadges[self.server.statsPlayer["survivorBadges"][i]] += 1
                        except: player.shopBadges[self.server.statsPlayer["survivorBadges"][i]] = 1
                        player.Shop.checkAndRebuildBadges()
                    i += 1



    def giveRacingStats(self):
        for player in self.clients.values():
            if not player.isNewPlayer:
                player.racingStats[0] += 1
                if player.hasCheese or player.hasEnter:
                    player.racingStats[1] += 1
                if player.hasEnter:
                    if player.currentPlace <= 3:
                        player.racingStats[2] += 1
                    if player.currentPlace == 1:
                        player.racingStats[3] += 1

                i = 0
                while i < 3:
                    if player.racingStats[i] >= self.server.statsPlayer["racingCount"][i] and not self.server.statsPlayer["racingBadges"][i] in player.shopBadges:
                        player.parseShop.sendUnlockedBadge(self.server.statsPlayer["racingBadges"][i])
                        try: player.shopBadges[self.server.statsPlayer["racingBadges"][i]] += 1
                        except: player.shopBadges[self.server.statsPlayer["racingBadges"][i]] = 1
                        player.parseShop.checkAndRebuildBadges()
                    i += 1


    def send20SecRemainingTimer(self):
        if not self.changed20secTimer:
            if not self.never20secTimer and self.roundTime + (self.gameStartTime - Utils.getTime()) > 21:
                self.changed20secTimer = True
  
    def changeMapTimers(self, seconds):
        if self.changeMapTimer != None: self.changeMapTimer.cancel()
        self.changeMapTimer = reactor.callLater(seconds, self.mapChange)

    def newConsumableTimer(self, code):
        self.roomTimers.append(reactor.callLater(10, lambda: self.sendAll(Identifiers.send.Remove_Object, ByteArray().writeInt(code).writeBoolean(False).toByteArray())))

if __name__ == "__main__":
    # Connection Settings
    config = configparser.ConfigParser()
    config.read("./include/configs.properties")

    # Transformice
    Database, Cursor = None, None
    Database = pymysql.connect(host="localhost",user="root",password="",database="transformice1")
    Database.isolation_level = None 
    Cursor = Database.cursor()
    Database.autocommit(True)
    
    # Maps
    DatabaseMaps, CursorMaps = None, None
    DatabaseMaps = sqlite3.connect("./database/Maps.db", check_same_thread = False)
    DatabaseMaps.text_factory = str
    DatabaseMaps.isolation_level = None
    DatabaseMaps.row_factory = sqlite3.Row
    CursorMaps = DatabaseMaps.cursor()

    # Cafe
    DatabaseCafe, CursorCafe = None, None
    DatabaseCafe = sqlite3.connect("./database/Cafe.db", check_same_thread = False)
    DatabaseCafe.text_factory = str
    DatabaseCafe.isolation_level = None
    DatabaseCafe.row_factory = sqlite3.Row
    CursorCafe = DatabaseCafe.cursor()

    # Connection Server
    _Server = Server()
