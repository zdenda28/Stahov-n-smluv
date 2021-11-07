CREATE TABLE `dodavatele` (
	`ico` BIGINT NOT NULL,
	`nace` VARCHAR(1000) NOT NULL,
	`ict_supplier` BOOLEAN NOT NULL COMMENT '1 = dodavatel ITC',
	PRIMARY KEY (`ico`)
) ENGINE=InnoDB;

INSERT INTO dodavatele (ico, nace, ict_supplier)
VALUES (45454, 45454, 1); 