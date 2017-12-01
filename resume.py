import os
from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

# setup SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
db = SQLAlchemy(app)

#Define databse tables
class Professor(db.Model):
    __tablename__ = 'professors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70))
    department = db.Column(db.Text)
    courses = db.relationship('Course', backref='professor', cascade="delete")


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    course_number = db.Column(db.Integer)
    title = db.Column(db.String(500))
    description = db.Column(db.Text)
    professor_id = db.Column(db.Integer, db.ForeignKey('professors.id'))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/courses')
def get_all_courses():
    courses =[
    'BUAD306',
    'EDUC247',
    'FINC311',
    'COMM212'
    ]
    return render_template('courses.html', courses = courses)



@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/professors')
def show_all_professors():
    professors = Professor.query.all()
    return render_template('professor-all.html', professors=professors)


@app.route('/course-directory')
def show_all_courses():
    courses = Course.query.all()
    return render_template('course-all.html', courses=courses)


@app.route('/professors/edit/<int:id>', methods=['GET', 'POST'])
def edit_professor(id):
    professor = Professor.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('professor-edit.html', professor=professor)
    if request.method == 'POST':
        professor.name = request.form['name']
        professor.department = request.form['department']
        db.session.commit()
        return redirect(url_for('show_all_professors'))

@app.route('/professor/delete/<int:id>', methods=['GET', 'POST'])
def delete_professor(id):
    professor = Professor.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('professor-delete.html', professor=professor)
    if request.method == 'POST':
        # delete the professor by id
        # all related entries are deleted as well
        db.session.delete(professor)
        db.session.commit()
        return redirect(url_for('show_all_professors'))


@app.route('/api/professor/<int:id>', methods=['DELETE'])
def delete_ajax_professor(id):
    professor = Professor.query.get_or_404(id)
    db.session.delete(professor)
    db.session.commit()
    return jsonify({"id": str(professor.id), "name": professor.name})


@app.route('/course-directory/edit/<int:id>', methods=['GET', 'POST'])
def edit_course(id):
    course = Course.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('course-edit.html', course=course)
    if request.method == 'POST':
        course.course_number = request.form['course number']
        course.title = request.form['title']
        course.description = request.form['description']
        db.session.commit()
        return redirect(url_for('show_all_courses'))

@app.route('/course-directory/delete/<int:id>', methods=['GET', 'POST'])
def delete_course(id):
    course = Course.query.filter_by(id=id).first()
    professor = Professor.query.all()
    if request.method == 'GET':
        return render_template('course-delete.html', course=course, professor=professor)
    if request.method == 'POST':
        db.session.delete(course)
        db.session.commit()
        return redirect(url_for('show_all_courses'))


@app.route('/api/course-directory/<int:id>', methods=['DELETE'])
def delete_ajax_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({"id": str(course.id), "name": course.name})


@app.route('/professors/add', methods=['GET', 'POST'])
def add_professors():
    if request.method == 'GET':
        return render_template('professor-add.html')
    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']

        professor = Professor(name=name, department=department)
        db.session.add(professor)
        db.session.commit()
        return redirect(url_for('show_all_professors'))


@app.route('/course-directory/add', methods=['GET', 'POST'])
def add_courses():
    if request.method == 'GET':
        return render_template('course-add.html')
    if request.method == 'POST':
        course_number = request.form['course number']
        title = request.form['title']
        description = request.form['description']

        course = Course(course_number=course_number, title=title, description=description)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('show_all_courses'))

if __name__ == '__main__':
    app.run()
