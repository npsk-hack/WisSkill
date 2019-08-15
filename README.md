# WisSkill
#### National Public School, Rajajinagar
A student-teacher portal. One of its main features is a forum where students can ask their doubts, and the teachers can clarify them. Each student will have a unique account that is linked to the teachers handling the class (including the class teacher). The website will give a time-bound test each week, created by the teachers. The marks will automatically be calculated and shown. At the end of the allotted time, all of the students' marks will be submitted to their respective class teachers and they will be saved in a database, ready to access at any point of time. The teacher can search for the student’s marks by simply entering their name. The website will also have additional features such as report cards and leader boards.


# Setup
### pip
Install pip. Tutorial on how to do this can be found at https://www.liquidweb.com/kb/install-pip-windows/
Make sure that pip is installed in the dir in which the web-app is present.
Run pip install -r requirements.txt in the dir in which requirements.txt is present to install the python dependencies.
### Node JS
Install Node JS on your computer.
Navigate to WisSkill\app\nodejs.
Use npm install to install all the nodejs dependancies.
### SQL
Run both the setup files in the databases folder in the app folder.

#### NOTE:
Base Code has two bugs. One: After enterring all the data in the register page, it does not take you bake to the login page. Clicking submit twice will submit the same request twice. Two: The aproval and deletion of registration requests in home page when logged in as admin does not work.
