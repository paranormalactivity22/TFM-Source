#coding: utf-8
import random, os, time, json, sys
from struct import *

# Modules
from ByteArray import ByteArray
from Identifiers import Identifiers

# Utils
from utils import Utils

class Missions:
    def __init__(self, client, server):
        self.client = client
        self.server = client.server
        self.Cursor = client.Cursor
        
        # Int
        self.missionsCompleted = 0
        # Dict
        self.playerMissions = {}

    def loadMissions(self):
        self.getMissions()
        self.activateMissions()

    def activateMissions(self):
    	self.client.sendPacket(Identifiers.send.Activate_Missions, ByteArray().writeBoolean(True).toByteArray())
        
    def updateMissions(self):
        self.Cursor['missions'].update_one({'userid':self.client.playerID},{'$set':{'missions':json.dumps(self.playerMissions),'totalfinished_missions':self.missionsCompleted}})

    #def getMissionsGuest(self):
    #    i = 0
    #    while i < 3:
    #        self.randomMission()
    #        i += 1

    def getMissions(self):
        rs = self.Cursor['missions'].find_one({'userid':self.client.playerID})
        if rs and rs['missions'] != "{}":
            self.playerMissions = json.loads(rs['missions'])
            self.missionsCompleted = rs['totalfinished_missions']
        else:
            i = 0
            while i < 3:
                self.randomMission()
                i += 1
            self.Cursor['missions'].insert_one({'userid':self.client.playerID,'missions':json.dumps(self.playerMissions),'totalfinished_missions':self.missionsCompleted})

    def randomMission(self, isTrue=False): 
        missionID,missionType = random.randint(1, 7), 0
        while str(missionID) in self.playerMissions:
            missionID = random.randint(1, 7)

        if missionID == 2:
            missionType = random.randint(1, 3)

        collect = random.choice({10:[20,40,60],21:[50],22:[70],23:[90],30:[50,70,90],40:[20,40,60],50:[20,40,60],60:[1],70:[3,5,7]}[int(f'{missionID}{missionType}')])
        reward = {20:20,40:35,60:50,50:20,70:35,90:50,3:20,5:35,7:50,1:25}[collect]
        
        if missionType != 0: missionID = f'{missionID}_{missionType}'
        else: missionID = str(missionID)
        if isTrue:
            return [missionID, missionType, 0, collect, reward, True]
        else:
            self.playerMissions[missionID] = [missionID, missionType, 0, collect, reward, True]

    def getMission(self, missionID):
        missionID = str(missionID)
        if missionID in self.playerMissions:
            return self.playerMissions[missionID]

    def changeMission(self, missionID):
        mission = self.randomMission(True)
                
        self.playerMissions[mission[0]] = [mission[0], mission[1], mission[2], mission[3], mission[4], True]

        if int(missionID) == 2:
            for missionID in ['2_1','2_2','2_3']: 
                if missionID in self.playerMissions: del self.playerMissions[missionID]
        if missionID in self.playerMissions:
            del self.playerMissions[missionID]

        self.canChangeMission = False
        self.sendMissions()

    def upMission(self, missionID,missionType=0):
        if missionID in self.playerMissions and not self.client.isGuest:
            mission = self.playerMissions[missionID]
            mission[2] += 1
            if mission[2] >= mission[3]:
                self.completeMission(missionID)
            else:
                self.client.sendPacket(Identifiers.send.Complete_Mission, ByteArray().writeShort(missionID).writeByte(0).writeShort(mission[2]).writeShort(mission[3]).writeShort(mission[4]).writeShort(0).toByteArray())
        
    def upMissionAD(self):
        if int(self.missionsCompleted) >= 20:
            self.client.sendPacket(Identifiers.send.Complete_Mission, ByteArray().writeByte(237).writeByte(129).writeByte(0).writeShort(self.missionsCompleted).writeShort(20).writeInt(20).writeShort(0).toByteArray())
            self.client.shopFraises += 20
            self.missionsCompleted = 0
            self.updateMissions()
        else:
            self.client.sendPacket(Identifiers.send.Complete_Mission, ByteArray().writeByte(237).writeByte(129).writeByte(0).writeShort(self.missionsCompleted).writeShort(20).writeInt(20).writeShort(1).toByteArray())

    def completeMission(self, missionID):
        if missionID in self.playerMissions:
            mission = self.playerMissions[missionID]
            self.client.shopCheeses += mission[4]
            self.client.sendPacket(Identifiers.send.Complete_Mission, ByteArray().writeShort(missionID).writeByte(0).writeShort(mission[2]).writeShort(mission[3]).writeShort(mission[4]).writeShort(0).toByteArray())
            del self.playerMissions[missionID]
            self.randomMission()
            self.updateMissions()
            self.missionsCompleted += 1
            self.upMissionAD()
            
    def sendMissions(self):
        p = ByteArray()
        p.writeByte(len(self.playerMissions) + 1)
        for id, mission in self.playerMissions.items():
            p.writeShort(mission[0].split('_')[0]) # langues -> $QJTFM_% (short)%
            p.writeByte(mission[1])
            p.writeShort(mission[2])
            p.writeShort(mission[3])
            p.writeShort(mission[4])
            p.writeShort(0)
            p.writeBoolean(False) #self.client.canChangeMission
            
        # 4
        p.writeByte(237)
        p.writeByte(129)
        p.writeByte(0)
        p.writeShort(int(self.missionsCompleted))
        p.writeShort(20)
        p.writeInt(20)
        p.writeBoolean(False)
        self.client.sendPacket(Identifiers.send.Send_Missions, p.toByteArray())
