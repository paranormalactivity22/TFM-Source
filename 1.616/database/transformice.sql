-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : jeu. 15 juil. 2021 à 07:58
-- Version du serveur :  10.4.17-MariaDB
-- Version de PHP : 7.3.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `transformice`
--

-- --------------------------------------------------------

--
-- Structure de la table `account`
--

CREATE TABLE `account` (
  `ip` longtext NOT NULL,
  `time` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

CREATE TABLE `records` (
  `id` int(11) NOT NULL,
  `name` longtext NOT NULL,
  `data` longtext NOT NULL,
  `code` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

--
-- Déchargement des données de la table `account`
--

-- --------------------------------------------------------

--
-- Structure de la table `banlog`
--

CREATE TABLE `banlog` (
  `username` text NOT NULL,
  `bannedby` text NOT NULL,
  `time` text NOT NULL,
  `reason` text NOT NULL,
  `date` text NOT NULL,
  `status` text NOT NULL,
  `ip` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Structure de la table `bmlog`
--

CREATE TABLE `bmlog` (
  `Name` text NOT NULL,
  `State` text NOT NULL,
  `Timestamp` text NOT NULL,
  `Bannedby` text NOT NULL,
  `Time` text NOT NULL,
  `Reason` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;


--
-- Structure de la table `chats`
--

CREATE TABLE `chats` (
  `ID` int(11) NOT NULL DEFAULT 0,
  `Name` text CHARACTER SET utf8 COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

-- --------------------------------------------------------

--
-- Structure de la table `commandlog`
--

CREATE TABLE `commandlog` (
  `Time` int(11) NOT NULL,
  `Username` text NOT NULL,
  `Command` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

-- --------------------------------------------------------

--
-- Structure de la table `dailyquest`
--

CREATE TABLE `dailyquest` (
  `UserID` int(11) NOT NULL,
  `MissionID` int(11) NOT NULL,
  `MissionType` int(11) NOT NULL,
  `QntToCollect` int(11) NOT NULL,
  `QntCollected` int(11) NOT NULL,
  `Reward` int(11) NOT NULL,
  `Fraise` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

--
-- Déchargement des données de la table `dailyquest`
--

-- --------------------------------------------------------

--
-- Structure de la table `ddos`
--

CREATE TABLE `ddos` (
  `IP` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

-- --------------------------------------------------------

--
-- Structure de la table `ippermaban`
--

CREATE TABLE `ippermaban` (
  `ip` longtext NOT NULL,
  `bannedby` longtext NOT NULL,
  `reason` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

-- --------------------------------------------------------

--
-- Structure de la table `loginlog`
--

CREATE TABLE `loginlog` (
  `username` longtext NOT NULL,
  `ip` longtext NOT NULL,
  `date` longtext NOT NULL,
  `Community` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

-- --------------------------------------------------------

--
-- Structure de la table `loginlogs`
--

CREATE TABLE `loginlogs` (
  `Username` text NOT NULL,
  `IP` text NOT NULL,
  `Time` text NOT NULL,
  `Country` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `tribe`
--

CREATE TABLE `tribe` (
  `Code` int(11) NOT NULL,
  `Name` text CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Message` text CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `House` int(11) NOT NULL DEFAULT 0,
  `Ranks` text NOT NULL,
  `Historique` text CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Members` text CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Chat` int(11) NOT NULL DEFAULT 0,
  `Points` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

-- --------------------------------------------------------

--
-- Structure de la table `userpermaban`
--

CREATE TABLE `userpermaban` (
  `username` longtext NOT NULL,
  `reason` longtext NOT NULL,
  `bannedby` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

CREATE TABLE `users` (
  `Username` longtext NOT NULL,
  `Password` longtext NOT NULL,
  `PlayerID` int(11) NOT NULL,
  `PrivLevel` int(11) NOT NULL,
  `TitleNumber` int(11) NOT NULL,
  `FirstCount` int(11) NOT NULL,
  `CheeseCount` int(11) NOT NULL,
  `ShamanCheeses` int(11) NOT NULL,
  `ShopCheeses` int(11) NOT NULL,
  `ShopFraises` int(11) NOT NULL,
  `ShamanSaves` int(11) NOT NULL,
  `HardModeSaves` int(11) NOT NULL,
  `DivineModeSaves` int(11) NOT NULL,
  `BootcampCount` int(11) NOT NULL,
  `ShamanType` int(11) NOT NULL,
  `ShopItems` longtext NOT NULL,
  `ShamanItems` longtext NOT NULL,
  `Clothes` longtext NOT NULL,
  `Look` longtext NOT NULL,
  `ShamanLook` longtext NOT NULL,
  `MouseColor` longtext NOT NULL,
  `ShamanColor` longtext NOT NULL,
  `RegDate` int(11) NOT NULL,
  `Badges` longtext NOT NULL,
  `CheeseTitleList` longtext NOT NULL,
  `FirstTitleList` longtext NOT NULL,
  `ShamanTitleList` longtext NOT NULL,
  `ShopTitleList` longtext NOT NULL,
  `BootcampTitleList` longtext NOT NULL,
  `HardModeTitleList` longtext NOT NULL,
  `DivineModeTitleList` longtext NOT NULL,
  `SpecialTitleList` longtext NOT NULL,
  `BanHours` int(11) NOT NULL,
  `ShamanLevel` int(11) NOT NULL,
  `ShamanExp` int(11) NOT NULL,
  `ShamanExpNext` int(11) NOT NULL,
  `Skills` longtext NOT NULL,
  `LastOn` int(11) NOT NULL,
  `FriendsList` longtext NOT NULL,
  `IgnoredsList` longtext NOT NULL,
  `Gender` int(11) NOT NULL,
  `LastDivorceTimer` int(11) NOT NULL,
  `Marriage` longtext NOT NULL,
  `TribeCode` int(11) NOT NULL,
  `TribeRank` int(11) NOT NULL,
  `TribeJoined` int(11) NOT NULL,
  `Gifts` longtext NOT NULL,
  `Messages` longtext NOT NULL,
  `SurvivorStats` longtext NOT NULL,
  `RacingStats` longtext NOT NULL,
  `Consumables` longtext NOT NULL,
  `EquipedConsumables` longtext NOT NULL,
  `Pet` int(11) NOT NULL,
  `PetEnd` int(11) NOT NULL,
  `ShamanBadges` longtext NOT NULL,
  `EquipedShamanBadge` int(11) NOT NULL,
  `UnRanked` int(11) NOT NULL,
  `totemitemcount` int(11) NOT NULL,
  `totem` longtext NOT NULL,
  `VisuDone` longtext NOT NULL,
  `customitems` longtext NOT NULL,
  `coins` int(11) NOT NULL,
  `tokens` int(11) NOT NULL,
  `deathstats` longtext NOT NULL,
  `viptime` int(11) NOT NULL,
  `langue` longtext NOT NULL,
  `mayor` longtext NOT NULL,
  `notificationcode` longtext NOT NULL,
  `VipInfos` longtext NOT NULL,
  `aventurecounts` longtext NOT NULL,
  `aventurepoints` longtext NOT NULL,
  `savesaventure` int(11) NOT NULL,
  `user_community` varchar(3) NOT NULL DEFAULT 'xx',
  `avatar` varchar(30) NOT NULL DEFAULT '0.jpg',
  `user_line_status` int(1) NOT NULL DEFAULT 1,
  `user_token` text NOT NULL,
  `user_email` varchar(70) NOT NULL DEFAULT '0',
  `user_birthday` varchar(20) NOT NULL DEFAULT '0',
  `user_location` varchar(50) NOT NULL DEFAULT '0',
  `user_presentation` text NOT NULL,
  `user_sanction_status` varchar(10) NOT NULL DEFAULT '0',
  `user_line_param` int(11) NOT NULL DEFAULT 1,
  `Email` longtext NOT NULL,
  `DailyQuest` longtext NOT NULL,
  `RemainingMissions` int(11) NOT NULL,
  `Letters` longtext NOT NULL,
  `recCount` int(11) NOT NULL,
  `deathCount` int(11) NOT NULL,
  `user_title_forum` text NOT NULL,
  `Time` int(11) NOT NULL,
  `Karma` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

--
-- Déchargement des données de la table `users`
--

--
-- Structure de la table `usertempban`
--

CREATE TABLE `usertempban` (
  `username` longtext NOT NULL,
  `reason` longtext NOT NULL,
  `time` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;


CREATE TABLE `usertempmute` (
  `username` longtext NOT NULL,
  `time` int(11) NOT NULL,
  `reason` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

--
-- Déchargement des données de la table `usertempmute`
--


--
-- Index pour la table `tribe`
--
ALTER TABLE `tribe`
  ADD PRIMARY KEY (`Code`) USING BTREE;

--
-- AUTO_INCREMENT pour la table `tribe`
--
ALTER TABLE `tribe`
  MODIFY `Code` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=245;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
