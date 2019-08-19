CREATE TABLE `wizlearn`.`student_test` (
  `admission_no` INT NOT NULL,
  `test_no` INT NOT NULL,
  `test_marks` INT NULL,
  PRIMARY KEY (`admission_no`, `test_no`),
  CONSTRAINT `admission_no`
    FOREIGN KEY (`admission_no`)
    REFERENCES `wizlearn`.`students` (`admission_no`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `test_no`
    FOREIGN KEY (`test_no`)
    REFERENCES `wizlearn`.`testdata` (`test_no`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);