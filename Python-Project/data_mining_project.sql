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
DROP DATABASE IF EXISTS `data mining project`;
CREATE DATABASE IF NOT EXISTS `data mining project` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `data mining project`;

-- Dumping structure for table data mining project.patients_data_mining
DROP TABLE IF EXISTS `patients_data_mining`;
CREATE TABLE IF NOT EXISTS `patients_data_mining` (
  `patient_id` int NOT NULL AUTO_INCREMENT,
  `age` int DEFAULT NULL,
  `gender` char(1) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `chest_pain_type` int DEFAULT NULL,
  `resting_blood_pressure` int DEFAULT NULL,
  `cholesterol` int DEFAULT NULL,
  `max_heart_rate` int DEFAULT NULL,
  `exercise_angina` char(1) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `blood_sugar` tinyint(1) DEFAULT NULL,
  `diagnosis` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`patient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=108 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table data mining project.patients_data_mining: ~100 rows (approximately)
DELETE FROM `patients_data_mining`;
INSERT INTO `patients_data_mining` (`patient_id`, `age`, `gender`, `chest_pain_type`, `resting_blood_pressure`, `cholesterol`, `max_heart_rate`, `exercise_angina`, `blood_sugar`, `diagnosis`) VALUES
	(1, 62, 'M', 3, 148, 258, 138, 'Y', 1, 1),
	(2, 45, 'F', 2, 132, 192, 170, 'N', 0, 0),
	(3, 52, 'M', 4, 155, 250, 148, 'Y', 1, 1),
	(4, 48, 'F', 3, 122, 180, 162, 'N', 0, 0),
	(5, 55, 'M', 2, 140, 285, 125, 'Y', 1, 1),
	(6, 59, 'M', 4, 165, 275, 132, 'Y', 1, 1),
	(7, 41, 'F', 1, 118, 200, 178, 'N', 0, 0),
	(8, 53, 'M', 3, 145, 235, 152, 'N', 1, 1),
	(9, 47, 'F', 2, 128, 250, 155, 'Y', 0, 0),
	(10, 38, 'M', 1, 115, 175, 180, 'N', 0, 0),
	(11, 56, 'F', 3, 142, 260, 128, 'Y', 1, 1),
	(12, 50, 'M', 2, 135, 225, 165, 'N', 0, 0),
	(13, 60, 'F', 4, 150, 280, 122, 'Y', 1, 1),
	(14, 43, 'M', 1, 110, 205, 175, 'N', 0, 0),
	(15, 46, 'F', 2, 120, 215, 158, 'N', 0, 0),
	(16, 51, 'M', 3, 138, 245, 148, 'Y', 1, 1),
	(17, 37, 'F', 1, 105, 190, 180, 'N', 0, 0),
	(18, 57, 'M', 4, 155, 270, 128, 'Y', 1, 1),
	(19, 48, 'F', 3, 145, 255, 138, 'N', 0, 0),
	(20, 52, 'M', 2, 140, 230, 158, 'Y', 1, 1),
	(21, 44, 'F', 4, 135, 265, 135, 'Y', 1, 1),
	(22, 39, 'M', 1, 125, 180, 175, 'N', 0, 0),
	(23, 58, 'F', 2, 150, 270, 132, 'Y', 0, 1),
	(24, 49, 'M', 3, 142, 240, 145, 'Y', 1, 1),
	(25, 42, 'F', 1, 118, 195, 170, 'N', 0, 0),
	(26, 61, 'M', 4, 160, 285, 126, 'Y', 1, 1),
	(27, 46, 'F', 3, 132, 225, 155, 'Y', 1, 1),
	(28, 40, 'M', 2, 125, 210, 165, 'N', 0, 0),
	(29, 54, 'F', 1, 115, 200, 172, 'N', 0, 0),
	(30, 56, 'M', 3, 148, 265, 138, 'Y', 1, 1),
	(31, 47, 'F', 2, 135, 230, 160, 'N', 0, 0),
	(32, 63, 'M', 4, 155, 290, 125, 'Y', 1, 1),
	(33, 41, 'F', 1, 120, 205, 175, 'N', 0, 0),
	(34, 55, 'M', 3, 142, 250, 145, 'Y', 1, 1),
	(35, 59, 'F', 4, 165, 300, 122, 'Y', 1, 1),
	(36, 37, 'M', 1, 128, 190, 180, 'N', 0, 0),
	(37, 62, 'F', 2, 150, 260, 135, 'Y', 1, 1),
	(38, 49, 'M', 4, 145, 240, 152, 'Y', 0, 1),
	(39, 44, 'F', 3, 138, 230, 165, 'Y', 1, 1),
	(40, 53, 'M', 2, 132, 225, 148, 'N', 0, 0),
	(41, 58, 'F', 1, 125, 210, 160, 'N', 0, 0),
	(42, 45, 'M', 2, 135, 245, 152, 'Y', 0, 1),
	(43, 51, 'F', 3, 155, 270, 132, 'Y', 1, 1),
	(44, 39, 'M', 1, 110, 195, 170, 'N', 0, 0),
	(45, 57, 'F', 4, 150, 265, 138, 'Y', 1, 1),
	(46, 42, 'M', 2, 128, 230, 165, 'Y', 0, 1),
	(47, 60, 'F', 4, 160, 290, 125, 'Y', 1, 1),
	(48, 46, 'M', 3, 135, 220, 148, 'N', 1, 0),
	(49, 54, 'F', 2, 128, 245, 142, 'Y', 0, 1),
	(50, 52, 'M', 3, 145, 240, 152, 'Y', 1, 1),
	(51, 48, 'F', 4, 155, 285, 132, 'Y', 1, 1),
	(52, 40, 'M', 2, 138, 230, 165, 'N', 0, 0),
	(53, 56, 'F', 3, 142, 260, 138, 'Y', 1, 1),
	(54, 59, 'M', 4, 155, 300, 125, 'Y', 1, 1),
	(55, 43, 'F', 1, 128, 215, 170, 'N', 0, 0),
	(56, 61, 'M', 3, 148, 270, 152, 'Y', 1, 1),
	(57, 47, 'F', 4, 160, 295, 132, 'Y', 1, 1),
	(58, 38, 'M', 2, 135, 240, 158, 'N', 0, 0),
	(59, 55, 'F', 1, 122, 210, 175, 'N', 0, 0),
	(60, 53, 'M', 4, 155, 285, 138, 'Y', 1, 1),
	(61, 42, 'F', 2, 120, 220, 158, 'N', 0, 0),
	(62, 50, 'M', 3, 142, 250, 145, 'Y', 1, 1),
	(63, 36, 'F', 1, 108, 190, 172, 'N', 0, 0),
	(64, 57, 'M', 4, 155, 275, 128, 'Y', 1, 1),
	(65, 45, 'F', 2, 128, 230, 158, 'Y', 0, 1),
	(66, 37, 'M', 1, 115, 200, 165, 'N', 0, 0),
	(67, 48, 'F', 3, 132, 240, 152, 'Y', 1, 1),
	(68, 41, 'M', 2, 128, 210, 175, 'N', 0, 0),
	(69, 52, 'F', 3, 142, 265, 148, 'Y', 1, 1),
	(70, 55, 'M', 4, 155, 290, 132, 'Y', 1, 1),
	(71, 39, 'F', 1, 118, 185, 170, 'N', 0, 0),
	(72, 46, 'M', 2, 132, 220, 162, 'Y', 1, 1),
	(73, 54, 'F', 3, 145, 250, 138, 'Y', 1, 1),
	(74, 57, 'M', 1, 138, 235, 158, 'N', 0, 0),
	(75, 48, 'F', 2, 140, 270, 148, 'Y', 0, 1),
	(76, 42, 'M', 4, 155, 265, 142, 'Y', 1, 1),
	(77, 44, 'F', 3, 128, 240, 152, 'N', 0, 0),
	(78, 50, 'M', 2, 122, 230, 162, 'Y', 0, 1),
	(79, 46, 'F', 4, 150, 290, 132, 'Y', 1, 1),
	(80, 39, 'M', 1, 135, 220, 158, 'N', 0, 0),
	(81, 55, 'F', 3, 145, 265, 138, 'Y', 1, 1),
	(82, 52, 'M', 2, 132, 250, 152, 'N', 0, 0),
	(83, 47, 'F', 4, 155, 280, 132, 'Y', 1, 1),
	(84, 43, 'M', 3, 138, 225, 165, 'Y', 1, 1),
	(85, 59, 'F', 1, 118, 215, 170, 'N', 0, 0),
	(86, 61, 'M', 4, 155, 300, 128, 'Y', 1, 1),
	(87, 48, 'F', 2, 128, 230, 152, 'Y', 1, 1),
	(88, 45, 'M', 3, 142, 240, 145, 'Y', 0, 1),
	(89, 51, 'F', 4, 150, 270, 132, 'Y', 1, 1),
	(90, 37, 'M', 1, 122, 200, 158, 'N', 0, 0),
	(91, 44, 'F', 2, 132, 250, 148, 'Y', 1, 1),
	(92, 56, 'M', 3, 145, 280, 138, 'Y', 1, 1),
	(93, 42, 'F', 4, 155, 295, 128, 'Y', 1, 1),
	(94, 49, 'M', 2, 138, 230, 165, 'N', 0, 0),
	(95, 54, 'F', 3, 142, 265, 132, 'Y', 1, 1),
	(96, 40, 'M', 1, 118, 210, 170, 'N', 0, 0),
	(97, 43, 'F', 2, 122, 220, 158, 'N', 0, 0),
	(98, 47, 'M', 3, 138, 250, 145, 'Y', 1, 1),
	(99, 52, 'F', 4, 155, 275, 132, 'Y', 1, 1),
	(100, 57, 'M', 1, 128, 230, 158, 'N', 0, 0),
	(101, 45, 'M', 2, 123, 123, 123, 'Y', 1, 1),
	(102, 45, 'F', 3, 245, 300, 70, 'N', 0, 1),
	(103, 60, 'M', 2, 100, 250, 120, 'Y', 1, 1),
	(104, 50, 'M', 1, 200, 150, 150, 'N', 0, 0),
	(105, 50, 'M', 1, 200, 150, 150, 'N', 1, 0),
	(106, 45, 'F', 4, 150, 300, 150, 'N', 0, 1),
	(107, 35, 'M', 2, 145, 200, 100, 'N', 0, 0);

-- Dumping structure for table data mining project.users
DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `avatar` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table data mining project.users: ~0 rows (approximately)
DELETE FROM `users`;
INSERT INTO `users` (`id`, `username`, `password`, `avatar`) VALUES
	(1, 'testuser', 'testpassword', NULL),
	(2, 'tantt121', 'tantt121', NULL);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
