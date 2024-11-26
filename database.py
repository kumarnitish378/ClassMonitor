import sqlite3

DATABASE = 'attendance.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, roll_number TEXT NOT NULL, name TEXT NOT NULL, subjects TEXT NOT NULL, class_section TEXT NOT NULL, year_semester TEXT NOT NULL)')
        conn.execute('CREATE TABLE IF NOT EXISTS attendance (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER NOT NULL, date TEXT NOT NULL, status TEXT NOT NULL, FOREIGN KEY (student_id) REFERENCES students (id))')
        conn.commit()

# def add_student(roll_number, name, subjects, class_section, year_semester):
#     with get_db_connection() as conn:
#         # Check if a student with the same roll number already exists
#         existing_student = conn.execute('SELECT * FROM students WHERE roll_number = ?', (roll_number,)).fetchone()
#         if existing_student:
#             return False  # Indicate that the student already exists
#         conn.execute('INSERT INTO students (roll_number, name, subjects, class_section, year_semester) VALUES (?, ?, ?, ?, ?)', 
#                      (roll_number, name, subjects, class_section, year_semester))
#         conn.commit()
#         return True  # Indicate success

def add_student(roll_number, name, subjects, class_section, year_semester):
    with get_db_connection() as conn:
        existing_student = conn.execute('SELECT * FROM students WHERE roll_number = ?', (roll_number,)).fetchone()
        if existing_student:
            return False
        conn.execute('INSERT INTO students (roll_number, name, subjects, class_section, year_semester) VALUES (?, ?, ?, ?, ?)', 
                     (roll_number, name, subjects, class_section, year_semester))
        conn.commit()
        return True



def mark_attendance(student_id, date, status):
    with get_db_connection() as conn:
        conn.execute('INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)', (student_id, date, status))
        conn.commit()

def get_student_by_roll_number(roll_number):
    with get_db_connection() as conn:
        return conn.execute('SELECT * FROM students WHERE roll_number = ?', (roll_number,)).fetchone()


def get_attendance_by_class_and_year(class_section, year_semester, date):
    with get_db_connection() as conn:
        return conn.execute('''
            SELECT s.roll_number, s.name, a.status 
            FROM students s
            LEFT JOIN attendance a 
            ON s.id = a.student_id 
            AND a.date = ?
            WHERE s.class_section = ? 
            AND s.year_semester = ?''', 
            (date, class_section, year_semester)).fetchall()


def get_attendance_by_student_id(student_id):
    with get_db_connection() as conn:
        return conn.execute('SELECT * FROM attendance WHERE student_id = ?', (student_id,)).fetchall()

def get_students_by_class_and_year(class_section, year_semester):
    with get_db_connection() as conn:
        return conn.execute('SELECT * FROM students WHERE class_section = ? AND year_semester = ?', 
                            (class_section, year_semester)).fetchall()

def get_attendance_by_student_and_date(student_id, date):
    with get_db_connection() as conn:
        return conn.execute('SELECT * FROM attendance WHERE student_id = ? AND date = ?', 
                            (student_id, date)).fetchone()

def update_attendance(attendance_id, status):
    with get_db_connection() as conn:
        conn.execute('UPDATE attendance SET status = ? WHERE id = ?', (status, attendance_id))
        conn.commit()

def mark_attendance(student_id, date, status):
    with get_db_connection() as conn:
        conn.execute('INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)', (student_id, date, status))
        conn.commit()

def get_all_students_with_today_status(date):
    with get_db_connection() as conn:
        return conn.execute('''
            SELECT s.id, s.roll_number, s.name, 
            COALESCE(a.status, 'absent') as status 
            FROM students s
            LEFT JOIN attendance a 
            ON s.id = a.student_id 
            AND a.date = ?
        ''', (date,)).fetchall()

def get_students_by_class_and_year_with_status(class_section, year_semester, date):
    with get_db_connection() as conn:
        return conn.execute('''
            SELECT s.id, s.roll_number, s.name, 
            COALESCE(a.status, 'absent') as status 
            FROM students s
            LEFT JOIN attendance a 
            ON s.id = a.student_id 
            AND a.date = ?
            WHERE s.class_section = ? 
            AND s.year_semester = ?
        ''', (date, class_section, year_semester)).fetchall()
    
    
def get_students_by_class_and_year(class_section, year_semester):
    with get_db_connection() as conn:
        return conn.execute('SELECT * FROM students WHERE class_section = ? AND year_semester = ?', 
                            (class_section, year_semester)).fetchall()

def get_attendance_by_student_and_date(student_id, date):
    with get_db_connection() as conn:
        return conn.execute('SELECT * FROM attendance WHERE student_id = ? AND date = ?', 
                            (student_id, date)).fetchone()

def update_attendance(attendance_id, status):
    with get_db_connection() as conn:
        conn.execute('UPDATE attendance SET status = ? WHERE id = ?', (status, attendance_id))
        conn.commit()

def mark_attendance(student_id, date, status):
    with get_db_connection() as conn:
        conn.execute('INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)', (student_id, date, status))
        conn.commit()

def get_all_students_with_today_status(date):
    with get_db_connection() as conn:
        return conn.execute('''
            SELECT s.id, s.roll_number, s.name, 
            COALESCE(a.status, 'absent') as status 
            FROM students s
            LEFT JOIN attendance a 
            ON s.id = a.student_id 
            AND a.date = ?
        ''', (date,)).fetchall()


def get_classes_and_sections():
    with get_db_connection() as conn:
        return conn.execute('SELECT DISTINCT class_section FROM students').fetchall()

def get_years_and_semesters():
    with get_db_connection() as conn:
        return conn.execute('SELECT DISTINCT year_semester FROM students').fetchall()

def add_student(roll_number, name, subjects, class_section, year_semester):
    with get_db_connection() as conn:
        existing_student = conn.execute('SELECT * FROM students WHERE roll_number = ?', (roll_number,)).fetchone()
        if existing_student:
            return False
        conn.execute('INSERT INTO students (roll_number, name, subjects, class_section, year_semester) VALUES (?, ?, ?, ?, ?)', 
                     (roll_number, name, subjects, class_section, year_semester))
        conn.commit()
        return True


if __name__ == '__main__':
    init_db()
