import os.path
import threading
import zipfile
import uuid
from ..io import *
from ..io import _terminal_ui
from ..errors import *
import numpy
from ..utils import floor
from .student import Student
from .course import Course
import json
import pickle


class Classroom:

    @staticmethod
    def _sync(func):
        def new_func(self, *args, **kwargs):

            output = func(self, *args, **kwargs)

            def thread_func():

                def execute():
                    students_obj = {key: value.to_dict() for key, value in self.students.items()}
                    courses_obj = {key: value.to_dict() for key, value in self.courses.items()}
                    with open("students", "wb") as file:
                        pickle.dump(students_obj, file)
                    with open("courses", "wb") as file:
                        pickle.dump(courses_obj, file)
                    with open("info", "wb") as file:
                        pickle.dump({"max_students": self.max_students}, file)
                    with zipfile.ZipFile("data", "w") as file:
                        file.write("students", "/students")
                        file.write("courses", "/courses")
                        file.write("info", "/info")

                with self.__lock:
                    try:
                        self.__executing_threads += 1
                        execute()
                    finally:
                        self.__executing_threads -= 1
                        self.__cond.notify()

            cur_thread = threading.Thread(target=thread_func)
            cur_thread.start()
            return output

        return new_func

    def __load(self):
        with zipfile.ZipFile("data", "r") as file:
            file.extract("students")
            file.extract("courses")
            file.extract("info")
        with open("students", "rb") as file:
            raw = pickle.load(file)
            self.students = {key: Student.from_dict(value) for key, value in raw.items()}
        with open("courses", "rb") as file:
            raw = pickle.load(file)
            self.courses = {key: Course.from_dict(value) for key, value in raw.items()}
        with open("info", "rb") as file:
            raw = pickle.load(file)
            self.max_students = raw["max_students"]

    def __init__(self, max_students: typing.Union[int, None] = None):
        self.__lock = threading.Lock()
        self.__cond = threading.Condition(self.__lock)
        self.__executing_threads = 0
        if os.path.exists("data"):
            self.__load()
            return
        self.max_students = max_students if max_students is not None else integer_input(
            "Enter max number of students: > ")
        self.students: dict[str, Student] = {}
        self.courses: dict[str, Course] = {}

    @_sync
    def __create_course(self) -> Course:
        new_course_id = uuid.uuid4()
        while new_course_id in self.courses:
            new_course_id = uuid.uuid4()
        new_course = Course()
        self.courses[str(new_course_id)] = new_course
        return new_course

    @_sync
    def __list_courses(self):
        terminal_print("All courses:")
        for course in self.courses.values():
            terminal_print(str(course), clear=False)
        terminal_print(clear=False)
        terminal_input("Press Enter to go back.", clear=False)

    @_sync
    def __select_course_id(self) -> str:
        def print_courses():
            terminal_print("Select a course.")
            i = 0
            for course_id, course in self.courses.items():
                i += 1
                terminal_print(f"{i}: {course}", clear=False)

        if len(self.courses) <= 0:
            raise NotEnoughDataException("No courses.")
        id_mapping: dict[int, str] = {}
        i = 0
        for course_id, course in self.courses.items():
            i += 1
            id_mapping[i] = course_id
        while True:
            print_courses()
            course_index = integer_input("Select a course: > ", False)
            if course_index in id_mapping:
                return id_mapping[course_index]

    @_sync
    def __select_course(self) -> Course:
        return self.courses[self.__select_course_id()]

    @_sync
    def __rename_course(self) -> Course:
        return self.__select_course().rename(clear=False)

    @_sync
    def __remove_course(self) -> None:
        course_id_to_remove = self.__select_course_id()
        del self.courses[course_id_to_remove]
        for student in self.students.values():
            try:
                del student.marks[course_id_to_remove]
            except KeyError:
                pass

    @_sync
    def __create_student(self) -> Student:
        new_student_id = uuid.uuid4()
        while new_student_id in self.courses:
            new_student_id = uuid.uuid4()
        new_student = Student()
        self.students[str(new_student_id)] = new_student
        return new_student

    @_sync
    def __select_student_id(self) -> str:
        def print_students():
            terminal_print("Select a student.")
            i = 0
            for student_id, student in self.students.items():
                i += 1
                terminal_print(f"{i}: {student}", clear=False)

        if len(self.students) <= 0:
            raise NotEnoughDataException("No students.")
        id_mapping: dict[int, str] = {}
        i = 0
        for student_id, student in self.students.items():
            i += 1
            id_mapping[i] = student_id
        while True:
            print_students()
            student_id = integer_input("Select a student: > ", clear=False)
            if student_id in id_mapping:
                return id_mapping[student_id]

    @_sync
    def __select_student(self) -> Student:
        return self.students[self.__select_student_id()]

    @_sync
    def __rename_student(self) -> Student:
        return self.students[self.__select_student_id()].rename()

    @_sync
    def __change_student_dob(self) -> Student:
        return self.students[self.__select_student_id()].change_date_of_birth()

    @_sync
    def __mark_student(self) -> Student:
        student_id = self.__select_student_id()
        course_id = self.__select_course_id()
        return self.students[student_id].mark(course_id)

    @_sync
    def __remove_student(self):
        student_id_to_remove = self.__select_student_id()
        del self.students[student_id_to_remove]

    @_sync
    def __list_students(self):
        def print_student_item(item):
            terminal_print("Student info:")
            average = item["average"]
            student = item["student"]
            terminal_print(student, clear=False)
            terminal_print(clear=False)
            terminal_print("MARKSHEET:", clear=False)
            terminal_print(clear=False)
            for course_id, score in student.marks.items():
                terminal_print(f'{self.courses[course_id]}: {score}', clear=False)
            terminal_print(clear=False)
            terminal_print(clear=False)
            terminal_print(f"AVERAGE SCORE: {average}", clear=False)
            terminal_print(clear=False)

        if len(self.students) == 0:
            raise NotEnoughDataException("No students.")

        sorted_students = []
        for student in self.students.values():
            np_scores = numpy.array(list(student.marks.values()))
            if len(student.marks) == 0:
                avg_score = 0
            else:
                avg_score = floor(numpy.average(np_scores), 1)
            sorted_students.append({
                "average": avg_score,
                "student": student,
            })
        sorted_students.sort(key=lambda x: x["average"], reverse=True)

        index = 0
        while True:
            if index < 0:
                index = 0
            if index >= len(sorted_students):
                index = len(sorted_students) - 1
            print_student_item(sorted_students[index])
            terminal_print("Press left or right to move, and Enter to go back.", clear=False)
            mode = _terminal_ui.getch()
            if mode == 10:
                break
            elif mode == curses.KEY_LEFT:
                index -= 1
            elif mode == curses.KEY_RIGHT:
                index += 1

    def start_manager(self):
        terminal_start()

        def exit_loop():
            # locked = self.__lock.locked()
            # print(locked)
            # if locked and self.__executing_threads == 0:
            #     raise RuntimeError("Hmmmm.")
            self.__lock.acquire()
            while self.__executing_threads > 0:
                self.__cond.wait()
            self.__lock.release()
            raise SystemExit

        functionalities = {
            "1": {"function": self.__list_courses, "description": "List courses"},
            "2": {"function": self.__create_course, "description": "Create course"},
            "3": {"function": self.__rename_course, "description": "Rename course"},
            "4": {"function": self.__remove_course, "description": "Remove course"},
            "5": {"function": self.__list_students, "description": "List students"},
            "6": {"function": self.__create_student, "description": "Create student"},
            "7": {"function": self.__rename_student, "description": "Rename student"},
            "8": {"function": self.__change_student_dob, "description": "Change student date of birth"},
            "9": {"function": self.__mark_student, "description": "Mark student"},
            "0": {"function": self.__remove_student, "description": "Remove student"},
            "q": {"function": exit_loop, "description": "Quit"},
        }

        def main_display():
            _terminal_ui.erase()
            _terminal_ui.addstr(0, 0, "Good morning user!")

            i = 1
            for commandKey, functionality in functionalities.items():
                _terminal_ui.addstr(i, 0, f'{commandKey}: {functionality["description"]}')
                i += 1

            _terminal_ui.refresh()

        while True:
            try:
                main_display()
                c = _terminal_ui.getch()
                if functionalities.get(chr(c), None):
                    functionalities[chr(c)]["function"]()
            except ValueError:
                continue
            except NotEnoughDataException as e:
                terminal_print(e)
            except KeyboardInterrupt:
                continue
            except SystemExit:
                terminal_shutdown()
                break
            except Exception as e:
                terminal_shutdown()
                raise e
