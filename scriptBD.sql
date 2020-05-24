-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema psd
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema psd
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `psd` DEFAULT CHARACTER SET latin1 ;
USE `psd` ;

-- -----------------------------------------------------
-- Table `psd`.`celula`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `psd`.`celula` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `referencia` VARCHAR(10) NULL,
  `latCentral` DOUBLE NULL,
  `logCentral` DOUBLE NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `psd`.`corrida`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `psd`.`corrida` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `identificadorTaxi` VARCHAR(45) NOT NULL,
  `data_horaSaida` DATETIME NOT NULL,
  `data_horaChegada` DATETIME NOT NULL,
  `distancia` DOUBLE NOT NULL,
  `duracao` DOUBLE NULL,
  `valorTarifa` DOUBLE NULL,
  `sobretaxa` DOUBLE NULL,
  `imposto` DOUBLE NULL,
  `gorjeta` DOUBLE NULL,
  `valorTotal` DOUBLE NOT NULL,
  `latInicio` DOUBLE NOT NULL,
  `logInicio` DOUBLE NOT NULL,
  `latFim` DOUBLE NOT NULL,
  `logFim` DOUBLE NOT NULL,
  `id_celula_inicio` INT NOT NULL,
  `id_celula_fim` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_corrida_celula_idx` (`id_celula_inicio` ASC),
  INDEX `fk_corrida_celula1_idx` (`id_celula_fim` ASC),
  CONSTRAINT `fk_corrida_celula`
    FOREIGN KEY (`id_celula_inicio`)
    REFERENCES `psd`.`celula` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_corrida_celula1`
    FOREIGN KEY (`id_celula_fim`)
    REFERENCES `psd`.`celula` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
