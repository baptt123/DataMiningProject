-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.0.30 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for data mining project
CREATE DATABASE IF NOT EXISTS `data mining project` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `data mining project`;

-- Dumping structure for table data mining project.patients_data_mining
CREATE TABLE IF NOT EXISTS `patients_data_mining` (
  `patient_id` int NOT NULL,
  `fullname` text COLLATE utf8mb4_unicode_ci,
  `age` int DEFAULT NULL,
  `gender` char(1) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `chest_pain_type` int DEFAULT NULL,
  `resting_blood_pressure` int DEFAULT NULL,
  `cholesterol` int DEFAULT NULL,
  `max_heart_rate` int DEFAULT NULL,
  `exercise_angina` char(1) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `blood_sugar` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `shortness_of_breath` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fatigue` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dizziness` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `chest_pain_frequency` int DEFAULT NULL,
  `heart_rate_variability` int DEFAULT NULL,
  `pulse_pressure` int DEFAULT NULL,
  `ldl_hdl_ratio` float DEFAULT NULL,
  `stress_level` int DEFAULT NULL,
  `family_history` char(1) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `diagnosis` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table data mining project.patients_data_mining: ~110 rows (approximately)
DELETE FROM `patients_data_mining`;
INSERT INTO `patients_data_mining` (`patient_id`, `fullname`, `age`, `gender`, `chest_pain_type`, `resting_blood_pressure`, `cholesterol`, `max_heart_rate`, `exercise_angina`, `blood_sugar`, `shortness_of_breath`, `fatigue`, `dizziness`, `chest_pain_frequency`, `heart_rate_variability`, `pulse_pressure`, `ldl_hdl_ratio`, `stress_level`, `family_history`, `diagnosis`) VALUES
	(1, 'a', 62, 'M', 3, 148, 258, 138, 'Y', 'High', 'Severe', 'Often', 'Never', 3, 35, 45, 2.8, 7, 'Y', 1),
	(2, 'a', 45, 'F', 2, 132, 192, 170, 'N', 'Normal', 'None', 'Never', 'Occasional', 1, 25, 40, 1.8, 4, 'N', 0),
	(3, 'a', 52, 'M', 4, 155, 280, 148, 'Y', 'High', 'Severe', 'Often', 'Often', 4, 42, 52, 3.2, 8, 'Y', 1),
	(4, 'a', 48, 'F', 3, 122, 180, 162, 'N', 'Normal', 'None', 'Never', 'Never', 2, 22, 38, 1.6, 3, 'N', 0),
	(5, 'a', 55, 'M', 2, 140, 285, 125, 'Y', 'High', 'Moderate', 'Sometimess', 'Often', 3, 38, 48, 2.9, 7, 'Y', 1),
	(6, 'a', 59, 'M', 4, 165, 275, 132, 'Y', 'High', 'Severe', 'Often', 'Often', 4, 45, 58, 3.1, 9, 'Y', 1),
	(7, 'a', 41, 'F', 1, 118, 200, 178, 'N', 'Normal', 'None', 'Never', 'Never', 1, 20, 35, 1.5, 2, 'N', 0),
	(8, 'a', 53, 'M', 3, 145, 235, 152, 'N', 'High', 'Moderate', 'Sometimes', 'Occasional', 3, 32, 43, 2.2, 6, 'Y', 1),
	(9, 'a', 47, 'F', 2, 128, 250, 155, 'Y', 'Normal', 'None', 'Never', 'Often', 2, 28, 41, 2, 5, 'N', 0),
	(10, 'a', 38, 'M', 1, 115, 175, 180, 'N', 'Normal', 'None', 'Never', 'Never', 1, 18, 36, 1.6, 2, 'N', 0),
	(11, 'a', 56, 'F', 3, 142, 380, 128, 'N', 'Normal', 'Severe', 'Often', 'Never', 3, 50, 60, 3.8, 8, 'N', 1),
	(12, 'a', 50, 'M', 2, 135, 145, 165, 'Y', 'High', 'None', 'Sometimes', 'Often', 2, 35, 45, 1.5, 4, 'Y', 0),
	(13, 'a', 60, 'F', 4, 150, 320, 122, 'N', 'High', 'Moderate', 'Never', 'Often', 4, 48, 62, 3.5, 9, 'Y', 0),
	(14, 'a', 43, 'M', 1, 110, 205, 175, 'N', 'Normal', 'None', 'Never', 'Never', 1, 22, 37, 1.7, 3, 'N', 0),
	(15, 'a', 46, 'F', 2, 120, 215, 158, 'N', 'Normal', 'None', 'Never', 'Occasional', 2, 25, 39, 1.8, 4, 'N', 0),
	(16, 'a', 51, 'M', 3, 138, 400, 148, 'N', 'Normal', 'Severe', 'Often', 'Never', 3, 55, 63, 4, 7, 'N', 1),
	(17, 'a', 37, 'F', 1, 105, 120, 180, 'Y', 'High', 'None', 'Sometimes', 'Often', 1, 18, 35, 1.5, 2, 'Y', 0),
	(18, 'a', 44, 'M', 2, 130, 210, 160, 'N', 'Normal', 'None', 'Never', 'Occasional', 2, 27, 38, 1.9, 4, 'N', 0),
	(19, 'a', 58, 'F', 3, 140, 300, 140, 'Y', 'High', 'Moderate', 'Sometimes', 'Often', 3, 35, 46, 2.5, 6, 'Y', 1),
	(20, 'a', 52, 'M', 4, 155, 290, 135, 'Y', 'High', 'Severe', 'Often', 'Often', 4, 42, 52, 3.2, 8, 'Y', 1),
	(21, 'a', 36, 'F', 1, 110, 180, 170, 'N', 'Normal', 'None', 'Never', 'Never', 1, 20, 33, 1.5, 2, 'N', 0),
	(22, 'a', 49, 'M', 3, 142, 260, 145, 'N', 'High', 'Moderate', 'Sometimes', 'Occasional', 3, 30, 42, 2.1, 5, 'Y', 1),
	(23, 'a', 65, 'F', 2, 160, 90, 100, 'N', 'Very High', 'Severe', 'Never', 'Never', 4, 60, 70, 5, 10, 'Y', 1),
	(24, 'a', 28, 'M', 1, 115, 140, 185, 'N', 'Normal', 'None', 'Never', 'Never', 1, 15, 30, 1.3, 1, 'N', 0),
	(25, 'a', 54, 'F', 3, 145, 275, 132, 'Y', 'High', 'Severe', 'Often', 'Often', 4, 44, 55, 3.3, 7, 'Y', 1),
	(26, 'a', 39, 'M', 2, 125, 190, 172, 'N', 'Normal', 'None', 'Never', 'Occasional', 2, 24, 36, 1.7, 3, 'N', 0),
	(27, 'a', 60, 'F', 4, 150, 320, 122, 'N', 'High', 'Moderate', 'Never', 'Often', 4, 48, 62, 3.5, 9, 'Y', 0),
	(28, 'a', 50, 'M', 3, 135, 245, 150, 'Y', 'High', 'Moderate', 'Sometimes', 'Occasional', 3, 32, 43, 2.2, 6, 'Y', 1),
	(29, 'a', 42, 'F', 2, 118, 200, 176, 'N', 'Normal', 'None', 'Never', 'Never', 1, 22, 37, 1.7, 3, 'N', 0),
	(30, 'a', 56, 'M', 4, 148, 285, 134, 'Y', 'High', 'Severe', 'Often', 'Often', 4, 45, 58, 3.1, 8, 'Y', 1),
	(31, 'a', 40, 'M', 2, 120, 210, 165, 'N', 'Normal', 'None', 'Never', 'Occasional', 2, 26, 39, 1.8, 4, 'N', 0),
	(32, 'a', 57, 'F', 3, 138, 295, 130, 'Y', 'High', 'Moderate', 'Sometimes', 'Often', 3, 36, 47, 2.6, 6, 'Y', 1),
	(33, 'a', 55, 'M', 4, 160, 310, 128, 'Y', 'High', 'Severe', 'Often', 'Often', 4, 44, 56, 3.4, 8, 'Y', 1),
	(34, 'a', 35, 'F', 1, 108, 170, 172, 'N', 'Normal', 'None', 'Never', 'Never', 1, 19, 32, 1.4, 2, 'N', 0),
	(35, 'a', 60, 'M', 4, 150, 330, 120, 'Y', 'High', 'Severe', 'Often', 'Often', 4, 90, 64, 3.7, 9, 'Y', 1),
	(36, 'a', 37, 'F', 2, 118, 180, 160, 'N', 'Normal', 'None', 'Never', 'Never', 1, 22, 35, 1.6, 3, 'N', 0),
	(37, 'a', 150, 'M', 2, 200, 700, 180, 'Y', 'High', 'Severe', 'Often', 'Never', 3, 45, 58, 4.5, 10, 'Y', 1),
	(38, 'a', 23, 'F', 4, 100, 350, 140, 'N', 'Low', 'None', 'Never', 'Never', 2, 28, 39, 2.2, 5, 'N', 0),
	(39, 'a', 32, 'M', 1, 110, 180, 200, 'Y', 'High', 'Severe', 'Often', 'Occasional', 4, 35, 48, 3, 7, 'Y', 1),
	(40, 'a', 95, 'F', 3, 110, 1000, 145, 'N', 'Very High', 'None', 'Never', 'Never', 1, 20, 33, 2.8, 6, 'Y', 0),
	(41, 'a', 40, 'M', 2, 120, 290, 150, 'N', 'Normal', 'Moderate', 'Sometimes', 'Often', 3, 38, 50, 3.1, 5, 'Y', 1),
	(42, 'a', 55, 'F', 4, 130, 450, 120, 'Y', 'High', 'Severe', 'Sometimes', 'Never', 4, 42, 60, 3.6, 8, 'N', 1),
	(43, 'a', 28, 'M', 3, 140, 275, 160, 'N', 'Normal', 'None', 'Never', 'Never', 2, 33, 46, 2.5, 4, 'N', 0),
	(44, 'a', 60, 'F', 2, 125, 400, 155, 'Y', 'High', 'Moderate', 'Often', 'Often', 4, 50, 60, 3.2, 7, 'Y', 1),
	(45, 'a', 100, 'M', 3, 180, 800, 130, 'Y', 'Normal', 'None', 'Never', 'Never', 3, 55, 70, 4.2, 9, 'N', 1),
	(46, 'a', 33, 'F', 2, 118, 220, 180, 'N', 'Normal', 'Severe', 'Sometimes', 'Often', 2, 25, 40, 2.3, 5, 'Y', 0),
	(47, 'a', 110, 'M', 4, 200, 1000, 200, 'Y', 'High', 'Severe', 'Often', 'Never', 4, 60, 80, 5, 10, 'Y', 1),
	(48, 'a', 50, 'F', 1, 115, 150, 170, 'N', 'Normal', 'None', 'Never', 'Never', 1, 20, 35, 2, 3, 'N', 0),
	(49, 'a', 72, 'M', 2, 140, 350, 180, 'Y', 'High', 'Moderate', 'Sometimes', 'Often', 3, 40, 55, 3.4, 6, 'Y', 1),
	(50, 'a', 65, 'F', 3, 145, 400, 165, 'N', 'Normal', 'Severe', 'Often', 'Never', 4, 47, 62, 3.7, 8, 'N', 1),
	(51, 'a', 30, 'M', 2, 110, 200, 190, 'Y', 'Very High', 'None', 'Never', 'Occasional', 2, 30, 45, 2.9, 6, 'Y', 1),
	(52, 'a', 25, 'F', 4, 125, 300, 160, 'N', 'Normal', 'Moderate', 'Never', 'Never', 2, 28, 42, 3, 5, 'N', 0),
	(53, 'a', 80, 'M', 3, 150, 750, 140, 'Y', 'High', 'Severe', 'Often', 'Occasional', 4, 50, 65, 4.3, 7, 'Y', 1),
	(54, 'a', 90, 'F', 2, 135, 300, 125, 'N', 'High', 'Moderate', 'Never', 'Often', 3, 48, 60, 3.8, 9, 'Y', 1),
	(55, 'a', 35, 'M', 1, 110, 170, 155, 'N', 'Normal', 'None', 'Never', 'Never', 1, 22, 36, 2.4, 3, 'N', 0),
	(56, 'a', 70, 'M', 2, 115, 350, 150, 'Y', 'High', 'Severe', 'Often', 'Never', 4, 38, 50, 3.1, 8, 'Y', 1),
	(57, 'a', 80, 'F', 3, 130, 300, 140, 'N', 'Normal', 'None', 'Never', 'Never', 3, 43, 55, 3.6, 7, 'Y', 1),
	(58, 'a', 60, 'M', 1, 140, 200, 165, 'Y', 'Very High', 'Moderate', 'Sometimes', 'Occasional', 2, 30, 44, 2.9, 6, 'N', 0),
	(59, 'a', 85, 'F', 2, 150, 800, 125, 'N', 'High', 'None', 'Never', 'Never', 1, 25, 40, 3.3, 5, 'Y', 0),
	(60, 'a', 45, 'M', 4, 130, 400, 190, 'Y', 'Normal', 'Moderate', 'Sometimes', 'Occasional', 4, 50, 65, 3.2, 6, 'Y', 1),
	(61, 'a', 23, 'F', 1, 105, 250, 175, 'N', 'Normal', 'Severe', 'Never', 'Never', 2, 20, 35, 2.4, 4, 'N', 0),
	(62, 'a', 40, 'M', 2, 120, 320, 160, 'Y', 'Normal', 'Moderate', 'Sometimes', 'Never', 3, 35, 48, 3, 7, 'Y', 1),
	(63, 'a', 50, 'F', 3, 110, 150, 140, 'N', 'Very High', 'None', 'Never', 'Never', 2, 28, 43, 3.1, 5, 'N', 0),
	(64, 'a', 75, 'M', 4, 130, 250, 180, 'Y', 'High', 'Severe', 'Sometimes', 'Occasional', 4, 40, 58, 3.5, 9, 'Y', 1),
	(65, 'a', 32, 'F', 2, 115, 280, 150, 'N', 'Normal', 'None', 'Never', 'Never', 1, 23, 37, 2.7, 4, 'Y', 0),
	(66, 'a', 200, 'M', 3, 140, 600, 170, 'Y', 'Normal', 'Severe', 'Sometimes', 'Occasional', 3, 50, 63, 3.4, 7, 'Y', 1),
	(67, 'a', 35, 'F', 1, 120, 270, 160, 'N', 'Normal', 'None', 'Never', 'Never', 2, 30, 45, 2.6, 5, 'N', 0),
	(68, 'a', 90, 'M', 2, 125, 450, 130, 'Y', 'High', 'Moderate', 'Sometimes', 'Never', 4, 55, 75, 3.8, 8, 'Y', 1),
	(69, 'a', 25, 'F', 4, 110, 181, 180, 'N', 'Very High', 'None', 'Never', 'Never', 2, 27, 40, 2.2, 4, 'N', 0),
	(70, 'a', 38, 'M', 3, 130, 400, 150, 'Y', 'Normal', 'Severe', 'Sometimes', 'Never', 3, 45, 60, 3, 6, 'Y', 1),
	(71, 'a', 50, 'F', 2, 140, 350, 155, 'N', 'Normal', 'Moderate', 'Never', 'Never', 2, 30, 45, 2.8, 5, 'N', 0),
	(72, 'a', 80, 'M', 1, 145, 170, 170, 'Y', 'High', 'Severe', 'Often', 'Often', 3, 50, 65, 3.7, 9, 'Y', 1),
	(73, 'a', 29, 'F', 4, 120, 200, 160, 'N', 'Normal', 'None', 'Never', 'Never', 2, 25, 38, 2.3, 4, 'N', 0),
	(74, 'a', 92, 'M', 2, 130, 900, 145, 'Y', 'Very High', 'None', 'Never', 'Never', 4, 55, 70, 4, 8, 'Y', 1),
	(75, 'a', 65, 'F', 3, 110, 300, 135, 'N', 'Normal', 'Severe', 'Sometimes', 'Never', 3, 40, 55, 3.1, 7, 'N', 0),
	(76, 'a', 90, 'M', 1, 120, 400, 160, 'Y', 'Normal', 'Severe', 'Often', 'Often', 4, 50, 65, 3.6, 8, 'Y', 1),
	(77, 'a', 30, 'F', 2, 125, 220, 150, 'N', 'Normal', 'None', 'Never', 'Never', 2, 27, 42, 2.5, 6, 'N', 0),
	(78, 'a', 75, 'M', 4, 145, 700, 180, 'Y', 'Very High', 'None', 'Often', 'Never', 3, 50, 68, 4.2, 9, 'Y', 1),
	(79, 'a', 55, 'F', 3, 135, 215, 140, 'N', 'High', 'Moderate', 'Never', 'Occasional', 3, 45, 60, 3.3, 7, 'N', 0),
	(80, 'a', 47, 'M', 2, 110, 250, 165, 'Y', 'Normal', 'None', 'Sometimes', 'Never', 4, 35, 50, 3, 5, 'Y', 1),
	(81, 'a', 28, 'F', 1, 120, 180, 155, 'N', 'Normal', 'None', 'Never', 'Never', 2, 25, 38, 2.2, 4, 'N', 0),
	(82, 'a', 72, 'M', 3, 130, 150, 160, 'Y', 'Very High', 'Severe', 'Often', 'Occasional', 4, 50, 65, 3.8, 8, 'Y', 1),
	(83, 'a', 32, 'F', 2, 115, 290, 145, 'N', 'Normal', 'None', 'Never', 'Never', 1, 20, 30, 2.3, 3, 'N', 0),
	(84, 'a', 95, 'M', 4, 150, 1000, 130, 'Y', 'High', 'None', 'Sometimes', 'Never', 3, 55, 70, 4, 9, 'Y', 1),
	(85, 'a', 50, 'F', 3, 140, 400, 145, 'N', 'Normal', 'Severe', 'Often', 'Never', 2, 30, 43, 3.2, 6, 'Y', 0),
	(86, 'a', 60, 'M', 1, 125, 270, 155, 'Y', 'Normal', 'Moderate', 'Sometimes', 'Never', 4, 45, 60, 3.5, 7, 'Y', 1),
	(87, 'a', 36, 'F', 2, 110, 220, 165, 'N', 'High', 'None', 'Never', 'Never', 1, 25, 38, 2.6, 4, 'N', 0),
	(88, 'a', 80, 'M', 3, 145, 750, 170, 'Y', 'Normal', 'Severe', 'Often', 'Never', 3, 55, 75, 4.1, 9, 'Y', 1),
	(89, 'a', 63, 'F', 4, 120, 300, 140, 'N', 'Very High', 'None', 'Sometimes', 'Occasional', 2, 30, 45, 3.3, 5, 'N', 0),
	(90, 'a', 25, 'M', 1, 110, 250, 160, 'Y', 'Normal', 'Severe', 'Never', 'Never', 2, 20, 35, 2.7, 4, 'Y', 0),
	(91, 'a', 77, 'F', 2, 130, 260, 145, 'N', 'High', 'None', 'Sometimes', 'Never', 3, 40, 55, 3.5, 7, 'Y', 1),
	(92, 'a', 48, 'M', 3, 120, 370, 155, 'Y', 'Normal', 'Moderate', 'Sometimes', 'Never', 2, 33, 47, 3, 6, 'Y', 0),
	(93, 'a', 35, 'F', 2, 110, 300, 150, 'N', 'Normal', 'None', 'Never', 'Often', 1, 28, 40, 2.8, 5, 'Y', 0),
	(94, 'a', 60, 'M', 1, 135, 178, 160, 'Y', 'Very High', 'Severe', 'Sometimes', 'Often', 4, 50, 63, 3.4, 8, 'Y', 1),
	(95, 'a', 75, 'F', 4, 120, 200, 145, 'N', 'Normal', 'None', 'Never', 'Never', 3, 25, 38, 2.9, 5, 'N', 0),
	(96, 'a', 90, 'M', 3, 145, 800, 130, 'Y', 'High', 'Severe', 'Often', 'Never', 4, 55, 70, 4.2, 9, 'Y', 1),
	(97, 'a', 45, 'F', 2, 125, 350, 160, 'N', 'Normal', 'None', 'Sometimes', 'Often', 3, 30, 50, 3.1, 6, 'Y', 0),
	(98, 'a', 85, 'M', 1, 130, 200, 170, 'Y', 'Normal', 'Severe', 'Never', 'Never', 4, 40, 60, 3.2, 8, 'Y', 1),
	(99, 'a', 30, 'F', 2, 120, 250, 155, 'N', 'Normal', 'None', 'Never', 'Often', 2, 28, 42, 2.6, 5, 'N', 0),
	(100, 'a', 65, 'M', 3, 140, 238, 160, 'Y', 'High', 'Moderate', 'Sometimes', 'Occasional', 3, 45, 60, 3.3, 7, 'Y', 1),
	(101, 'a', 72, 'F', 4, 135, 350, 145, 'N', 'Very High', 'None', 'Never', 'Never', 4, 48, 65, 3.6, 8, 'Y', 0),
	(102, 'a', 50, 'M', 1, 120, 300, 150, 'Y', 'Normal', 'Moderate', 'Sometimes', 'Never', 3, 35, 50, 2.9, 6, 'Y', 1),
	(103, 'a', 60, 'F', 2, 115, 250, 140, 'N', 'Normal', 'Severe', 'Never', 'Often', 1, 20, 38, 2.7, 5, 'N', 0),
	(104, 'a', 68, 'M', 3, 145, 150, 180, 'Y', 'High', 'None', 'Sometimes', 'Never', 4, 55, 70, 4.1, 9, 'Y', 1),
	(105, 'a', 75, 'F', 2, 135, 190, 155, 'N', 'Normal', 'Moderate', 'Never', 'Occasional', 3, 50, 60, 3.2, 6, 'Y', 0),
	(106, 'a', 80, 'M', 4, 150, 700, 160, 'Y', 'Normal', 'Severe', 'Often', 'Never', 4, 58, 75, 4.3, 10, 'Y', 1),
	(107, 'a', 65, 'F', 1, 110, 230, 150, 'N', 'Very High', 'None', 'Never', 'Never', 2, 22, 40, 2.5, 4, 'N', 0),
	(108, 'a', 23, 'F', 2, 124, 350, 123, 'Y', 'High', 'Severe', 'Often', 'Often', 3, 45, 55, 3.5, 5, 'Y', 1),
	(109, 'a', 30, 'F', 2, 150, 320, 123, 'N', 'High', 'Moderate', 'Sometimes', 'Often', 3, 40, 50, 3, 6, 'Y', 1),
	(110, 'a', 20, 'F', 1, 150, 400, 200, 'Y', 'High', 'Severe', 'Often', 'Often', 4, 55, 63, 4, 9, 'Y', 1),
	(111, 'tan', 60, 'M', 2, 150, 150, 150, 'Y', 'Normal', 'None', 'None', 'None', 2, 30, 30, 2, 5, '1', 0),
	(112, 'tan', 60, 'F', 2, 150, 150, 150, 'Y', 'Normal', 'None', 'None', 'None', 2, 30, 30, 2, 5, '1', 0),
	(113, 'testuser', 60, 'F', 3, 150, 150, 150, 'Y', 'Normal', 'None', 'None', 'None', 2, 30, 40, 3, 5, '1', 0),
	(114, 'a', 30, 'F', 3, 150, 180, 145, 'Y', 'Normal', 'None', 'None', 'None', 2, 30, 40, 3, 4, '1', 0);

-- Dumping structure for table data mining project.users
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table data mining project.users: ~0 rows (approximately)
DELETE FROM `users`;
INSERT INTO `users` (`id`, `username`, `password`, `role`) VALUES
	(1, 'a', 'a', 'admin');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
