""" Homework 10
    Xueshi Wang
    10.30.2018
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
        self.major_path = os.path.join(dir_path, 'majors.txt')
        self.student = dict()   # students[cwid] = Student(cwid, name, major)
        self.instructor = dict()
        self.major = dict()
        self.feed_major()
        self.feed_student()
        self.feed_instructor()
        

    def feed_major(self):
        """Feed data to major table"""
        try:
            fp = open(self.major_path, 'r')
        except FileNotFoundError:
            raise FileNotFoundError('Error! Cannot open the majors.txt file', self.major_path)
        else:
            with fp:         
                for line in fp:
                    line = line.strip().split('\t')
                    if line[0] in self.major.keys():                                            
                        if line[1] == 'R':                        
                            self.major[line[0]].add_required(line[2])
                        elif line[1] == 'E':              
                            self.major[line[0]].add_elective(line[2])
                    else:
                        self.major[line[0]] = Major(line[0])
                        if line[1] == 'R':                      
                            self.major[line[0]].add_required(line[2])
                        elif line[1] == 'E':
                            self.major[line[0]].add_elective(line[2])
            self.table_maj(self.major)
    
    def table_maj(self, maj):
        """print table for majors"""
        maj_pt = PrettyTable(field_names=Major.columns)
        for key in maj.keys():
            maj_pt.add_row([maj[key].major, sorted(maj[key].Required), sorted(maj[key].Electives)])
        print(maj_pt)

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
            for key in self.student:
                self.student[key].get_classes()  #Get all the passed class to student class attribute
                required = self.major[self.student[key].Major].Required #Get the major required course
                elective = self.major[self.student[key].Major].Electives    #Get the major elective course
                self.student[key].eva_required(required)    #Fill the attribute for student's remain_required
                self.student[key].eva_electives(elective)   #Fill the attribute for student's remain_electives

            self.table_stu(self.student)

    def table_stu(self, stu):
        """Print table for student"""
        stu_pt = PrettyTable(field_names=Student.columns)
        for key in stu.keys():
            
            stu_pt.add_row([stu[key].CWID, stu[key].Name, sorted(list(stu[key].completed)), stu[key].remain_required, stu[key].remain_electives])
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

class Major:
    """Class for all the majors with dept, required courses and electives courses"""
    columns = ['Dept', 'Required', 'Electives'] #Class attributes for pretty table columns
    acceptable = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']

    def __init__(self, major):
        """Constructor for major class"""
        self.major = major
        self.Required = list()
        self.Electives = list()

    def add_required(self, required):
        """add required course to major"""
        self.Required.append(required)
    
    def add_elective(self, elective):
        """add elective course to major"""
        self.Electives.append(elective)
    
        
class Student:
    """Class for all the student records. CWID, Name, completed courses."""
    columns = ['CWID', 'Name', 'Completed Courses', 'Remaining Required', 'Remaining Electives'] #Class attributes for pretty table columns
    #columns = ['CWID', 'Name', 'Completed Courses']
    acceptable = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']

    def __init__(self, CWID, Name, Major):
        """Student will have cwid, name, major, course name and grade"""
        self.CWID = CWID
        self.Name = Name
        self.Major = Major
        self.grade = defaultdict(str) #Course name is the key with grade be the value
        self.remain_required = set()
        self.remain_electives = set()
        self.completed = set()
        
    def course_grade(self, course_name, letter_grade):
        self.grade[course_name] = letter_grade

    def get_classes(self):
        """Get passed classes"""
        for key in self.grade:
            if self.grade[key] in self.acceptable:
                self.completed.add(key)
    
    def eva_required(self, required):
        """calculate remaining required"""
        req = set(required)
        self.remain_required = req.difference(self.completed)
        
    def eva_electives(self, elective):
        """calculate remaining elective"""
        elec = set(elective)
        if len(self.completed.intersection(elective)) > 0:
            self.remain_electives = ("Passed")
        else:
            self.remain_electives = elec.difference(self.completed)

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
    #path = input("Please enter the path of student, instructor and grade. (All three files must exist in the same directory): ")
    path = r'D:\stevens\ssw 810'
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

    def test_course(self):
        """test student course related function"""
        stu = Student(5950, "LT", "SW")
        stu.course_grade("SSW 540", "D")
        stu.course_grade("SSW 564", "C-")
        stu.course_grade("SSW 810", "A")
        stu.course_grade("SSW 555", "B")
        required = {"SSW 512", "SSW 156", "SSW 810"}
        elective = {"SSW 123", "SSW 555"}
        stu.get_classes()
        stu.eva_required(required)
        stu.eva_electives(elective)
        result = {'SSW 810', 'SSW 555'}
        remain_required = {'SSW 512', 'SSW 156'}
        remain_electives = {"SSW 123"}
        self.assertEqual(stu.completed, result)
        self.assertEqual(stu.remain_required, remain_required)
        self.assertEqual(stu.remain_electives, remain_electives)

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)