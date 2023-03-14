from ..io import *


class Course:
    def __init__(self, name: typing.Union[str, None] = None, *args, **kwargs):
        self.name = name if name is not None else terminal_input("Enter new course name: > ", *args, **kwargs)

    def rename(self, name: typing.Union[str, None] = None, *args, **kwargs):
        self.name = name if name is not None else terminal_input("Enter new course name: > ", *args, **kwargs)
        return self

    def __str__(self):
        return f"COURSE NAME: {self.name}"
