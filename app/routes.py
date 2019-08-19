from app import app
import mysql.connector
from mysql.connector import Error
import json
from flask import render_template, redirect, url_for, request,send_from_directory, session
app.config['SECRET_KEY'] = 'you-will-never-guess'

#To get date in DDMMYYYY Format:
#   import datetime
#   from dateutil.relativedelta import relativedelta
#
#   date = datetime.datetime.now()
#   date_formated = one_year_from_now.strftime("%d/%m/%Y")
#   print date_formated



@app.route("/")
def hello():
    return "Hello World!"

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route("/Hi")
def hello1():
    return "Hello Anirudh"

@app.route("/login", methods=["GET","POST"])
def login():
    app.logger.debug('Enterred')
    connection = mysql.connector.connect(
        host="localhost",
        port="3306",
        database='wizlearn',
        user='root',
        password='pokemon2345'
    )
    cursor = connection.cursor(buffered=True)

    error = None

    if request.method == 'POST':
        app.logger.debug("Inside login POST")

        username = request.form['username']
        category = request.form['category']
        password = request.form['password']
        string = "Username is {0}, password is {1} and category is {2}"
        string = string.format(username,password,category)
        app.logger.debug(string)

        if category == 'Student':
            try:
                password = int(password)
            except ValueError:
                return render_template('login.html')
            cursor.execute("SELECT username_of_student FROM students")
            usernames = list(sum(cursor.fetchall(), ()))    
            cursor.execute("SELECT admission_no FROM students")
            passwords = list(sum(cursor.fetchall(), ()))
            for row in usernames:
                if row == username:
                    for password_row in passwords:
                        if password_row == password:
                            validication = True
        elif category == 'Teacher':
            try:
                password = int(password)
            except ValueError:
                return render_template('login.html')
            cursor.execute("SELECT username_of_teacher FROM teachers")
            usernames = list(sum(cursor.fetchall(), ()))
            cursor.execute("SELECT teacher_id FROM teachers")
            passwords = list(sum(cursor.fetchall(), ()))
            for row in usernames:
                if row == username:
                    for password_row in passwords:
                        if password_row == password:
                            validication = True
        elif category == 'Administrator':
            cursor.execute("SELECT username_of_admin FROM admins")
            usernames = list(sum(cursor.fetchall(), ()))
            cursor.execute("SELECT password FROM admins")
            passwords = list(sum(cursor.fetchall(), ()))
            for row in usernames:
                if row == username:
                    for password_row in passwords:
                        if password_row == password:
                            validication = True
        else:
            app.logger.debug("Error")

        try:
            if validication != True:
                validication = False
        except NameError:
            app.logger.debug("Incorrect login")           
            validication = False
        
        if validication == True:
            if category=="Administrator":
                cursor.execute("SELECT level_of_access FROM admins WHERE username_of_admin = '{0}' AND password = '{1}'".format(username, password))
                level_of_access = list(sum(cursor.fetchall(), ()))
                session['login'] = "Admin"
                session['admin_level'] = level_of_access
                with open('C:/Users/Anirudh/Desktop/Hackathon/app/nodejs/admin.json', 'w') as file:
                    y = json.dumps(True)
                    file.write(y)
                app.logger.debug(session['admin_level'])
            elif category=="Student":
                cursor.execute("SELECT * FROM students WHERE admission_no = {0}".format(password))
                data = list(sum(cursor.fetchall(),()))
                session['login'] = data
            elif category=="Teacher":
                cursor.execute("SELECT * FROM teachers WHERE teacher_id= {0}".format(password))
                data = list(sum(cursor.fetchall(),()))
                session['login'] = data
            cursor.close()
            connection.close()

            return render_template("home.html")

    cursor.close()
    connection.close()


    #return redirect(url_for('home'))
    return render_template('login.html')

@app.route("/TestDBConnection")
def testDB():
    try:
        connection = mysql.connector.connect(host='127.0.0.1',database='school_py',user='root',password='pokemon2345')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL database... MySQL Server version on ",db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print ("Your connected to - ", record)
    except Exception as e:
        print ("Error while connecting to MySQL", e)
    finally:
        if(connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed") 


@app.route('/register')
def renderRegister():
    if 'admin_level' in session:
        if session['admin_level'] == 1 or session['admin_level'] == 2:
            app.logger.debug("You are admin. Returning admin_add_users")
            return render_template('admin_add_users.html')
    app.logger.debug("Going to register page")
    return render_template('register.html')

@app.route('/teacher_student_registration', methods=["GET", "POST"])
def renderStudentTeacherRegister():
    if request.method == 'POST':
        app.logger.debug(request.form)
        category = request.form['category']
        if category == "Student":
            return render_template('new_student.html')
        return render_template('new_teacher.html')
    else:
        return "Hi this is GET"

@app.route('/test')
def test():
    with open('C:/Users/Anirudh/Desktop/Hackathon/app/nodejs/admin.json', 'w') as file:
        y = json.dumps(True)
        file.write(y)
    return "Done"

@app.route('/logout')
def logout():
    try:
        app.logger.debug(session['login'])
        session.clear()
        with open('C:/Users/Anirudh/Desktop/Hackathon/app/nodejs/admin.json', 'w') as file:
            y = json.dumps(False)
            file.write(y)    
        #app.logger.debug(session['login'])
        return render_template('login.html')
    except KeyError:
        return render_template('login.html')
    return "Error"



@app.route('/submittest')
def answer_check() :
	
	
	my db = mysql.connector.connect(host="localhost ", user = "root", passwd = "insertpassword", database = "wizlearn")
	
	my cursor.execute("SELECT submittedans FROM StudentTestData")
	x = str(mycursor.fetchall())
	app.logger.debug(wm)
	
	my cursor.execute("SELECT correctans FROM StudentTestData")
	y = str(mycursor.fetchall())
	app.logger.debug(wm)
	
	
	for a,b in zip(x,y):
		if a==b :
			score+=1
	return score

@app.route('/demo')
def updatequestion() :
	
	
	my db = mysql.connector.connect(host="localhost ", user = "root", passwd = "insertpassword", database = "wizlearn")
	
	my cursor.execute("SELECT question_no FROM TestData  WHERE test_no = (SELECT max(test_no) from TestData)")
	question_no = list(mycursor.fetchall())
	
	my cursor.execute("SELECT question FROM TestData WHERE test_no = (SELECT max(test_no) from TestData) ")
	question = list(mycursor.fetchall())
	
	my cursor.execute("SELECT option_a FROM TestData WHERE test_no = (SELECT max(test_no) from TestData) ")
	option_a = list(mycursor.fetchall())
	
	my cursor.execute("SELECT option_b FROM TestData WHERE test_no = (SELECT max(test_no) from TestData) ")
	option_b = list(mycursor.fetchall())
	
	my cursor.execute("SELECT option_c FROM TestData WHERE test_no = (SELECT max(test_no) from TestData) ")
	option_c = list(mycursor.fetchall())
	
	my cursor.execute("SELECT option_d FROM TestData WHERE test_no = (SELECT max(test_no) from TestData) ")
	option_d = list(mycursor.fetchall())
	
	return question_no , question , option_a , option_b , option_c , option_d
;
