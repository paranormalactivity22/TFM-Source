-- Transformice #anvilwar module loader - Version 2.248.1
-- By Morganadxana#0000
-- Included sub-modules: #beach, #naturalpark, #watercatch, #mountain.

local anvilwar = {
	_NAME = "anvilwar",
	_VERSION = "2.248.1",
	_MAINV = "53336.219 LTS",
	_DEVELOPER = "Morganadxana#0000" }
	
initAnvilwar = function()
--[[ #anvilwar
Module authors : Morganadxana#0000
(C) 2017-2023 Spectra Advanced Module Group
Version : RTM 53336.219 LTS
Compilation date : 01/19/2023 14:53 UTC
Sending player : Morganadxana#0000
Number of maps : 188
Number of module special members : 12 ]]--

_VERSION = "Lua 5.4"
_AUTHOR = "Morganadxana#0000"

maps={"@7467262","@7463118","@7436867","@7412348","@7467977","@7470456","@7480017","@7433435","@7483583","@7485139","@7486518","@7486596","@7486946","@7487828","@7488212","@7487008","@7493568","@7375714","@7495286","@7495744","@7497388","@7501996","@7511352","@7522536","@7522330","@7521998","@7540655","@7532950","@7542639","@7512942","@7114424","@7546132","@7546118","@7545653","@7543543","@7547908","@7544349","@7553313","@7554201","@7554203","@7554206","@7559566","@7560668","@7557788","@7559595","@7560873","@7562374","@7577539","@7596259","@7596249","@7599725","@7600421","@7648431","@7648852","@7648907","@7648899","@7658998","@7659642","@7663560","@7497808","@7489867","@5943895","@7666256","@3941375","@3956702","@4550664","@7678628","@3133327","@6947287","@7678921","@7679763","@7684909","@7672711","@3161494","@3996861","@7689921","@7685324","@7685127","@7695537","@7695654","@7693917","@7697503","@7723407","@5358451","@5451175","@6025712","@7727464","@7689192","@6198267","@6201091","@6244376","@6822539","@6879247","@7032584","@7760006","@7690854","@7686080","@7686207","@7685181","@7679443","@7802671","@7736985","@7495020","@7498659","@7543661","@7804689","@7804694","@7804362","@6759094","@4431434","@7807504","@7808946","@7809120","@7811210","@7811555","@7816639","@7818453","@7823992","@4084781","@7825615","@7826036","@7826050","@7826892","@7497395","@7512948","@7555653","@7688028","@7655209","@7690671","@7845674","@7845680","@7845682","@7845738","@7859139","@7845709","@7844985","@7859144","@7860343","@7860623","@7860498","@7863972","@7803705","@7845724","@7866585","@7834953","@7866596","@7703547","@7795869","@7869247","@7844978","@7869610","@7654290","@7876838","@7879243","@7664077","@7760487","@7802869","@7808177","@7882449","@7882451","@7882453","@7882454","@7882456","@7882458","@7879251","@7748874","@7891576","@7891577","@7891578","@7892788","@7902610","@7904039","@7869352","@7869389","@7841404","@7922465","@7919510","@7919518","@7919522","@7920813","@7922467","@7921968","@7922249","@7922362","@7922698","@7923483","@7922924","@7920975"}
map_names={"The Dual-Sided Fight Area","No Name","Inside the Castle","Hell and Water","A very simple waterfall","No Name","The Frozen Arena","The Golden Flying Arena","The Beach Test Map 1","Inside the Theasure Cave","A random fall map","No Name","The first #anvilwar map","The Beach Test Map 2","No Name","No Name","The Six Attributes","Inside the Ocean","No Name","No Name","No Name","No Name","The Stone Platforms","Inside the Hell","Testing Spaceship","Inside the Volcano","The Dance of Anvils on Stone","On the Space Tower","On the Edge of Void (Remaked)","No Name","No Name","On the Seabed","The Palace of Swords","The Castle of Fire","No Name","The Example of Map","Fitting The Anvil","The Beach Test Map 3","Dead Maze Map #1","Dead Maze Map #2","Dead Maze Map #3","The Clouds Under Trampoline","Dead Maze Map #4","No Name","Anvilwar Prison","The Pyramid of Grass","Arena of Darkness","No Name","The Limit of Waters","Black and White","On the Edge of the Space (v2)","Above the Sea Level (v3)","Dark Side of The Moon","Stairway to Heaven","Reversed Colors","Underwater Pression","The Darkin Blade","Testing Purposes","Christmas Frozen Cave","No Name","No Name","Default Water Force","Expert Lava Maze","Lava Links","Time of Revenge (v2)","Trampoline Test","Basketball of Death","Football Soccer Anvilwar","Destruction in Two Levels","The Forest","No Name","Island of Anvils","The Limit of Heaven","Giant and Crazy","Lava Battle Arena","Go and Back","Terrifying Love","Terror Christmas","Ninja Degrees","Chocoland","Cage","No Name","On the Edge of The Abyss","Pier of Columns","The Floor is Lava","Hybrid Grounds","The Flying Water","Natural Cloud Maze","Winter and Spring","Extended Grass Test","The Palace of Lava","Chocolate Maze","The Beach Test Map 4","Between Liquids","Soccer Teams #1","May the force Be with You","Don't Jump! #1","Autumn","Falling Walnuts","Ancient Egypt","Testing Acid Floors","Above the Earth Level","No Name","No Name","Do Not Hit The Anvil","Natural Landscape","Apocalypse","Look the Explosion!","The Beach Test Map 5","Love in Vain","Floating Acid","Moving Bridges","This is a Test","Only Two Grounds","Aim of Death","What The Hell","Discover of Seven Seas","Rotating Motors","Ultimate Acid Maze","The Anvils are Strange","Ghost Dimension","Animal Fury #1","Released Things","No Name","No Name","This is a Terror","No Name","No Name","Escape from Nyan Cat","Sharingan Eye","Zombie Attack","Destructed Zone","Eye of Black Hole","Soccer Teams #2","No Name","No Name","The Beach Test Map 6","The Beach Test Map 7","Vexos Arena","Releasing Anvils","The Hug of Agony","Try a Little More","No Name","No Name","No Name","Land of Spirits","No Name","No Name","No Name","No Name","Tobi - Akatsuki","Water Backgrounds","Up and Down","Watcher","Stranger Things","The Beach Test Map 8","Circle Compression","Gradient Colors","Background Reflection","Locked Dimensions","Now I See","Legacy Mansion","Water Equilibrium","Terrific Alternative","No Name","The Frozen Witch","Animal Fury #2","The Beach Test Map 9","Object Alchemy","Don't Jump! #2","The Bridge of Death","Balancing Things","Uzumaki Boruto Eyes","Namikaze Minato","Dragon Eyes","No Name","Stone Overriding","The Beach Test Map 10","Extreme Stone Maze","Neathian Guardian","No Name","No Name","No Name","Halloween","Soccer Teams #3","PSG","Apple VS Android","The Fallen Angel"}
objects={1,2,3,4,6,7,10,23,33,34,39,45,46,54,60,61,65,68,69,90,95}
players_red={}; alives_red={};
players_blue={}; alives_blue={};
lobby_map="@7884784"
current_map=""; actual_player="";
enabled=false; powerups=false; permafrost=false; night_mode=false; gravity=false; change=false; custom_mode=false;
mices=0; loop=0; turns=0; needs=0; turn=0; choose_time=20; time_passed=0; time_remain=0; current_red=0; current_blue=0; ping_check=2; sudden_death=false; old_limit=40;
points_loop=0; pf_time=0; general_time=0; total_time=0; map_id=0; set_player=""; set_map="-1"; def_map=-1; red_cap=""; blue_cap=""; temp_name=""; bar_text="";
settings={time=180,plimit=16,map_mode=0,map_select="@7412348",g_powerups=true,shoot_time=16,anti_kami=false,sd_switch=true,bg_switch=false}
mode="lobby"
divider="　　　　　　　　　";
images_id={};
playersList={}; helpers={}; mods={
"Dinamarquers#0000",
"Flaysama#5935",
"Chavestomil#0000",
"Lacoste#8972"};
admins={"Ashearcher#0000",
"Spectra_phantom#6089",
"Morganadxana#0000",
"Geracionz#0000"}
ninjas={"Viego#0345",
"Forzaldenon#0000",
"Caitlyndma7#0000",
"Aurelianlua#0000"};
data={}

lang = {}
lang.br = {
	version = "Versão",
	mices_room = "Ratos : ",
	comp_date = "Data de compilação : ",
	uploaded = "Carregado por ",
	ending = "Fim de jogo! Retornando à tela principal em alguns segundos...",
	won = "Você ganhou ",
	manager = "Você é o gerenciador desta sala. Digite !adcommands para ver os comandos disponíveis para os administradores de sala.",
	p1 = "usou o powerup Disparo Duplo!",
	p2 = "usou o powerup Disparo Triplo!",
	p3 = "usou o powerup Olha a Explosão!",
	p4 = "usou o powerup Congelamento!",
	p5 = "usou o powerup Modo Noturno!",
	p6 = "usou o powerup Chuva de Bigornas!",
	p7 = "usou o powerup Anomalia Gravitacional!",
	p8 = "usou o powerup Caixa de Acompanhamento!",
	p9 = "usou o powerup Tiro Aleatório!",
	p10 = "Você precisa ser capitão do seu time e possuir 30 pontos para reviver.<br>Além disso, não é possível reviver faltando menos de 30 segundos.",
	p0 = "Você não possui pontos e/ou níveis suficientes para usar este powerup.",
	ap = "Potência: ",
	ag = "Ângulo: ",
	suicide = "O seguinte jogador cometeu suicídio: ",
	rankw = "Aviso: Tenha em mente que os dados do Ranking e do Perfil são temporários e são redefinidos quando a sala esvazia.",
	tk1 = "Oh não! ",
	tk2 = " matou um companheiro de equipe: ",
	submission = "<br><N>As avaliações de mapas do #anvilwar estão abertas!",
	pw = "Senha trocada para: ",
	pw0 = "Senha removida.",
	limit = "Limite de ratos na sala: ",
	load1 = "O seguinte mapa será carregado: ",
	load2 = "Certifique-se que há pelo menos 1 jogador em cada equipe.",
	load0 = "Você precisa estar na tela principal para executar esta função. Digite !reset para fazer isso e tente novamente.",
	ac = "Você atualmente possui ",
	powerups = "<font size='11.5'><b>Tecla '1' - Disparo Duplo</b><br>Este powerup faz você atirar duas bigornas de uma vez.<br><b>Nível Mínimo:  1  /  Pontuação: 8pts</b><br><br><b>Tecla '2' - Disparo Triplo</b><br>Este powerup faz você atirar três bigornas de uma vez.<br><b>Nível Mínimo:  2  /  Pontuação: 12pts</b><br><br><b>Tecla '3' - Olha a Explosão</b><br>Este powerup permite a você criar uma explosão em um local do time inimigo.<br><b>Nível Mínimo:  3  /  Pontuação: 26pts</b><br><br><b>Tecla '4' - Congelamento</b><br>Este powerup congela todos os jogadores do time inimigo por um tempo limitado.<br><b>Nível Mínimo:  3  /  Pontuação: 20pts</b><br><p align='right'><a href='event:pw2'>Ir à Página 2</a>",
	commands = "<font size='11.5'>!commands (ou <b>B</b>) - Mostra esta caixa de texto.<br>!anvils - Mostra as bigornas disponíveis para compra<br>!help (ou <b>H</b>) - Mostra a ajuda do jogo.<br>!tc [mensagem] - Envia uma mensagem que aparece apenas para os jogadores do seu time.<br>!powerups (ou <b>U</b>) - Mostra os powerups disponíveis e seus respectivos custos.<br>!p [usuário] (ou <b>P</b>) - Mostra o perfil do usuário especificado. Digite apenas !p para ver o seu perfil.<br>!ranking (ou <b>R</b>) - Mostra o ranking dos jogadores na sala.",
	help = "<font size='12'><b>Bem-vindo ao #anvilwar!</b><br>O objetivo deste module é matar os jogadores do time adversário usando bigornas.<br><br>O jogo é simples de ser jogado. Quando for sua vez, use as teclas <b>Z e X</b> para mudar a potência do seu tiro e as teclas <b>C e V</b> para mudar o ângulo. Use a <b>BARRA DE ESPAÇO</b> para atirar.<br>O time que conseguir eliminar todos os jogadores do outro time vencerá o jogo!<br><br>Quando você joga ou ganha partidas, você vai receber <J><b>AnvilCoins</b><N>. Esta é a moeda do jogo. Ela pode ser usada para comprar novas bigornas.<br>Divirta-se e que vença o melhor time!<br><br><N><R><b>Administradores:</b><N> Morganadxana#0000 e Geracionz#0000<br><VP><b>Contribuidores:</b><N> Flaysama#5935, Chavestomil#0000, Dinamarquers#0000 e Spectra_phantom#6089<br><J><b>Tradutores:</b><N> Patrick_mahomes#1795 (BR)",
	adcommands = "<font size='11.5'><N>!pw [senha] - Adiciona uma senha na sala. Digite apenas !pw para remover a senha.<br>!reset - Cancela a partida atual e retorna à tela inicial.<br>!limit [número] - Altera o limite de jogadores da sala.<br>!lc [0-3] - Altera a configuração do verificador de latência dos jogadores.<br>!settings - Altera as configurações da sala.",
	seconds = " segundos.",
	leave = "Sair",
	join = "Entrar",
	getr = "Preparem-se! A partida vai começar em instantes!",
	powerups2 = "<font size='11.5'><b>Tecla '5' - Modo Noturno</b><br>Este powerup remove a visão dos jogadores do time inimigo por um tempo limitado.<br><b>Nível Mínimo: 3  /  Pontuação: 15pts</b><br><br><b>Tecla '6' - Chuva de Bigornas</b><br>Este powerup vai fazer chover bigornas em áreas aleatórias do time inimigo.<br><b>Nível Mínimo: 3  /  Pontuação: 25pts</b><br><br><b>Tecla '7' - Anomalia Gravitacional</b><br>Este powerup vai aumentar consideravelmente a gravidade até o outro time atirar.<br><b>Nível Mínimo: 4  /  Pontuação: 14pts</b><br><br><b>Tecla '8' - Caixa de Acompanhamento</b><br>Atira uma caixa de acompanhamento ao invés de uma bigorna.<br><b>Nível Mínimo: 2  /  Pontuação: 15pts</b><br><br><b>Tecla '9' - Tiro Aleatório</b><br>Atira uma objeto aleatório ao invés de uma bigorna.<br><b>Nível Mínimo: 2  /  Pontuação: 10pts</b><br><p align='right'><a href='event:pw1'>Voltar à Página 1</a>",
	using = "Bigorna sendo utilizada: ",
	ac0 = "Você não possui AnvilCoins suficientes para comprar esta bigorna :(",
	level = "avançou para o nível ",
	draw = "<b>Empate!</b><br>A tela principal será carregada em alguns instantes.",
	winblue = "<b>Vitória do time AZUL!</b><br>A tela principal será carregada em alguns instantes.",
	winred = "<b>Vitória do time VERMELHO!</b><br>A tela principal será carregada em alguns instantes.",
	as = "É a vez de: ",
	as1 = "<b>É a sua vez de atirar!</b><br><J>Use a BARRA DE ESPAÇO para atirar. Digite !help para mais informações.<br><br><N>Pontos para gastar com powerups: ",
	rm = "Sorteando mapa...",
	rm1 = "Mapa selecionado: ",
	t60s = "Faltam 60 segundos!",
	t30s = "Faltam 30 segundos!<br><br>A partir deste momento, não é mais possível reviver jogadores.",
	powerups_a = "Os powerups estão liberados!",
	time = "<b>Tempo esgotado!</b> O time adversário irá atirar agora.",
	cap_text = "foi escolhido para ser o líder do seu time.",
	cap = "<J><b>Você foi escolhido como o líder do time.</b><N><br>Digite !leader para saber as funcionalidades e os benefícios de ser o líder do seu time.",
	leader = "Os líderes dos times <b>são escolhidos aleatoriamente</b> e possui as seguintes vantagens em relação aos outros jogadores:<br><br>• Recebe 50% a mais de quantidade de pontos e AnvilCoins em relação aos outros jogadores<br>• Pode reviver jogadores mortos do seu time usando !rv [jogador]<br>• Pode transferir seus pontos para outro jogador do seu time usando !tp [jogador]<br>• Possui 20% a mais de tempo para atirar do que os outros jogadores<br>• Pode voltar a vida uma vez se morto.",
	legacy = "<N>Conheça todas as salas dentro do modo #anvilwar:<br><br><J><b>Fuja do tubarão (shaman) e sobreviva dentro do oceano!</b><br><VP>/sala #anvilwar00watercatch<br><br><J><b>Um mapa-script tipo village, porém de praia!</b><br><VP>/sala #anvilwar00beach<br><br><J><b>Um mapa-script para quem gosta de aventuras radicais e natureza!</b><br><VP>/sala #anvilwar00naturalpark<br><br><J><b>Teste suas habilidades de WJ escalando a montanha!</b><br><VP>/sala #anvilwar00mountain",
	disabled = "Este comando foi desabilitado por um administrador.",
	gametime = "Tempo",
	timeup = "<ROSE>Tempo esgotado! Este será o último tiro!",
	red_team = "Time Vermelho",
	blue_team = "Time Azul",
	revived = "O seguinte jogador reviveu: ",
	suddendeath = "<J><b>MORTE SÚBITA ATIVADA!</b><br><br>A partir de agora, a equipe que conseguir qualquer eliminação será declarada a vencedora!",
	latency = "Você não pode participar do jogo pois sua média de ping está muito alta.",
	custom = "<VP>O administrador da sala definiu regras personalizadas para esta sala.",
	defining = "<J>O administrador da sala está definindo regras personalizadas para esta sala. Por favor, aguarde...",
	kami = "<R>O modo anti-kamikaze está ativo nesta sala.",
	errorbg1 = "O modo Meninos contra Meninas está habilitado. Apenas meninas podem entrar no time vermelho.",
	errorbg2 = "O modo Meninos contra Meninas está habilitado. Apenas meninos podem entrar no time azul.",
	bgtext = "<N>O modo Meninos contra Meninas está habilitado. Meninos precisam entrar no time azul, enquanto meninas precisam entrar no time vermelho.",
	wrong = "Você não possui permissão para usar este comando",
	tmaperror = "O comando !testmap foi descontinuado. Para rodar um mapa personalizado, use o comando !settings e crie uma partida personalizada.",
	cap2 = "<J>Os capitães das equipes agora possuem 2 vidas!",
	life1 = "<VP>O capitão do time <BL>azul <VP>foi morto, e agora possui apenas <b>1</b> vida",
	life2 = "<VP>O capitão do time <R>vermelho <VP>foi morto, e agora possui apenas <b>1</b> vida",
}
lang.en = {
	version = "Version",
	mices_room = "Mice : ",
	comp_date = "Compilation date : ",
	uploaded = "Uploaded by ",
	ending = "End of game! The lobby screen will be loaded in a few seconds.",
	won = "You won ",
	manager = "You are the manager of this room. Type !adcommands to see all available commands for room managers.",
	p1 = "used the powerup Double Shoot!",
	p2 = "used the powerup Triple Shoot!",
	p3 = "used the powerup Explosion!",
	p4 = "used the powerup Permafrost!",
	p5 = "used the powerup Night Mode!",
	p6 = "used the powerup Anvil Rain!",
	p7 = "used the powerup Gravity Anomaly!",
	p8 = "used the powerup Companion Box!",
	p9 = "used the powerup Random Shoot!",
	p10 = "You must be the leader of your team and have at least 30 points to revive.<br>Also, isn't allowed to revive players on the last 30 seconds.",
	p0 = "You don't have level and score to use this powerup.",
	ap = "Power: ",
	ag = "Angle: ",
	suicide = "The following player commited suicide: ",
	rankw = "Keep in mind that the profile and ranking data is temporary and will be lost when the room is gone.",
	tk1 = "Oh no! ",
	tk2 = " has killed a player of her team: ",
	submission = "<br><N>#anvilwar Map Submissions are now open!",
	pw = "Password changed to: ",
	pw0 = "Password cleared.",
	limit = "New room mice limit ",
	load1 = "The next map will be loaded: ",
	load2 = "The room needs to have a least 1 player into each team.",
	load0 = "You needs to stay into LOBBY mode to use this command. Use !reset command and try again.",
	ac = "You currently have ",
	powerups = "<font size='11.5'><b>Key '1' - Double Shoot</b><br>This powerup makes you shoot 2 anvils at once.<br><b>Required Level: 1  /  Required Score: 8pts</b><br><br><b>Key '2' - Triple Shoot</b><br>This powerup makes you shoot 3 anvils at once.<br><b>Required Level: 2  /  Required Score: 12pts</b><br><br><b>Key '3' - Explosion</b><br>This powerup allows you to create an explosion on the enemy team area.<br><b>Required Level: 3  /  Required Score: 26pts</b><br><br><b>Key '4' - Permafrost</b><br>This powerup freezes all enemy team players by a limited time.<br><b>Required Level: 3  /  Required Score: 20pts</b><br><p align='right'><a href='event:pw2'>Go to Page 2</a>",
	commands = "<font size='11.5'>!commands (or <b>B</b> key) - Display this message box.<br>!anvils - Show available #anvilwar anvils to buy.<br>!help (or <b>H</b> key) - Display the game help.<br>!tc [message] - Send a message that is visible only for players of your team.<br>!powerups (or <b>U</b> key) - Show all available powerups and their respective costs.<br>!p [username] (or <b>P</b> key) - Show the profile of the specified user. Type !p only to see your profile.<br>!ranking (or <b>R</b> key) - Show the room ranking.",
	adcommands = "<font size='11.5'><N><br>!pw [password] - Locks the room with a password. Use only !pw to clear the password.<br>!reset - Cancel the current match and returns to the lobby screen.<br>!limit [number] - Change the limit of mices on the room.<br>!lc [0-3] - Change the level of the player's latency checker.<br>!settings - Change the room settings.",
	help = "<font size='12'><b>Welcome to #anvilwar!</b><br>The objective of this module is kill all the players of other team using anvils.<br><br>The module is very easy to play. When reaches your turn, use <b>Z and X</b> keys to change the intensity of the anvil shoot and <b>C and V</b> keys to change the angle of the anvil. Use the <b>SPACEBAR</b> to shoot.<br>The team that kill all players of other team will win the game!<br><br>When you kill players or win matches, you will receive <J><b>AnvilCoins</b><N>. This is the money of #anvilwar module. It can be used to unlock custom anvils.<br>Enjoy the module and may the best team wins!<br><br><N><R><b>Administrators:</b><N> Morganadxana#0000 and Geracionz#0000<br><VP><b>Contributors:</b><N> Flaysama#5935, Chavestomil#0000, Dinamarquers#0000 and Spectra_phantom#6089<br><J><b>Translators:</b><N> Patrick_mahomes#1795 (BR)",
	seconds = " seconds.",
	leave = "Leave",
	join = "Join",
	getr = "Get Ready! The match will start in a few seconds!",
	powerups2 = "<font size='11.5'><b>Key '5' - Night Mode</b><br>This powerup remove the vision of players of enemy team.<br><b>Required Level: 3  /  Required Score: 15pts</b><br><br><b>Key '6' - Anvil Rain</b><br>This powerup will create a anvil rain on random enemy team areas.<br><b>Required Level: 3  /  Required Score: 25pts</b><br><br><b>Key '7' - Gravity Anomaly</b><br>This powerup will incrase the gravity of map by 200% until the next player shoots.<br><b>Required Level: 4  /  Required Score: 14pts</b><br><br><b>Key '8' - Companion Box</b><br>Shoot an companion box instead of an anvil.<br><b>Required Level: 2  /  Required Score: 15pts</b><br><br><b>Key '9' - Random Shoot</b><br>Shoot an random object instead of an anvil.<br><b>Required Level: 2  /  Required Score: 10pts</b><br><p align='right'><a href='event:pw1'>Return to Page 1</a>",
	using = "You are now using the ",
	ac0 = "You don't have AnvilCoins to buy this anvil.",
	level = "reached the level",
	draw = "<b>Draw!</b><br>The lobby screen will load shortly.",
	winblue = "<b>Victory of the BLUE team!</b><br>The lobby screen will load shortly.",
	winred = "<b>Victory of the RED team!</b><br>The lobby screen will load shortly.",
	as = "Actual shooter: ",
	as1 = "<b>It's your time to shoot.</b><br><J>Use the SPACEBAR to shoot. Type !help for more information.<br><br><N>Points available: ",
	rm = "Randomizing map...",
	rm1 = "Selected Map : ",
	t60s = "60 seconds remaining!",
	t30s = "30 seconds remaining!<br><br>After this warning, isn't possible to revive players.",
	powerups_a = "The powerups are now available!",
	time = "<b>Time is up!</b> The next team will play now.",
	cap_text = "was selected to be the leader of your team.",
	cap = "<J><b>You are now the team leader.</b><N><br>Type !leader to know all the functions and benefits of team leaders.",
	leader = "The team leaders <b>are randomly choosed</b> and have various advantages and benefits:<br><br>• Will receive 50% more points and AnvilCoins regarding to the other players<br>• Can revive dead team players using the !rv [player] command<br>• Can transfer your powerup score to other team players using the !tp [player] command<br>• Have 20% more shooting time<br>• Will be revived once if was killed.",
	legacy = "",
	disabled = "This command was disabled by an administrator.",
	gametime = "Game Time",
	timeup = "<ROSE>Time is up! This will be the last shoot!",
	red_team = "Red Team",
	blue_team = "Blue Team",
	revived = "The following player revived: ",
	suddendeath = "<J><b>SUDDEN DEATH ENABLED!</b><br><br>The team that gets any player killed will lose the game!",
	latency = "You cannot enter the game because your average latency is very high.",
	custom = "<VP>The room administrator defined custom rules for this room.",
	defining = "<J>The room administrator is defining custom rules for this room. Please wait...",
	kami = "<R>The anti-kamikaze is now active.",
	errorbg1 = "The Boys against Girls mode is active. Only girls can join the red team.",
	errorbg2 = "The Boys against Girls mode is active. Only boys can join the blue team.",
	bgtext = "<N>The Boys against Girls mode is now active. Boys need to join the blue team, and girls need to join the red team.",
	wrong = "You don't have permission to use this command",
	tmaperror = "The !testmap command was discontinued. To run a custom map, create a custom match using the !settings command.",
	cap2 = "<J>The team capitains have now 2 lifes each!",
	life1 = "<VP>The capitain of the <BL>blue <VP>was killed. (S)he has now <b>1</b> life",
	life2 = "<VP>The capitain of the <R>red <VP>was killed. (S)he has now <b>1</b> life",
}
if tfm.get.room.isTribeHouse == true then
	text = lang.en
else
	if tfm.get.room.community == "br" or tfm.get.room.community == "pt" then
		text = lang.br
	else
		text = lang.en
	end
end

for _,f in next,{"AutoShaman","AutoScore","AutoNewGame","AutoTimeLeft","PhysicalConsumables","DebugCommand","MortCommand","AfkDeath"} do
	tfm.exec["disable"..f](true)
end
for _,g in next,{"help","sync","pw","kill","commands","adcommands","powerups","p","limit","ranking","t","T","tc","TC","Tc","tC","anvils","set","testmap","defmap","leader","rv","tp","changelog","get","lc","settings"} do
	system.disableChatCommandDisplay(g)
end
if not tfm.get.room.isTribeHouse then tfm.exec.setRoomMaxPlayers(40) end

function tableSearch(table,element)
	for i=1,rawlen(table) do
		if element == table[i] then
			return true
		end
	end
end

function showMessage(message,name)
	temp_text=string.gsub(message,"<b>","")
	temp_text=string.gsub(temp_text,"</b>","")
	if tfm.get.room.isTribeHouse == false then
		tfm.exec.chatMessage(message,name)
	elseif tfm.get.room.isTribeHouse == true then
		if name == nil then
			print("<ROSE>[Test Mode] : <br><BL>"..temp_text.."")
		else
			print("<ROSE>[Test Mode] - "..name.." : <br><BL>"..temp_text.."")
		end
	end
end

function showImage(name,link,x,y,scalex,scaley)
	image_id=tfm.exec.addImage(link,":1",x,y,name,scalex,scaley,0,0.95)
	table.insert(images_id,image_id)
end
	
function showImageBackground(name,link,x,y,scalex,scaley)
	image_id=tfm.exec.addImage(link,"?1",x,y,name,scalex,scaley,0,1)
	table.insert(images_id,image_id)
end

function showAvailableAnvils(name)
	i=0
	for _,link in next,{"1788f85d7e2.png","1788f85ef53.png","1788f8606c4.png","1788f861e33.png"} do
		i=i+1
		image_id=tfm.exec.addImage(link,"&1",63,120+(i*50),name,1.0,1.0,0,1.0)
		table.insert(data[name].active_imgs,image_id)
	end
	i=0
	for _,link in next,{"1788f8635a6.png","1788f864d16.png","1788f866489.png","1789826a888.png"} do
		i=i+1
		image_id=tfm.exec.addImage(link,"&1",217,120+(i*50),name,1.0,1.0,0,1.0)
		table.insert(data[name].active_imgs,image_id)
	end
	i=0
	for _,link in next,{"1789826bffa.png","1789826d76c.png","178982679a6.png","17898269116.png"} do
		i=i+1
		image_id=tfm.exec.addImage(link,"&1",389,120+(i*50),name,1.0,1.0,0,1.0)
		table.insert(data[name].active_imgs,image_id)
	end
	i=0
	for _,link in next,{"179ec21b84d.png","179ec2171f9.png","179ec21896c.png","179ec21a0dd.png"} do
		i=i+1
		image_id=tfm.exec.addImage(link,"&1",561,120+(i*50),name,1.0,1.0,0,1.0)
		table.insert(data[name].active_imgs,image_id)
	end
end

function showTeams(name)
	ui.addTextArea(480,"<font size='18'><font color='#ff4500'><p align='center'><b><a href='event:enter_red'>"..text.join.."",name,320,140,150,25,0,0,0.9,true)
	ui.addTextArea(481,"<font size='18'><font color='#0045ff'><p align='center'><b><a href='event:enter_blue'>"..text.join.."",name,320,230,150,25,0,0,0.9,true)
end

function showMenu(name,color,x,y,width,height,title,content)
	if data[name].opened == false then
		data[name].opened=true
		ui.addTextArea(1004,"",name,-1000,-600,2800,1600,0x000001,0x000001,0.65,true)
		ui.addTextArea(1001,"",name,x+5,y+5,width,height,color,color,0.95,true)
		ui.addTextArea(1000,"<font size='13'><i><br><br>"..content.."",name,x,y,width,height,0x151515,color,0.95,true)
		ui.addTextArea(1002,"<font color='#f8d802'><font size='14'><p align='center'><i><b>"..title.."",name,x+5,y+5,width-11,22,0x101010,0x101010,0.95,true)
		ui.addTextArea(1003,"<font color='#ff2300'><font size='14'><b><a href='event:close'>X</a>",name,x+width-25,y+5,width-10,20,0,0,0.95,true)
	end
end

function showRoomSettings(name)
	choose_time=30
	if data[name] and data[name].ranking >= 2 then
		for i=1000,1011 do
			ui.removeTextArea(i,name)
		end
		data[name].opened=false
		if settings.map_mode == 0 then
			string1="normal"
		elseif settings.map_mode == 1 then
			string1="@code"
		end
		showMenu(name,0x405401,200,125,400,235,""..tfm.get.room.name.." Room Settings","<p align='center'>Custom Room Mode : <b>"..tostring(custom_mode).."</b> <a href='event:cmode'>[change]</a></p><br>------------------ CUSTOM ROOM SETTINGS ------------------<br>Game Time : <b>"..tostring(settings.time).."</b> sec <a href='event:ctimea'>[-]</a> <a href='event:ctimeb'>[+]</a><br>Max Players/Team : <b>"..tostring(settings.plimit).."</b> <a href='event:cplayersa'>[-]</a> <a href='event:cplayersb'>[+]</a><br>Map Mode : <b>"..string1.."</b> <a href='event:cmap'>[change]</a><br>Map @code (for @CODE mode) : <b>"..tostring(settings.map_select).."</b> <a href='event:cmapcode'>[change]</a><br>Powerups : <b>"..tostring(settings.g_powerups).."</b> <a href='event:cpowerups'>[change]</a><br>Shooting Time : <b>"..tostring(settings.shoot_time).."</b> sec <a href='event:cstimea'>[-]</a> <a href='event:cstimeb'>[+]</a><br>Anti-Kamikaze Mode : <b>"..tostring(settings.anti_kami).."</b> <a href='event:ckami'>[change]</a><br>Sudden Death : <b>"..tostring(settings.sd_switch).."</b> <a href='event:csd'>[change]</a><br>Boys against Girls mode : <b>"..tostring(settings.bg_switch).."</b> <a href='event:bgd'>[change]</a>")
	end
end

function showLobbyText(name)
	ui.addTextArea(402,"<p align='center'><font size='12'><b><font face='Courier New'><i>"..text.version.." RTM 53336.219 LTS - "..text.comp_date.."01/19/2023 14:53 UTC - "..text.uploaded.."Morganadxana#0000</i>",name,-10,380,820,36,0,0,1.0,true)
end

function setLeaders()
	if rawlen(alives_red) > 0 and rawlen(alives_blue) > 0 then
		red_cap=alives_red[math.random(#alives_red)]
		blue_cap=alives_blue[math.random(#alives_blue)]
		showMessage(""..red_cap.." "..text.cap_text.."")
		showMessage(""..blue_cap.." "..text.cap_text.."")
		if rawlen(alives_red) >= 2 and rawlen(alives_blue) >= 2 then
			data[red_cap].lives=2; data[blue_cap].lives=2;
			showMessage(text.cap2)
		end
		showMessage(text.cap,red_cap)
		showMessage(text.cap,blue_cap)
		tfm.exec.setNameColor(red_cap,0x80f000)
		tfm.exec.setNameColor(blue_cap,0x80f000)
	else
		lobby();
	end
end

function eventRanking(name)
	local sc = {}
	for id,name in next,playersList do
		sc[#sc+1] = {n=name,s=data[name].kills,f=data[name].level,d=data[name].winrate,l=data[name].eff}
	end

	table.sort(sc,function(a,b) return a.s>b.s end)

	str1 = ''
	str2 = ''
	str3 = ''
	str4 = ''
	str5 = ''
	rk = ""
	for k,v in pairs(sc) do
		if k < 21 then
			if str ~= '' then
				if k < 10 then rk=tostring(0)..k; else rk=tostring(k) end
				str1=str1.."<br><N>"..rk.."° | <VP>"..v.n..""
				str2=str2.."<br><b><N>"..v.s.."</b>"
				str3=str3.."<br><N>"..v.f..""
				str4=str4.."<br><N>"..v.d..""
				str5=str5.."<br><N>"..v.l..""
			else
				str1="<J>"..k.."° | <VP>"..v.n..""
				str2="<J><b>"..v.s.."</b>"
				str3="<J>"..v.f..""
				str4="<J>"..v.d..""
				str5="<J>"..v.l..""
			end
		end
	end
	showMenu(name,0xffffff,200,35,400,340,""..tfm.get.room.name.." Ranking","<font size='12'># / Name                                            Kills  Level   Wins% Kills%")
	ui.addTextArea(1010,"<p align='left'><font size='12'><font face='Consolas'>"..str1,name,200,70,220,320,0,0,nil,true)
	ui.addTextArea(1011,"<p align='right'><font size='12'><font face='Consolas'>"..str2,name,420,70,40,320,0,0,nil,true)
	ui.addTextArea(1007,"<p align='right'><font size='12'><font face='Consolas'>"..str3,name,460,70,40,320,0,0,nil,true)
	ui.addTextArea(1008,"<p align='right'><font size='12'><font face='Consolas'>"..str4,name,500,70,50,320,0,0,nil,true)
	ui.addTextArea(1009,"<p align='right'><font size='12'><font face='Consolas'>"..str5,name,550,70,50,320,0,0,nil,true)
end

function giveRankings(name)
	if data[name] then
		if tableSearch(helpers,name) == true then
			data[name].ranking=1
			tfm.exec.setNameColor(name,0x00a9a9)
		elseif tableSearch(mods,name) == true then
			data[name].ranking=2
			tfm.exec.setNameColor(name,0xa9a900)
		elseif tableSearch(ninjas,name) == true then
			data[name].ranking=3
		elseif tableSearch(admins,name) == true then
			data[name].ranking=4
			tfm.exec.setNameColor(name,0xa90000)
		end
	end
end

function updateTextBar()
	if mode == "end" then
		ui.setMapName("<VP><b>"..text.ending.."</b>   <G>|   <N>"..text.mices_room.."<V><b>"..mices.."</b><")
	else
		ui.setMapName("<N><b>#anvilwar</b>   <G>|   <VP>"..text.version.." <b>RTM 53336.219 LTS</b> <R>   <G>|   <N>"..text.mices_room.."<V><b>"..mices.."</b><")
	end
end

function spawnAnvil(object,x,y,xp,yp,ghost)
	if data[actual_player].powerup < 8 then
		id=tfm.exec.addShamanObject(object,x,y,xp,yp,ghost)
		if data[actual_player].current_anvil == 1 then
			tfm.exec.addImage("1788f85ef53.png","#"..id.."",-20,-12)
		elseif data[actual_player].current_anvil == 2 then
			tfm.exec.addImage("1788f8606c4.png","#"..id.."",-20,-12)
		elseif data[actual_player].current_anvil == 3 then
			tfm.exec.addImage("1788f861e33.png","#"..id.."",-20,-12)
		elseif data[actual_player].current_anvil == 4 then
			tfm.exec.addImage("1788f8635a6.png","#"..id.."",-20,-12)
		elseif data[actual_player].current_anvil == 5 then
			tfm.exec.addImage("1788f864d16.png","#"..id.."",-20,-12)
		elseif data[actual_player].current_anvil == 6 then
			tfm.exec.addImage("1788f866489.png","#"..id.."",-20,-12)
		elseif data[actual_player].current_anvil == 7 then
			tfm.exec.addImage("1789826a888.png","#"..id.."",-20,-12)
		elseif data[actual_player].current_anvil == 8 then
			tfm.exec.addImage("1789826bffa.png","#"..id.."",-20,-12)
		elseif data[actual_player].current_anvil == 9 then
			tfm.exec.addImage("1789826d76c.png","#"..id.."",-20,-12)
		elseif data[actual_player].current_anvil == 10 then
			tfm.exec.addImage("178982679a6.png","#"..id.."",-20,-12)
		elseif data[actual_player].current_anvil == 11 then
			tfm.exec.addImage("17898269116.png","#"..id.."",-20,-12)
		elseif data[actual_player].current_anvil == 12 then
			tfm.exec.addImage("179ec21b84d.png","#"..id.."",-20,-12)
		elseif data[actual_player].current_anvil == 13 then
			tfm.exec.addImage("179ec2171f9.png","#"..id.."",-20,-12)
		elseif data[actual_player].current_anvil == 14 then
			tfm.exec.addImage("179ec21896c.png","#"..id.."",-20,-12)
		elseif data[actual_player].current_anvil == 15 then
			tfm.exec.addImage("179ec21a0dd.png","#"..id.."",-20,-12)
		end
	elseif data[actual_player].powerup == 8 then
		id=tfm.exec.addShamanObject(61,x,y,xp,yp,ghost)
	elseif data[actual_player].powerup == 9 then
		id=tfm.exec.addShamanObject(objects[math.random(#objects)],x,y,xp,yp,ghost)
	end
end

function calculateMatchTime()
	if custom_mode == false then
		total_time=165+(mices*5)	
	else
		total_time=settings.time
	end
	general_time=total_time
end

function calculatePoints(name)
	if data[name] then
		data[name].winrate=math.floor((data[name].wins/data[name].matches)*100)
		if data[name].current_coins > 0 then
			if name == red_cap or name == blue_cap then
				local gained=math.floor(data[name].current_coins*1.2)+data[name].score+turns
				data[name].coins=data[name].coins+gained
				showMessage("<VP>"..text.won.."<b>"..gained.."</b> AnvilCoins!",name)
			else
				local gained=math.floor(data[name].current_coins*0.8)+math.floor(data[name].score*0.5)+math.floor(turns*0.5)
				data[name].coins=data[name].coins+gained
				showMessage("<VP>"..text.won.."<b>"..gained.."</b> AnvilCoins!",name)
			end
			data[name].exp=data[name].exp+(data[name].current_coins*2)
			if data[name].exp >= data[name].maxp then
				advanceLevel(name)
			end
		end
		data[name].current_coins=0
		data[name].eff=math.floor((data[name].kills/data[name].killeds)*100)
	end
end

function suddenDeath()
	showMessage(text.suddendeath)
	sudden_death=true;
	general_time=60;
	setShooter()
end

function detectVictory()
	if turns == 1 then
		for _,name in next,players_blue do
			if tfm.get.room.playerList[name].isDead == false then
				data[name].lives=1
			end
		end
		for _,name in next,players_red do
			if tfm.get.room.playerList[name].isDead == false then
				data[name].lives=1
			end
		end
		setLeaders()
	end
	if general_time > 0 then
		if rawlen(alives_red) == 0 and rawlen(alives_blue) == 0 then
			drawMatch()
		elseif rawlen(alives_red) == 0 then
			victoryBlue()
		elseif rawlen(alives_blue) == 0 then
			victoryRed()
		else
			setShooter()
		end
	else
		if custom_mode == false then
			if rawlen(alives_red) == rawlen(alives_blue) then
				if (rawlen(alives_red)+rawlen(alives_blue)) >= 3 and sudden_death == false then
					suddenDeath()
				else
					drawMatch()
				end
			end
		else
			if rawlen(alives_red) == rawlen(alives_blue) then
				if (rawlen(alives_red)+rawlen(alives_blue)) >= 3 and settings.sd_switch == true and sudden_death == false then
					suddenDeath()
				else
					drawMatch()
				end
			end
		end
		if rawlen(alives_red) > rawlen(alives_blue) then
			victoryRed()
		end
		if rawlen(alives_red) < rawlen(alives_blue) then
			victoryBlue()
		end
	end
end

function updatePlayerList()
	text1=""; text2="";
	for id,name in next,players_red do
		text1="<font size='13'>"..text1.."<b> "..id.."</b> - "..name.."<br>"
	end
	for id,name in next,players_blue do
		text2="<font size='13'>"..text2.."<b> "..id.."</b> - "..name.."<br>"
	end
	if mode == "lobby" or mode == "map_sort" then
		for name,player in next,tfm.get.room.playerList do
			if data[name] and data[name].opened == false then
				ui.addTextArea(-4,"<font color='#000001'><font face='Consolas,Lucida Console'><font size='9'>"..text2.."",name,501,125,260,270,0,0,1.0,true)
				ui.addTextArea(-3,"<BL><font face='Consolas,Lucida Console'><font size='9'>"..text2.."",name,500,124,260,270,0,0,1.0,true)
				ui.addTextArea(-1,"<font color='#000001'><font face='Consolas,Lucida Console'><font size='9'>"..text1.."",name,21,125,260,270,0,0,1.0,true)
				ui.addTextArea(-2,"<R><font face='Consolas,Lucida Console'><font size='9'>"..text1.."",name,20,124,260,270,0,0,1.0,true)
			end
		end
	end
end

function removeImagePlayers(name)
	if rawlen(data[name].active_imgs) > 0 then
		for _,id in next,data[name].active_imgs do
			tfm.exec.removeImage(id)
		end
		data[name].active_imgs={}
	end
end

function removeScoreboard(name)
	if data[name] then
		tfm.exec.removeImage(data[name].scoreboard_id,false)
		data[name].scoreboard_id=-1
	end
	for j=5651, 5658 do
		ui.removeTextArea(j,nil)
	end
end

function checkPing(name)
	if data[name] then
		if ping_check == 0 then
			return false
		elseif ping_check == 1 then
			if tfm.get.room.playerList[name].averageLatency >= 2000 then
				return true
			else
				return false
			end
		elseif ping_check == 2 then
			if tfm.get.room.playerList[name].averageLatency >= 1000 then
				return true
			else
				return false
			end
		elseif ping_check == 3 then
			if tfm.get.room.playerList[name].averageLatency >= 500 then
				return true
			else
				return false
			end
		end
	end
end

function eventNewPlayer(name)
	mices=mices+1
	if not data[name] then
		data[name]={level=1,exp=0,maxp=100,score=0,kills=0,wins=0,matches=0,killeds=0,eff=0.0,winrate=0.0,coins=0,multikills=0,
		killed=false,team=0,ranking=0,angle=0,power=5,powerup=0,
		current_coins=0,opened=false,active_imgs={},anvils={0,0,0,0,0,0,0,0,0,0,0},current_anvil=0,test_time=0,scoreboard_id=-1,left=false,lives=0}
		table.insert(playersList,name)
	else
		data[name].left=false
	end
	if name:sub(1,1) == "*" then
		data[name].ranking=-1
	end
	if string.find(tfm.get.room.name,name) then
		table.insert(mods,name)
		showMessage(text.manager,name)
	end
	for _,k in next,{32,48,49,50,51,52,53,54,55,56,57,66,67,72,77,80,82,85,86,88,90,112,113,114,115,116,117,118} do
		tfm.exec.bindKeyboard(name,k,true,true)
	end
	system.bindMouse(name,true)
	if mode == "lobby" then
		if data[name] then
			if data[name].ranking >= 0 then
				showImageBackground(name,"1835da9d15e.png",0,1,1.0,1.0)
				showTeams(name)
				showLobbyText(name)
				tfm.exec.respawnPlayer(name)
			end
		end
		updatePlayerList()
	end
	if mode == "wait2" then
		data[name].scoreboard_id = tfm.exec.addImage("1835da984ec.png", ":1", 266, 15, name, 1.0, 1.0, 0, 1)
	end
	giveRankings(name)
	tfm.exec.setPlayerScore(name,0,false)
end

for name,player in next,tfm.get.room.playerList do
	eventNewPlayer(name)
end

function permaFrost()
	if data[actual_player].team == 1 then
		for _,name in next,players_blue do
			tfm.exec.freezePlayer(name,true)
		end
	elseif data[actual_player].team == 2 then
		for _,name in next,players_red do
			tfm.exec.freezePlayer(name,true)
		end
	end
end

function anvilRain()
	if data[actual_player].team == 1 then
		for i=1,7 do
			spawnAnvil(10,math.random(850,1599),100,0,1,false)
		end
	elseif data[actual_player].team == 2 then
		for i=1,7 do
			spawnAnvil(10,math.random(1,750),100,0,1,false)
		end
	end
end

function showPowerMeter(name)
	bar_text=""
	for i=1,data[name].power do
		bar_text=bar_text.."▊▊"
	end
	ui.addTextArea(750,"<font size='15'>         Anvil Power: <b>"..data[name].power.."</b> "..bar_text.."",name,10,376,780,20,0x010101,0x010101,1.0,true)
end

function showAngleMeter(name)
	ag=math.ceil(data[name].angle/8)
	bar_text=""
	for i=1,ag do
		bar_text=bar_text.."▊▊▊"
	end
	ui.addTextArea(750,"<font size='15'>                   Anvil Angle: <b>"..data[name].angle.."°</b> "..bar_text.."",name,10,376,780,20,0x010101,0x010101,1.0,true)
end

function nightMode()
	if data[actual_player].team == 1 then
		ui.addTextArea(999,"",nil,800,-300,1200,1400,0x000001,0x000001,0.99,false)
	elseif data[actual_player].team == 2 then
		ui.addTextArea(999,"",nil,-400,-300,1200,1400,0x000001,0x000001,0.99,false)
	end
end

function setScores(name,points)
	if offset == false then
		data[name].score=points
	else
		data[name].score=data[name].score+points
	end
	tfm.exec.setPlayerScore(name,data[name].score,false)
end

function eventKeyboard(name,code,down,x,y)
	if mode == "shoot" and actual_player == name and enabled == true then
		if code == 32 then
			if data[name].team == 1 then
				spawnAnvil(10,x,y-55,(data[name].angle)*-1,(2.5+data[name].power*1.2),-5-(data[name].power*0.3),false)
				if data[name].powerup == 1 then
					id=spawnAnvil(10,x+45,y-55,(data[name].angle)*-1,(2.5+data[name].power*1.2),-5-(data[name].power*0.3),false)
				elseif data[name].powerup == 2 then
					for i=1,2 do
						spawnAnvil(10,x+(45*i),y-55,(data[name].angle)*-1,(2.5+data[name].power*1.2),-5-(data[name].power*0.3),false)
					end
				end
				tfm.exec.playSound("bouboum/x_explosion_3.mp3", 90)
			elseif data[name].team == 2 then
				spawnAnvil(10,x,y-55,(data[name].angle)*-1,(2.5+data[name].power*1.2)*-1,-5-(data[name].power*0.3),false)
				if data[name].powerup == 1 then
					spawnAnvil(10,x+45,y-55,(data[name].angle)*-1,(2.5+data[name].power*1.2)*-1,-5-(data[name].power*0.3),false)
				elseif data[name].powerup == 2 then
					for i=1,2 do
						spawnAnvil(10,x+(45*i),y-55,(data[name].angle)*-1,(2.5+data[name].power*1.2)*-1,-5-(data[name].power*0.3),false)
					end
				end
				tfm.exec.playSound("bouboum/x_explosion_3.mp3", 90)
			end
			mode="wait3"
			enabled=false
			tfm.exec.setGameTime(7)
			ui.removeTextArea(750,nil)
		end
		if powerups == true then
			if data[name].powerup == 0 then
				if code == 49 and data[name].score >= 8 and data[name].level >= 1 then
					showMessage("<VP><b>"..name.."</b> "..text.p1.."")
					data[name].powerup=1
					setScores(name,-8,true)
					tfm.exec.playSound("/bouboum/x_bonus.mp3", 80)
				elseif code == 49 then
					showMessage("<R>"..text.p0.."",name)
				end
				if code == 50 and data[name].score >= 12 and data[name].level >= 2 then
					showMessage("<VP><b>"..name.."</b> "..text.p2.."")
					data[name].powerup=2
					setScores(name,-12,true)
					tfm.exec.playSound("/bouboum/x_bonus.mp3", 80)
				elseif code == 50 then
					showMessage("<R>"..text.p0.."",name)
				end
				if code == 51 and data[name].score >= 26 and data[name].level >= 3 then
					showMessage("<VP><b>"..name.."</b> "..text.p3.."")
					setScores(name,-26,true)
					data[name].powerup=3
					mode="wait3"
					tfm.exec.setGameTime(10)
					tfm.exec.playSound("/bouboum/x_bonus.mp3", 80)
				elseif code == 51 then
					showMessage("<R>"..text.p0.."",name)
				end
				if code == 52 and data[name].score >= 20 and data[name].level >= 3 then
					showMessage("<VP><b>"..name.."</b> "..text.p4.."")
					setScores(name,-20,true)
					data[name].powerup=4
					permafrost=true
					permaFrost()
					tfm.exec.playSound("/bouboum/gel.mp3", 75)
				elseif code == 52 then
					showMessage("<R>"..text.p0.."",name)
				end
				if code == 53 and data[name].score >= 15 and data[name].level >= 3 then
					showMessage("<VP><b>"..name.."</b> "..text.p5.."")
					setScores(name,-15,true)
					data[name].powerup=5
					night_mode=true
					nightMode()
					tfm.exec.playSound("/transformice/son/dash.mp3", 85)
				elseif code == 53 then
					showMessage("<R>"..text.p0.."",name)
				end
				if code == 54 and data[name].score >= 24 and data[name].level >= 3 then
					showMessage("<VP><b>"..name.."</b> "..text.p6.."")
					setScores(name,-24,true)
					data[name].powerup=6
					enabled=false
					mode="wait3"
					tfm.exec.setGameTime(10)
					anvilRain()
					tfm.exec.playSound("/deadmaze/combat/casse.mp3", 95)
				elseif code == 54 then
					showMessage("<R>"..text.p0.."",name)
				end
				if code == 55 and data[name].score >= 14 and data[name].level >= 4 then
					showMessage("<VP><b>"..name.."</b> "..text.p7.."")
					setScores(name,-14,true)
					data[name].powerup=7
					tfm.exec.setWorldGravity(0,22)
					pf_time=-2
					gravity=false
					tfm.exec.playSound("/bouboum/x_bonus.mp3", 80)
				elseif code == 55 then
					showMessage("<R>"..text.p0.."",name)
				end
				if code == 56 and data[name].score >= 15 and data[name].level >= 2 then
					showMessage("<VP><b>"..name.."</b> "..text.p8.."")
					setScores(name,-15,true)
					data[name].powerup=8
					tfm.exec.playSound("/bouboum/x_bonus.mp3", 80)
				elseif code == 56 then
					showMessage("<R>"..text.p0.."",name)
				end
				if code == 57 and data[name].score >= 10 and data[name].level >= 2 then
					showMessage("<VP><b>"..name.."</b> "..text.p9.."")
					setScores(name,-10,true)
					data[name].powerup=9
					tfm.exec.playSound("/bouboum/x_bonus.mp3", 80)
				elseif code == 57 then
					showMessage("<R>"..text.p0.."",name)
				end
				ui.removeTextArea(750,nil)
			end
		end
		if code == 90 then
			if data[name].power > 1 then
				data[name].power=data[name].power-1
			end
			showPowerMeter(name)
		end
		if code == 88 then
			if data[name].power < 20 then
				data[name].power=data[name].power+1
			end
			showPowerMeter(name)
		end
		if code == 67 then
			if data[name].angle > 0 then
				data[name].angle=data[name].angle-10
			end
			showAngleMeter(name)
		end
		if code == 86 then
			if data[name].angle < 90 then
				data[name].angle=data[name].angle+10
			end
			showAngleMeter(name)
		end
	end
	if code == 66 then
		eventChatCommand(name,"commands")
	end
	if code == 72 then
		eventChatCommand(name,"help")
	end
	if code == 82 then
		eventChatCommand(name,"ranking")
	end
	if code == 85 then
		eventChatCommand(name,"powerups")
	end
	if code == 80 then
		eventChatCommand(name,"p")
	end
end

function eventPlayerLeft(name)
	removeTeam(name)
	data[name].left=true
	mices=mices-1
end

function eventPlayerDied(name)
	if mode == "lobby" and data[name].ranking >= 0 then
		tfm.exec.respawnPlayer(name)
	end
	if mode == "wait2" and time_passed < 20 then
		if data[name] and data[name].team == 1 then
			tfm.exec.respawnPlayer(name)
			tfm.exec.movePlayer(name,600,195,false,0,0,false)
		end
		if data[name] and data[name].team == 2 then
			tfm.exec.respawnPlayer(name)
			tfm.exec.movePlayer(name,1000,195,false,0,0,false)
		end
	end
	if mode == "shoot" then
		if name == actual_player then
			data[name].current_coins=math.floor(data[name].current_coins/2)
			showMessage(""..text.suicide..""..actual_player)
			setScores(name,0,false)
			tfm.exec.setGameTime(6)
			if custom_mode == true and settings.anti_kami == true and data[actual_player].left == false then
				if data[actual_player].team == 1 then
					victoryBlue()
				elseif data[actual_player].team == 2 then
					victoryRed()
				end
			end
			mode="wait3"
		else
			if data[name] then data[name].lives=data[name].lives-1 end
			if data[name].lives <= 0 then
				if data[name].team > 0 then
					data[name].current_coins=math.floor(data[name].current_coins/2)
				end
				data[name].killeds=data[name].killeds+1
				setScores(name,0,false)
				if sudden_death == true then
					if data[name].team == 1 then
						victoryBlue()
					elseif data[name].team == 2 then
						victoryRed()
					end
				end
			elseif data[name].lives > 0 then
				tfm.exec.respawnPlayer(name)
				if data[name].team == 2 then
					tfm.exec.movePlayer(name,1000,205,false,0,0,false)
					data[name].killed=false
					showMessage(text.life1)
				end
				if data[name].team == 1 then
					tfm.exec.movePlayer(name,600,205,false,0,0,false)
					data[name].killed=false
					showMessage(text.life2)
				end
			end
		end
	end
	if mode == "wait3" then
		if data[name] then data[name].lives=data[name].lives-1 end
		if data[actual_player].team == data[name].team then
			if actual_player == name then
				data[actual_player].current_coins=0
				setScores(actual_player,0,false)
				showMessage(""..text.suicide..""..actual_player)
				if custom_mode == true and settings.anti_kami == true and data[actual_player].left == false then
					if data[actual_player].team == 1 then
						victoryBlue()
					elseif data[actual_player].team == 2 then
						victoryRed()
					end
				end
			else
				data[actual_player].current_coins=data[actual_player].current_coins-5
				setScores(actual_player,-5,true)
				showMessage("<VP>"..text.tk1.."<b>"..actual_player.."</b>"..text.tk2..""..name..".")
			end
		else
			if data[name].lives <= 0 then
				data[name].current_coins=math.floor(data[name].current_coins/3)
				setScores(name,math.floor(data[name].current_coins/2)*-1,true)
				data[name].killeds=data[name].killeds+1
				setScores(name,0,false)
			elseif data[name].lives > 0 then
				tfm.exec.respawnPlayer(name)
				if data[name].team == 2 then
					tfm.exec.movePlayer(name,1000,205,false,0,0,false)
					data[name].killed=false
					showMessage(text.life1)
					setScores(name,math.floor(data[name].current_coins/2)*-1,true)
				end
				if data[name].team == 1 then
					tfm.exec.movePlayer(name,600,205,false,0,0,false)
					data[name].killed=false
					showMessage(text.life2)
					setScores(name,math.floor(data[name].current_coins/2)*-1,true)
				end
			end
		end
		tfm.exec.playSound("/bouboum/x_mort.mp3", 77)
		if sudden_death == true then
			if data[name].team == 1 then
				victoryBlue()
			elseif data[name].team == 2 then
				victoryRed()
			end
		end
	end
end

function eventMouse(name,x,y)
	if actual_player == name and data[name].powerup == 3 and mode == "wait3" then
		if time_remain >= 2 then
			if data[name].team == 1 and x > 805 then
				tfm.exec.explosion(x,y,25,150,true)
				tfm.exec.displayParticle(12,x,y,0,0,0,0,nil)
			end
			if data[name].team == 2 and x < 795 then
				tfm.exec.explosion(x,y,25,150,true)
				tfm.exec.displayParticle(12,x,y,0,0,0,0,nil)
			end
			mode="wait2"
			tfm.exec.setGameTime(6)
		end
	end
end

function lobby()
	mode="lobby"; choose_time=30; powerups=false;
	tfm.exec.newGame(lobby_map)
	tfm.exec.setGameTime(36000)
	tfm.exec.setRoomMaxPlayers(old_limit)
	ui.removeTextArea(750,nil)
	players_red={};	players_blue={}; loop=0;
	for i=-8, -1 do
		ui.removeTextArea(i,nil)
	end
	for name,player in next,tfm.get.room.playerList do
		ui.removeTextArea(999,name)
		tfm.exec.freezePlayer(name,false)
		removeImagePlayers(name)
		showLobbyText(name)
		removeScoreboard(name)
		if data[name] then
			for i=1000,1011 do
				ui.removeTextArea(i,name)
			end
			data[name].opened=false
			if data[name].ranking >= 0 then
				showTeams(name)
				showImageBackground(name,"1835da9d15e.png",0,1,1.0,1.0)
				data[name].team=0
				data[name].current_coins=0
				setScores(name,0,false)
			else
				tfm.exec.killPlayer(name)
			end
		end
	end
	permafrost=false; night_mode=false;
	showMessage("<VP>"..text.legacy.."")
	if custom_mode == true then
		showMessage(text.custom)
	end
end

function eventNewGame()
	ui.setBackgroundColor("#000000")
	set_map="-1"; def_map=-1; turns=0;
	if mode == "wait1" then
		for i=400,403 do ui.removeTextArea(i,nil) end
		mode="wait2"
		tfm.exec.setGameTime(20)
		moveTeams()
		for name,player in next,tfm.get.room.playerList do
			data[name].scoreboard_id = tfm.exec.addImage("1835da984ec.png", ":1", 266, 15, name, 1.0, 1.0, 0, 1)
			tfm.exec.setNameColor(name,0xd7d7e6)
			data[name].score=0
			if data[name].team > 0 then
				data[name].matches=data[name].matches+1
			else
				tfm.exec.setPlayerScore(name,0,false)
			end
		end
	end
	actual_shooter="-"
end

function split(t,s)
	local a={}
	for i,v in string.gmatch(t,string.format("[^%s]+",s or "%s")) do
		table.insert(a,i)
	end
	return a
end

function eventChatCommand(name,command)
	local arg = split(command, " ")
	if arg[1] == "p" then
		if arg[2] then
			nome = arg[2]:lower():gsub('%a', string.upper, 1)
		else
			nome = name
		end
		if tfm.get.room.playerList[nome] and data[nome].opened == false then
			showMenu(name,0x518394,250,120,300,225,nome,"<b>Level: "..data[nome].level.."</b><br><br>Experience: "..data[nome].exp.."/"..data[nome].maxp.."<br><br><br>Kills: "..data[nome].kills.."<br>Matches: "..data[nome].matches.."<br>Wins: "..data[nome].wins.."<br><br>Victory Rate: "..data[nome].winrate.."%<br>Kill Rate: "..data[nome].eff.."%")
			ui.addTextArea(1006,"",name,265,215,270,10,0x101010,0x161903,1.0,true)
			ui.addTextArea(1005,"",name,265,215,((data[nome].exp/data[nome].maxp)*260)+10,10,0x95a810,0x658704,1.0,true)
			showMessage("<R>"..text.rankw.."",name)
		else
			showMessage("<R>User not found",nome)
		end
	end

	if (command:sub(0,4) == "sync") then if data[name].ranking >= 3 then
		tfm.exec.setPlayerSync(command:sub(6))
		showMessage("Sync: "..command:sub(6).."",name)
	else showMessage(text.wrong,name) end end
	if command == "reset" and time_passed >= 6 then if data[name].ranking >= 2 then
		lobby()
	else showMessage(text.wrong,name) end end
	if command == "settings" then if data[name].ranking >= 2 then
		if mode == "lobby" then
			showRoomSettings(name)
			mode="define";
			showMessage(text.defining)
		else
			showMessage(text.load0,name)
		end
	else showMessage(text.wrong,name) end end
	if (command:sub(0,2) == "pw") then if data[name].ranking >= 2 then
		tfm.exec.setRoomPassword(tostring(command:sub(4)))
		if string.len(command:sub(4)) > 0 then
			showMessage(""..text.pw..""..command:sub(4).."",name)
		else
			showMessage(text.pw0,name)
		end
	else showMessage(text.wrong,name) end end
	if (command:sub(0,2) == "lc") then if data[name].ranking >= 2 then
		if tostring(command:sub(4)) == "0" or tostring(command:sub(4)) == "1" or tostring(command:sub(4)) == "2" or tostring(command:sub(4)) == "3" then
			level=tonumber(command:sub(4))
			if level == 0 then
				ping_check=0
				showMessage("The player's latency checker is now disabled.")
			elseif level == 1 then
				ping_check=1
				showMessage("The player's latency checker is now set to WEAK. Players with average latency greater than 2000 ms cannot enter into the teams.")
			elseif level == 2 then
				ping_check=2
				showMessage("The player's latency checker is now set to DEFAULT. Players with average latency greater than 1000 ms cannot enter into the teams.")
			elseif level == 3 then
				ping_check=3
				showMessage("The player's latency checker is now set to STRICT. Players with average latency greater than 500 ms cannot enter into the teams.")
			end
		end
	else showMessage(text.wrong,name) end end
	if command == "changelog" then
		showMenu(name,0xa8f233,140,130,520,105,"#anvilwar Changelog - RTM 53336.219 LTS","• The room managers commands are enabled again")
	end
	if (command:sub(0,2) == "rv") then
		if name == actual_player and general_time >= 25 then
			if name == red_cap or name == blue_cap then
				temp_name=command:sub(4)
				print(temp_name)
				if data[temp_name] then
					if data[name].score >= 25 then
						if tfm.get.room.playerList[temp_name].isDead == true then
							tfm.exec.respawnPlayer(temp_name)
							if data[temp_name].team == 2 then
								tfm.exec.movePlayer(temp_name,1000,205,false,0,0,false)
								data[temp_name].killed=false
							end
							if data[temp_name].team == 1 then
								tfm.exec.movePlayer(temp_name,600,205,false,0,0,false)
								data[temp_name].killed=false
							end
							showMessage("<J>"..text.revived..""..temp_name.."")
							setScores(name,-25,true)
						end
					else
						showMessage(text.p10,name)
					end
				end
			end
		end
	end
	if (command:sub(0,2) == "tp") then
		if name == actual_player then
			if name == red_cap or name == blue_cap then
				temp_name=command:sub(4)
				if data[temp_name] then
					ui.addPopup(100,2,"Points",name,350,175,200,true)
				end
			end
		end
	end
	if (command:sub(0,5) == "limit") then if data[name].ranking >= 3 then
		old_limit=tonumber(command:sub(7))
		tfm.exec.setRoomMaxPlayers(old_limit)
		showMessage(""..text.limit..""..old_limit.."",name)
	else showMessage(text.wrong,name) end end
	if (command:sub(0,5) == "score") then if data[name].ranking >= 3 then
		temp_name=command:sub(7)
		if data[temp_name] then
			ui.addPopup(105,2,"Points",name,350,175,200,true)
		end
	else showMessage(text.wrong,name) end end
	if (command:sub(0,3) == "set") then if data[name].ranking >= 3 then
		if data[command:sub(5)] then
			set_player=command:sub(5)
		end
	else showMessage(text.wrong,name) end end
 	if (command:sub(0,6) == "defmap") then if data[name].ranking >= 2 then
		if mode == "lobby" then
			def_map=tonumber(command:sub(8))
			showMessage("Defined map: "..def_map.."",name)
		end
	else showMessage(text.wrong,name) end end
	if (command:sub(0,4) == "kill") then if data[name].ranking >= 3 then
		tfm.exec.killPlayer(command:sub(6))
	else showMessage(text.wrong,name) end end
	if (command:sub(0,7) == "testmap") then
		showMessage(text.tmaperror,name)
	end
	if (command:sub(0,3) == "get") then
		if tonumber(command:sub(5)) <= rawlen(map_names) then
			showMessage(""..map_names[tonumber(command:sub(5))].." - "..maps[tonumber(command:sub(5))].."",name)
		end
	end
	if (command:sub(0,2) == "tc") or (command:sub(0,2) == "TC") or (command:sub(0,2) == "Tc") or (command:sub(0,2) == "tC") then
		if data[name] then
			if data[name].team == 1 then
				for _,p in next,players_red do
					showMessage("<VP>• <b>["..name.."]</b> "..command:sub(4).."",p)
				end
			elseif data[name].team == 2 then
				for _,p in next,players_blue do
					showMessage("<VP>• <b>["..name.."]</b> "..command:sub(4).."",p)
				end
			end
		end
	end
	if command == "ranking" then
		if data[name].opened == false then
			eventRanking(name)
		end
		showMessage("<R>"..text.rankw.."",name)
	end
	if command == "anvils" then
		if data[name].opened == false then
			showMessage("<J>"..text.ac.."<b>"..data[name].coins.."</b> AnvilCoins.",name)
			showMenu(name,0x999999,56,120,690,235,"#anvilwar Anvils","<font size='11.5'>"..divider.."<b>Default Anvil</b><br>"..divider.."Cost: 0 coins<br>"..divider.."<a href='event:a0'>Equip!</a><br><br>"..divider.."<b>Red Anvil</b><br>"..divider.."Cost: 100 coins<br>"..divider.."<a href='event:a1'>Equip!</a><br><br>"..divider.."<b>Blue Anvil</b><br>"..divider.."Cost: 100 coins<br>"..divider.."<a href='event:a2'>Equip!</a><br><br>"..divider.."<b>White Anvil</b><br>"..divider.."Cost: 200 coins<br>"..divider.."<a href='event:a3'>Equip!</a>")
			ui.addTextArea(1005,"<i><font size='11.5'>"..divider.."<b>Rainbow Anvil</b><br>"..divider.."Cost: 250 coins<br>"..divider.."<a href='event:a4'>Equip!</a><br><br>"..divider.."<b>Sharingan Anvil</b><br>"..divider.."Cost: 500 coins<br>"..divider.."<a href='event:a5'>Equip!</a><br><br>"..divider.."<b>Black Hole Anvil</b><br>"..divider.."Cost: 500 coins<br>"..divider.."<a href='event:a6'>Equip!</a><br><br>"..divider.."<b>4K 1080p Anvil</b><br>"..divider.."Cost: 200 coins<br>"..divider.."<a href='event:a7'>Equip!</a>",name,208,151,175,215,0,0,1.0,true)
			ui.addTextArea(1006,"<i><font size='11.5'>"..divider.."<b>Thug Life Anvil</b><br>"..divider.."Cost: 300 coins<br>"..divider.."<a href='event:a8'>Equip!</a><br><br>"..divider.."<b>Water Anvil</b><br>"..divider.."Cost: 300 coins<br>"..divider.."<a href='event:a9'>Equip!</a><br><br>"..divider.."<b>Grass Anvil</b><br>"..divider.."Cost: 300 coins<br>"..divider.."<a href='event:a10'>Equip!</a><br><br>"..divider.."<b>RadWhite Anvil</b><br>"..divider.."Cost: 350 coins<br>"..divider.."<a href='event:a11'>Equip!</a>",name,380,151,175,215,0,0,1.0,true)
			ui.addTextArea(1007,"<i><font size='11.5'>"..divider.."<b>Stars Anvil</b><br>"..divider.."Cost: 400 coins<br>"..divider.."<a href='event:a12'>Equip!</a><br><br>"..divider.."<b>Asteroid Anvil</b><br>"..divider.."Cost: 350 coins<br>"..divider.."<a href='event:a13'>Equip!</a><br><br>"..divider.."<b>Expanded Anvil</b><br>"..divider.."Cost: 125 coins<br>"..divider.."<a href='event:a14'>Equip!</a><br><br>"..divider.."<b>Yellow Anvil</b><br>"..divider.."Cost: 100 coins<br>"..divider.."<a href='event:a15'>Equip!</a>",name,552,151,175,215,0,0,1.0,true)
			showAvailableAnvils(name)
		end
	end
	if command == "powerups" then
		showMenu(name,0xc23517,140,90,520,260,"#anvilwar Powerups",text.powerups)
	end
	if command == "sound" then
		showMessage(text.sound,name)
	end
	if command == "leader" then
		showMenu(name,0x873469,140,90,520,215,"#anvilwar Team Leader Funcions",text.leader)
	end
	if command == "commands" then
		showMenu(name,0x125490,120,130,560,155,"#anvilwar Commands",text.commands)
	end
	if command == "adcommands" then
		if data[name].ranking >= 1 then
			showMenu(name,0x125490,120,130,560,122,"#anvilwar Commands",text.adcommands)
		else
			showMessage(text.wrong,name)
		end
	end
	if command == "help" then
		showMenu(name,0x457426,100,125,600,260,"Help",text.help)
	end
end
function eventPopupAnswer(id,name,message)
	if id == 100 then
		if data[temp_name] and actual_player == name then
			local sp=tonumber(message)
			if sp <= data[name].score then
				setScores(name,sp*-1,true)
				setScores(temp_name,sp,true)
			end
		end
	end
	if id == 105 then
		if data[temp_name] then
			setScores(temp_name,tonumber(message),true)
		end
	end
	if id == 1000 then
		if message == "0" then
			settings.map_mode=0
			showRoomSettings(name)
		elseif message == "1" then
			ui.addPopup(2001,2,"Insert the map @code",name,350,175,200,true)
		end
	end
	if id == 2001 then
		if string.len(message) == 8 then
			settings.map_mode=1
			settings.map_select=message
		end
		showRoomSettings(name)
	end
end
function enterRedTeam(name)
	if custom_mode == false then limit=13 else limit=settings.plimit; end
	
	if choose_time > 1 and data[name].team == 0 and rawlen(players_red) < limit then
		if settings.bg_switch == true and custom_mode == true then
			if tfm.get.room.playerList[name].gender == 1 then
				tfm.exec.respawnPlayer(name)
				table.insert(players_red,name)
				updatePlayerList()
				tfm.exec.movePlayer(name,200,280,false,0,0,false)
				data[name].team=1
				for i=479,481 do
					ui.removeTextArea(i,name)
					ui.addTextArea(482,"<font size='16'><font color='#ffffff'><p align='center'><b><a href='event:quit'>"..text.leave.."",name,320,250,150,25,0,0,0.9,true)
				end
			else
				showMessage(text.errorbg1,name)
			end
		else
			tfm.exec.respawnPlayer(name)
			table.insert(players_red,name)
			updatePlayerList()
			tfm.exec.movePlayer(name,200,280,false,0,0,false)
			data[name].team=1
			for i=479,481 do
				ui.removeTextArea(i,name)
				ui.addTextArea(482,"<font size='16'><font color='#ffffff'><p align='center'><b><a href='event:quit'>"..text.leave.."",name,320,250,150,25,0,0,0.9,true)
			end
		end
	end
end

function enterBlueTeam(name)
	if custom_mode == false then limit=13 else limit=settings.plimit; end

	if choose_time > 1 and data[name].team == 0 and rawlen(players_blue) < limit then
		if settings.bg_switch == true and custom_mode == true then
			if tfm.get.room.playerList[name].gender == 2 then
				tfm.exec.respawnPlayer(name)
				table.insert(players_blue,name)
				updatePlayerList()
				data[name].team=2
				tfm.exec.movePlayer(name,600,280,false,0,0,false)
				for i=479,481 do
					ui.removeTextArea(i,name)
					ui.addTextArea(482,"<font size='16'><font color='#ffffff'><p align='center'><b><a href='event:quit'>"..text.leave.."",name,320,250,150,25,0,0,0.9,true)
				end
			else
				showMessage(text.errorbg2,name)
			end
		else
			tfm.exec.respawnPlayer(name)
			table.insert(players_blue,name)
			updatePlayerList()
			data[name].team=2
			tfm.exec.movePlayer(name,600,280,false,0,0,false)
			for i=479,481 do
				ui.removeTextArea(i,name)
				ui.addTextArea(482,"<font size='16'><font color='#ffffff'><p align='center'><b><a href='event:quit'>"..text.leave.."",name,320,250,150,25,0,0,0.9,true)
			end
		end
	end
end

function moveTeams()
	ui.setBackgroundColor("#6a7495")
	if custom_mode == true and settings.anti_kami == true then
		showMessage("<VP>"..text.getr.."<br>"..text.kami.."")
	else
		showMessage("<VP>"..text.getr.."")
	end
	for _,id in next,images_id do
		tfm.exec.removeImage(id)
		images_id={}
	end
	if mode == "wait2" then
		for _,name in next,players_red do
			tfm.exec.respawnPlayer(name)
			tfm.exec.movePlayer(name,600,198,false,0,0,false)
		end
		for _,name in next,players_blue do
			tfm.exec.respawnPlayer(name)
			tfm.exec.movePlayer(name,1000,198,false,0,0,false)
		end
		for name,player in next,tfm.get.room.playerList do
			if data[name] and data[name].team == 0 then
				tfm.exec.killPlayer(name)
			end
		end
	end
end

function removeTeam(name)
	length1=rawlen(players_red)
	length2=rawlen(players_blue)
	tfm.exec.killPlayer(name)
	for i=1,length1 do
		if players_red[i] == name then
			table.remove(players_red,i)
			updatePlayerList()
			showTeams(name)
			data[name].team=0
			ui.removeTextArea(482,name); break
		end
	end
	for i=1,length2 do
		if players_blue[i] == name then
			table.remove(players_blue,i)
			updatePlayerList()
			showTeams(name)
			data[name].team=0
			ui.removeTextArea(482,name); break
		end
	end
end

function eventTextAreaCallback(id,name,callback)
	if callback == "enter_red" then
		if checkPing(name) == false then
			enterRedTeam(name)
		else
			showMessage(text.latency,name)
		end
	end
	if callback == "enter_blue" then
		if checkPing(name) == false then
			enterBlueTeam(name)
		else
			showMessage(text.latency,name)
		end
	end
	if callback == "quit" then
		removeTeam(name)
	end
	if callback == "close" then
		for _,i in next,{1000,1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011} do
			ui.removeTextArea(i,name)
		end
		data[name].opened=false
		removeImagePlayers(name)
		if mode == "lobby" or mode == "map_sort" then
			updatePlayerList()
		end
		if mode == "define" then
			lobby()
		end
	end
	if callback == "pw1" then
		data[name].opened=false
		eventChatCommand(name,"powerups")
	end
	if callback == "pw2" then
		data[name].opened=false
		showMenu(name,0xc23517,140,60,520,305,"#anvilwar Powerups",text.powerups2)
	end
	if callback == "a0" then
		data[name].current_anvil=0
		showMessage(""..text.using.."<N><b>Default Anvil!</b>",name)
	end
	if callback == "a1" then
		if data[name].anvils[1] == 1 then
			data[name].current_anvil=1
			showMessage(""..text.using.."<N><b>Red Anvil!</b>",name)
		else
			if data[name].coins >= 100 then
				data[name].coins=data[name].coins-100
				data[name].anvils[1]=1
				data[name].current_anvil=1
				showMessage(""..text.using.."<N><b>Red Anvil!</b>",name)
			else
				showMessage("<R>"..text.ac0.."",name)
			end
		end
	end
	if callback == "a2" then
		if data[name].anvils[2] == 1 then
			data[name].current_anvil=2
			showMessage(""..text.using.."<N><b>Blue Anvil!</b>",name)
		else
			if data[name].coins >= 100 then
				data[name].coins=data[name].coins-100
				data[name].anvils[2]=1
				data[name].current_anvil=2
				showMessage(""..text.using.."<N><b>Blue Anvil!</b>",name)
			else
				showMessage("<R>"..text.ac0.."",name)
			end
		end
	end
	if callback == "a3" then
		if data[name].anvils[3] == 1 then
			data[name].current_anvil=3
			showMessage(""..text.using.."<N><b>White Anvil!</b>",name)
		else
			if data[name].coins >= 200 then
				data[name].coins=data[name].coins-200
				data[name].anvils[3]=1
				data[name].current_anvil=3
				showMessage(""..text.using.."<N><b>White Anvil!</b>",name)
			else
				showMessage("<R>"..text.ac0.."",name)
			end
		end
	end
	if callback == "a4" then
		if data[name].anvils[4] == 1 then
			data[name].current_anvil=4
			showMessage(""..text.using.."<N><b>Rainbow Anvil!</b>",name)
		else
			if data[name].coins >= 250 then
				data[name].coins=data[name].coins-250
				data[name].anvils[4]=1
				data[name].current_anvil=4
				showMessage(""..text.using.."<N><b>Rainbow Anvil!</b>",name)
			else
				showMessage("<R>"..text.ac0.."",name)
			end
		end
	end
	if callback == "a5" then
		if data[name].anvils[5] == 1 then
			data[name].current_anvil=5
			showMessage(""..text.using.."<N><b>Sharingan Anvil!</b>",name)
		else
			if data[name].coins >= 500 then
				data[name].coins=data[name].coins-500
				data[name].anvils[5]=1
				data[name].current_anvil=5
				showMessage(""..text.using.."<N><b>Sharingan Anvil!</b>",name)
			else
				showMessage("<R>"..text.ac0.."",name)
			end
		end
	end
	if callback == "a6" then
		if data[name].anvils[6] == 1 then
			data[name].current_anvil=6
			showMessage(""..text.using.."<N><b>Black Hole Anvil!</b>",name)
		else
			if data[name].coins >= 500 then
				data[name].coins=data[name].coins-500
				data[name].anvils[6]=1
				data[name].current_anvil=6
				showMessage(""..text.using.."<N><b>Black Hole Anvil!</b>",name)
			else
				showMessage("<R>"..text.ac0.."",name)
			end
		end
	end
	if callback == "a7" then
		if data[name].anvils[7] == 1 then
			data[name].current_anvil=7
			showMessage(""..text.using.."<N><b>4K 1080p Anvil!</b>",name)
		else
			if data[name].coins >= 200 then
				data[name].coins=data[name].coins-200
				data[name].anvils[7]=1
				data[name].current_anvil=7
				showMessage(""..text.using.."<N><b>4K 1080p Anvil!</b>",name)
			else
				showMessage("<R>"..text.ac0.."",name)
			end
		end
	end
	if callback == "a8" then
		if data[name].anvils[8] == 1 then
			data[name].current_anvil=8
			showMessage(""..text.using.."<N><b>Thug Life Anvil!</b>",name)
		else
			if data[name].coins >= 300 then
				data[name].coins=data[name].coins-300
				data[name].anvils[8]=1
				data[name].current_anvil=8
				showMessage(""..text.using.."<N><b>Thug Life Anvil!</b>",name)
			else
				showMessage("<R>"..text.ac0.."",name)
			end
		end
	end
	if callback == "a9" then
		if data[name].anvils[9] == 1 then
			data[name].current_anvil=9
			showMessage(""..text.using.."<N><b>Water Anvil!</b>",name)
		else
			if data[name].coins >= 300 then
				data[name].coins=data[name].coins-300
				data[name].anvils[9]=1
				data[name].current_anvil=9
				showMessage(""..text.using.."<N><b>Water Anvil!</b>",name)
			else
				showMessage("<R>"..text.ac0.."",name)
			end
		end
	end
	if callback == "a10" then
		if data[name].anvils[10] == 1 then
			data[name].current_anvil=10
			showMessage(""..text.using.."<N><b>Grass Anvil!</b>",name)
		else
			if data[name].coins >= 300 then
				data[name].coins=data[name].coins-300
				data[name].anvils[10]=1
				data[name].current_anvil=10
				showMessage(""..text.using.."<N><b>Grass Anvil!</b>",name)
			else
				showMessage("<R>"..text.ac0.."",name)
			end
		end
	end
	if callback == "a11" then
		if data[name].anvils[11] == 1 then
			data[name].current_anvil=11
			showMessage(""..text.using.."<N><b>RadWhite Anvil!</b>",name)
		else
			if data[name].coins >= 350 then
				data[name].coins=data[name].coins-350
				data[name].anvils[11]=1
				data[name].current_anvil=11
				showMessage(""..text.using.."<N><b>RadWhite Anvil!</b>",name)
			else
				showMessage("<R>"..text.ac0.."",name)
			end
		end
	end
	if callback == "a12" then
		if data[name].anvils[12] == 1 then
			data[name].current_anvil=12
			showMessage(""..text.using.."<N><b>Stars Anvil!</b>",name)
		else
			if data[name].coins >= 400 then
				data[name].coins=data[name].coins-400
				data[name].anvils[12]=1
				data[name].current_anvil=12
				showMessage(""..text.using.."<N><b>Stars Anvil!</b>",name)
			else
				showMessage("<R>"..text.ac0.."",name)
			end
		end
	end
	if callback == "a13" then
		if data[name].anvils[13] == 1 then
			data[name].current_anvil=13
			showMessage(""..text.using.."<N><b>Asteroid Anvil!</b>",name)
		else
			if data[name].coins >= 350 then
				data[name].coins=data[name].coins-350
				data[name].anvils[13]=1
				data[name].current_anvil=13
				showMessage(""..text.using.."<N><b>Asteroid Anvil!</b>",name)
			else
				showMessage("<R>"..text.ac0.."",name)
			end
		end
	end
	if callback == "a14" then
		if data[name].anvils[14] == 1 then
			data[name].current_anvil=14
			showMessage(""..text.using.."<N><b>Expanded Anvil!</b>",name)
		else
			if data[name].coins >= 125 then
				data[name].coins=data[name].coins-125
				data[name].anvils[14]=1
				data[name].current_anvil=14
				showMessage(""..text.using.."<N><b>Expanded Anvil!</b>",name)
			else
				showMessage("<R>"..text.ac0.."",name)
			end
		end
	end
	if callback == "a15" then
		if data[name].anvils[15] == 1 then
			data[name].current_anvil=15
			showMessage(""..text.using.."<N><b>Yellow Anvil!</b>",name)
		else
			if data[name].coins >= 100 then
				data[name].coins=data[name].coins-100
				data[name].anvils[15]=1
				data[name].current_anvil=15
				showMessage(""..text.using.."<N><b>Yellow Anvil!</b>",name)
			else
				showMessage("<R>"..text.ac0.."",name)
			end
		end
	end
	if callback == "cmode" then
		if custom_mode == false then custom_mode=true else custom_mode=false; end
		showRoomSettings(name)
	end
	if callback == "ctimea" then
		if settings.time > 120 then settings.time=settings.time-10 end
		showRoomSettings(name)
	end
	if callback == "ctimeb" then
		if settings.time < 600 then settings.time=settings.time+10 end
		showRoomSettings(name)
	end
	if callback == "cplayersa" then
		if settings.plimit > 1 then settings.plimit=settings.plimit-1 end
		showRoomSettings(name)
	end
	if callback == "cplayersb" then
		if settings.plimit < 16 then settings.plimit=settings.plimit+1 end
		showRoomSettings(name)
	end
	if callback == "cmap" then
		ui.addPopup(1000,2,"Insert the map mode:<br><br>0 = Normal<br>1 = @code based",name,350,175,200,true)
	end
	if callback == "cpowerups" then
		if settings.g_powerups == false then settings.g_powerups=true else settings.g_powerups=false end
		showRoomSettings(name)
	end
	if callback == "cstimea" then
		if settings.shoot_time > 8 then settings.shoot_time=settings.shoot_time-1 end
		showRoomSettings(name)
	end
	if callback == "cstimeb" then
		if settings.shoot_time < 24 then settings.shoot_time=settings.shoot_time+1 end
		showRoomSettings(name)
	end
	if callback == "ckami" then
		if settings.anti_kami == false then settings.anti_kami=true else settings.anti_kami=false end
		showRoomSettings(name)
	end
	if callback == "csd" then
		if settings.sd_switch == false then settings.sd_switch=true else settings.sd_switch=false end
		showRoomSettings(name)
	end
	if callback == "bgd" then
		if settings.bg_switch == false then settings.bg_switch=true else settings.bg_switch=false end
		showRoomSettings(name)
	end
end

function advanceLevel(name)
	data[name].level=data[name].level+1
	data[name].exp=data[name].exp-data[name].maxp
	data[name].maxp=data[name].maxp+50
	showMessage("<VP><b>"..name.."</b> "..text.level.."<b>"..data[name].level.."</b>!",name)
end

function drawMatch()
	mode="end"
	sudden_death=false
	tfm.exec.setGameTime(math.random(5,15))
	showMessage("<J>"..text.draw.."")
	for _,name in next,players_red do
		calculatePoints(name)
	end
	for _,name in next,players_blue do
		calculatePoints(name)
	end
	ui.removeTextArea(750,nil)
	for name,_ in next,tfm.get.room.playerList do
		if data[name] then
			removeScoreboard(name)
		end
	end
end

function victoryBlue()
	mode="end"
	sudden_death=false
	for _,name in next,players_blue do
		data[name].current_coins=data[name].current_coins+20
		tfm.exec.respawnPlayer(name)
		tfm.exec.movePlayer(name,math.random(900,1200),198,false,0,0,false)
		tfm.exec.playEmote(name,0)
		data[name].wins=data[name].wins+1
	end
	tfm.exec.setGameTime(math.random(5,20))
	showMessage("<BL>"..text.winblue.."")
	for _,name in next,players_red do
		calculatePoints(name)
		tfm.exec.playEmote(name,2)
		tfm.exec.playSound("/fortoresse/x_defaite.mp3",63,nil,nil,name)
	end
	for _,name in next,players_blue do
		calculatePoints(name)
		tfm.exec.playSound("/fortoresse/x_victoire.mp3",78,nil,nil,name)
	end
	ui.removeTextArea(750,nil)
	for name,_ in next,tfm.get.room.playerList do
		if data[name] then
			removeScoreboard(name)
		end
	end
end

function victoryRed()
	mode="end"
	sudden_death=false
	for _,name in next,players_red do
		data[name].current_coins=data[name].current_coins+20
		tfm.exec.respawnPlayer(name)
		tfm.exec.movePlayer(name,math.random(400,700),198,false,0,0,false)
		tfm.exec.playEmote(name,0)
		data[name].wins=data[name].wins+1
	end
	tfm.exec.setGameTime(math.random(5,20))
	showMessage("<R>"..text.winred.."")
	for _,name in next,players_red do
		calculatePoints(name)
		tfm.exec.playSound("/fortoresse/x_victoire.mp3",78,nil,nil,name)
	end
	for _,name in next,players_blue do
		calculatePoints(name)
		tfm.exec.playEmote(name,2)
		tfm.exec.playSound("/fortoresse/x_defaite.mp3",63,nil,nil,name)
	end
	ui.removeTextArea(750,nil)
	for name,_ in next,tfm.get.room.playerList do
		if data[name] then
			removeScoreboard(name)
		end
	end
end

function setShooter()
	if set_player == "" then
		if turn == 0 then
			turn=1
			actual_player=alives_blue[math.random(#alives_blue)]
			if custom_mode == false then
				tfm.exec.setGameTime(15)
				if actual_player == blue_cap then
					tfm.exec.setGameTime(22)
				end
			else
				tfm.exec.setGameTime(settings.shoot_time)
				if actual_player == blue_cap then
					tfm.exec.setGameTime(math.floor(settings.shoot_time*1.2))
				end
			end
		elseif turn == 1 then
			turn=0
			actual_player=alives_red[math.random(#alives_red)]
			if custom_mode == false then
				tfm.exec.setGameTime(15)
				if actual_player == red_cap then
					tfm.exec.setGameTime(18)
				end
			else
				tfm.exec.setGameTime(settings.shoot_time)
				if actual_player == red_cap then
					tfm.exec.setGameTime(math.floor(settings.shoot_time*1.2))
				end
			end
		end
	else
		if turn == 0 then
			turn=1
		elseif turn == 1 then
			turn=0
		end
		actual_player=set_player
		tfm.exec.setGameTime(15)
	end
	set_player=""
	tfm.exec.addShamanObject(0, tfm.get.room.playerList[actual_player].x, tfm.get.room.playerList[actual_player].y-55, 0, 0, 0, false)
	ui.addTextArea(750,"<i><font size='15'><p align='center'>"..text.as.." <b>"..actual_player.."</b>",nil,110,352,580,22,0x010101,0x323232,0.6,true)
	showMessage("<VP>"..text.as1..""..data[actual_player].score.."",actual_player)
	tfm.exec.playSound("/tfmadv/xp.mp3",100,nil,nil,actual_player)
	enabled=true
	mode="shoot"
end

function getAlivePlayers()
	tfm.exec.setWorldGravity(0,10)
	current_red=rawlen(alives_red); current_blue=rawlen(alives_blue); pf_time=0;
	alives_red={}
	alives_blue={}
	turns=turns+1
	for _,name in next,players_red do
		data[name].powerup=0
		if tfm.get.room.playerList[name].isDead == false then
			data[name].killed=false
			table.insert(alives_red,name)
		else
			data[name].killed=true
			setScores(name,0,false)
		end
	end
	for _,name in next,players_blue do
		data[name].powerup=0
		if tfm.get.room.playerList[name].isDead == false then
			data[name].killed=false
			table.insert(alives_blue,name)
		else
			data[name].killed=true
			setScores(name,0,false)
		end
	end
	if mode == "wait3" then
		if data[actual_player].team == 1 then
			killsc=current_blue-rawlen(alives_blue)
			data[actual_player].kills=data[actual_player].kills+killsc
			data[actual_player].current_coins=data[actual_player].current_coins+2*killsc
			setScores(actual_player,killsc*3,true)
			if actual_player == red_cap or actual_player == blue_cap then
				setScores(actual_player,killsc*2,true)
			end
			if data[actual_player].multikills < killsc then
				data[actual_player].multikills=killsc
			end
			if killsc == 2 then
				showMessage("<J>Double Kill of <b>"..actual_player.."</b>!")
			elseif killsc >= 3 then
				showMessage("<J>Multi Kill! "..killsc.." kills of <b>"..actual_player.."</b>!")
			end
		elseif data[actual_player].team == 2 then
			killsc=current_red-rawlen(alives_red)
			data[actual_player].kills=data[actual_player].kills+killsc
			data[actual_player].current_coins=data[actual_player].current_coins+2*killsc
			setScores(actual_player,killsc*3,true)
			if actual_player == red_cap or actual_player == blue_cap then
				setScores(actual_player,killsc*2,true)
			end
			if data[actual_player].multikills < killsc then
				data[actual_player].multikills=killsc
			end
			if killsc == 2 then
				showMessage("<J>Double Kill of <b>"..actual_player.."</b>!")
			elseif killsc >= 3 then
				showMessage("<J>Multi Kill! "..killsc.." kills of <b>"..actual_player.."</b>!")
			end
		end
	end
	detectVictory()
end

function eventLoop(passed,remain)
	time_passed=math.floor(passed/1000)
	time_remain=math.floor(remain/1000)
	updateTextBar()
	for name,player in next,tfm.get.room.playerList do
		if data[name] and data[name].test_time > 0 then
			data[name].test_time=data[name].test_time-0.5
		end
	end
	if mode == "lobby" then
		if choose_time > 0 then
			choose_time=choose_time-0.5
			for name,player in next,tfm.get.room.playerList do
				if data[name] and data[name].opened == false then
					ui.addTextArea(483,"<font size='55'><p align='center'><font color='#000001'>"..math.ceil(choose_time).."",name,357,162,80,60,0,0,0.97,true)
					ui.addTextArea(484,"<font size='55'><p align='center'>"..math.ceil(choose_time).."",name,355,160,80,60,0,0,0.97,true)
				end
			end
		end
		if choose_time == 0 then
			if rawlen(players_red) > 0 and rawlen(players_blue) > 0 then
				if rawlen(players_red) - rawlen(players_blue) <= 1 and rawlen(players_red) - rawlen(players_blue) >= -1 then
					for i=478,484 do ui.removeTextArea(i,nil) end
					mode="map_sort"
				else
					choose_time=15
				end
			else
				choose_time=30
			end
		end
	end
	if mode == "map_sort" then
		if custom_mode == false then
			if loop < 12 then
				loop=loop+1
				ui.addTextArea(-6,"<font face='Arial'><p align='center'><font color='#000000'><font size='24'><i>"..text.rm.."",nil,102,97,600,45,0,0,1.0,true)
				ui.addTextArea(-5,"<font face='Arial'><p align='center'><font size='24'><i>"..text.rm.."",nil,100,95,600,45,0,0,1.0,true)
				map_id=math.random(1,rawlen(maps))
				tfm.exec.playSound("/bouboum/x_pose_bombe.mp3",65)
			elseif loop == 12 then
				if def_map > 0 then
					map_id=def_map
				end
				current_map=maps[map_id]
				ui.addTextArea(-6,"<font face='Arial'><p align='center'><font color='#000000'><font size='24'><i>"..text.rm1..""..map_names[map_id].." - "..maps[map_id].."",nil,2,97,800,45,0,0,1.0,true)
				ui.addTextArea(-5,"<font face='Arial'><p align='center'><font size='24'><VP><i>"..text.rm1..""..map_names[map_id].." - "..maps[map_id].."",nil,0,95,800,45,0,0,1.0,true)
				mode="wait1"
				tfm.exec.setGameTime(10)
				tfm.exec.playSound("/bouboum/x_bonus_alea.mp3",75)
			end
		else
			if settings.map_mode == 0 then
				if loop < 12 then
					loop=loop+1
					ui.addTextArea(-6,"<font face='Arial'><p align='center'><font color='#000000'><font size='24'><i>"..text.rm.."",nil,102,97,600,45,0,0,1.0,true)
					ui.addTextArea(-5,"<font face='Arial'><p align='center'><font size='24'><i>"..text.rm.."",nil,100,95,600,45,0,0,1.0,true)
					map_id=math.random(1,rawlen(maps))
					tfm.exec.playSound("/bouboum/x_pose_bombe.mp3",65)
				elseif loop == 12 then
					if def_map > 0 then
						map_id=def_map
					end
					current_map=maps[map_id]
					ui.addTextArea(-6,"<font face='Arial'><p align='center'><font color='#000000'><font size='24'><i>"..text.rm1..""..map_names[map_id].." - "..maps[map_id].."",nil,2,97,800,45,0,0,1.0,true)
					ui.addTextArea(-5,"<font face='Arial'><p align='center'><font size='24'><VP><i>"..text.rm1..""..map_names[map_id].." - "..maps[map_id].."",nil,0,95,800,45,0,0,1.0,true)
					mode="wait1"
					tfm.exec.setGameTime(10)
					tfm.exec.playSound("/bouboum/x_bonus_alea.mp3",75)
				end
			elseif settings.map_mode == 1 then
				current_map=settings.map_select
				ui.addTextArea(-6,"<font face='Arial'><p align='center'><font color='#000000'><font size='24'><i>"..text.rm1..""..settings.map_select.."",nil,2,95,800,45,0,0,1.0,true)
				ui.addTextArea(-5,"<font face='Arial'><p align='center'><font size='24'><VP><i>"..text.rm1..""..settings.map_select.."",nil,0,95,800,45,0,0,1.0,true)
				mode="wait1"
				tfm.exec.setGameTime(10)
				tfm.exec.playSound("/bouboum/x_bonus_alea.mp3",75)
			end
		end
		if rawlen(players_red) == 0 or rawlen(players_blue) == 0 then
			lobby()
		end
	end
	if mode == "wait1" and time_remain > 1 then
		if rawlen(players_red) == 0 or rawlen(players_blue) == 0 then
			lobby()
		end
	end
	if mode == "wait2" or mode == "wait3" or mode == "shoot" then
		local m=math.floor(general_time/60)
		local s=math.floor(general_time-(m*60))
		if sudden_death == false then
			if s >= 10 then
				ui.addTextArea(5652,"<font size='24'><p align='center'><font color='#050505'><b>"..m..":"..s.."",nil,353,24,100,40,0,0,1.0,true)
				ui.addTextArea(5651,"<font size='24'><p align='center'><b>"..m..":"..s.."",nil,351,22,100,40,0,0,1.0,true)
			else
				ui.addTextArea(5652,"<font size='24'><p align='center'><font color='#050505'><b>"..m..":0"..s.."",nil,353,24,100,40,0,0,1.0,true)
				ui.addTextArea(5651,"<font size='24'><p align='center'><b>"..m..":0"..s.."",nil,351,22,100,40,0,0,1.0,true)
			end
		elseif sudden_death == true then
			if s >= 10 then
				ui.addTextArea(5652,"<font size='24'><p align='center'><font color='#050505'><b>"..m..":"..s.."",nil,353,24,100,40,0,0,1.0,true)
				ui.addTextArea(5651,"<font size='24'><p align='center'><b><J>"..m..":"..s.."",nil,351,22,100,40,0,0,1.0,true)
			else
				ui.addTextArea(5652,"<font size='24'><p align='center'><font color='#050505'><b>"..m..":0"..s.."",nil,353,24,100,40,0,0,1.0,true)
				ui.addTextArea(5651,"<font size='24'><p align='center'><b><J>"..m..":0"..s.."",nil,351,22,100,40,0,0,1.0,true)
			end
		end
		ui.addTextArea(5654,"<font size='28'><p align='center'><font color='#050505'><b>"..rawlen(alives_red).."",nil,248,24,100,40,0,0,1.0,true)
		ui.addTextArea(5653,"<font size='28'><p align='center'><b><R>"..rawlen(alives_red).."",nil,246,22,100,40,0,0,1.0,true)
		ui.addTextArea(5656,"<font size='28'><p align='center'><font color='#050505'><b>"..rawlen(alives_blue).."",nil,458,24,100,40,0,0,1.0,true)
		ui.addTextArea(5655,"<font size='28'><p align='center'><b><BL>"..rawlen(alives_blue).."",nil,456,22,100,40,0,0,1.0,true)
		if mode == "shoot" then
			ui.addTextArea(5658,"<font size='24'><p align='center'><font color='#050505'><b>"..time_remain.."",nil,353,70,100,40,0,0,1.0,true)
			ui.addTextArea(5657,"<font size='24'><p align='center'><VP><b>"..time_remain.."",nil,351,68,100,40,0,0,1.0,true)
		end
		if general_time > 0 then
			general_time=general_time-0.5
			if sudden_death == false then
				if general_time == 60 then
					showMessage("<ROSE>"..text.t60s.."")
					tfm.exec.playSound("/tfmadv/parade1.mp3",58)
				end
				if general_time == 30 then
					showMessage("<ROSE>"..text.t30s.."")
					tfm.exec.playSound("/tfmadv/parade1.mp3",58)
				end
			end
			if mode == "shoot" and general_time == 0.5 then
				showMessage("<ROSE>"..text.timeup.."")
				tfm.exec.playSound("/tfmadv/soins7.mp3",66)
			end
		end
		if time_passed == 60 and powerups == false and settings.g_powerups == true then
			powerups=true
			showMessage(text.powerups_a)
		end
		if time_passed % 27 == 0 then
			for name,player in next,tfm.get.room.playerList do
				if data[name] and data[name].team > 0 then
					if data[name].killed == false then
						data[name].current_coins=data[name].current_coins+1
					end
				end
			end
		end
		if time_passed % 18 == 0 then
			for name,player in next,tfm.get.room.playerList do
				if data[name] and data[name].team > 0 then
					if data[name].killed == false then
						setScores(name,1,true)
						if name == red_cap or name == blue_cap then
							setScores(name,1,true)
						end
					end
				end
			end
		end
		for name,player in next,tfm.get.room.playerList do
			if data[name] and data[name].team == 1 then
				if tfm.get.room.playerList[name].x > 800 then
					tfm.exec.killPlayer(name)
				end
			end
			if data[name] and data[name].team == 2 then
				if tfm.get.room.playerList[name].x < 800 then
					tfm.exec.killPlayer(name)
				end
			end
		end
	end
	if mode == "wait3" and time_remain <= 1 then
		getAlivePlayers()
	end
	if mode == "shoot" and time_remain == 0 then
		mode="wait2"
		tfm.exec.setGameTime(6)
		enabled=false
		showMessage("<R>"..text.time.."")
	end
	if mode == "wait2" and time_remain <= -1 then
		mode="shoot"
		getAlivePlayers()
	end
	if mode == "wait1" and time_remain == 1 then
		for i=-8, -1 do
			ui.removeTextArea(i,nil)
		end
		tfm.exec.newGame(current_map)
		calculateMatchTime()
	end
	if mode == "end" and time_remain <= 0 then
		lobby()
	end
	if permafrost == true or night_mode == true or gravity == true then
		pf_time=pf_time+1
		if pf_time == 7 then
			permafrost=false
			night_mode=false
			for name,player in next,tfm.get.room.playerList do
				tfm.exec.freezePlayer(name,false)
			end
			ui.removeTextArea(999,nil)
		end
	end
end
lobby()
end

initBeach = function()
for _,f in next,{"AutoNewGame","AfkDeath","AutoShaman","MinimalistMode","PhysicalConsumables"} do
	tfm.exec["disable"..f](true)
end
debug.disableEventLog(true)
system.disableChatCommandDisplay("reset")
tfm.exec.newGame("@7917999")
data={}; changed=false; xml2='';

function showMessage(message,name)
	temp_text=string.gsub(message,"<b>","")
	temp_text=string.gsub(temp_text,"</b>","")
	if tfm.get.room.isTribeHouse == false then
		tfm.exec.chatMessage(message,name)
	else
		ui.addPopup(0,0,temp_text,name,250,75,400,true)
	end
end
function showNPCs(name)
	tfm.exec.addNPC("Julia Lynner",{title = 382, look = "1;228,50,72,0,50_d946a7,90,44,0,0",x = 10032,y = 989,female = true,lookLeft = false,lookAtPlayer = false,interactive = true},name)
	tfm.exec.addNPC("Brand Northern",{title = 357, look = "1;225,0,46,34,26,104_3c3a87+6e7291+a5a7c1+caccdd+7582b3+f3f5f7,49,0,0",x = 10259,y = 875,female = false,lookLeft = false,lookAtPlayer = false,interactive = true},name)
	tfm.exec.addNPC("John Grand",{title = 298, look = "1;231,8,7,34,5,105,0,0,33",x = 9236,y = 1106,female = false,lookLeft = false,lookAtPlayer = true,interactive = true},name)
	tfm.exec.addNPC("Danniel Victor",{title = 296, look = "1;194,29,27,41,54,103,33,81,57",x = 3172,y = 1202,female = false,lookLeft = false,lookAtPlayer = true,interactive = true},name)
	tfm.exec.addNPC("Kenner Henderson",{title = 266, look = "27;236,45,22,0,44,0,50,67,35",x = 751,y = 1263,female = false,lookLeft = false,lookAtPlayer = true,interactive = true},name)
	tfm.exec.addNPC("Keith Cramer",{title = 216, look = "7;190_220b04+767576+585155+c44444+e0ddce+202020+e7e6e5,6_1d1c1c+464646,5_70707+d4c316,9,54,94,36,0,20",x = 648,y = 1337,female = false,lookLeft = false,lookAtPlayer = true,interactive = true},name)
	tfm.exec.addNPC("Mandery Under",{title = 387, look = "138;31,8,69,41,49,0,49,0,0",x = 4778,y = 742,female = false,lookLeft = false,lookAtPlayer = true,interactive = true},name)
	tfm.exec.addNPC("Katarina Worlynder",{title = 220, look = "240;101_e0d9d0+1e9fa8+e0d9d0,36,38,0,62,0,0,0,0",x = 4600,y = 750,female = true,lookLeft = false,lookAtPlayer = true,interactive = true},name)
	tfm.exec.addNPC("Mayra Flowers",{title = 1, look = "112;0,4,0,74_212121+d2d2d2,39,39,44,0,1",x = 6353,y = 355,female = true,lookLeft = true,lookAtPlayer = true,interactive = true},name)
	tfm.exec.addNPC("Aaron Grand",{title = 9, look = "4;225,43,38,0,54,104,0,0,20",x = 9450,y = 146,female = false,lookLeft = false,lookAtPlayer = true,interactive = true},name)
	tfm.exec.addNPC("Daniel Winngs",{title = 2, look = "1;203,50,20,41,42,103,50,0,0",x = 6174,y = 354,female = false,lookLeft = true,lookAtPlayer = true,interactive = true},name)
	tfm.exec.addNPC("Camille Sanders",{title = 257, look = "1;44,40,87,3,62,91,37,52,0",x = 8586,y = 760,female = true,lookLeft = false,lookAtPlayer = true,interactive = true},name)
end
function showWater(name)
	tfm.exec.addImage("182d6e2c97d.png","?1",3080,1,name,1,1)
	tfm.exec.addImage("17be536e980.png","?1",-800,3680,name)
	for _,b in next,{0,2,4} do
		tfm.exec.addImage("183d7db795c.png","?1",-800+(b*1920),1405,name,1,1,0,0.25)
	end
	for _,c in next,{1,3,5} do
		tfm.exec.addImage("183d7db795c.png","?1",1120+(c*1920),1405,name,-1,1,0,0.25)
	end
	for i=0,3 do
		tfm.exec.addImage("183d7dc6861.png","!1",-800+(i*3600),1380,name,1,1,0,0.5)
		tfm.exec.addImage("183d7dc6861.png","?1",-800+(i*3600),1380,name,1,1)
		tfm.exec.addImage("183d7dbc65f.png","!1",-800+(i*3600),1469,name,8,8)
		tfm.exec.addImage("183d7dc1b2f.jpg","?1",-800+(i*3600),1469,name,2,2)
	end
	for h=0,4 do
		tfm.exec.addImage("1803e8e2250.jpg","?1",-1200+(h*2169),1050,name,1,0.75,0,1)
	end
	for k=0,5 do
		tfm.exec.addImage("181ba85ccc2.png","!1",math.random(500,7500),math.random(150,550),name)
	end
	for l=0,5 do
		tfm.exec.addImage("181ba86195e.png","!1",math.random(500,7500),math.random(150,550),name)
	end
	for m=0,5 do
		tfm.exec.addImage("181ba86655c.png","!1",math.random(500,7500),math.random(150,550),name)
	end
	for n=0,4 do
		tfm.exec.addImage("181ba86b15a.png","!1",math.random(7500,10000),math.random(50,300),name)
	end
	tfm.exec.addImage("185c2e9252b.png","!1",4761,770,name,1,1,0,0.8)
	for o=1,3 do
		tfm.exec.addImage("183b4bf34ba.png","+"..o.."",-50,-48,name)
	end
	ui.setBackgroundColor("#7DB1E0")
end
function eventChatCommand(name,message)
	if message == "reset" then
		if name == "Morganadxana#0000" or name == "Ashearcher#0000" then
			tfm.exec.newGame(xml2,false)
			ui.removeTextArea(0,nil)
		end
	end
end
function eventTalkToNPC(name, npc)
	if npc == "Julia Lynner" then
		showMessage("<V>[Julia Lynner] <N>Bem-vindo(a) ao Quiosque do Raposo Azul. Confira os preços de nossos produtos...<br><br>Espera, eu perdi meu papel com os preços!",name)
	elseif npc == "Brand Northern" then
		showMessage("<V>[Brand Northern] <N>Olha, olha, olha a água mineral, água mineral, água mineral...",name)
	elseif npc == "John Grand" then
		showMessage("<V>[John Grand] <J>Ah! Que delícia, cara!",name)
	elseif npc == "Danniel Victor" then
		showMessage("<V>[Danniel Victor] <N>Esta é a área conhecida como <R>Ilha do Dragão Vermelho.<N><br><br>Debaixo dela existe um recife de plantas muito grande, no qual vários peixes conseguem viver muito bem. É um lugar muito lindo, vale a pena conhecer. Ah, e tome cuidado com a água. Não fique muito tempo dentro do mar. Você pode afundar e não voltar mais.",name)
	elseif npc == "Kenner Henderson" then
		showMessage("<V>[Kenner Henderson] <N>Foi você o <R>fi********* <N>que amarrou aquele pneu nas ligações elétricas?<br><br><VP>Não? Ainda bem. <N>Pois algum ser sem cérebro inventou de colocar um pneu nos fios para tentar fazer uma tirolesa. Como estou furioso por isso...<br><br>Ah, e se está curioso para saber o que é aquela escada, ela dá para o gerador nuclear principal, que fica bem no fundo do mar. Não me aventuraria a descer até lá...",name)
	elseif npc == "Keith Cramer" then
		showMessage("<V>[Keith Cramer] <R>NÃO ESTÁ VENDO QUE ESTA É UMA ÁREA RESTRITA? SAIA DAQUI AGORA! QUER SER INFECTADO(A)? NÃO? ENTÃO SAIA AGORA, C******!",name)
	elseif npc == "Mandery Under" then
		showMessage("<V>[Mandery Under] <N>Ei, o que está fazendo na minha piscina suspensa?! Isso tudo é meu!",name)
	elseif npc == "Katarina Worlynder" then
		showMessage("<V>[Katarina Worlynder] <N>Sou a engenheira que ajudei a construir toda a parte elétrica desta praia, que é 100% ecológica.<br><br>Utilizamos energia renovável para alimentar o bar e as tirolesas, e ao mesmo tempo proteger o meio ambiente. Não é lindo?",name)
	elseif npc == "Mayra Flowers" then
		showMessage("<V>[Mayra Flowers] <N>Muuuuuuuu! <font face='Segoe UI Symbol'>(●'◡'●)<font face='Verdana'>",name)
	elseif npc == "Aaron Grand" then
		showMessage("<V>[Aaron Grand] <N>Esta é a Torre do Nascer do Sol. O lugar mais alto da praia. Daqui dá para ver absolutamente tudo. Incluindo o pôr do sol que é lindo.<br><br>Se eu fosse você, nunca mais sairia daqui. Tenho um baita medo de mar...",name)
	elseif npc == "Daniel Winngs" then
		showMessage("<V>[Daniel Winngs] <N>Seja bem-vindo(a). Você definitivamente está em um lugar privilegiado.<br><br>Esta é uma praia totalmente paradisíaca. Com sua água cristinalina, duas tirolesas e uma piscina suspensa, você não vai querer sair daqui tão cedo.",name)
	elseif npc == "Camille Sanders" then
		showMessage("<V>[Camille Sanders] <N>Me paga um passeio de barco? Tenho um desejo incrível de conhecer este lugar!",name)
	end
end
function eventPlayerWon(name)
	if changed == true then
		tfm.exec.respawnPlayer(name)
	end
end
function eventPlayerDied(name)
	if changed == true then
		tfm.exec.respawnPlayer(name)
	end
end
function eventNewGame(name)
	if changed == true then
		for name,_ in next,tfm.get.room.playerList do
			showWater(name)
			showNPCs(name)
		end
		ui.setMapName("Praia da Reserva Verde - <ROSE>Morgana's Mechanical Maps<")
		tfm.exec.setGameTime(3600)
	else
		tfm.exec.setGameTime(5)
		if changed == false then
			xml2=tfm.get.room.xmlMapInfo.xml
			ui.addTextArea(0,"",nil,-800,-400,2400,1200,0x6a7495,0x6a7495,1.0,true)
			ui.setMapName("<J>Carregando mapa. Por favor, aguarde...<")
		else
			ui.removeTextArea(0,nil)
		end
	end
end
function eventNewPlayer(name)
	tfm.exec.respawnPlayer(name)
	showWater(name)
	showNPCs(name)
	newData={
	["z"]=1;
	};
	data[name] = newData;
	if changed == true then
		ui.setMapName("Praia da Reserva Verde - <ROSE>Morgana's Mechanical Maps<")
	end
	showMessage("<VP><b>Bem-vindo(a) a Praia da Reserva Verde.</b><br><br><p align='left'><N>Este é um mapa-script de praia bem grande e com diversos recursos para se divertir. Aproveite e curta!<br><br><R>Aviso: Este mapa pode consumir até 1,8GB de RAM dependendo de casos específicos.<br><br><ROSE><b>Mapa feito por Morganadxana#0000.</b><br><J>Agradecimentos especiais para <b>Draw#6691, Soft#1388, Viincenzo#9526, Lacoste#8972, Lipersz#9863, Spectra_phantom#6089, Threshlimit#0000, Star#8558 e Lanadelrey#4862.</b><br><br><N>Deseja usar este mapa-script no cafofo de sua tribo? Use o link a seguir:<br><N><VP>raw.githubusercontent.com/JW26T-Prj/FunCorpModules/master/Praia%20da%20Reserva%20Verde.lua<br><br><N>Revisão 1.4",name)
end
function eventLoop(p,f)
	if changed == true then
		for name,player in next,tfm.get.room.playerList do
			if tfm.get.room.playerList[name].y >= 1399 then
				if data[name].z <= 1.53 then
					data[name].z=data[name].z+0.003
				end
			else
				data[name].z=1
			end
			tfm.exec.setPlayerGravityScale(name,data[name].z)
			if p >= 6000 then
				if tfm.get.room.playerList[name].y <= 400 and tfm.get.room.playerList[name].x <= 800 and not tfm.get.room.playerList[name].isDead then
					showMessage("<R>Aviso: Não há mais memória disponível para o Transformice. Para poder entrar neste mapa, saia do jogo e entre novamente.",name)
				end
			end
		end
	else
		if f <= 1 then
			changed=true
			tfm.exec.newGame(xml2,false)
			ui.removeTextArea(0,nil)
		end
	end
end
for name,_ in next,tfm.get.room.playerList do
	eventNewPlayer(name)
end
end

initNP = function()
for _,f in next,{"AutoNewGame","AfkDeath","AutoShaman","MinimalistMode","PhysicalConsumables","AutoTimeLeft"} do
	tfm.exec["disable"..f](true)
end
debug.disableEventLog(true)
system.disableChatCommandDisplay("reset")
tfm.exec.newGame("@7917579")
data={}; changed=false; xml2='';
npc_01={title = 5,look = "1;190_dbe10f+767576+585155+c44444+e0ddce+202020+e7e6e5,0,30_1f618d+2fb9a2+3a2cf0,0,54,111,49,0,0",x = 141,y = 2275,female = false,lookLeft = false,lookAtPlayer = true,interactive = true}
npc_02={title = 339,look = "1;40_d0ff+1825e7,6_700ff+b8ff,20_beff,0,29_d99+b2ff,0,1_ffff+ff0000,0,0",x = 40,y = 2950,female = false,lookLeft = false,lookAtPlayer = false,interactive = true}
npc_03={title = 382,look = "179;236_434f55+434f55+434f55+434f55+605520+a19d88,50,82,0,62,112,44,0,0",x = 3128,y = 1906,female = true,lookLeft = false,lookAtPlayer = false,interactive = true}
npc_04={title = 115,look = "222;229,46,84_988c5c+d252d6+b8a866+3062c7+d3eb29,0,65,0,52,84,0",x = 5072,y = 1632,female = true,lookLeft = true,lookAtPlayer = true,interactive = true}
npc_05={title = 10,look = "1;44,40,89,34,0,0,31,77,2_c918be",x = 1908,y = 2402,female = true,lookLeft = false,lookAtPlayer = true,interactive = true}
npc_06={title = 2,look = "113;223,8,27_252525+383838+242424,31,55_6d2e29+9e9983+ddba1d,0,0,51,48",x = 1088,y = 336,female = false,lookLeft = true,lookAtPlayer = true,interactive = true}
npc_07={title = 42,look = "157;83,0,9,0,6,102_148960+f7eeba+f7eeba,0,79,47",x = 1033,y = 1121,female = false,lookLeft = true,lookAtPlayer = false,interactive = true}
npc_08={title = 213,look = "223;244,33,89,0,6,102_148960+f7eeba+f7eeba,0,72,47",x = 5117,y = 1417,female = true,lookLeft = false,lookAtPlayer = true,interactive = true}
npc_09={title = 11,look = "213;217_436b98+41d7fb+327548+287f9d+e0e8f3+555e88,23_3976eb+21170d+3488bb+21170d+21170d,23_b68ad,34_1c815b,17,83,49_3477ac+2d2d2d,0,0",x = 883,y = 2985,female = false,lookLeft = true,lookAtPlayer = true,interactive = true}
npc_10={title = 1, look = "112;0,4,0,74_212121+d2d2d2,39,39,44,0,1",x = 685,y = 912,female = true,lookLeft = true,lookAtPlayer = true,interactive = true}

function initNPC(name)
	tfm.exec.addNPC("Keith Hertzon", npc_01, name)
	tfm.exec.addNPC("Dhanny Dier", npc_02, name)
	tfm.exec.addNPC("Andressa Nyeder", npc_03, name)
	tfm.exec.addNPC("Fabia Murray", npc_04, name)
	tfm.exec.addNPC("Carla Esther", npc_05, name)
	tfm.exec.addNPC("Dereek Nandertz", npc_06, name)
	tfm.exec.addNPC("Damian Henderson", npc_07, name)
	tfm.exec.addNPC("Luciana Bander", npc_08, name)
	tfm.exec.addNPC("Jesse Malcolm", npc_09, name)
	tfm.exec.addNPC("Mayra Flowers", npc_10, name)
end
function showMessage(message,name)
	temp_text=string.gsub(message,"<b>","")
	temp_text=string.gsub(temp_text,"</b>","")
	if tfm.get.room.isTribeHouse == false then
		tfm.exec.chatMessage(message,name)
	else
		ui.addPopup(0,0,temp_text,name,250,75,400,true)
	end
end

function eventTalkToNPC(name, npc)
	if npc == "Keith Hertzon" then
		showMessage("<V>[Keith Hertzon] <N>Quem é você? Ah, mais um visitante...<br><br>Bem, se quer saber o destino deste elevador... Bem, eu acho que não deve ser bem o que você espera.<br><br>Você vai descer bastante dentro do rio. Chuto que deva ser uns 20 metros de profundidade... Você vai encontrar umas cápsulas bem antigas que era usadas para navegação, mas aquilo já existe há anos, então duvido que ainda funcione. Mas vai que, né...",name)
	elseif npc == "Dhanny Dier" then
		showMessage("<V>[Dhanny Dier] <N>Você é muito(a) corajoso(a) para estar neste lugar. A pressão aqui é bem alta.<br><br>Mas se quiser saber o que são aquelas coisas, são esferas submarinas. Elas eram utilizadas há décadas atrás, mas acredito que estejam todas enferrujadas. Não recomendo tentar ir para lá, a não ser que realmente seja muito curioso(a). <b>E sim, isto é um aviso.</b>",name)
	elseif npc == "Andressa Nyeder" then
		showMessage("<V>[Andressa Nyeder] <N>Seja bem-vindo(a). Este é o mirante de observação do Parque Aquático Natural das Cobras. Daqui é possível ver quase toda a extensão do rio com muito mais clareza.<br><br>As cobras não são lindas? E o melhor de tudo, não são venenosas! Você pode fazer carinho nelas sem medo.",name)
	elseif npc == "Fabia Murray" then
		showMessage("<V>[Fabia Murray] <N>Alguém aqui está preparado(a) para grandes emoções? Tomem cuidado apenas com as cobras!",name)
	elseif npc == "Carla Esther" then
		local chance=math.random(1,50)
		if chance == 10 and data[name].below == false then
			showMessage("<V>[Carla Esther] <R><b>Afunde e conheça as profundezas, seu inconveniente!</b>",name)
			tfm.exec.giveCheese(name)
			data[name].below=true
		else
			showMessage("<V>[Carla Esther] <J>Alguém me salve! A água está muito gelada e eu não sei nadar!",name)
		end
	elseif npc == "Dereek Nandertz" then
		showMessage("<V>[Dereek Nandertz] <N>Está perdido(a)? Não precisa se preocupar. Eu serei o seu guia.<br><br>Ali na frente, há uma tirolesa bem grande e um trampolim. Desse jeito, você consegue sentir a água gelada do rio com muito mais propriedade.<br><br><R>Só vê se não fica muito tempo pulando no trampolim... Aquilo já quebrou várias vezes por conta de alguns que nem quero comentar.",name)
	elseif npc == "Damian Henderson" then
		showMessage("<V>[Damian Henderson] <N>Está preparado? Pois se não estiver, é melhor estar. Esta é o maior escorregador aquático do mundo!<br><br>Com quase 55 metros de altura, é literalmente uma aventura de cair o queixo. Definitivamente não é um brinquedo para medrosos.<br><br>E aí, vai encarar?",name)
	elseif npc == "Luciana Bander" then
		showMessage("<V>[Luciana Bander] <N>Espera! Não está chovendo! Como eu queria uma boa chuva por aqui... Faz muito tempo que não cai uma água. Fora a que já tem no rio.",name)
	elseif npc == "Jesse Malcolm" then
		showMessage("<V>[Jesse Malcolm] <N>Nunca imaginarei que alguém pudesse chegar neste lugar tão ruim... No fundo de um gelado rio... Mas se quiser saber quem eu sou, então deixe-me explicar.<br><br>Certo dia estava me divertindo aqui no parque e praticando natação no rio, que é meu esporte favorito. Mas certo dia, o feitiço de uma mulher desconhecida me atacou e agora sou obrigado a viver aqui. Na escuridão. No frio.<br><br>Ah, vê se não fica muito tempo aqui em baixo, ou você pode congelar.",name)
	elseif npc == "Mayra Flowers" then
		showMessage("<V>[Mayra Flowers] <N>Muuuuuuuu! <font face='Segoe UI Symbol'>(●'◡'●)<font face='Verdana'>",name)
	end
end

function showWater(name)
	for _,h in next,{0,2,4} do
		tfm.exec.addImage("18204168d2e.png","?1",-1200+(h*1400),3050,name,1,0.5,0,1)
	end
	for _,j in next,{1,3,5} do
		tfm.exec.addImage("18204168d2e.png","?1",200+(j*1400),3050,name,-1,0.5,0,1)
	end
	for _,m in next,{0,2,4} do
		tfm.exec.addImage("18204168d2e.png","?1",-1200+(m*1400),3672,name,1,-2,0,1)
	end
	for _,n in next,{1,3,5} do
		tfm.exec.addImage("18204168d2e.png","?1",200+(n*1400),3672,name,-1,-2,0,1)
	end
	for _,as in next,{0,2,4} do
		tfm.exec.addImage("183bac46d1a.png","?1",-800+(as*1488),3365,name,1,-1,0,0.7)
	end
	for _,at in next,{1,3,5} do
		tfm.exec.addImage("183bac46d1a.png","?1",688+(at*1488),3365,name,-1,-1,0,0.7)
	end
	for i=0,1 do
		tfm.exec.addImage("18200689108.png", "?1", -800+(i*7180), 2387, name, 1.0, 1.0, 0, 1.0)
		tfm.exec.addImage("18200689108.png", "!1", -800+(i*7180), 2387, name, 1.0, 1.0, 0, 0.56)
		tfm.exec.addImage("1820068de62.png", "!1", -800+(i*7180), 2445, name, 6, 1.5, 0, 0.8)
	end
	for w=1,6 do
		tfm.exec.addImage("181ba85ccc2.png","!1",math.random(50,5300),math.random(160,1800),name)
	end
	for b=0,1 do
		tfm.exec.addImage("18200692b61.jpg","?1",-800+(b*1795),2445,name,4,4)
	end
	for x=1,6 do
		tfm.exec.addImage("181ba86195e.png","!1",math.random(50,5300),math.random(160,1800),name)
	end
	for y=1,6 do
		tfm.exec.addImage("181ba86655c.png","!1",math.random(50,5300),math.random(160,1800),name)
	end
	for z=1,6 do
		tfm.exec.addImage("181ba86b15a.png","!1",math.random(50,5300),math.random(160,1800),name)
	end
	for a=0,3 do
		for c=0,4 do
			tfm.exec.addImage("181b9de5c95.png","?1",-800+(c*1920),2380-(a*1080),name, 1, 1, 0, 0.2+(a*0.2))
		end
	end
	tfm.exec.addImage("17e937f4f5a.png","?1",-800,-1735,name,30,1)
	tfm.exec.addImage("182386211f8.png","+1",-90,-90,name)
	tfm.exec.addImage("182386211f8.png","+2",-90,-90,name)
	tfm.exec.addImage("182386211f8.png","+3",-90,-90,name)
end
function eventChatCommand(name,message)
	if message == "reset" then
		if name == "Morganadxana#0000" or name == "Ashearcher#0000" then
			tfm.exec.newGame(xml2,false)
			ui.removeTextArea(0,nil)
		end
	end
end
function eventPlayerWon(name)
	if changed == true then
		tfm.exec.respawnPlayer(name)
	end
end
function eventPlayerDied(name)
	if changed == true then
		tfm.exec.respawnPlayer(name)
	end
	data[name].z=1; data[name].below=false; data[name].fs=0; data[name].freezed=false;
end
function eventNewGame(name)
	if changed == true then
		for name,_ in next,tfm.get.room.playerList do
			showMessage("<VP><b>Bem-vindo(a) ao Parque Aquático Natural das Cobras.</b><br><br><p align='left'><N>Este é um mapa-script bem diferente de tudo o que você já viu.<br>O rio é muito profundo! Caso não saiba nadar, recomendo sair desta sala agora! Mas se souber, apenas aproveite e curta!<br><br><R>Aviso: Este mapa pode consumir até 1,2GB de RAM dependendo de casos específicos.<br><br><ROSE><b>Mapa feito por Morganadxana#0000.</b><br><J>Agradecimentos especiais para Aurelianlua#0000, Velkozdapic#0000, Lanadelrey#4862, Lorena#0960, Star#8558, Soft#1388, Some#2636, Leticia1k#0000, Draw#6691 e Joanaanne#0000.<b></b><br><br><N>Deseja usar este mapa-script no cafofo de sua tribo? Use o link a seguir:<br><N><VP>raw.githubusercontent.com/JW26T-Prj/FunCorpModules/master/Parque%20Aqu%C3%A1tico%20Natural%20das%20Cobras.lua<br><br><N>Revisão 1.1",name)
			showWater(name)
			initNPC(name)
		end
		ui.setMapName("<VP>Parque Aquático Natural das Cobras - <ROSE>Morgana's Mechanical Maps<")
		tfm.exec.setGameTime(7200)
	else
		tfm.exec.setGameTime(5)
		if changed == false then
			xml2=tfm.get.room.xmlMapInfo.xml
			ui.addTextArea(0,"",nil,-800,-400,2400,1200,0x6a7495,0x6a7495,1.0,true)
			ui.setMapName("<J>Carregando mapa. Por favor, aguarde...<")
		else
			ui.removeTextArea(0,nil)
		end
	end
end
function eventNewPlayer(name)
	tfm.exec.respawnPlayer(name)
	newData={
	["z"]=1;
	["below"]=false;
	["fs"]=0;
	["freezed"]=false;
	["warn"]=false;
	};
	data[name] = newData;
	if changed == true then
		ui.setMapName("<VP>Parque Aquático Natural das Cobras - <ROSE>Morgana's Mechanical Maps<")
		showMessage("<VP><b>Bem-vindo(a) ao Parque Aquático Natural das Cobras.</b><br><br><p align='left'><N>Este é um mapa-script bem diferente de tudo o que você já viu.<br>O rio é muito profundo! Caso não saiba nadar, recomendo sair desta sala agora! Mas se souber, apenas aproveite e curta!<br><br><R>Aviso: Este mapa pode consumir até 1,2GB de RAM dependendo de casos específicos.<br><br><ROSE><b>Mapa feito por Morganadxana#0000.</b><br><J>Agradecimentos especiais para Aurelianlua#0000, Velkozdapic#0000, Lanadelrey#4862, Lorena#0960, Star#8558, Soft#1388, Some#2636, Leticia1k#0000, Draw#6691 e Joanaanne#0000.<b></b><br><br><N>Deseja usar este mapa-script no cafofo de sua tribo? Use o link a seguir:<br><N><VP>raw.githubusercontent.com/JW26T-Prj/FunCorpModules/master/Parque%20Aqu%C3%A1tico%20Natural%20das%20Cobras.lua<br><br><N>Revisão 1.1",name)
		showWater(name)
		initNPC(name)
	end
end
for name,player in next,tfm.get.room.playerList do
	eventNewPlayer(name)
end
function eventLoop(p,f)
	if changed == true then
	for name,player in next,tfm.get.room.playerList do
		if not string.find(tfm.get.room.playerList[name].look,"106") then
			if tfm.get.room.playerList[name].y >= 2395 then
				if data[name].z <= 1.32 then
					data[name].z=data[name].z+0.002
				end
			else
				data[name].z=data[name].z-0.04
				if data[name].z <= 1 then
					data[name].z=1
				end
			end
		end
		if tfm.get.room.playerList[name].y >= 2550 then
			data[name].fs=data[name].fs+1
			if data[name].fs == 5 and data[name].warn == false then
				data[name].warn=true
				showMessage("<VP>Tenha cuidado: A água do rio é muito gelada. Ficar por muito tempo pode congelar seu rato.",name)
			end
			if data[name].fs == 150 then
				data[name].freezed=true
				tfm.exec.freezePlayer(name)
				tfm.exec.setPlayerGravityScale(name,1.4)
			end
		else
			data[name].fs=0
		end
		if data[name].freezed == false then
			tfm.exec.setPlayerGravityScale(name,data[name].z)
		end
	end
	else
		if f <= 1 then
			changed=true
			tfm.exec.newGame(xml2,false)
			ui.removeTextArea(0,nil)
		end
	end
end
end

initWatercatch = function()
admin={""} -- Insira o nome dos FunCorps aqui!

for _,f in next,{"AutoNewGame","AutoShaman","AutoTimeLeft","DebugCommand","AllShamanSkills","PhysicalConsumables"} do
	tfm.exec["disable"..f](true)
end
for _,f in next,{"help","ajuda","tc","kill","powerups","creditos","changelog","reset","skins"} do
	system.disableChatCommandDisplay(f)
end
if tfm.get.room.isTribeHouse == false then tfm.exec.setRoomMaxPlayers(40) end
shaman=""; alives=0; cannons=10; z=0; data={}; mode="load"; changed=false; loop=0; timer=0; xml=''; time_passed=0; time_remain=0;
powerups={x1=-1,x2=-1,x3=-1,x4=-1,x5=-1,y1=-1,y2=-1,y3=-1,y4=-1,y5=-1,t1=0,t2=0,t3=0,t4=0,t5=0}

function showMessage(message,name)
	temp_text=string.gsub(message,"<b>","")
	temp_text=string.gsub(temp_text,"</b>","")
	if tfm.get.room.isTribeHouse == false then
		tfm.exec.chatMessage(message,name)
	elseif tfm.get.room.isTribeHouse == true then
		if name == nil then
			print("<ROSE>[Test Mode] : <br><BL>"..temp_text.."")
		else
			print("<ROSE>[Test Mode] - "..name.." : <br><BL>"..temp_text.."")
		end
	end
end
function showAvailableSharks(name)
	i=0
	for _,link in next,{"18309d69a5a.png","18309d64e58.png","18309d7325a.png","18412b7b55e.png"} do
		i=i+1
		image_id=tfm.exec.addImage(link,"&1",83,90+(i*49),name,0.5,0.5,0,1.0)
		table.insert(data[name].active_imgs,image_id)
	end
	i=0
	for _,link in next,{"18309d6029f.png","18412b7695c.png","18309d6e65a.png","18412b71ce2.png"} do
		i=i+1
		image_id=tfm.exec.addImage(link,"&1",293,90+(i*52),name,0.5,0.5,0,1.0)
		table.insert(data[name].active_imgs,image_id)
	end
	i=0
	for _,link in next,{"185c2e9722e.png","185c2ea0c4f.png","185c2e9bf2f.png"} do
		i=i+1
		image_id=tfm.exec.addImage(link,"&1",503,90+(i*48),name,0.5,0.5,0,1.0)
		table.insert(data[name].active_imgs,image_id)
	end
	ui.addTextArea(1006,"<i><font size='11.5'><b>Tubarão Normal 1</b><br><br><a href='event:a1'>Usar!</a><br><br><b>Tubarão Normal 2</b><br><br><a href='event:a2'>Usar!</a><br><br><b>Tubarão Normal 3</b><br><br><a href='event:a3'>Usar!</a><br><br><b>Tubarão Normal 4</b><br><br><a href='event:a6'>Usar!</a>",name,170,129,175,315,0,0,1.0,true)
	ui.addTextArea(1007,"<i><font size='11.5'><b>Tubarão Branco 1</b><br><br><a href='event:a4'>Usar!</a><br><br><b>Tubarão Branco 2</b><br><br><a href='event:a7'>Usar!</a><br><br><b>Tubarão-Martelo</b><br><br><a href='event:a5'>Usar!</a><br><br><b>Barracuda</b><br><br><a href='event:a8'>Usar!</a>",name,380,129,175,265,0,0,1.0,true)
	ui.addTextArea(1008,"<i><font size='11.5'><b>Peixe Diabo-Negro</b><br><br><a href='event:a9'>Usar!</a><br><br><b>Tubarão-Tigre</b><br><br><a href='event:a11'>Usar!</a><br><br><b>Baleia</b><br><br><a href='event:a10'>Usar!</a><br><br><br><b><a href='event:a0'>Desativar skins</a>",name,590,129,175,265,0,0,1.0,true)
end
function removeImagePlayers(name)
	if rawlen(data[name].active_imgs) > 0 then
		for _,id in next,data[name].active_imgs do
			tfm.exec.removeImage(id)
		end
		data[name].active_imgs={}
	end
end
function displayShark(name,type,reverse)
	if type == 1 then
		if reverse == false then
			data[name].shark_id=tfm.exec.addImage("18309d69a5a.png","$"..name.."",85,-42,nil,-1,1)
		else
			data[name].shark_id=tfm.exec.addImage("18309d69a5a.png","$"..name.."",-90,-42,nil,1,1)
		end
	elseif type == 2 then
		if reverse == true then
			data[name].shark_id=tfm.exec.addImage("18309d64e58.png","$"..name.."",85,-31,nil,-1,1)
		else
			data[name].shark_id=tfm.exec.addImage("18309d64e58.png","$"..name.."",-90,-31,nil,1,1)
		end
	elseif type == 3 then
		if reverse == false then
			data[name].shark_id=tfm.exec.addImage("18309d7325a.png","$"..name.."",78,-50,nil,-1,1)
		else
			data[name].shark_id=tfm.exec.addImage("18309d7325a.png","$"..name.."",-80,-50,nil,1,1)
		end
	elseif type == 4 then
		if reverse == false then
			data[name].shark_id=tfm.exec.addImage("18309d6029f.png","$"..name.."",70,-29,nil,-1,1)
		else
			data[name].shark_id=tfm.exec.addImage("18309d6029f.png","$"..name.."",-50,-29,nil,1,1)
		end
	elseif type == 5 then
		if reverse == false then
			data[name].shark_id=tfm.exec.addImage("18309d6e65a.png","$"..name.."",85,-55,nil,-1,1)
		else
			data[name].shark_id=tfm.exec.addImage("18309d6e65a.png","$"..name.."",-90,-55,nil,1,1)
		end
	elseif type == 6 then
		if reverse == false then
			data[name].shark_id=tfm.exec.addImage("18412b7b55e.png","$"..name.."",85,-40,nil,-1,1)
		else
			data[name].shark_id=tfm.exec.addImage("18412b7b55e.png","$"..name.."",-90,-40,nil,1,1)
		end
	elseif type == 7 then
		if reverse == false then
			data[name].shark_id=tfm.exec.addImage("18412b7695c.png","$"..name.."",65,-39,nil,-1,1)
		else
			data[name].shark_id=tfm.exec.addImage("18412b7695c.png","$"..name.."",-70,-39,nil,1,1)
		end
	elseif type == 8 then
		if reverse == false then
			data[name].shark_id=tfm.exec.addImage("18412b71ce2.png","$"..name.."",75,-26,nil,-1,1)
		else
			data[name].shark_id=tfm.exec.addImage("18412b71ce2.png","$"..name.."",-80,-26,nil,1,1)
		end
	elseif type == 9 then
		if reverse == false then
			data[name].shark_id=tfm.exec.addImage("185c2e9722e.png","$"..name.."",35,-60,nil,-1,1)
		else
			data[name].shark_id=tfm.exec.addImage("185c2e9722e.png","$"..name.."",-40,-60,nil,1,1)
		end
	elseif type == 10 then
		if reverse == false then
			data[name].shark_id=tfm.exec.addImage("185c2e9bf2f.png","$"..name.."",65,-44,nil,-1,1)
		else
			data[name].shark_id=tfm.exec.addImage("185c2e9bf2f.png","$"..name.."",-70,-44,nil,1,1)
		end
	elseif type == 11 then
		if reverse == false then
			data[name].shark_id=tfm.exec.addImage("185c2ea0c4f.png","$"..name.."",75,-36,nil,-1,1)
		else
			data[name].shark_id=tfm.exec.addImage("185c2ea0c4f.png","$"..name.."",-80,-36,nil,1,1)
		end
	end
end
function verifyAdmin(name)
	for i=1,rawlen(admin) do
		if admin[i] == name then
			return true
		end
	end
end
function showWater(name)
	for i=0,6 do
		tfm.exec.addImage("185c2e9252b.png", "?1", -800+(i*944), 457, name, 1.0, 1.0, 0, 1.0)
		tfm.exec.addImage("185c2e9252b.png", "!1", -800+(i*944), 457, name, 1.0, 1.0, 0, 0.55)
	end
	tfm.exec.addImage("185c2e88ac8.png", "!1", -800, 664, name, 30, 3.6)
	tfm.exec.addImage("185c2e88ac8.png", "!1", -800, 3904, name, 30, -3.6)
	tfm.exec.addImage("185c2e8d858.png", "?1", -800, 664, name, 30, 3.6)
	for _,m in next,{0,2,4} do
		tfm.exec.addImage("18204168d2e.png","!1",-1200+(m*1400),2590,name,1,-1.5,0,1)
	end
	for _,n in next,{1,3,5} do
		tfm.exec.addImage("18204168d2e.png","!1",200+(n*1400),2590,name,-1,-1.5,0,1)
	end
	for _,h in next,{0,2,4} do
		tfm.exec.addImage("18204168d2e.png","!1",-1200+(h*1400),2122,name,1,0.4,0,1)
	end
	for _,j in next,{1,3,5} do
		tfm.exec.addImage("18204168d2e.png","!1",200+(j*1400),2122,name,-1,0.4,0,1)
	end
	for w=1,2 do
		tfm.exec.addImage("181ba85ccc2.png","!1",math.random(50,4000),math.random(-50,250),name,0.5,0.5)
	end
	for x=1,2 do
		tfm.exec.addImage("181ba86195e.png","!1",math.random(50,4000),math.random(-50,250),name,0.5,0.5)
	end
	for y=1,3 do
		tfm.exec.addImage("181ba86655c.png","!1",math.random(50,4000),math.random(-50,250),name,0.5,0.5)
	end
	for z=1,3 do
		tfm.exec.addImage("181ba86b15a.png","!1",math.random(50,4000),math.random(-50,250),name,0.5,0.5)
	end
	tfm.exec.addImage("17fe3741e5f.jpg","?1",-400,-350,name,8.5,1,0,1)
end
function eventPlayerDied(n)
	if not tfm.get.room.playerList[n].isShaman then
		alives=alives-1
		tfm.exec.setPlayerScore(n,1,true)
	end
	if alives <= 0 then
		mode="end"
		tfm.exec.setGameTime(15)
		showMessage("<VP><b>O shaman matou todos os ratos e venceu o jogo!</b><br><N>Próxima rodada iniciando em 15 segundos.")
	end
	data[n].o=0
	if mode == "hide" or mode == "game" then
		if tfm.get.room.playerList[n].isShaman then
			showMessage("<R>O shaman morreu, está AFK ou saiu da sala. Iniciando nova partida...")
			tfm.exec.setPlayerScore(shaman,-2,false)
			mode="end"
			tfm.exec.setGameTime(10)
			for n,_ in next,tfm.get.room.playerList do
				if not tfm.get.room.playerList[n].isDead then
					tfm.exec.setPlayerScore(n,1,true)
					alives=alives+1
					ui.removeTextArea(300,n)
				end
			end
		end
	end
end
function moveShaman()
	position=math.random(1,3)
	if position == 1 then
		tfm.exec.movePlayer(shaman,631,181,false,0,0,false)
	elseif position == 2 then
		tfm.exec.movePlayer(shaman,2769,50,false,0,0,false)
	elseif position == 3 then
		tfm.exec.movePlayer(shaman,4333,186,false,0,0,false)
	end
end
function checkOxygenZones(name)
	if tfm.get.room.playerList[name].x >= 2328 and tfm.get.room.playerList[name].x <= 2474 then
		if tfm.get.room.playerList[name].y >= 1230 and tfm.get.room.playerList[name].y <= 1300 then
			return true
		end
	end
	if  tfm.get.room.playerList[name].x >= 442 and tfm.get.room.playerList[name].x <= 585 then
		if tfm.get.room.playerList[name].y >= 2106 then
			return true
		end
	end
	if tfm.get.room.playerList[name].x >= 3918 and tfm.get.room.playerList[name].x <= 4066 then
		if tfm.get.room.playerList[name].y >= 1270 and tfm.get.room.playerList[name].y <= 1405 then
			return true
		end
	end
	if tfm.get.room.playerList[name].x >= 3818 and tfm.get.room.playerList[name].x <= 3966 then
		if tfm.get.room.playerList[name].y >= 1800 and tfm.get.room.playerList[name].y <= 1894 then
			return true
		end
	end
	if tfm.get.room.playerList[name].x >= 705 and tfm.get.room.playerList[name].x <= 850 then
		if tfm.get.room.playerList[name].y >= 1467 and tfm.get.room.playerList[name].y <= 1548 then
			return true
		end
	end
end
function eventNewPlayer(name)
	tfm.exec.setPlayerScore(name,0,false)
	showWater(name)
	ui.setMapName("<font color='#0080ff'><b>#watercatch!</b><N> Versão <VP><b>v4.3.0</b><N> - criado por <ROSE><b>Morganadxana#0000</b><")
	newData={
	["o"]=99; ["i"]=0; ["t"]=0; ["c"]=0; ["opened"]=false; ["imageid"]=-1; ["imageid2"]=-1; ["imageid3"]=-1; ["imageid4"]=-1; ["imaget"]=5; ["shark_id"]=0; ["shark"]=0; ["active_imgs"]={};
	};
	data[name] = newData;
	showMessage("<font color='#0080ff'><b>Bem-vindos ao module #watercatch!</b><br><J>Digite !help para ver a ajuda deste module.<br><br><N>Module criado por Morganadxana#0000.<br><br><BL>Atenção: Conexões lentas com a Internet podem fazer com que as artes da água demorem para carregar.<br><br>Caso o mapa não carregue, saia do jogo e entre novamente.",name)
	data[name].imageid = tfm.exec.addImage("17a53e210bf.png","&1",180,90,name)
	data[name].imageid2 = tfm.exec.addImage("17a53e1f94c.png",":1",0,350,name)
	data[name].imageid3 = tfm.exec.addImage("17ae4e47000.png","&1",2,22,name)
	data[name].imageid4 = tfm.exec.addImage("17ae4e48770.png","&1",670,22,name)
	data[name].imaget=5
	ui.addTextArea(299,"<p align='center'><a href='event:hide_menu'><font size='18'>Menu",name,365,25,70,24,0x000001,0x000001,0.75,true)
end
for name,player in next,tfm.get.room.playerList do
	eventNewPlayer(name)
end
function eventChatCommand(name,message)
	if message == "help" or message == "ajuda" then
		showMenu(name,0xf0f0f0,140,90,520,265,"Ajuda do Module #watercatch","O objetivo é bem simples: <b>Fugir do shaman</b>, se escondendo dentro do lago e tomando cuidado para não morrer afogado!<br><R><b>Shamans, não esqueçam de se mexer, ou irão morrer AFK!</b><br><br><VP>Os quadrados marcados por <N>'!'<VP> são powerups, que geram efeitos aleatórios nos ratos.<J><br>Estes powerups podem ser acionados pressionando ESPAÇO em cima deles.<br><N>Você pode ver os possíveis efeitos dos powerups indo no Menu e clicando em Powerups. Vale ressaltar que eles funcionam apenas depois que o shaman for liberado.<br><br><N>Caso você seja shaman, você tem um limite de <b>10</b> objetos que podem ser utilizados. Exceder este limite fará com que a partida acabe.")
	end
	if message == "powerups" then
		showMenu(name,0xf0f0f0,140,86,520,290,"Powerups do Module #watercatch","<font size='11'>Os seguintes powerups estão disponíveis no momento:<br><ROSE><b>• ARMADILHA</b><N><br>Prende seu rato em uma armadilha triangular.<br><ROSE><b>• OXIGÊNIO</b><N><br>Aumenta o seu nível de oxigênio em 50%.<br><ROSE><b>• VELOCIDADE</b><N><br>Te dá um grande impulso de velocidade.<br><ROSE><b>• AFUNDAR</b><N><br>Cria uma curta anomalia que puxa todos os ratos em direção ao fundo do lago.<br><ROSE><b>• MEEP</b><N><br>Te dá o poder de usar o Meep!<br><ROSE><b>• SUFOCO</b><N><br>Diminui o seu nível de oxigênio em 35%. Caso seu nível esteja abaixo disso e você pegue este powerup, você morrerá afogado.<br><ROSE><b>• CONGELAR</b><N><br>Congela o seu rato.<br><ROSE><b>• QUEIJO</b><N><br>Dá queijo para o seu rato. Caso você esteja dentro do lago, você provavelmente será levado para o fundo dele.")
	end
	if message == "creditos" then
		showMenu(name,0xf0f0f0,140,90,520,150,"Créditos","As seguintes pessoas ajudaram no desenvolvimento deste module:<br><br><ROSE><b>• Morganadxana#0000</b><N> - Desenvolvedora do código<br><ROSE><b>• Shun_kazami#7014</b><N> - Criação do mapa<br><ROSE><b>• Akwimos#1937</b><N> - Tradução do código original para o Português<br><ROSE><b>• Spectra_phantom#6089</b><N> - Ideia original e criação das artes")
	end
	if message == "skins" then
		if name == "Morganadxana#0000" or name == "Akwimos#1937" or name == "Spectra_phantom#6089" or verifyAdmin(name) == true then
			showMessage("<R>As skins de tubarão serão exibidas quando você for shaman, e estiver dentro do lago!",name)
			showMenu(name,0x949494,65,98,670,240,"Skins","")
			showAvailableSharks(name)
		else
			if tfm.get.room.playerList[name].isShaman == false then
				showMessage("<R>As skins de tubarão serão exibidas quando você for shaman, e estiver dentro do lago!",name)
				showMenu(name,0x949494,65,98,670,240,"Skins","")
				showAvailableSharks(name)
			else
				showMessage("<J>Para evitar bugs, não é mais possível trocar de skin de tubarão enquanto for shaman.",name)
			end
		end
	end
	if message == "changelog" then
		showMenu(name,0xf0f0f0,140,90,520,180,"Changelog da Versão 4.3.0","• Correções de bugs nas zonas de oxigênio<br>• Correção de bug na escolha de skins<br>• O powerup OXIGÊNIO foi melhorado de 40% para 50%<br>• O powerup CAIXA foi substituído por ARMADILHA<br>• O tempo do powerup QUEIJO foi reduzido de 12 para 8 segundos<br>• O tempo do powerup CONGELAR foi reduzido de 8 para 6 segundos<br>• O tempo das partidas agora é fixado em 4 minutos<br>• Os ratos que morrem afogados viram pedras ao invés de galinhas")
	end
	if (message:sub(0,2)== "tc") then
		if tfm.get.room.playerList[name].isShaman == false then
			for n,_ in next,tfm.get.room.playerList do
				if tfm.get.room.playerList[n].isShaman == false then
					showMessage("<R>• ["..name.."]</b> <N>"..message:sub(4).."",n)
				end
			end
		end
	end
	if name == "Morganadxana#0000" or name == "Akwimos#1937" or name == "Spectra_phantom#6089" or verifyAdmin(name) == true then
		if (message:sub(0,3) == "msg") then
			showMessage("<VP>• [FunCorp - <b>"..name.."</b>] "..message:sub(5).."")
		end
		if (message:sub(0,4) == "kill") then
			tfm.exec.killPlayer(message:sub(6))
		end
		if message == "reset" then
			reset()
		end
	end
end
function eventSummoningEnd(name,id,x,y)
	if id >= 1 then
		cannons=cannons-1
		if cannons >= 1 then
			showMessage("<VP>O shaman agora pode usar <b>"..cannons.."</b> objetos.")
		elseif cannons == 0 then
			showMessage("<VP>O shaman não pode mais usar objetos!")
			showMessage("<R>Você não pode mais invocar objetos! Fazer isso ocasionará na sua morte e na perda de sua vez de shaman.",shaman)
		elseif cannons <= -1 then
			showMessage("<R>O shaman excedeu o limite de objetos utilizáveis!")
			tfm.exec.killPlayer(shaman)
		end
	end
end
function eventSummoningStart(name,id,x,y)
	if cannons == 0 then
		showMessage("<R>Você não pode mais invocar objetos! Fazer isso ocasionará na sua morte e na perda de sua vez de shaman.",name)
	end
end
function resetMap()
	if xml == '' then
		tfm.exec.disableAutoShaman(true)
		tfm.exec.newGame("@7925247")
		ui.setMapName("Carregando mapa. Por favor, aguarde...<")
		changed=false
		mode="load"
	else
		changed=true
		tfm.exec.newGame(xml)
	end
end
function activatePowerup(name,id,number)
	if id == 1 then
		showMessage("<N>"..name.." <J>ativou o powerup <ROSE><b>ARMADILHA!</b>")
		dropPlayer(name)
		tfm.exec.playSound("/transformice/son/petard.mp3", 75, nil, nil, name)
	elseif id == 2 then
		showMessage("<N>"..name.." <J>ativou o powerup <ROSE><b>OXIGÊNIO!</b>")
		if not tfm.get.room.playerList[name].isShaman then
			data[name].o=data[name].o+50
			if data[name] and data[name].o > 100 then
				data[name].o=100
			end
		end
		tfm.exec.playSound("/deadmaze/objectif2.mp3", 75, nil, nil, name)
	elseif id == 3 then
		showMessage("<N>"..name.." <J>ativou o powerup <ROSE><b>VELOCIDADE!</b>")
		if tfm.get.room.playerList[name].movingRight == true then
			tfm.exec.movePlayer(name,0,0,true,120,0,false)
		else
			tfm.exec.movePlayer(name,0,0,true,-120,0,false)
		end
		tfm.exec.playSound("/transformice/son/chamane2.mp3", 65, nil, nil, name)
	elseif id == 4 then
		showMessage("<N>"..name.." <J>ativou o powerup <ROSE><b>AFUNDAR!</b>")
		timer=1
		tfm.exec.playSound("/transformice/son/bulle2.mp3", 75, nil, nil, name)
	elseif id == 5 then
		showMessage("<N>"..name.." <J>ativou o powerup <ROSE><b>MEEP!</b>")
		tfm.exec.giveMeep(name,true)
		tfm.exec.playSound("/transformice/son/emote.mp3", 75, nil, nil, name)
	elseif id == 6 then
		showMessage("<N>"..name.." <J>ativou o powerup <ROSE><b>SUFOCO!</b>")
		if not tfm.get.room.playerList[name].isShaman then
			data[name].o=data[name].o-35
			if data[name] and data[name].o < 1 then
				data[name].o=1
			end
		end
		tfm.exec.playSound("/cite18/combo2.mp3", 75, nil, nil, name)
	elseif id == 7 then
		showMessage("<N>"..name.." <J>ativou o powerup <ROSE><b>CONGELAR!</b>")
		congelar(name)
	elseif id == 8 then
		showMessage("<N>"..name.." <J>ativou o powerup <ROSE><b>QUEIJO!</b>")
		queijo(name)
	end
	if number == 1 then
		powerups.x1=-1; powerups.y1=-1;
		ui.removeTextArea(100,nil)
	elseif number == 2 then
		powerups.x2=-1; powerups.y2=-1;
		ui.removeTextArea(101,nil)
	elseif number == 3 then
		powerups.x3=-1; powerups.y3=-1;
		ui.removeTextArea(102,nil)
	elseif number == 4 then
		powerups.x4=-1; powerups.y4=-1;
		ui.removeTextArea(103,nil)
	elseif number == 5 then
		powerups.x5=-1; powerups.y5=-1;
		ui.removeTextArea(104,nil)
	end
end
function eventKeyboard(name,key,down)
	if key == 32 and mode == "game" then
		if tfm.get.room.playerList[name].x > powerups.x1-10 and tfm.get.room.playerList[name].x < powerups.x1+34 then
			if tfm.get.room.playerList[name].y > powerups.y1-10 and tfm.get.room.playerList[name].y < powerups.y1+34 then
				activatePowerup(name,math.random(1,8),1)
			end
		end
		if tfm.get.room.playerList[name].x > powerups.x2-10 and tfm.get.room.playerList[name].x < powerups.x2+34 then
			if tfm.get.room.playerList[name].y > powerups.y2-10 and tfm.get.room.playerList[name].y < powerups.y2+34 then
				activatePowerup(name,math.random(1,8),2)
			end
		end
		if tfm.get.room.playerList[name].x > powerups.x3-10 and tfm.get.room.playerList[name].x < powerups.x3+34 then
			if tfm.get.room.playerList[name].y > powerups.y3-10 and tfm.get.room.playerList[name].y < powerups.y3+34 then
				activatePowerup(name,math.random(1,8),3)
			end
		end
		if tfm.get.room.playerList[name].x > powerups.x4-10 and tfm.get.room.playerList[name].x < powerups.x4+34 then
			if tfm.get.room.playerList[name].y > powerups.y4-10 and tfm.get.room.playerList[name].y < powerups.y4+34 then
				activatePowerup(name,math.random(1,8),4)
			end
		end
		if tfm.get.room.playerList[name].x > powerups.x5-10 and tfm.get.room.playerList[name].x < powerups.x5+34 then
			if tfm.get.room.playerList[name].y > powerups.y5-10 and tfm.get.room.playerList[name].y < powerups.y5+34 then
				activatePowerup(name,math.random(1,8),5)
			end
		end
	end
	if key == 37 or key == 38 or key == 39 or key == 40 or key == 65 or key == 68 or key == 83 or key == 87 then
		if shaman == name and data[name].shark >= 1 then
			if data[name] and tfm.get.room.playerList[name].y >= 505 then
				tfm.exec.changePlayerSize(name,0.2)
				if key == 39 or key == 68 then
					tfm.exec.removeImage(data[name].shark_id)
					displayShark(name,data[name].shark,false)
				elseif key == 37 or key == 65 then
					tfm.exec.removeImage(data[name].shark_id)
					displayShark(name,data[name].shark,true)
				end
				if key == 38 or key == 40 or key == 83 or key == 87 then
					if tfm.get.room.playerList[name].movingRight then
						tfm.exec.removeImage(data[name].shark_id)
						displayShark(name,data[name].shark,false)
					else
						tfm.exec.removeImage(data[name].shark_id)
						displayShark(name,data[name].shark,true)
					end
				end
			else
				tfm.exec.changePlayerSize(name,1)
				tfm.exec.removeImage(data[name].shark_id)
			end
		end
	end
end
function eventNewGame()
	xml=tfm.get.room.xmlMapInfo.xml
	ui.addTextArea(0,"",nil,-800,-400,2400,1200,0x6a7495,0x6a7495,1.0,true)
	if changed == true then
		ui.removeTextArea(0,nil)
		z=-1
		cannons=10
		ui.removeTextArea(22,nil)
		alives=0
		mode="hide"
		for n,p in next,tfm.get.room.playerList do
			showWater(n)
			tfm.exec.giveMeep(n,false)
			tfm.exec.removeImage(data[n].shark_id)
			tfm.exec.changePlayerSize(n,1)
			if n:sub(1,1) == "*" then
				tfm.exec.killPlayer(n)
				showMessage("<R>Jogadores convidados não podem jogar este jogo. Logue em uma conta para jogar #watercatch.",name)
				tfm.exec.setPlayerScore(n,-2,false)
			end
			alives=alives+1
			data[n].o=99; data[n].i=0; data[n].t=0; data[n].c=0; data[n].opened=false;
			for i=32,40 do
				tfm.exec.bindKeyboard(n,i,true,true)
			end
			for i=65,87 do
				tfm.exec.bindKeyboard(n,i,true,true)
			end
			if tfm.get.room.playerList[n].isShaman then
				tfm.exec.setShamanMode(n,0)
				tfm.exec.setPlayerScore(n,-1,false)
				if tfm.get.room.isTribeHouse == false then
					tfm.exec.setPlayerSync(n)
				end
				showMessage("<ROSE>Não esqueça de se mover, ou você perderá sua vez de shaman!",n)
				shaman=n
				alives=alives-1
			end
			ui.addTextArea(300,"",n,8,390,782,3,0x202020,0x121212,1.0,true)
			ui.addTextArea(299,"<p align='center'><a href='event:show_menu'><font size='18'>Menu",n,365,25,70,24,0x000001,0x000001,0.75,true)
			ui.removeTextArea(298,n)
		end
		tfm.exec.setGameTime(60)
	end
end
function showMenu(name,color,x,y,width,height,title,content)
	if data[name].opened == false then
		data[name].opened=true
		ui.addTextArea(1004,"",name,-1000,-600,2800,1600,0x000001,0x000001,0.65,true)
		ui.addTextArea(1001,"",name,x+5,y+5,width,height,color,color,0.95,true)
		ui.addTextArea(1000,"<font size='13'><i><br><br>"..content.."",name,x,y,width,height,0x151515,color,0.95,true)
		ui.addTextArea(1002,"<font color='#f8d802'><font size='14'><p align='center'><i><b>"..title.."",name,x+5,y+5,width-10,20,0x101010,0x101010,0.95,true)
		ui.addTextArea(1003,"<font color='#ff2300'><font size='14'><b><a href='event:close'>X</a>",name,x+width-25,y+5,width-10,20,0,0,0.95,true)
	end
end
function genPowerup(pos,type,x,y)
	if pos == 1 then
		ui.addTextArea(100,"<font size='18'><font color='#010101'><p align='center'>?",nil,x,y,22,22,0xd0d0d0,0x808080,1.0,false)
		powerups.x1=x; powerups.y1=y; powerups.t1=type;
	elseif pos == 2 then
		ui.addTextArea(101,"<font size='18'><font color='#010101'><p align='center'>?",nil,x,y,22,22,0xd0d0d0,0x808080,1.0,false)
		powerups.x2=x; powerups.y2=y; powerups.t2=type;
	elseif pos == 3 then
		ui.addTextArea(102,"<font size='18'><font color='#010101'><p align='center'>?",nil,x,y,22,22,0xd0d0d0,0x808080,1.0,false)
		powerups.x3=x; powerups.y3=y; powerups.t3=type;
	elseif pos == 4 then
		ui.addTextArea(103,"<font size='18'><font color='#010101'><p align='center'>?",nil,x,y,22,22,0xd0d0d0,0x808080,1.0,false)
		powerups.x4=x; powerups.y4=y; powerups.t4=type;
	elseif pos == 5 then
		ui.addTextArea(104,"<font size='18'><font color='#010101'><p align='center'>?",nil,x,y,22,22,0xd0d0d0,0x808080,1.0,false)
		powerups.x5=x; powerups.y5=y; powerups.t5=type;
	end
end
function congelar(name)
	tfm.exec.freezePlayer(name,true)
	data[name].t=6
	tfm.exec.playSound("/transformice/son/gel.mp3", 75, nil, nil, name)
end
function queijo(name)
	tfm.exec.giveCheese(name)
	data[name].t=8
end
function dropPlayer(name)
	tfm.exec.addShamanObject(10,tfm.get.room.playerList[name].x,tfm.get.room.playerList[name].y,0,0,0,true)
	data[name].i=tfm.exec.addShamanObject(68,tfm.get.room.playerList[name].x,tfm.get.room.playerList[name].y,0,0,0,false)
	data[name].t=6
	tfm.exec.playSound("/transformice/son/tp.mp3", 70, nil, nil, name)
end
function eventLoop(p,r)
	loop=loop+0.5
	time_passed=math.ceil(p/500)
	time_remain=math.ceil(r/500)
	if time_passed >= 12 and tfm.get.room.currentMap == "@7925247" then
		tfm.exec.disableAutoShaman(false)
		resetMap()
	end
	if changed == true then
		ui.setMapName("<font color='#0080ff'><b>#watercatch!</b><N> Versão <VP><b>v4.3.0</b><N> - criado por <ROSE><b>Morganadxana#0000</b><")
		local m=math.floor(r/60000)
		local s=math.floor((((m*60000)-r) * -1) / 1000)
		ui.addTextArea(-1,"<font size='44'><font color='#222222'><font face='Copperplate Gothic Bold,Times New Roman'><b>"..m..":"..s.."</b>",n,557,27,125,54,0,0,1.0,true)
		ui.addTextArea(-2,"<font size='44'><font color='#d0d0d0'><font face='Copperplate Gothic Bold,Times New Roman'><b>"..m..":"..s.."</b>",n,554,24,125,54,0,0,1.0,true)
		if s < 10 then
			ui.addTextArea(-1,"<font size='44'><font face='Copperplate Gothic Bold,Times New Roman'><font color='#222222'><b>"..m..":0"..s.."</b>",n,557,27,125,54,0,0,1.0,true)
			ui.addTextArea(-2,"<font size='44'><font color='#d0d0d0'><font face='Copperplate Gothic Bold,Times New Roman'><b>"..m..":0"..s.."</b>",n,554,24,125,54,0,0,1.0,true)
		end
		if mode == "game" then
			if loop >= 24 then
				if time_passed >= 120 then
					for i=1,5 do
						genPowerup(i,math.random(1,9),math.random(100,4700),math.random(600,1800))
					end
					loop=0
					tfm.exec.playSound("/transformice/son/invoc.mp3", 40, nil, nil, nil)
				end
			end
			if time_remain == 120 then
				showMessage("<ROSE>Restam 60 segundos!")
			end
			if time_remain == 60 then
				showMessage("<ROSE>Restam 30 segundos!")
			end
		end
		if mode == "game" or mode == "hide" then
			ui.addTextArea(31,"<font size='44'><font color='#222222'><font face='Copperplate Gothic Bold,Times New Roman'><b>"..alives.."</b>",n,135,27,80,54,0,0,1.0,true)
			ui.addTextArea(30,"<font size='44'><font color='#d0d0d0'><font face='Copperplate Gothic Bold,Times New Roman'><b>"..alives.."</b>",n,132,24,80,54,0,0,1.0,true)
			if timer > 0 then
				timer=timer-0.5
				tfm.exec.setWorldGravity(0,21)
			elseif timer == 0 then
				tfm.exec.setWorldGravity(0,10.5)
			end
			for n,q in next,tfm.get.room.playerList do
				if not tfm.get.room.playerList[n].isShaman then
					if not tfm.get.room.playerList[n].isDead then
						if mode == "game" or mode == "hide" then
							if tfm.get.room.playerList[n].y < 498 then
								if data[n].o < 99 then
									data[n].o=data[n].o+1
								end
							data[n].y=0
						else
							if checkOxygenZones(n) == true then
								data[n].o=data[n].o-0.2
							else
								tfm.exec.playSound("/transformice/son/bulle2.mp3", 6, nil, nil, n)
								if tfm.get.room.playerList[n].y <= 1625 then
									data[n].o=data[n].o-0.5
									data[n].c=0
									elseif tfm.get.room.playerList[n].y > 1625 then
										data[n].o=data[n].o-0.7
										data[n].c=0
									end
								end
							end
						end
					end
				end
			end
		else
			for i=-6,104 do
				ui.removeTextArea(i,nil)
			end
		end
		for n,q in next,tfm.get.room.playerList do
			if data[n] then
				if data[n].imaget >= 0 then
					data[n].imaget=data[n].imaget-0.5
				end
				if data[n].imaget == 0 then
					tfm.exec.removeImage(data[n].imageid)
				end
				data[n].x=tfm.get.room.playerList[n].x
				data[n].yp=tfm.get.room.playerList[n].y
				if mode == "game" then
					if q.x >= data[shaman].x - 60 and q.x <= data[shaman].x + 60 then
						if q.y >= data[shaman].yp - 60 and q.y <= data[shaman].yp + 60 then
							if not tfm.get.room.playerList[n].isShaman then
								tfm.exec.killPlayer(n)
								tfm.exec.playSound("/deadmaze/monstres/m_4/attaque1.mp3", 90, nil, nil, n)
								tfm.exec.playSound("/deadmaze/monstres/m_4/touche_0.mp3", 60, nil, nil, shaman)
							end
						end
					end
					if data[n].t > 0 then
						data[n].t=data[n].t-0.5
						if data[n].t <= 0 then
							tfm.exec.removeObject(data[n].i)
							tfm.exec.freezePlayer(n,false)
							tfm.exec.removeCheese(n)
						end
					end
					if not tfm.get.room.playerList[n].isDead then
						if data[n].o <= 0 then
							tfm.exec.playSound("/deadmaze/monstres/mort/mf0.mp3", 80, nil, nil, n)
							tfm.exec.killPlayer(n)
							showMessage("<R>O jogador <b>"..n.."</b> morreu afogado!")
							tfm.exec.addShamanObject(85, tfm.get.room.playerList[n].x, tfm.get.room.playerList[n].y, 0, 0.1, 0.1, false)
						end
					end
				end
				if mode == "game" or mode == "hide" then
					if data[n].o > 30 then
						ui.addTextArea(10,"",n,8,390,(data[n].o*7.9),3,0xf0f0f0,0x808080,1.0,true)
						data[n].d=0
						tfm.exec.setNameColor(n,0xc2c2da)
					elseif data[n].o > 0 then
						tfm.exec.playSound("/transformice/son/bulle3.mp3", 30, nil, nil, n)
						ui.addTextArea(10,"",n,8,390,(data[n].o*7.9),3,0x801500,0xa01000,1.0,true)
						data[n].d=data[n].d+1
						tfm.exec.setNameColor(n,0xff4500)
						if data[n].d == 1 and data[n].o > 0 and tfm.get.room.playerList[n].y >= 498 then
							tfm.exec.playSound("/deadmaze/monstres/mort/mh0.mp3", 35+(30-math.floor(data[n].o)), nil, nil, n)
							showMessage("<R>Você está ficando sem oxigênio! Saia da água o mais rápido possível ou você morrerá afogado!",n)
						end
						if data[n].d > 10 then
							data[n].d=0
						end
					end
				else
					ui.removeTextArea(10,nil)
					ui.removeTextArea(300,nil)
				end
			end
		end
		if r <= 1500 and mode == "hide" then
			mode="game"
			tfm.exec.setGameTime(240)
			ui.removeTextArea(22,nil)
			showMessage("<J><b>O shaman foi liberado! Salvem-se quem puder!</b><br><br><ROSE>Use o comando !tc [mensagem] para falar no chat sem que o shaman saiba.<br><br><VP>As áreas marcadas por preto e amarelo são zonas de oxigênio. Fique nelas para ter seu consumo de oxigênio reduzido.")
			moveShaman()
			for n,p in next,tfm.get.room.playerList do
				ui.addTextArea(300,"",n,8,390,782,3,0x202020,0x121212,1.0,true)
				tfm.exec.playSound("cite18/squelette-spawn.mp3", 80, nil, nil, n)
			end
		end
		if r <= 1000 and mode == "game" then
			tfm.exec.setGameTime(15)
			mode="end"
			local lives=0
			for n,p in next,tfm.get.room.playerList do
				if not tfm.get.room.playerList[n].isShaman and not tfm.get.room.playerList[n].isDead then
					lives=lives+1
					tfm.exec.giveCheese(n)
					tfm.exec.playerVictory(n)
				end
				ui.removeTextArea(300,n)
			end
			showMessage("<VP>Tempo esgotado! <b>"..lives.."</b> ratos sobreviveram! Iniciando nova partida...")
		end
		if time_remain <= 0 and mode == "end" then
			resetMap()
		end
	else
		if time_passed >= 10 and changed == false and mode == "load" then
			tfm.exec.disableAutoShaman(false)
			resetMap()
			changed=true
			mode="hide"
		end
	end
end
function eventTextAreaCallback(id,name,callback)
	if callback == "show_menu" then
		ui.addTextArea(299,"<p align='center'><a href='event:hide_menu'><font size='18'>Menu",name,365,25,70,24,0x000001,0x000001,0.75,true)
		ui.addTextArea(298,"<p align='center'><a href='event:help'>Ajuda</a><br><a href='event:powerups'>Powerups</a><br><a href='event:cred'>Créditos</a><br><a href='event:change'>Changelog</a><br><a href='event:skins'>Skins</a>",name,355,55,90,75,0x000001,0x000001,0.80,true)
	end
	if callback == "hide_menu" then
		ui.addTextArea(299,"<p align='center'><a href='event:show_menu'><font size='18'>Menu",name,365,25,70,24,0x000001,0x000001,0.75,true)
		ui.removeTextArea(298,name)
	end
	if callback == "close" then
		for _,i in next,{1000,1001,1002,1003,1004,1005,1006,1007,1008} do
			ui.removeTextArea(i,name)
		end
		data[name].opened=false
		removeImagePlayers(name)
	end
	if callback == "help" then
		eventChatCommand(name,"help")
	end
	if callback == "powerups" then
		eventChatCommand(name,"powerups")
	end
	if callback == "cred" then
		eventChatCommand(name,"creditos")
	end
	if callback == "change" then
		eventChatCommand(name,"changelog")
	end
	if callback == "skins" then
		eventChatCommand(name,"skins")
	end
	if callback == "a0" then
		data[name].shark=0
		tfm.exec.removeImage(data[name].shark_id)
		showMessage("<N>Você desativou as skins de tubarão.",name)
		tfm.exec.changePlayerSize(name,1)
	end
	if callback == "a1" then
		data[name].shark=1
		showMessage("<VP>Você está agora usando a skin <b>Tubarão Normal 1.</b>",name)
	end
	if callback == "a2" then
		data[name].shark=2
		showMessage("<VP>Você está agora usando a skin <b>Tubarão Normal 2.</b>",name)
	end
	if callback == "a3" then
		data[name].shark=3
		showMessage("<VP>Você está agora usando a skin <b>Tubarão Normal 3.</b>",name)
	end
	if callback == "a4" then
		data[name].shark=4
		showMessage("<VP>Você está agora usando a skin <b>Tubarão-Branco 1.</b>",name)
	end
	if callback == "a5" then
		data[name].shark=5
		showMessage("<VP>Você está agora usando a skin <b>Tubarão-Martelo.</b>",name)
	end
	if callback == "a6" then
		data[name].shark=6
		showMessage("<VP>Você está agora usando a skin <b>Tubarão Normal 4.</b>",name)
	end
	if callback == "a7" then
		data[name].shark=7
		showMessage("<VP>Você está agora usando a skin <b>Tubarão-Branco 2.</b>",name)
	end
	if callback == "a8" then
		data[name].shark=8
		showMessage("<VP>Você está agora usando a skin <b>Barracuda.</b>",name)
	end
	if callback == "a9" then
		data[name].shark=9
		showMessage("<VP>Você está agora usando a skin <b>Peixe Diabo-Negro.</b>",name)
	end
	if callback == "a10" then
		data[name].shark=10
		showMessage("<VP>Você está agora usando a skin <b>Baleia.</b>",name)
	end
	if callback == "a11" then
		data[name].shark=11
		showMessage("<VP>Você está agora usando a skin <b>Tubarão-Tigre.</b>",name)
	end
end
resetMap()
end

initMountain = function()
for _,f in next,{"AutoNewGame","AutoTimeLeft","AfkDeath","AutoShaman","AutoScore","DebugCommand","PhysicalConsumables"} do
	tfm.exec["disable"..f](true)
end
for _,g in next,{"help","powerups","creditos","changelog"} do
	system.disableChatCommandDisplay(g)
end
number_scale={8240,7400,6760,6230,5760,5350,4970,4620,4260,4000,3693,3417,3175,2900,2650,2390,2180,1950,1750,1550,1360,1150,935,770}
data={}; lang={}; loop=0; map_count=0; event_selected=0; running=false; pass_int=0; falt_int=0; run_int=0; event_int=0; endgame=false; changed=false; vencedor="";
map="@7901662"; xml2=''
ground={type = 12,width = 10,height = 210,foregound = 1,friction = 0.0,restitution = 1.0,angle = 0,color = 0xffffff,miceCollision = true,groundCollision = true,dynamic = false}
powerups={wind=false,meteor=false,gravity=false,cheese=false}
events_pt={"Fúria da Tormenta","Chuva de Meteoros","Anomalia Gravitacional","Queijo para Todos"}
events_en={"Wind Fury","Meteor Rain","Gravity Anomaly","Cheese for All"}
power_d={p2={6,8,10,12},p3={12,14,16,18,20,22}}
lang.br = {
	mapname = "<N><b>#mountain</b>  <V>-  <N>versão <ROSE>v1.1.2   <G>|   <N>Desenvolvido por <J>Morganadxana#0000<",
	enter = "<N>Bem-vindo ao module <J><b>#mountain!</b><br><N>Você tem 3 minutos para escalar a grande montanha que há pelo caminho!<br><br><ROSE>Versão v1.1.2 - desenvolvido por Morganadxana#0000<br><VP>O module foi atualizado! Para descobrir as novidades, digite !changelog.",
	newgame = "<N>Caso não saiba o que fazer neste module, digite <b>!help</b>.",
	getready = "<J>Se prepare! A estrada para a montanha será liberada em breve!",
	start = "<VP><b>E que comece a batalha!</b>",
	event1 = "O evento",
	event2 = "será iniciado em instantes, e terá duração de ",
	event3 = "segundos!",
	event4 = " começou! Salve-se quem puder!",
	t10secs = "<font color='#ff8000'>Restam apenas 10 segundos! Apenas o rato que estiver mais alto sobreviverá!",
	winner = "é o grande vencedor!",
	scaled = "Ele(a) subiu ",
	recognized = "metros e agora é reconhecido pelos deuses da montanha!",
	event5 = " foi encerrado!",
	reached2 = "<G>Você atingiu os 2000 metros de altura.<br>Ventos bem gelados começam a te rodear e você começa a sentir falta de ar.",
	reached3 = "<G>Você atingiu os 5000 metros de altura.<br>Já está impossível de suportar o extremo frio, e você começa a ter sérias dificuldades para respirar.",
	reached4 = "<G>Você atingiu os 10000 metros de altura.<br>As correntes geladas começam a te fazer congelar, e seu rato passa a ter um sério problema de asfixia devido a falta de ar.",
	reached5 = "<G>Você atingiu os 20000 metros de altura.<br>Você começa a ver as estrelas muito mais claramente, mesmo no dia claro. No entanto, isto é um péssimo sinal. O ar rarefeito e as baixíssimas temperaturas fazem seu rato morrer aos poucos.",
	reached6 = "<VP>Você chegou no pico da montanha! Os deuses reconheceram sua bravura e coragem e te acolheram para o céu!",
	reached7 = " <VP>chegou até o topo da montanha!<br><N>Ele(a) agora se integra nas estrelas e passa a brilhar como nunca!",
	nowinners = "<R>Não há vencedores!",
	help = "<p align='center'><VP><b>Bem-vindo ao module #mountain.</b><br><br><p align='left'><N>Este modo é bem simples. O objetivo é subir o máximo possível a grande montanha que há pela frente.<br><br>No entanto, os deuses da montanha estão furiosos, e podem atacar com vários contratempos.<br><br>A partida acaba depois de 3 minutos, quando todos os ratos morrem ou quando alguém chega no pico da montanha.<br><br><ROSE>Quaisquer bugs ou problemas reporte para Morganadxana#0000.",
	powerups = "<G>• Fúria da Tormenta: <N>Correntes de vento começam a pairar em volta da montanha.<br><G>• Chuva de Meteoros: <N>Meteoros começam a cair do céu, fazendo com que você caia.<br><G>• Anomalia Gravitacional: <N>Um campo gravítico intenso aparece na montanha, alterando de forma aleatória a gravidade do mapa.<br><G>• Queijo para Todos: <N>Todos os jogadores recebem queijo.",
	credits = "As seguintes pessoas ajudaram no desenvolvimento deste module:<br><br><ROSE><b>• Morganadxana#0000</b><N> - Desenvolvedora do código e criadora do mapa<br><ROSE><b>• Rakan_raster#0000</b><N> - Tradução do código para o Inglês<br><ROSE><b>• Spectra_phantom#6089</b><N> - Criação das artes",
	memory_error = "<R>Aviso: Não há mais memória disponível para o Transformice. Para continuar jogando este module, saia do jogo e entre novamente.",
	juliahenderson = "Você não me acha linda?",
	andersondarther = "Não ligue para ela. Sempre gosta de se exibir com seus visuais...<br><br>Agora falando sério, os deuses escondem um segredo gigante nesta montanha. Poderes extremamente fortes estão presentes no topo dela.<br><br>No entanto, não se empolgue. Os mesmos deuses estão muito furiosos ultimamente, e não querem que ninguém suba...",
	mylenneganditz = "Ei, você! Fique comigo, preciso de amigos!",
	lyncdowryammer = "Sinto na pele a desgraça que ela passou. Perdeu todos os seus amigos durante uma chuva de meteoros...<br><br>Agora falando sério, os deuses escondem um segredo gigante nesta montanha. Poderes extremamente fortes estão presentes no topo dela.<br><br>No entanto, não se empolgue. Os mesmos deuses estão muito furiosos ultimamente, e não querem que ninguém suba..."
}
lang.en = {
	mapname = "<N><b>#mountain</b>  <V>-  <N>version <ROSE>v1.1.2   <G>|   <N>Developed by <J>Morganadxana#0000<",
	enter = "<N>Welcome to the <J><b>#mountain</b> module!<br><N>You have 3 minutes to scale the big mountain that is on your way!<br><ROSE>Version v1.1.2 - developed by Morganadxana#0000<br><V>Translation by Rakan_raster#0000<br><VP>If you want to see the latest updates, type !changelog.",
	newgame = "<N>If you don't know about this module, please type <b>!help</b>.",
	getready = "<J>Get ready! The road to the mountain will be opened!",
	start = "<VP><b>Go!</b>",
	event1 = "The event",
	event2 = "will start in a few seconds, and will last for ",
	event3 = "seconds!",
	event4 = " started!",
	t10secs = "<font color='#ff8000'>10 seconds remaining! The player that scaled more will survive!",
	winner = "is the winner!",
	scaled = "(S)he scaled ",
	recognized = "meters and now is recognized by the mountain gods!",
	event5 = " is gone!",
	reached2 = "<G>You reached 2000 meters of height.<br>The cold wings starts to surround you, and the air starts to be rarefied...",
	reached3 = "<G>You reached 5000 meters of height.<br>It's almost impossible to tolerate the extreme cold temperatures, and you starts to have serious difficulties to breathe correctly.",
	reached4 = "<G>You reached 10000 meters of height.<br>The strong cold wings starts to freeze you, and your mice starts to have serious suffocation problems because of lack of air...",
	reached5 = "<G>You reached 20000 meters of height.<br>You starts to see the stars with much more clarity, even on the clear day. However, the rarified air and the extremely low temperatures is making your mice to die.",
	reached6 = "<VP>You reached the peak of the mountain! The gods recognized your bravery and courage. Now, you is part of the heaven!",
	reached7 = " <VP>reached the top of the mountain!<br><N>(S)he now is part of the stars and will bright many more!",
	nowinners = "<R>No winners!",
	help = "<p align='center'><VP><b>Welcome to the #mountain module.</b><br><br><p align='left'><N>This game is very simple. The objective is scale the big mountain that is in front of you.<br><br>However, the mountain gods are furious, and can attack you with various events.<br><br>The match will end after 3 minutes, when there is no more alive mices or when someone reaches the top of the mountain.<br><br><ROSE>Bugs and problems? Report to Morganadxana#0000.",
	powerups = "<G>• Wind Fury: <N>Strong winds hover around the mountain.<br><G>• Meteor Rain: <N>Some meteors will fall from the heaven, making you go down.<br><G>• Gravity Anomaly: <N>A strong gravitational field appears on the mountain, randomly changing the gravity of the map.<br><G>• Cheese For All: <N>All the players will have cheese.",
	credits = "The following players helped on this module:<br><br><ROSE><b>• Morganadxana#0000</b><N> - Code developer and creator of the map<br><ROSE><b>• Akwimos#1937</b><N> - English translation<br><ROSE><b>• Spectra_phantom#6089</b><N> - Image creation",
	memory_error = "<R>Warning: There's no more available memory for Transformice. To continue playing this game, log out of your account and enter again.",
	juliahenderson = "You don't think that I'm beautiful?",
	andersondarther = "Don't be fooled by her. She always likes to show off...<br><br>Talking serious, the mountain gods are hiding a very powerful secret. Extremely powerful things are present on the peak of the mountain.<br><br>However, don't get carried. The same gods are very furious recently. They like that nobody scale the mountain...",
	mylenneganditz = "Hey! Stay with me! I need of friends!",
	lyncdowryammer = "I'm sorry about what happened. She lost all of your friends during a meteor rain...<br><br>However, don't get carried. The same gods are very furious recently. They like that nobody scale the mountain..."
}
if tfm.get.room.community == "br" or tfm.get.room.community == "pt" then
	text = lang.br
else
	text = lang.en
end
function showMessage(message,name)
	temp_text=string.gsub(message,"<b>","")
	temp_text=string.gsub(temp_text,"</b>","")
	if tfm.get.room.isTribeHouse == false then
		tfm.exec.chatMessage(message,name)
	elseif tfm.get.room.isTribeHouse == true then
		print(temp_text)
	end
end
function showMenu(name,color,x,y,width,height,title,content)
	if data[name].opened == false then
		data[name].opened=true
		ui.addTextArea(1004,"",name,-1000,-600,2800,1600,0x000001,0x000001,0.65,true)
		ui.addTextArea(1001,"",name,x+5,y+5,width,height,color,color,0.95,true)
		ui.addTextArea(1000,"<font size='13'><i><br><br>"..content.."",name,x,y,width,height,0x151515,color,0.95,true)
		ui.addTextArea(1002,"<font color='#f8d802'><font size='14'><p align='center'><i><b>"..title.."",name,x+5,y+5,width-10,22,0x101010,0x101010,0.95,true)
		ui.addTextArea(1003,"<font color='#ff2300'><font size='14'><b><a href='event:close'>X</a>",name,x+width-25,y+5,width-10,20,0,0,0.95,true)
	end
end
function defineVencedor()
	max_score=10800
	winner=""
	for name,player in next,tfm.get.room.playerList do
		if tfm.get.room.playerList[name].y < max_score and data[name].enabled == true then
			winner=name
			max_score=tfm.get.room.playerList[name].y
		end
	end
	return winner
end
function showImages(name)
	for a=1,2 do tfm.exec.addImage("182d6e2305b.png","?1",math.random(1300,4700),math.random(-450,1000),name) end
	for b=1,2 do tfm.exec.addImage("182d6e2305b.png","?1",math.random(1300,4700),math.random(-450,1000),name,-1,1) end
	for c=1,3 do tfm.exec.addImage("182d6e1e45c.png","?1",math.random(1300,4700),math.random(-450,1000),name) end
	for d=1,3 do tfm.exec.addImage("182d6e1e45c.png","?1",math.random(1300,4700),math.random(-450,1000),name,-1,1) end
	for e=1,12 do tfm.exec.addImage("182d6e197bb.png","?1",math.random(1300,4700),math.random(-250,1200),name) end
	for k=0,6 do
		tfm.exec.addImage("181ba85ccc2.png","!1",math.random(1700,4300),math.random(4500,8600),name)
	end
	for l=0,6 do
		tfm.exec.addImage("181ba86195e.png","!1",math.random(1700,4300),math.random(4500,8600),name)
	end
	for m=0,6 do
		tfm.exec.addImage("181ba86655c.png","!1",math.random(1700,4300),math.random(4500,8600),name)
	end
	for n=0,6 do
		tfm.exec.addImage("181ba86b15a.png","!1",math.random(1700,4300),math.random(4500,8600),name)
	end
	for j=0,5 do
		tfm.exec.addImage("181b9de5c95.png","?1",-800+(1920*j),-1240,name)
		tfm.exec.addImage("181b9de5c95.png","?1",-800+(1920*j),-160,name)
		tfm.exec.addImage("181b9de5c95.png","?1",-800+(1920*j),920,name)
	end
	for i=0,1 do
		tfm.exec.addImage("17fe373d035.jpg","?1",-400+(i*3400),9592,name,1,1)
	end
	tfm.exec.addImage("17fe3741e5f.jpg","?1",-400,800,name,10,10,0,1)
end
function resetEvents()
	wind=false; meteor=false; gravity=false; cheese=false;
	run_int=0;
	for name,player in next,tfm.get.room.playerList do
		tfm.exec.removeCheese(name)
	end
	tfm.exec.setWorldGravity(0,10)
end
function eventChatCommand(name,command)
	if command == "help" then
		showMenu(name,0x808080,150,120,500,250,"Help",text.help)
	end
	if command == "powerups" then
		showMenu(name,0xf2a267,150,120,500,160,"Powerups",text.powerups)
	end
	if command == "creditos" then
		showMenu(name,0xb6e980,140,90,520,130,"Credits",text.credits)
	end
	if command == "changelog" then
		showMenu(name,0x2578f6,140,70,520,260,"Changelog","<font size='11'>[v1.1.2]:<br>• Addiction of new NPC<br><br>[v1.1.1]:<br>• Addiction of various decorations on the map<br><br>[v1.1.0]:<br>• Added cloud images<br>• Some modifications on the map<br><br>[v1.0.9]:<br>• Some modifications on the map<br><br>[v1.0.8]:<br>• Various modifications on the map<br>• Increased the game time by 20 seconds")
	end
end
function eventNewPlayer(name)
	showMessage(text.enter,name)
	ui.setMapName(text.mapname)
	newData={
		["x"]=0; ["a"]=0; ["enabled"]=false; ["opened"]=false; }
	data[name]=newData;
	showImages(name)
	ui.addTextArea(299,"<p align='center'><a href='event:show_menu'><font size='18'>Menu",n,365,25,70,24,0x000001,0x000001,0.75,true)
end
for name,player in next,tfm.get.room.playerList do
	eventNewPlayer(name)
	tfm.exec.setPlayerScore(name,0,false)
end
function eventPlayerDied(name)
	data[name].enabled=false
	if changed == true then
	local i=0
	local n
	for pname,player in pairs(tfm.get.room.playerList) do
		if not player.isDead then
			i=i+1
			n=pname
		end
	end
	if i==0 then
		showMessage(text.nowinners)
		tfm.exec.setGameTime(15)
		endgame=true; running=false;
		tfm.exec.newGame(xml2,false)
	end
	end
end
function eventTalkToNPC(name, npc)
	if npc == "Julia Henderson" then
		showMessage("<V>[Julia Henderson] <N>"..text.juliahenderson.."",name)
	elseif npc == "Anderson Darther" then
		showMessage("<V>[Anderson Darther] <N>"..text.andersondarther.."",name)
	elseif npc == "Mylenne Ganditz" then
		showMessage("<V>[Mylenne Ganditz] <N>"..text.mylenneganditz.."",name)
	elseif npc == "Lync Dowryammer" then
		showMessage("<V>[Lync Dowryammer] <N>"..text.lyncdowryammer.."",name)
	elseif npc == "Mayra Flowers" then
		showMessage("<V>[Mayra Flowers] <N>Muuuuuuuu! <font face='Segoe UI Symbol'>(●'◡'●)<font face='Verdana'>",name)
	end
end
function eventTextAreaCallback(id,name,callback)
	if callback == "show_menu" then
		ui.addTextArea(299,"<p align='center'><a href='event:hide_menu'><font size='18'>Menu",name,365,25,70,24,0x000001,0x000001,0.75,true)
		ui.addTextArea(298,"<p align='center'><a href='event:help'>Ajuda</a><br><a href='event:powerups'>Powerups</a><br><a href='event:cred'>Créditos</a><br><a href='event:change'>Changelog</a>",name,355,57,90,60,0x000001,0x000001,0.80,true)
	end
	if callback == "hide_menu" then
		ui.addTextArea(299,"<p align='center'><a href='event:show_menu'><font size='18'>Menu",name,365,25,70,24,0x000001,0x000001,0.75,true)
		ui.removeTextArea(298,name)
	end
	if callback == "close" then
		for i=1000,1004 do
			ui.removeTextArea(i,name)
		end
		data[name].opened=false
	end
	if callback == "help" then
		eventChatCommand(name,"help")
	end
	if callback == "powerups" then
		eventChatCommand(name,"powerups")
	end
	if callback == "cred" then
		eventChatCommand(name,"creditos")
	end
	if callback == "change" then
		eventChatCommand(name,"changelog")
	end
end
function eventNewGame()
	ui.setBackgroundColor("#000000")
	if changed == true then
		resetEvents()
		running=false; map_count=map_count+1; run_int=0; pass_int=0; event_int=0; endgame=false; vencedor="";
		tfm.exec.setGameTime(246)
		for i=0,1 do
			tfm.exec.addPhysicObject(i, 180+(i*5680), 10475, ground)
		end
		for name,player in next,tfm.get.room.playerList do
			data[name].a=0;
			data[name].enabled=true;
			showImages(name)
			ui.setMapName(text.mapname)
		end
		showMessage(text.newgame)
		for i=1,24 do
			ui.addTextArea(i,"<p align='center'>"..tostring(i*1000).."",nil,2980,number_scale[i],40,16,0x010101,0x010101,1.0,false)
		end
		tfm.exec.addNPC("Anderson Darther",{title = 298, look = "1;123_125508,0,0,4,60_324716+316441+4b926d+900f31+20310+ece674+e47c39+8d2637+900f31+900f31,40_256c23+717a30,31_ef4a6+f3f9bc,0,47",x = 4680,y = 10550,female = false,lookLeft = false,lookAtPlayer = true,interactive = true})
		tfm.exec.addNPC("Lync Dowryammer",{title = 253, look = "176;40_7b00c8+70335,0,20_9d00ff,43_290448,29_729be0+1d0241,0,1_5c00cb+211ce0,0,0",x = 1700,y = 10320,female = false,lookLeft = true,lookAtPlayer = true,interactive = true})
		tfm.exec.addNPC("Mylenne Ganditz",{title = 244, look = "161;212,38,57,66,62,0,33,0,0",x = 2430,y = 9368,female = true,lookLeft = true,lookAtPlayer = true,interactive = true})
		tfm.exec.addNPC("Julia Henderson",{title = 125, look = "142;234,49_efa5e2+edf1f2+edf1f2+edf1f2,77,0,43,97,3,0,0",x = 3505,y = 9188,female = true,lookLeft = false,lookAtPlayer = true,interactive = true})
		tfm.exec.addNPC("Mayra Flowers",{title = 1, look = "112;0,4,0,74_212121+d2d2d2,39,39,44,0,1",x = 3000,y = 6176,female = true,lookLeft = true,lookAtPlayer = true,interactive = true},name)
	else
		tfm.exec.setGameTime(5)
		if changed == false then
			xml2=tfm.get.room.xmlMapInfo.xml
			ui.addTextArea(0,"",nil,-800,-400,2400,1200,0x6a7495,0x6a7495,1.0,true)
			ui.setMapName("<J>Loading map. Please wait...<")
		else
			ui.removeTextArea(0,nil)
		end
	end
end
function eventLoop(passado,faltando)
	pass_int=pass_int+1
	falt_int=math.floor(faltando/500)
	if changed == true then
	if pass_int == 14 then
		showMessage(text.getready)
	elseif pass_int == 28 then
		showMessage("<BL><b>3...</b>")
		for name,player in next,tfm.get.room.playerList do
			if tfm.get.room.playerList[name].y <= 400 and not tfm.get.room.playerList[name].isDead then
				tfm.exec.killPlayer(name)
				data[name].enabled=false
				showMessage(text.memory_error,name)
			end
		end
	elseif pass_int == 30 then
		showMessage("<BL><b>2...</b>")
	elseif pass_int == 32 then
		showMessage("<BL><b>1...</b>")
	elseif pass_int == 34 then
		showMessage(text.start)
		for i=0,1 do
			tfm.exec.removePhysicObject(i)
		end	
		running=true
	end
	if running == true then
		if wind == true then
			for i=1,24 do
				x=math.random(2800,3200)
				y=math.random(2000,10000)
				tfm.exec.explosion(x, y, -8, 100, true)
				tfm.exec.displayParticle(math.random(26,27), x, y, 1, 1, 1, 1)
			end
		end
		if meteor == true then
			loop=loop+1
			if loop == 4 then
				for i=1,2 do
					x=math.random(2600,3400)
					tfm.exec.addShamanObject(85, x, 0, 0, 0, 0, false)
				end
				loop=0
			end
		end
		if gravity == true then
			loop=loop+1
			if loop == 4 then
				tfm.exec.setWorldGravity(0,math.random(10,15))
				loop=0
			end
		end
		if cheese == true then
			for name,player in next,tfm.get.room.playerList do
				tfm.exec.giveCheese(name)
			end
		end
		run_int=run_int+0.5
		if run_int == 28 and falt_int >= 48 then
			event_selected=math.random(1,4)
			if event_selected == 2 then
				event_int=power_d.p2[math.random(#power_d.p2)]
			elseif event_selected == 3 then
				event_int=power_d.p3[math.random(#power_d.p3)]
			else
				event_int=math.random(12,24)
			end
			if tfm.get.room.community == "br" or tfm.get.room.community == "pt" then
				showMessage("<VP>"..text.event1.." <V><b>"..events_pt[event_selected].."</b> <VP>"..text.event2.."<J><b>"..event_int.."</b> <VP>"..text.event3.."")
			else
				showMessage("<VP>"..text.event1.." <V><b>"..events_en[event_selected].."</b> <VP>"..text.event2.."<J><b>"..event_int.."</b> <VP>"..text.event3.."")
			end
		end
		if run_int == 33 and falt_int >= 48 then
			if tfm.get.room.community == "br" or tfm.get.room.community == "pt" then
				showMessage("<VP>"..text.event1.." <V><b>"..events_pt[event_selected].."</b><VP>"..text.event4.."")
			else
				showMessage("<VP>"..text.event1.." <V><b>"..events_en[event_selected].."</b><VP>"..text.event4.."")
			end
			if event_selected == 1 then
				wind=true
			elseif event_selected == 2 then
				meteor=true
			elseif event_selected == 3 then
				gravity=true
			elseif event_selected == 4 then
				cheese=true
			end
		end
		if falt_int == 20 and endgame == false then
			showMessage(text.t10secs)
		end
		if falt_int <= 2 and endgame == false then
			while vencedor == "" do
				vencedor = defineVencedor()
			end
			for name,player in next,tfm.get.room.playerList do
				if not name == vencedor then
					tfm.exec.killPlayer(name)
				end
			end
			tfm.exec.giveCheese(vencedor)
			tfm.exec.playerVictory(vencedor)
			tfm.exec.setPlayerScore(vencedor,data[vencedor].a,true)
			showMessage("<VP><V><b>"..vencedor.."</b> <VP>"..text.winner.."<br><N>"..text.scaled.."<V>"..math.floor(math.pow((tfm.get.room.playerList[vencedor].y/-1+10565)/100,2.2)).." <N>"..text.recognized.."")
			tfm.exec.setGameTime(15)
			falt_int=15
			endgame=true
		end
		if falt_int <= 1 and endgame == true then
			tfm.exec.newGame(xml2,false)
		end
		if wind == true or meteor == true or gravity == true or cheese == true then
			event_int=event_int-0.5
			if event_int == 0 then
				resetEvents()
				if tfm.get.room.community == "br" or tfm.get.room.community == "pt" then
					showMessage("<VP>"..text.event1.." <V><b>"..events_pt[event_selected].."</b><VP>"..text.event5.."")
				else
					showMessage("<VP>"..text.event1.." <V><b>"..events_en[event_selected].."</b><VP>"..text.event5.."")
				end
				event_selected=0;
			end
		end
	end
	for name,player in next,tfm.get.room.playerList do
		if data[name].enabled == true then
		if running == true then
			data[name].x=math.floor(math.pow((tfm.get.room.playerList[name].y/-1+10565)/100,2.2))
			if data[name].x >= 1000 and data[name].a == 0 then
				data[name].a=1
			end
			if data[name].x >= 2000 and data[name].a == 1 then
				showMessage(text.reached2,name)
				data[name].a=2
			end
			if data[name].x >= 5000 and data[name].a == 2 then
				showMessage(text.reached3,name)
				data[name].a=3
			end
			if data[name].x >= 10000 and data[name].a == 3 then
				showMessage(text.reached4,name)
				data[name].a=4
			end
			if data[name].x >= 20000 and data[name].a == 4 then
				showMessage(text.reached5,name)
				data[name].a=5
			end
			if data[name].x >= 24650 and data[name].a == 5 then
				showMessage(text.reached6,name)
				data[name].a=10
				for n,player in next,tfm.get.room.playerList do
					if not name == n then
						tfm.exec.killPlayer(name)
					else
						tfm.exec.giveCheese(name)
						tfm.exec.playerVictory(name)
						tfm.exec.setPlayerScore(name,data[name].a,true)
						showMessage("<b>"..name.."</b>"..text.reached7.."")
						tfm.exec.setGameTime(15)
						falt_int=15
						endgame=true
						data[name].enabled=false
					end
				end
			end
		end
		end
	end
	else
		if faltando <= 1 then
			changed=true
			tfm.exec.newGame(xml2,false)
			ui.removeTextArea(0,nil)
		end
	end
end
tfm.exec.newGame(map)
end

tfm.exec.chatMessage("<ROSE><b>#anvilwar</b> Multiple Module Loader revision 2<br>Version 2.248.1<br>By Morganadxana#0000")

if tfm.get.room.isTribeHouse == true then
	tfm.exec.chatMessage("<br><VP>Tribehouse detected. Initialising main #anvilwar module.<br><ROSE>The game will be available only in English.")
	initAnvilwar()
else
	if string.find(tfm.get.room.name,"bootcamp") or string.find(tfm.get.room.name,"racing") or string.find(tfm.get.room.name,"defilante") or string.find(tfm.get.room.name,"village") or string.find(tfm.get.room.name,"vanilla") or string.find(tfm.get.room.name,"survivor") then
		tfm.exec.chatMessage("<R>Room name not allowed.")
	elseif string.find(tfm.get.room.name,"watercatch") then
		tfm.exec.chatMessage("<br><VP>Detected keyword 'watercatch' on room name.<br>Initialising #watercatch module...")
		initWatercatch()
	elseif string.find(tfm.get.room.name,"beach") then
		tfm.exec.chatMessage("<br><VP>Detected keyword 'beach' on room name.<br>Initialising #beach module...")
		initBeach()
	elseif string.find(tfm.get.room.name,"naturalpark") then
		tfm.exec.chatMessage("<br><VP>Detected keyword 'naturalpark' on room name.<br>Initialising #naturalpark module...")
		initNP()
	elseif string.find(tfm.get.room.name,"mountain") then
		tfm.exec.chatMessage("<br><VP>Detected keyword 'objects' on room name.<br>Initialising #mountain module...")
		initMountain()
	else
		tfm.exec.chatMessage("<br><VP>Additional keywords was not detected. Initialising main #anvilwar module.")
		initAnvilwar()
	end
end