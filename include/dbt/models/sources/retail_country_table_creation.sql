CREATE TABLE IF NOT EXISTS `retail.country` (
  `id` INT NOT NULL,
  `iso` STRING NOT NULL,
  `name` STRING NOT NULL,
  `nicename` STRING NOT NULL,
  `iso3` STRING DEFAULT NULL,
  `numcode` INT DEFAULT NULL,
  `phonecode` INT NOT NULL,
);