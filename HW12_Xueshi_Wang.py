""" Homework 12
    Xueshi Wang
    11.16.2018
    Last Python homework!
""" 

from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/') #default page
def course():
    DB_file = r'D:\stevens\ssw 810\sqlite-tools-win32-x86-3250300\HW11_XW.db'
    query = 'select CWID, Name, Dept, Course, count(*) as number_students from HW11_grades gra join HW11_instructors ins on ins.CWID = gra.Instructor_CWID group by Course, ins.CWID, ins.Name, ins.Dept'
    db = sqlite3.connect(DB_file)
    results = db.execute(query)

    data = [{'CWID': CWID, 'Name': Name, 'Dept': Dept, 'Course': Course, 'number_students': number_students}
            for CWID, Name, Dept, Course, number_students in results]
    db.close()

    return render_template('instructor.html',
                            title = 'Stevens Repository',
                            table_title = 'Number of students by course and instructor',
                            instructors = data)
app.run(debug= True)