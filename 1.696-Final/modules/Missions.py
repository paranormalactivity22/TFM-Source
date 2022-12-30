#coding: utf-8
import random, os, time, json, sys
from struct import *

# Modules
#from ByteArray import ByteArray
from Identifiers import Identifiers

# Utils
from utils import Utils

class ByteArray:
    def __init__(self, bytes=b""):
        if type(bytes) == str:
            try:
                bytes = bytes.encode()
            except Exception as e:
                pass
        self.bytes = bytes

    def writeByte(self, value):
        self.write(pack("!B", int(value) & 0xFF))
        return self

    def writeShort(self, value):
        self.write(pack("!H", int(value) & 0xFFFF))
        return self
    
    def writeInt(self, value):
        self.write(pack("!I", int(value) & 0xFFFFFFFF))
        return self

    def writeBool(self, value):
        return self.writeByte(1 if bool(value) else 0)
        
    def writeBoolean(self, value):
        return self.writeByte(1 if bool(value) else 0)

    def writeUTF(self, value):
        value = bytes(value.encode())
        self.writeShort(len(value))
        self.write(value)
        return self

    def writeBytes(self, value):
        self.bytes += value
        return self

    def read(self, c = 1):
        found = ""
        if self.getLength() >= c:
            found = self.bytes[:c]
            self.bytes = self.bytes[c:]

        return found

    def write(self, value):
        self.bytes += value
        return self

    def readByte(self):
        value = 0
        if self.getLength() >= 1:
            value = unpack("!B", self.read())[0]
        return value

    def readShort(self):
        value = 0
        if self.getLength() >= 2:
            value = unpack("!H", self.read(2))[0]
        return value

    def readInt(self):
        value = 0
        if self.getLength() >= 4:
            value = unpack("!I", self.read(4))[0]
        return value

    def readUTF(self):
        value = ""
        if self.getLength() >= 2:
            value = self.read(self.readShort()).decode()
        return value

    def readBool(self):
        return self.readByte() > 0

    def readUTFBytes(self, size):
        value = self.bytes[:int(size)]
        self.bytes = self.bytes[int(size):]
        return value

    def getBytes(self):
        return self.bytes

    def toByteArray(self):
        return self.getBytes()

    def getLength(self):
        return len(self.bytes)

    def bytesAvailable(self):
        return self.getLength() > 0

class Missions:
    def __init__(self, client, server):
        self.client = client
        self.server = client.server
        self.Cursor = client.Cursor
        
        #Int
        self.missionsCompleted = 0

    def loadMissions(self):
        if not self.client.isGuest:
            self.getMissions()
            self.activateMissions()

    def activateMissions(self):
    	self.client.sendPacket(Identifiers.send.Activate_Missions, ByteArray().writeBoolean(True).toByteArray())

    def getMissions(self):
        now, playerID = Utils.getTime(), str(self.client.playerID)
        self.Cursor.execute("select * from missions where userid = %s", [playerID])
        rs = self.Cursor.fetchone()
        if rs:
            if rs[2] > rs[2] + 86400:
                while True:
                    if len(self.client.playerMissions) == 4: break
                    self.randomMission()
                self.Cursor.execute("update missions set missions = %s, time = %s where userid = %s", [json.dumps(self.client.playerMissions), now, playerID])
            else:
                self.client.playerMissions = json.loads(rs[1])
        else:
            while True:
                if len(self.client.playerMissions) == 4:
                    break
                self.randomMission()
            self.Cursor.execute("insert into missions values (%s, %s, %s)", [playerID, json.dumps(self.client.playerMissions), now])

    def updateMissions(self, alterDB = False):
        if alterDB:
            playerID = str(self.client.playerID)
            self.Cursor.execute("update missions set missions=%s where userid=%s", [json.dumps(self.client.playerMissions), playerID])

    def randomMission(self, isTrue=False):
        missionID = random.randint(1, 7)
        while str(missionID) in self.client.playerMissions:
            missionID = random.randint(1, 7)

        missionType = 0
        reward = random.randint(15, 50)
        collect = random.randint(10, 65)

        if missionID == 2:
            missionType = random.randint(1, 3)

        if missionID == 6:
            collect = 1
        missionID = str(missionID)
        if isTrue:
            return [missionID, missionType, 0, collect, reward, True]
        else:
            self.client.playerMissions[missionID] = [missionID, missionType, 0, collect, reward, True]

    def getMission(self, missionID):
        missionID = str(missionID)
        if missionID in self.client.playerMissions:
            return self.client.playerMissions[missionID]

    def changeMission(self, missionID):
        missionID = str(missionID)
        mission = self.randomMission(True)
        
        i = 0
        while missionID == int(mission[0]):
            mission = self.randomMission(True)
            i += 1
            if i > 21:
                break
                
        if i <= 21:
            self.client.playerMissions[mission[0]] = [mission[0], mission[1], mission[2], mission[3], mission[4], True if 10 > i else False]
            

        if missionID in self.client.playerMissions:
            del self.client.playerMissions[missionID]

        """for id, mission in self.client.playerMissions.items():
            mission[5] = False"""
        self.sendMissions(False)

        self.updateMissions(True)

    def upMission(self, missionID, args=1):
        if missionID in self.client.playerMissions and not self.client.isGuest:
            mission = self.client.playerMissions[missionID]
            mission[2] += args
            if mission[2] >= mission[3]:
                self.completeMission(missionID)
            else:
                self.client.sendPacket(Identifiers.send.Complete_Mission, ByteArray().writeShort(missionID).writeByte(0).writeShort(mission[2]).writeShort(mission[3]).writeShort(mission[4]).writeShort(0).toByteArray())
        self.updateMissions(True)
        
    def upMissionAD(self):
        if int(self.missionsCompleted) >= 20:
            self.completeMission(missionID)
        else:
            self.client.sendPacket(Identifiers.send.Complete_Mission, ByteArray().writeByte(237).writeByte(129).writeByte(0).writeShort(self.missionsCompleted).writeShort(20).writeInt(20).writeShort(1).toByteArray())
        self.updateMissions(True)

    def completeMission(self, missionID):
        if missionID in self.client.playerMissions:
            mission = self.client.playerMissions[missionID]
            self.client.cheeseCount += mission[4]
            self.client.shopCheeses += mission[4]
            self.client.sendPacket(Identifiers.send.Complete_Mission, ByteArray().writeShort(missionID).writeByte(0).writeShort(mission[2]).writeShort(mission[3]).writeShort(mission[4]).writeShort(0).toByteArray())
            del self.client.playerMissions[missionID]
            self.randomMission()
            self.updateMissions(True)
            self.missionsCompleted += 1
            self.upMissionAD()
            
    def sendMissions(self, canChangeMission=True):
        missions = self.client.playerMissions
        count = len(missions)
        p = ByteArray()
        p.writeByte(count)
        IDOO = 0
        for id, mission in missions.items():
            if IDOO == 3:
                break
            p.writeShort(mission[0]) # langues -> $QJTFM_% (short)%
            p.writeByte(mission[1])
            p.writeShort(mission[2])
            p.writeShort(mission[3])
            p.writeShort(mission[4])
            p.writeShort(0)
            p.writeBoolean(mission[5])
            IDOO +=1
            
        # 4
        mission4 = self.getMission(237129)
        p.writeByte(237)
        p.writeByte(129)
        p.writeByte(0)
        p.writeShort(int(self.missionsCompleted))
        p.writeShort(20)
        p.writeInt(20)
        p.writeBoolean(False) # Substituir missão
        self.client.sendPacket(Identifiers.send.Send_Missions, p.toByteArray())
