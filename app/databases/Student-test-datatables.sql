CREATE TABLE `TestData` (
  `test_no` INT NOT NULL,
  `question_no` INT NOT NULL,
  `question` VARCHAR(1000) NULL,
  `option_a` VARCHAR(200) NULL,
  `option_b` VARCHAR(200) NULL,
  `option_c` VARCHAR(200) NULL,
  `option_d` VARCHAR(200) NULL,
  `correct_option` CHAR(1) NULL,
  PRIMARY KEY (`test_no`, `question_no`));

CREATE TABLE `Tests` (
  `test_no` INT NOT NULL,
  `teacher_id` INT NOT NULL,
  PRIMARY KEY (`test_no`));
  
CREATE TABLE `StudentTestData` (
`questionno` INT NOT NULL,
`submitted_ans` VARCHAR(1) NULL
);
  
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

