# -*- coding: cp1252 -*-
import json

class AntiCheat:
    def __init__(self, client, server):
        self.client = client
        self.server = client.server
        self.hours = 0
        self.bans_done = 0
        self.reason = "Hack (last warning before account deletion)"
        
    def getBans(self, playerName):
        global total_bans
        total_bans = 0
        bl = open('./cheat/anticheat_bans.txt', 'r').read()
        lista = bl.split('=')
        lista.remove("")
        for listas in lista:
            data = listas.split(" ")
            data.remove("")
            name = data[1]
            if name == playerName:
                total_bans += 1
        return total_bans
        
    def update(self):
        self.ac_config = open('./cheat/anticheat_config.txt', 'r').read()
        self.ac_c = json.loads(self.ac_config)
        self.learning = self.ac_c['learning']
        self.bantimes = self.ac_c['ban_times']
        self.s_list = open('./cheat/anticheat_allow', 'r').read()
        if self.s_list != "":
            self.s_list = self.s_list.split(',')
            self.s_list.remove("")
        else: self.s_list = []
           
    def getHack(self, packet):
        if packet == 55 or packet == 51: 
            return "Speed / Cheat Engine"
        elif packet == 31: 
            return "Fly"
        return "Unknown"
           
    def readPacket(self, packet):
        if packet == " " or packet == "":
            self.list.remove(packet)
        if str(packet) not in self.server.s_list and str(packet) != "":
            if self.server.learning == "true":
                self.client.sendServerMessage("[Anti-Cheat] I found a new package coming from <BL>"+self.client.playerName+"</BL> (<VP>"+str(packet)+"</VP>)")
                self.server.s_list.append(str(packet))
                w = open('./cheat/anticheat_allow', 'a')
                w.write(str(packet) + ",")
                w.close()
            else:
                if self.getHack(packet) != "Unknown":
                    self.client.sendServerMessage("[Anti-Cheat] The player <BL>"+ self.client.playerName +"<BL> is suspected of cheat! (<VP>"+self.getHack(packet)+").")
                    self.bans_done = self.getBans(self.client.playerName)
                    if self.bans_done == 0:
                        self.hours = 360
                    else:
                        self.hours = self.bans_done * 360
                       
                    self.bans_done += 1
                    x = open('./cheat/anticheat_bans.txt', 'a')
                    x.write("= Player: "+ self.client.playerName +" | Time: "+ str(self.hours) +" time (s) | Banned by: "+ str(packet) +" | Date: "+ self.getHack(packet) +" |\n")
                    x.close()
                    self.server.banPlayer(self.client.playerName, 0, "Hack (last warning before account deletion)", "ANTI-CHEAT")
