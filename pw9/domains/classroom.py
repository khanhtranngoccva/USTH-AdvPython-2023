import datetime
import os.path
import threading
import zipfile
import uuid
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

    def _load(self):
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

    def __init__(self, max_students=20):
        self.__lock = threading.Lock()
        self.__cond = threading.Condition(self.__lock)
        self.__executing_threads = 0
        if os.path.exists("data"):
            self._load()
            return
        self.max_students = max_students
        self.students: dict[str, Student] = {}
        self.courses: dict[str, Course] = {}

    def wait_sync(self):
        self.__lock.acquire()
        while self.__executing_threads > 0:
            self.__cond.wait()
        self.__lock.release()

    @_sync
    def create_course(self, name: str) -> Course:
        new_course_id = uuid.uuid4()
        while new_course_id in self.courses:
            new_course_id = uuid.uuid4()
        new_course = Course(name)
        self.courses[str(new_course_id)] = new_course
        return new_course

    def list_courses(self):
        return self.courses

    @_sync
    def rename_course(self, course_id: str, new_name: str) -> Course:
        course = self.courses[course_id]
        if new_name:
            return course.rename(new_name)
        else:
            return course

    @_sync
    def remove_course(self, course_id: str) -> None:
        del self.courses[course_id]
        for student in self.students.values():
            try:
                del student.marks[course_id]
            except KeyError:
                pass

    @_sync
    def create_student(self, name: str, dob: datetime.date) -> Student:
        new_student_id = uuid.uuid4()
        while new_student_id in self.courses:
            new_student_id = uuid.uuid4()
        new_student = Student(name=name, dob=dob)
        self.students[str(new_student_id)] = new_student
        return new_student

    @_sync
    def rename_student(self, student_id: str, new_name: str) -> Student:
        return self.students[student_id].rename(new_name)

    @_sync
    def change_student_dob(self, student_id: str, new_dob: datetime.date) -> Student:
        return self.students[student_id].change_date_of_birth(new_dob)

    @_sync
    def edit_student(self, student_id, name: str, dob: datetime.date):
        cur_student = self.students.get(student_id, None)
        if cur_student is None:
            raise RuntimeError("Student not found.")
        if name is not None:
            cur_student.rename(name)
        if dob is not None:
            cur_student.change_date_of_birth(dob)

    @_sync
    def mark_student(self, student_id: str, course_id: str, new_mark: float) -> Student:
        return self.students[student_id].mark(course_id=course_id, score=new_mark)

    @_sync
    def remove_student(self, student_id: str):
        del self.students[student_id]

    def list_students(self):
        return self.students
