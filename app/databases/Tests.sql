CREATE TABLE `TestData` (
  `test_no` INT NOT NULL,
  `question_no` INT NOT NULL,
  `question` VARCHAR(1000) NULL,
  `option_a` VARCHAR(85) NULL,
  `option_b` VARCHAR(85) NULL,
  `option_c` VARCHAR(85) NULL,
  `option_d` VARCHAR(85) NULL,
  `correct_option` CHAR(1) NULL,
  PRIMARY KEY (`test_no`, `question_no`))
