USE wizlearn;
#SELECT * FROM admins WHERE 1=0;
#Date is in MMDDYYYY Format
INSERT INTO students 
VALUES ('Samarth M', 'samarthm', 8, 'D', 60015, 'Math', 'Indian Music'),
	   ('Aditya K', 'adityak', 10, 'A', 52912, 'Heritage', 'Western Music'),
       ('Raaghav O', 'raaghavo', 10, 'C', 59991, 'Computer Science', 'Art');
INSERT INTO teachers
VALUES ('Malathy R Narayan','malathirn','false','{"11A" : "Biology", "12B" : "Biology", "10C" : "Chemistry"}', 001),
	   ('Veena L','veenal','6B','{"6B" : "English", "6A" : "English", "7D" : "English", "8C" : "English", "2D" : "Life Skills"}', 093),
       ('Poornima C','poornimac','false','{"all":"Yoga"}', 143);
#{all:yoga} means she teaches to all classes
#{8:yoga} means she teaches to all 8th grade classes
INSERT INTO admins
VALUES (0, 'anirudh', 'creator', 'Anirudh', 1),
	   (1, 'vaibhav', 'creator', 'Vaibhav', 1),
       (2, 'archith', 'creator', 'Archith', 1),
	   (3, 'npsrnr', 'main_admin', 'Malathy R Narayan', 2);
SELECT * FROM students;
SELECT * FROM teachers;
SELECT * FROM admins;