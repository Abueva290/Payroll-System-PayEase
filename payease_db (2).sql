-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 15, 2026 at 12:33 PM
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
-- Database: `payease_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts`
--

CREATE TABLE `accounts` (
  `ID` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `role` varchar(50) NOT NULL,
  `employee_id` varchar(50) DEFAULT NULL,
  `password_hash` varchar(255) DEFAULT NULL,
  `salt` varchar(64) DEFAULT NULL,
  `password_changed_at` datetime DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `failed_login_attempts` int(11) DEFAULT 0,
  `is_locked` tinyint(1) DEFAULT 0,
  `locked_until` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`ID`, `username`, `password`, `role`, `employee_id`, `password_hash`, `salt`, `password_changed_at`, `last_login`, `failed_login_attempts`, `is_locked`, `locked_until`) VALUES
(1, 'vange', 'vange123', 'employee', 'E000', NULL, NULL, NULL, NULL, 0, 0, NULL),
(2, 'Noel', '123456', 'employee', 'E001', NULL, NULL, NULL, NULL, 0, 0, NULL),
(3, 'vincent@gmail.com', '12345678', 'employee', 'E002', NULL, NULL, NULL, NULL, 0, 0, NULL),
(4, 'Hariss321', '12345678', 'employee', 'E003', NULL, NULL, NULL, NULL, 0, 0, NULL),
(5, 'calvinabueva', '123456', 'employee', 'E004', NULL, NULL, NULL, NULL, 0, 0, NULL),
(6, 'kiro', 'palauto123', 'employee', 'E005', NULL, NULL, NULL, NULL, 0, 0, NULL),
(7, 'jhpnabueva', '123456', 'employee', 'E006', NULL, NULL, NULL, NULL, 0, 0, NULL),
(8, 'bibi', 'bibi123', 'employee', 'E007', NULL, NULL, NULL, NULL, 0, 0, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--

CREATE TABLE `attendance` (
  `id` int(11) NOT NULL,
  `employee_id` varchar(50) NOT NULL,
  `date` date NOT NULL,
  `clock_in` time DEFAULT NULL,
  `clock_out` time DEFAULT NULL,
  `status` varchar(20) DEFAULT 'Present',
  `notes` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `attendance`
--

INSERT INTO `attendance` (`id`, `employee_id`, `date`, `clock_in`, `clock_out`, `status`, `notes`, `created_at`) VALUES
(1, 'E000', '2025-12-16', '09:00:00', '20:00:00', 'Half Day', NULL, '2025-12-16 08:37:13'),
(2, 'E000', '2025-12-17', '09:00:00', '17:00:00', 'Present', NULL, '2025-12-16 08:37:35'),
(3, 'E000', '2027-12-13', '14:00:00', '05:00:00', 'Present', NULL, '2025-12-16 08:37:56'),
(4, 'E001', '2025-12-17', '09:00:00', '17:00:00', 'Present', NULL, '2025-12-16 17:16:33'),
(5, 'E002', '2025-12-17', '08:00:00', '19:00:00', 'Present', NULL, '2025-12-17 07:48:12'),
(6, 'E003', '2025-12-17', '09:00:00', '17:00:00', 'Present', NULL, '2025-12-17 07:58:48'),
(7, 'E004', '2025-12-17', '09:00:00', '17:00:00', 'Half Day', NULL, '2025-12-17 08:19:37'),
(8, 'E005', '2025-12-17', '09:00:00', '17:00:00', 'Present', NULL, '2025-12-17 09:01:08'),
(9, 'E006', '2025-12-17', '06:00:00', '14:00:00', 'Present', NULL, '2025-12-17 11:10:01');

-- --------------------------------------------------------

--
-- Table structure for table `employees`
--

CREATE TABLE `employees` (
  `Employee_ID` varchar(60) NOT NULL,
  `FullName` varchar(60) NOT NULL,
  `Email` varchar(60) NOT NULL,
  `Role` varchar(60) NOT NULL,
  `Position` varchar(60) NOT NULL,
  `Salary` int(20) NOT NULL,
  `Department` varchar(50) NOT NULL,
  `Phone` int(15) NOT NULL,
  `Address` varchar(60) NOT NULL,
  `data_hired` date NOT NULL,
  `is_archived` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employees`
--

INSERT INTO `employees` (`Employee_ID`, `FullName`, `Email`, `Role`, `Position`, `Salary`, `Department`, `Phone`, `Address`, `data_hired`, `is_archived`) VALUES
('E000', 'Vange Abuevea', 'vange@gmail.com', 'employee', 'Developer', 123456, 'Engineering', 0, '', '0000-00-00', 0),
('E001', 'noelbingco', 'noelbingco@gmail.com', 'Employee', 'data analyst', 5000000, 'Marketing', 0, '', '2025-12-17', 0),
('E002', 'Vincent Torrejas', 'vincent@gmail.com', 'HR', 'Senior Manager', 1000000, 'Engineering', 0, '', '2021-12-17', 0),
('E003', 'Julharizz Usman', 'haris@pogi.com', 'Employee', 'Senior Managee', 100000, 'Marketing', 2147483647, 'Sandawa Phase 1', '2025-12-15', 0),
('E004', 'calvinabueva', 'calvinabueva@gmail.com', 'Finance', 'senior manager', 1000000, 'Marketing', 0, '', '2025-12-13', 0),
('E005', 'Alvin Legarbes', 'legarbes@gmail.com', 'Employee', 'Engineering', 10000, 'Engineering', 2147483647, 'Buhangin Jalikod', '2025-12-17', 0),
('E006', 'justine', 'j.abueva.555671@umindanao.edu.ph', 'manager', 'senior manager', 10000, 'Marketing', 2147483647, 'tigatto', '2025-12-17', 0),
('E007', 'bibiabueva', 'bibiabueva@gmail.com', 'HR', 'senior manager', 2000000, 'Operations', 0, '', '2026-01-09', 0);

-- --------------------------------------------------------

--
-- Table structure for table `password_history`
--

CREATE TABLE `password_history` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `payroll`
--

CREATE TABLE `payroll` (
  `id` int(11) NOT NULL,
  `employee_id` varchar(50) NOT NULL,
  `month` varchar(20) NOT NULL,
  `year` int(11) NOT NULL,
  `base_salary` decimal(10,2) NOT NULL,
  `bonus` decimal(10,2) DEFAULT 0.00,
  `deductions` decimal(10,2) DEFAULT 0.00,
  `net_salary` decimal(10,2) NOT NULL,
  `present_days` varchar(20) DEFAULT '30 days',
  `status` varchar(20) DEFAULT 'Processed',
  `notes` text DEFAULT NULL,
  `processed_date` datetime NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `released_date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `payroll`
--

INSERT INTO `payroll` (`id`, `employee_id`, `month`, `year`, `base_salary`, `bonus`, `deductions`, `net_salary`, `present_days`, `status`, `notes`, `processed_date`, `created_at`, `released_date`) VALUES
(1, 'E000', 'December', 2025, 123456.00, 0.00, 10000.00, 113456.00, '2 days', 'Released', '', '2025-12-16 16:38:28', '2025-12-16 08:38:28', '2025-12-16 16:38:44'),
(2, 'E001', 'June', 2025, 5000000.00, 200.00, 100.00, 5000100.00, '0 days', 'Pending', '', '2025-12-17 01:17:42', '2025-12-16 17:17:42', NULL),
(3, 'E002', 'December', 2025, 1000000.00, 20000.00, 200.00, 1019800.00, '1 days', 'Released', 'kupal ka', '2025-12-17 15:49:26', '2025-12-17 07:49:26', '2025-12-17 15:49:44'),
(4, 'E003', 'December', 2025, 100000.00, 230000.00, 0.00, 330000.00, '1 days', 'Released', 'pogi', '2025-12-17 15:59:15', '2025-12-17 07:59:15', '2025-12-17 15:59:29'),
(5, 'E004', 'July', 2025, 1000000.00, 15000000.00, 1000000.00, 15000000.00, '0 days', 'Released', 'heyyyy', '2025-12-17 16:19:58', '2025-12-17 08:19:58', '2025-12-17 16:20:04'),
(6, 'E005', 'December', 2025, 10000.00, 50.00, 0.00, 10050.00, '1 days', 'Released', '', '2025-12-17 17:01:50', '2025-12-17 09:01:50', '2025-12-17 17:02:09'),
(7, 'E006', 'July', 2024, 10000.00, 2000.00, 1000.00, 11000.00, '0 days', 'Released', 'idol', '2025-12-17 19:10:28', '2025-12-17 11:10:28', '2025-12-17 19:10:48');

-- --------------------------------------------------------

--
-- Table structure for table `security_logs`
--

CREATE TABLE `security_logs` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `username` varchar(100) DEFAULT NULL,
  `action` varchar(50) DEFAULT NULL,
  `details` text DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `timestamp` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `idx_employee_id` (`employee_id`),
  ADD KEY `idx_username` (`username`),
  ADD KEY `idx_email_lookup` (`employee_id`);

--
-- Indexes for table `attendance`
--
ALTER TABLE `attendance`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_attendance` (`employee_id`,`date`),
  ADD KEY `idx_employee_id` (`employee_id`),
  ADD KEY `idx_date` (`date`);

--
-- Indexes for table `employees`
--
ALTER TABLE `employees`
  ADD PRIMARY KEY (`Employee_ID`);

--
-- Indexes for table `password_history`
--
ALTER TABLE `password_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `payroll`
--
ALTER TABLE `payroll`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_employee_id` (`employee_id`),
  ADD KEY `idx_month_year` (`month`,`year`),
  ADD KEY `idx_processed_date` (`processed_date`);

--
-- Indexes for table `security_logs`
--
ALTER TABLE `security_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accounts`
--
ALTER TABLE `accounts`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `attendance`
--
ALTER TABLE `attendance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `password_history`
--
ALTER TABLE `password_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `payroll`
--
ALTER TABLE `payroll`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `security_logs`
--
ALTER TABLE `security_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `password_history`
--
ALTER TABLE `password_history`
  ADD CONSTRAINT `password_history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `accounts` (`ID`) ON DELETE CASCADE;

--
-- Constraints for table `security_logs`
--
ALTER TABLE `security_logs`
  ADD CONSTRAINT `security_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `accounts` (`ID`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
