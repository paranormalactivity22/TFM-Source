local module = {
	owner = "Bolodefchoco#0000",
	map_file = 2,
	time = 6 * 60
}

-- Commands
local commands = {
	keyboard = {
		checkpoint = "E",
		removeCheckpoint = "Shift + E",
		die = "Del",
		timeLeaderboard = "L"
	},
	nextMap = "next",
	reloadMap = "again",
	newMap = "map",
	time = "time",
	standardTime = "standtime",
	checkpoint = "checkpoint",
	password = "password",
	removecheese = "remcheese"
}

-- Init
system.disableChatCommandDisplay()
local disable = { "AutoShaman", "AutoScore", "AutoTimeLeft", "AutoNewGame", "PhysicalConsumables", "AfkDeath" }
for i = 1, #disable do
	tfm.exec["disable" .. disable[i]]()
end
tfm.exec.setAutoMapFlipMode(false)

-- Translations
local translations = {
	en = {
		-- Init
		welcome = "Welcome to <B>#Hardcamp</B>! Press H to check the commands.\n\tYou as admin: <I>/room *#hardcamp0%s</I>\n\tReport any issue to Bolodefchoco#0000!",

		-- Info
		skip = "<VP>%s</VP> just skipped the map!",
		restart = "<VP>%s</VP> just restarted the current map!",
		loadmap = "<VP>%s</VP> just loaded the map %s!",
		settime = "The time has been set to %s minutes!",
		setstandtime = "The standard time of all the rounds has been set to %s minutes!",
		enabled = "enabled! Press <B>E</B> to put a checkpoint and <B>Shift+E</B> to remove it.",
		difficulty = "Difficulty",

		-- Simple words
		disabled = "disabled!",

		-- Menu
		menu = {
			[1] = {"%s", "\tThe difference between a regular Bootcamp and Hardcamp is that we accept harder maps or maps that need more thought to be completed. It's like a bit harder version of bootcamp for experienced players.\n\nIf you want to be a room admin to use some special commands, join your room: %s"},
			[2] = {"Admin Commands", {
				[1] = {"\t<J>» Maps</J>\n", {
					[1] = "<VP>!%s</VP> - Pass the map!",
					[2] = "<VP>!%s</VP> - Reloads the current map!",
					[3] = "<VP>!%s</VP> <PS>@Code</PS> <R>or</R> <VP>!np <PS>@Code</PS></VP> - Loads a map!",
				}},
				[2] = {"\n\t<J>» Others</J>\n", {
					[1] = "<VP>!%s</VP> <PS>Time</PS> - Set the time of the current round",
					[2] = "<VP>!%s</VP> <PS>Time</PS> - Set the time of all the rounds",
					[3] = "<VP>!%s</VP> <PS>[[not] cheese]</PS> - Enables/Disables the checkpoint with or without cheese",
					[4] = "<VP>!%s</VP> <PS>[Password]</PS> - Sets/Unsets a password in the room",
				}},
			}},
			[3] = {"Keyboard Commands", {
				[1] = {"\t<J>» Checkpoint</J>\n", {
					[1] = "<VP>Key %s</VP> - Put a checkpoint",
					[2] = "<VP>Key %s</VP> - Remove a checkpoint",
				}},
				[2] = {"\n\t<J>» Others</J>\n", {
					[1] = "<VP>Key %s</VP> - Kill yourself",
					[2] = "<VP>Hold Key %s</VP> - Displays the time leaderboard for the current map",
					[3] = "<VP>!%s</VP> - Removes your cheese",
				}},
			}},
			[4] = {"Maps", "<J>Maps : %s\n\n\tAccess %s and send your map. Do not forget to read all the rules before!"},
			[5] = {"Thanks for", "<R>%s <G>- <N>Developer\n%s <G>- <N>Map evaluators"},
		},
	},
	ar = {
		welcome = "أهلا بك في <B>#Hardcamp</B>! أكتب !info لتري الأوامر\n\tالابلاغ عن المشاكل لـ Bolodefchoco#0000!",

		skip = "<VP>%s</VP> قام بتخطي الخريطة!",
		restart = "<VP>%s</VP> قام بإعادة الخريطة الحالية",
		loadmap = "<VP>%s</VP> قام بتحميل الخريطة %s!",
		settime = "تم تغيير  الوقت ل %s دقيقة!",
		setstandtime = "تم تعيين الوقت القياسي لجميع جولات ل %s دقيقة!",
		enabled = "تمكين! إضغط <B>E</B> لوضع نقطة البداية ة <B>Shift+E</B> لحذفها.",

		disabled = "تعطيل!",
	},
	br = {
		welcome = "Bem-vindo ao <B>#Hardcamp</B>! Digite !info para checar os comandos.\n\tVocê como admin: <I>/sala *#hardcamp0%s</I>\n\tReporte quaisquer problemas para Bolodefchoco#0000!",

		skip = "<VP>%s</VP> acabou de passar o mapa!",
		restart = "<VP>%s</VP> acabou de reiniciar o mapa atual!",
		loadmap = "<VP>%s</VP> acabou de carregar o mapa %s!",
		settime = "O tempo foi definido para %s minutos!",
		setstandtime = "O tempo padrão para todas as partidas foram definidas para %s minutos!",
		enabled = "ativado! Pressione <B>E</B> para marcar um checkpoint e <B>Shift+E</B> para remove-lo.",
		difficulty = "Dificuldade",

		disabled = "desativado!",

		menu = {
			[1] = {"%s", "\tA diferença entre o bootcamp normal e o Hardcamp é que aceitamos mapas mais difíceis que precisam de mais pensamento para serem completados. É uma versão um pouco mais dificultosa para jogadores experientes.\n\nSe você quiser ser um administrador da sala para usar alguns comandos especiais, entre na sala: %s"},
			[2] = {"Comandos de Admin", {
				[1] = {"\t<J>» Mapas</J>\n", {
					[1] = "<VP>!%s</VP> - Passa o mapa!",
					[2] = "<VP>!%s</VP> - Recarrega o mapa atual!",
					[3] = "<VP>!%s</VP> <PS>@Código</PS> <R>ou</R> <VP>!np <PS>@Código</PS></VP> - Carrega um mapa!",
				}},
				[2] = {"\n\t<J>» Outros</J>\n", {
					[1] = "<VP>!%s</VP> <PS>Tempo</PS> - Define o tempo do mapa atual",
					[2] = "<VP>!%s</VP> <PS>Tempo</PS> - Define o tempo para todos os rounds",
					[3] = "<VP>!%s</VP> <PS>[[not] cheese]</PS> - Ativa/Desativa o checkpoint com ou sem queijo",
					[4] = "<VP>!%s</VP> <PS>[Senha]</PS> - Define/remove uma senha para a sala",
				}},
			}},
			[3] = {"Comandos do Teclado", {
				[1] = {"\t<J>» Checkpoint</J>\n", {
					[1] = "<VP>Tecla %s</VP> - Por um checkpoint",
					[2] = "<VP>Tecla %s</VP> - Remover um checkpoint",
				}},
				[2] = {"\n\t<J>» Outros</J>\n", {
					[1] = "<VP>Tecla %s</VP> - Se matar",
					[2] = "<VP>Pressionar Tecla %s</VP> - Mostra o ranking de tempo do mapa atual",
					[3] = "<VP>!%s</VP> - Remove seu queijo",
				}},
			}},
			[4] = {"Mapas", "<J>Mapas : %s\n\n\tAccesse %s e envie seu mapa. Não se esqueça de ler todas as regras antes!"},
			[5] = {"Agradecimentos", "<R>%s <G>- <N>Desenvolvedor\n%s <G>- <N>Avaliadores de Mapas"},
		},
	},
	fr = {
		welcome = "Bienvenue dans <B>#Hardcamp</B>! Ecrivez !info pour prendre connaîssance des commandes\n\tVeuillez reporter tout problèmes à Bolodefchoco#0000!",

		skip = "<VP>%s</VP> vient de passer la carte!",
		restart = "<VP>%s</VP> vient de recharger la carte actuelle!",
		loadmap = "<VP>%s</VP> vient de charger la carte %s!",
		settime = "Le temps restant à été définie à %s minutes!",
		setstandtime = "Le temps général pour toutes les cartes à été définie à %s minutes!",
		enabled = "enabled! Appuyez sur <B>E</B> pour mettre un checkpoint et sur <B>Shift+E</B> pour le supprimer.",
		difficulty = "Difficulté",

		disabled = "désactivé!",

		menu = {
			[1] = {"%s", "\tLa différentre entre le bootcamp normal et Hardcamp est que nous acceptons des cartes plus dures et qui demandent plus de réflexion pour être complétées. C'est une version plus compliquée du bootcamp pour des joueurs expérimentés.\n\nSi vous voulez être admin dans un salon et utilisé des commandes spéciales, rejoignez le salon: %s"},
			[2] = {"Commandes Admin", {
				[1] = {"\t<J>» Cartes</J>\n", {
					[1] = "<VP>!%s</VP> - Passe la carte!",
					[2] = "<VP>!%s</VP> - Recharge la carte actuelle!",
					[3] = "<VP>!%s</VP> <PS>@Code</PS> <R>ou</R> <VP>!np @Code</VP> - Charge une carte!",
				}},
				[2] = {"\n\t<J>» Autres</J>\n", {
					[1] = "<VP>!%s</VP> <PS>Time</PS> - Définie le temps de la carte actuelle",
					[2] = "<VP>!%s</VP> <PS>Time</PS> - Définie le temps de toutes les cartes",
					[3] = "<VP>!%s</VP> <PS>[[not] cheese]</PS> - Active/Désactive les checkpoints avec ou sans fromage",
					[4] = "<VP>!%s</VP> <PS>[Mot de passe]</PS> - Ajoute/supprime un mot de passe au salon",
				}},
			}},
			[3] = {"Commandes de claviers", {
				[1] = {"\t<J>» Checkpoint</J>\n", {
						[1] = "<VP>Touche %s</VP> - Met un checkpoint",
						[2] = "<VP>Touche %s</VP> - Supprime un checkpoint",
				}},
				[2] = {"\n\t<J>» Autres</J>\n", {
					[1] = "<VP>Touche %s</VP> - Vous tue",
					[2] = "<VP>Maintenez la touche %s</VP> - Affiche le classement des temps sur la carte actuelle"
				}},
			}},
			[4] = {"Cartes", "<J>Cartes : %s\n\n\tCliquez sur %s et envoyez votre carte. N'oubliez pas de lire les règles avant!"},
			[5] = {"Remerciements", "<R>%s <G>- <N>Developeur\n%s <G>- <N>Evaluateurs de cartes"},
		},
	},
	pl = {
		welcome = "Witaj w <B>#Hardcamp</B>! Wpisz !info na czacie aby sprawdzić jakie są komendy\n\tZgłaszaj wszelkie błędy do Bolodefchoco#0000!",

		skip = "<VP>%s</VP> pominął/-ęła mapę!",
		restart = "<VP>%s</VP> zrestartował/-a mapę!",
		loadmap = "<VP>%s</VP> załadował/-a mapę %s!",
		settime = "Czas został ustawiony na %s minut!",
		setstandtime = "Standardowy czas dla wszystkich map został ustawiony na %s minut!",
		enabled = "włączony! Kliknij <B>E</B>, aby ustawić checkpoint i <B>Shift+E</B>, aby go usunąć.",

		disabled = "wyłączony!",
	},
}
local translation = translations[tfm.get.room.community] or translations.en

table.turnTable = function(x)
	return (type(x)=="table" and x or { x })
end
table.merge = function(this, src)
	for k, v in next, src do
		if this[k] then
			if type(v) == "table" then
				this[k] = table.turnTable(this[k])
				table.merge(this[k], v)
			else
				this[k] = this[k] or v
			end
		else
			this[k] = v
		end
	end
end

for k, v in next, translations do
	if k ~= "en" then
		table.merge(v, translations.en)
	end
end

-- Functions
table.list = function(tbl, sep, f, i, j)
	local out = {}

	sep = sep or ""

	i, j = (i or 1), (j or #tbl)

	local counter = 1
	for k, v in next, tbl do
		if type(k) ~= "number" or (k >= i and k <= j) then
			if f then
				out[counter] = f(k, v)
			else
				out[counter] = tostring(v)
			end
			counter = counter + 1
		end
	end

	return table.concat(out, sep)
end
string.nick = function(player, ignoreCheck)
	if not ignoreCheck and not player:find("#") then
		player = player .. "#0000"
	end

	return string.gsub(string.lower(player), "%a", string.upper, 1)
end
string.split = function(value, pattern, f)
	local out = {}
	for v in string.gmatch(value, pattern) do
		out[#out + 1] = (not f and v or f(v))
	end
	return out
end
local concat
concat = function(k, v)
	if type(v) == "table" then
		return table.list(v, "\n", function(i, j) return concat(i, j) end)
	else
		return v
	end
end

-- Encode
local encodeMaps
encodeMaps = function(list, one)
	if one then
		return "[" .. table.concat(list, ',') .. "]"
	else
		local out = { }
		for i = 1, #list do
			out[i] = encodeMaps(list[i], true)
		end
		return table.concat(out)
	end
end 

local decodeMaps = function(str)
	local out = string.split(str, "%[(.-)%]")
	for i = 1, #out do
		out[i] = string.split(out[i], "[^,]+", tonumber)
	end
	return out
end

-- Maps
local maps

local loading_maps = system.loadFile(module.map_file)
local reloader
reloader = system.newTimer(function()
	if not loading_maps then
		system.loadFile(module.map_file)
	end
end, 1000, true)
eventFileLoaded = function(id, data)
	system.removeTimer(reloader)
	reloader = nil

	maps = decodeMaps(data)
	for i = 1, #maps do
		maps[i].queue = maps[i]
	end
	maps.queue = { 2, 1, 3, 2, 1, 3, 2, 4 }

	do
		local shuffle = function(list)
			local index
			for i = #list, 1, -1 do
				index = math.random(i)
				list[index], list[i] = list[i], list[index]
			end
		end
		local set = function(list)
			local out = { }
			for _, index in next, list do
				out[index] = true
			end
			return out
		end

		maps.queue._next = 1
		maps.queue._lastCat = nil
		maps.queue._len = #maps.queue
		for i = 1, #maps do
			shuffle(maps[i].queue)
			maps[i] = {
				_next = 1,
				fBefore = maps[i].fBefore,
				fAfter = maps[i].fAfter,
				queue = maps[i].queue,
				_queueLen = #maps[i].queue,
				_hashedQueue = set(maps[i].queue)
			}
		end

		maps = setmetatable(maps, {
			__call = function(this, category)
				category = tonumber(category)
				local hasCat = not not category
				if not hasCat or not this[category] then
					category = this.queue[this.queue._next]
					if type(category) == "table" then
						category = category[math.random(#category)]
					end
					this.queue._next = this.queue._next % maps.queue._len + 1
				end
				this.queue._lastCat = category

				local map
				if hasCat then
					map = this[category].queue[math.random(this[category]._queueLen)]
				else
					map = this[category].queue[this[category]._next]

					if this[category]._next == this[category]._queueLen then
						shuffle(this[category].queue)
						this[category]._next = 1
					else
						this[category]._next = this[category]._next + 1
					end
				end

				if this[category].fBefore then
					this[category].fBefore(map)
				end

				return map
			end
		})
	end
	tfm.exec.setGameTime(4)
	eventLoop(0, 0)
end

-- System
local roomManagers = {
	["Auroraclears#0000"] = true,
	["Bolodefchoco#0000"] = true,
	["Mquk#0095"] = true,
	["Xorcist#0000"] = true
}
local roomAdmins = { }
for k, v in next, roomManagers do roomAdmins[k] = v end

local mapTimes = { }
local info = { }
local checkpoint = false
local respawnCheese = false

local setPodium
do
	local colors = { 0xF8BA00, 0x959595, 0x763C16, 0xD7D7E6 }
	setPodium = function()
		local players = { }
		for k, v in next, tfm.get.room.playerList do
			players[#players + 1] = { k, v.score }
		end
		table.sort(players, function(p1, p2) return p1[2] > p2[2] end)

		for i = 1, #players do
			tfm.exec.setNameColor(players[i][1], colors[(i>4 or players[i][2] < 1) and 4 or i])
		end
	end
end

local rank = function(showPos, showPoints, pointsName, lim)
	local source = #mapTimes > 0 and mapTimes or { {"?", 0} }
	local rank = ""
	local p = { }
	for i, j in next, source do
		p[#p + 1] = { name = j[1], v = j[2] }
	end
	table.sort(p, function(f, s) return f.v < s.v end)

	for o, n in next, p do
		if o <= lim then
			rank = rank .. (showPos and "<J>" .. o .. ". " or "") .. "<V>" .. n.name .. (showPoints and (" <BL>- <VP>" .. n.v .. " " .. (pointsName or "points") .. "\n") or "\n")
		end
	end
	return rank
end

-- UI
ui.menu = function(n)
	if not info[n].menu.accessing then
		info[n].menu.page = 1
		info[n].menu.accessing = true
	end

	local langue = translation.menu

	if info[n].menu.page < 1 then
		info[n].menu.page = #langue
	elseif info[n].menu.page > #langue then
		info[n].menu.page = 1
	end

	local popupFormat = "<%s><a href='event:menu.page.%d'>%s</a>"
	local popups = {}
	for k, v in next, langue do
		popups[#popups+1] = string.format(popupFormat, (k == info[n].menu.page and "PT" or "CEP"), k, string.format(v[1], string.nick("hardcamp", true)))
	end

	local displayText = {table.unpack(langue[info[n].menu.page])}

	if info[n].menu.page == 1 then
		displayText[1] = string.format(displayText[1], string.nick("hardcamp", true))
		displayText[2] = string.format(displayText[2], "\n<p align='center'><PT><a href='event:print./room #hardcamp0"..n.."'>/room #hardcamp0" .. n)
	else
		local textFormat = nil
		if info[n].menu.page == 2 then
			displayText[2] = table.list(displayText[2], "\n", function(k, v)
				return concat(k, v)
			end)
			displayText[2] = "<font size='10'>" .. string.format(displayText[2], commands.nextMap, commands.reloadMap, commands.newMap, commands.time, commands.standardTime, commands.checkpoint, commands.password)
		elseif info[n].menu.page == 3 then
			displayText[2] = table.list(displayText[2], "\n", function(k, v)
				return concat(k, v)
			end)
			displayText[2] = "<font size='10'>" .. string.format(displayText[2], commands.keyboard.checkpoint, commands.keyboard.removeCheckpoint, commands.keyboard.die, commands.keyboard.timeLeaderboard, commands.removecheese)

		elseif info[n].menu.page == 4 then
			local m = 0
			for i = 1, #maps do
				m = m + #maps[i].queue
			end
			displayText[2] = string.format(displayText[2], m.."<N>", "<BV><a href='event:print.atelier801¬com/topic?f=6&t=850791'>#HARDCAMP MAP SUBMISSIONS</a></BV>")
		elseif info[n].menu.page == 5 then
			displayText[2] = string.format(displayText[2], "Bolodefchoco#0000", "<BV>Mquk#0095, Xorcist#0000, Auroraclears#0000</BV>")
		end
	end

	ui.addTextArea(3, "<font size='1'>\n</font><p align='center'><J><B><a href='event:menu.right'>»</a>", n, 543, 352, 40, 20, 1, 1, 1, true)
	ui.addTextArea(4, "<font size='1'>\n</font><p align='center'><J><B><a href='event:menu.left'>«</a>", n, 217, 352, 40, 20, 1, 1, 1, true)

	ui.addTextArea(5, "<font size='11'><J>"..table.concat(popups, "\n\n"), n, 546, 107, 115, 155, 0x140C07, 1, 1, true)

	ui.addTextArea(6, "<p align='center'><B><R><a href='event:menu.close'>X", n, 543, 42, 20, 20, 1, 1, 1, true)
	ui.addTextArea(7, "<p align='center'><font size='20' color='#92CF91'><B>"..string.upper(displayText[1]).."</B></V><font size='15'>\n<R>_____________\n\n<font size='11'><N><p align='left'>"..displayText[2], n, 260, 42, 280, 330, 0x1E120B, 1, 1, true)
end

-- Events
local nextMap
currentTime = 0
eventLoop = function(currentTime, leftTime)
	_G.currentTime = currentTime
	if leftTime < 500 then
		if not nextMap then
			nextMap = maps()
		end
		tfm.exec.newGame(nextMap)
	end

	for p, d in next, info do
		if d.logo then
			d.logo_timer = d.logo_timer - .5
			if d.logo_timer <= 0 then
				tfm.exec.removeImage(d.logo)
			end
		end
	end
end

eventNewPlayer = function(n)
	if not info[n] then
		info[n] = {
			shift = false,
			checkpoint = {false, 0, 0, false},
			cheese = false,
			menu = {
				accessing = false,
				page = 1,
				timer = 0,
			},
			logo = tfm.exec.addImage("15d75ac6aa9.png", "&0", 120, 100, n),
			logo_timer = 6
		}
	end

	tfm.exec.respawnPlayer(n)

	for i = 1, 2 do
		system.bindKeyboard(n, 16, i==1, true)
		system.bindKeyboard(n, 76, i == 1, true) -- L
	end

	for k, v in next, {46, string.byte("HE", 1, 2)} do -- 46 is del
		system.bindKeyboard(n, v, true, true)
	end

	tfm.exec.chatMessage("<T>" .. string.format(translation.welcome, n) .. "\n\t<CEP>atelier801.com/topic?f=6&t=850791", n)
end

eventNewGame = function()
	if not maps or not maps.queue then return tfm.exec.setGameTime(0) end

	nextMap = nil
	if tfm.get.room.xmlMapInfo then
		local code = tonumber(tfm.get.room.xmlMapInfo.mapCode)
		local diff
		for j = 1, #maps do
			if maps[j]._hashedQueue[code] then
				diff = j
				break
			end
		end
		if diff then
			ui.setMapName("<J>" .. (tfm.get.room.xmlMapInfo and tfm.get.room.xmlMapInfo.author or "?") .. " <BL>- " .. tfm.get.room.currentMap .. "   <G>|<N>   " .. translation.difficulty .. " : <V>" .. diff)
		end
	end

	mapTimes = { }
	tfm.exec.setGameTime(module.time)

	for k, v in next, info do
		v.cheese = false
		v.checkpoint = { false, 0, 0, false }
		ui.removeTextArea(1, n)
	end
	setPodium()
end

eventKeyboard = function(n, k, d, x, y)
	if k == 16 then
		info[n].shift = d
	elseif k == string.byte("E") and checkpoint and not tfm.get.room.playerList[n].isDead then
		if info[n].shift then
			info[n].checkpoint = { false, 0, 0, info[n].checkpoint[4] }
			ui.removeTextArea(1, n)
		else
			info[n].checkpoint = {true, x, y, true}
			ui.addTextArea(1, "", n, x-5, y-5, 10, 10, 0x56A75A, 0x56A75A, .5, false)
		end
	elseif k == string.byte("L") then
		if d then
			ui.addTextArea(2, rank(true, true, "s", 20), n, 5, 30, nil, 200, nil, nil, .8, true)
		else
			ui.removeTextArea(2, n)
		end
	elseif k == string.byte("H") then
		eventChatCommand(n, "h")
	elseif k == 46 then
		tfm.exec.killPlayer(n)
	end
end

local toAdd, toRem, toSave = { }, { }
eventChatCommand = function(n, c)
	local p = string.split(c, "[^%s]+", string.lower)
	if p[1] == "info" or p[1] == "h" then
		if info[n].menu.accessing then
			eventTextAreaCallback(nil, n, "menu.close")
		else
			if os.time() > info[n].menu.timer then
				info[n].menu.timer = os.time() + 1e3
				ui.menu(n)
			end
		end
	elseif p[1] == "remcheese" then
		if tfm.get.room.playerList[n].hasCheese then
			info[n].cheese = false

			tfm.exec.removeCheese(n)
		end
	else
		if roomAdmins[n] then
			if p[1] == "next" and currentTime > 5000 then
				tfm.exec.newGame(maps())
				tfm.exec.chatMessage("<T>• " .. string.format(translation.skip, n))
			elseif p[1] == "again" and currentTime > 5000 then
				if tfm.get.room.currentMap then
					tfm.exec.newGame(tfm.get.room.currentMap)
					tfm.exec.chatMessage("<T>• " .. string.format(translation.restart, n))
				end
			elseif (p[1] == "np" or p[1] == "map") and currentTime > 5000 then
				if p[2] then
					if #p[2] == 1 then
						tfm.exec.newGame(maps(tonumber(p[2])))
						tfm.exec.chatMessage("<T>• " .. string.format(translation.loadmap, n, "Level " .. p[2]))
					else
						tfm.exec.newGame(p[2])
						tfm.exec.chatMessage("<T>• " .. string.format(translation.loadmap, n, string.find(p[2], "@") and p[2] or "@"..p[2]))
					end
				else
					tfm.exec.newGame(maps())
					tfm.exec.chatMessage("<T>• " .. string.format(translation.loadmap, n, "Random"))
				end

			elseif p[1] == "time" then
				p[2] = p[2] and tonumber(p[2]) or 6
				tfm.exec.setGameTime(p[2] * 60)
				tfm.exec.chatMessage(string.format(translation.settime, p[2]))
			elseif p[1] == "standtime" then
				p[2] = p[2] and tonumber(p[2]) or 6
				if p[2] > 0 and p[2] < 10 then
					module.time = p[2] * 60
					tfm.exec.chatMessage(string.format(translation.setstandtime, p[2]))
				end
			elseif p[1] == "checkpoint" then
				local attribute = false
				if p[2] then
					attribute = true
					if p[2] == "not" and p[3] and p[3] == "cheese" then
						respawnCheese = false
					elseif p[2] == "cheese" then
						respawnCheese = true
					else
						attribute = false
					end
				end

				if not (checkpoint and attribute) then
					checkpoint = not checkpoint
					tfm.exec.chatMessage("<T>Checkpoint " .. translation[checkpoint and "enabled" or "disabled"])

					if not checkpoint then
						ui.removeTextArea(1, nil)
						for k, v in next, info do
							v.checkpoint = { false, 0, 0, v.checkpoint[4] }
						end
						respawnCheese = false
						for k, v in next, info do
							v.cheese = false
						end
					end
				end
			elseif p[1] == "password" or p[1] == "pw" then
				tfm.exec.setRoomPassword(p[2])
				if p[2] then
					tfm.exec.chatMessage("<CE>The password has been set to <B>" .. p[2] .. "</B>", n)
				else
					tfm.exec.chatMessage("<CE>The password has been removed", n)
				end
			end
		end
		if roomManagers[n] then
			if p[1] == "list" then
				p[2] = tonumber(p[2])
				if not p[2] then
					return tfm.exec.chatMessage("<R>• Missing difficulty level parameter. (1 - 4)", n)
				end
				if p[2] > 0 and p[2] <= #maps then
					tfm.exec.chatMessage("\n<B>Maps with difficulty level " .. p[2] .. "</B>:\n" .. string.rep('-', 60), n)
					local out = "@" .. encodeMaps(maps[p[2]].queue, true):sub(2, -2):gsub(",", " @")
					for i = 1, #out, 901 do
						tfm.exec.chatMessage("<font size='11'><T>" .. string.sub(out, i, i + 900) .. "</T></font>", n)
					end
					tfm.exec.chatMessage(string.rep('-', 60), n)
				end
			elseif p[1] == "add" then
				if not p[3] then
					return tfm.exec.chatMessage("<R>• Missing map code. Syntax: !add level map_code [map_code ...]", n)
				end
				p[2] = tonumber(p[2])
				if not p[2] then
					return tfm.exec.chatMessage("<R>• Missing difficulty level parameter. (1 - 4). Syntax: !add level map_code [map_code ...]", n)
				end
				if p[2] > 0 and p[2] <= #maps then
					for i = 3, #p do
						if string.find(p[i], "^@") then
							p[i] = tonumber(string.sub(p[i], 2))
						else
							p[i] = tonumber(p[i])
						end

						if not maps[p[2]]._hashedQueue[p[i]] then
							maps[p[2]].queue[maps[p[2]]._queueLen + 1] = p[i]
							maps[p[2]]._queueLen = maps[p[2]]._queueLen + 1
							maps[p[2]]._hashedQueue[p[i]] = true

							toAdd[#toAdd + 1] = p[i]
							tfm.exec.chatMessage("<T>• Map @" .. p[i] .. " added to the level " .. p[2] .. " map queue!")
						end
					end
				end
			elseif p[1] == "rem" then
				if not p[2] then
					return tfm.exec.chatMessage("<R>• Missing map_code.", n)
				end

				for i = 2, #p do
					if string.find(p[i], "^@") then
						p[i] = string.sub(p[i], 2)
					end
					p[i] = tonumber(p[i])
					for j = 1, #maps do
						if maps[j]._hashedQueue[p[i]] then
							maps[j]._hashedQueue[p[i]] = nil
							for k = 1, maps[j]._queueLen do
								if maps[j].queue[k] == p[i] then
									table.remove(maps[j].queue, k)
									toRem[#toRem + 1] = p[i]
									tfm.exec.chatMessage("<T>• Map @" .. p[i] .. " removed from the level " .. j .. " map queue!")
									break
								end
							end
							maps[j]._queueLen = maps[j]._queueLen - 1
						end
					end
				end
			elseif p[1] == "save" then
				if #toAdd == 0 and #toRem == 0 then
					return tfm.exec.chatMessage("<R>• No updates available.", n)
				end

				if not toSave then
					toSave = { }
					for i = 1, #maps do
						toSave[i] = maps[i].queue
					end
					toSave = encodeMaps(toSave)
					tfm.exec.chatMessage("<O>Type <B>!save</B> to save the maps.\n<O>• <B>Update stats:</B>\n\t<BL>- Size : <N>" .. #toSave .. "kb\n\t<BL>- Editions : <T>+<N>" .. #toAdd .. " <R>-<N>" .. #toRem, n)
					if #toAdd > 0 then
						tfm.exec.chatMessage("<O>To add: <T><font size='10'>@" .. table.concat(toAdd, ' @') .. "</font>", n)
					end
					if #toRem > 0 then
						tfm.exec.chatMessage("<O>To remove: <T><font size='10'>@" .. table.concat(toRem, ' @') .. "</font>", n)
					end
				else
					toAdd = { }
					toRem = { }
					system.saveFile(toSave, module.map_file)
					toSave = nil
					tfm.exec.chatMessage("<T>• Saved.", n)
				end
			end
		end
	end
end

eventPlayerDied = function(n)
	system.newTimer(function()
		tfm.exec.respawnPlayer(n)

		if checkpoint and info[n].checkpoint[1] then
			tfm.exec.movePlayer(n, info[n].checkpoint[2], info[n].checkpoint[3])
			if info[n].cheese and respawnCheese then
				tfm.exec.giveCheese(n)
			end
		end
	end, 1500, false)
end

eventPlayerWon = function(n, t, time)
	info[n].cheese = false
	info[n].checkpoint = {false, 0, 0, info[n].checkpoint[4]}
	ui.removeTextArea(1, n)

	mapTimes[#mapTimes + 1] = {n .. (info[n].checkpoint[4] and "<R>*</R>" or ""), time/100}

	eventPlayerDied(n, true)
	if maps.queue._lastCat  then
		tfm.exec.setPlayerScore(n, maps.queue._lastCat, true)
	end

	tfm.exec.chatMessage(string.format("<ROSE>%s (%ss <PT>(%scheckpoint)</PT>)", n, time/100, info[n].checkpoint[4] and "" or "no "), n)
end

eventPlayerGetCheese = function(n)
	if checkpoint and respawnCheese then
		info[n].cheese = true
		info[n].checkpoint[4] = true
	end
end

eventTextAreaCallback = function(i, n, c)
	local p = string.split(c, "[^%.]+")
	if p[1] == "menu" and os.time() > info[n].menu.timer then
		info[n].menu.timer = os.time() + 750
		if p[2] == "page" and p[3] then
			info[n].menu.page = tonumber(p[3])
			ui.menu(n)
		elseif p[2] == "right" then
			info[n].menu.page = info[n].menu.page + 1
			ui.menu(n)
		elseif p[2] == "left" then
			info[n].menu.page = info[n].menu.page - 1
			ui.menu(n)
		elseif p[2] == "close" then
			for i = 7, 3, -1 do
				ui.removeTextArea(i, n)
			end
			info[n].menu.accessing = false
		end
	elseif p[1] == "print" then
		p[2] = string.gsub(p[2], "¬", ".")
		tfm.exec.chatMessage(string.format("<PT>[•] <BV>%s", p[2]), n)
	end
end

-- Room
if string.byte(tfm.get.room.name, 2) ~= 3 then -- Is room
	local info = string.match(tfm.get.room.name, "^*?#hardcamp%d+(.+)")
	if info then
		local admins = string.gsub(info, "%S+", function(value)
			roomAdmins[string.nick(value)] = true
		end)
	end
end

for k, v in next, tfm.get.room.playerList do
	tfm.exec.setPlayerScore(k, 0)
	eventNewPlayer(k)
end