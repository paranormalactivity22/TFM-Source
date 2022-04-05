# -*- coding: cp1252 -*-
import json
class AntiCheat:
    def __init__(self, client, server):
        self.client = client
        self.server = client.server
        
    def update(self):
        ac = ("[F.A.C] ")
        self.ac_config = open('./cheat/anticheat_config.txt', 'r').read()
        self.ac_c = json.loads(self.ac_config)
        self.learning = self.ac_c['learning']
        self.bantimes = self.ac_c['ban_times']
        self.s_list = open('./cheat/anticheat_allow', 'r').read()
        if self.s_list != "":
            self.s_list = self.s_list.split(',')
            self.s_list.remove("")
        else: self.s_list = []
            
    def readPacket(self, packet, pd=None):
        ac = ("[R.A.C] ")
        if packet == " " or packet == "":
            self.list.remove(packet)
        if str(packet) not in self.server.s_list and str(packet) != "":
            if self.server.learning == "true":
                self.client.sendServerMessage("[Anti-Hack] I found a new package coming from <BL>"+self.client.playerName+"</BL> [<VP>"+str(packet)+"</VP>]")
                self.server.s_list.append(str(packet))
                w = open('./cheat/anticheat_allow', 'a')
                w.write(str(packet) + ",")
                w.close()
            else:
                if self.client.privLevel != 15:
                    if packet == 55 or packet == 31 or packet == 51:
                        self.client.dac += 1
                        self.server.sendStaffMessage(5, "<ROSE>[Anti-Hack]<V> The player <J> "+ self.client.playerName +" <V> is suspected of cheat! <J>"+str(3-self.client.dac)+" <V> alerts it will be banned automatically.")
                        #self.client.sendMessage("<V>Dear <J> "+ self.client.playerName +" <V>, we detected Cheat Engine in your Standalone, please deactivate it or it will be banned within seconds.")
                    else: self.client.dac = 3
                    if self.client.dac >= 0 and self.client.dac <= 2:
                        self.client.dac += 1
                    else:
                        bans_done = 0
                        bl = open('./cheat/anticheat_bans.txt', 'r').read()
                        lista = bl.split('=')
                        lista.remove("")
                        for listas in lista:
                            data = listas.split(" ")
                            data.remove("")
                            name = data[1]
                            if name == self.client.playerName:
                                bans_done += 1
                        if bans_done == 0:
                            tb = int(self.server.bantimes)
                        elif bans_done == 1:
                            tb = int(self.server.bantimes)*2
                        elif bans_done == 2:
                            tb = int(self.server.bantimes)*3
                        elif bans_done >= 3:
                            tb = int(self.server.bantimes)*4
                        if int(packet) == 31:
                            info = "Fly hack"
                        elif int(packet) == 51 or int(packet) == 55:
                            info = "Speed"
                        else: info = "Unknown"
                            
                        bans_done += 1
                        x = open('./cheat/anticheat_bans.txt', 'a')
                        x.write("= Player: "+ self.client.playerName +" | Time: "+ str (tb) +" time (s) | Banned by: "+ str (packet) +" | Date: "+ info +" | + Info: "+ repr (pd) +"\n")
                        x.close()
                        self.server.sendStaffMessage(5, "<V>[Anti-Hack]<J> The player "+ self.client.playerName +" was banned by cheat for "+ str (tb) +" time (s). ["+ info +"]")
                        #if int(packet) == 51 or int(packet) == 55 or int(packet) == 31:
                            #self.server.banPlayer(self.client.playerName, int(tb), "Cheat Engine Detected [Ban #"+str(bans_done)+" - "+info+"]", "Anti-Hack", False)
                        #else: self.server.banPlayer(self.client.playerName, 0, "Suspected Activity Detected [Ban #"+str(bans_done)+" - "+info+"]", "Anti-Hack", False)
                else:
                    if int(packet) == 31:
                        info = "Fly hack"
                    elif int(packet) == 51 or int(packet) == 55:
                        info = "Speed"
                    else: info = "Unknown"
                    self.client.dac += 1
