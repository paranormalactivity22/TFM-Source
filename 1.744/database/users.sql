SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `account` (
  `ip` longtext NOT NULL,
  `time` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

CREATE TABLE `banlog` (
  `username` text NOT NULL,
  `bannedby` text NOT NULL,
  `time` text NOT NULL,
  `reason` text NOT NULL,
  `date` text NOT NULL,
  `status` text NOT NULL,
  `ip` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `casierlog` (
  `Name` text NOT NULL,
  `IP` text NOT NULL,
  `State` text NOT NULL,
  `Timestamp` text NOT NULL,
  `Moderator` text NOT NULL,
  `Time` text NOT NULL,
  `Reason` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

CREATE TABLE `chats` (
  `ID` int(11) NOT NULL DEFAULT 0,
  `Name` text CHARACTER SET utf8 COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

CREATE TABLE `commandlog` (
  `Time` int(11) NOT NULL,
  `Username` text NOT NULL,
  `Command` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

CREATE TABLE `ddos` (
  `IP` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

CREATE TABLE `ippermaban` (
  `ip` longtext NOT NULL,
  `bannedby` longtext NOT NULL,
  `reason` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

CREATE TABLE `loginlogs` (
  `Username` text NOT NULL,
  `IP` text NOT NULL,
  `IPColor` text NOT NULL,
  `Time` text NOT NULL,
  `Country` text NOT NULL,
  `Community` text NOT NULL,
  `ConnectionID` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `missions` (
  `userid` longtext NOT NULL,
  `missions` longtext NOT NULL,
  `totalfinished_missions` int(3) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

CREATE TABLE `records` (
  `id` int(11) NOT NULL,
  `name` longtext NOT NULL,
  `data` longtext NOT NULL,
  `code` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `tribe` (
  `Code` int(11) NOT NULL,
  `Name` text CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Message` text CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `House` int(11) NOT NULL DEFAULT 0,
  `Ranks` text NOT NULL,
  `Historique` text CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Members` text CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Chat` int(11) NOT NULL DEFAULT 0,
  `Points` int(11) NOT NULL,
  `createTime` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

CREATE TABLE `userpermaban` (
  `username` longtext NOT NULL,
  `reason` longtext NOT NULL,
  `bannedby` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

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
  `ShamanSavesNoSkill` int(11) NOT NULL,
  `HardModeSaves` int(11) NOT NULL,
  `HardModeSavesNoSkill` int(11) NOT NULL,
  `DivineModeSaves` int(11) NOT NULL,
  `DivineModeSavesNoSkill` int(11) NOT NULL,
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
  `DefilanteStats` longtext NOT NULL,
  `Consumables` longtext NOT NULL,
  `EquipedConsumables` longtext NOT NULL,
  `Pet` int(11) NOT NULL,
  `PetEnd` int(11) NOT NULL,
  `Fur` int(11) NOT NULL,
  `FurEnd` int(11) NOT NULL,
  `ShamanBadges` longtext NOT NULL,
  `EquipedShamanBadge` int(11) NOT NULL,
  `totemitemcount` int(11) NOT NULL,
  `totem` longtext NOT NULL,
  `VisuDone` longtext NOT NULL,
  `customitems` longtext NOT NULL,
  `langue` longtext NOT NULL,
  `AventureCounts` longtext NOT NULL,
  `AventurePoints` longtext NOT NULL,
  `AventureSaves` longtext NOT NULL,
  `user_community` varchar(3) NOT NULL DEFAULT 'xx',
  `avatar` varchar(30) NOT NULL DEFAULT '0.jpg',
  `Email` longtext NOT NULL,
  `Letters` longtext NOT NULL,
  `Time` int(11) NOT NULL,
  `Karma` int(11) NOT NULL,
  `Roles` varchar(50) NOT NULL DEFAULT '{}'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

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


ALTER TABLE `tribe`
  ADD PRIMARY KEY (`Code`) USING BTREE;

ALTER TABLE `tribe`
  MODIFY `Code` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=281;
COMMIT;