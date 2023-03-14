import uuid
import math

import numpy
import curses

def integer_input(prompt: str | None = None) -> int:
    while True:
        try:
            result = int(input(prompt))
            break
        except ValueError:
            pass
    return result


def float_input(prompt: str | None = None) -> float:
    while True:
        try:
            result = float(input(prompt))
            break
        except ValueError:
            pass
    return result


def floor(x: float, decimal_places: int = 0):
    return math.floor(x * 10 ** decimal_places) / (10 ** decimal_places)


class NotEnoughDataException(BaseException):
    pass


class Student:
    def __init__(self, name: str | None = None, dob: str | None = None):
        self.name = name if name is not None else input("Student name: > ")
        self.dob = dob if dob is not None else input("Student date of birth: > ")
        self.marks: dict[str, float] = {}

    def mark(self, course_id: str, score: float | None = None):
        new_score = score if score is not None else float_input("Enter the student's score: > ")
        self.marks[course_id] = floor(new_score, 2)
        return self

    def rename(self, new_name: str | None = None):
        self.name = new_name if new_name is not None else input("Enter the student's new name: > ")
        return self

    def change_date_of_birth(self, dob: str | None = None):
        self.dob = dob if dob is not None else input("Enter the student's new date of birth: > ")
        return self

    def __str__(self):
        return f"STUDENT NAME: {self.name}, DOB: {self.dob}"


class Course:
    def __init__(self, name: str | None = None):
        self.name = name if name is not None else input("Enter new course name: > ")

    def rename(self, name: str | None = None):
        self.name = name if name is not None else input("Enter new course name: > ")
        return self

    def __str__(self):
        return f"COURSE NAME: {self.name}"


class Classroom:
    def __init__(self, max_students: int | None = None):
        self.max_students = max_students if max_students is not None else integer_input(
            "Enter max number of students: > ")
        self.students: dict[str, Student] = {}
        self.courses: dict[str, Course] = {}

    def create_course(self) -> Course:
        new_course_id = uuid.uuid4()
        while new_course_id in self.courses:
            new_course_id = uuid.uuid4()
        new_course = Course()
        self.courses[str(new_course_id)] = new_course
        return new_course

    def list_courses(self):
        for course in self.courses.values():
            print(course)

    def _select_course_id(self) -> str:
        if len(self.students) <= 0:
            raise NotEnoughDataException("No courses.")
        id_mapping: dict[int, str] = {}
        i = 0
        for course_id, course in self.courses.items():
            i += 1
            print(f"{i}: {course}")
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
        if len(self.students) <= 0:
            raise NotEnoughDataException("No students.")
        id_mapping: dict[int, str] = {}
        i = 0
        for student_id, student in self.students.items():
            i += 1
            print(f"{i}: {student}")
            id_mapping[i] = student_id
        while True:
            student_id = integer_input("Select a student: > ")
            if student_id in id_mapping:
                return id_mapping[student_id]

    def select_student(self) -> Student:
        return self.students[self._select_student_id()]

    def rename_student(self) -> Student:
        return self.students[self._select_student_id()].rename()

    def change_student_dob(self) -> Student:
        return self.students[self._select_student_id()].change_date_of_birth()

    def mark_student(self) -> Student:
        student_id = self._select_student_id()
        course_id = self._select_course_id()
        return self.students[student_id].mark(course_id)

    def remove_student(self):
        student_id_to_remove = self._select_student_id()
        del self.students[student_id_to_remove]

    def list_students(self):
        sorted_students = []
        for student in self.students.values():
            np_scores = numpy.array(student.marks.values())
            avg_score = floor(numpy.average(np_scores), 1)
            sorted_students.append({
                "average": avg_score,
                "student": student,
            })
        sorted_students.sort(key=lambda x: x["average"], reverse=True)
        for item in sorted_students:
            average = item["average"]
            student = item["student"]
            print(student)
            print("MARKSHEET:")
            print("-" * 20)
            for course_id, score in student.marks.items():
                print(f'{self.courses[course_id]}: {score}')
            print(f"AVERAGE SCORE: {average}")
            print("-" * 20)

    def start_manager(self):
        def exit_loop():
            raise SystemExit

        functionalities = {
            1: {"function": self.list_courses, "description": "List courses"},
            2: {"function": self.create_course, "description": "Create course"},
            3: {"function": self.rename_course, "description": "Rename course"},
            4: {"function": self.remove_course, "description": "Remove course"},
            5: {"function": self.list_students, "description": "List students"},
            6: {"function": self.create_student, "description": "Create student"},
            7: {"function": self.rename_student, "description": "Rename student"},
            8: {"function": self.change_student_dob, "description": "Change student date of birth"},
            9: {"function": self.mark_student, "description": "Mark student"},
            10: {"function": self.remove_student, "description": "Remove student"},
            0: {"function": exit_loop, "description": "Quit"},
        }
        while True:
            try:
                print()
                for commandKey, functionality in functionalities.items():
                    print(f'{commandKey}: {functionality["description"]}')
                command = int(input("Enter functionality: > "))
                if command in functionalities:
                    # pass
                    functionalities[command]["function"]()
            except ValueError:
                continue
            except NotEnoughDataException as e:
                print(e)
            except SystemExit:
                break
            except Exception as e:
                print(e.with_traceback(None))
                break


if __name__ == "__main__":
    primary_classroom = Classroom()
    primary_classroom.start_manager()
