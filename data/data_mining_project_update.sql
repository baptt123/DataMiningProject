-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 29, 2024 at 04:43 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `data mining project`
--

-- --------------------------------------------------------

--
-- Table structure for table `patients_data_mining`
--

CREATE TABLE `patients_data_mining` (
  `patient_id` int(11) NOT NULL,
  `age` int(11) DEFAULT NULL,
  `gender` char(1) DEFAULT NULL,
  `chest_pain_type` int(11) DEFAULT NULL,
  `resting_blood_pressure` int(11) DEFAULT NULL,
  `cholesterol` int(11) DEFAULT NULL,
  `max_heart_rate` int(11) DEFAULT NULL,
  `exercise_angina` char(1) DEFAULT NULL,
  `blood_sugar` tinyint(1) DEFAULT NULL,
  `diagnosis` tinyint(1) DEFAULT NULL,
  `fullname` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `patients_data_mining`
--

INSERT INTO `patients_data_mining` (`patient_id`, `age`, `gender`, `chest_pain_type`, `resting_blood_pressure`, `cholesterol`, `max_heart_rate`, `exercise_angina`, `blood_sugar`, `diagnosis`, `fullname`) VALUES
(1, 62, 'M', 3, 148, 258, 138, 'Y', 1, 1, 'thanh tan'),
(2, 45, 'F', 2, 132, 192, 170, 'N', 0, 0, 'thanh tan'),
(3, 52, 'M', 4, 155, 250, 148, 'Y', 1, 1, 'thanh tan'),
(4, 48, 'F', 3, 122, 180, 162, 'N', 0, 0, 'thanh tan'),
(5, 55, 'M', 2, 140, 285, 125, 'Y', 1, 1, 'thanh tan'),
(6, 59, 'M', 4, 165, 275, 132, 'Y', 1, 1, 'thanh tan'),
(7, 41, 'F', 1, 118, 200, 178, 'N', 0, 0, 'thanh tan'),
(8, 53, 'M', 3, 145, 235, 152, 'N', 1, 1, 'thanh tan'),
(9, 47, 'F', 2, 128, 250, 155, 'Y', 0, 0, 'thanh tan'),
(10, 38, 'M', 1, 115, 175, 180, 'N', 0, 0, 'thanh tan'),
(11, 56, 'F', 3, 142, 260, 128, 'Y', 1, 1, 'thanh tan'),
(12, 50, 'M', 2, 135, 225, 165, 'N', 0, 0, 'thanh tan'),
(13, 60, 'F', 4, 150, 280, 122, 'Y', 1, 1, 'thanh tan'),
(14, 43, 'M', 1, 110, 205, 175, 'N', 0, 0, 'thanh tan'),
(15, 46, 'F', 2, 120, 215, 158, 'N', 0, 0, 'thanh tan'),
(16, 51, 'M', 3, 138, 245, 148, 'Y', 1, 1, 'thanh tan'),
(17, 37, 'F', 1, 105, 190, 180, 'N', 0, 0, 'thanh tan'),
(18, 57, 'M', 4, 155, 270, 128, 'Y', 1, 1, 'thanh tan'),
(19, 48, 'F', 3, 145, 255, 138, 'N', 0, 0, 'thanh tan'),
(20, 52, 'M', 2, 140, 230, 158, 'Y', 1, 1, 'thanh tan'),
(21, 44, 'F', 4, 135, 265, 135, 'Y', 1, 1, 'thanh tan'),
(22, 39, 'M', 1, 125, 180, 175, 'N', 0, 0, 'thanh tan'),
(23, 58, 'F', 2, 150, 270, 132, 'Y', 0, 1, 'thanh tan'),
(24, 49, 'M', 3, 142, 240, 145, 'Y', 1, 1, 'thanh tan'),
(25, 42, 'F', 1, 118, 195, 170, 'N', 0, 0, 'thanh tan'),
(26, 61, 'M', 4, 160, 285, 126, 'Y', 1, 1, 'thanh tan'),
(27, 46, 'F', 3, 132, 225, 155, 'Y', 1, 1, 'thanh tan'),
(28, 40, 'M', 2, 125, 210, 165, 'N', 0, 0, 'thanh tan'),
(29, 54, 'F', 1, 115, 200, 172, 'N', 0, 0, 'thanh tan'),
(30, 56, 'M', 3, 148, 265, 138, 'Y', 1, 1, 'thanh tan'),
(31, 47, 'F', 2, 135, 230, 160, 'N', 0, 0, 'thanh tan'),
(32, 63, 'M', 4, 155, 290, 125, 'Y', 1, 1, 'thanh tan'),
(33, 41, 'F', 1, 120, 205, 175, 'N', 0, 0, 'thanh tan'),
(34, 55, 'M', 3, 142, 250, 145, 'Y', 1, 1, 'thanh tan'),
(35, 59, 'F', 4, 165, 300, 122, 'Y', 1, 1, 'thanh tan'),
(36, 37, 'M', 1, 128, 190, 180, 'N', 0, 0, 'thanh tan'),
(37, 62, 'F', 2, 150, 260, 135, 'Y', 1, 1, 'thanh tan'),
(38, 49, 'M', 4, 145, 240, 152, 'Y', 0, 1, 'thanh tan'),
(39, 44, 'F', 3, 138, 230, 165, 'Y', 1, 1, 'thanh tan'),
(40, 53, 'M', 2, 132, 225, 148, 'N', 0, 0, 'thanh tan'),
(41, 58, 'F', 1, 125, 210, 160, 'N', 0, 0, 'thanh tan'),
(42, 45, 'M', 2, 135, 245, 152, 'Y', 0, 1, 'thanh tan'),
(43, 51, 'F', 3, 155, 270, 132, 'Y', 1, 1, 'thanh tan'),
(44, 39, 'M', 1, 110, 195, 170, 'N', 0, 0, 'thanh tan'),
(45, 57, 'F', 4, 150, 265, 138, 'Y', 1, 1, 'thanh tan'),
(46, 42, 'M', 2, 128, 230, 165, 'Y', 0, 1, 'thanh tan'),
(47, 60, 'F', 4, 160, 290, 125, 'Y', 1, 1, 'thanh tan'),
(48, 46, 'M', 3, 135, 220, 148, 'N', 1, 0, 'thanh tan'),
(49, 54, 'F', 2, 128, 245, 142, 'Y', 0, 1, 'thanh tan'),
(50, 52, 'M', 3, 145, 240, 152, 'Y', 1, 1, 'thanh tan'),
(51, 48, 'F', 4, 155, 285, 132, 'Y', 1, 1, 'thanh tan'),
(52, 40, 'M', 2, 138, 230, 165, 'N', 0, 0, 'thanh tan'),
(53, 56, 'F', 3, 142, 260, 138, 'Y', 1, 1, 'thanh tan'),
(54, 59, 'M', 4, 155, 300, 125, 'Y', 1, 1, 'thanh tan'),
(55, 43, 'F', 1, 128, 215, 170, 'N', 0, 0, 'thanh tan'),
(56, 61, 'M', 3, 148, 270, 152, 'Y', 1, 1, 'thanh tan'),
(57, 47, 'F', 4, 160, 295, 132, 'Y', 1, 1, 'thanh tan'),
(58, 38, 'M', 2, 135, 240, 158, 'N', 0, 0, 'thanh tan'),
(59, 55, 'F', 1, 122, 210, 175, 'N', 0, 0, 'thanh tan'),
(60, 53, 'M', 4, 155, 285, 138, 'Y', 1, 1, 'thanh tan'),
(61, 42, 'F', 2, 120, 220, 158, 'N', 0, 0, 'thanh tan'),
(62, 50, 'M', 3, 142, 250, 145, 'Y', 1, 1, 'thanh tan'),
(63, 36, 'F', 1, 108, 190, 172, 'N', 0, 0, 'thanh tan'),
(64, 57, 'M', 4, 155, 275, 128, 'Y', 1, 1, 'thanh tan'),
(65, 45, 'F', 2, 128, 230, 158, 'Y', 0, 1, 'thanh tan'),
(66, 37, 'M', 1, 115, 200, 165, 'N', 0, 0, 'thanh tan'),
(67, 48, 'F', 3, 132, 240, 152, 'Y', 1, 1, 'thanh tan'),
(68, 41, 'M', 2, 128, 210, 175, 'N', 0, 0, 'thanh tan'),
(69, 52, 'F', 3, 142, 265, 148, 'Y', 1, 1, 'thanh tan'),
(70, 55, 'M', 4, 155, 290, 132, 'Y', 1, 1, 'thanh tan'),
(71, 39, 'F', 1, 118, 185, 170, 'N', 0, 0, 'thanh tan'),
(72, 46, 'M', 2, 132, 220, 162, 'Y', 1, 1, 'thanh tan'),
(73, 54, 'F', 3, 145, 250, 138, 'Y', 1, 1, 'thanh tan'),
(74, 57, 'M', 1, 138, 235, 158, 'N', 0, 0, 'thanh tan'),
(75, 48, 'F', 2, 140, 270, 148, 'Y', 0, 1, 'thanh tan'),
(76, 42, 'M', 4, 155, 265, 142, 'Y', 1, 1, 'thanh tan'),
(77, 44, 'F', 3, 128, 240, 152, 'N', 0, 0, 'thanh tan'),
(78, 50, 'M', 2, 122, 230, 162, 'Y', 0, 1, 'thanh tan'),
(79, 46, 'F', 4, 150, 290, 132, 'Y', 1, 1, 'thanh tan'),
(80, 39, 'M', 1, 135, 220, 158, 'N', 0, 0, 'thanh tan'),
(81, 55, 'F', 3, 145, 265, 138, 'Y', 1, 1, 'thanh tan'),
(82, 52, 'M', 2, 132, 250, 152, 'N', 0, 0, 'thanh tan'),
(83, 47, 'F', 4, 155, 280, 132, 'Y', 1, 1, 'thanh tan'),
(84, 43, 'M', 3, 138, 225, 165, 'Y', 1, 1, 'thanh tan'),
(85, 59, 'F', 1, 118, 215, 170, 'N', 0, 0, 'thanh tan'),
(86, 61, 'M', 4, 155, 300, 128, 'Y', 1, 1, 'thanh tan'),
(87, 48, 'F', 2, 128, 230, 152, 'Y', 1, 1, 'thanh tan'),
(88, 45, 'M', 3, 142, 240, 145, 'Y', 0, 1, 'thanh tan'),
(89, 51, 'F', 4, 150, 270, 132, 'Y', 1, 1, 'thanh tan'),
(90, 37, 'M', 1, 122, 200, 158, 'N', 0, 0, 'thanh tan'),
(91, 44, 'F', 2, 132, 250, 148, 'Y', 1, 1, 'thanh tan'),
(92, 56, 'M', 3, 145, 280, 138, 'Y', 1, 1, 'thanh tan'),
(93, 42, 'F', 4, 155, 295, 128, 'Y', 1, 1, 'thanh tan'),
(94, 49, 'M', 2, 138, 230, 165, 'N', 0, 0, 'thanh tan'),
(95, 54, 'F', 3, 142, 265, 132, 'Y', 1, 1, 'thanh tan'),
(96, 40, 'M', 1, 118, 210, 170, 'N', 0, 0, 'thanh tan'),
(97, 43, 'F', 2, 122, 220, 158, 'N', 0, 0, 'thanh tan'),
(98, 47, 'M', 3, 138, 250, 145, 'Y', 1, 1, 'thanh tan'),
(99, 52, 'F', 4, 155, 275, 132, 'Y', 1, 1, 'thanh tan'),
(100, 57, 'M', 1, 128, 230, 158, 'N', 0, 0, 'thanh tan'),
(101, 45, 'M', 2, 123, 123, 123, 'Y', 1, 1, 'thanh tan'),
(102, 45, 'F', 3, 245, 300, 70, 'N', 0, 1, 'thanh tan'),
(103, 60, 'M', 2, 100, 250, 120, 'Y', 1, 1, 'thanh tan'),
(104, 50, 'M', 1, 200, 150, 150, 'N', 0, 0, 'thanh tan'),
(105, 50, 'M', 1, 200, 150, 150, 'N', 1, 0, 'thanh tan'),
(106, 45, 'F', 4, 150, 300, 150, 'N', 0, 1, 'thanh tan'),
(107, 35, 'M', 2, 145, 200, 100, 'N', 0, 0, 'thanh tan'),
(108, 23, 'F', 2, 124, 123, 123, 'Y', 1, 1, 'thanh tan'),
(109, 30, 'F', 2, 150, 300, 123, 'N', 1, 1, 'thanh tan'),
(110, 20, 'F', 1, 150, 400, 200, 'Y', 1, 1, 'thanh tan');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`) VALUES
(1, 'testuser', 'testpassword', 'admin'),
(2, 'tantt121', 'tantt121', 'user'),
(3, 'tanbadao123', 'tanbadao123', 'user');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `patients_data_mining`
--
ALTER TABLE `patients_data_mining`
  ADD PRIMARY KEY (`patient_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `patients_data_mining`
--
ALTER TABLE `patients_data_mining`
  MODIFY `patient_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=112;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
