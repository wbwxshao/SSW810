""" Homework 11
    Xueshi Wang
    11.09.2018
""" 

import sqlite3
from prettytable import PrettyTable

database = r'C:\Users\Administrator\Documents\GitHub\SSW810\HW11_XW.db'
db = sqlite3.connect(database)
sql_command = "select CWID, Name, Dept, Course, count(*) as number_students from HW11_grades gra join HW11_instructors ins on ins.CWID = gra.Instructor_CWID group by Course"
ins_pt = PrettyTable(field_names = ['CWID', 'Name', 'Dept', 'Course', 'number_students'])
for row in db.execute(sql_command):
    ins_pt.add_row(row)
print(ins_pt)