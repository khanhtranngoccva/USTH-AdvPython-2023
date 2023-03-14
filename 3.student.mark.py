import uuid
import math

import numpy
import curses

_terminal_ui = curses.initscr()
curses.endwin()


def terminal_print(message=None, clear=True):
    if message is None:
        message = ""
    if clear:
        _terminal_ui.clear()
        _terminal_ui.move(0, 0)
    y, x = _terminal_ui.getyx()
    _terminal_ui.refresh()
    _terminal_ui.addstr(y, 0, str(message))
    _terminal_ui.move(y + 1, 0)


def terminal_input(prompt="", clear=True):
    if clear:
        _terminal_ui.clear()
        _terminal_ui.addstr(0, 0, str(prompt))
    else:
        y, x = _terminal_ui.getyx()
        _terminal_ui.addstr(y, 0, str(prompt))

    curses.echo()
    user_input = _terminal_ui.getstr()
    curses.noecho()
    return user_input


def integer_input(prompt: str | None = None, *args, **kwargs) -> int:
    while True:
        try:
            result = int(terminal_input(prompt, *args, **kwargs))
            break
        except ValueError:
            pass
    return result


def float_input(prompt: str | None = None, *args, **kwargs) -> float:
    while True:
        try:
            result = float(terminal_input(prompt, *args, **kwargs))
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
        self.name = name if name is not None else terminal_input("Student name: > ")
        self.dob = dob if dob is not None else terminal_input("Student date of birth: > ", clear=False)
        self.marks: dict[str, float] = {}

    def mark(self, course_id: str, score: float | None = None):
        new_score = score if score is not None else float_input("Enter the student's score: > ")
        self.marks[course_id] = floor(new_score, 2)
        return self

    def rename(self, new_name: str | None = None):
        self.name = new_name if new_name is not None else terminal_input("Enter the student's new name: > ")
        return self

    def change_date_of_birth(self, dob: str | None = None):
        self.dob = dob if dob is not None else terminal_input("Enter the student's new date of birth: > ")
        return self

    def __str__(self):
        return f"STUDENT NAME: {self.name}, DOB: {self.dob}"


class Course:
    def __init__(self, name: str | None = None, *args, **kwargs):
        self.name = name if name is not None else terminal_input("Enter new course name: > ", *args, **kwargs)

    def rename(self, name: str | None = None, *args, **kwargs):
        self.name = name if name is not None else terminal_input("Enter new course name: > ", *args, **kwargs)
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
        terminal_print("All courses:")
        for course in self.courses.values():
            terminal_print(str(course), clear=False)
        terminal_print(clear=False)
        terminal_input("Press Enter to go back.", clear=False)

    def _select_course_id(self) -> str:
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

    def select_course(self) -> Course:
        return self.courses[self._select_course_id()]

    def rename_course(self) -> Course:
        return self.select_course().rename(clear=False)

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
        global _terminal_ui
        _terminal_ui = curses.initscr()
        curses.noecho()
        curses.cbreak()
        _terminal_ui.keypad(True)

        def exit_loop():
            raise SystemExit

        functionalities = {
            "1": {"function": self.list_courses, "description": "List courses"},
            "2": {"function": self.create_course, "description": "Create course"},
            "3": {"function": self.rename_course, "description": "Rename course"},
            "4": {"function": self.remove_course, "description": "Remove course"},
            "5": {"function": self.list_students, "description": "List students"},
            "6": {"function": self.create_student, "description": "Create student"},
            "7": {"function": self.rename_student, "description": "Rename student"},
            "8": {"function": self.change_student_dob, "description": "Change student date of birth"},
            "9": {"function": self.mark_student, "description": "Mark student"},
            "0": {"function": self.remove_student, "description": "Remove student"},
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
                curses.echo()
                curses.nocbreak()
                _terminal_ui.keypad(False)
                curses.endwin()
                break
            except Exception as e:
                curses.echo()
                curses.nocbreak()
                _terminal_ui.keypad(False)
                curses.endwin()
                raise e


if __name__ == "__main__":
    primary_classroom = Classroom(5)
    primary_classroom.start_manager()
