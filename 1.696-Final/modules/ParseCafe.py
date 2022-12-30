from Identifiers import Identifiers
from ByteArray import ByteArray
from Utils import *

class Cafe:
    def __init__(self, client, server):
        self.client = client
        self.server = server
        self.chec = 0

    def loadCafeMode(self):
        if self.client.isGuest:
            self.client.sendLangueMessage("", "<ROSE>$PasAutoriseParlerSurServeur")
        self.client.sendPacket(Identifiers.send.Open_Cafe, ByteArray().writeBoolean(not self.client.isGuest).toByteArray())

        packet = ByteArray().writeBoolean(True).writeBoolean(not self.client.privLevel < 7)
        self.client.CursorCafe.execute("select * from cafetopics order by Date desc limit 0, 20")
        for rs in self.client.CursorCafe.fetchall():
            if rs["Posts"] == 0:
                self.client.CursorCafe.execute("delete from cafetopics where TopicID = ?", [rs["TopicID"]])
                self.client.CursorCafe.execute("delete from cafeposts where TopicID = ?", [rs["TopicID"]])
            packet.writeInt(rs["TopicID"]).writeUTF(rs["Title"]).writeInt(self.server.getPlayerID(rs["Author"])).writeInt(rs["Posts"]).writeUTF(rs["LastPostName"]).writeInt(Utils.getSecondsDiff(rs["Date"]))
        self.client.sendPacket(Identifiers.send.Cafe_Topics_List, packet.toByteArray())
        self.sendWarnings()

    def openCafeTopic(self, topicID):
        packet = ByteArray().writeBoolean(True).writeInt(topicID).writeBoolean(0).writeBoolean(True)
        self.client.CursorCafe.execute("select * from cafeposts where TopicID = ? order by PostID asc", [topicID])
        for rs in self.client.CursorCafe.fetchall():
            if self.client.privLevel >= 7 and rs["Status"] in [0, 2]:
                packet.writeInt(rs["PostID"]).writeInt(self.server.getPlayerID(rs["Name"])).writeInt(Utils.getSecondsDiff(rs["Date"])).writeUTF(rs["Name"]).writeUTF(rs["Post"]).writeBoolean(str(self.client.playerCode) not in rs["Votes"].split(",")).writeShort(rs["Points"]).writeUTF(rs["ModeratedBY"]).writeByte(rs["Status"])
                self.chec = rs["PostID"]
            elif rs["Status"] < 2: # == 1
                packet.writeInt(rs["PostID"]).writeInt(self.server.getPlayerID(rs["Name"])).writeInt(Utils.getSecondsDiff(rs["Date"])).writeUTF(rs["Name"]).writeUTF(rs["Post"]).writeBoolean(str(self.client.playerCode) not in rs["Votes"].split(",")).writeShort(rs["Points"]).writeUTF("").writeByte(rs["Status"])
        self.server.lastCafeTopicID = topicID
        self.client.sendPacket(Identifiers.send.Open_Cafe_Topic, packet.toByteArray())
        
    def createNewCafePost(self, topicID, message):
        commentsCount = 0
        if topicID == 0:
            topicID = self.server.lastCafeTopicID
        if not self.server.checkMessage(message):
            self.client.CursorCafe.execute("insert into cafeposts values (null, ?, ?, ?, ?, 0, ?, '', 0)", [topicID, self.client.playerName, message, Utils.getTime(), self.client.playerCode])
            self.client.CursorCafe.execute("update cafetopics set LastPostName = ?, Posts = Posts + 1, Date = ? where TopicID = ?", [self.client.playerName, Utils.getTime(), topicID])
            self.client.CursorCafe.execute("select count(*) as count from cafeposts where TopicID = ?", [topicID])
            rs = self.client.CursorCafe.fetchone()
            commentsCount = rs["count"]
            self.openCafeTopic(topicID)
            for player in self.server.players.copy().values():
                if player.isCafe:
                    player.sendPacket(Identifiers.send.Cafe_New_Post, ByteArray().writeInt(topicID).writeUTF(self.client.playerName).writeInt(commentsCount).toByteArray())
        
    def createNewCafeTopic(self, title, message):
        if not self.server.checkMessage(title):
            self.client.CursorCafe.execute("insert into cafetopics values (null, ?, ?, '', 0, ?, ?)", [title, self.client.playerName, Utils.getTime(), self.client.langue])
            self.createNewCafePost(self.client.CursorCafe.lastrowid, message)
        self.loadCafeMode()
        
    def voteCafePost(self, topicID, postID, mode):
        points = 0
        votes = ""

        self.client.CursorCafe.execute("select Points, Votes from cafeposts where TopicID = ? and PostID = ?", [topicID, postID])
        rs = self.client.CursorCafe.fetchone()
        if rs:
            points = rs["Points"]
            votes = rs["Votes"]
            
        if not str(self.client.playerID) in votes:
            votes += str(self.client.playerID) if votes == "" else "," + str(self.client.playerID)
            if mode:
                points += 1
            else:
                points -= 1

            self.client.CursorCafe.execute("update cafeposts set Points = ?, Votes = ? where TopicID = ? and PostID = ?", [points, votes, topicID, postID])
            self.client.updateDatabase()
            self.openCafeTopic(topicID)
        
    def getTopicID(self, postID):
        self.client.CursorCafe.execute("select TopicID from cafeposts where postID = ?", [postID])
        rs = self.client.CursorCafe.fetchone()
        return rs[0] if rs else -1
        
    def getPlayerPosts(self, playerName, topicID):
        self.client.CursorCafe.execute("select PostID from cafeposts where Name = ? and TopicID = ?", [playerName, topicID])
        r = self.client.CursorCafe.fetchall()
        return len(r)
        
    def deleteCafePost(self, postID):
        topicID = self.getTopicID(postID)
        if topicID != -1:
            self.client.CursorCafe.execute("delete from cafeposts where TopicID = ? and PostID = ?", [topicID, postID])
            self.client.CursorCafe.execute("update cafetopics set Posts = Posts - 1 where TopicID = ?", [topicID])
            self.client.sendPacket(Identifiers.send.Delete_Cafe_Message, ByteArray().writeInt(topicID).writeInt(postID).toByteArray())
            self.openCafeTopic(topicID)

    def deleteAllCafePost(self, topicID, playerName):
        n = self.getPlayerPosts(playerName, topicID)
        self.client.CursorCafe.execute("delete from cafeposts where TopicID = ? and Name = ?", [topicID, playerName])
        self.client.CursorCafe.execute("update cafetopics set Posts = Posts - ? where TopicID = ?", [n, topicID])
        self.loadCafeMode()
        self.openCafeTopic(topicID)
        
    def ReportCafeTopic(self, topicID, postID):
        pass
        
    def ViewCafeMessages(self, playerName):
        pass
        
    def checkTopic(self, topicID):
        if self.client.privLevel < 7:
            return 0
        else:
            self.client.CursorCafe.execute("select count(*) as count from cafeposts where TopicID = ? and Status = 0", [topicID])
            return int(self.client.CursorCafe.fetchone()["count"])
    
    def CheckMessageType(self, topicID, status):
        if status:
            self.client.CursorCafe.execute("update cafeposts set Status = 2, ModeratedBY = ? where PostID = ?", [self.client.playerName, self.chec])
            self.chec = 0
            self.openCafeTopic(topicID)
        else:
            self.client.CursorCafe.execute("update cafeposts set Status = 1, ModeratedBY = ? where PostID = ?", [self.client.playerName, self.chec])
            self.chec = 0
            self.openCafeTopic(topicID)
        
    def sendWarnings(self):
        self.client.CursorCafe.execute("select * from cafeposts where status = 2 and name = ? order by postid asc", [self.client.playerName])
        self.client.sendPacket([144, 11], ByteArray().writeShort(len(self.client.CursorCafe.fetchall())).toByteArray())