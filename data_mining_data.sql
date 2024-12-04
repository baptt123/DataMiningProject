-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th10 25, 2024 lúc 10:09 AM
-- Phiên bản máy phục vụ: 10.4.32-MariaDB
-- Phiên bản PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `data mining project`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `patients_data_mining`
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
  `diagnosis` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `patients_data_mining`
--

INSERT INTO `patients_data_mining` (`patient_id`, `age`, `gender`, `chest_pain_type`, `resting_blood_pressure`, `cholesterol`, `max_heart_rate`, `exercise_angina`, `blood_sugar`, `diagnosis`) VALUES
(1, 65, 'M', 3, 155, 280, 140, 'Y', 1, 1),
(2, 41, 'F', 2, 135, 190, 175, 'N', 0, 0),
(3, 49, 'M', 4, 160, 245, 150, 'Y', 1, 1),
(4, 52, 'F', 3, 125, 185, 165, 'N', 0, 0),
(5, 58, 'M', 2, 145, 300, 120, 'Y', 1, 1),
(6, 62, 'M', 4, 170, 270, 135, 'Y', 1, 1),
(7, 43, 'F', 1, 112, 195, 180, 'N', 0, 0),
(8, 56, 'M', 3, 150, 240, 155, 'N', 1, 1),
(9, 50, 'F', 2, 130, 255, 160, 'Y', 0, 1),
(10, 40, 'M', 1, 120, 180, 185, 'N', 0, 0);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `avatar` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `avatar`) VALUES
(1, 'testuser', 'testpassword', NULL),
(2, 'tantt121', 'tantt121', NULL);

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `patients_data_mining`
--
ALTER TABLE `patients_data_mining`
  ADD PRIMARY KEY (`patient_id`);

--
-- Chỉ mục cho bảng `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `patients_data_mining`
--
ALTER TABLE `patients_data_mining`
  MODIFY `patient_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT cho bảng `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
