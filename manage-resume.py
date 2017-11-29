##file used to manage the resume page

from flask_script import Manager
from resume import app, db, Professor, Course

manager = Manager(app)

@manager.command
def deploy():
    db.drop_all()
    db.create_all()
    murphy = Professor(name='Susan B Murphy', department='Business')
    hampel = Professor(name='Richard Hampel', department='History')
    lynch = Professor(name='Christopher Lynch', department='Accounting & MIS')
    oberzytz = Professor(name='Lucy Oberzytz', department='Communications')
    course1 = Course(course_number= 'BUAD 306', title='Introduction to Operations Management', description='Students will begin to explore the topics related to all operation fields in business.')
    course2 = Course(course_number='EDUC 247', title='History of Educaiton in America', description='Students will explore the history of the educational system in the US.')
    course3 = Course(course_number='FINC 311', title='Introduction Finance', description='Students will learn how to use and understand basic financial statements.')
    course4 = Course(course_number='COMM 212', title='Introduction to Communications', description='Students will practice writing and presenting speeches while learning the basic elements of delivering effective speeches')
    db.session.add(murphy)
    db.session.add(hampel)
    db.session.add(lynch)
    db.session.add(oberzytz)
    db.session.add(course1)
    db.session.add(course2)
    db.session.add(course3)
    db.session.add(course4)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
