from flask import Flask, render_template, request, redirect, url_for, flash
import database
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for flash messages

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/add_student', methods=['GET', 'POST'])
# def add_student():
#     if request.method == 'POST':
#         roll_number = request.form['roll_number']
#         name = request.form['name']
#         subjects = request.form['subjects']
#         class_section = request.form['class_section']
#         year_semester = request.form['year_semester']
#         success = database.add_student(roll_number, name, subjects, class_section, year_semester)
#         if not success:
#             flash('Error: Student with this roll number already exists.')
#         else:
#             flash('Student added successfully.')
#         return redirect(url_for('add_student'))
#     else:
#         classes_and_sections = database.get_classes_and_sections()
#         years_and_semesters = database.get_years_and_semesters()
#         return render_template('add_student.html', classes_and_sections=classes_and_sections, years_and_semesters=years_and_semesters)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        roll_number = request.form['roll_number']
        name = request.form['name']
        subjects = request.form['subjects']
        class_section = request.form['class_section']
        year_semester = request.form['year_semester']
        success = database.add_student(roll_number, name, subjects, class_section, year_semester)
        if not success:
            flash('Error: Student with this roll number already exists.')
        else:
            flash('Student added successfully.')
        return redirect(url_for('add_student'))
    return render_template('add_student.html')


@app.route('/view_attendance', methods=['GET', 'POST'])
def view_attendance():
    if request.method == 'POST':
        date = request.form['date']
        class_section = request.form['class_section']
        year_semester = request.form['year_semester']
        students = database.get_students_by_class_and_year_with_status(class_section, year_semester, date)
        return render_template('view_attendance.html', current_date=date, students=students, classes_and_sections=database.get_classes_and_sections(), years_and_semesters=database.get_years_and_semesters())
    return render_template('view_attendance.html', classes_and_sections=database.get_classes_and_sections(), years_and_semesters=database.get_years_and_semesters())

@app.route('/view_attendance_filter', methods=['POST'])
def view_attendance_filter():
    class_section = request.form['class_section']
    year_semester = request.form['year_semester']
    current_date = datetime.today().strftime('%Y-%m-%d')
    students = database.get_students_by_class_and_year_with_status(class_section, year_semester, current_date)
    return render_template('view_attendance.html', current_date=current_date, students=students, classes_and_sections=database.get_classes_and_sections(), years_and_semesters=database.get_years_and_semesters())


@app.route('/mark_attendance', methods=['GET', 'POST'])
def mark_attendance():
    if request.method == 'POST':
        date = request.form['date']
        class_section = request.form['class_section']
        year_semester = request.form['year_semester']
        students = database.get_students_by_class_and_year(class_section, year_semester)
        for student in students:
            status = 'absent'  # Default value
            if request.form.get(f'attendance-{student["id"]}', 'off') == 'on':
                status = 'present'
            existing_entry = database.get_attendance_by_student_and_date(student['id'], date)
            if existing_entry:
                database.update_attendance(existing_entry['id'], status)
            else:
                database.mark_attendance(student['id'], date, status)
        flash('Attendance marked successfully.')
        return redirect(url_for('mark_attendance'))
    return render_template('mark_attendance.html', classes_and_sections=database.get_classes_and_sections(), years_and_semesters=database.get_years_and_semesters())


@app.route('/mark_attendance_filter', methods=['POST'])
def mark_attendance_filter():
    class_section = request.form['class_section']
    year_semester = request.form['year_semester']
    current_date = datetime.today().strftime('%Y-%m-%d')
    students_with_status = database.get_students_by_class_and_year_with_status(class_section, year_semester, current_date)
    return render_template('mark_attendance.html', current_date=current_date, students=students_with_status, classes_and_sections=database.get_classes_and_sections(), years_and_semesters=database.get_years_and_semesters())

if __name__ == '__main__':
    database.init_db()
    app.run(debug=True)
