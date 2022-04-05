#coding: utf-8
import random, os, sys
from struct import *

class ByteArray:
    def __init__(self, bytes=b""):
        try:
            bytes = bytes.encode()
        except:
            bytes = bytes
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


class DailyQuest:
    def __init__(self, client, server):
        self.client = client
        self.server = client.server
        self.Cursor = client.Cursor

        # List
        self.missionCheck = []

        # Boolean
        self.createAccount = False

    def loadDailyQuest(self, createAccount):
        self.createAccount = createAccount
        self.getMissions()
        self.activeDailyQuest()
        self.updateDailyQuest(True)

    def activeDailyQuest(self):
        self.client.sendPacket([144, 5], ByteArray().writeBool(True).toByteArray())

    def getMissions(self):
        if self.createAccount:
            ID = 0
            while ID < 3:
                if self.client.dailyQuest[ID] == 0:
                    mission = self.randomMission()
                    if mission[0] == self.client.dailyQuest[0] or self.client.dailyQuest[1] or self.client.dailyQuest[2]:
                        mission = self.randomMission()
                    self.Cursor.execute("select * from DailyQuest where MissionID = %s and UserID = %s", [int(mission[0]), self.client.playerID])
                    rs = self.Cursor.fetchone()
                    if not rs:
                        self.Cursor.execute("insert into DailyQuest values (%s, %s, %s, %s, '0', %s, '0')", [self.client.playerID, int(mission[0]), int(mission[1]), int(mission[2]), int(mission[3])])
                    self.client.dailyQuest[ID] = int(mission[0])
                    self.client.remainingMissions += 1
                    self.updateDailyQuest(True)
                ID += 1
            self.client.dailyQuest[3] = 1
            self.updateDailyQuest(True)

        self.Cursor.execute("select MissionID from DailyQuest where UserID = %s", [self.client.playerID])
        rs = self.Cursor.fetchall()
        if rs:
            for ms in rs:
                self.missionCheck.append(int(ms[0]))

        for missionID in self.missionCheck:
            if self.checkFinishMission(missionID, self.client.playerID):
                if int(missionID) in self.client.dailyQuest:
                    self.completeMission(missionID, self.client.playerID)
            self.missionCheck.remove(missionID)

    def checkFinishMission(self, missionID, playerID):
        self.Cursor.execute("select * from DailyQuest where MissionID = %s and UserID = %s", [missionID, playerID])
        rs = self.Cursor.fetchone()
        if int(rs[4]) >= int(rs[3]):
            return True
        return False

    def updateDailyQuest(self, alterDB = False):
        if alterDB:
            self.client.updateDatabase()
            
        self.Cursor.execute("select DailyQuest, RemainingMissions from Users where PlayerID = %s", [self.client.playerID])
        rs = self.Cursor.fetchone()
        if rs:
            self.client.remainingMissions = rs[1]
            self.client.dailyQuest = list(map(str, filter(None, rs[0].split(",")))) if rs[0] != "" else [0, 0, 0, 1]

    def randomMission(self):
        missionID = random.randint(1, 7)
        id = 0
        while int(self.client.dailyQuest[id]) == int(missionID):
            missionID = random.randint(1, 7)
            id += 1
        missionType = 0
        reward = random.randint(15, 50)
        collect = random.randint(10, 65)

        if missionID == 2:
            missionType = random.randint(1, 3)

        if missionID == 6:
            collect = 1

        return [missionID, missionType, collect, reward]

    def getMission(self, missionID, playerID):
        self.Cursor.execute("select * from DailyQuest where MissionID = %s and UserID = %s", [missionID, playerID])
        rs = self.Cursor.fetchone()
        if rs:
            if int(rs[6]) == 0:
                return [int(missionID), int(rs[2]), int(rs[3]), int(rs[4]), int(rs[5])]
            else:
                return int(rs[4])

    def changeMission(self, missionID, playerID):
        mission = self.randomMission()
        continueChange = False

        while missionID == int(mission[0]):
            mission = self.randomMission()

        if missionID == int(self.client.dailyQuest[0]):
            self.client.dailyQuest[3] = 0
            self.Cursor.execute("select * from DailyQuest where MissionID = %s and UserID = %s", [mission[0], playerID])
            rs = self.Cursor.fetchone()
            if rs:
                if not mission[0] == int(self.client.dailyQuest[0]) or int(self.client.dailyQuest[1]) or int(self.client.dailyQuest[2]):
                    self.client.dailyQuest[0] = mission[0]
            else:
                if not mission[0] == int(self.client.dailyQuest[0]) or int(self.client.dailyQuest[1]) or int(self.client.dailyQuest[2]):
                    self.Cursor.execute("insert into DailyQuest values (%s, %s, %s, %s, '0', %s, '0')", [playerID, mission[0], mission[1], mission[2], mission[3]])
                    self.client.dailyQuest[0] = mission[0]

        elif missionID == int(self.client.dailyQuest[1]):
            self.client.dailyQuest[3] = 0
            self.Cursor.execute("select * from DailyQuest where MissionID = %s and UserID = %s", [mission[0], playerID])
            rs = self.Cursor.fetchone()
            if rs:
                if not mission[0] == int(self.client.dailyQuest[0]) or int(self.client.dailyQuest[1]) or int(self.client.dailyQuest[2]):
                    self.client.dailyQuest[1] = self.client.dailyQuest[0]
                    self.client.dailyQuest[0] = mission[0]
            else:
                if not mission[0] == int(self.client.dailyQuest[0]) or int(self.client.dailyQuest[1]) or int(self.client.dailyQuest[2]):
                    self.Cursor.execute("insert into DailyQuest values (%s, %s, %s, %s, '0', %s, '0')", [playerID, mission[0], mission[1], mission[2], mission[3]])
                    self.client.dailyQuest[1] = self.client.dailyQuest[0]
                    self.client.dailyQuest[0] = mission[0]

        elif missionID == int(self.client.dailyQuest[2]):
            self.client.dailyQuest[3] = 0
            self.Cursor.execute("select * from DailyQuest where MissionID = %s and UserID = %s", [mission[0], playerID])
            rs = self.Cursor.fetchone()
            if rs:
                if not mission[0] == int(self.client.dailyQuest[0]) or int(self.client.dailyQuest[1]) or int(self.client.dailyQuest[2]):
                    self.client.dailyQuest[2] = self.client.dailyQuest[1]
                    self.client.dailyQuest[1] = self.client.dailyQuest[0]
                    self.client.dailyQuest[0] = mission[0]
            else:
                if not mission[0] == int(self.client.dailyQuest[0]) or int(self.client.dailyQuest[1]) or int(self.client.dailyQuest[2]):
                    self.Cursor.execute("insert into DailyQuest values (%s, %s, %s, %s, '0', %s, '0')", [playerID, mission[0], mission[1], mission[2], mission[3]])
                    self.client.dailyQuest[2] = self.client.dailyQuest[1]
                    self.client.dailyQuest[1] = self.client.dailyQuest[0]
                    self.client.dailyQuest[0] = mission[0]

        self.updateDailyQuest(True)

    def upMission(self, missionID, playerID):
        self.Cursor.execute("select * from DailyQuest where MissionID = %s and UserID = %s", [missionID, playerID])
        rs = self.Cursor.fetchone()
        if rs:
            self.Cursor.execute("update DailyQuest set QntCollected = QntCollected + 1 where MissionID = %s and UserID = %s", [missionID, playerID])
            self.updateDailyQuest(True)
            self.Cursor.execute("select * from DailyQuest where MissionID = %s and UserID = %s", [missionID, playerID])
            rs = self.Cursor.fetchone()
            if self.checkFinishMission(int(missionID), playerID):
                self.completeMission(int(missionID), playerID)
            else:
                self.client.sendPacket([144, 4], ByteArray().writeShort(missionID).writeByte(0).writeShort(rs[4]).writeShort(rs[3]).writeShort(rs[5]).writeShort(0).toByteArray())

    def completeMission(self, missionID, playerID):
        self.Cursor.execute("select * from DailyQuest where Fraise = '1' and UserID = %s", [playerID])
        rs = self.Cursor.fetchone()
        if rs:
            self.Cursor.execute("update DailyQuest set QntCollected = QntCollected + 1 where Fraise = '1' and UserID = %s", [playerID])
            self.client.cheeseCount += int(rs[5])
            self.client.shopCheeses += int(rs[5])
            #self.client.addConsumable(random.randint(0, 2350), random.randint(0, 5))
            self.client.remainingMissions -= 1
            mission = self.randomMission()
            if missionID == 6:
                mission[2] = 1

            if missionID == int(self.client.dailyQuest[0]):
                self.client.dailyQuest[0] = 0
                self.Cursor.execute("update DailyQuest set QntCollected = 0 and QntToCollect = %s and Reward = %s where MissionID = %s and UserID = %s", [mission[2], mission[3], missionID, playerID])

            elif missionID == int(self.client.dailyQuest[1]):
                self.client.dailyQuest[1] = 0
                self.Cursor.execute("update DailyQuest set QntCollected = 0 and QntToCollect = %s and Reward = %s where MissionID = %s and UserID = %s", [mission[2], mission[3], missionID, playerID])

            elif missionID == int(self.client.dailyQuest[2]):
                self.client.dailyQuest[2] = 0
                self.Cursor.execute("update DailyQuest set QntCollected = 0 and QntToCollect = %s and Reward = %s where MissionID = %s and UserID = %s", [mission[2], mission[3], missionID, playerID])

            self.updateDailyQuest(True)
            self.client.sendPacket([144, 4], ByteArray().writeByte(237).writeByte(129).writeByte(0).writeShort(int(rs[4])+1).writeShort(20).writeInt(20).toByteArray())

    def sendDailyQuest(self):
        p = ByteArray()
        p.writeByte(self.client.remainingMissions) # Quantidade de missões

        # Missions
        ID = 0
        while ID < 3:
            if int(self.client.dailyQuest[ID]) != 0:
                mission = self.getMission(int(self.client.dailyQuest[ID]), self.client.playerID)
                p.writeShort(int(mission[0])) # ID da missão
                p.writeByte(int(mission[1])) # Tipo de missão
                p.writeShort(int(mission[3])) # Quantidade coletada
                p.writeShort(int(mission[2])) # Quantidade a coletar
                p.writeShort(int(mission[4])) # Quantidade a receber
                p.writeShort(0)
                p.writeBool(True if bool(int(self.client.dailyQuest[3])) else False) # Substituir missão
            ID += 1

        # 4
        mission4 = self.getMission(237129, self.client.playerID)
        p.writeByte(237)
        p.writeByte(129)
        p.writeByte(0)
        p.writeShort(int(mission4)) # Quantidade coletada
        p.writeShort(20) # Quantidade a coletar
        p.writeInt(20) # Quantidade a receber
        p.writeBool(False) # Substituir missão

        self.client.sendPacket([144, 5], p.toByteArray())
