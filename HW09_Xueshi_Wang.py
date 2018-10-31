""" Homework 09
    Xueshi Wang
    10.26.2018
"""
import os
from collections import defaultdict
from prettytable import PrettyTable
import unittest

class Repository:
    def __init__(self, dir_path):
        """Hold all the data files"""
        
        self.student_path = os.path.join(dir_path, 'students.txt')
        self.instructor_path = os.path.join(dir_path, 'instructors.txt')
        self.grade_path = os.path.join(dir_path, 'grades.txt')
        self.student = dict()   # students[cwid] = Student(cwid, name, major)
        self.instructor = dict()
        
        self.feed_student()
        self.feed_instructor()

    def feed_student(self):
        """Feed data to student class and print the pretty table"""
        try:
            fp = open(self.student_path, 'r')
        except FileNotFoundError:
            raise FileNotFoundError('Error! Cannot open the student.txt file', self.student_path)
        else:
            with fp:         
                for line in fp:
                    line = line.strip().split('\t')
                    self.student[line[0]] = Student(line[0], line[1], line[2])
        try:
            file = open(self.grade_path, 'r')
        except FileNotFoundError:
            raise FileNotFoundError('Error! Cannot open the grades.txt file', self.grade_path)
        else:
            with file:                
                for grade_line in file:
                    grade_line = grade_line.strip().split('\t')
                    try:
                        self.student[grade_line[0]].course_grade(grade_line[1], grade_line[2])
                    except KeyError:
                        raise KeyError("Grade file has a student ID that does not exist!")
            self.table_stu(self.student)

    def table_stu(self, stu):
        """Print table for student"""
        stu_pt = PrettyTable(field_names=Student.columns)
        for key in stu.keys():
            stu_pt.add_row([stu[key].CWID, stu[key].Name,sorted(list(stu[key].grade))])
        print(stu_pt)
             
    def feed_instructor(self):
        """Feed data to instructor class and print the pretty table"""
        try:
            fp = open(self.instructor_path, 'r')
        except FileNotFoundError:
            raise FileNotFoundError('Error! Cannot open the instructor.txt file', self.instructor_path)
        else:
            with fp:             
                for line in fp:
                    line = line.strip().split('\t')
                    self.instructor[line[0]] = instructor(line[0], line[1], line[2])
                  
        try:
            file = open(self.grade_path, 'r')
        except FileNotFoundError:
            raise FileNotFoundError('Error! Cannot open the grades.txt file', self.grade_path)
        else:
            with file:                             
                for grade_line in file:
                    grade_line = grade_line.strip().split('\t')
                    try:
                        self.instructor[grade_line[3]].num_course(grade_line[1])
                    except KeyError:
                        raise KeyError("Grade file has an instructor ID that does not exist!")
            self.table_ins(self.instructor)

    def table_ins(self, ins):
        """Print the pretty table for instructor"""
        ins_pt = PrettyTable(field_names = instructor.columns)
        for key in ins.keys():
            for a in ins[key].generator_ins():
                ins_pt.add_row(a)
        
        print(ins_pt)

class Student:
    """Class for all the student records. CWID, Name, completed courses."""
    columns = ['CWID', 'Name', 'Completed Courses'] #Class attributes for pretty table columns

    def __init__(self, CWID, Name, Major):
        """Student will have cwid, name, major, course name and grade"""
        self.CWID = CWID
        self.Name = Name
        self.Major = Major
        self.grade = defaultdict(str) #Course name is the key with grade be the value
    def course_grade(self, course_name, letter_grade):
        self.grade[course_name] = letter_grade

class instructor:
    """Class for all the instructor records. """
    columns = ['CWID', 'Name', 'Dept', 'Course', 'Students']    #Class attributes for pretty table columns

    def __init__(self, CWID, Name, Dept):
        """Container for instructor"""
        self.CWID = CWID
        self.Name = Name
        self.Dept = Dept
        self.Course = defaultdict(int)  #Course name is the key with number of students be the value

    def num_course(self, course_name):
        """Add course and number of students to course dict"""
        self.Course[course_name] += 1

    def generator_ins(self):
        """Generator for prettytable"""
        for course_name, num in self.Course.items():
            yield [self.CWID, self.Name, self.Dept, course_name, num]
                   
def main():
    """Run repo"""
    path = input("Please enter the path of student, instructor and grade. (All three files must exist in the same directory): ")
    #path = r'D:\stevens\ssw 810'
    Repository(path)

 
if __name__ == '__main__':
    main()


class Test(unittest.TestCase):
  
    def test_instructor(self):
        """Test instructor course function"""
      
        ins = instructor(5957, 'XW', 'SW')
        for i in range(10):
            ins.num_course("SSW 810")
        for a in range(4):
            ins.num_course("SSW 540")
        dict = ins.Course
        result = {"SSW 810":10, "SSW 540":4}
        self.assertEqual(dict, result)
        
    def test_student(self):
        """Test student course grade function"""
        stu = Student(5950, "LT", "SW")
        stu.course_grade("SSW 540", "A")
        stu.course_grade("SSW 564", "A")
        stu.course_grade("SSW 810", "A")
        dict = stu.grade
        result = {"SSW 540":"A", "SSW 564":"A", "SSW 810":"A"}
        self.assertEqual(dict, result)

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)