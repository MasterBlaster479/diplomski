__author__ = 'goran'
import pdb;pdb.set_trace()
from pony.orm import *
from datetime import date,datetime

db = Database('postgres', user='goran', password='', host='localhost', database='pony')

class Person(db.Entity):
    name = Required(str)
    age = Required(int)
    courses = Set("Course", reverse="person_id")

class Course(db.Entity):
    name = Required(str)
    semester = Required(int)
    lectures = Set("Lecture")
    person_id = Set(Person)

class Lecture(db.Entity):
    date = Required(datetime)
    courses = Set(Course)

sql_debug(True)
db.generate_mapping(create_tables=True, check_tables=True)

@db_session
def pony_test():
    import pdb;pdb.set_trace()

pony_test()
