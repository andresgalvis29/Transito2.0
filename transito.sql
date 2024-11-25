-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: appDB
-- Generation Time: Feb 05, 2024 at 04:00 AM
-- Server version: 8.3.0
-- PHP Version: 8.2.15

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `transito`
--

-- --------------------------------------------------------

--
-- Table structure for table `Carro`
--

CREATE TABLE `Carro` (
  `idCarro` varchar(6) COLLATE utf8mb4_general_ci NOT NULL,
  `Concesionario` varchar(45) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Motor` int DEFAULT NULL,
  `FechadeFabricacion` varchar(45) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Conductor_idConductor` int NOT NULL,
  `Marca_idMarca` varchar(45) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Conductor`
--

CREATE TABLE `Conductor` (
  `idConductor` int NOT NULL,
  `NombreConductor` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  `FechaNacimientoConductor` date NOT NULL,
  `DireccionConductor` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  `CelularConductor` varchar(45) COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Marca`
--

CREATE TABLE `Marca` (
  `idMarca` varchar(45) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Multa`
--

CREATE TABLE `Multa` (
  `CodigoMulta` int NOT NULL,
  `ArticuloInfringido` varchar(45) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Diamulta` date NOT NULL,
  `ValorMulta` int DEFAULT NULL,
  `DescripcionMulta` varchar(300) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Conductor_idConductor` int NOT NULL,
  `Policia_Usuario` varchar(30) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Policia`
--

CREATE TABLE `Policia` (
  `Usuario` varchar(30) COLLATE utf8mb4_general_ci NOT NULL,
  `Contraseña` varchar(40) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `NombrePolicia` varchar(45) COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Policia`
--

INSERT INTO `Policia` (`Usuario`, `Contraseña`, `NombrePolicia`) VALUES
('andres', 'dc76e9f0c0006e8f919e0c515c66dbba3982f785', 'Andres Galvis');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Carro`
--
ALTER TABLE `Carro`
  ADD PRIMARY KEY (`idCarro`),
  ADD UNIQUE KEY `idCarro_UNIQUE` (`idCarro`),
  ADD KEY `fk_Carro_Conductor_idx` (`Conductor_idConductor`),
  ADD KEY `Marca_idMarca` (`Marca_idMarca`);

--
-- Indexes for table `Conductor`
--
ALTER TABLE `Conductor`
  ADD PRIMARY KEY (`idConductor`),
  ADD UNIQUE KEY `idConductor` (`idConductor`);

--
-- Indexes for table `Marca`
--
ALTER TABLE `Marca`
  ADD PRIMARY KEY (`idMarca`),
  ADD UNIQUE KEY `Marca` (`idMarca`);

--
-- Indexes for table `Multa`
--
ALTER TABLE `Multa`
  ADD PRIMARY KEY (`CodigoMulta`),
  ADD KEY `fk_Multa_Conductor1_idx` (`Conductor_idConductor`),
  ADD KEY `fk_Multa_Policia1_idx` (`Policia_Usuario`);

--
-- Indexes for table `Policia`
--
ALTER TABLE `Policia`
  ADD PRIMARY KEY (`Usuario`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
