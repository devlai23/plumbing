CREATE DATABASE  IF NOT EXISTS `capstone_2223_mochinut` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `capstone_2223_mochinut`;
-- MySQL dump 10.13  Distrib 8.0.26, for Win64 (x86_64)
--
-- Host: soccerdb.calingaiy4id.us-east-2.rds.amazonaws.com    Database: capstone_2223_mochinut
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '';

--
-- Table structure for table `Customer`
--

DROP TABLE IF EXISTS `Customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Customer` (
  `Customer_ID` bigint NOT NULL,
  `Customer_Name` text,
  `Reg_Date` text,
  `Customer_Bday` text,
  `Customer_Email` text,
  `Bonus` text,
  `Bonus_Used` text,
  `Sales_Total` text,
  `Discount_Total` text,
  `Discount_Ratio` text,
  `Customer_Rank` int DEFAULT NULL,
  `Visit_Count` int DEFAULT NULL,
  `Last_Visit_Date` text,
  PRIMARY KEY (`Customer_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Customer`
--

LOCK TABLES `Customer` WRITE;
/*!40000 ALTER TABLE `Customer` DISABLE KEYS */;
INSERT INTO `Customer` VALUES (1111111111,'Lee, Anni','06/01/23 06:35:36 PM','4/2','annli23@bergen.org',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(1234567890,'Project, Great','06/01/23 06:35:29 PM','03/01/2000','goodjob@gmail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(1234567895,'Youcjshbeizhchtkfoaihcjekdochgndidhfnnfivudndofjrojf, Mekaifuebdovuebwofuebdicowpqicuhehzugjrhwyvvtkdhwodhejochrnkqouqhckrovptjencish','06/01/23 06:37:43 PM','Today','meyoudjekpqpxirnebtodhcnrkxovufndkdovjrnsocjrnodchnfkdjcjfnjd@gmail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2012012011,'Mama, Joe','06/01/23 06:35:44 PM','April 1, 1975','chrjo24@bergen.org',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2012022011,'Green, Bob','05/19/23 1:59:54 AM','6/3','bobgreen@gmail.com','0',NULL,NULL,NULL,NULL,11,NULL,NULL),(2012032033,'Hay, John','05/19/23 2:01:46 AM','05/05/05','johnhay@gmail.com','0',NULL,NULL,NULL,NULL,10,NULL,NULL),(2012344321,'Green, John','05/28/23 10:54:03 PM','05/05/03','johngreen@gmail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2014789326,'Cho, Lorien','06/01/23 06:35:43 PM','11/05/2004','lorien.yuna.cho@gmail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2018733036,'drachuk, tina','06/01/23 06:35:37 PM','12/04/2005','cdrachuk@gmail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2018744812,'Kim, Natalie','05/18/23 2:20:37 PM','4/5','natakim23@bergen.org','47',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2019134835,'Be, Mika','06/01/23 06:35:43 PM','05/18/2006','mikabe2019@gmail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(4085692193,'Vemuri, Satwika','06/01/23 06:35:29 PM','02/21/2006','satvem23@bergen.org',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(5512841113,'Hogan, Daniel','05/18/23 2:21:02 PM','08/10','danhog23@bergen.org','3',NULL,NULL,NULL,NULL,8,NULL,NULL),(5512845341,'Wang, Mr','06/01/23 2:35:34 PM','3/14','matwan@bergen.org',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(6661042735,'Test, Remington Kim','06/01/23 06:35:30 PM','Abc','poooooo@gmail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(8008888888,'Kaddough, Christina','06/01/23 06:35:47 PM','6/2/2005','chrkad23@bergen.org',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(9148261333,'Bunal, Patrick','06/01/23 06:37:13 PM','December 3rd 2005','patrickdb123@gmail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(9175313151,'Lee, Alvina','05/31/23 9:33:28 PM','3/3','alvinalai@gmail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(9178059231,'Lai, Devon','05/18/23 2:20:37 PM','2/7','devlai23@bergen.org','35',NULL,NULL,NULL,NULL,6,NULL,NULL),(9178059232,'Magda, Aditya','05/18/23 2:20:37 PM','1/5','devlai23@bergen.org','83',NULL,NULL,NULL,NULL,3,NULL,NULL),(9178059237,'Thoukydides, Atalanta','05/18/23 2:20:37 PM','3/8','devlai23@bergen.org','100',NULL,NULL,NULL,NULL,1,NULL,NULL),(9178059239,'Iyov, Liberatus','05/18/23 2:20:37 PM','2/5','devlai23@bergen.org','63',NULL,NULL,NULL,NULL,4,NULL,NULL),(9178059323,'Thiemom, Chiyoko','05/18/23 2:20:37 PM','2/17','devlai23@bergen.org','58',NULL,NULL,NULL,NULL,5,NULL,NULL),(9178059324,'Amalie, Karyn','05/18/23 2:20:37 PM','2/27','devlai23@bergen.org','14',NULL,NULL,NULL,NULL,7,NULL,NULL),(9178059325,'Yseult, Helga','05/18/23 2:20:37 PM','3/7','devlai23@bergen.org','93',NULL,NULL,NULL,NULL,2,NULL,NULL),(9178275938,'Joaninha, Dubthach','05/29/23 3:13:20 PM','5/28','jjunkdoc@gmail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(9275928123,'Petia, Wessel','05/29/23 3:13:45 PM','5/30','jjunkdoc@gmail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `Customer` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-06 14:15:53
