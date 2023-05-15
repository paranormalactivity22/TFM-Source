class Identifiers:
    class tribulle:
        class send:
            ET_ResultatIdentificationService = 2
            ET_ResultatMiseAJourLocalisation = 5
            ET_ResultatMiseAJourLocalisations = 7
            ET_ResultatMessageCanal = 21
            ET_SignaleMessageCanal = 22
            ET_ResultatRejoindreCanal = 24
            ET_ResultatQuitterCanal = 26
            ET_SignaleRejointCanal = 27
            ET_SignaleQuitteCanal = 28
            ET_SignaleMembreRejointCanal = 29
            ET_SignaleMembresRejoignentCanal = 30
            ET_SignaleMembreQuitteCanal = 31
            ET_SignaleMembresQuittentCanal = 32
            ET_ResultatMessagePrive = 34
            ET_RecoitMessagePriveSysteme = 35
            ET_RecoitMessagePrive = 36
            ET_ResultatDefinitModeSilence = 40
            ET_ResultatDemandeMembresCanal = 42
            ET_ErreurDemandeMembresCanal = 43
            ET_ResultatAjoutAmi = 45
            ET_ResultatRetireAmi = 47
            ET_ResultatListeAmis = 49
            ET_ErreurListeAmis = 50
            ET_SignaleAjoutAmi = 51
            ET_SignaleModificationLocalisationAmi = 52
            ET_SignaleRetraitAmi = 53
            ET_SignaleConnexionAmi = 54
            ET_SignaleDeconnexionAmi = 55
            ET_SignaleConnexionAmis = 56
            ET_SignaleDeconnexionAmis = 57
            ET_SignaleAjoutAmiBidirectionnel = 58
            ET_SignaleRetraitAmiBidirectionnel = 59
            ET_ResultatDemandeEnMariage = 61
            ET_ErreurDemandeEnMariage = 62
            ET_SignaleDemandeEnMariage = 63
            ET_ResultatRepondDemandeEnMariage = 65
            ET_SignaleMariage = 66
            ET_ResultatDemandeDivorce = 68
            ET_SignaleDivorce = 69
            ET_ResultatAjoutListeNoire = 71
            ET_ResultatRetireListeNoire = 73
            ET_ResultatListeNoire = 75
            ET_ErreurListeNoire = 76
            ET_SignaleAjoutListeNoire = 77
            ET_SignaleRetraitListeNoire = 78
            ET_CreerTribu = 79
            ET_ResultatCreerTribu = 80
            ET_SignaleTribuCreee = 81
            ET_SignaleInvitationTribu = 82
            ET_ErreurRepondInvitationTribu = 84
            ET_ResultatInformationsTribu = 86
            ET_ErreurInformationsTribu = 87
            ET_ResultatInformationsTribuSimple = 89
            ET_ErreurInformationsTribuSimple = 90
            ET_ResultatMembresTribu = 92
            ET_ErreurMembresTribu = 93
            ET_ResultatQuitterTribu = 95
            ET_ResultatListeHistoriqueTribu = 97
            ET_ErreurListeHistoriqueTribu = 98
            ET_SignaleConnexionMembre = 99
            ET_SignaleDeconnexionMembre = 100
            ET_SignaleConnexionMembres = 101
            ET_SignaleDeconnexionMembres = 102
            ET_SignaleChangementMessageJour = 103
            ET_SignaleChangementCodeMaisonTFM = 104
            ET_SignaleChangementRang = 105
            ET_SignaleExclusion = 106
            ET_SignaleNouveauMembre = 107
            ET_SignaleDepartMembre = 108
            ET_SignaleModificationLocalisationMembreTribu = 109
            ET_ResultatChangerMessageJour = 111
            ET_ResultatExclureMembre = 115
            ET_ResultatInviterMembre = 117
            ET_ErreurInviterMembre = 118
            ET_ResultatChangerCodeMaisonTFM = 120
            ET_ResultatListeRangs = 122
            ET_ErreurListeRangs = 123
            ET_ResultatAffecterRang = 125
            ET_ResultatAjouterRang = 127
            ET_ErreurAjouterRang = 128
            ET_ResultatSupprimerRang = 130
            ET_ResultatRenommerRang = 132
            ET_ResultatAjouterDroitRang = 134
            ET_ResultatSupprimerDroitRang = 136
            ET_ResultatInverserOrdreRangs = 138
            ET_ResultatDesignerChefSpirituel = 142
            ET_ResultatRenommerTribu = 144
            ET_ResultatDissoudreTribu = 146
            ET_SignaleDissolutionTribu = 147
            ET_ResultatDonneesUtilisateur = 153
            ET_ErreurDonneesUtilisateur = 154
            ET_ResultatDefinitDonneesUtilisateur = 156
            ET_ResultatChangerDeGenre = 158
            ET_SignaleChangementAvatar = 160
            ET_SignaleChangementDeGenre = 159
            ET_DemandeNouveauxMessagesPrivesWeb = 161
            ET_DemandeNouveauxMessagesPrivesWebEnMasse = 162
            ET_SignalNouveauxMessagesPrivesWeb = 163
            ET_SignalNouveauMessagePriveWeb = 164
            ET_ReponseDemandeInfosJeuUtilisateur = 166
            ET_ErreurDemandeInfosJeuUtilisateur = 167
        
        class recv:
            ST_IdentificationService = 1
            ST_PingUtilisateur = 3
            ST_MiseAJourLocalisation = 4
            ST_MiseAJourLocalisations = 6
            ST_EnvoitMessageCanal = 20
            ST_RejoindreCanal = 23
            ST_QuitterCanal = 25
            ST_EnvoitMessagePrive = 33
            ST_DefinitModeSilence = 39
            ST_DemandeMembresCanal = 41
            ST_AjoutAmi = 44
            ST_RetireAmi = 46
            ST_ListeAmis = 48
            ST_DemandeEnMariage = 60
            ST_RepondDemandeEnMariage = 64
            ST_DemandeDivorce = 67
            ST_AjoutListeNoire = 70
            ST_RetireListeNoire = 72
            ST_ListeNoire = 74
            ST_CreerTribu = 79
            ST_ResultatCreerTribu = 80
            ST_RepondInvitationTribu = 83
            ST_DemandeInformationsTribu = 85
            ST_DemandeInformationsTribuSimpleParNom = 88
            ST_DemandeMembresTribu = 91
            ST_QuitterTribu = 94
            ST_ListeHistoriqueTribu = 96
            ST_ChangerMessageJour = 110
            ST_ExclureMembre = 114
            ST_InviterMembre = 116
            ST_ChangerCodeMaisonTFM = 119
            ST_ListeRangs = 121
            ST_AffecterRang = 124
            ST_AjouterRang = 126
            ST_SupprimerRang = 129
            ST_RenommerRang = 131
            ST_AjouterDroitRang = 133
            ST_SupprimerDroitRang = 135
            ST_InverserOrdreRangs = 137
            ST_DesignerChefSpirituel = 141
            ST_RenommerTribu = 143
            ST_DissoudreTribu = 145
            ST_DemandeDonneesUtilisateur = 152
            ST_DefinitDonneesUtilisateur = 155
            ST_ChangerDeGenre = 157
            ST_SignaleChangementDeGenre = 159
            ST_SignaleChangementAvatar = 160
            ST_SignalNouveauxMessagesPrivesWeb = 163
            ST_SignalNouveauMessagePriveWeb = 164
            ST_RequeteDemandeInfosJeuUtilisateur = 165
    class recv:
        Old_Protocol = (1, 1)

        Object_Sync = (4, 3)
        Mouse_Movement = (4, 4)
        Mort = (4, 5)
        Player_Position = (4, 6)
        Shaman_Position = (4, 8)
        Crouch = (4, 9)
        Consumable_Object = (4, 16)

        Map_26 = (5, 8)
        Shaman_Message = (5, 9)
        Convert_Skill = (5, 14)
        Demolition_Skill = (5, 15)
        Projection_Skill = (5, 16)
        Enter_Hole = (5, 18)
        Get_Cheese = (5, 19)
        Place_Object = (5, 20)
        Ice_Cube = (5, 21)
        Bridge_Break = (5, 24)
        Defilante_Points = (5, 25)
        Restorative_Skill = (5, 26)
        Recycling_Skill = (5, 27)
        Gravitational_Skill = (5, 28)
        Antigravity_Skill = (5, 29)
        Handymouse_Skill = (5, 35)
        Enter_Room = (5, 38)
        Room_Password = (5, 39)
        #Send_Music = (5, 70)
        #Music_Time = (5, 71)
        #Send_PlayList = (5, 73)

        Chat_Message = (6, 6)
        Staff_Chat = (6, 10)
        Commands = (6, 26)

        Player_Emote = (8, 1)
        Player_Emotions = (8, 5)
        Player_Shaman_Fly = (8, 15)
        Player_Shop_List = (8, 20)
        Player_Buy_Skill = (8, 21)
        Player_Redistribute = (8, 22)
        Player_Report = (8, 25)
        Player_Ping1 = (8, 30)
        Player_Meep = (8, 39)
        Player_Bolos = (8, 43)
        Player_Vampire = (8, 66)
        Player_Calendar = (8, 70)
        
        Purchase_Fraises = (12, 1)
        Cancel_Transaction = (12, 3)
        Buy_Fraises = (12, 10)
        Purchase_Fraises_allpass = (12, 11)
        Purchase_Fraises_Steam = (12, 12)
        Purchase_Fraises_G2APAY = (12, 15)
        Purchase_Fraises_primeiroPay = (12, 16)
        
        Tribe_House = (16, 1)
        Tribe_Invite = (16, 2)
        Bot_Bolo = (16, 10)

        Equip_Clothe = (20, 6)
        Save_Clothe = (20, 7)
        Shop_Info = (20, 15)
        Equip_Item = (20, 18)
        Buy_Item = (20, 19)
        Buy_Custom = (20, 20)
        Custom_Item = (20, 21)
        Buy_Clothe = (20, 22)
        Buy_Shaman_Item = (20, 23)
        Equip_Shaman_Item = (20, 24)
        Buy_Shaman_Custom = (20, 25)
        Custom_Shaman_Item = (20, 26)
        Buy_Full_Look_Confirm = (20, 27)
        Send_gift = (20, 28)
        Gift_result = (20, 29)
			
        Modopwet = (25, 2)
        Modopwet_Notifications = (25, 12)
        Delete_Report = (25, 23)
        Watch = (25, 24)
        Ban_Hack = (25, 25)
        Change_Langue = (25, 26)
        Chat_Log = (25, 27)

        Create_Account = (26, 7)
        Login = (26, 8)
        Player_FPS = (26, 13)
        New_Survey = (26, 16)
        Survey_Answer = (26, 17)
        Survey_Result = (26, 18)
        Captcha = (26, 20)
        Player_MS = (26, 25)
        Dummy = (26, 26)
        Player_Info = (26, 28)
        Player_Info2 = (26, 29)
        Temps_Client = (26, 30)
        Rooms_List = (26, 35)
        Request_Info = (26, 40)
        
        Transformation_Object = (27, 11)
        
        Correct_Version = (28, 1)
        Game_Log = (28, 4)
        Player_Ping = (28, 6)
        Change_Shaman_Type = (28, 10)
        Letter = (28, 15)
        Computer_Info = (28, 17)
        Change_Shaman_Color = (28, 18)
        Check_Command_Tab = (28, 48)

        Lua_Script = (29, 1)
        Key_Board = (29, 2)
        Mouse_Click = (29, 3)
        Popup_Answer = (29, 20)
        Text_Area_Callback = (29, 21)
        Color_Picked = (29, 32)
        
        Reload_Cafe = (30, 40)
        Open_Cafe_Topic = (30, 41)
        Create_New_Cafe_Post = (30, 43)
        Create_New_Cafe_Topic = (30, 44)
        Open_Cafe = (30, 45)
        Vote_Cafe_Post = (30, 46)
        Delete_Cafe_Message = (30, 47)
        Delete_All_Cafe_Message = (30, 48)
            
        Mulodrome_Close = (30, 13)
        Mulodrome_Join = (30, 15)
        Mulodrome_Leave = (30, 17)
        Mulodrome_Play = (30, 20)
        
        Open_Inventory = (31, 1)
        Use_Consumable = (31, 3)
        Equip_Consumable = (31, 4)
        Trade_Invite = (31, 5)
        Cancel_Trade = (31, 6)
        Trade_Add_Consusmable = (31, 8)
        Trade_Result = (31, 9)
        
        Bulle = (44, 1)

        Old_Tribulle = (60, 1)
        Tribulle = (60, 3)
        Invocation = (100, 2)
        Remove_Invocation = (100, 3)
        Keep_Shaman_STRM = (100, 20)
        Full_Look = (100, 31)
        Crazzy_Packet = (100, 40)
        Question = (100, 50)
        NPC_Functions = (100, 75)
        Change_Shaman_Badge = (100, 79)
        Map_Info = (100, 80)
        
        Set_Language = (176, 1)
        Language_List = (176, 2)
        Open_Community_Partner = (176, 4)
        BotProtection = (176, 47)
        
        
        Open_Missions = (149, 1)
        Change_Mission = (149, 2)
        Report_Cafe_Post = (149, 4)
        Send_Warnings = (149, 5)
        Check_Cafe_Message = (149, 6)
        Sonar_System = (149, 8)
        Attach_Player = (149, 10)
        NotAttach_Player = (149, 11)
        Open_Outfits = (149, 12)
        Add_Outfit = (149, 13)
        Remove_Outfit = (149, 14)
        View_Posts = (149, 15)
        Open_Sales = (149, 16)
        Remove_Sale = (149, 17)
        Add_Sale = (149, 18)
        Ranking = (149, 21)
        Purchase_Emojies = (149, 25)
    
    class send:
        Sync = [4, 3]
        Player_Movement = [4, 4]
        Player_Position = [4, 6]
        Move_Object = [4, 7]
        Remove_Object = [4, 8]
        Crouch = [4, 9]
        Shaman_Position = [4, 10]
		
        Rounds_Count = [5, 1]
        New_Map = [5, 2]
        Shaman_Message = [5, 9]
        Map_Start_Timer = [5, 10]
        Spawn_Item = [5, 12]
        Convert_Skill = [5, 13]
        Skill_Object = [5, 14]
        Demolition_Skill = [5, 15]
        Projection_Skill = [5, 16]
        Explosion = [5, 17]
        Spawn_Object = [5, 20]
        Enter_Room = [5, 21]
        Round_Time = [5, 22]
        Snow = [5, 23]
        Bridge_Break = [5, 24]
        Restorative_Skill = [5, 26]
        Recycling_Skill = [5, 27]
        Gravitation_Skill = [5, 28]
        Antigravity_Skill = [5, 29]
        Rollout_Mouse_Skill = [5, 30]
        Mouse_Size = [5, 31]
        Remove_All_Objects_Skill = [5, 32]
        Leaf_Mouse_Skill = [5, 33]
        Iced_Mouse_Skill = [5, 34]
        Handymouse_Skill = [5, 35]
        Spider_Mouse_Skill = [5, 36]
        Grapnel_Mouse_Skill = [5, 37]
        Evolution_Skill = [5, 38]
        Room_Password = [5, 39]
        Skill = [5, 40]
        Reset_Shaman_Skills = [5, 42]
        Gatman_Skill = [5, 43]
        Bonfire_Skill = [5, 45]
        Soulmate = [5, 48]
        Teleport = [5, 50]
        Lower_Sync_Delay = [5, 52]
        Music_Video = [5, 72]
        Music_PlayList = [5, 73]
        Tutorial = [5, 90]
        
        Chat_Message = [6, 6]
        Tribe_Message = [6, 8]
        Message = [6, 9]
        Staff_Chat = [6, 10]
        Recv_Message = [6, 20]
        
        Room_Server = [7, 1]
        Room_Type = [7, 30]
        
        Player_Emote = [8, 1]
        Give_Currency = [8, 2]
        Move_Player = [8, 3]
        Emotion = [8, 5]
        Player_Win = [8, 6]
        Set_Player_Score = [8, 7]
        Shaman_Exp = [8, 8]
        Shaman_Gain_Exp = [8, 9]
        Enable_Skill = [8, 10]
        Shaman_Info = [8, 11]
        New_Shaman = [8, 12]
        SpeechBubbles = [8, 13]
        Titles_List = [8, 14]
        Shaman_Fly = [8, 15]
        Profile = [8, 16]
        Meep_IMG = [8, 18]
        #Remove_Cheese = [8, 19]
        Shop_List = [8, 20]
        New_Shaman_Without_Items = [8, 21]
        Shaman_Skills = [8, 22]
        NPC = [8, 30]
        Start_Position = [8, 37]
        Meep = [8, 38]
        Can_Meep = [8, 39]
        Unlocked_Badge = [8, 42]
        Send_Gift_Animation = [8, 43]
        Anim_Zelda = [8, 44]
        Anim_Donation = [8, 50]
        Vampire_Mode = [8, 66]
        Adventures = [8, 70]
        
        Payment_in_progress_popup = [12, 2]
        Transaction_error_popup = [12, 3]
        Transaction_error_popup2 = [12, 9]
        Purchase_Menu = [12, 12]
        allpass_Purchase_Menu = [12, 13]
        Kongregate_Purchase_Menu = [12, 14]
        G2APAY_Purchase_Menu = [12, 16]
        primeiroPay_Purchase_Menu = [12, 17]
        Purchase_Fraises_Completed_Popup = [12, 20]
        Error_Occured_Popup = [12, 60]
        
        Hide_Room_Details = [14, 1]
        Hide_Room_Details2 = [14, 2]
        
        Tribe_Invite = [16, 2]
        Banner_Login = [16, 9]
        
        Item_Buy = [20, 2]
        Promotion = [20, 3]
        Undefined = [20, 4]
        Shop_Info = [20, 15]
        Look_Change = [20, 17]
        New_Hat_Available_Message = [20, 20]
        Shaman_Look = [20, 24]
        Shaman_Items = [20, 27]
        Gift_result = [20, 29]
        Shop_Gift = [20, 30]
        
        Shaman_Earned_Exp = [24, 1]
        Shaman_Earned_Level = [24, 2]
        Redistribute_Error_Time = [24, 3]
        Redistribute_Error_Cheeses = [24, 4]
        
        Modopwet_Open = [25, 2]
        Modopwet_Banned = [25, 5]
        Modopwet_Disconnected = [25, 6]
        Modopwet_Deleted = [25, 7]
        Modopwet_Update_Language = [25, 9]
        Modopwet_Chatlog = [25, 10]
        Watch = [25, 11]
        Modopwet_Add_Language = [25, 12]
        
        
        Gain_Give = [26, 1]
        Player_Identification = [26, 2]
        Correct_Version = [26, 3]
        Player_Lifes = [26, 4]
        Attack = [26, 9]
        Player_Damanged = [26, 11]
        Login_Result = [26, 12]
        Player_FPS = [26, 13]
        Survey = [26, 16]
        Survey_Answer = [26, 17]
        Captcha = [26, 20]
        Player_MS = [26, 25]
        Player_Info = [26, 28]
        Temps_Client = [26, 30]
        Login_Souris = [26, 33]
        Game_Mode = [26, 35]
        NPC_Shop = [26, 38]
        Tribulle_Token = [26, 41]
        
        Can_Transformation = [27, 10]
        Transformation = [27, 11]
        
        Time_Stamp = [28, 2]
        Promotion_Popup = [28, 3]
        Message_Langue = [28, 5]
        Ping = [28, 6]
        Shaman_Type = [28, 10]
        Totem_Item_Count = [28, 11]
        Account_Link_Successfull = [28, 12]
        Letter = [28, 15]
        Account_Link_Error_Popup = [28, 30]
        Take_Cheese = [28, 41]
        Log_Message = [28, 46]
        Enter_Command = [28, 48]
        Request_Info = [28, 50]
        Queue_popup = [28, 61]
        TextBox_Popup = [28, 60]
        Verify_Email_Popup = [28, 64]
        Server_Restart = [28, 88]
        
        # Lua
        Lua_Minigame = [29, 1]
        Bind_Key_Board = [29, 2]
        Bind_Mouse = [29, 3]
        Set_Name_Color = [29, 4]
        Reset_Lua = [29, 5]
        Lua_Message = [29, 6]
        Remove_Image = [29, 18]
        Add_Image = [29, 19]
        Add_Text_Area = [29, 20]
        Update_Text_Area = [29, 21]
        Remove_Text_Area = [29, 22]
        Add_Popup = [29, 23]
        Set_Map_Name = [29, 25]
        Set_Shaman_Name = [29, 26]
        Display_Particle = [29, 27]
        Add_Physic_Object = [29, 28]
        Remove_Physic_Object = [29, 29]
        Add_Joint = [29, 30]
        Remove_Joint = [29, 31]
        Show_Color_Picker = [29, 32]
        Lua_Disable = [29, 33]
        
        # Mulodrome and Cafe
        Mulodrome_Result = [30, 4]
        Mulodrome_End = [30, 13]
        Mulodrome_Start = [30, 14]
        Mulodrome_Join = [30, 15]
        Mulodrome_Leave = [30, 16]
        Mulodrome_Winner = [30, 21]
        Cafe_Topics_List = [30, 40]
        Open_Cafe_Topic = [30, 41]
        Open_Cafe = [30, 42]
        Cafe_New_Post = [30, 44]
        Delete_Cafe_Message = [30, 47]
        
        # Inventory and Trade
        Inventory = [31, 1]
        Update_Inventory_Consumable = [31, 2]
        Use_Inventory_Consumable = [31, 3]
        Trade_Invite = [31, 5]
        Trade_Result = [31, 6]
        Trade_Start = [31, 7]
        Trade_Add_Consumable = [31, 8]
        Trade_Confirm = [31, 9]
        Trade_Close = [31, 10]

        # Bulle
        Bulle = [44, 1]
        
        # Tribulle
        Old_Tribulle = [60, 1]
        Tribulle = [60, 3]
        Switch_Tribulle = [60, 4]

        Invocation = [100, 2]
        Remove_Invocation = [100, 3] # remove by id
        Joquempo = [100, 5]
        Dead_Bubble = [100, 7]
        #Remove_Invocation2 = [100, 10] # remove by utf
        Buy_Full_Look = [100, 31]
        Crazzy_Packet = [100, 40]
        Questionable_Popup = [100, 50]
        Stop_Moving = [100, 66]
        New_Consumable = [100, 67]
        Add_Anim = [100, 68]
        Add_Frame = [100, 69]
        Pet = [100, 70]
        Balloon_Badge = [100, 71]
        Change_Title = [100, 72]
        Steam_Purchase_Menu = [100, 90]
        Image_Login = [100, 99]


        # new packets
        Player_List = [144, 1]
        Player_Respawn = [144, 2]
        Send_Missions = [144, 3]
        Complete_Mission = [144, 4]
        Activate_Missions = [144, 5]
        Player_Get_Cheese = [144, 6]
        Remove_Shaman = [144, 7]
        SetPositionToAttach = [144, 9]
        Send_Cafe_Warnings = [144, 11]
        Browser_Version_Attention = [144, 13]
        Change_Nickname_Popup = [144, 14]
        Minibox_1 = [144, 17]
        Room_Info_Message = [144, 18]
        AttachPlayer = [144, 20]
        UnAttachPlayer = [144, 21]
        Open_Outfits = [144, 22]
        NPC_Emote = [144, 23]
        Background_color = [144, 25]
        Score_Fur_vs_Fur = [144, 26]
        Limit_Shaman_Item = [144, 28]
        Open_Sales = [144, 29]
        setAIEMode = [144, 30]
        Shaman_Cache = [144, 31]
        PlayerScale = [144, 32]
        NightMode = [144, 33]
        Fur_Cache = [144, 34]
        Ranking = [144, 36]
        #Play_Sound = [144, 38]
        Emoji_panel = [144, 44]
        
        # New new packets
        Init_Sonar = [145, 174]
        End_Sonar = [145, 181]
        
        # Login packets #2
        Set_Language = [176, 5]
        Language_List = [176, 6]
        Verify_Code = [176, 7]
        Community_Partners = [176, 8]
        Open_Link = [176, 9]
        

    class old:
        class recv:
            class Player:
                C = 4
                Bomb_Explode = 6
                Conjure_Start = 12
                Conjure_End = 13
                Conjuration = 14
                Snow_Ball = 16
            
            class Room:
                C = 5
                Anchors = 7
                Begin_Spawn = 8
                Spawn_Cancel = 9
                Totem_Anchors = 13
                Move_Cheese = 16
                Bombs = 17
            
            class Balloons:
                C = 8
                Place_Balloon = 16
                Remove_Balloon = 17
            
            class Map:
                C = 14
                Vote_Map = 4
                Load_Map = 6
                Validate_Map = 10
                Map_Xml = 11
                Return_To_Editor = 14
                Export_Map = 18
                Reset_Map = 19
                Exit_Editor = 26
            
            class Draw:
                C = 25
                Clear = 3
                Drawing = 4
                Point = 5

        class send:
            Bomb_Explode = [4, 6]
            Conjure_Start = [4, 12]
            Conjure_End = [4, 13]
            Add_Conjuration = [4, 14]
            Conjuration_Destroy = [4, 15]
            
            Anchors = [5, 7]
            Begin_Spawn = [5, 8]
            Spawn_Cancel = [5, 9]
            Move_Cheese = [5, 16]
            Bombs = [5, 17]
            Player_Get_Cheese = [5, 19]
            Gravity = [5, 22]
            
            Player_Died = [8, 5]
            Player_Disconnect = [8, 7]
            Player_Respawn = [8, 8]
            Player_List = [8, 9]
            Unlocked_Title = [8, 14]
            Titles_List = [8, 15]
            Balloon = [8, 16]
            Shaman_Perfomance = [8, 17]
            Save_Remaining = [8, 18]
            Mute_Player_Message = [8, 19]
            Sync = [8, 21]
            Catch_The_Cheese_Map = [8, 23]
            NPC = [8, 30]
            
            Vote_Box = [14, 4]
            Map_Exported = [14, 5]
            Load_Map_Result = [14, 8]
            Load_Map = [14, 9]
            Map_Editor = [14, 14]
            Map_Validated = [14, 17]
            Editor_Message = [14, 20]

            Tribe_Result = [16, 4]
            
            Totem = [22, 22]
            
            Drawing_Clear = [25, 3]
            Drawing_Start = [25, 4]
            Drawing_Point = [25, 5]
            
            Player_Ban_Message = [26, 7]
            Login = [26, 8]
            Ban_Consideration = [26, 9]
            Music = [26, 12]
            Player_Ban = [26, 17]
            Player_Ban_Login = [26, 18]
            Facebook_URL = [26, 19]
            Log = [26, 23]
            Old_Exception = [26, 25] # ["he is stup*d", "The player made an error because"]