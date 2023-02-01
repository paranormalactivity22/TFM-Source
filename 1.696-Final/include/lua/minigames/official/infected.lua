local module = {
	owner = "Bolodefchoco#0000",
	winner_score = 5 - 1,
	winner_color = 0xF79337,
	wait_time = 5,
	fly_power = -60,
	map_time = 60 * 2.3,
	garlic_winners = 2
}

local translations = {
	en = {
		greeting = "<R>Oh no, everyone is getting <VI><B>#infected</B><R>! RUN! <font size='11'>!help for +info</font>\n<VI>Submit maps in <CH2>https://atelier801.com/topic?f=6&t=882003</CH2>\n\tReport bugs to Bolodefchoco#0000\n\tDiscord server: <CH2>https://discord.gg/quch83R</CH2>",
		mice_win_1 = "<V>%s <FC>survived from the plague and got a point!",
		mice_win_2 = "<FC>All standing mice survived from the plague and got a point!",
		vamp_win = "<R>All standing vampires bit 'em all and got a point!",
		invalid_map = "<VI>You can't load this map in this module.",
		round_winner = "<%s>%s <%s>won the round!",
		help = "<R>Welcome to <VI><B>#infected</B><R>! The new version of the module was developed by <BV>Bolodefchoco#0000</B>.\n<font size='11'>\t<BL>- Each round a vampire will be chosen randomly!</BL>\n\t<G>- As a vampire, press spacebar to fly and capture all mice. You will win when all of them get infected.</G>\n\t<BL>- As a mouse, press space to push other players with Meep! and RUN from the vampires. You will win when all vampires die or when you are the only survivor.</BL>\n\t<G>- You will win the round when you get <B>5</B> points. Round winners have their nickname color changed.</G>\n\t<BL>- The winners of the last map can throw garlics when an icon appears. (Activation by clicking in the icon)</BL>\n\t<G>- Alpha Vampires can now teleport once in the map when an icon appears. (Activation by clicking in the icon)</G></font>",
		new_game = "<ROSE><font size='11'>A new game will start in %d seconds</font>",
		vamp = "<R>You're a vampire now. Press spacebar to fly and catch all mice!",
		teleport_skill = "<VI><B>Click in the map</B> <R>to teleport once!",
		garlic_skill = "<V><B>Press spacebar</B> <FC>to throw a garlic!"
	},
	br = {
		greeting = "<R>Ah não, todo mundo está sendo <VI><B>#infected</B><R>! CORRA! <font size='11'>!help para +info</font>\n<VI>Envie mapas em <CH2>https://atelier801.com/topic?f=6&t=882003</CH2>\n\tReporte bugs para Bolodefchoco#0000\n\tDiscord server: <CH2>https://discord.gg/quch83R</CH2>",
		mice_win_1 = "<V>%s <FC>sobreviveu(ram) à praga e ganhou(ram) um ponto!",
		mice_win_2 = "<FC>Todos os ratos que sobreviveram à praga ganharam um ponto!",
		vamp_win = "<R>Todos os vampiros em pé morderam os ratinhos vivos e ganharam um ponto!",
		invalid_map = "<VI>Você não pode carregar este mapa nesse módulo.",
		round_winner = "<%s>%s <%s>venceu(ram) a partida!",
		help = "<R>Bem-vindo ao <VI><B>#infected</B><R>! A nova versão do módulo foi desenvolvida por <BV>Bolodefchoco#0000</B>.\n<font size='11'>\t<BL>- A cada mapa um vampiro será escolhido aleatóriamente!</BL>\n\t<G>- Como vampiro, aperte a barra de espaço para voar e capture todos os ratos. Você irá ganhar quando todos forem infectados.</G>\n\t<BL>- Como rato, aperte a barra de espaço para empurrar os outros jogadores com Meep! e CORRA dos vampiros. Você irá gganhar quando todos os vampiros morrerem ou quando você for o único sobrevivente.</BL>\n\t<G>- Você vencerá a partida quando conseguir <B>5</B> pontos. Vencedores da partida terão a cor de seus nicknames alterada.</G>\n\t<BL>- Os vencedores do último mapa podem atirar alhos quando um ícone surgir. (Ativação ao clicar no ícone)</BL>\n\t<G>- Vampiros Alpha agora podem se teletransportar uma vez no mapa quando um ícone surgir. (Ativação ao clicar no ícone)</G></font>",
		new_game = "<ROSE><font size='11'>Um novo mapa começará em %d segundos</font>",
		vamp = "<R>Você é um vampiro agora. Aperte a barra de espaço para voar e pegue todos os ratos!",
		teleport_skill = "<VI><B>Clique no mapa</B> <R>para se teletransportar uma vez!",
		garlic_skill = "<V><B>Aperte a barra de espaço</B> <FC>para atirar um alho!"
	},
	fr = {
		greeting = "<R>Oh non, tout le monde est en train de devenir <VI><B>#infected</B><R>! COUREZ! <font size='11'>!help pour +info</font>\n<VI>Soumettez vos cartes à l'adresse <CH2>https://atelier801.com/topic?f=6&t=882003</CH2>\n\tSignalez des bugs à Bolodefchoco#0000\n\tServeur: <CH2>https://discord.gg/quch83R</CH2>",
		mice_win_1 = "<V>%s <FC>a/ont survécu à la peste et a/ont gagné un point!",
		mice_win_2 = "<FC>Toutes les souris ayant survécu à la peste ont gagné un point!",
		vamp_win = "<R>Tous les vampires ont mordu les souris et ont gagné un point!",
		invalid_map = "<VI>Vous ne pouvez pas charger cette map dans ce module.",
		round_winner = "<%s>%s <%s>a/ont gagné la manche!",
		help = "<R>Bienvenue dans <VI><B>#infected</B><R>! La nouvelle version du module a été développée par <BV>Bolodefchoco#0000</B>.\n<font size='11'>\t<BL>- Chaque manche, un vampire va être désigné aléatoirement!</BL>\n\t<G>- En tant que vampire, appuyez sur espace pour voler et capturer toutes les souris. Vous gagnerez lorsqu'elles sont toutes infectées.</G>\n\t<BL>- En tant que souris, appuyez sur espace pour écarter les autres joueurs avec le Meep! et ÉCHAPPEZ-vous des vampires. Vous gagnerez lorsque tous les vampires meurent ou lorsque vous êtes le dernier survivant.</BL>\n\t<G>- Vous gagnerez la manche lorsque vous aurez <B>5</B> points. Les gagnants de la manche auront la couleur de leur pseudo changée.</G>\n\t<BL>- Les gagnants de la dernière carte peuvent jeter une gousse d'ail lorsqu'un icone apparaît. (Activé en cliquant dessus)</BL>\n\t<G>- Les vampires Alpha peuvent alors se téléporter une fois, lorsqu'un icone apparaît. (Activé en cliquant dessus)</G></font>",
		new_game = "<ROSE><font size='11'>Une nouvelle partie va commencer dans %d secondes</font>",
		vamp = "<R>Vous êtes un vampire. Appuyez sur espace pour voler et essayez d'attraper toutes les souris!",
		teleport_skill = "<VI><B>Cliquez sur la carte</B> <R>pour vous téléporter!",
		garlic_skill = "<V><B>Appuyez sur espace</B> <FC>pour jeter une gousse d'ail!"
	},
	tr = {
		greeting = "<R>Olamaz, Herkes <VI><B>#infected</B><R>! KOŞ! <font size='11'>Bilgi için !help</font>\n<VI>Harita göndermek için <CH2>https://atelier801.com/topic?f=6&t=882003</CH2>\n\tHataları Bolodefchoco#0000'a bildirin\n\tDiscord sunucusu: <CH2>https://discord.gg/quch83R</CH2>",
		mice_win_1 = "<V>%s <FC>Enfeksiyondan kurtuldu ve 1 puan kazandı!",
		mice_win_2 = "<FC>Enfeksiyondan kurtulup hayatta kalan tüm fareler 1 puan kazandı!",
		vamp_win = "<R>Hayatta kalan tüm vampirler fareleri ısırarak 1 puan kazandı!",
		invalid_map = "<VI>Bu haritayı bu modülde açamazsın.",
		round_winner = "<%s>%s <%s>Turu kazandı!",
		help = " <VI><B>#infected</B><R><R>'e Hoşgeldin! Bu modülün yeni versiyonu <BV>Bolodefchoco#0000</B> tarafından kodlandı.\n<font size='11'>\t<BL>- Her tur rastgele vampir seçilicek!</BL>\n\t<G>- Vampir olarak, uçmak için boşluk tuşuna basın ve tüm fareleri yakalayın. Hepsini enfekte ettikten sonra kazanıcaksınız.</G>\n\t<BL>- Fare olarak, boşluk tuşuna basarak Meep ile vampirleri itebilirsiniz! ve vampirlerden kaçabilirsiniz. Tüm vampirler öldüğünde ya da hayatta kalan son kişi olduğunuzda kazanırsınız.</BL>\n\t<G>- Oyunu <B>5</B> puan toplayınca kazanıcaksınız. Kazananların isim rengi farklı olacak.</G>\n\t<BL>- Son haritanın kazananları ikon çıkınca sarımsak fırlatabilecek. (İkona basınca aktif olur)</BL>\n\t<G>- Alfa vampirler ikon çıkınca haritada 1 kere ışınlanabilecek. (İkona tıklayınca aktif olur)</G></font>",
		new_game = "<ROSE><font size='11'>Yeni oyun %d saniye içinde başlayacak</font>",
		vamp = "<R>Vampir oldunuz. Boşluk tuşuna basarak uçun ve tüm fareleri yakalayın!",
		teleport_skill = "<R>Işınlanmak için! <VI><B>Haritaya tıklayın</B>",
		garlic_skill = "<FC>Sarımsak atmak için! <V><B>Boşluk tuşuna basın</B>"
	},
}
local translate = translations[tfm.get.room.community] or translations.en

do
	local chatMessage = tfm.exec.chatMessage
	tfm.exec.chatMessage = function(msg, tgt, ignore)
		return chatMessage((ignore and '' or "<BL>[•] ") .. msg, tgt)
	end
end

local players = {
	_room = { },
	_alive = { },
	_dead = { },
	_vampire = { }
}

local copy = function(list)
	local out = { }
	for k, v in next, list do
		out[k] = v
	end
	return out
end

local insert = function(where, playerName)
	if not where[playerName] then
		where._count = (where._count or 0) + 1
		where[where._count] = playerName
		where[playerName] = where._count
	end
end

local remove = function(where, playerName)
	if where[playerName] then
		where._count = (where._count or 1) - 1
		table.remove(where, where[playerName])
		for i = where[playerName], where._count do
			where[where[i]] = where[where[i]] - 1
		end
		where[playerName] = nil
	end
end

table.random = function(list)
	return list[math.random(#list)]
end

math.pythag = function(x1, y1, x2, y2, range)
	return (x1 - x2) ^ 2 + (y1 - y2) ^ 2 <= (range ^ 2)
end

eventNewPlayer = function(playerName)
	insert(players._room, playerName)
	insert(players._dead, playerName)

	tfm.exec.lowerSyncDelay(playerName)
	system.bindKeyboard(playerName, 32, true, true)
	system.bindKeyboard(playerName, 72, true, true) -- H
	tfm.exec.chatMessage(translate.greeting, playerName)
end
for playerName in next, tfm.get.room.playerList do
	eventNewPlayer(playerName)
	tfm.exec.setPlayerScore(playerName, 0)
end

eventPlayerLeft = function(playerName)
	remove(players._room, playerName)
end

eventPlayerDied = function(playerName)
	remove(players._alive, playerName)
	remove(players._vampire, playerName)
	insert(players._dead, playerName)
end

local started -- nil : new game, didn't start ; true : started ; false : current game, finished

local vampData = { }

local alphaVampires = { }
eventPlayerVampire = function(playerName, vampire)
	remove(players._alive, playerName)
	insert(players._vampire, playerName)

	if started == nil then
		started = true
	end
	if not vampire then
		alphaVampires[playerName] = true
		alphaVampires[#alphaVampires + 1] = playerName
	
		local author = tfm.get.room.xmlMapInfo and tfm.get.room.xmlMapInfo.author or "?"
		ui.setMapName("<J>" .. author .. " <BL>- " .. tfm.get.room.currentMap .. "   <G>|   <N>Alpha : <font size='11'><R>" .. table.concat(alphaVampires, ", ") .. "</R></font>")
	end

	vampData[playerName] = {
		size = 1,
		cooldown = 0
	}

	tfm.exec.chatMessage(translate.vamp, playerName)
end

local lastRoundWinners = { }
local lastMapWinners = { } -- up to 2
local newGameTimer

local imgToDelete = { }

local spawnedMouseSkill = false
local spawnMouseSkill = function()
	for playerName in next, lastMapWinners do
		if not alphaVampires[playerName] then
			local pos = #imgToDelete + 1
			imgToDelete[pos] = tfm.exec.addImage("16a215d21de.png", ":0", 740, 340, playerName)
			ui.addTextArea(0, "<a href='event:" .. pos .. "'>\n\n\n\n\n\n\n\n\n\n\n\n", playerName, 745, 345, 50, 50, 1, 1, 0, true)
		end
	end
end

local spawnedVampireSkill = false
local spawnVampireSkill = function()
	for i = 1, #alphaVampires do
		local pos = #imgToDelete + 1
		imgToDelete[pos] = tfm.exec.addImage("16a21718053.png", ":0", 740, 340, alphaVampires[i])
		ui.addTextArea(0, "<a href='event:" .. pos .. "'>\n\n\n\n\n\n\n\n\n\n\n\n", alphaVampires[i], 745, 345, 50, 50, 1, 1, 0, true)
	end
end

eventKeyboard = function(playerName, key, _, x, y)
	if key == 72 then
		return tfm.exec.chatMessage(translate.help, playerName)
	end

	if players._dead[playerName] then return end

	if players._vampire[playerName] then
		tfm.exec.movePlayer(playerName, 0, 0, true, 0, module.fly_power)
	elseif started and lastMapWinners[playerName] then
		lastMapWinners[playerName] = nil

		tfm.exec.giveMeep(playerName)
		local dir = (tfm.get.room.playerList[playerName].isFacingRight and 1 or -1)
		for i = 0, math.random(1, 4) do
			tfm.exec.addImage(table.random({ "16a1ead3934.png", "16a1eba4903.png" }), "#" .. tfm.exec.addShamanObject(9500, x + (30 * dir), y + (i * 3), math.random(360), 10 * dir, -8), -10, -10)
		end
	end
end

local timer = 0
local isTribeHouse = string.byte(tfm.get.room.name, 2) == 3
eventNewGame = function()
	if isTribeHouse and (not tfm.get.room.xmlMapInfo or (tfm.get.room.xmlMapInfo.permCode ~= 11 and tfm.get.room.xmlMapInfo.permCode ~= 21)) then
		players._alive._count = 0
		tfm.exec.chatMessage(translate.invalid_map)
		return
	end

	timer = 0
	players._dead = { }
	players._vampire = { }
	players._alive = copy(players._room)
	players.__roundTotal = players._alive._count

	tfm.exec.setGameTime(module.map_time)

	for i = 1, #imgToDelete do
		tfm.exec.removeImage(imgToDelete[i])
	end

	for playerName in next, vampData do
		tfm.exec.changePlayerSize(playerName, 1)
	end

	for playerName in next, tfm.get.room.playerList do
		tfm.exec.giveMeep(playerName)
	end

	for i = 1, #lastRoundWinners do
		tfm.exec.setNameColor(lastRoundWinners[i], module.winner_color)
	end

	started = nil
	newGameTimer = nil
	vampData = { }
	alphaVampires = { }
	spawnedMouseSkill = false
	spawnedVampireSkill = false
end

eventLoop = function(currentTime, remainingTime)
	timer = timer + .5

	if newGameTimer then
		newGameTimer = newGameTimer - .5
	end

	if started then
		local roundWinner, counter, vampWin = { }, 0, false

		if timer % 1 == 0 then
			if players._alive._count == 0 then
				started = false

				for i = 1, players._vampire._count do
					if players._vampire[i] and tfm.get.room.playerList[players._vampire[i]] then
						tfm.exec.setPlayerScore(players._vampire[i], 1, true)
						if tfm.get.room.playerList[players._vampire[i]].score >= module.winner_score then
							counter = counter + 1
							roundWinner[counter] = players._vampire[i]
							if not vampWin then
								vampWin = true
							end
						end
					end
				end

				if players.__roundTotal > 3 then
					lastMapWinners = { }
					tfm.exec.chatMessage(translate.vamp_win)
				end
			elseif players._vampire._count == 0 or (players._alive._count == 1 and players.__roundTotal > 3) or (players._alive._count > 0 and remainingTime < 1000) then
				started = false

				for i = 1, players._alive._count do
					if players._alive[i] and tfm.get.room.playerList[players._alive[i]] then
						tfm.exec.setPlayerScore(players._alive[i], 1, true)
						if tfm.get.room.playerList[players._alive[i]].score >= module.winner_score then
							counter = counter + 1
							roundWinner[counter] = players._alive[i]
						end
					end
				end

				if players.__roundTotal > 3 then
					lastMapWinners = { }
					for i = 1, module.garlic_winners do
						if not players._alive[i] then break end
						lastMapWinners[players._alive[i]] = false
					end

					if players._alive._count < 3 then
						tfm.exec.chatMessage(string.format(translate.mice_win_1, table.concat(players._alive, ", ")))
					else
						tfm.exec.chatMessage(translate.mice_win_2)
					end
				end
			end

			if counter > 0 then
				for playerName in next, tfm.get.room.playerList do
					tfm.exec.setPlayerScore(playerName, 0)
				end

				lastRoundWinners = roundWinner
				
				tfm.exec.chatMessage(string.format(translate.round_winner, (vampWin and 'R' or "FC"), table.concat(roundWinner, ", "), (vampWin and "VI" or "ROSE")))
			end
		end

		if not started then
			if remainingTime > 5e3 then
				newGameTimer = module.wait_time
				if players.__roundTotal > 3 then
					tfm.exec.chatMessage(string.format(translate.new_game, newGameTimer))
				end
			end
		else
			if not spawnedVampireSkill and remainingTime <= 1e5 then
				spawnedVampireSkill = true
				spawnVampireSkill()
			end
			if not spawnedMouseSkill and remainingTime <= 1e5 and players._vampire._count > 1 then
				spawnedMouseSkill = true
				spawnMouseSkill()
			end

			local time, v = os.time()
			for id, obj in next, tfm.get.room.objectList do
				if obj.type == 9500 then
					for vamp = 1, players._vampire._count do
						if vampData[players._vampire[vamp]].size > 0 and time > vampData[players._vampire[vamp]].cooldown then
							v = tfm.get.room.playerList[players._vampire[vamp]]
							if math.pythag(v.x, v.y, obj.x, obj.y, 60) then
								vampData[players._vampire[vamp]].cooldown = time + 5e3
								vampData[players._vampire[vamp]].size = vampData[players._vampire[vamp]].size - .2
								tfm.exec.changePlayerSize(players._vampire[vamp], vampData[players._vampire[vamp]].size)
							end
						end
					end
				end
			end
		end
	end
	if not newGameTimer and ((players._alive._count or 0) + (players._vampire._count or 0)) < 2 and currentTime < 9e4 then
		newGameTimer = module.wait_time
	end

	if remainingTime < 500 or (newGameTimer and newGameTimer < .5) then
		ui.removeTextArea(0)
		tfm.exec.newGame("#" .. math.random(1, 2) .. "1")
	end
end

local onReviewMode = false
eventChatCommand = function(playerName, command)
	local cmd, param = string.match(command, "^(%S+) *(.*)")
	cmd = string.lower(cmd)

	if cmd == "help" or cmd == "h" or cmd == "info" then
		tfm.exec.chatMessage(translate.help, playerName)
	elseif playerName == module.owner then
		if cmd == "speak" and param then
			if param ~= '' then
				tfm.exec.chatMessage("<VI><B>[#infected]</B> " .. param, nil, true)
			end
		elseif cmd == "review" then
			onReviewMode = not onReviewMode
			tfm.exec.disableAutoShaman(onReviewMode)
			tfm.exec.chatMessage("<VI><B>[Map review]</B> " .. (onReviewMode and "on" or "off"), nil, true)
		elseif onReviewMode then
			if cmd == "np" and param then
				tfm.exec.newGame(param)
			end
		end
	end
end

eventTextAreaCallback = function(id, playerName, callback)
	if players._dead[playerName] then return end
	if players._vampire[playerName] then
		system.bindMouse(playerName, true)
		tfm.exec.chatMessage(translate.teleport_skill, playerName)
	else
		lastMapWinners[playerName] = true
		tfm.exec.giveMeep(playerName, false)
		tfm.exec.chatMessage(translate.garlic_skill, playerName)
	end
	tfm.exec.removeImage(imgToDelete[tonumber(callback)])
	ui.removeTextArea(0, playerName)
end

eventMouse = function(playerName, x, y)
	system.bindMouse(playerName, false)
	if not alphaVampires[playerName] then return end
	
	tfm.exec.movePlayer(playerName, x, y)
	local playerData = tfm.get.room.playerList[playerName]
	for i = -5, 5 do
		tfm.exec.displayParticle(3, playerData.x + (i * 2), playerData.y, math.random(10, 20) / 10 * table.random({ -1, 1 }), -math.random(10, 20) / 10)
	end
	tfm.exec.displayParticle(37, x, y)	
end

system.disableChatCommandDisplay()
tfm.exec.disableAutoNewGame()
tfm.exec.disableAutoTimeLeft()
tfm.exec.disableAutoScore()

eventLoop(0, 0)