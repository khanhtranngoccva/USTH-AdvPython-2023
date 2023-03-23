import time

import numpy

from ..utils import floor


class Student:
    def __init__(self, name: str, dob: str):
        self.name = name
        self.dob = dob
        self.marks: dict[str, float] = {}

    def mark(self, course_id: str, score: float):
        new_score = score
        self.marks[course_id] = floor(new_score, 2)
        return self

    def rename(self, new_name: str):
        self.name = new_name
        return self

    def change_date_of_birth(self, dob: str):
        self.dob = dob
        return self

    @property
    def average_score(self):
        if len(self.marks) == 0:
            return 0
        else:
            arr = numpy.array(self.marks.values())
            return numpy.average(arr)

    def __str__(self):
        return f"NAME: {self.name}, DOB: {self.dob}"

    def to_dict(self):
        return {"name": self.name, "dob": self.dob, "marks": self.marks}

    @staticmethod
    def from_dict(data):
        loaded_student = Student(data["name"], data["dob"])
        loaded_student.marks = data["marks"]
        return loaded_student
