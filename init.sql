CREATE DATABASE IF NOT EXISTS mydb;
USE mydb;

CREATE TABLE IF NOT EXISTS `events` (
   `ID` int(11) NOT NULL AUTO_INCREMENT,
   `School` varchar(255) NOT NULL,
   `Title` varchar(255) NOT NULL,
   `Title_Simplified` varchar(255) NOT NULL,
   `Link` text NOT NULL,
   `Post_Date` datetime NOT NULL DEFAULT current_timestamp(),
   `Location` varchar(255) DEFAULT NULL,
   `Info` varchar(255) DEFAULT NULL,
   `Type` varchar(255) DEFAULT NULL,
   PRIMARY KEY (`ID`),
   UNIQUE KEY `Title` (`Title`),
   UNIQUE KEY `Title_Simplified` (`Title_Simplified`),
   UNIQUE KEY `uq_school_link` (`School`,`Link`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;