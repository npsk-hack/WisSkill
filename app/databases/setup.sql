DROP DATABASE IF EXISTS wizlearn;
CREATE DATABASE wizlearn;
USE wizlearn;
CREATE TABLE students(
	name_of_student VARCHAR(255) NOT NULL,
    username_of_student VARCHAR(255) NOT NULL,
    class_of_student INTEGER NOT NULL,
    section_of_student VARCHAR(1) NOT NULL,
    admission_no INTEGER NOT NULL PRIMARY KEY,
    elective_club VARCHAR(255),
    elective_vpa VARCHAR(255)
)  ENGINE = INNODB;

CREATE TABLE teachers(
	name_of_teacher VARCHAR(255) NOT NULL,
    username_of_teacher VARCHAR(255) NOT NULL,
    class_teacher VARCHAR(5),
    teacher_id INTEGER NOT NULL PRIMARY KEY
);

CREATE TABLE admins(
	id INTEGER NOT NULL PRIMARY KEY,
    `password` VARCHAR(255) NOT NULL,
    username_of_admin VARCHAR(255) NOT NULL,
    name_of_admin VARCHAR(255) NOT NULL,
    level_of_access INTEGER NOT NULL
);

CREATE TABLE subjects(
	id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `subject` VARCHAR(20) NOT NULL,
    grade INTEGER(2) NOT NULL,
    section VARCHAR(1) NOT NULL,
    teacher_id INTEGER NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
) ENGINE = INNODB;

CREATE TABLE doubts(
	id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `subject` VARCHAR(100) NOT NULL,
    question TEXT NOT NULL,
    student INTEGER NOT NULL,
    teacher INTEGER NOT NULL,
    answer TEXT,
    FOREIGN KEY (student) REFERENCES students(admission_no),
    FOREIGN KEY (teacher) REFERENCES teachers(teacher_id)
) ENGINE = INNODB;

# 18:48:21	CREATE TABLE subjects(  id INTEGER NOT NULL PRIMARY KEY,     `subject` VARCHAR(20) NOT NULL,     grade INTEGER(2) NOT NULL,     section VARCHAR(1) NOT NULL,     teacher VARCHAR(100) NOT NULL,     FOREIGN KEY (teacher) REFERENCES teachers(teacher_id) )	Error Code: 1215. Cannot add foreign key constraint	0.953 sec
