import sqlite3


conn = sqlite3.connect('mydatabase.db')
sql = conn.cursor()


sql.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    grade TEXT NOT NULL
)
''')
conn.commit()



def insert_students():
    students = [
        ('TIMUR', 20, 'A'),
        ('AKBAR', 22, 'B'),
        ('MIRSAID', 21, 'C'),
        ('YASMINA', 23, 'B'),
        ('IRINA', 19, 'A')
    ]

    sql.executemany('INSERT INTO students (name, age, grade) VALUES (?, ?, ?)', students)
    conn.commit()



def get_student_by_name(name):
    sql.execute('SELECT name, age, grade FROM students WHERE name = ?', (name,))
    student = sql.fetchone()

    if student:
        print(f'Студент: {student[0]}, Возраст: {student[1]}, Оценка: {student[2]}')
    else:
        print(f'Студент с именем {name} не найден.')

    return student



def update_student_grade(name, new_grade):
    sql.execute('UPDATE students SET grade = ? WHERE name = ?', (new_grade, name))
    conn.commit()

    if sql.rowcount > 0:
        print(f'Оценка студента {name} успешно обновлена до {new_grade}.')
    else:
        print(f'Студент с именем {name} не найден.')



def delete_student(name):
    sql.execute('DELETE FROM students WHERE name = ?', (name,))
    conn.commit()

    if sql.rowcount > 0:
        print(f'Студент с именем {name} успешно удалён.')
    else:
        print(f'Студент с именем {name} не найден.')


insert_students()

get_student_by_name('MIRSAID')

update_student_grade('IRINA', 'A+')  # Обновление оценки студента

delete_student('SUHROB')
