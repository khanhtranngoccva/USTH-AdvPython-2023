from ..io import *
from ..utils import floor


class Student:
    def __init__(self, name: typing.Union[str, None] = None, dob: typing.Union[str, None] = None):
        self.name = name if name is not None else terminal_input("Student name: > ")
        self.dob = dob if dob is not None else terminal_input("Student date of birth: > ", clear=False)
        self.marks: dict[str, float] = {}

    def mark(self, course_id: str, score: typing.Union[float, None] = None):
        new_score = score if score is not None else float_input("Enter the student's score: > ")
        self.marks[course_id] = floor(new_score, 2)
        return self

    def rename(self, new_name: typing.Union[str, None] = None):
        self.name = new_name if new_name is not None else terminal_input("Enter the student's new name: > ")
        return self

    def change_date_of_birth(self, dob: typing.Union[str, None] = None):
        self.dob = dob if dob is not None else terminal_input("Enter the student's new date of birth: > ")
        return self

    def __str__(self):
        return f"STUDENT NAME: {self.name}, DOB: {self.dob}"
