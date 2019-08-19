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

def findStudentDetails(admission_no):
    connection = mysql.connector.connect(host='127.0.0.1',database='wizlearn',user='root',password='pokemon2345')
    cursor = connection.cursor(buffered=True)
    sql = 'SELECT * FROM students s WHERE s.admission_no = {0}'.format(admission_no)
    cursor.execute(sql)
    details = list(sum(cursor.fetchall(), ()))
    cursor.close()
    connection.close()
    return details

def findDoubtsConcerningMe(idt):
    connection = mysql.connector.connect(host='127.0.0.1',database='wizlearn',user='root',password='pokemon2345')
    cursor = connection.cursor(buffered=True)
    sql = 'SELECT * FROM doubts d WHERE d.teacher = {0}'.format(idt)
    cursor.execute(sql)
    doubts = list(cursor.fetchall())
    cursor.close()
    connection.close()
    return doubts    

def checkforAnsweredDoubts():
    connection = mysql.connector.connect(host='127.0.0.1',database='wizlearn',user='root',password='pokemon2345')
    cursor = connection.cursor(buffered=True)
    cursor.execute('SELECT * FROM doubts WHERE answer IS NOT NULL')
    result = list(cursor.fetchall())
    cursor.close()
    connection.close()
    return result

@app.route("/")
def hello():
    return render_template('login.html')

@app.route("/admin_forum")
def admin_forum():
    return render_template('admin_forum.html')

@app.route("/forum")
def forum():
    try:
        login = session['category']
    except KeyError:
        return 'You are not logged in'
    app.logger.debug(login)
    if login == 'Teacher':
        return redirect('http://127.0.0.1:5000/teacher_doubts_answer')
    elif login == 'Student':
        return redirect('http://127.0.0.1:5000/doubts')
    elif login == 'Admin':
        return redirect('http://127.0.0.1:5000/admin_forum')
    return 'You are not logged in'

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route("/Hi")
def hello1():
    return "Hello Anirudh"

@app.route('/doubts')
def returnDoubts():
    answeredDoubts = checkforAnsweredDoubts()
    if len(answeredDoubts) == 0:
        status = False
    else:
        status = True
    app.logger.debug(answeredDoubts)
    answeredDoubts = json.dumps(answeredDoubts)
    return render_template('doubts.html', status=status, doubts=answeredDoubts)

@app.route('/open_test')
def open_test():
    try:
        login = session['category']
        app.logger.debug(login)
    except KeyError:
        return 'You are not logged in'
    app.logger.debug(login)
    if login == 'Student':
        return redirect('http://127.0.0.1:5000/take_test')
    elif login == 'Admin':
        return redirect('http://127.0.0.1:5000/set_test')
    elif login == 'Teacher':
        return 'We are sorry, but for practical purposes, only the school admins can set tests.'
    return 'You are not logged in'

@app.route('/take_test')
def take_test():
    return render_template('test.html')

@app.route('/set_test')
def set_test():
    return render_template('set_test.html')


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
                session['category']= 'Admin'
                with open('C:/Users/Anirudh/Desktop/Hackathon/app/nodejs/admin.json', 'w') as file:
                    y = json.dumps(True)
                    file.write(y)
                app.logger.debug(session['admin_level'])
            elif category=="Student":
                cursor.execute("SELECT * FROM students WHERE admission_no = {0}".format(password))
                data = list(sum(cursor.fetchall(),()))
                session['login'] = data
                session['category']= 'Student'
            elif category=="Teacher":
                cursor.execute("SELECT * FROM teachers WHERE teacher_id= {0}".format(password))
                data = list(sum(cursor.fetchall(),()))
                session['login'] = data
                session['category']= 'Teacher'
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

@app.route('/add_doubt', methods=["GET","POST"])
def add_doubt():
    if request.method == "POST":
        app.logger.debug(request.form)
        subject = request.form['subject']
        doubt = request.form['doubt']
        connection = mysql.connector.connect(host='127.0.0.1',database='wizlearn',user='root',password='pokemon2345')
        cursor = connection.cursor(buffered=True)
        student_details = session['login']
        admission_no = student_details[4]
        grade = student_details[2]
        section = student_details[3]
        app.logger.debug(admission_no)
        sqlt = "SELECT s.teacher_id FROM subjects s WHERE s.grade = {0} AND s.section = '{1}' AND s.subject = '{2}';".format(grade,section,subject)
        cursor.execute(sqlt)
        app.logger.debug(sqlt)
        teacher = list(sum(cursor.fetchall(), ())) 
        app.logger.debug(teacher)
        sql = "INSERT INTO doubts (subject,question,student,teacher) VALUES ('{0}','{1}', {2}, {3});".format(subject,doubt,admission_no,teacher[0])
        app.logger.debug(sql)
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()
        return render_template('doubts.html')

@app.route('/teacher_doubts_answer')
def teacher_doubts_answer():
    connection = mysql.connector.connect(host='127.0.0.1',database='wizlearn',user='root',password='pokemon2345')
    cursor = connection.cursor(buffered=True)
    if len(session['login']) == 4:
        validication = True
    else:
        validication = False
        return 'You are not a teacher. Please Exit immidiately, or your computer will be infected with a deadly virus... Even if you are the admin, you cannot access this page as your sheer presence would crash the website'
    teacher_details = session['login']
    teacher_id = teacher_details[3]
    doubts = findDoubtsConcerningMe(teacher_id)
    doubtsLength = len(doubts)

    class Student:
        def __init__(self,name,grade,section,admission_no):
            self.name = name
            self.grade = grade
            self.section = section
            self.admission_no = admission_no

    class Teacher:
        def __init__(self,name,teacher_id):
            self.name = name
            self.teacher_id = teacher_id
    
    class Content:
        def __init__(self,doubt,subject,cid):
            self.doubt = doubt
            self.subject = subject
            self.id = cid

    class Doubt:
        def __init__(self,student,teacher,content):
            self.student = student
            self.teacher = teacher
            self.content = content
    
    array = []
    app.logger.debug(doubts)
    for i in doubts:
        app.logger.debug("I IS ")
        app.logger.debug(i)
        cursor.execute('SELECT * FROM students WHERE admission_no = {0}'.format(i[3]))
        s = list(sum(cursor.fetchall(),()))
        ss = Student(s[0],s[2],s[3],s[4])
        cursor.execute('SELECT * FROM teachers WHERE teacher_id = {0}'.format(i[4]))
        t = list(sum(cursor.fetchall(),()))
        tt = Teacher(t[0],t[3])
        cc = Content(i[2],i[1],i[0])
        dd = Doubt(ss,tt,cc)
        array.append(dd)
        s.clear()
        del ss
        t.clear()
        del tt
        del cc
        del dd

    cursor.close()
    connection.close()
    return render_template('answer_questions.html', array=array, no_ofDoubts=len(array))

@app.route('/answer_doubt', methods=['POST','GET'])
def addAnswer():
    if request.method=="POST":
        dId = request.form['id']
        ans = request.form['answer']
        app.logger.debug(dId)
        connection = mysql.connector.connect(host='127.0.0.1',database='wizlearn',user='root',password='pokemon2345')
        cursor = connection.cursor(buffered=True)
        cursor.execute("UPDATE doubts d SET d.answer = '{0}' WHERE d.id = {1}".format(ans,dId))
        connection.commit()
        cursor.close()
        connection.close()
        return "HI"

#SETTING UP OF QUESTION PAPER BY TEACHER
@app.route('/question_paper', methods=["GET","POST"])
def questionpaper():
    app.logger.debug('Entered')
    connection = mysql.connector.connect(
        host="localhost",
        port="3306",
        database='wizlearn',
        user='root',
        password='DkFjGh10#',
       )
    cursor = connection.cursor(buffered=True)
    app.logger.debug("Am here Cursor connection")
    error = None
    try:

        if request.method == 'POST':
            app.logger.debug("Inside Set question paper POST")
            
                                  
            cursor.execute("SELECT max(test_no)+1 as maxtestno FROM testdata")
                        
            records = cursor.fetchall()
            for row in records:
                maxtestno = row[0]
            if maxtestno == None:
                maxtestno = 1
                
            app.logger.debug(maxtestno)          
            question = request.form.getlist('question[]')
            app.logger.debug(question)
            option_a = request.form.getlist('option_a[]')
            app.logger.debug(option_a)
            option_b = request.form.getlist('option_b[]')
            app.logger.debug(option_b) 
            option_c = request.form.getlist('option_c[]')
            app.logger.debug(option_c)
            option_d = request.form.getlist('option_d[]')
            app.logger.debug(option_d)
            correct_option = request.form.getlist('correct_option[]')
            app.logger.debug(correct_option)
            app.logger.debug(len(question))
            
            for i in range(len(question)):
                cursor.execute("INSERT INTO TestData VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (maxtestno,i+1,question[i].strip(),option_a[i].strip(),option_b[i].strip(),option_c[i].strip(),option_d[i].strip(),correct_option[i]))            
            connection.commit()
            if (connection.is_connected()):
                    connection.close()
                    cursor.close()
                    app.logger.debug("MySQL is closed")
            return render_template('success.html')
    
    except error as e:
        app.logger.debug ("Error while executing SQL", e)
        return render_template('testsetting.html')
             
    finally:
        if (connection.is_connected()):
                connection.close()
                cursor.close()
                app.logger.debug("MySQL is closed")

@app.route('/home')
def home():
    return render_template('home.html')

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

	
	my db = mysql.connector.connect(host="localhost ", user = "root", password = "pokemon2345", database = "wizlearn")
	
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
	
	
	my db = mysql.connector.connect(host="localhost ", user = "root", password = "pokemon2345", database = "wizlearn")
	
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

