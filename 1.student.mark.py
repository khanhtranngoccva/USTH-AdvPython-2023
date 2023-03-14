import sys


def _gen_student(name: str, dob: str):
    return {
        "name": name,
        "dob": dob,
        "marks": {}
    }


def _gen_course(name: str):
    return {
        "name": name,
    }


def create_edit_course(classroom: dict[str, dict | int]):
    course_id = input("Input course ID: > ")
    course_name = input("Input course name: > ")
    classroom["course_data"][course_id] = _gen_course(course_name)


def create_edit_student(classroom: dict[str, dict | int]):
    student_id = input("Input student ID: > ")
    student_name = input("Input student name: > ")
    student_dob = input("Input student date of birth: > ")
    if student_id in classroom["student_data"] or len(classroom["student_data"]) < classroom["max_student_count"]:
        classroom["student_data"][student_id] = _gen_student(student_name, student_dob)
    else:
        raise Exception("Error - Classroom is full.")


def _input_marks(classroom: dict[str, dict | int], student: dict[str, str | dict[str, str | dict]]):
    course_id_to_mark = input("Input course ID: >")
    if course_id_to_mark not in classroom["course_data"]:
        raise Exception("Error - This course does not exist.")
    mark = input("Input course mark > ")
    student["marks"][course_id_to_mark] = mark


def mark_student(classroom: dict[str, dict | int]):
    student_id = input("Enter student ID: > ")
    if student_id not in classroom["student_data"]:
        raise Exception("Error - This student does not exist.")
    _input_marks(classroom, classroom["student_data"][student_id])


def gen_classroom(student_count: int = 10) -> dict[str, dict | int]:
    return {
        "max_student_count": student_count,
        "student_data": {},
        "course_data": {},
    }


def list_students(classroom: dict[str, dict | int]):
    for (student_id, data) in classroom["student_data"].items():
        raw_marks = data["marks"]
        print(f'Student ID: {student_id} | Name: {data["name"]} | DOB: {data["dob"]}')
        print(f"Marksheet for {data['name']}")
        for (course_id, course_mark) in raw_marks.items():
            course_name = classroom["course_data"][course_id]['name']
            print(f'Course name: {course_name} | Marks: {course_mark}')
        print()


def list_courses(classroom: dict[str, dict | int]):
    for (course_id, course) in classroom["course_data"].items():
        print(f"Course ID: {course_id} | Course name: {course['name']}")


functions = {
    1: create_edit_student,
    2: create_edit_course,
    3: mark_student,
    4: list_students,
    5: list_courses,
    6: lambda x: sys.exit(),
}

if __name__ == "__main__":
    primary_classroom = gen_classroom()
    while True:
        try:
            command = int(input("Enter functionality: > "))
            functions[command](primary_classroom)
        except KeyError:
            continue
        except ValueError:
            continue
        except Exception as e:
            print(e.with_traceback(None))
