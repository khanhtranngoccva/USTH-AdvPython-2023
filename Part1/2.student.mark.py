import sys
import uuid


def integer_input(prompt: str | None = None) -> int:
    while True:
        try:
            result = int(input(prompt))
            break
        except ValueError:
            pass
    return result


class Student:
    def __init__(self, name: str = input("Student name: > "), dob: str = input("Student date of birth: > ")):
        self.name = name
        self.dob = dob
        self.marks: dict[str, int] = {}

    def mark(self, course_id: str, score: int = integer_input("Enter your course score > ")):
        self.marks[course_id] = score
        return self

    def __str__(self):
        return f"STUDENT NAME: {self.name}"


class Course:
    def __init__(self, name: str = input("Enter new course name: > ")):
        self.name = name

    def rename(self, name: str = input("Enter new course name: > ")):
        self.name = name
        return self

    def __str__(self):
        return f"COURSE NAME: {self.name}"


class Classroom:
    def __init__(self, max_students: int = integer_input("Enter max number of students: > ")):
        self.max_students = max_students
        self.students: dict[str, Student] = {}
        self.courses: dict[str, Course] = {}

    def create_course(self) -> Course:
        new_course_id = uuid.uuid4()
        while new_course_id in self.courses:
            new_course_id = uuid.uuid4()
        new_course = Course()
        self.courses[str(new_course_id)] = new_course
        return new_course

    def _select_course_id(self) -> str:
        id_mapping: dict[int, str] = {}
        i = 0
        for course_id, course in self.courses.items():
            print(f"{i}: {course}")
            i += 1
            id_mapping[i] = course_id
        while True:
            course_index = integer_input("Select a course: > ")
            if course_index in id_mapping:
                return id_mapping[course_index]

    def select_course(self) -> Course:
        return self.courses[self._select_course_id()]

    def rename_course(self) -> Course:
        return self.select_course().rename()

    def remove_course(self) -> None:
        course_id_to_remove = self._select_course_id()
        del self.courses[course_id_to_remove]
        for student in self.students.values():
            try:
                del student.marks[course_id_to_remove]
            except KeyError:
                pass

    def create_student(self) -> Student:
        new_student_id = uuid.uuid4()
        while new_student_id in self.courses:
            new_student_id = uuid.uuid4()
        new_student = Student()
        self.students[str(new_student_id)] = new_student
        return new_student

    def _select_student_id(self) -> str:
        id_mapping: dict[int, str] = {}
        i = 0
        for student_id, student in self.students.items():
            print(f"{i}: {student}")
            i += 1
            id_mapping[i] = student_id
        while True:
            student_id = integer_input("Select a student: > ")
            if student_id in id_mapping:
                return id_mapping[student_id]

    def select_student(self) -> Student:
        return self.students[self._select_student_id()]


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
