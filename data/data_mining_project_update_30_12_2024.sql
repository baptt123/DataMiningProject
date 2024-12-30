-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 30, 2024 at 03:57 PM
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
  `fullname` text DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `gender` char(1) DEFAULT NULL,
  `chest_pain_type` int(11) DEFAULT NULL,
  `resting_blood_pressure` int(11) DEFAULT NULL,
  `cholesterol` int(11) DEFAULT NULL,
  `max_heart_rate` int(11) DEFAULT NULL,
  `exercise_angina` char(1) DEFAULT NULL,
  `blood_sugar` tinyint(1) DEFAULT NULL,
  `diagnosis` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `patients_data_mining`
--

INSERT INTO `patients_data_mining` (`patient_id`, `fullname`, `age`, `gender`, `chest_pain_type`, `resting_blood_pressure`, `cholesterol`, `max_heart_rate`, `exercise_angina`, `blood_sugar`, `diagnosis`) VALUES
(1, 'a', 62, 'M', 3, 148, 258, 138, 'Y', 1, 1),
(2, 'a', 45, 'F', 2, 132, 192, 170, 'N', 0, 0),
(3, 'a', 52, 'M', 4, 155, 250, 148, 'Y', 1, 1),
(4, 'a', 48, 'F', 3, 122, 180, 162, 'N', 0, 0),
(5, 'a', 55, 'M', 2, 140, 285, 125, 'Y', 1, 1),
(6, 'a', 59, 'M', 4, 165, 275, 132, 'Y', 1, 1),
(7, 'a', 41, 'F', 1, 118, 200, 178, 'N', 0, 0),
(8, 'a', 53, 'M', 3, 145, 235, 152, 'N', 1, 1),
(9, 'a', 47, 'F', 2, 128, 250, 155, 'Y', 0, 0),
(10, 'a', 38, 'M', 1, 115, 175, 180, 'N', 0, 0),
(11, 'a', 56, 'F', 3, 142, 260, 128, 'Y', 1, 1),
(12, 'a', 50, 'M', 2, 135, 225, 165, 'N', 0, 0),
(13, 'a', 60, 'F', 4, 150, 280, 122, 'Y', 1, 1),
(14, 'a', 43, 'M', 1, 110, 205, 175, 'N', 0, 0),
(15, 'a', 46, 'F', 2, 120, 215, 158, 'N', 0, 0),
(16, 'a', 51, 'M', 3, 138, 245, 148, 'Y', 1, 1),
(17, 'a', 37, 'F', 1, 105, 190, 180, 'N', 0, 0),
(18, 'a', 57, 'M', 4, 155, 270, 128, 'Y', 1, 1),
(19, 'a', 48, 'F', 3, 145, 255, 138, 'N', 0, 0),
(20, 'a', 52, 'M', 2, 140, 230, 158, 'Y', 1, 1),
(21, 'a', 44, 'F', 4, 135, 265, 135, 'Y', 1, 1),
(22, 'a', 39, 'M', 1, 125, 180, 175, 'N', 0, 0),
(23, 'a', 58, 'F', 2, 150, 270, 132, 'Y', 0, 1),
(24, 'a', 49, 'M', 3, 142, 240, 145, 'Y', 1, 1),
(25, 'a', 42, 'F', 1, 118, 195, 170, 'N', 0, 0),
(26, 'a', 61, 'M', 4, 160, 285, 126, 'Y', 1, 1),
(27, 'a', 46, 'F', 3, 132, 225, 155, 'Y', 1, 1),
(28, 'a', 40, 'M', 2, 125, 210, 165, 'N', 0, 0),
(29, 'a', 54, 'F', 1, 115, 200, 172, 'N', 0, 0),
(30, 'a', 56, 'M', 3, 148, 265, 138, 'Y', 1, 1),
(31, 'a', 47, 'F', 2, 135, 230, 160, 'N', 0, 0),
(32, 'a', 63, 'M', 4, 155, 290, 125, 'Y', 1, 1),
(33, 'a', 41, 'F', 1, 120, 205, 175, 'N', 0, 0),
(34, 'a', 55, 'M', 3, 142, 250, 145, 'Y', 1, 1),
(35, 'a', 59, 'F', 4, 165, 300, 122, 'Y', 1, 1),
(36, 'a', 37, 'M', 1, 128, 190, 180, 'N', 0, 0),
(37, 'a', 62, 'F', 2, 150, 260, 135, 'Y', 1, 1),
(38, 'a', 49, 'M', 4, 145, 240, 152, 'Y', 0, 1),
(39, 'a', 44, 'F', 3, 138, 230, 165, 'Y', 1, 1),
(40, 'a', 53, 'M', 2, 132, 225, 148, 'N', 0, 0),
(41, 'a', 58, 'F', 1, 125, 210, 160, 'N', 0, 0),
(42, 'a', 45, 'M', 2, 135, 245, 152, 'Y', 0, 1),
(43, 'a', 51, 'F', 3, 155, 270, 132, 'Y', 1, 1),
(44, 'a', 39, 'M', 1, 110, 195, 170, 'N', 0, 0),
(45, 'a', 57, 'F', 4, 150, 265, 138, 'Y', 1, 1),
(46, 'a', 42, 'M', 2, 128, 230, 165, 'Y', 0, 1),
(47, 'a', 60, 'F', 4, 160, 290, 125, 'Y', 1, 1),
(48, 'a', 46, 'M', 3, 135, 220, 148, 'N', 1, 0),
(49, 'a', 54, 'F', 2, 128, 245, 142, 'Y', 0, 1),
(50, 'a', 52, 'M', 3, 145, 240, 152, 'Y', 1, 1),
(51, 'a', 48, 'F', 4, 155, 285, 132, 'Y', 1, 1),
(52, 'a', 40, 'M', 2, 138, 230, 165, 'N', 0, 0),
(53, 'a', 56, 'F', 3, 142, 260, 138, 'Y', 1, 1),
(54, 'a', 59, 'M', 4, 155, 300, 125, 'Y', 1, 1),
(55, 'a', 43, 'F', 1, 128, 215, 170, 'N', 0, 0),
(56, 'a', 61, 'M', 3, 148, 270, 152, 'Y', 1, 1),
(57, 'a', 47, 'F', 4, 160, 295, 132, 'Y', 1, 1),
(58, 'a', 38, 'M', 2, 135, 240, 158, 'N', 0, 0),
(59, 'a', 55, 'F', 1, 122, 210, 175, 'N', 0, 0),
(60, 'a', 53, 'M', 4, 155, 285, 138, 'Y', 1, 1),
(61, 'a', 42, 'F', 2, 120, 220, 158, 'N', 0, 0),
(62, 'a', 50, 'M', 3, 142, 250, 145, 'Y', 1, 1),
(63, 'a', 36, 'F', 1, 108, 190, 172, 'N', 0, 0),
(64, 'a', 57, 'M', 4, 155, 275, 128, 'Y', 1, 1),
(65, 'a', 45, 'F', 2, 128, 230, 158, 'Y', 0, 1),
(66, 'a', 37, 'M', 1, 115, 200, 165, 'N', 0, 0),
(67, 'a', 48, 'F', 3, 132, 240, 152, 'Y', 1, 1),
(68, 'a', 41, 'M', 2, 128, 210, 175, 'N', 0, 0),
(69, 'a', 52, 'F', 3, 142, 265, 148, 'Y', 1, 1),
(70, 'a', 55, 'M', 4, 155, 290, 132, 'Y', 1, 1),
(71, 'a', 39, 'F', 1, 118, 185, 170, 'N', 0, 0),
(72, 'a', 46, 'M', 2, 132, 220, 162, 'Y', 1, 1),
(73, 'a', 54, 'F', 3, 145, 250, 138, 'Y', 1, 1),
(74, 'a', 57, 'M', 1, 138, 235, 158, 'N', 0, 0),
(75, 'a', 48, 'F', 2, 140, 270, 148, 'Y', 0, 1),
(76, 'a', 42, 'M', 4, 155, 265, 142, 'Y', 1, 1),
(77, 'a', 44, 'F', 3, 128, 240, 152, 'N', 0, 0),
(78, 'a', 50, 'M', 2, 122, 230, 162, 'Y', 0, 1),
(79, 'a', 46, 'F', 4, 150, 290, 132, 'Y', 1, 1),
(80, 'a', 39, 'M', 1, 135, 220, 158, 'N', 0, 0),
(81, 'a', 55, 'F', 3, 145, 265, 138, 'Y', 1, 1),
(82, 'a', 52, 'M', 2, 132, 250, 152, 'N', 0, 0),
(83, 'a', 47, 'F', 4, 155, 280, 132, 'Y', 1, 1),
(84, 'a', 43, 'M', 3, 138, 225, 165, 'Y', 1, 1),
(85, 'a', 59, 'F', 1, 118, 215, 170, 'N', 0, 0),
(86, 'a', 61, 'M', 4, 155, 300, 128, 'Y', 1, 1),
(87, 'a', 48, 'F', 2, 128, 230, 152, 'Y', 1, 1),
(88, 'a', 45, 'M', 3, 142, 240, 145, 'Y', 0, 1),
(89, 'a', 51, 'F', 4, 150, 270, 132, 'Y', 1, 1),
(90, 'a', 37, 'M', 1, 122, 200, 158, 'N', 0, 0),
(91, 'a', 44, 'F', 2, 132, 250, 148, 'Y', 1, 1),
(92, 'a', 56, 'M', 3, 145, 280, 138, 'Y', 1, 1),
(93, 'a', 42, 'F', 4, 155, 295, 128, 'Y', 1, 1),
(94, 'a', 49, 'M', 2, 138, 230, 165, 'N', 0, 0),
(95, 'a', 54, 'F', 3, 142, 265, 132, 'Y', 1, 1),
(96, 'a', 40, 'M', 1, 118, 210, 170, 'N', 0, 0),
(97, 'a', 43, 'F', 2, 122, 220, 158, 'N', 0, 0),
(98, 'a', 47, 'M', 3, 138, 250, 145, 'Y', 1, 1),
(99, 'a', 52, 'F', 4, 155, 275, 132, 'Y', 1, 1),
(100, 'a', 57, 'M', 1, 128, 230, 158, 'N', 0, 0),
(101, 'a', 45, 'M', 2, 123, 123, 123, 'Y', 1, 1),
(102, 'a', 45, 'F', 3, 245, 300, 70, 'N', 0, 1),
(103, 'a', 60, 'M', 2, 100, 250, 120, 'Y', 1, 1),
(104, 'a', 50, 'M', 1, 200, 150, 150, 'N', 0, 0),
(105, 'a', 50, 'M', 1, 200, 150, 150, 'N', 1, 0),
(106, 'a', 45, 'F', 4, 150, 300, 150, 'N', 0, 1),
(107, 'a', 35, 'M', 2, 145, 200, 100, 'N', 0, 0),
(108, 'a', 23, 'F', 2, 124, 123, 123, 'Y', 1, 1),
(109, 'a', 30, 'F', 2, 150, 300, 123, 'N', 1, 1),
(110, 'a', 20, 'F', 1, 150, 400, 200, 'Y', 1, 1);

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
