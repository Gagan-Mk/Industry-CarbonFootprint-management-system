-- MySQL dump 10.13  Distrib 8.0.38, for macos14 (arm64)
--
-- Host: 127.0.0.1    Database: icfms
-- ------------------------------------------------------
-- Server version	9.0.1

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

--
-- Table structure for table `Carbon_Offsets`
--

DROP TABLE IF EXISTS `Carbon_Offsets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Carbon_Offsets` (
  `offset_id` int NOT NULL AUTO_INCREMENT,
  `offset_type` varchar(50) DEFAULT NULL,
  `amount_offset` decimal(10,2) DEFAULT NULL,
  `date_purchased` date DEFAULT NULL,
  `provider_details` varchar(100) DEFAULT NULL,
  `industry_id` int NOT NULL,
  PRIMARY KEY (`offset_id`),
  KEY `fk_carbon_offsets_industry_id` (`industry_id`),
  CONSTRAINT `fk_carbon_offsets_industry_id` FOREIGN KEY (`industry_id`) REFERENCES `Industries` (`industry_id`),
  CONSTRAINT `fk_industry_id_new` FOREIGN KEY (`industry_id`) REFERENCES `Industries` (`industry_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Carbon_Offsets`
--

LOCK TABLES `Carbon_Offsets` WRITE;
/*!40000 ALTER TABLE `Carbon_Offsets` DISABLE KEYS */;
INSERT INTO `Carbon_Offsets` VALUES (1,'rev',23.12,'2024-11-08','env',1);
/*!40000 ALTER TABLE `Carbon_Offsets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Emission_Sources`
--

DROP TABLE IF EXISTS `Emission_Sources`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Emission_Sources` (
  `source_id` int NOT NULL AUTO_INCREMENT,
  `source_type` varchar(50) DEFAULT NULL,
  `emission_value` decimal(10,2) DEFAULT NULL,
  `process_id` int DEFAULT NULL,
  `industry_id` int DEFAULT NULL,
  PRIMARY KEY (`source_id`),
  KEY `process_id` (`process_id`),
  CONSTRAINT `emission_sources_ibfk_1` FOREIGN KEY (`process_id`) REFERENCES `Process` (`process_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Emission_Sources`
--

LOCK TABLES `Emission_Sources` WRITE;
/*!40000 ALTER TABLE `Emission_Sources` DISABLE KEYS */;
INSERT INTO `Emission_Sources` VALUES (1,'gas',21.00,NULL,1);
/*!40000 ALTER TABLE `Emission_Sources` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Industries`
--

DROP TABLE IF EXISTS `Industries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Industries` (
  `industry_id` int NOT NULL AUTO_INCREMENT,
  `industry_name` varchar(100) NOT NULL,
  `location` varchar(100) DEFAULT NULL,
  `industry_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`industry_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Industries`
--

LOCK TABLES `Industries` WRITE;
/*!40000 ALTER TABLE `Industries` DISABLE KEYS */;
INSERT INTO `Industries` VALUES (1,'KGF','7th main road','gold industry '),(2,'MTR pvt lmt','8th main road ','food');
/*!40000 ALTER TABLE `Industries` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `before_industry_delete` BEFORE DELETE ON `industries` FOR EACH ROW BEGIN
    DELETE FROM Process WHERE industry_id = OLD.industry_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `Process`
--

DROP TABLE IF EXISTS `Process`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Process` (
  `process_id` int NOT NULL AUTO_INCREMENT,
  `process_name` varchar(100) DEFAULT NULL,
  `energy_consumption` decimal(10,2) DEFAULT NULL,
  `emission_factor` decimal(10,2) DEFAULT NULL,
  `industry_id` int DEFAULT NULL,
  PRIMARY KEY (`process_id`),
  KEY `fk_industry_id` (`industry_id`),
  CONSTRAINT `fk_industry_id` FOREIGN KEY (`industry_id`) REFERENCES `Industries` (`industry_id`) ON DELETE CASCADE,
  CONSTRAINT `process_ibfk_1` FOREIGN KEY (`industry_id`) REFERENCES `Industries` (`industry_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Process`
--

LOCK TABLES `Process` WRITE;
/*!40000 ALTER TABLE `Process` DISABLE KEYS */;
INSERT INTO `Process` VALUES (1,'comb',12.30,2.45,2),(2,'rbst',21.50,7.90,1);
/*!40000 ALTER TABLE `Process` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `before_process_delete` BEFORE DELETE ON `process` FOR EACH ROW BEGIN
    DELETE FROM Emission_Sources WHERE process_id = OLD.process_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `ROLE`
--

DROP TABLE IF EXISTS `ROLE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ROLE` (
  `role_id` int NOT NULL AUTO_INCREMENT,
  `role_name` varchar(50) NOT NULL,
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ROLE`
--

LOCK TABLES `ROLE` WRITE;
/*!40000 ALTER TABLE `ROLE` DISABLE KEYS */;
INSERT INTO `ROLE` VALUES (1,'Admin'),(2,'Industry Manager'),(3,'Auditor'),(4,'Public User');
/*!40000 ALTER TABLE `ROLE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Transportation`
--

DROP TABLE IF EXISTS `Transportation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Transportation` (
  `transport_id` int NOT NULL AUTO_INCREMENT,
  `vehicle_type` varchar(50) DEFAULT NULL,
  `distance_travelled` decimal(10,2) DEFAULT NULL,
  `fuel_consumption` decimal(10,2) DEFAULT NULL,
  `industry_id` int DEFAULT NULL,
  PRIMARY KEY (`transport_id`),
  KEY `fk_transportation_industry_id` (`industry_id`),
  CONSTRAINT `fk_transportation_industry_id` FOREIGN KEY (`industry_id`) REFERENCES `Industries` (`industry_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Transportation`
--

LOCK TABLES `Transportation` WRITE;
/*!40000 ALTER TABLE `Transportation` DISABLE KEYS */;
INSERT INTO `Transportation` VALUES (2,'car',234.00,33.00,1);
/*!40000 ALTER TABLE `Transportation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `USER`
--

DROP TABLE IF EXISTS `USER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `USER` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role_id` int DEFAULT NULL,
  `industry_id` int DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  KEY `role_id` (`role_id`),
  KEY `fk_user_industry_id` (`industry_id`),
  CONSTRAINT `fk_user_industry_id` FOREIGN KEY (`industry_id`) REFERENCES `Industries` (`industry_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `ROLE` (`role_id`),
  CONSTRAINT `user_ibfk_2` FOREIGN KEY (`industry_id`) REFERENCES `Industries` (`industry_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `USER`
--

LOCK TABLES `USER` WRITE;
/*!40000 ALTER TABLE `USER` DISABLE KEYS */;
INSERT INTO `USER` VALUES (1,'krishm','kir@gmail.com','dywpuv-4tafdi-sagNyn',3,NULL),(3,'gagan','gag14krish@gmail.com','abc123',1,NULL),(4,'rocky','rocky@gmail.com','rocky123',2,1),(5,'murthy','mruthy@gmail.com','murthy123',2,2);
/*!40000 ALTER TABLE `USER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'icfms'
--

--
-- Dumping routines for database 'icfms'
--
/*!50003 DROP FUNCTION IF EXISTS `get_total_carbon_offset` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `get_total_carbon_offset`(industryId INT) RETURNS decimal(10,2)
    DETERMINISTIC
BEGIN
    DECLARE totalOffset DECIMAL(10,2);
    SELECT SUM(amount_offset) INTO totalOffset
    FROM Carbon_Offsets
    WHERE industry_id = industryId;
    RETURN totalOffset;
END ;;
DELIMITER ;

DROP TRIGGER IF EXISTS before_process_delete;

DELIMITER ;;
CREATE DEFINER=root@localhost TRIGGER before_process_delete 
BEFORE DELETE ON process 
FOR EACH ROW 
BEGIN
    DELETE FROM Emission_Sources WHERE industry_id = OLD.industry_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-19 22:30:45
