import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
# Create and check models
# Run and print your queries

from main_app.models import Student


def add_students():
    student_1 = Student(
        student_id='FC5204',
        first_name='John',
        last_name='Doe',
        birth_date='1995-05-15',
        email='john.doe@university.com')
    student_1.save()

    student_2 = Student(
        student_id='FE0054',
        first_name='Jane',
        last_name='Smith',
        email='jane.smith@university.com')
    student_2.save()

    student_3 = Student(
        student_id='FH2014',
        first_name='Alice',
        last_name='Johnson',
        birth_date='1998-02-10',
        email='alice.johnson@university.com')
    student_3.save()

    student_4 = Student(
        student_id='FH2015',
        first_name='Bob',
        last_name='Wilson',
        birth_date='1996-11-25',
        email='bob.wilson@university.com')
    student_4.save()


def get_students_info():
    info_list = []
    for student in Student.objects.all().order_by('student_id'):
        info_list.append(f"Student "
                         f"№{student.student_id}"
                         f": {student.first_name}"
                         f" {student.last_name}; "
                         f"Email: {student.email}")

    return '\n'.join(info_list)


def update_students_emails():
    for student in Student.objects.all():
        if 'university.com' in student.email:
            student.email = student.email.replace('university.com', 'uni-students.com')
            student.save()


def truncate_students():
    Student.objects.all().delete()


add_students()
update_students_emails()
truncate_students()
print(get_students_info())
