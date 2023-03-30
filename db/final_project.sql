-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 09, 2023 at 03:21 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `final_project`
--

-- --------------------------------------------------------

--
-- Table structure for table `loss_threshold`
--

CREATE TABLE `loss_threshold` (
  `threshold_id` int(11) NOT NULL,
  `threshold_success` float NOT NULL,
  `threshold_warning` float NOT NULL,
  `threshold_danger` float NOT NULL,
  `threshold_status` int(11) NOT NULL,
  `threshold_dt` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `loss_threshold`
--

INSERT INTO `loss_threshold` (`threshold_id`, `threshold_success`, `threshold_warning`, `threshold_danger`, `threshold_status`, `threshold_dt`) VALUES
(1, -8, -24, -27, 1, '2023-01-09 02:21:40');

-- --------------------------------------------------------

--
-- Table structure for table `olt`
--

CREATE TABLE `olt` (
  `olt_id` int(11) NOT NULL,
  `olt_power` float NOT NULL,
  `olt_dt` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `olt_status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `olt`
--

INSERT INTO `olt` (`olt_id`, `olt_power`, `olt_dt`, `olt_status`) VALUES
(1, 3, '2023-01-08 11:45:51', 1);

-- --------------------------------------------------------

--
-- Table structure for table `tbl_marker`
--

CREATE TABLE `tbl_marker` (
  `marker_id` int(11) NOT NULL,
  `marker_name` varchar(100) NOT NULL,
  `lat` float NOT NULL,
  `lng` float NOT NULL,
  `splitter_id` int(11) NOT NULL,
  `remain_slot` int(11) NOT NULL,
  `marker_dt` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_project`
--

CREATE TABLE `tbl_project` (
  `project_id` int(11) NOT NULL,
  `project_name` varchar(100) NOT NULL,
  `user_id` int(11) NOT NULL,
  `distance` float NOT NULL,
  `olt_power` float NOT NULL,
  `splitter` varchar(200) NOT NULL,
  `connector` int(11) NOT NULL,
  `splice` int(11) NOT NULL,
  `project_dt` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `loss_budget` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_project`
--

INSERT INTO `tbl_project` (`project_id`, `project_name`, `user_id`, `distance`, `olt_power`, `splitter`, `connector`, `splice`, `project_dt`, `loss_budget`) VALUES
(1, 'Test', 1, 1.012, 3, '[{\"splitter\":\"1:4\",\"loss\":\"7.2\"},{\"splitter\":\"1:8\",\"loss\":\"10.5\"}]', 4, 6, '2023-01-09 01:30:24', -18.6542);

-- --------------------------------------------------------

--
-- Table structure for table `tbl_role`
--

CREATE TABLE `tbl_role` (
  `role_id` int(11) NOT NULL,
  `role_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_role`
--

INSERT INTO `tbl_role` (`role_id`, `role_name`) VALUES
(1, 'admin'),
(2, 'manager'),
(3, 'staff');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_splitter`
--

CREATE TABLE `tbl_splitter` (
  `splitter_id` int(11) NOT NULL,
  `splitter_type` varchar(100) NOT NULL,
  `splitter_value` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_splitter`
--

INSERT INTO `tbl_splitter` (`splitter_id`, `splitter_type`, `splitter_value`) VALUES
(1, '1:2', 4),
(2, '1:4', 7.2),
(3, '1:8', 10.5),
(4, '1:16', 13.8),
(5, '1:32', 17),
(6, '1:64', 20.5);

-- --------------------------------------------------------

--
-- Table structure for table `tbl_user`
--

CREATE TABLE `tbl_user` (
  `user_id` int(11) NOT NULL,
  `fname` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `pwd` varchar(200) NOT NULL,
  `line_userID` varchar(200) NOT NULL,
  `role_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_user`
--

INSERT INTO `tbl_user` (`user_id`, `fname`, `email`, `pwd`, `line_userID`, `role_id`) VALUES
(1, 'admin', 'admin@mail.com', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', '', 1),
(2, 'manager ', 'manager@mail.com', '6ee4a469cd4e91053847f5d3fcb61dbcc91e8f0ef10be7748da4c4a1ba382d17', '', 2),
(3, 'staff', 'staff@mail.com', '1562206543da764123c21bd524674f0a8aaf49c8a89744c97352fe677f7e4006', '', 3);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `loss_threshold`
--
ALTER TABLE `loss_threshold`
  ADD PRIMARY KEY (`threshold_id`);

--
-- Indexes for table `olt`
--
ALTER TABLE `olt`
  ADD PRIMARY KEY (`olt_id`);

--
-- Indexes for table `tbl_marker`
--
ALTER TABLE `tbl_marker`
  ADD PRIMARY KEY (`marker_id`);

--
-- Indexes for table `tbl_project`
--
ALTER TABLE `tbl_project`
  ADD PRIMARY KEY (`project_id`);

--
-- Indexes for table `tbl_role`
--
ALTER TABLE `tbl_role`
  ADD PRIMARY KEY (`role_id`);

--
-- Indexes for table `tbl_splitter`
--
ALTER TABLE `tbl_splitter`
  ADD PRIMARY KEY (`splitter_id`);

--
-- Indexes for table `tbl_user`
--
ALTER TABLE `tbl_user`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `loss_threshold`
--
ALTER TABLE `loss_threshold`
  MODIFY `threshold_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `olt`
--
ALTER TABLE `olt`
  MODIFY `olt_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `tbl_marker`
--
ALTER TABLE `tbl_marker`
  MODIFY `marker_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_project`
--
ALTER TABLE `tbl_project`
  MODIFY `project_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `tbl_role`
--
ALTER TABLE `tbl_role`
  MODIFY `role_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `tbl_splitter`
--
ALTER TABLE `tbl_splitter`
  MODIFY `splitter_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `tbl_user`
--
ALTER TABLE `tbl_user`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
