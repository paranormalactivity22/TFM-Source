--Creator: Bolodefchoco
--Made in: 28/05/2016
--Last update: 27/07/2018

--[[ Data ]]--
data={ 
	-- Type, Level, Damage, Uses, Timer, Images(code,x,y)
	light = {
		t = 2, l = 30, d = 10, u = 10, m = 5000,
		i = {"155d05699c9.png",325,105},
	},
	lspeed = {
		t = 1, l = 0, d = 0, u = "Infinity", m = 1500,
		i = {"155d0565587.png",275,108},
	},
	whole = {
		t = 1, l = 10, d = 0, u = "Infinity", m = 2500,
		i = {"155d055f8d0.png",300,105},
	},
	dbjump = {
		t = 1, l = 10, d = 0, u = "Infinity", m = 3000,
		i = {"155d0560b19.png",310,110},
	},
	snova = {
		t = 2, l = 40, d = 20, u = 6, m = 6000,
		i = {"155d055d277.png",288,105},
	},
	helix = {
		t = 1, l = 20, d = 0, u = "Infinity", m = 2500,
		i = {"155d056201e.png",300,105},
	},
	dome = {
		t = 2, l = 20, d = 5, u = 15, m = 4000,
		i = {"155d05689b8.png",295,105},
	},
	ray = {
		t = 2, l = 0, d = 5, u = "Infinity", m = 1000,
		i = {"155d0567651.png",265,125},
	},
	dray = {
		t = 2, l = 70, d = 50, u = 1, m = 10000,
		i = {"155d05633dc.png",270,140},
	},
	hsmash = {
		t = 2, l = 50, d = 20, u = 10, m = 8000,
		i = {"155d055e49f.png",295,105},
	},
	dhug = {
		t = 3, l = 50, d = "Infinity", u = 8, m = 15000,
		i = {"155d0566680.png",300,105},
	},
	anom = {
		t = 4, l = 60, d = 0, u = 1, m = 10000,
		i = {"155d05645e0.png",270,130},
	},
	-- Timer next power
	timernp = 200,
	-- Additional time
	newtimer = 60,
	-- Ui timer
	uitimer = 800,
	-- Help commands
	help = {
		m = 3,
		c1 = "help",
		c2 = "powers",
		c3 = "healthbar",
		c4 = "hints",
		c5 = "messages",
		c6 = "align",
		c7 = "np",
		c8 = "langue",
		c9 = "maxplayers",
		c10 = "renamebot",
		c11 = "setnewtime",
		c12 = "admin",
		c13 = "profile",
		c14 = "quality",
		c15 = "rank",
		c16 = "map",
		l = "http://atelier801.com/topic?f=6&t=832659",
	},
	-- Name
	game = "Powers",
	botName = "Einstein",
	-- Life
	life = 100,
}
--[[ Vars ]]--
	-- Room admins
admins = {}
	-- Tables
maps = {6602343,6576101,6562101,6516460,6703747,6703751,6402787,6422045,3969874,4021639,3952121,6720637,6720600,6721110,6422055,6375156,6370960,6729762,6379260,6302281,6302178,6730125,6730148,6731380,6733122,6733411,6755053,5971883,6773401,6792905,6833553,6835357,6835351,6798088,6834984,6849838,6045163,4015685,6174131,6394667,6397861,5234134}
colors = {"2ECF73","B500FF","A0A0A0","5E5C9E","EED656","D95ED1","FF7100","CB546B","FEFFD7","D7FFE4","D7ECFF","FFFFFF","009D9D"}
podiumColors = {"00FFFF","00EBEB","00D8D8"}
mice={}
toDespawn={}
power=setmetatable({},{
	__newindex = function(a,b,c)
		if type(c) == "function" then
			rawset(a,b,function(...)
				local var = {...}
				if mice[var[1]] ~= nil then
					mice[var[1]].nPTimer = os.time() + data.timernp
				end
				c(table.unpack(var))
			end)
		else
			rawset(a,b,c)
		end
	end
})
botNames = {
	[1] = "Einstein",
	[2] = "Nikola Tesla",
	[3] = "Marie Curie",
	[4] = "Isaac Newton",
	[5] = "Hawking",
	[6] = "Freud",
	[7] = "Galileu",
	[8] = "Darwin",
	[9] = "Alan Turing",
	[10] = "Archimedes",
	[11] = "Franklin",
	[12] = "Drummond",
	[13] = "Armstrong",
	[14] = "Homer",
	[15] = "Sponge Bob",
	[16] = "Goku",
}
	-- Strings
bot = "<font color='#"..colors[#colors].."'><B>["..data.botName.."]</B></font> %s"
	-- Booleans
anomaly = false
deathhug = {false,0}
skip = false
newtimer = false
adminRoom = {false,false}
isRoom = tfm.get.room.name:byte(2) ~= 3
	-- Other
advice = 0
newp = 0
newmaptimer = 0
--[[ Translation EN BR PT ES AR NL PL FR CZ (TR) ]]--
T = {}
T.en = {
	titles = {
		title = {"Apprentice","Wizard","Professor","Researcher","Master","Lord of Spells","Prince of Spells","King of Magic","Omnipresent","Omniscient","Omnipotent","God","Alpha & Omega"},
		newlevel = "%s reached level %s",
		unlock = {
			unlocked = "You just unlocked the power: ",
			title = "<J>%s <G>just unlocked the title %s«%s»",
			[10] = "<N><I>Worm Hole</I><J> and <CEP><I>Double Jump</I><J>!",
			[20] = "<J><I>Dome</I> and <CS><I>Helix</I><J>!",
			[30] = "<J><I>Lightning</I>!",
			[40] = "<ROSE><I>Supernova</I><J>!",
			[50] = "<VP><I>Hulk Smash</I><J> and <R><I>Death Hug</I><J>!",
			[60] = "<VI><I>Anomaly</I><J>!",
			[70] = "<BV><I>Death Ray</I><J>!",		
		},
	},
	powers = {
		-- Name, Activate, Description
		[1] = {"Light Speed",{"← ←","→ →"},"Makes you teleport 255px in the chosen direction"},
		[2] = {"Ray",{"Key <U>Space</U>"},"Shoots a ray laser"},
		[3] = {"Worm Hole",{"↑↓","↓↑"},"Makes you teleport 200px in your direction"},
		[4] = {"Double Jump",{"↑↑"},"Enables you to do a double jump"},
		[5] = {"Dome",{"Facepalm Emote","<I>PROTECTOS</I> on chat"},"Creates a big dome"},
		[6] = {"Helix",{"Key <U>SHIFT</U>"},"Boosts you diagonally"},
		[7] = {"Lightning",{"Mouse (Click)"},"Summons a big Lightning"},
		[8] = {"Supernova",{"Key <U>CTRL</U>"},"Creates a big Supernova"},
		[9] = {"Hulk Smash",{"↓↓"},"Makes an animation of the original Hulk Smash"},
		[10] = {"Death Hug",{"Hug Emote"},"Kills who hugs you"},
		[11] = {"Anomaly",{"<I>ANOMALY</I> on chat (You must know that the match will rarely be successful)"},"Creates an Anomaly in the game!"},
		[12] = {"Death Ray",{"Key <U>P</U> for 30-40 times"},"Shoot a powerful ray"},
	},
	botMessages = {
		welcome = "<BV>Welcome to <CH>#%s<BV>. Type <CH>!%s<BV> for more informations!",
		roomplayers = "<R>To start the game, the room must have at least 2 players!",
		notplayers = "<BV>At least 6 players are needed for stats count.",
		alive = "<R>You must be alive to do this!",
		timernp = "<R>You must wait %sms to do this!",
		powerlimit = "You have reached the limit of use of this power! (%s)",
		newtimer = "%s seconds were added in this round! Enjoy!",
		allpowers = "Santa Claus gave a gift for you! If the room keep with 3 mice or less, you will be able to use ALL the powers!",
		nextmap = "%s will be the next map!",
		wnextmap = "%s will not be the next map!",
		anomaly = "<CH>THE ANOMALY IS HERE!",
		anomtim = "<R>The match was not found and the request was not successful! :( Wait %s seconds.",
		won = "<J>%s <G>won the round!",
	},
	enables = {
		healthbar = {
			on = "<VP>Healthbar enabled!",
			off = "<R>Healthbar disabled!",
		},
		messages = {
			on = "<VP>Messages enabled!",
			off = "<R>Messages disabled!",
		},
		hints = {
			on = "<VP>Hints enabled!",
			off = "<R>Hints disabled!",
		},
		bot = {
			on = "<VP>Bot messages enabled!",
			off = "<R>Bot messages disabled!",
		},
		graphics = {
			on = "<VP>Graphic: High",
			off = "<R>Graphic: Low",
		},
		pw = {
			on = "<VP>Password: %s",
			off = "<R>Password disabled.",
		},
	},
	help = {
		[1] = {"#%s!","<PT>#%s was developed and idealized by Bolodefchoco.\n\n<VP>Your objective in this minigame is to be <I>the survivor</I> during %s minutes using all your powers, being guided by %s!\n\n<R>Do NOT forget to ENABLE the particle effects (In options, next to the Café, the 7th option)."},
		[2] = {"Chat Commands","<VP>!%s <G>- Displays the Help message\n<VP>!%s <G>- Displays all the power informations\n<VP>!%s <G>- Activate/Deactivate the healthbar\n<VP>!%s <G>- Activate/Deactivate the hints\n<VP>!%s <G>- Activate/Deactivate the bot messages.\n<VP>!%s <PT>1/2/3/4 <G>- Changes the healthbar position\n<VP>!%s <PT>@Code <G>- Load a map (3 mice or less)\n<VP>!%s <PT>ID <G>- Changes the language of the game (For you, only)\n<VP>!%s <PT>PlayerName <G>- Displays your profile, or the profile of the specified player.\n<VP>!%s <G>- Changes the quality of the game.\n<VP>!%s <G>- Opens the leaderboard.\n<VP>!%s <PT>@Code <G>- Verifies if the map is in the official rotation."},
		[3] = {"Stats","<N>• <J>Level <G>- The highest level you can reach is %s.\n<N>• <J>Title <G>- The title of the current level (%s titles)\n<N>• <J>Experience <G>- Calculates how many points you already have and how many points you need to level up\n<N>• <J>Rounds <G>- Calculates how many rounds you have played\n<N>• <J>Wins <G>- Calculates how many victories you have <R>(+%s per victory or each 35 minutes)\n<N>• <J>Kills <G>- Calculates how many mice you have killed\n<N>• <J>Profile Ratio <G>- The ratio between <I>Rounds, Wins</I> and <I>Kills"},
		[4] = {"Maps","<CEP>Send your maps in here: %s\n\n<CS>The complete list of maps below: (%s)\n%s"},
		[5] = {"Admins","<PT>To create a room with admins, make sure to add the nickname after some numbers <VP>(/room %s)\n<R>Stats will not count if you change the round time or put the maximum players in the room in less than 8 players.\n\n<BV>!%s <CH>Number/String <G>- Changes the limit of players in the room (2-18)\n<BV>!%s <CH>Id <G>- Renames the bot\n<BV>!%s <CH>Time <G>- Changes the time of the rounds\n<BV>!%s <CH>Name <G>- Gives/Removes admin from someone"},
		[6] = {"Special Thanks","<R>Bolodefchoco <N>- CEO + EN Translation + Tradução BR\n<BV>Tocuto<J>eltuco <N>- Traducción ES + Little Code\n<BV>Error<CE>_404 <N>- الترجمة AR + Map evaluation\n<J>Squalleze <N>- Little Code\n<PT>Lukamoii <N>- Ideas\n<CE>Error_404, Ujkos, Kimsterjay, Pratton and Mabste <N>- Map Evaluation\n<BV>Chamelinct <N>- Traducción ES\n<BV>Distances en Kalkoen <N>- NL Translation\n<BV>Aanguson <N>- Tłumacz PL\n<BV>Animjarcanin <N>- Traduction FR\n<BV>Bublamorce <N>- CZ Překlad"},
	},
	hints = {
		[1] = "Do NOT forget to ENABLE the particle effects (In options, next to the Café, the 7th option).",
	},
	other = {
		close = "Close",
		powers_textformat = "<J>Type: <N>%s\n<J>Level: <N>%s\n<BV>Uses: <N>%s\n<VP>Activate: <N>%s\n<R>Damage: <N>%s\n<PS>%s",
		powers_types = {"Defense","Attack","Troll","God Mode"},
		profile_textformat = "<font color='#%s'><J>Level</J> %s\n<J>Title:</J> «%s»\n<J>Experience:</J> %s\n\n<J>Rounds:</J> %s\n<J>Wins:</J> %s\n<J>Kills:</J> %s\n\n<J>Playing Time:</J> %s\n<J>Profile Ratio:</J> %s%%",
	},
	admins = {
		iftrue = "<R>Stats will not count if you change the botName or the round time.",
		maxroom = "The limit of players has been set to %s",
		renamed = "%s has been renamed to %s",
		time = "The time standard has been set in %s min.",
		notadmin = "%s is no longer an admin!",
		isadmin = "%s is now an admin!",
	},
	ranking = {
		[1] = {"#Room Leaderboard","Displays the ranking of the room"},
		[2] = {"#Global Leaderboard","Displays the ranking of the whole game"},
	},
}
T.br = {
	titles = {
		title = {"Aprendiz","Bruxo","Professor","Pesquisador","Mestre","Senhor dos Feitiços","Príncipe dos Feitiços","Rei da Mágica","Onipresente","Onisciente","Onipotente","God","Alpha & Omega"},
		newlevel = "%s alcançou o nível %s",
		unlock = {
			unlocked = "Você acaba de desbloquear o poder: ",
			title = "<J>%s <G>desbloqueou o titulo %s«%s»",
			[10] = "<N><I>Buraco de Minhoca</I><J> e <CEP><I>Pulo Duplo</I><J>!",
			[20] = "<J><I>Domo</I> e <CS><I>Hélice</I><J>!",
			[30] = "<J><I>Relâmpago</I>!",
			[40] = "<ROSE><I>Supernova</I><J>!",
			[50] = "<VP><I>Hulk Esmaga</I><J> e <R><I>Abraço da Morte</I><J>!",
			[60] = "<VI><I>Anomalia</I><J>!",
			[70] = "<BV><I>Raio da Morte</I><J>!",
		},
	},
	powers = {
		[1] = {"Velocidade da Luz",{"← ← ","→ →"},"Teletransporta-o 255px na direção escolhida"},
		[2] = {"Raio",{"Tecla <U>Espaço</U>"},"Atira um raio laser"},
		[3] = {"Buraco de Minhoca",{"↑↓ <BL>|</BL> ↓↑"},"Teletransporta-o 200px em sua direção"},
		[4] = {"Salto Duplo",{"↑↑"},"Permite que você faça um salto duplo"},
		[5] = {"Domo",{"Emoção Facepalm","<I>PROTECTOS</I> no chat"},"Cria um grande domo"},
		[6] = {"Hélice",{"Tecla <U>SHIFT</U>"},"Te impulsiona diagonalmente"},
		[7] = {"Relâmpago",{"Mouse (Clique)"},"Invoca um grande Relâmpago"},
		[8] = {"Supernova",{"Tecla <U>CTRL</U>"},"Cria uma grande Supernova"},
		[9] = {"Hulk Esmaga",{"↓↓"},"Cria uma animação do original Hulk Esmaga"},
		[10] = {"Abraço da Morte",{"Emoção de Abraço"},"Mata quem abraça-lo"},
		[11] = {"Anomalia",{"<I>ANOMALY</I> no chat (Você deve saber que o padrão será, raramente, bem sucedido)"},"Cria uma Anomalia no jogo!"},
		[12] = {"Raio da Morte",{"Digite <U>P</U> por 30-40 vezes"},"Atira um poderoso raio"},
	},
	botMessages = {
		welcome = "<BV>Bem-vindo ao <CH>#%s<BV>. <BV>Digite <CH>!%s<BV> para mais informações!",
		roomplayers = "<R>Para começar o jogo, a sala deve ter pelo menos 2 jogadores!",
		notplayers = "<BV>São necessários pelo menos 6 jogadores para crescer de nível.",
		alive = "<R>Você deve estar vivo para fazer isto!",
		timernp = "<R>Você deve esperar %sms para fazer isto!",
		powerlimit = "Você atingiu o limite de uso deste poder! (%s)",
		newtimer = "%s segundos foram adicionados nesta partida! Aproveitem!",
		allpowers = "Noel trouxe presentes para vocês! Se a sala se manter com 3 ratos ou menos, todos vocês poderão usar TODOS os poderes!",
		nextmap = "%s será o próximo mapa!",
		wnextmap = "%s não será o próximo mapa!",
		anomaly = "<CH>A ANOMALIA ESTÁ AQUI!",
		anomtim = "<R>O padrão não foi bem sucedido e a anomalia foi negada! :( Aguarde %s segundos.",
		won = "<J>%s <G>ganhou a partida!",
	},
	enables = {
		healthbar = {
			on = "<VP>Barra de Vida ativada!",
			off = "<R>Barra de Vida desativada!",
		},
		messages = {
			on = "<VP>Mensagens ativadas!",
			off = "<R>Mensagens desativadas!",
		},
		hints = {
			on = "<VP>Avisos ativados!",
			off = "<R>Avisos desativados!",
		},
		bot = {
			on = "<VP>Mensagens do bot ativadas!",
			off = "<R>Mensagens do bot desativadas!",
		},
		graphics = {
			on = "<VP>Gráfico: Alto",
			off = "<R>Gráfico: Baixo",
		},
		pw = {
			on = "<VP>Senha: %s",
			off = "<R>Senha desativada.",
		},
	},
	help = {
		[1] = {"#%s!","<PT>#%s foi desenvolvido e idealizado por Bolodefchoco!\n\n<VP>Seu objetivo neste minigame é ser <I>o sobrevivente</I> durante %s minutos usando todos os seus poderes, sendo guiado por %s!\n\n<R>NÃO se esqueça de ATIVAR os efeitos especiais (Nas opções, ao lado do Café, a 7ª opção)."},
		[2] = {"Comandos do Chat","<VP>!%s <G>- Mostra a mensagem de ajuda\n<VP>!%s <G>- Mostra todas as informações dos poderes.\n<VP>!%s <G>- Ativar/Desativar a barra de vida.\n<VP>!%s <G>- Ativar/Desativar os avisos.\n<VP>!%s <G>- Ativar/Desativar as mensagens do bot.\n<VP>!%s <PT>1/2/3/4 <G>- Alterar a posição da barra de vida.\n<VP>!%s <PT>@Código <G>- Carrega um mapa (3 ratos ou menos)\n<VP>!%s <PT>ID <G>- Altera a tradução do jogo (Apenas para você)\n<VP>!%s <PT>Jogador <G>- Abre seu perfil, ou o perfil do jogador especificado.\n<VP>!%s <G>- Altera a qualidade do jogo.\n<VP>!%s <G>- Abre o ranking.\n<VP>!%s <PT>@Código <G>- Verifica se o mapa está na rotação oficial."},
		[3] = {"Estatísticas","<N>• <J>Nível <G>- O maior que nível que você pode alcançar é %s.\n<N>• <J>Título <G>- O título do nível atual (%s títulos)\n<N>• <J>Experiência <G>- Calcula quantos pontos você já tem e quantos você precisa para subir de nível\n<N>• <J>Partidas <G>- Calcula quantas partidas você já jogou\n<N>• <J>Vitórias <G>- Calcula quantas vitórias você tem <R>(+%s por vitória ou a cada 35 minutos)\n<N>• <J>Mortos <G>- Calcula quantos ratos você matou\n<N>• <J>Proporção do Perfil <G>- A proporção entre <I>Partidas, Vitórias</I> e <I>Mortos"},
		[4] = {"Mapas","<CEP>Envie seus mapas aqui: %s\n\n<CS>A lista completa de mapas abaixo: (%s)\n%s"},
		[5] = {"Admins","<PT>Para criar uma sala com admins, certifique-se de adicionar o nickname depois de alguns números <VP>(/sala %s)\n<R>Estatísticas não vão contar se você alterar o tempo de jogo ou colocar o número máximo de jogadores em menos de 8 jogadores.\n\n<BV>!%s <CH>Número/Texto <G>- Altera o limite de jogadores na sala (2-18)\n<BV>!%s <CH>Id <G>- Renomeia o bot\n<BV>!%s <CH>Tempo <G>- Altera o tempo padrão das partidas\n<BV>!%s <CH>Nome <G>- Dá/Remove admin para alguém"},
		[6] = {"Agradecimentos Especiais","<R>Bolodefchoco <N>- CEO + EN Translation + Tradução BR\n<BV>Tocuto<J>eltuco <N>- Traducción ES + Little Code\n<BV>Error<CE>_404 <N>- الترجمة AR + Map evaluation\n<J>Squalleze <N>- Little Code\n<PT>Lukamoii <N>- Ideas\n<CE>Error_404, Ujkos, Kimsterjay, Pratton and Mabste <N>- Map Evaluation\n<BV>Chamelinct <N>- Traducción ES\n<BV>Distances en Kalkoen <N>- NL Translation\n<BV>Aanguson <N>- Tłumacz PL\n<BV>Animjarcanin <N>- Traduction FR\n<BV>Bublamorce <N>- CZ Překl"},
	},
	hints = {
		[1] = "NÃO se esqueça de ATIVAR os efeitos especiais (Nas opções, ao lado do Café, a 7ª opção)!",
	},
	other = {
		close = "Fechar",
		powers_textformat = "<J>Tipo: <N>%s\n<J>Nível: <N>%s\n<BV>Usos: <N>%s\n<VP>Ativar: <N>%s\n<R>Dano: <N>%s\n<PS>%s",
		powers_types = {"Defesa","Ataque","Troll","Modo Deus"},
		profile_textformat = "<font color='#%s'><J>Nível</J> %s\n<J>Título:</J> «%s»\n<J>Experiência:</J> %s\n\n<J>Partidas:</J> %s\n<J>Vitórias:</J> %s\n<J>Mortos:</J> %s\n\n<J>Tempo de Jogo:</J> %s\n<J>Proporção do Perfil:</J> %s%%",
	},
	admins = {
		iftrue = "<R>Estatísticas não vão contar se você alterar o nome do bot ou o tempo de jogo.",
		maxroom = "O limite de jogadores foi definido para %s",
		renamed = "%s foi renomeado para %s",
		time = "O tempo padrão foi definido para %s min.",
		notadmin = "%s não é mais um admin!",
		isadmin = "%s agora é um admin!",
	},
	ranking = {
		[1] = {"#Ranking Sala","Mostra o ranking da sala"},
		[2] = {"#Ranking Global","Mostra o ranking do jogo inteiro"},
	},
}
T.es = {
	titles = {
		title = {"Aprendiz","Mago","Profesor","Rebuscador","Maestro","Señor de los Hechizos","Príncipe de los Hechizos","Rey de la Magia","Omnipresente","Omnisciente","Omnipotente","Dios","Alpha & Omega"},
		newlevel = "%s alcanzó el nivel %s",
		unlock = {
			unlocked = "Haz desbloqueado el poder: ",
			title = "<J>%s <G>desbloqueó el título %s«%s»",
			[10] = "<N><I>Agujero de Gusano</I><J> y <CEP><I>Doble Salto</I><J>!",
			[20] = "<J><I>Domo</I> y <CS><I>Hélice</I><J>!",
			[30] = "<J><I>Relámpago</I>!",
			[40] = "<ROSE><I>Supernova</I><J>!",
			[50] = "<VP><I>Aplastamiento de Hulk</I><J> y <R><I>Abrazo de la Muerte</I><J>!",
			[60] = "<VI><I>Anomalía</I><J>!",
			[70] = "<BV><I>Rayo de la muerte</I><J>!",		
		},		
	},
	powers = {
		[1] = {"Velocidad Luz",{"← ←","→ →"},"Te teletransporta 250px en la dirección elegida"},
		[2] = {"Rayo",{"Tecla <U>Espacio</U>"},"Dispara un rayo láser"},
		[3] = {"Agujero de gusano",{"↑↓","↓↑"},"Te teletransporta 200px en tu dirección"},
		[4] = {"Doble salto",{"↑↑"},"Te prooca un doble salto"},
		[5] = {"Domo",{"Emoción Facepalm ","<I>PROTECTOS</I> en el chat"},"Crea un gran domo"},
		[6] = {"Hélice",{"Tecla <U>SHIFT</U>"},"Te mueve diagonalmente"},
		[7] = {"Relámpago",{"Mouse (Clic)"},"Invoca un Relámpago"},
		[8] = {"Supernova",{"Tecla <U>CTRL</U>"},"Crea una gran Supernova"},
		[9] = {"Aplastamiento de Hulk",{"↓↓"},"Crea una animación del aplastamiento real de Hulk"},
		[10] = {"Abrazo de la muerte",{"Emoción del abrazo"},"Mata a quien te abrace"},
		[11] = {"Anomalía",{"<I>ANOMALY</I> en el chat ((Tienes que saber, que es muy raro que pase))"},"¡Crea una anomalía dentro de juego!"},
		[12] = {"Rayo de la muerte",{"Tecla <U>P</U> 30-40 veces"},"Dispara un poderoso rayo"},
	},
	botMessages = {
		welcome = "<BV>Bienvenido a <CH>#%s<BV>. ¡Escribe <CH>!%s<BV> para más información!",
		roomplayers = "<R>¡Para empezar el juego, la sala debe tener por lo menos 2 jugadores!",
		notplayers = "<BV>Por lo menos 6 jugadores son necesarios para que las estadísticas cuenten.",
		alive = "<R>¡Necesitas estar vivo para hacer esto!",
		timernp = "<R>¡Tienes que esperar 100ms para hacer esto!",
		powerlimit = "¡Haz pasado el límite de usos de ese poder! (%s)",
		newtimer = "¡Hemos añadido %s segundos al juego! ¡Disfrútalos!",
		allpowers = "¡Papá Noel tiene un regalo para tí! Si la sala sigue con 3 ratones o menos, ¡Tú vas a poder usar TODOS los poderes!",
		nextmap = "%s será el próximo mapa!",
		wnextmap = "%s no será el próximo mapa",
		anomaly = "<CH>¡LA ANOMALÍA ESTÁ AQUÍ!",
		anomtim = "<R>¡No tuviste suerte y no puedo llamar a la anomalía! :( Espera %s segundos.",
		won = "<J>%s <G>ha ganado la ronda!",
	},
	enables = {
		healthbar = {
			on = "<VP>¡Barra de vida activada!",
			off = "<R>¡Barra de vida desactivada!",
		},
		messages = {
			on = "<VP>¡Mensajes activados!",
			off = "<R>¡Mensajes desactivados!",
		},
		hints = {
			on = "<VP>Anuncios activados!",
			off = "<R>Anuncios desactivados!",
		},
		bot = {
			on = "<VP>Mensajes del bot activadas!",
			off = "<R>Mensajes del bot desactivadas!",
		},
		graphics = {
			on = "<VP>Gráfico: Alto",
			off = "<R>Gráfico: Bajo",
		},
		pw = {
			on = "<VP>Contraseña: %s",
			off = "<R>Contraseña desactivada.",
		},
	},
	help = {
		[1] = {"#%s!","<PT>#%s fue programado e idealizado por Bolodefchoco.\n\n<VP>Tu objetivo en este juego es ser <I>el sobreviviente</I> durante %s minutos usando tus poderes, el juego va a ser guiado por %s!\n\n<R>¡NO te olvides de ACTIVAR los efectos de partículas! (En opciones, después del Café, la séptima opción)."},
		[2] = {"Comandos del chat","<VP>!%s <G>- Muestra el mensaje de ayuda\n<VP>!%s <G>- Muestra toda la información de poderes\n<VP>!%s <G>- Activa/Desactiva la barra de vida\n<VP>!%s <G>- Activa/Desactiva los anuncios\n<VP>!%s <G>- Activar/Desactivar los mensajes del bot\n<VP>!%s <PT>1/2/3/4 <G>- Cambia la posición de la barra de vida\n<VP>!%s <PT>@Code <G>- Carga un mapa (3 jugadores o menos)\n<VP>!%s <PT>ID <G>- Cambia la traducción del juego (Solo para tí)\n<VP>!%s <PT>Jugador <G>- Muestra tu perfil, o el perfil de un jugador específico.\n<VP>!%s <G>- Cambia la calidad del juego.\n<VP>!%s <G>- Abre la tabla de posiciones.\n<VP>!%s <PT>@Code <G>- Verifica si el mapa está en la rotación oficial."},
		[3] = {"Estadísticas","<N>• <J>Nivel <G>- El nivel más alto al que puedes llegar es %s.\n<N>• <J>Título <G>- El título del nivel actual (%s títulos)\n<N>• <J>Experiencia <G>- Calcula cuántos puntos ya tienes y cuántos puntos necesitas para subir de nivel\n<N>• <J>Rondas <G>- Calcula cuántas rondas has jugado\n<N>• <J>Victorias <G>- Calcula cuántas victorias tienes <R>(+%s por victoria o cada 35 minutos)\n<N>• <J>Matanzas <G>- Calcula cuántos ratones has matado\n<N>• <J>Porcentaje del perfil <G>- El porcentaje entre <I>Rondas, Victorias</I> y <I>Matanzas"},
		[4] = {"Mapas","<CEP>Envía tus mapas aquí: %s\n\n<CS>La lista completa de mapas abajo: (%s)\n%s"},
		[5] = {"Admins","<PT>Para crear una sala con administradores, asegúrate de añadir el nombre de usuario luego de algunos números <VP>(/room %s)\n<R>Las estadísticas no contarán si cambias el tiempo de la ronda o poner el máximo de jugadores en menos de 8 jugadores.\n\n<BV>!%s <CH>Número/Texto <G>- Cambia el límite de jugadores en la sala (2-18)\n<BV>!%s <CH>Id <G>- Cambia el nombre del bot\n<BV>!%s <CH>Tiempo <G>- Cambia el tiempo de las rondas\n<BV>!%s <CH>Nombre <G>- Da/Remueve el poder de administrar de alguien"},
		[6] = {"Agradecimientos Especiales","<R>Bolodefchoco <N>- CEO + EN Translation + Tradução BR\n<BV>Tocuto<J>eltuco <N>- Traducción ES + Little Code\n<BV>Error<CE>_404 <N>- الترجمة AR + Map evaluation\n<J>Squalleze <N>- Little Code\n<PT>Lukamoii <N>- Ideas\n<CE>Error_404, Ujkos, Kimsterjay, Pratton and Mabste <N>- Map Evaluation\n<BV>Chamelinct <N>- Traducción ES\n<BV>Distances en Kalkoen <N>- NL Translation\n<BV>Aanguson <N>- Tłumacz PL\n<BV>Animjarcanin <N>- Traduction FR\n<BV>Bublamorce <N>- CZ Překl"},
	},
	hints = {
		[1] = "¡No te olvides de ACTIVAR los efectos de partículas! (En opciones, después del Café, la séptima opción).",
	},
	other = {
		close = "Cerrar",
		powers_textformat = "<J>Tipo: <N>%s\n<J>Nivel: <N>%s\n<BV>Usos: <N>%s\n<VP>Activación: <N>%s\n<R>Daño: <N>%s\n<PS>%s",
		powers_types = {"Defensa","Ataque","Troll","Modo Dios"},
		profile_textformat = "<font color='#%s'><J>Nivel</J> %s\n<J>Título:</J> «%s»\n<J>Experiencia:</J> %s\n\n<J>Rondas:</J> %s\n<J>Victorias:</J> %s\n<J>Matanzas:</J> %s\n\n<J>Tiempo de Juego:</J> %s\n<J>Porcentaje del perfil:</J> %s%%",
	},
	admins = {
		iftrue = "<R>Las estadísticas no contarán si cambias el nombre del bot o el tiempo de la ronda.",
		maxroom = "La cantidad máxima de jugadores se ha cambiado a %s",
		renamed = "%s se ha renombrado a %s",
		time = "El tiempo estándar se ha combiado a %s min.",
		notadmin = "%s ya no es un admin!",
		isadmin = "%s es ahora un admin!",
	},
	ranking = {
		[1] = {"#Ranking Sala","Muestra el ranking de la sala"},
		[2] = {"#Ranking Global","Muestra el ranking de todo el juego"},
	},
}
T.ar = {
	titles={
		title = {"المبتدئ","الساحر","البروفيسور","الباحث","السيد","سيد التعويذات","ملك التعويذات","ملك السحر","في جميع الأماكن","عالم","قادر على كل شيء","المتحكم","ألفا و اوميجا"},
		newlevel = "%s وصل الى المستوى %s",
		unlock = {
			unlocked = "لقد حصلت على القوة: ",
			title = "<J>%s <G>لقد حصل على اللقب %s«%s»",
			[10] = "<N><I>حفرة الدودة</I><J> و <CEP><I>القفزة المضاعفة</I><J>!",
			[20] = "<J><I>القبة</I> و <CS><I>الحلزون</I><J>!",
			[30] = "<J><I>الصاعقة</I>!",
			[40] = "<ROSE><I>سوبر نوفا</I><J>!",
			[50] = "<VP><I>التدمير الضخم</I><J> و <R><I>الحضن القاتل</I><J>!",
			[60] = "<VI><I>الغير طبيعي</I><J>!",
			[70] = "<BV><I>اشعة الموت</I><J>!",		
		},
	},
	powers = {
		[1] = {"سرعة الضوء",{"← ← ","→ →"},"تستطيع التنقل 225 بيكسل في الطريق المحدد"},
		[2] = {"شعاع",{"المفتاح <U>المسطرة</U>"},"تقوم باطلاق شعاع"},
		[3] = {"حفرة الدودة",{"↑↓","↓↑"},"تستطيع التنقل 200 بيكسل في الطريق المحدد"},
		[4] = {"اسوبر نوفا",{"↑↑"},"القفز ضعف مرة"},
		[5] = {"القبة",{"حركة الصفع على الوجه","<I>PROTECTOS</I> في المحادثة العامة"},"تصنع قبة كبيرة"},
		[6] = {"الحلزون",{"المفتاح <U>SHIFT</U>"},"الزيادة في الانحراف"},
		[7] = {"الصاعقة",{"الفأرة (اضغط)"},"استدعاء صاعقة كبيرة"},
		[8] = {"سوبر نوفا",{"المفتاح <U>CTRL</U>"},"تصنع انفجار كبير"},
		[9] = {"التدمير الضخم",{"↓↓"},"يصنع نسخة متحركة من التدمير الضخم"},
		[10] = {"الحضن القاتل",{"حركة الحضن"},"تقتل من تحضن"},
		[11] = {"الغير طبيعي",{"<I>ANOMALY</I> (في المحادثة العامة (يجب ان تعلم ان المبار"},"تقوم بصنع شيء غير طبيعي في اللعبة"},
		[12] = {"الشعاع القاتل",{"المفتاح <U>P</U> مرة 30-40  اضغط لمدة "},"تطلق شعاعا قويا"},
	},
	botMessages={
		welcome = "<BV>اهلا الى <CH>#%s<BV>. اكتب <CH>!%s<BV> لمزيد من المعلومات",
		roomplayers = "<R>لبدأ اللعبة , يجب ان تحتوي الغرفة على اكثر من 2 فأر",
		notplayers = "<BV>يجب ان يكون هناك على الأقل 6 لاعبين ليتم حساب الاحصائيات",
		alive = "<R>يجب ان تكون حي للقيام بذلك",
		timernp = "<R>يجب ان تنتظر 100 ميلي ثانية للقيام بذلك",
		powerlimit = "لقد وصلت الى الحد الأقصى لهذه القوة (%s)",
		newtimer = "%s ثانية تم اضافتها الى هذه المباراة استمتعوا!",
		allpowers = "لقد اعطاك سانتا هدية! اذا بقيت الغرفة 3 فئران او اقل, ستستطيع استعمال جميع القوى!",
		nextmap = "%s ستكون الخريطة التالية!",
		wnextmap = "%s لن تكون الخريطة التالية!",
		anomaly = "<CH>الغير طبيعي هنا!",
		anomtim = "<R>, لم يتم العثور على مباراة و الطلب لم ينجح :( انتظر 10 ثواني ",
		won = "<J>%s <G>فاز بالجولة!",
	},
	enables = {
		healthbar = {
			on = "<VP>تم تفعيل شريط الصحة!",
			off = "<R>تم تعطيل شريط الصحة!",
		},
		messages = {
			on = "<VP>تم تفعيل الرسائل!",
			off = "<R>تم تعطيل الرسائل!",
		},
		hints = {
			on = "<VP>تفعيل النصائح!",
			off = "<R>تعطيل النصائح!",
		},
		bot = {
			on = "<VP>تفعيل رسائل الروبوت!",
			off = "<R>تعطيل رسائل الروبوت!",
		},
		graphics = {
			on = "<VP>جرافيكس: عالي",
			off = "<R>جرافيكس: قليل",
		},
		pw = {
			on = "<VP>كلمة السر: %s",
			off = "<R>تم تعطيل كلمة السر.",
		},
	},
	help = {
		[1] = {"#%s!","<PT>#%s تم صنعها عن طريق اللاعب Bolodefchoco.\n\n<VP>ما عليك فعله في هذه اللعبة الصغيرة هو ان تصبح <I>الناجي</I> خلال %s دقيقة باستخدام جميع قواك, بقيادة %s!\n\n<R>لا تنسى تفعيل عرض المؤثرات الخاصة (في الاعدادات, بالقرب من الكافي, الاختيار السابع في الاعدادات)."},
		[2] = {"اوامر التحدث","<VP>!%s <G>- عرض رسالة المساعدة\n<VP>!%s <G>- عرض جميع معلومات القوى\n<VP>!%s <G>- تفعيل/تعطيل شريط الصحة\n<VP>!%s <G>- تفعيل/تعطيل المساعدات\n<VP>!%s <G>- تفعيل/تعطيل رسائل الروبوت.\n<VP>!%s <PT>1/2/3/4 <G>- تغيير موقع شريط الصحة\n<VP>!%s <PT>@رمز الخارطة <G>- اذا كنت في بيت القبيلة الخاص بك مع 3 فئران او اكثر, تستطيع تفعيل الخارطة (بدون جحر)\n<VP>!%s <PT>ID <G>- تغيير لغة اللعبة الصغيرة (فقط انت)\n<VP>!%s <PT>اسم اللاعب <G>- تعرض الملف الشخصي الخاص بك, او ملف شخصي لاعب محدد.\n<VP>!%s <G>- تغيير جودة اللعبة.\n<VP>!%s <G>- افتح لائحة المراكز.\n<VP>!%s <PT>@رمز <G>- لتأكد وجود الماب في اللعبة الصغيرة."},
		[3] = {"الاحصائيات","<N>• <J>المستوى <G>- اعلى مستوى تستطيع الحصول عليه هو %s.\n<N>• <J>اللقب <G>- اللقب في هذا المستوى (%s الألقاب)\n<N>• <J>المهارة <G>- تقوم بحساب كم نقاط لديك وكم نقاط تلزمك للانتقال الى المستوى التالي\n<N>• <J>الجولات <G>- حساب عدد الجولات التي تم لعبها\n<N>• <J>الفوز <G>- حساب كم فوز قمة بالحصول عليه <R>(+%s لكل فوز او كل 35 دقائق)\n<N>• <J>القتل <G>- حساب عدد الفئران التي قمت بقتلها\n<N>• <J>النسبة للملف الشخصي <G>- النسبة بين <I>الجولات, الفوز</I> و <I>القتل"},
		[4] = {"الخرائط","<CEP>ارسل الخرائط هنا: %s\n\n<CS>جميع الخرائط في هذه اللعبة الصغيرة:\n%s\n%s"},
		[5] = {"المدراء","<PT>>لصناعة غرفة مع مدراء, تأكد من وضع اسمك بعد عدة ارقام <VP>(/room %s)\n<R>الاحصائيات لن تحسب اذا قمت بتغيير توقيت الجولة او وضعت الحد الأقصى لللاعبين في الغرفة  8 لاعبين.\n\n<BV>!%s <CH>رقم/السلسلة <G>- تغيير عدد اللاعبين في الغرفة (3-20)\n<BV>!%s <CH>الاسم الجديد <G>- تغيير اسم الروبوت\n<BV>!%s <CH>الوقت <G>- تغيير توقيقت الجولات\n<BV>!%s <CH>الاسم <G>- اعطاء/ازالة القوى من شخص"},
		[6] = {"شكر خاص لـ","<R>Bolodefchoco <N>- CEO + EN Translation + Tradução BR\n<BV>Tocuto<J>eltuco <N>- Traducción ES + Little Code\n<BV>Error<CE>_404 <N>- الترجمة AR + Map evaluation\n<J>Squalleze <N>- Little Code\n<PT>Lukamoii <N>- Ideas\n<CE>Error_404, Ujkos, Kimsterjay, Pratton and Mabste <N>- Map Evaluation\n<BV>Chamelinct <N>- Traducción ES\n<BV>Distances en Kalkoen <N>- NL Translation\n<BV>Aanguson <N>- Tłumacz PL\n<BV>Animjarcanin <N>- Traduction FR\n<BV>Bublamorce <N>- CZ Překl"},
	},
	hints = {
		[1] = "لا تنسى تفعيل عرض المؤثرات الخاصة (في الاعدادات, بالقرب من الكافي, الاختيار السابع في الاعدادات) لتجاهل الاعلانات,اكتب",
	},
	other={
		close = "إغلاق النافذة",
		powers_textformat = "<J>النوع: <N>%s\n<J>المستوى: <N>%s\n<BV>عدد الاستخدامات: <N>%s\n<VP>تفعيل: <N>%s\n<R>الضرر: <N>%s\n<PS>%s",
		powers_types = {"دفاع","هجوم","المزاح","الخارق"},
		profile_textformat = "<font color='#%s'><J>المستوى</J> %s\n<J>اللقب:</J> «%s»\n<J>المهارة:</J> %s\n\n<J>الجولات:</J> %s\n<J>الفوز:</J> %s\n<J>القتل:</J> %s\n\n<J>وقت اللعب:</J> %s\n<J>الملف الشخصي النسبة:</J> %s%%",
	},
	admins = {
		iftrue = "<R>الاحصائيات لن تحسب اذا غيرة توقيت الغرفة او اسم الروبوت.",
		maxroom = "تم تغيير الحد الأقصى لللاعبين الى %s",
		renamed = "%s تم تغيير الاسم الى %s",
		time = "التوقيت العادي تم وضعه خلال %s دقيقة.",
		notadmin = "%s لم يعد مديرا!",
		isadmin = "%s اصبح مديرا!",
	},
	ranking = {
		[1] = {"#لائحة المراكز في الغرفة","تظهر المراكز في الغرفة"},
		[2] = {"#لائحة المراكز العالمية","تزهر المراكز الخاصة بالعالم"},
	},
}
T.nl = {
	titles = {
		title = {"Leerling","Tovenaar","Professor","Onderzoeker","Meester","Lord van de Spreuken","Prins van de Spreuken","Koning van Magie","Alomtegenwoordig","Alwetend","Almachtig","God","Alpha & Omega"},
		newlevel = "%s haalde level %s",
		unlock = {
			unlocked = "Je ontvangt de power: ",
			title = "<J>%s <G>heeft net power ontvangen %s«%s»",
			[10] = "<N><I>Tijdreizen</I><J> en <CEP><I>Dubbele Sprong</I><J>!",
			[20] = "<J><I>Koepel</I> en <CS><I>Helix</I><J>!",
			[30] = "<J><I>Lichtstraal</I>!",
			[40] = "<ROSE><I>Supernova</I><J>!",
			[50] = "<VP><I>Hulk Verplettering</I><J> en <R><I>Knuffeldood</I><J>!",
			[60] = "<VI><I>Gekte</I><J>!",
			[70] = "<BV><I>Dodenstraal</I><J>!",		
		},
	},
	powers = {
		[1] = {"Lichtstraal",{"← ←","→ →"},"Zorgt ervoor dat je 255x in de gekozen richting wordt geteleport"},
		[2] = {"Straal",{"Key <U>Spatie</U>"},"Schiet een ray laser"},
		[3] = {"Tijdreizen",{"↑↓","↓↑"},"Zorgt ervoor dat je 200px in je richting wordt geteleporteerd"},
		[4] = {"Dubbele Sprong",{"↑↑"},"Hiermee kun je een dubbele sprong doen."},
		[5] = {"Koepel",{"Facepalm Emotie","<I>PROTECTOS</I> on chat"},"Maakt een grote koepel"},
		[6] = {"Helix",{"Key <U>SHIFT</U>"},"Boosts je diagonaal"},
		[7] = {"Lichtstraal",{"Muis (Click)"},"Schiet een krachtige Straal"},
		[8] = {"Supernova",{"Key <U>CTRL</U>"},"Maakt een grote Supernova"},
		[9] = {"Hulk Verplettering",{"↓↓"},"Maakt een animatie van de originele Hulk Verplettering"},
		[10] = {"Knuffeldood",{"Knuffel Emotie"},"Iedereen die jou knuffelt, gaat dood."},
		[11] = {"Gekte",{"<I>ANOMALY</I> in de chat (Je moet weten dat de match zelden succesvol is)"},"Maakt een Gekte in het spel!"},
		[12] = {"Dodenstraal",{"Sleutel <U>P</U> voor 30-40 keer"},"Schiet een krachtige straal"},
	},
	botMessages = {
		welcome = "<BV>Welkom bij <CH>#%s<BV>. Type <CH>!%s<BV> voor meer informatie!",
		roomplayers = "<R>Om het spel te starten, moet de kamer ten minste 2 spelers hebben!",
		notplayers = "<BV>Ten minste 6 spelers zijn nodig, om de stats mee te laten tellen.",
		alive = "<R>Je moet leven om dit te kunnen doen!",
		timernp = "<R>Je moet %sms wachten om dit te kunnen doen!",
		powerlimit = "Je hebt de limit bereikt om deze power te gebruiken! (%s)",
		newtimer = "%s secondes zijn toegevoegd aan de ronde! Veel plezier!",
		allpowers = "De Kerstman gaf je een cadeau! Als de kamer met 3 of minder spelers blijft, zul je alle powers kunnen gebruiken!",
		nextmap = "%s zal de volgende map worden!",
		wnextmap = "%s zal de volgende map niet worden!",
		anomaly = "<CH>DE GEKTE IS HIER!",
		anomtim = "<R>De match was niet gevonden en de aanvraag was niet succesvol! :( Wacht %s secondes.",
		won = "<J>%s <G>heeft de ronde gewonnen!",
	},
	enables = {
		healthbar = {
			on = "<VP>Gezondheidsbalk ingeschakeld!",
			off = "<R>Gezondheidsbalk uitgeschakeld!",
		},
		messages = {
			on = "<VP>Berichten ingeschakeld!",
			off = "<R>Berichten uitgeschakeld!",
		},
		hints = {
			on = "<VP>Hints ingeschakeld!",
			off = "<R>Hints uitgeschakeld!",
		},
		bot = {
			on = "<VP>Bot berichten ingeschakeld!",
			off = "<R>Bot Berichten uitgeschakeld!",
		},
		graphics = {
			on = "<VP>Grafisch: Hoog",
			off = "<R>Grafisch: Laag",
		},
		pw = {
			on = "<VP>Wachtwoord: %s",
			off = "<R>Wachtwoord uitgeschakeld.",
		},
	},
	help = {
		[1] = {"#%s!","<PT>#%s werd ontwikkeld en geïdealiseerd door Bolodefchoco.\n\n<VP>Je doel in deze minigame is om als <I>de overlevende</I> gedurende %s minuten al je powers te gebruiken. Je wordt geleid door %s!\n\n<R>Vergeet NIET om de special effects AAN te zetten (In opties, naast het Café, de 7e optie)."},
		[2] = {"Chat Commando's","<VP>!%s <G>- Laat het HELP bericht zien\n<VP>!%s <G>- Laat alle Power informatie zien\n<VP>!%s <G>- Schakelt de gezondheidsbalk aan of uit\n<VP>!%s <G>- Schakelt de hints aan of uit\n<VP>!%s <G>- Schakelt de berichten aan of uit\n<VP>!%s <PT>1/2/3/4 <G>- Verandert de gezondheidsbalk\n<VP>!%s <PT>@Code <G>- Laadt een map (3 muizen of minder)\n<VP>!%s <PT>ID <G>- Verandert de taal in het spel (Voor jou, alleen)\n<VP>!%s <PT>SpelerNaam <G>- Toont je profiel, of het profiel van een specifieke speler.\n<VP>!%s <G>- Verandert de kwaliteit van het spel.\n<VP>!%s <G>- Opent de leaderboard.\n<VP>!%s <PT>@Code <G>- Controleert of de map in de officiële rotatie is."},
		[3] = {"Stats","<N>• <J>Level <G>- De hoogste level die je kunt behalen is %s.\n<N>• <J>Titel <G>- De titel van je huidige level (%s titels)\n<N>• <J>Ervaring <G>- Rekent uit hoeveel punten je hebt en hoeveel punten je nodig hebt om level up te komen\n<N>• <J>Rondes <G>- Rekent uit hoeveel rondes je hebt gespeeld\n<N>• <J>Overwinningen <G>- Rekent uit hoevaak je hebt gewonnen <R>(+%s per win of elke 35 minuten)\n<N>• <J>Gedood <G>- Rekent uit hoeveel muizen je hebt gedood\n<N>• <J>Profiel Ratio <G>- De ratio tussen <I>Rondes, Wins</I> en <I>Gedood"},
		[4] = {"Maps","<CEP>Stuurt je map hierin: %s\n\n<CS>De complete maplijst hieronder: (%s)\n%s"},
		[5] = {"Admins","<PT>Om een kamer te maken met een admin, zorg ervoor om de gebruikersnaam toe te voegen achter wat nummers <VP>(/room %s)\n<R>Stats tellen niet mee, als je de tijd van een ronde aanpast als je de maximale spelersaantal veranderd naar minder dan 8 in de kamer.\n\n<BV>!%s <CH>Nummer/String <G>- Verandert het limiet aan muizen in de kamer (2-18)\n<BV>!%s <CH>Id <G>- Verandert de naam van de bot\n<BV>!%s <CH>Tijd <G>- Verandert de tijd van de ronde\n<BV>!%s <CH>Naam <G>- Maak/verwijder iemand als admin"},
		[6] = {"Speciale Dank","<R>Bolodefchoco <N>- CEO + EN Translation + Tradução BR\n<BV>Tocuto<J>eltuco <N>- Traducción ES + Little Code\n<BV>Error<CE>_404 <N>- الترجمة AR + Map evaluation\n<J>Squalleze <N>- Little Code\n<PT>Lukamoii <N>- Ideas\n<CE>Error_404, Ujkos, Kimsterjay, Pratton and Mabste <N>- Map Evaluation\n<BV>Chamelinct <N>- Traducción ES\n<BV>Distances en Kalkoen <N>- NL Translation\n<BV>Aanguson <N>- Tłumacz PL\n<BV>Animjarcanin <N>- Traduction FR\n<BV>Bublamorce <N>- CZ Překl"},
	},
	hints = {
		[1] = "Vergeet NIET om de special Effects in te schakelen (In opties, naast het Café, de 7e optie).",
	},
	other = {
		close = "Sluit",
		powers_textformat = "<J>Type: <N>%s\n<J>Level: <N>%s\n<BV>Gebruikt: <N>%s\n<VP>Activeer: <N>%s\n<R>Beschadigd: <N>%s\n<PS>%s",
		powers_types = {"Verdedigen","Aanvallen","Troll","God Mode"},
		profile_textformat = "<font color='#%s'><J>Level</J> %s\n<J>Titel:</J> «%s»\n<J>Ervaring:</J> %s\n\n<J>Rondes:</J> %s\n<J>Wins:</J> %s\n<J>Gedood:</J> %s\n\n<J>Gespeelde Tijd:</J> %s\n<J>Profiel Ratio:</J> %s%%",
	},
	admins = {
		iftrue = "<R>Stats zullen niet tellen, als je de botName of de tijd van de ronde veranderd.",
		maxroom = "De limit van spelers is veranderd naar %s",
		renamed = "%s is hernoemd naar %s",
		time = "De standaard tijd is veranderd naar %s min.",
		notadmin = "%s is niet langer een admin!",
		isadmin = "%s is nu een admin!",
	},
	ranking = {
		[1] = {"#Kamer Leaderboard","Toont de ranking van de kamer"},
		[2] = {"#Globale Leaderboard","Toont de ranking van het hele spel"},
	},
}
T.pl = {
	titles = {
		title = {"Uczeń","Czarodziej","Profesor","Badacz","Mistrz","Władca Zaklęć","Książe Zaklęć","Król Magii","Wszechobecny","Wszechwiedzący","Wszechpotężny","Bóg","Alfa i Omega"},
		newlevel = "%s osiągnął poziom %s",
		unlock = {
			unlocked = "Właśnie odblokowałeś nową moc: ",
			title = "<J>%s <G>właśnie odblokował tytuł %s«%s»",
			[10] = "<N><I>Czarna Dziura</I><J> i <CEP><I>Podwójny Skok</I><J>!",
			[20] = "<J><I>Kopuła</I> i <CS><I>Helisa</I><J>!",
			[30] = "<J><I>Błyskawica</I>!",
			[40] = "<ROSE><I>Supernowa</I><J>!",
			[50] = "<VP><I>Hulk Miażdzyć</I><J> and <R><I>Zabójczy Uścisk</I><J>!",
			[60] = "<VI><I>Anomalia</I><J>!",
			[70] = "<BV><I>Promień Śmierci</I><J>!",		
		},
	},
	powers = {
		[1] = {"Nadprędkość",{"← ←","→ →"},"Sprawia, że teleportujesz się 255 pikseli w wybranym kierunku"},
		[2] = {"Promień",{"Klawisz <U>Spacji</U>"},"Wystrzeliwujesz promień lasera"},
		[3] = {"Czarna Dziura",{"↑↓","↓↑"},"Sprawia, że teleportujesz się 200 pikseli w wybranym kierunku"},
		[4] = {"Podwójny Skok",{"↑↑"},"Pozwala skoczyć drugi raz"},
		[5] = {"Kopuła",{"Emotikona \"Facepalm\"","<I>PROTECTOS</I> na czacie"},"Tworzy dużą kopułę"},
		[6] = {"Helisa",{"Klawisz <U>SHIFT</U>"},"Przyśpiesza Cię po przekątnej"},
		[7] = {"Błyskawica",{"Kliknięcię myszką"},"Przywołuję wielką Błyskawicę"},
		[8] = {"Supernowa",{"Key <U>CTRL</U>"},"Tworzy dużą Supernowę"},
		[9] = {"Hulk Miażdzyć",{"↓↓"},"Tworzy animację oryginalnego \"Hulk Miażdzyć\""},
		[10] = {"Zabójczy Uścisk",{"Emotikona Przytulenia"},"Zabija każdego, kto Cię przytuli"},
		[11] = {"Anomalia",{"<I>ANOMALY</I> na czacie (Musisz wiedzieć, że gra żadko będzie udana)"},"Tworzy Anomalię w grze!"},
		[12] = {"Promień Śmierci",{"Klawisz<U>P</U> 30-40 razy"},"Wystrzeliwuje potężny promień."},
	},
	botMessages = {
		welcome = "<BV>Witaj w <CH>#%s<BV>. Wpisz <CH>!%s<BV>, aby dowiedzieć się więcej!",
		roomplayers = "<R>Aby zacząć grę, w pokoju musi być przynajmniej 2 graczy!",
		notplayers = "<BV>Musi być przynajmniej 6 graczy, aby naliczane były statystyki.",
		alive = "<R>Aby to zrobić, musisz być żywy!",
		timernp = "<R>Musisz poczekać %s milisekund, aby to zrobić!",
		powerlimit = "Osiągnąłeś limit użyć danej mocy! (%s)",
		newtimer = "Do rundy zostało dodanych %s sekund! Miłej gry!",
		allpowers = "Święty Mikołaj dał Ci prezent! Jeśli w pokoju będzie 3 myszy lub mniej, będziesz mógł użyć WSZYSTKICH mocy!",
		nextmap = "%s będzie następną mapą!",
		wnextmap = "%s nie będzie następną mapą!",
		anomaly = "<CH>ANOMALIA NADESZŁA!",
		anomtim = "<R>Gra nie została odnaleziona, a proźba została odrzucona! :( Zaczekaj %s sekund.",
		won = "<J>%s <G>wygrał rundę!",
	},
	enables = {
		healthbar = {
			on = "<VP>Pasek życia włączony!",
			off = "<R>Pasek życia wyłączony!",
		},
		messages = {
			on = "<VP>Wiadomości włączone!",
			off = "<R>Wiadomości wyłączone!",
		},
		hints = {
			on = "<VP>Wskazówki włączone!",
			off = "<R>Wskazówki wyłączone!",
		},
		bot = {
			on = "<VP>Wiadomości bota włączone!",
			off = "<R>Wiadomości bota wyłączone!",
		},
		graphics = {
			on = "<VP>Grafika: Wysoka",
			off = "<R>Grafika: Niska",
		},
		pw = {
			on = "<VP>Hasło: %s",
			off = "<R>Hasło wyłączone.",
		},
	},
	help = {
		[1] = {"#%s!","<PT>#%s została was stworzona przez Bolodefchoco.\n\n<VP>W tej minigrze twoim celem jest zostanie <I>ocalałym</I> podczas %s minut używając wszystkich swoich mocy, kierując się pomocą %s!\n\n<R>Nie zapomnij WŁĄCZYĆ efektów cząsteczkowych (W opcjach obok Café, 7 opcja)."},
		[2] = {"Komendy Czatu","<VP>!%s <G>- Wyświetla wiadomość Pomocy\n<VP>!%s <G>- Wyświetla informacje o wszystkich mocach\n<VP>!%s <G>- Aktywuje/Dezaktywuje pasek życia\n<VP>!%s <G>- Aktywuje/Dezaktywuje wskazówki\n<VP>!%s <G>- Aktywuje/Dezaktywuje wiadomości bota.\n<VP>!%s <PT>1/2/3/4 <G>- zmienia pozycje paska życia\n<VP>!%s <PT>@Kod <G>- Ładuje mapę (3 lub mniej mysz)\n<VP>!%s <PT>ID <G>- Zmienia język gry (Tylko tobie)\n<VP>!%s <PT>Nazwa_Gracza <G>- Wyświetla twój profi, lub profil określonego gracza.\n<VP>!%s <G>- Zmienia jakość gry.\n<VP>!%s <G>- Otwiera ranking.\n<VP>!%s <PT>@Kod <G>- Sprawdza, czy mapa jest w oficjalnej rotacji."},
		[3] = {"Statystyki","<N>• <J>Poziom <G>- Najwyższy poziom jaki możesz osiągnąć to %s\n<N>• <J>Tytuł <G>- Tytuł danego poziomu (%s tytułów)\n<N>• <J>Doświadczenie <G>- Pokazuje ile punktów posiadasz, a także ile ci brakuje do następnego poziomu\n<N>• <J>Rundy <G>- Pokazuje ile rund rozegrałeś\n<N>• <J>Wygrane <G>- Pokazuje ile zwycięstw masz na swoim koncie<R>(+%s za zwycięstwo lub co 10 minut)\n<N>• <J>Zabójstwa <G>- Pokazuje ile myszy zabiłeś\n<N>• <J>Współczynnik profilu <G>- Stosunek między <I>Rundami, Wygranymi,</I> a <I>Zabójstwami"},
		[4] = {"Mapy","<CEP>Wysślij swoje mapy tu: %s\n\n<CS>Kompletna lista map poniżej: (%s)\n%s"},
		[5] = {"Administratorzy","<PT>Aby stworzyć pokój z administratorami, dodaj swoją nazwę użytkownika po dowolnej liczbie <VP>(/room %s)\n<R> Statystyki nie będą naliczane jeśli zmienisz czas rundy lub ustawisz maksymalną liczbę graczy na 8 lub mniej\n\n<BV>!%s <CH>Liczba <G>- Zmienia limit graczy w pokoju (2-18)\n<BV>!%s <CH>Nazwa <G>- Zmienia nazwę bota\n<BV>!%s <CH>Czas <G>- Zmienia czas trwania rund\n<BV>!%s <CH>Nazwa <G>- Daje/Usuwa uprawnienia administratora z wybranej osoby."},
		[6] = {"Specjalne podziękowania","<R>Bolodefchoco <N>- CEO + EN Translation + Tradução BR\n<BV>Tocuto<J>eltuco <N>- Traducción ES + Little Code\n<BV>Error<CE>_404 <N>- الترجمة AR + Map evaluation\n<J>Squalleze <N>- Little Code\n<PT>Lukamoii <N>- Ideas\n<CE>Error_404, Ujkos, Kimsterjay, Pratton and Mabste <N>- Map Evaluation\n<BV>Chamelinct <N>- Traducción ES\n<BV>Distances en Kalkoen <N>- NL Translation\n<BV>Aanguson <N>- Tłumacz PL\n<BV>Animjarcanin <N>- Traduction FR\n<BV>Bublamorce <N>- CZ Překl"},
	},
	hints = {
		[1] = "Nie zapomnij WŁĄCZYĆ efektów cząsteczkowych (W opcjach obok Café, 7 opcja).",
	},
	other = {
		close = "Zamknij",
		powers_textformat = "<J>Typ: <N>%s\n<J>Poziom: <N>%s\n<BV>Użyć: <N>%s\n<VP>Aktywacja: <N>%s\n<R>Obrażenia: <N>%s\n<PS>%s",
		powers_types = {"Obrona","Atak","Troll","Tryb Boski"},
		profile_textformat = "<font color='#%s'><J>Poziom</J> %s\n<J>Tytuł:</J> «%s»\n<J>Doświadczenie:</J> %s\n\n<J>Rundy:</J> %s\n<J>Wygrane:</J> %s\n<J>Zabójstwa:</J> %s\n\n<J>Czas Gry:</J> %s\n<J>Współczynnik profilu:</J> %s%%",
	},
	admins = {
		iftrue = "<R>Statystyki nie będą naliczane, jeśli zmienisz nazwę Bota lub czas trwania rundy.",
		maxroom = "Limit graczy został ustawiony na %s",
		renamed = "Nazwa %s została zmieniona na %s",
		time = "Czas został zmieniony na %s minut",
		notadmin = "%s nie ma już uprawnień administratora!",
		isadmin = "%s ma od teraz uprawnienia administratora!",
	},
	ranking = {
		[1] = {"#Ranking Pokoju","Wyświetla ranking pokoju"},
		[2] = {"#Ranking Globalny","Wyświetla ranking gry"},
	},
}
T.fr = {
	titles = {
		title = {"Apprenti","Sorcier","Professeur","Chercheur","Maitre","Seigneur","Prince","Roi","Omnipresent","Omniscient","Omnipotent","Dieu","Alpha & Omega"},
		newlevel = "%s a atteint le level %s",
		unlock = {
			unlocked = "Vous venez de débloquer le pouvoir : ",
			title = "<J>%s <G>jvient de débloquer le titre %s«%s»",
			[10] = "<N><I>Wormhole</I><J> et <CEP><I>double-saut</I><J>!",
			[20] = "<J><I>Dôme</I> et <CS><I>Helix</I><J>!",
			[30] = "<J><I>Éclair</I>!",
			[40] = "<ROSE><I>Supernova</I><J>!",
			[50] = "<VP><I>Hulk Smash</I><J> et <R><I>Death Hug</I><J>!",
			[60] = "<VI><I>Anomalie</I><J>!",
			[70] = "<BV><I>Rayon de la mort</I><J>!",		
		},
	},
	powers = {
		[1] = {"Propulsion",{"← ←","→ →"},"Te propulse à 255px dans la direction choisie"},
		[2] = {"Rayon",{"Barre d'<U>espace</U>"},"Tire un rayon laser"},
		[3] = {"Wormhole",{"↑↓","↓↑"},"Te propulse à 200px dans ta direction"},
		[4] = {"Double-saut",{"↑↑"},"Active le double-saut"},
		[5] = {"Dôme",{"Emote facepalm","Écrire <I>PROTECTOS</I> dans le tchat"},"Crée un grand dôme"},
		[6] = {"Helix",{"Touche <U>SHIFT</U>"},"Te propulse en diagonal"},
		[7] = {"Éclair",{"Souris (Clic)"},"Invoque un bel éclair"},
		[8] = {"Supernova",{"Touche <U>CTRL</U>"},"Crée une grande Supernova"},
		[9] = {"Hulk Smash",{"↓↓"},"Produit une animation Hulk Smash"},
		[10] = {"Calin de la mort",{"Emote câlin"},"Tue ceux qui te font un câlin"},
		[11] = {"Anomalie",{"Écrire <I>ANOMALY</I> dans le tchat (fonctionne rarement)"},"Crée une anomalie dans le jeu"},
		[12] = {"Rayon de la mort",{"Touche <U>P</U> 30 à 40 fois"},"Tire un rayon très puissant"},
	},
	botMessages = {
		welcome = "<BV>Bienvenue sur le module <CH>#%s<BV>. Utilise la commande <CH>!%s<BV> pour plus d'informations !",
		roomplayers = "<R>Pour commencer une partie, le salon doit contenir au moins deux joueurs !",
		notplayers = "<BV>Six joueurs minimum sont requis pour la comptabilisation des statistiques.",
		alive = "<R>Vous ne pouvez pas faire ça : vous êtes mort !",
		timernp = "<R>Vous devez attendre %sms pour pouvoir faire ça.",
		powerlimit = "Vous avez atteint la limite d'utilisation de cette compétence. (%s)",
		newtimer = "%s secondes ont été ajoutées à cette partie. Amusez-vous bien !",
		allpowers = "Le Père Noël vous a offert un cadeau ! Tant que le salon ne dépasse pas le nombre de trois souris présentes, vous pouvez utiliser TOUS les pouvoirs !",
		nextmap = "%s sera la prochaine carte.",
		wnextmap = "%s ne sera pas la prochaine carte.",
		anomaly = "<CH>Virus informatique o/",
		anomtim = "<R>Oups, ça n'a pas matché! :( Attendez %s secondes.",
		won = "<J>%s <G>remporte la partie !",
	},
	enables = {
		healthbar = {
			on = "<VP>Barre de vie activée.",
			off = "<R>Barre de vie désactivée.",
		},
		messages = {
			on = "<VP>Messages activés.",
			off = "<R>Messages désactivés.",
		},
		hints = {
			on = "<VP>Hints enabled!",
			off = "<R>Hints disabled!",
		},
		bot = {
			on = "<VP>Bot activé.",
			off = "<R>Bot désactivé.",
		},
		graphics = {
			on = "<VP>Qualité : haute",
			off = "<R>Qualité : basse",
		},
		pw = {
			on = "<VP>Mot de passe : %s",
			off = "<R>Mot de passe retiré.",
		},
	},
	help = {
		[1] = {"#%s!","<PT>#%s a été développé par Bolodefchoco.\n\n<VP>Votre objectif, dans ce minijeu, est de rester <I>en vie</I> durant %s minutes en utilisant les pouvoirs à votre disposition, vous serez guider par %s !\n\n<R>N'OUBLIE pas d'activer TOUTES les particules (dans l'onglet option, après l'icône du Café, le 7ème boutton)."},
		[2] = {"Commandes","<VP>!%s <G>- Affiche la page d'AIDE\n<VP>!%s <G>- Affiche les informations pour chaque pouvoir\n<VP>!%s <G>- Active/désactive la barre de vie\n<VP>!%s <G>- Active/désactive les conseils\n<VP>!%s <G>- Active/désactive les messages du bot.\n<VP>!%s <PT>1/2/3/4 <G>- Change la position de la bar de vie\n<VP>!%s <PT>@Code <G>- Charge une carte (3 souris ou moins)\n<VP>!%s <PT>ID <G>- Change la langue du jeu (pour vous seulement)\n<VP>!%s <PT>pseudonyme <G>- Affiche votre profil, ou celui du joueur mentionné\n<VP>!%s <G>- Change la qualité du jeu\n<VP>!%s <G>- Ouvre le classement\n<VP>!%s <PT>@Code <G>- Vérifie si la carte est dans la rotation officielle"},
		[3] = {"Statistiques","<N>• <J>Niveau <G>- Le plus haut niveau que vous pouvez atteindre est %s\n<N>• <J>Titre <G>- Le titre correspondant au niveau actuel (%s titles)\n<N>• <J>Éxperience <G>- Nombre de points d'expérience que vous avez et combien il vous en manque pour monter de niveau\n<N>• <J>Parties <G>- Nombre de parties jouées\n<N>• <J>Victoires <G>- Nombre de victoires <R>(+%s par victoire ou toutes les 35 minutes)\n<N>• <J>Souris tués <G>- Nombre de souris tués par vos soins\n<N>• <J>Ratio <G>- Le ratio entre nombre de <I>parties, victoires</I> et <I>morts"},
		[4] = {"Cartes","<CEP>Envoyez vos cartes ici : %s\n\n<CS>Liste complète des cartes ci-dessous : (%s)\n%s"},
		[5] = {"Admins","<PT>Pour créer un salon avec des administrateurs, assurez vous d'ajouter dans le nom du salon votre pseudo après une suite de chiffres <VP>(/room %s)\n<R>Les statistiques ne comptent pas si vous changez le temps de jeu ou si le maximum de joueurs dans le salon est fixé en-dessous de 8.\n\n<BV>!%s <CH>Nombre/Mot <G>- Change la limite de joueurs dans le salon (2-18)\n<BV>!%s <CH>Id <G>- Renomme le bot\n<BV>!%s <CH>Temps <G>- Change la durée d'une partie\n<BV>!%s <CH>Nom <G>- Donne ou retire les droits d'administrer le salon au joueur mentionné."},
		[6] = {"Remerciements Spéciaux","<R>Bolodefchoco <N>- CEO + EN Translation + Tradução BR\n<BV>Tocuto<J>eltuco <N>- Traducción ES + Little Code\n<BV>Error<CE>_404 <N>- الترجمة AR + Map evaluation\n<J>Squalleze <N>- Little Code\n<PT>Lukamoii <N>- Ideas\n<CE>Error_404, Ujkos, Kimsterjay, Pratton and Mabste <N>- Map Evaluation\n<BV>Chamelinct <N>- Traducción ES\n<BV>Distances en Kalkoen <N>- NL Translation\n<BV>Aanguson <N>- Tłumacz PL\n<BV>Animjarcanin <N>- Traduction FR\n<BV>Bublamorce <N>- CZ Překl"},
	},
	hints = {
		[1] = "N'OUBLIE pas d'activer les particules (dans le menu option, à droite du Café, 7ème icône).",
	},
	other = {
		close = "Fermer",
		powers_textformat = "<J>Type : <N>%s\n<J>Niveau : <N>%s\n<BV>Utilisations : <N>%s\n<VP>Activation : <N>%s\n<R>Dommages : <N>%s\n<PS>%s",
		powers_types = {"Défense","Attaque","Troll","God Mode"},
		profile_textformat = "<font color='#%s'><J>Niveau</J> %s\n<J>Titre :</J> «%s»\n<J>Experience :</J> %s\n\n<J>Parties jouées :</J> %s\n<J>Victoires :</J> %s\n<J>Souris tués :</J> %s\n\n<J>Temps de jeu :</J> %s\n<J>Ratio :</J> %s%%",
	},
	admins = {
		iftrue = "<R>Les statistiques ne comptent pas si vous changez le nom du bot ou la durée d'une partie.",
		maxroom = "Le salon est limité à %s souris",
		renamed = "%s s'appelle désormais %s",
		time = "Une partie dure dorénavant %s minutes.",
		notadmin = "%s n'est plus administrateur.",
		isadmin = "%s est désormais administrateur.",
	},
	ranking = {
		[1] = {"#Salon","Affiche le classement aux joueurs présents dans le salon"},
		[2] = {"#Global","Affiche le classement général"},
	},
}
T.cz = {
	titles = {
		title = {"Učeň","Kouzelník","Profesor","Badatel","Mistr","Lord Kouzel","Princ Kouzel","Král Magie","Všudypřítomný","Vševědoučí","Všemohoucí","Bůh","Alfa a Omega"},
		newlevel = "%s dosáhl levelu %s",
		unlock = {
			unlocked = "Právě jsi odemkl schopnost: ",
			title = "<J>%s <G>právě odemkl titul %s«%s»",
			[10] = "<N><I>Červí Díra</I><J> a <CEP><I>Dvojitý Skok</I><J>!",
			[20] = "<J><I>Kupole</I> a <CS><I>Spirála</I><J>!",
			[30] = "<J><I>Blesk</I>!",
			[40] = "<ROSE><I>Supernova</I><J>!",
			[50] = "<VP><I>Hulkův Úder</I><J> a <R><I>Smrtící Objetí</I><J>!",
			[60] = "<VI><I>Anomálie</I><J>!",
			[70] = "<BV><I>Paprsek Smrti</I><J>!",		
		},
	},
	powers = {
		[1] = {"Rychlost Světla",{"← ←","→ →"},"Teleportuje tě 255px do zvoleného směru"},
		[2] = {"Paprsek",{"Zmáčknutím <U>Mezerníku</U>"},"Vystřelí paprsek"},
		[3] = {"Červí Díra",{"↑↓","↓↑"},"Teleportuje tě 200px ve tvém směru"},
		[4] = {"Dvojitý Skok",{"↑↑"},"Dovolí ti udělat dvojitý skok"},
		[5] = {"Kupole",{"Facepalm akcí/emocí","<I>PROTECTOS</I> do chatu"},"Vytvoří velkou kupoli"},
		[6] = {"Spirála",{"Zmáčknutím <U>SHIFTU</U>"},"Vystřelí tě diagonálně"},
		[7] = {"Blesk",{"Levým kliknutím"},"Vytvoří blesk"},
		[8] = {"Supernova",{"Zmáčknutím <U>CTRL</U>"},"Vytvoří velkou supernovu"},
		[9] = {"Hulkův Úder",{"↓↓"},"Udělá originální Hulkův Úder"},
		[10] = {"Smrtící Objetí",{"Objímací akcí/emocí"},"Zabije toho,kdo tě obejme"},
		[11] = {"Anomálie",{"Napiš <I>ANOMALY</I> do chatu (Podaří se to jen vzácně)"},"Vytvoří anomálii!"},
		[12] = {"Paprsek Smrti",{"Zmáčknutím <U>P</U> 30-40 krát"},"Vystřelí silný paprsek"},
	},
	botMessages = {
		welcome = "<BV>Vítej v <CH>#%s<BV>. Napiš <CH>!%s<BV> Pro více informací!",
		roomplayers = "<R>Pro spuštění hry,v místnosti musí být 2 myši!",
		notplayers = "<BV>Minimálně 6 hráčů je potřeba pro počítání skóre.",
		alive = "<R>Musíš být naživu,aby jsi to udělal!",
		timernp = "<R>Musíš počkat %sms aby jsi to udělal!",
		powerlimit = "Dosáhl jsi limitu použití této schopnosti! (%s)",
		newtimer = "%s sekund bylo přidáno! Užijte si!",
		allpowers = "Santa Claus ti dal dárek! Pokud v místnosti budou 3 myši a méně,můžeš použít VŠECHNY schopnosti!",
		nextmap = "%s bude nová mapa!",
		wnextmap = "%s nebude nová mapa!",
		anomaly = "<CH>ANOMÁLIE JE TADY!",
		anomtim = "<R>Nezdařilo se přivolat Anomálii! :( Počkej %s sekund.",
		won = "<J>%s <G>vyhrál kolo!",
	},
	enables = {
		healthbar = {
			on = "<VP>Zdraví zapnuté!",
			off = "<R>Zdraví vypnuté!",
		},
		messages = {
			on = "<VP>Zprávy zapnuté!",
			off = "<R>Zprávy vypnuté!",
		},
		hints = {
			on = "<VP>Nápovědy zapnuté!",
			off = "<R>Nápovědy vypnuté!",
		},
		bot = {
			on = "<VP>Zprávy bota zapnuté!",
			off = "<R>Zprávy bota vypnuté!",
		},
		graphics = {
			on = "<VP>Grafika: Vysoká",
			off = "<R>Grafika: Nízká",
		},
		pw = {
			on = "<VP>Heslo: %s",
			off = "<R>Heslo vypnuto.",
		},
	},
	help = {
		[1] = {"#%s!","<PT>#%s bylo vyrobeno a idealizováno hráčem Bolodefchoco.\n\n<VP>Tvůj cíl v této minihře je být <I>the survivor</I> v %s minutách používáním všech tvých schopností, naváděn %s!\n\n<R>Nezapomeň ZAPNOUT malé efekty (V nastavení, vedle Café, sedmý řádek)."},
		[2] = {"Příkazy","<VP>!%s <G>- Ukáže nápovědu\n<VP>!%s <G>- Ukáže všechny informace o schopnostech\n<VP>!%s <G>- Zapne/Vypne zdraví\n<VP>!%s <G>- Zapne/Vypne nápovědy\n<VP>!%s <G>- Zapne/Vypne botovy zprávy.\n<VP>!%s <PT>1/2/3/4 <G>- Změní pozici,kde se bude ukazovat zdraví\n<VP>!%s <PT>@Code <G>- Načte mapu (3 nebo míň myší)\n<VP>!%s <PT>ID <G>- Změní jazyk hry (Jen pro tebe,ostatní to neuvidí)\n<VP>!%s <PT>PlayerName <G>- Zobrazí tvůj profil, nebo profil specifického hráče.\n<VP>!%s <G>- Změní kvalitu hry.\n<VP>!%s <G>- Otevře tabulku.\n<VP>!%s <PT>@Code <G>- Zkontroluje,jestli je mapa v oficiální rotaci."},
		[3] = {"Statistiky","<N>• <J>Level <G>- Nejvyšší level,kterého můžeš dosáhnout je %s.\n<N>• <J>Titul <G>- Název kola, které je právě hrané (%s titles)\n<N>• <J>Zkušenost <G>- Spočítá kolik bodů právě máš a kolik potřebuješ pro další level\n<N>• <J>Kola <G>- Spočítá,kolik kol jsi hrál\n<N>• <J>Výhry <G>- Spočítá,kolikrát jsi vyhrál <R>(+%s za výhru nebo každých 35 minut)\n<N>• <J>Zabití <G>- Spočítá,kolik myší jsi zabil\n<N>• <J>Profilová hodnota <G>- Hodnota mezi <I>Koly, Vítězstvími</I> and <I>Zabitími"},
		[4] = {"Mapy","<CEP>Pošli své mapy zde: %s\n\n<CS>Kompletní list map: (%s)\n%s"},
		[5] = {"Admini","<PT>Pro vytvoření místnosti, přidej do názvu přezdívku a nějaká čísla <VP>(/room %s)\n<R>Statistiky se nebudou počítat pokud změníš čas kola a nebo nastavíš maximum hráčů v místnosti větší než 8.\n\n<BV>!%s <CH>Number/String <G>- Změní limit hráčů v místnosti (2-18)\n<BV>!%s <CH>Id <G>- Přejmenuje bota\n<BV>!%s <CH>Time <G>- Změní čas kola\n<BV>!%s <CH>Name <G>- Dá/Oddělá někomu adminská práva"},
		[6] = {"Speciální poděkování","<R>Bolodefchoco <N>- CEO + EN Translation + Tradução BR\n<BV>Tocuto<J>eltuco <N>- Traducción ES + Little Code\n<BV>Error<CE>_404 <N>- الترجمة AR + Map evaluation\n<J>Squalleze <N>- Little Code\n<PT>Lukamoii <N>- Ideas\n<CE>Error_404, Ujkos, Kimsterjay, Pratton and Mabste <N>- Map Evaluation\n<BV>Chamelinct <N>- Traducción ES\n<BV>Distances en Kalkoen <N>- NL Translation\n<BV>Aanguson <N>- Tłumacz PL\n<BV>Animjarcanin <N>- Traduction FR\n<BV>Bublamorce <N>- CZ Překl"},
	},
	hints = {
		[1] = "Nezapomeň ZAPNOUT malé efekty (V nastavení, vedle Café, sedmý řádek).",
	},
	other = {
		close = "Zavřít",
		powers_textformat = "<J>Typ: <N>%s\n<J>Level: <N>%s\n<BV>Uses: <N>%s\n<VP>Aktivace: <N>%s\n<R>Síla útoku: <N>%s\n<PS>%s",
		powers_types = {"Obrana","Útok","Trollování","Božský Mód"},
		profile_textformat = "<font color='#%s'><J>Level</J> %s\n<J>Titul:</J> «%s»\n<J>Zkušenost:</J> %s\n\n<J>Kola:</J> %s\n<J>Výhry:</J> %s\n<J>Zabití:</J> %s\n\n<J>Čas hraní:</J> %s\n<J>Profilová hodnota:</J> %s%%",
	},
	admins = {
		iftrue = "<R>Statistiky se nebudou počítat pokud měníš jméno bota nebo čas kola.",
		maxroom = "Limit hráčů byl nastaven na %s",
		renamed = "%s byl přejmenován na %s",
		time = "Čas byl nastaven na %s min.",
		notadmin = "%s už není admin!",
		isadmin = "%s je nyní admin!",
	},
	ranking = {
		[1] = {"#Žebříček Místnosti","Ukáže žebříček místnosti"},
		[2] = {"#Globální Žebříček","Ukáže žebříček celé hry"},
	},
}
T.ro = {
	titles = {
		title = {"Ucenic","Vrăjitor","Profesor","Cercetător","Maestru","Lordul Vrăjiilor","Prințul Vrăjiilor","Regele Magiei","Omniprezent","Atotștiutor","Atotputernic","Zeu","Alpha & Omega"},
		newlevel = "%s a ajuns la nivelul %s",
		unlock = {
			unlocked = "Tocmai ai deblocat puterea: ",
			title = "<J>%s <G>tocmai a deblocat titlul %s«%s»",
			[10] = "<N><I>Gaură de Vierme</I><J> și <CEP><I>Dublu Salt</I><J>!",
			[20] = "<J><I>Cupolă</I> și <CS><I>Helix</I><J>!",
			[30] = "<J><I>Fulger</I>!",
			[40] = "<ROSE><I>Supernova</I><J>!",
			[50] = "<VP><I>Zdrobitura lui Hulk</I><J> și <R><I>Îmbrățișarea Morții</I><J>!",
			[60] = "<VI><I>Anomalie</I><J>!",
			[70] = "<BV><I>Raza Morții</I><J>!",	
		},
	},
	powers = {
		[1] = {"Viteza Luminii",{"← ←","→ →"},"Te teleportează 255px în direcția aleasă"},
		[2] = {"Rază",{"Tasta <U>Space</U>"},"Trage cu o rază laser"},
		[3] = {"Gaură de Vierme",{"↑↓","↓↑"},"Te face să te teleportezi 200px în direcția ta"},
		[4] = {"Dublu Salt",{"↑↑"},"Sari de două ori"},
		[5] = {"Cupolă",{"Emoția Facepalm","<I>PROTECTOS</I> pe chat"},"Creează o mare cupolă"},
		[6] = {"Spirală",{"Tasta <U>SHIFT</U>"},"Te stimulează diagonal"},
		[7] = {"Fulger",{"Mouse (Click)"},"Invocă un mare Fulger"},
		[8] = {"Supernova",{"Tasta <U>CTRL</U>"},"Creează o mare Supernovă"},
		[9] = {"Zdrobitura lui Hulk",{"↓↓"},"Creează o animație a originalei Zdorbitură a lui Hulk"},
		[10] = {"Îmbrățișarea Morții",{"Emoția Îmbrățișării"},"Omoară pe cine imbrățișezi"},
		[11] = {"Anomalie",{"<I>ANOMALY</I> pe chat (Ar trebui să știi că rar se întâmplă să meargă)"},"Creează o Anomalie în joc!"},
		[12] = {"Raza Morții",{"Tasta <U>P</U> de 30-40 de ori"},"Trage cu o rază puternică"},
	},
	botMessages = {
		welcome = "<BV>Bine ai venit <CH>#%s<BV>. Scrie <CH>!%s<BV> pentru mai multe informații!",
		roomplayers = "<R>Pentru a începe jocul, trebuie ca 2 jucătorii să fie pe sală!",
		notplayers = "<BV>Trebuie ca maxim 6 jucătorii să fie pe sală ca statusuriile să se pună.",
		alive = "<R>Trebuie să fii în viață pentru a face asta!",
		timernp = "<R>Trebuie să aștepți %sms să faci asta!",
		powerlimit = "Ai atins limita pentru a folosi această putere! (%s)",
		newtimer = "%s secunde au fost adăugate în runda asta! Distracție plăcută în continuare!",
		allpowers = "Moș Crăciun are un cadou pentru tine! Dacă în sală rămân 3 șoricei sau mai puțini, vei putea folosi TOATE puteriile!",
		nextmap = "%s va fii următoarea mapă!",
		wnextmap = "%s nu va fii următoarea mapă!",
		anomaly = "<CH>ANOMALIA ESTE AICI!",
		anomtim = "<R>Potrivirea nu a fost găsită și cererea nu a fost finalizată cu succes :( Așteaptă %s secunde.",
		won = "<J>%s <G>a câștigat runda!",
	},
	enables = {
		healthbar = {
			on = "<VP>Bara care afișează sănătatea este activată!",
			off = "<R>Bara care afișează sănătatea este dezactivată!",
		},
		messages = {
			on = "<VP>Mesajele sunt activate!",
			off = "<R>Mesajele sunt dezactivate!",
		},
		hints = {
			on = "<VP>Indicii activate!",
			off = "<R>Indicii dezactivate!",
		},
		bot = {
			on = "<VP>Mesajele bot-ului sunt acum activate!",
			off = "<R>Mesajele bot-ului sunt acum dezactivate!",
		},
		graphics = {
			on = "<VP>Grafică: Intensă",
			off = "<R>Grafică: Slabă",
		},
		pw = {
			on = "<VP>Parolă: %s",
			off = "<R>Parolă dezactivată.",
		},
	},
	help = {
		[1] = {"#%s!","<PT>#%s a fost realizat și idealiat de Bolodefchoco.\n\n<VP>Scopul tău în acest minigame este să fii <I>supraviețuitorul</I> timp de %s minute folosind toate puteriile tale, fiind ghidat de %s!\n\n<R>NU uita să ACTIVEZI efectul particulelor (În opțiuni, lângă Café, a șaptea opțiune)."},
		[2] = {"Comenziile Chat-ului","<VP>!%s <G>-Afișează mesajul de ajutor\n<VP>!%s <G>- Afișează toate informațiile despre puteri\n<VP>!%s <G>- Activează/dezactivează bara cu sănătate\n<VP>!%s <G>- Activează/dezactivează indiciile\n<VP>!%s <G>- Activează/dezactivează mesajele bot-ului.\n<VP>!%s <PT>1/2/3/4 <G>- Schimbă poziția barei cu sănătate\n<VP>!%s <PT>@Cod <G>- Încarcă o mapă (3 șoareci sau mai puțin)\n<VP>!%s <PT>ID <G>- Schimbă limba jocului (Doar pentru tine)\n<VP>!%s <PT>NumeleJucătorului <G>- afișează profilul tău, sau alt profil al jucătorului ales.\n<VP>!%s <G>- Schimbă calitatea jocului.\n<VP>!%s <G>- Deschide topul.\n<VP>!%s <PT>@Cod <G>- Verifică dacă mapa este în rotația oficială."},
		[3] = {"Statistici","<N>• <J>Nivel <G>- Cel mai mare nivel la care poți să ajungi este %s.\n<N>• <J>Titlul <G>- Nivelul al titlului respectiv (%s titluri)\n<N>• <J>Experiență <G>- Calculează câte puncte ai și câte puncte mai ai nevoie să avansezi în nivel\n<N>• <J>Runde <G>- Calculează câte runde ai jucat\n<N>• <J>Câștiguri <G>- Calculează câte victorii ai <R>(+%s pentru victorie sau în fiecare 35 de minute)\n<N>• <J>Ucideri <G>- Calculează câți șoareci ai ucis\n<N>• <J>Raportul Profilului <G>- Raportul este despre <I>Runde, Câștiguri</I> și <I>Ucideri"},
		[4] = {"Mape","<CEP>Trimite mapa ta pe: %s\n\n<CS>Lista completă a mapelor: (%s)\n%s"},
		[5] = {"Admini","<PT>Pentru a crea o sală cu admini, fii sigur să adaugi un nume de utilizator după câteva numere <VP>(/sala %s)\n<R>Statisticile nu vor conta dacă schimbii timpul de joc sau dacă setezi limita de jucători sub 8 jucători..\n\n<BV>!%s <CH>Numărul <G>- Schimbă limita de jucători din sală (2-18)\n<BV>!%s <CH>Id <G>- Numește bot-ul\n<BV>!%s <CH>Timp <G>- Schimbă timpul rundelor\n<BV>!%s <CH>Name <G>- Făcând/scoțând statutul de admin al jucătorului ales."},
		[6] = {"Mulțumiri lui","<BV>Lukamoii - Idealizatorul Titlurilor, Culorilor și puțin Gameplay.\n\nAnimjarcanin, Evilsantah, Jamesqwartz, Podoko, Squirrelmanx, Ultraspeedy, Tweetis - Activarea minijocului în testăriile Beta.\n\nTomdizzy - Reprezentatorul minijocului pentru Pikashu, fiind „gazda” minijocului.."},
	},
	hints = {
		[1] = "NU uita să activezi opțiunea „vezi efectul particulelor” (În setări, lângă Café, a șaptea opțiune.).",
	},
	other = {
		close = "Închide",
		powers_textformat = "<J>Tip: <N>%s\n<J>Nivel: <N>%s\n<BV>Folosiri: <N>%s\n<VP>Activează: <N>%s\n<R>Daună: <N>%s\n<PS>%s",
		powers_types = {"Defensiv","Ofensiv","Troll","Modul Zeu"},
		profile_textformat = "<font color='#%s'><J>Nivelul</J> %s\n<J>Titlul:</J> «%s»\n<J>Experiența:</J> %s\n\n<J>Rundele jucate:</J> %s\n<J>Câștiguri:</J> %s\n<J>Ucideri:</J> %s\n\n<J>Timpul de joc:</J> %s\n<J>Raportul profilului:</J> %s%%",
	},
	admins = {
		iftrue = "<R>Statisticile nu vor conta dacă schimbi botName sau timpul rundei.",
		maxroom = "Limita jucătoriilor a fost setată la numărul %s",
		renamed = "%s a fost renumit în %s",
		time = "Timpul standard a fost setat la %s minute.",
		notadmin = "%s nu mai este un admin!",
		isadmin = "%s este acum un admin!",
	},
	ranking = {
		[1] = {"#Topul Sălii","Afișează topul acestei sălii"},
		[2] = {"#Topul Global","Afișează topul global al minijocului #powers"},
	},
}
T.pt = T.br
tr=function(t,l1,l2,l3)
	t = (t and mice[t].community or tfm.get.room.community)
	t = (T[t] and t or "en")
	return (l3 and T[t][l1][l2][l3] or l2 and T[t][l1][l2] or l1 and T[t][l1] or "")
end
--[[ Remake ]]--
local chatmsg = tfm.exec.chatMessage
tfm.exec.chatMessage=function(t,txt,n,d)
	txt = txt or "";n = n or nil
	d = d and mice[n].botMessages or not d and true
	if d then
		if t == 0 then
			chatmsg(txt,n)
		elseif t == 1 then
			chatmsg(bot:format(txt),n)
		elseif t == 2 then
			chatmsg("[•] "..txt,n)
		elseif t == 3 then
			chatmsg("[^_^] "..txt,n)
		end
	end
end
local particle = tfm.exec.displayParticle
tfm.exec.displayParticle=function(id,x,y,xs,ys,xa,ya,player)
	xs,ys,xa,ya = xs or 0,ys or 0,xa or 0,ya or 0
	if not player then
		for n,p in next,tfm.get.room.playerList do
			if mice[n] then
				if not mice[n].isAfk[1] and not p.isDead then
					if math.pythag(p.x,p.y,x,y,(mice[n].graphics and 300 or 250)) then
						particle(id,x,y,xs,ys,xa,ya,n)
					end
				end
			end
		end
	else
		particle(id,x,y,xs,ys,xa,ya,player)
	end
end
--[[ Settings ]]--
for _,f in next,{"utoShaman","utoScore","utoNewGame","utoTimeLeft","fkDeath"} do
	tfm.exec["disableA"..f]()
end
tfm.exec.setRoomMaxPlayers(18)
--[[ Functions ]]--
	-- Languages
system.languages=function()
	local str = {}
	for language in next,T do
		str[#str+1]=language:upper()
	end
	return table.concat(str," <G>-</G> ")
end
	-- Admins
system.admins=function()
	if not adminRoom[1] then
		if isRoom then
			local name = tfm.get.room.name:match("%*?#"..data.game:lower().."%d+(.*)")
			local name = string.nick(tostring(name))
			if tfm.get.room.playerList[name] and not table.find(admins,name) then
				adminRoom[1] = true
				table.insert(admins,name)
			end
		end
	end
end
	-- UI
ui.smart = function(id,player,alpha,title,text,x,y,w,h,u)
	id = id or 0
	player = player or nil
	alpha,title,text = alpha or 1,title or "",text or ""
	x,y,w,h = x or 10,y or 15,w or 100,h or 100
	if mice[player].graphics then
		ui.addTextArea(id + 0,"",player,x-2,y+18,w+24,h+14,0x2E221B,0x2E221B,alpha,true)
		ui.addTextArea(id + 1,"",player,x-1,y+19,w+22,h+12,0x986742,0x986742,alpha,true)
		ui.addTextArea(id + 2,"",player,x+2,y+22,w+16,h+6,0x171311,0x171311,alpha,true)
		ui.addTextArea(id + 3,"",player,x+3,y+23,w+14,h+4,0x0C191C,0x0C191C,alpha,true)
		ui.addTextArea(id + 4,"",player,x+4,y+24,w+12,h+2,0x24474D,0x24474D,alpha,true)
		ui.addTextArea(id + 5,"",player,x+5,y+25,w+10,h,0x183337,0x183337,alpha,true)
		ui.addTextArea(id + 6,"<p align='center'><font size='15' face='verdana' ><V><B>"..title:upper().."</B></p></font>"..(u and "<R>"..("_"):rep(w/6/2) or "").."<p align='left'><font size='12' /><N>\n"..(u and "\n" or "")..text,player,x+6,y+26,w+8,h-2,0x122528,0x122528,alpha,true)
		ui.addTextArea(id + 7,"",player,x+15,y+h+5,w-10,15,0x5D7D90,0x5D7D90,alpha,true)
		ui.addTextArea(id + 8,"",player,x+15,y+h+7,w-10,15,0x11171C,0x11171C,alpha,true)
		ui.addTextArea(id + 9,"<p align='center'><a href='event:closeUiSmart'><N>"..tr(n,"other","close").."</a>",player,x+15,y+h+6,w-10,15,0x3C5064,0x3C5064,alpha,true)
	else
		ui.addTextArea(id + 0,"<p align='center'><font size='15' face='verdana' ><V><B>"..title:upper().."</B></p></font>"..(u and "<R>"..("_"):rep(w/6/2) or "").."<p align='left'><font size='12' /><N>\n"..(u and "\n" or "")..text,player,x+6,y+26,w+8,h-2,0x122528,0x122528,alpha,true)
		ui.addTextArea(id + 1,"<p align='center'><a href='event:closeUiSmart'><N>"..tr(n,"other","close").."</a>",player,x+15,y+h+6,w-10,15,0x3C5064,0x3C5064,alpha,true)
	end
end
ui.menu=function(id,player,alpha,title,text,x,y,w,h,list,char,char2,u,fixed)
	x,y,w,h,u,fixed = x or 10,y or 15,w or 100,h or 100,u or false,fixed or true
	local menutext = ""
	if list then
		for k,v in next,list do
			menutext = menutext .. "<a href='event:"..char.."_"..k.."'>"..(v[1]:format(data.game):lower()==title:lower() and "<J>"..v[1]:format(data.game).."</J>" or v[1]:format(data.game)).."</a>\n"
		end
	end
	if mice[player].graphics then
		ui.addTextArea(id + 0,"",player,x-2,y+18,w+147,h+14,0x2E221B,0x2E221B,alpha,fixed)
		ui.addTextArea(id + 1,"",player,x-1,y+19,w+145,h+12,0x986742,0x986742,alpha,fixed)
		ui.addTextArea(id + 2,"",player,x+2,y+22,w+16,h+6,0x171311,0x171311,alpha,fixed)
		ui.addTextArea(id + 3,"",player,x+3,y+23,w+14,h+4,0x0C191C,0x0C191C,alpha,fixed)
		ui.addTextArea(id + 4,"",player,x+4,y+24,w+12,h+2,0x24474D,0x24474D,alpha,fixed)
		ui.addTextArea(id + 5,"",player,x+5,y+25,w+10,h,0x183337,0x183337,alpha,fixed)
		ui.addTextArea(id + 6,"<p align='center'><font size='15' face='verdana' ><V><B>"..title:upper().."</B></p></font>"..(u and "<R>"..("_"):rep(w/6/2) or "").."<p align='left'><font size='12' /><N>\n"..(u and "\n" or "")..text,player,x+6,y+26,w+8,h-2,0x122528,0x122528,alpha,fixed)
		ui.addTextArea(id + 7,"",player,x+15,y+h+5,w-10,15,0x5D7D90,0x5D7D90,alpha,fixed)
		ui.addTextArea(id + 8,"",player,x+15,y+h+7,w-10,15,0x11171C,0x11171C,alpha,fixed)
		ui.addTextArea(id + 9,"<B><p align='center'><a href='event:"..char2.."_left'>&lt;&lt;</a>                    <a href='event:close'>"..tr(n,"other","close").."</a>                    <a href='event:"..char2.."_right'>>></a>",player,x+15,y+h+6,w-10,15,0x3C5064,0x3C5064,alpha,fixed)
		ui.addTextArea(id + 10,"",player,x+381,y+22,w-240,h+6,0x171311,0x171311,alpha,fixed)
		ui.addTextArea(id + 11,"",player,x+382,y+23,w-242,h+4,0x0C191C,0x0C191C,alpha,fixed)
		ui.addTextArea(id + 12,"",player,x+383,y+24,w-244,h+2,0x24474D,0x24474D,alpha,fixed)
		ui.addTextArea(id + 13,"",player,x+384,y+25,w-246,h,0x183337,0x183337,alpha,fixed)
		ui.addTextArea(id + 14,"<p align='center'>"..menutext,player,x+385,y+26,w-248,h-2,0x122528,0x122528,alpha,fixed)
	else
		ui.addTextArea(id + 0,"<p align='center'><font size='15' face='verdana' ><V><B>"..title:upper().."</B></p></font>"..(u and "<R>"..("_"):rep(w/6/2) or "").."<p align='left'><font size='12' /><N>\n"..(u and "\n" or "")..text,player,x+6,y+26,w+8,h-2,0x122528,0x122528,alpha,fixed)
		ui.addTextArea(id + 1,"<B><p align='center'><a href='event:"..char2.."_left'>&lt;&lt;</a>                    <a href='event:close'>"..tr(n,"other","close").."</a>                    <a href='event:"..char2.."_right'>>></a>",player,x+15,y+h+6,w-10,15,0x3C5064,0x3C5064,alpha,fixed)
		ui.addTextArea(id + 2,"<p align='center'>"..menutext,player,x+385,y+26,w-248,h-2,0x122528,0x122528,alpha,fixed)
	end
	mice[player].nextUiTimer = os.time() + data.uitimer
end
	-- Returns the position
tfm.exec.position=function(n)
	return tfm.get.room.playerList[n].x,tfm.get.room.playerList[n].y,mice[n].right
end
	-- Returns true if x1,y1 is in the circle x2,y2 with range range
math.pythag=function(x1,y1,x2,y2,range)
	return ((x1-x2)^2+(y1-y2)^2<range^2)
end
	-- Returns the players of the room and the players that are alive
system.players=function(trdArg)
	local alive,players,able = {},{},{}
	for k,v in next,tfm.get.room.playerList do
		if not v.isDead then
			alive[#alive+1]=k
		end
		if trdArg then
			if os.time() - v.registrationDate > 432e6 then
				able[#able+1]=k
			end
		end
		players[#players+1] = k
	end
	return alive,players,able
end
	-- Returns true case value is in list
table.find=function(list,value)
	local found,keys,times = false,{},0
	for k,v in next,list do
		if type(v) ~= "table" then
			if v == value then
				found = true
				keys[#keys+1] = k
				times = times + 1
			end
		else
			local a,b,c = table.find(v,value)
			if not found then found = a end
			if b then table.insert(keys,table.unpack(b)) end
			if c then times = times + c end
		end
	end
	return found,keys,times
end
	-- Remove value from table
table.destroy=function(list,value)
	for k,v in next,list do
		if v == value then
			table.remove(list,k);break
		end
	end
end
	-- Color Hex/Ansii
math.color=function(x)
	if type(x) == "string" then
		return tonumber(x,16)
	elseif type(x) == "number" then
		return string.format("%x",x)
	end
end
	-- Nick
string.nick=function(player)
	return player:lower():gsub('%a',string.upper,1)
end
	-- Verify if the game can start
system.start=function(n)
	local alive,players = system.players()
	if #players > 1 then
		if table.find(alive,n) then
			if loopTimer>3 and not anomaly and not skip then
				if os.time() > mice[n].nPTimer then
					return true
				else
					tfm.exec.chatMessage(1,tr(n,"botMessages","timernp"):format(data.timernp),n,true)
				end
			end
		else
			tfm.exec.chatMessage(1,tr(n,"botMessages","alive"),n,true)
		end
	else
		tfm.exec.chatMessage(1,tr(nil,"botMessages","roomplayers"),n,true)
	end
	return false
end
	-- Life
system.healthbar=function(n)
	local position = mice[n].healthbarp
	local positions = {
		x = {
			{5,7,40},
			{691,693,729},
		},
		y = {
			{28,30,29},
			{319,321,320},
		},
	}
	local x = (position<3 and positions.x[1] or positions.x[2])
	local y = (position%2~=0 and positions.y[1] or positions.y[2])
	ui.addTextArea(0,"",n,x[1],y[1],data.life+4,20,0xc7ced2,1,1,true)
	if not mice[n].ded and mice[n].graphics then ui.addTextArea(1,"",n,x[2]-1,y[2],math.floor(mice[n].health)+2,16,math.color(mice[n].level[3]),math.color(mice[n].level[3]),1,true) end
	ui.addTextArea(2,"<B><font color='#0'>"..math.floor(mice[n].health).."%",n,x[3],y[3],50,20,1,1,0,true)
end
	-- Add Life
system.addLife=function(n,p,x,y)
	if mice[p].health <= 0 then
		mice[n].health = mice[n].health + 5
		tfm.exec.displayParticle(15,x,y,0,0,0,0,n)
		local _,players = system.players()
		if #players > 5 then
			mice[n].stats.kills = mice[n].stats.kills + 1
		end
	end
end
	-- Damage
system.damage=function(n,x,y,range,damage,right,Y)
	for p,v in next,tfm.get.room.playerList do
		if p~=n and not v.isDead then
			if right ~= nil then
				if (right and v.x>x and v.x<x+range) or (not right and v.x<x and v.x>x-range) then
					if v.y>y-Y and v.y<y+Y then
						mice[p].health = mice[p].health - damage
						system.addLife(n,p,x,y)
					end
				end
			else
				if math.pythag(v.x,v.y,x,y,range) then
					mice[p].health = mice[p].health - damage
					system.addLife(n,p,x,y)
				end
			end
		end
	end
end
	-- Add dray bar
system.draybar=function(n,close)
	if mice[n].graphics then
		if close then
			mice[n].dray = {0,math.random(30,40),0,false}
			for i = 4,6 do ui.removeTextArea(i,n) end
		else
			mice[n].dray[4] = true
			local percent = math.floor(mice[n].dray[1]/mice[n].dray[2]*100)
			ui.addTextArea(4,"",n,691,380,103,11,0x2c3e36,1,1,true)
			ui.addTextArea(5,"", n,692,382,(percent~=percent and 0 or percent),7,0x5EA0D5,0x5EA0D5,1,true)
			ui.addTextArea(6,tostring(percent):gsub("nan","0").."%",n,691,377,50,20,1,1,0,true)
		end
	end
end
	-- add menu
system.addMenu=function(n)
	local s = mice[n].showhealthbar
	local p = mice[n].healthbarp
	local c = {"?","+","!","#"}
	local x = (p>2 and 800 or -18)
	for i = 1,#c do
		local id = i+6
		local t = c[i]
		local y = (p%2==0 and 348 or (s and 56 or 30))
		x = (p<3 and x + 26 or x - 26)
		ui.addTextArea(id,"<p align='center'><a href='event:@"..t.."'>"..t,n,x,y,18,18,0x986742,0x2E221B,1,true)
	end
end
	-- get time
system.getTime=function(time)
	if type(time)~="number" then return "?" end
	local second = time%60
	local minutes = time/60
	local minute = minutes%60
	local hours = minutes/60
	local hour = hours%24
	local day = hours/24
	return ("%dd %dh %dm %ds"):format(day,hour,minute,second)
end
	-- ranking
system.rank=function(players,lim,player)
	local p,rank = {},""
	lim = tonumber(lim) or 100
	for n in next,players do
		p[#p+1] = {name=n,v=system.ratio(n)}
	end
	table.sort(p,function(f,s) return f.v>s.v end)
	for o,n in next,p do
		if o <= lim then
			local t = n.name
			rank = rank .. "<J>"..o..".\t<font color='#"..(podiumColors[o] and podiumColors[o] or t==player and "6B99A9" or "009D9D").."'><a href='event:P_"..t.."'>"..t.."</a>\t<font color='#"..mice[t].level[3].."'>"..mice[t].level[1].."</font>\t<BL>"..mice[t].stats.rounds.."\t<S>"..mice[t].stats.wins.."\t<R>"..mice[t].stats.kills.."\t<CE><font size='"..(n.v<1000 and 10 or n.v<10000 and 9 or 8).."'>"..(math.ceil(n.v*100)/100).."</font>\n"
		end
	end
	return rank
end
	-- ratio
system.ratio=function(n)
	local math = ((mice[n].level[1]^.5) * (#colors * mice[n].stats.kills / (mice[n].stats.rounds+1)) + (#colors * mice[n].stats.wins / (mice[n].stats.rounds+1)) + (#colors * mice[n].level[1] / (#colors*10))) - .1
	return math~=math and 0 or math
end
--[[ Powers ]]--
power.lightning=function(n,x,y)
	system.damage(n,x,y+150,40,data.light.d)
	tfm.exec.explosion(x,y+150,-30,40)
	local a,b = {11,2,2,11},{1,-1}
	for i = 0,30 do
		tfm.exec.displayParticle(a[(i%#a)+1],b[(i%#b)+1]+x,y+i*5)
	end
	mice[n].timers[1][1] = os.time() + data.light.m
end
power.lightspeed=function(n,x,y)
	local right = mice[n].right
	for n in next,tfm.get.room.playerList do
		local px,py,r = tfm.exec.position(n)
		if (right and (px>x and px<x+255) or (px<x and px>x-255)) then
			if py>y-60 and py<y+60 then
				local s = right and 30 or -30
				tfm.exec.movePlayer(n,0,0,true,s)
			end
		end
	end
	tfm.exec.movePlayer(n,x+(right and 225 or -255),y)
	for i = 1,6 do
		tfm.exec.displayParticle(35,x,y,(right and 15 or -15),math.random(-3,3))
	end
	mice[n].timers[2] = os.time() + data.light.m
end
power.wormhole=function(n,x,y,s)
	local right = mice[n].right
	local a = {0,4,11}
	for i = 1,40 do
		tfm.exec.displayParticle(a[(i%#a)+1],x + (s and (right and 200 or -200) or 0),y,(.1*i)*math.cos(math.rad(90+i*18)),(.1*i)*math.sin(math.rad(90-i*18)))
	end
	if not s then
		tfm.exec.movePlayer(n,x + (right and 200 or -200),y)
		power.wormhole(n,x,y,true)
	else
		tfm.exec.movePlayer(n,0,0,true,0,-50,true)
	end
	mice[n].timers[3] = os.time() + data.whole.m
end
power.doublejump=function(n,x,y)
	tfm.exec.movePlayer(n,0,0,true,0,-80,true)
	for i = 0,15,.25 do
		tfm.exec.displayParticle(({2,11})[((i*4)%2)+1],x+math.sin(i*1.1)*20,y+40+-i*3.5)
	end
	mice[n].timers[9] = os.time() + data.dbjump.m
end
power.supernova=function(n,x,y)
	system.damage(n,x+(right and 50 or -50),y-50,70,data.snova.d)
	tfm.exec.explosion(x+(right and 50 or -50),y-50,50,110)
	local right = mice[n].right
	local particle = {1,2,9,11};particle = particle[math.random(#particle)]
	for i = 1,38 do
		local a = i<3 and 13 or i<20 and 11 or 2
		tfm.exec.displayParticle(a,x + (right and 50 or -50),y - 50,(.1*i)*math.cos(math.rad(120+i*18)),(.1*i)*math.sin(math.rad(120-i*18)))
		tfm.exec.displayParticle(a,x + (right and 50 or -50),y - 50,(.1*i)*math.cos(math.rad(60-i*18)),(.1*i)*math.sin(math.rad(120-i*18)))
	end
	mice[n].timers[4][1] = os.time() + data.snova.m
	mice[n].health = mice[n].health - 5
end
power.helix=function(n,x,y)
	local right = mice[n].right
	tfm.exec.movePlayer(n,0,0,false,(right and 100 or -100),-115,true)
	local a={2,0,0,2}
	for i = 1,40 do
		tfm.exec.displayParticle(a[(i%#a)+1],x+(right and i or -i),y-i,(right and (.1*i) or -(.1*i))*math.cos(math.rad(200+i*18)),(.1*i)*math.sin(math.rad(200-i*18)),(right and .4 or -.4),-.2)
	end
	mice[n].timers[5] = os.time() + data.helix.m
end
power.dome=function(n)
	local x,y = tfm.exec.position(n)
	system.damage(n,x,y,130,data.dome.d)
	tfm.exec.explosion(x,y,-40,130)
	local a={11,11,0,2,0,2,0,11,11}
	for i = 1,10 do
		local xPos = math.cos(i) * 130
		local yPos = math.sin(i) * 130
		for k = -1,1 do
			for j = -1,1 do
				tfm.exec.displayParticle(a[(i%#a)+1],x + k*xPos,y + j*yPos)
			end
		end
	end
	mice[n].timers[6][1] = os.time() + data.dome.m
end
power.ray=function(n,x,y)
	system.damage(n,x+(right and 20 or -20),y,120,data.ray.d,right,20)
	local right = mice[n].right
	for i = 1,20 do
		tfm.exec.displayParticle(9,(x + (right and 20 or -20)) + (right and math.sqrt(i*2)*8 or -math.sqrt(i*2)*8),y-10,(right and 6 or -6))
	end
	local id = tfm.exec.addShamanObject(6000,x+(right and 40 or -40),y-10,0,(right and 9 or -9))
	table.insert(toDespawn,{os.time(),id})
	mice[n].timers[7] = os.time() + data.ray.m
end
power.deathray=function(n,x,y)
	system.damage(n,x,y,120,data.dray.d,right,30)
	local right = mice[n].right
	local a = {9,2,2,9}
	for i = 1,40 do
		tfm.exec.displayParticle(a[(i%#a)+1],x + (right and i*3 or -i*3),y + (i%2 == 0 and 1 or -1))
	end
	mice[n].timers[8][1] = os.time() + data.dray.m
	mice[n].health = mice[n].health - 10
end
power.hulksmash=function(n,t,x,y)
	if t == 0 then
		tfm.exec.movePlayer(n,0,0,true,0,-110,true)
		mice[n].hsmash[1] = 1;mice[n].hsmash[2] = os.time() + 500
		mice[n].timers[10][1] = os.time() + data.hsmash.m
	end if t == 1 then
		tfm.exec.movePlayer(n,0,0,true,0,400,true)
		mice[n].hsmash[1] = 2;mice[n].hsmash[2] = os.time() + 300
	end if t == 2 then mice[n].health = mice[n].health - 5
	for k,v in next,tfm.get.room.playerList do
			if k ~= n then
				if v.x>x-100 and v.x<x+100 then
					if v.y<y+60 and v.y>y-60 then
						local rand = math.random(50,100)
						tfm.exec.movePlayer(k,0,0,true,0,-rand,true)
						if rand > 69 then mice[k].health = mice[k].health - data.hsmash.d end
					end
				end
			end
		end
		for i = 1,10 do
			tfm.exec.displayParticle(3,x + math.random(-100,100),y + i*math.cos(i))
		end
	end
end
power.deathhug=function(n)
	tfm.exec.killPlayer(n)
end
--[[ Events ]]--
	-- New player
eventNewPlayer=function(n)
	if not mice[n] then
		mice[n]={
			-- Settings
			right = true,
			health = data.life,
			showhealthbar = true,
			hints = true,
			botMessages = true,
			ded = false,
			isAfk = {true,0},
			graphics = true,
			-- Data
			level = {99,"",""}, -- Level, Title, #Color
			time = 0, -- Time played
			lbto = 0,
			healthbarp = 1,
			community = (T[tfm.get.room.playerList[n].community] and tfm.get.room.playerList[n].community or "en"),
			stats = {
				rounds = 0,
				wins = 0,
				kills = 0,
			},
			-- Game
			nPTimer = 0, -- Timer to execute a new power
			timers = {
				-- os.time, used, can use
				[1] = {0,0,data.light.u}, -- Lightning
				[2] = 0, -- Light Speed
				[3] = 0, -- Worm Hole
				[4] = {0,0,data.snova.u}, -- Supernova
				[5] = 0, -- Helix
				[6] = {0,0,data.dome.u}, -- Dome
				[7] = 0, -- Ray
				[8] = {0,0,data.dray.u}, -- Death Ray
				[9] = 0, -- Double Jump
				[10] = {0,0,data.hsmash.u}, -- Hulk Smash
				[11] = {0,0,data.dhug.u}, -- Death Hug
				[12] = {0,0,data.anom.u}, -- Anomaly
			},
			lspeed = {-1,0},
			whole = {-1,0},
			dray = {0,math.random(30,40),0,false}, -- Times holding, times to hold, timer, using
			dbjump = 0,
			hsmash = {0,0,{0,0},0},
			-- UIs
			pages = 1,
			newPlayer = true,
			image = {nil,0,0,nil},
			nextUiTimer = 0,
		}
		ui.addTextArea(-100,"",n,-1500,-1500,3000,3000,1,1,.8,true)
		eventChatCommand(n,"help")
	end
	for _,k in next,{0,1,2,3,16,17,32,80} do
		system.bindKeyboard(n,k,true,true)
	end
	system.bindMouse(n,true)
	tfm.exec.chatMessage(1,tr(n,"botMessages","welcome"):format(data.game,data.help.c1) .. "\n\t<ROSE>Discord: https://discord.gg/quch83R",n)
	tfm.exec.lowerSyncDelay(n)
	system.addMenu(n)
	if not isRoom then
		table.insert(admins,n)
	end
end
	-- Powers in eventMouse: 1
eventMouse=function(n,x,y)
	mice[n].isAfk = {false,os.time()+35000}
	if system.start(n) then
		if mice[n].level[1]>=data.light.l then -- Lightning Lv 30
			local px,py = tfm.exec.position(n)
			if os.time() > mice[n].timers[1][1] and math.pythag(x,y,px,py,200) then
				if mice[n].timers[1][2] < mice[n].timers[1][3] then
					mice[n].timers[1][2] = mice[n].timers[1][2] + 1
					power.lightning(n,x,y)
				else
					tfm.exec.chatMessage(1,"<R>"..tr(n,"botMessages","powerlimit"):format("<VP>"..mice[n].timers[1][3].."</VP>"),n)
				end
			end
		end
	end
end
	-- Powers in eventKeyboard: 8
eventKeyboard=function(n,k,d,x,y)
	mice[n].isAfk = {false,os.time()+35000}
	if k == 0 then mice[n].right = false end if k == 2 then mice[n].right = true end
	if system.start(n) then
		-- Light Speed
		if k == 0 or k == 2 and mice[n].level[1]>=data.lspeed.l then
			if mice[n].lspeed[2] == 0 then
				if os.time() > mice[n].timers[2] then
					mice[n].lspeed = {k,os.time()+300}
				end
			else
				if mice[n].lspeed[2] > os.time() and k == mice[n].lspeed[1] then
					power.lightspeed(n,x,y)
				end
				mice[n].lspeed = {k,0}
			end
		end
		-- Worm Hole
		if k == 1 or k == 3 and mice[n].level[1]>=data.whole.l then
			if mice[n].whole[2] == 0 then
				if os.time() > mice[n].timers[3] then
					mice[n].whole = {k,os.time()+300}
				end
			else
				if mice[n].whole[2] > os.time() and k ~= mice[n].whole[1] then
					power.wormhole(n,x,y)
				end
				mice[n].whole = {-1,0}
			end
		end
		-- Supernova
		if k == 17 and mice[n].level[1]>=data.snova.l then
			if os.time() > mice[n].timers[4][1] then
				if mice[n].timers[4][2] < mice[n].timers[4][3] then
					mice[n].timers[4][2] = mice[n].timers[4][2] + 1
					power.supernova(n,x,y)
				else
					tfm.exec.chatMessage(1,"<R>"..tr(n,"botMessages","powerlimit"):format("<VP>"..mice[n].timers[4][3].."</VP>"),n)
				end
			end
		end
		-- Helix
		if k == 16 and mice[n].level[1]>=data.helix.l then
			if os.time() > mice[n].timers[5] then
				power.helix(n,x,y)	
			end
		end
		-- Ray
		if k == 32 and mice[n].level[1]>=data.ray.l then
			if os.time() > mice[n].timers[7] then
				power.ray(n,x,y)
			end
		end
		-- Deathray
		if k == 80 and mice[n].level[1]>=data.dray.l then
			if os.time() > mice[n].timers[8][1] then
				if mice[n].timers[8][2] < mice[n].timers[8][3] then
					if mice[n].dray[3] > os.time() then
						mice[n].dray[1] = mice[n].dray[1] + 1
						system.draybar(n)
						if mice[n].dray[1] >= mice[n].dray[2] then
							mice[n].timers[8][2] = mice[n].timers[8][2] + 1
							power.deathray(n,x,y)
							mice[n].dray = {0,math.random(30,40),0,false}
							system.draybar(n,true)
						end
					else
						mice[n].dray[3] = os.time() + 700
					end
				else
					tfm.exec.chatMessage(1,"<R>"..tr(n,"botMessages","powerlimit"):format("<VP>"..mice[n].timers[8][3].."</VP>"),n)
				end
			end
		end	
		-- Double Jump
		if k == 1 and mice[n].level[1]>=data.dbjump.l then
			if mice[n].dbjump == 0 then
				if os.time() > mice[n].timers[9] then
					mice[n].dbjump = os.time() + 300
				end
			else
				if mice[n].dbjump > os.time() then
					power.doublejump(n,x,y)
				end
				mice[n].dbjump = 0
			end
		end
		-- Hulk Smash
		if k == 3 and mice[n].level[1]>=data.hsmash.l then
			if mice[n].hsmash[4] == 0 then
				if os.time() > mice[n].timers[10][1] then
					mice[n].hsmash[4] = os.time() + 300
				end
			else
				if mice[n].hsmash[4] > os.time() then
					if mice[n].timers[10][2] < mice[n].timers[10][3] then
						mice[n].timers[10][2] = mice[n].timers[10][2] + 1
						power.hulksmash(n,0)
						mice[n].hsmash[3] = {x,y}	
					else
						tfm.exec.chatMessage(1,"<R>"..tr(n,"botMessages","powerlimit"):format("<VP>"..mice[n].timers[10][3].."</VP>"),n)
					end
				end
				mice[n].hsmash[4] = 0
			end
		end
	end
end
	-- Powers in eventEmotePlayed: 2
eventEmotePlayed=function(n,i)
	mice[n].isAfk = {false,os.time()+35000}
	if system.start(n) then
		-- Dome
		if i == 7 and mice[n].level[1]>=data.dome.l then
			if os.time() > mice[n].timers[6][1] then
				if mice[n].timers[6][2] < mice[n].timers[6][3] then
					mice[n].timers[6][2] = mice[n].timers[6][2] + 1
					power.dome(n)
				else
					tfm.exec.chatMessage(1,"<R>"..tr(n,"botMessages","powerlimit"):format("<VP>"..mice[n].timers[6][3].."</VP>"),n)
				end
			end
		end
		-- Death Hug
		if i == 17 and mice[n].level[1]>=data.dhug.l then
			if os.time() > mice[n].timers[11][1] then
				if mice[n].timers[11][2] < mice[n].timers[11][3] then
					mice[n].timers[11][1] = os.time() + data.dhug.m
					mice[n].timers[11][2] = mice[n].timers[11][2] + 1
					deathhug = {true,os.time() + 8000}
				else
					tfm.exec.chatMessage(1,"<R>"..tr(n,"botMessages","powerlimit"):format("<VP>"..mice[n].timers[11][3].."</VP>"),n)
				end
			end
		end
		if i == 18 and deathhug[1] then
			power.deathhug(n)
			deathhug = {false,0}
		end
	end
end
	-- Powers in eventChatMessage: 1 + 1^
eventChatMessage=function(n,c,access)
	-- Dome
	if c:find("^PRO+TE+CTO+S") then
		if system.start(n) then
			eventEmotePlayed(n,7)
		end
	end
	-- Anomaly
	if c:find("^A+NO+MA+LY+") and mice[n].level[1]>=data.anom.l or access then
		if system.start(n) then
			if os.time() > mice[n].timers[12][1] then
				if mice[n].timers[12][2] < mice[n].timers[12][3] then
					if math.random(5) == math.random(5) or access then
						mice[n].timers[12][2] = mice[n].timers[12][2] + 1
						opacity,objects = 1,{}
						anomaly = true
						tfm.exec.chatMessage(0,"\n\t"..tr(nil,"botMessages","anomaly").."\n")
					else
						tfm.exec.chatMessage(2,tr(n,"botMessages","anomtim"):format(data.anom.m/1000),n)
						mice[n].timers[12][1] = os.time() + data.anom.m
					end
				else
					tfm.exec.chatMessage(1,"<R>"..tr(n,"botMessages","powerlimit"):format("<VP>"..mice[n].timers[12][3].."</VP>"),n)
				end
			end
		end
	end
end
	-- Loop
eventLoop=function(time,left,start)
	_G.loopTimer = time/1000
	local alive,players,able = system.players(true)
	newmaptimer = newmaptimer + 1
	if newmaptimer>1 then
		advice = advice + .5
		if #alive==1 and loopTimer>3 and #players>1 then
			if not mice[alive[1]].isAfk[1] then
				local n = alive[1]
				tfm.exec.setPlayerScore(n,10,true)
				tfm.exec.giveCheese(n);tfm.exec.playerVictory(n)
				tfm.exec.chatMessage(0,tr(nil,"botMessages","won"):format(n))
				if #able > 5 then
					if adminRoom[2] then
						tfm.exec.chatMessage(1,tr(n,"admins","iftrue"),n,true)
					else
						mice[n].level[1] = mice[n].level[1] + (mice[n].level[1]<16 and 1 or mice[n].level[1]<31 and .5 or mice[n].level[1]<61 and .25 or mice[n].level[1]<101 and .1 or mice[n].level[1]>100 and .05)
						mice[n].stats.wins = mice[n].stats.wins + 1
					end
				else
					tfm.exec.chatMessage(1,tr(n,"botMessages","notplayers"),n,true)
				end
			end
			eventLoop(0,0,true)
		end
		if (time > -3 and time < 0) or left<=0 or (#alive < 1 and loopTimer>5) or start==true then
			if tostring(newp):sub(1,1) == "@" then
				tfm.exec.newGame(newp)
				newp = 0
			else
				local lastMap = currentMap or 0
				repeat currentMap = maps[math.random(#maps)] until currentMap ~= lastMap
				tfm.exec.newGame(currentMap,math.random(5)<3)
			end
		end
		if math.floor(left/1000) == 10 and #players>1 and #alive>#players/2 and not newtimer then
			tfm.exec.setGameTime(data.newtimer)
			tfm.exec.chatMessage(1,"<BV>"..tr(nil,"botMessages","newtimer"):format(data.newtimer))
			newtimer = true
			for n in next,tfm.get.room.playerList do
				mice[n].timers[1][3] = data.light.u + 5 -- Lightning
				mice[n].timers[4][3] = data.snova.u + 3 -- Supernova
				mice[n].timers[6][3] = data.dome.u + 5 -- Dome
				mice[n].timers[10][3] = data.hsmash.u + 3 -- Hulk Smash
				mice[n].timers[12][3] = data.anom.u + 1 -- Anomaly
			end
		end
		for k,v in ipairs(toDespawn) do
			if v[1] <= os.time()-450 then
				tfm.exec.removeObject(v[2])
				table.remove(toDespawn,k)
			end
		end
		if deathhug[1] then
			if os.time() > deathhug[2] then
				deathhug = {false,0}
			end
		end
		for n, v in next, mice do
			if v.dray[4] then
				if os.time() > v.dray[3]+300 then
					system.draybar(n,true)
				end
			end
			if os.time()>v.isAfk[2] and loopTimer>30 then
				v.isAfk[1] = true
			end
			if loopTimer>25 and v.isAfk[1] then
				if tfm.get.room.playerList[n] and not tfm.get.room.playerList[n].isDead then
					v.health = 0
				end
			end
			if loopTimer>4 then
				if v.health > data.life then v.health = data.life end
				if v.health < 0 then v.heath = 0 end
				if not v.ded then
					if v.health <= 0 then
						tfm.exec.killPlayer(n)
						ui.removeTextArea(3,n)
						v.ded = true
					end
				end
			end
			if v.hints then
				if advice%300 == 0 then
					local hints = tr(nil,"hints")
					local random = math.random(#hints)
					tfm.exec.chatMessage(3,"<ROSE>"..hints[random],n)
				end
			end
			local color = tonumber(v.level[3],16)
			if color then tfm.exec.setNameColor(n,color) end
			if v.hsmash[1] ~= 0 then
				if os.time() > v.hsmash[2] then
					if v.hsmash[1] == 1 then
						power.hulksmash(n,1)
					end
					if v.hsmash[1] == 2 then
						power.hulksmash(n,2,table.unpack(v.hsmash[3]))
						v.hsmash[1] = 0
					end
				end
			end
			v.time = v.time + .5
			if v.time % 2100 == 0 then
				if #players>5 then
					if adminRoom[2] then
						tfm.exec.chatMessage(1,tr(n,"admins","iftrue"),n,true)
					else
						v.level[1] = v.level[1] + (v.level[1]<16 and 1 or v.level[1]<31 and .5 or v.level[1]<61 and .25 or v.level[1]<101 and .1 or v.level[1]>100 and .05)
					end
				else
					tfm.exec.chatMessage(1,tr(n,"botMessages","notplayers"),n,true)
				end
			end
			local x,y = math.modf(v.level[1] + 1)
			if x-y == x and x ~= v.lbto then
				v.lbto = x
				local ceil = x < #colors*10+1 and math.ceil(x/10) or #colors
				v.level[2] = tr(n,"titles","title",ceil)
				v.level[3] = colors[ceil]
				if x>1 then
					local ceilLevel = math.ceil(v.level[1])
					if v.level[1] > 1 then tfm.exec.chatMessage(0,tr(nil,"titles","newlevel"):format("<J>"..n.."<G>","<font color='#"..v.level[3].."'>"..ceilLevel.."<G>!")) end
					if T.en.titles.unlock[ceilLevel] then
						tfm.exec.chatMessage(1,tr(n,"titles","unlock","unlocked")..tr(n,"titles","unlock",math.floor(v.level[1])),n)
					end
					if ceilLevel%10 == 0 and ceilLevel <= #colors*10 and v.level[1] > 1 then
						tfm.exec.chatMessage(0,tr(nil,"titles","unlock","title"):format(n,"<font color='#"..v.level[3].."'>",v.level[2]))
					end
				end
			end
			if v.showhealthbar then system.healthbar(n) end
		end
	else
		for n, v in next,mice do v.health = data.life end
	end
	if anomaly then
		opacity = opacity - .05
		if opacity <= .1 or start then
			ui.removeTextArea(3,nil)
			for _,id in next,objects do
				tfm.exec.removeObject(id)
			end
			anomaly = false
		else
			for i = 1,3 do
				local obj = {1,2,3,4,6,10,17,23,28,54,60,61,68};obj=obj[math.random(#obj)]
				local id = tfm.exec.addShamanObject(obj,math.random(800),math.random(380),math.random(360),math.random(-7,7),math.random(-5,5))
				table.insert(objects,id)
			end
			tfm.exec.explosion(math.random(15,785),math.random(380),math.random(-30,30),math.random(300,600))
			ui.addTextArea(3,"",nil,-1500,-1500,3000,3000,1,1,opacity,true)
			for n,p in next,tfm.get.room.playerList do
				if mice[n] and math.random(8) == 1 then
					mice[n].health = mice[n].health + math.random(1,5)
					tfm.exec.displayParticle(15,p.x,p.y,0,0,0,0,n)
				end
			end
		end
	end
end
	-- Died
eventPlayerDied=function(n)
	if mice[n] then mice[n].health = 0 end
end
	-- New Game
eventNewGame=function()
	ui.setMapName("<PT>#"..data.game.."   <G>|   <J>"..(tfm.get.room.xmlMapInfo.author or "???").." <BL>- "..(tfm.get.room.currentMap or "@???"))
	local _,players = system.players()
	if tfm.get.room.xmlMapInfo.xml:find("<T") then
		skip = true
		tfm.exec.setGameTime(6)
		eventLoop(loopTimer,6)
	else
		skip = false
		newtimer = false
		deathhug = {false,0}
		for n in next,tfm.get.room.playerList do
			system.draybar(n,true)
			-- Position
			mice[n].right = not tfm.get.room.mirroredMap
			-- Life
			mice[n].health = data.life
			mice[n].ded = false
			mice[n].isAfk = {true,0}
			-- Stats
			if #players > 5 then mice[n].stats.rounds = mice[n].stats.rounds + 1 end
			-- Powers
			mice[n].timers[1] = {3000 + os.time() + data.light.m,0,data.light.u} -- Lightning
			mice[n].timers[2] = 3000 + os.time() + data.lspeed.m -- Light Speed
			mice[n].timers[3] = 3000 + os.time() + data.whole.m -- Worm Hole
			mice[n].timers[4] = {3000 + os.time() + data.snova.m,0,data.snova.u} -- Supernova
			mice[n].timers[5] = 3000 + os.time() + data.helix.m -- Helix
			mice[n].timers[6] = {3000 + os.time() + data.dome.m,0,data.dome.u} -- Dome
			mice[n].timers[7] = 3000 + os.time() + data.ray.m -- Ray
			mice[n].timers[8] = {3000 + os.time() + data.dray.m,0,data.dray.u} -- Death Ray
			mice[n].timers[9] = 3000 + os.time() + data.dbjump.m -- Double Jump
			mice[n].timers[10] = {3000 + os.time() + data.hsmash.m,0,data.hsmash.u} -- Hulk Smash
			mice[n].timers[11] = {3000 + os.time() + data.dhug.m,0,data.dhug.u} -- Death Hug
			mice[n].timers[12] = {3000 + os.time() + data.anom.m,0,data.anom.u} -- Anomaly
			tfm.exec.respawnPlayer(n)
		end
		--[[
			if #players>1 and #players < 4 and not isRoom then
				for k,v in next,data do
					if type(v) == "table" and v.l~=nil then
						v.l = 0
					end
				end
				tfm.exec.chatMessage(1,"<PS>"..tr(nil,"botMessages","allpowers"))
			end
		]]--
		tfm.exec.setGameTime(data.help.m*60)
	end
	newmaptimer = 0
	if anomaly then
		anomaly = false
		opacity,objects = 1,{}
		ui.removeTextArea(5,nil)
	end
end
	-- Callbacks
eventTextAreaCallback=function(i,n,c)
	local p = {}
	for val in c:gmatch("[^_]+") do table.insert(p,val) end
	if p[1] == "closeUiSmart" then
		for v = i,i-9,-1 do
			ui.removeTextArea(v,n)
		end
	end
	if p[1] == "close" then
		if mice[n].newPlayer then mice[n].newPlayer=false;ui.removeTextArea(-100,n) end
		if mice[n].image[4] then for i = 1,2 do tfm.exec.removeImage(mice[n].image[4]) end end
		for v = i + 5,i - 22,-1 do 
			ui.removeTextArea(v,n)
		end
		mice[n].pages = 1
	end
	if p[1]:sub(1,5) == "close" then system.addMenu(n) end
	if (p[1] == "powers" or p[1] == "help" or p[1] == "rank") and os.time()>mice[n].nextUiTimer then
		mice[n].pages = (p[2]=="left" and (mice[n].pages>1 and mice[n].pages-1 or (p[1]=="powers" and #T.en.powers or p[1]=="help" and #T.en.help or 2)) or (mice[n].pages<(p[1]=="powers" and #T.en.powers or p[1]=="help" and #T.en.help or 2) and mice[n].pages+1 or 1))
		eventChatCommand(n,p[1],true)
	end
	if (p[1] == "+" or p[1] == "#" or p[1] == "?") and os.time()>mice[n].nextUiTimer then
		mice[n].pages = tonumber(p[2])
		eventChatCommand(n,p[1]=="+" and "powers" or p[1] == "?" and "help" or "rank",true)
	end
	if p[1] == "click" then
		tfm.exec.chatMessage(2,"<BV>"..data.help.l,n)
	end
	if p[1] == "room" then
		tfm.exec.chatMessage(2,"/room #"..data.game:lower()..math.random(0,999)..n,n)
	end
	if p[1] == "maps" then
		tfm.exec.chatMessage(2,"@"..table.concat(maps,", @"),n)
	end
	if p[1] == "P" then
		if tfm.get.room.playerList[p[2]] then
			eventChatCommand(n,"p "..p[2])
		end
	end
	if p[1] == "@?" then eventChatCommand(n,"help") end
	if p[1] == "@+" then eventChatCommand(n,"powers") end
	if p[1] == "@!" then eventChatCommand(n,"p") end
	if p[1] == "@#" then eventChatCommand(n,"rank") end
end
	-- Commands
eventChatCommand=function(n,c,m)
	local p = {}
	for val in c:gmatch("[^%s]+") do table.insert(p,val) end
	p[1] = p[1]:lower()
	if p[1] == data.help.c13 or p[1] == "p" then -- Profile
		eventTextAreaCallback(109,n,"close")
		local player = ""
		if p[2] then
			p[2] = string.nick(p[2])
			if tfm.get.room.playerList[p[2]] then
				player = p[2]
			end
		else player = n end
		if player ~= "" then
			ui.removeTextArea(9,n)
			ui.smart(200,n,1,player,tr(n,"other","profile_textformat"):format(mice[player].level[3],math.floor(mice[player].level[1]),mice[player].level[2],mice[player].level[1].."/"..(math.floor(mice[player].level[1]) + 1),mice[player].stats.rounds,mice[player].stats.wins,mice[player].stats.kills,system.getTime(mice[player].time),system.ratio(player)),260,60,230,230,false)
		end
	end
	if p[1] == data.help.c14 then -- Quality
		mice[n].graphics = not mice[n].graphics
		tfm.exec.chatMessage(2,tr(n,"enables","graphics",(mice[n].graphics and "on" or "off")),n)
		ui.removeTextArea(1,n)
	end
	if (p[1] == data.help.c1 or p[1] == "?") and os.time()>mice[n].nextUiTimer then -- Help
		ui.removeTextArea(7,n)
		if not m then mice[n].pages = 1 end	
		local info = tr(n,"help")
		local _format = {
			[1] = {{data.game},{data.game,data.help.m,data.botName}},
			[2] = {{""},{data.help.c1,data.help.c2,data.help.c3,data.help.c4,data.help.c5,data.help.c6,data.help.c7,data.help.c8,data.help.c13,data.help.c14,data.help.c15,data.help.c16}},
			[3] = {{""},{#colors*10,#colors,(mice[n].level[1]<16 and 1 or mice[n].level[1]<31 and .5 or mice[n].level[1]<61 and .25 or mice[n].level[1]<101 and .1 or mice[n].level[1]>100 and .05)}},
			[4] = {{""},{"<a href='event:click'>Click</a>",#maps,"\n<a href='event:maps'>@List</a>"}},
			[5] = {{""},{"<a href='event:room'>#"..data.game:lower()..math.random(0,999)..n.."</a>",data.help.c9,data.help.c10,data.help.c11,data.help.c12}},
			[6] = {{""},{""}},
		}
		ui.menu(100,n,1,info[mice[n].pages][1]:format(table.unpack(_format[mice[n].pages][1])),info[mice[n].pages][2]:format(table.unpack(_format[mice[n].pages][2])),150,50,350,280,info,"?","help")
	end
	if (p[1] == data.help.c2 or p[1] == "+" or p[1]=="power") and os.time()>mice[n].nextUiTimer then -- Powers
		ui.removeTextArea(8,n)
		if not m then mice[n].pages = 1 end
		if mice[n].image[4] then tfm.exec.removeImage(mice[n].image[4]) end
		local info = tr(n,"powers")
		local types = tr(n,"other","powers_types")
		local powers = {"lspeed","ray","whole","dbjump","dome","helix","light","snova","hsmash","dhug","anom","dray"}
		powers = powers[mice[n].pages]
		mice[n].image = data[powers].i
		mice[n].image[4] = tfm.exec.addImage(mice[n].image[1],"&0",mice[n].image[2],mice[n].image[3],n)
		ui.menu(100,n,1,info[mice[n].pages][1],"\n\n\n\n\n\n<p align='center'>"..tr(n,"other","powers_textformat",n):format(types[data[powers].t],data[powers].l,data[powers].u,table.concat(info[mice[n].pages][2]," <G>|</G> "),data[powers].d..((powers=="snova" or powers=="hsmash") and " <R>-5</R>" or powers=="dray" and " <R>-10</R>" or ""),info[mice[n].pages][3]),150,50,350,280,info,"+","powers")
	end
	if p[1] == data.help.c15 and os.time()>mice[n].nextUiTimer then -- Rank
		ui.removeTextArea(10,n)
		if not m then mice[n].pages = 1 end
		local info = tr(n,"ranking")
		local t = mice[n].pages == 1 and tfm.get.room.playerList or mice
		ui.menu(100,n,1,info[mice[n].pages][1],"<R>"..info[mice[n].pages][2].."\n\n<font size='13'><V><textformat leading='2' tabStops='[1,30,130,170,220,270,310]'><B>#\t?\tL\tR\tW\tK\t%</B>\n<font size='10'>"..system.rank(t,10,n),150,50,350,280,info,"#","rank")
	end
	if p[1] == data.help.c3 then -- Healthbar
		mice[n].showhealthbar = not mice[n].showhealthbar
		system.addMenu(n)
		for i = 0,4 do ui.removeTextArea(i,n) end
		tfm.exec.chatMessage(2,tr(n,"enables","healthbar",(mice[n].showhealthbar and "on" or "off")),n)
	end
	if p[1] == data.help.c4 then -- Hints
		mice[n].hints = not mice[n].hints
		tfm.exec.chatMessage(2,tr(n,"enables","hints",(mice[n].hints and "on" or "off")),n)
	end
	if p[1] == data.help.c5 then -- Messages
		mice[n].botMessages = not mice[n].botMessages
		tfm.exec.chatMessage(2,tr(n,"enables","bot",(mice[n].botMessages and "on" or "off")),n)
	end
	if p[1] == data.help.c6 and p[2] then -- Align
		p[2] = tonumber(p[2])
		if p[2] and p[2] < 5 and p[2] > 0 then
			mice[n].healthbarp = p[2]
			system.addMenu(n)
		end
	end
	if p[1] == data.help.c7 and p[2] then -- Np
		local _,players = system.players()
		if not isRoom and #players<4 then
			if newp == 0 then
				if p[2]:sub(1,1) == "@" then
					newp = p[2]
					tfm.exec.chatMessage(2,tr(n,"botMessages","nextmap"):format(newp),n)
				end
			else
				tfm.exec.chatMessage(2,tr(n,"botMessages","wnextmap"):format(newp),n)
				newp = 0
			end
		end
	end
	if p[1] == data.help.c8 then -- Langue
		if p[2] then
			mice[n].community = (p[2]=="default" and (T[tfm.get.room.playerList[n].community] and tfm.get.room.playerList[n].community or "en") or T[p[2]:lower()] and p[2]:lower() or T[mice[n].community] and mice[n].community or "en")
			tfm.exec.chatMessage(2,string.nick(p[1])..": "..mice[n].community,n)
		else
			tfm.exec.chatMessage(2,"<J>!"..data.help.c8.." <PT>"..system.languages(),n)
		end
	end
	if p[1] == data.help.c16 and p[2] then
		p[2] = tonumber(p[2]:match("@*(%d+)"))
		if p[2] then
			tfm.exec.chatMessage(2,"@"..p[2].." : "..tostring(table.find(maps,p[2])==true),n)
		end
	end
	if table.find(admins,n) then
		if isRoom then
			if p[1] == data.help.c9 then -- maxplayers
				if type(tonumber(p[2])) == "number" then
					p[2] = tonumber(p[2])
					if p[2] < 19 and p[2] > 2 then
						tfm.exec.setRoomMaxPlayers(p[2])
						tfm.exec.chatMessage(2,tr(nil,"admins","maxroom"):format(p[2]))
						adminRoom[2] = (p[2]<7 and true or false)
					end
				else
					if type(p[2]) == "string" and #p[2]>3 then
						tfm.exec.setRoomPassword(p[2])
						for k in next,tfm.get.room.playerList do
							if table.find(admins,k) then
								tfm.exec.chatMessage(2,tr(nil,"enables","pw","on"):format(p[2]),k)
							else
								tfm.exec.chatMessage(2,tr(nil,"enables","pw","on"):format(("*"):rep(#p[2])),k)
							end
						end
					else
						tfm.exec.chatMessage(2,tr(nil,"enables","pw","off"))
						tfm.exec.setRoomPassword("")
					end					
				end
			end
			if p[1] == data.help.c12 and p[2] and n == admins[1] then -- admin
				p[2] = string.nick(p[2])
				if tfm.get.room.playerList[p[2]] then
					if table.find(admins,p[2]) and p[2]~=admins[1] then
						table.destroy(admins,p[2])
						tfm.exec.chatMessage(2,tr(nil,"admins","notadmin"):format(p[2]))
					else
						table.insert(admins,p[2])
						tfm.exec.chatMessage(2,tr(nil,"admins","isadmin"):format(p[2]))
					end
				end
			end
		end
		if p[1] == data.help.c10 then -- renamebot
			if p[2] then
				p[2] = tonumber(p[2])
				if p[2]~=nil then
					if p[2] > 0 and p[2] < #botNames+1 then
						tfm.exec.chatMessage(2,tr(nil,"admins","renamed"):format(data.botName,botNames[p[2]]))
						data.botName = botNames[p[2]]
						bot = "<font color='#"..colors[#colors].."'><B>["..data.botName.."]</B></font> %s"
					end
				end
			else
				tfm.exec.chatMessage(2,"<R>"..p[1]..":",n)
				local text = "\n\t"
				p[1] = p[1]:lower()
				for k,v in next,botNames do
					text = text .. "!" .. p[1] .. " " .. k .. " = " .. v .. "\n\t"
				end
				tfm.exec.chatMessage(2,text,n)
			end
		end
		if p[1] == data.help.c11 and p[2] then -- setnewtime
			p[2] = tonumber(p[2])
			if type(p[2]) == "number" then
				p[2] = math.floor(p[2])
				if p[2] > 0 and p[2] < 6 then
					data.help.m = p[2]
					tfm.exec.chatMessage(2,tr(nil,"admins","time"):format(p[2]))
					adminRoom[2] = not p[2] == 3
				end
			end
		end
	end
end
for _,c in next,{data.help.c1,data.help.c2,data.help.c3,data.help.c4,data.help.c5,data.help.c6,data.help.c7,data.help.c8,data.help.c9,data.help.c10,data.help.c11,data.help.c12,data.help.c13,data.help.c14,data.help.c15,data.help.c16,"power","?","p","+"} do system.disableChatCommandDisplay(c,true) end
	-- Start
system.admins()
table.foreach(tfm.get.room.playerList,function(n)
	eventNewPlayer(n)
	tfm.exec.setPlayerScore(n,0)
end)
eventLoop(0,0,true)
tfm.exec.setGameTime(5)