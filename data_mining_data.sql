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
(1, 63, 'M', 3, 145, 233, 150, 'N', 1, 1),
(2, 37, 'F', 2, 130, 250, 187, 'N', 0, 0),
(3, 45, 'M', 4, 138, 236, 172, 'Y', 0, 1),
(4, 50, 'F', 3, 120, 200, 160, 'N', 0, 0),
(5, 54, 'M', 2, 140, 266, 118, 'Y', 1, 1),
(6, 60, 'M', 4, 150, 240, 130, 'Y', 0, 1),
(7, 42, 'F', 1, 110, 213, 190, 'N', 0, 0),
(8, 55, 'M', 3, 144, 220, 155, 'N', 1, 1),
(9, 47, 'F', 2, 128, 245, 168, 'Y', 0, 1),
(10, 39, 'M', 1, 118, 210, 180, 'N', 0, 0),
(11, 12, 'F', 3, 250, 250, 128, 'Y', 0, 0),
(12, 25, 'F', 3, 156, 230, 100, 'Y', 0, 0),
(13, 60, 'F', 2, 145, 233, 145, 'Y', 0, 0),
(14, 26, 'F', 1, 123, 123, 123, 'N', 1, 0),
(15, 46, 'M', 1, 244, 244, 244, 'N', 0, 1),
(16, 46, 'M', 1, 244, 244, 345, 'N', 1, 1),
(17, 23, 'M', 3, 123, 123, 123, 'N', 0, 1),
(18, 23, 'M', 3, 123, 123, 123, 'N', 1, 1),
(19, 23, 'M', 3, 123, 245, 245, 'N', 1, 1),
(20, 23, 'M', 2, 123, 245, 245, 'N', 1, 1),
(21, 67, 'M', 2, 123, 245, 245, 'N', 1, 1),
(22, 45, 'F', 1, 89, 89, 100, 'N', 0, 0);

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
