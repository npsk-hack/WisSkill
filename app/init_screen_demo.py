from flask import Flask
import mysql.connector
import json
from mysql.connector import Error
from flask import render_template, redirect, url_for, request,send_from_directory, session

app = Flask(__name__,template_folder='templates',static_url_path='/css/styles.css')

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
            
if __name__ == "__main__":
    app.run(debug = True)


