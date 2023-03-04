-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: db:3306
-- Generation Time: Dec 07, 2022 at 08:58 PM
-- Server version: 5.7.40
-- PHP Version: 8.0.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `app_db`
--

-- --------------------------------------------------------


CREATE TABLE `Orase` (
  `id` int(11) PRIMARY KEY AUTO_INCREMENT,
  `id_tara` int(11) NOT NULL,
  `nume_oras` varchar(100) NOT NULL,
  `latitudine` double NOT NULL,
  `longitudine` double NOT NULL,
   CONSTRAINT KEY_ORASE UNIQUE (`id_tara`,`nume_oras`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `Tari` (
  `id` int(11) PRIMARY KEY AUTO_INCREMENT,
  `nume_tara` varchar(100) UNIQUE,
  `latitudine` double NOT NULL,
  `longitudine` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `Temperaturi` (
  `id` int(11) PRIMARY KEY AUTO_INCREMENT,
  `valoare` double NOT NULL,
  `timestamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `id_oras` int(11) NOT NULL,
   CONSTRAINT KEY_TEMP UNIQUE (`timestamp`,`id_oras`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
