import os
import time
import tkinter
import datetime

import tkcalendar
import typing

from .domains.classroom import Classroom


class ClassroomManager:

    def __init__(self):
        self.__classroom = Classroom()
        self.__window = tkinter.Tk()
        self.__window.geometry("1280x720")
        self.__window_entities = {}
        self.__student_ids = []
        self.__course_ids = []
        self.__cur_student_id = None
        self.__cur_course_id = None

        window_entities = self.__window_entities
        window_entities["frame1"] = tkinter.Frame(master=self.__window)
        window_entities["frame1"].pack(fill=tkinter.X, padx=24, pady=16)

        window_entities["title_label"] = tkinter.Label(master=window_entities["frame1"], text="Classroom Manager",
                                                       font=("Lato", 24, "bold"))
        window_entities["title_label"].pack(side=tkinter.LEFT)

        window_entities["frame2"] = tkinter.Frame(master=self.__window)
        window_entities["frame2"].pack(fill=tkinter.BOTH, expand=True, padx=24, pady=(0, 16))

        window_entities["student_list"] = tkinter.Listbox(master=window_entities["frame2"], width=40, relief="flat")
        window_entities["student_list"].pack(side=tkinter.LEFT, fill=tkinter.Y)

        window_entities["student_list"].bind("<ButtonRelease-1>", self.select_student_id)

        window_entities["course_list"] = tkinter.Listbox(master=window_entities["frame2"], width=40, relief="flat")
        window_entities["course_list"].pack(side=tkinter.LEFT, fill=tkinter.Y)

        window_entities["course_list"].bind("<ButtonRelease-1>", self.select_course_id)

        window_entities["input_frame"] = tkinter.Frame(master=window_entities["frame2"], relief="flat")
        window_entities["input_frame"].pack(side=tkinter.LEFT, fill=tkinter.Y)

        window_entities["student_fields"] = tkinter.LabelFrame(master=window_entities["input_frame"],
                                                               text="Student info", padx=8, pady=4)
        window_entities["student_fields"].pack(side=tkinter.TOP, fill=tkinter.X)

        window_entities["name_label"] = tkinter.LabelFrame(master=window_entities["student_fields"],
                                                           text="Student name")
        window_entities["name_label"].pack(side=tkinter.TOP, fill=tkinter.X)

        window_entities["student_name"] = tkinter.Entry(master=window_entities["name_label"], width=40)
        window_entities["student_name"].pack(side=tkinter.TOP, fill=tkinter.X)

        window_entities["dob_label"] = tkinter.LabelFrame(master=window_entities["student_fields"],
                                                          text="Student date of birth")
        window_entities["dob_label"].pack(side=tkinter.TOP, fill=tkinter.X)

        window_entities["student_dob"] = tkcalendar.Calendar(master=window_entities["dob_label"], width=40)
        window_entities["student_dob"].pack(side=tkinter.TOP, fill=tkinter.X)

        window_entities["mark_fields"] = tkinter.LabelFrame(master=window_entities["input_frame"],
                                                            text="Student marks", padx=8, pady=4)
        window_entities["mark_fields"].pack(side=tkinter.TOP, fill=tkinter.X)

        window_entities["mark_label"] = tkinter.LabelFrame(master=window_entities["mark_fields"],
                                                           text="Mark subject")
        window_entities["mark_label"].pack(side=tkinter.TOP, fill=tkinter.X)

        window_entities["student_mark"] = tkinter.Entry(master=window_entities["mark_label"], width=40, )
        window_entities["student_mark"].pack(side=tkinter.TOP, fill=tkinter.X)

        window_entities["add_student"] = tkinter.Button(master=window_entities["student_fields"], text="Add student")
        window_entities["add_student"].pack(side=tkinter.TOP, fill=tkinter.X)
        window_entities["add_student"].bind("<ButtonRelease-1>", self.add_student)

        window_entities["save_student_info"] = tkinter.Button(master=window_entities["student_fields"],
                                                              text="Edit student information")
        window_entities["save_student_info"].pack(side=tkinter.TOP, fill=tkinter.X)
        window_entities["save_student_info"].bind("<ButtonRelease-1>", self.edit_student)

        window_entities["delete_student"] = tkinter.Button(master=window_entities["student_fields"],
                                                           text="Delete student")
        window_entities["delete_student"].pack(side=tkinter.TOP, fill=tkinter.X)
        window_entities["delete_student"].bind("<ButtonRelease-1>", self.remove_student)

        window_entities["mark_student"] = tkinter.Button(master=window_entities["mark_fields"], text="Mark student")
        window_entities["mark_student"].pack(side=tkinter.TOP, fill=tkinter.X)

        window_entities["mark_student"].bind("<ButtonRelease-1>", self.mark_student)

        window_entities["course_fields"] = tkinter.LabelFrame(master=window_entities["input_frame"],
                                                              text="Course information", padx=8, pady=4)
        window_entities["course_fields"].pack(side=tkinter.TOP, fill=tkinter.X)

        window_entities["course_name_label"] = tkinter.LabelFrame(master=window_entities["course_fields"],
                                                                  text="Course name")
        window_entities["course_name_label"].pack(side=tkinter.TOP, fill=tkinter.X)

        window_entities["course_name"] = tkinter.Entry(master=window_entities["course_name_label"], width=40, )
        window_entities["course_name"].pack(side=tkinter.TOP, fill=tkinter.X)

        window_entities["add_course"] = tkinter.Button(master=window_entities["course_fields"], text="Add course")
        window_entities["add_course"].pack(side=tkinter.TOP, fill=tkinter.X)

        window_entities["add_course"].bind("<ButtonRelease-1>", self.add_course)

        window_entities["edit_course"] = tkinter.Button(master=window_entities["course_fields"], text="Edit course")
        window_entities["edit_course"].pack(side=tkinter.TOP, fill=tkinter.X)

        window_entities["edit_course"].bind("<ButtonRelease-1>", self.edit_course)

        window_entities["delete_course"] = tkinter.Button(master=window_entities["course_fields"], text="Delete course")
        window_entities["delete_course"].pack(side=tkinter.TOP, fill=tkinter.X)

        window_entities["delete_course"].bind("<ButtonRelease-1>", self.remove_course)

    def fill_students_list(self):
        student_list = self.__window_entities["student_list"]
        student_list.delete(0, student_list.size())
        self.__student_ids = []
        i = 0
        for student_id, student in self.__classroom.list_students().items():
            self.__student_ids.append(student_id)
            student_list.insert(tkinter.END, str(student))
            if student_id == self.__cur_student_id:
                student_list.selection_set(i, i)
            i += 1
        self.fill_course_list()

    def fill_course_list(self):
        if self.__cur_student_id is None:
            cur_student = None
        else:
            cur_student = self.__classroom.students.get(self.__cur_student_id, None)

        course_list = self.__window_entities["course_list"]
        course_list.delete(0, course_list.size())
        self.__course_ids = []
        for course_id, course in self.__classroom.list_courses().items():
            self.__course_ids.append(course_id)
            if cur_student is None:
                course_string = str(course)
            else:
                marks = cur_student.marks.get(course_id, None)
                course_string = f'{str(course)}: {marks if marks is not None else "No score"}'
            course_list.insert(tkinter.END, course_string)

    def select_student_id(self, event):
        widget: tkinter.Listbox = event.widget
        try:
            self.__cur_student_id = self.__student_ids[widget.curselection()[0]]
        except IndexError:
            self.__cur_student_id = None
        self.fill_course_list()

    def select_course_id(self, event):
        widget: tkinter.Listbox = event.widget
        try:
            self.__cur_course_id = self.__course_ids[widget.curselection()[0]]
        except IndexError:
            self.__cur_course_id = None

    def get_entry_info(self):
        name_widget: tkinter.Entry = self.__window_entities["student_name"]
        date_widget: tkcalendar.Calendar = self.__window_entities["student_dob"]
        out: dict[str, typing.Union[str, datetime.date, None]] = {}
        name_data = name_widget.get()
        if name_data:
            out["name"] = name_data
        else:
            out["name"] = None
        date_data = date_widget.get_date()
        if date_data:
            out["dob"] = date_widget.parse_date(date_widget.get_date())
        else:
            out["dob"] = None
        return out

    def clear_student_input(self):
        name_widget: tkinter.Entry = self.__window_entities["student_name"]
        date_widget: tkcalendar.Calendar = self.__window_entities["student_dob"]
        date_widget.selection_clear()
        name_widget.delete(0, tkinter.END)

    def add_student(self, event):
        info = self.get_entry_info()
        if info["name"] is None or info["dob"] is None:
            raise RuntimeError("Missing name or date of birth.")
        self.__classroom.create_student(**info)
        self.clear_student_input()
        self.fill_students_list()

    def edit_student(self, event):
        info = self.get_entry_info()
        self.__classroom.edit_student(self.__cur_student_id, **info)
        self.clear_student_input()
        self.fill_students_list()

    def mark_student(self, event):
        name_widget: tkinter.Entry = self.__window_entities["student_mark"]
        self.__classroom.mark_student(self.__cur_student_id, self.__cur_course_id,
                                      name_widget.getdouble(name_widget.get()))
        self.clear_student_input()
        self.fill_students_list()

    def add_course(self, event):
        name_widget: tkinter.Entry = self.__window_entities["course_name"]
        self.__classroom.create_course(name_widget.get())
        name_widget.delete(0, tkinter.END)
        self.fill_course_list()

    def edit_course(self, event):
        name_widget: tkinter.Entry = self.__window_entities["course_name"]
        self.__classroom.rename_course(self.__cur_course_id, name_widget.get())
        name_widget.delete(0, tkinter.END)
        self.fill_course_list()

    def remove_course(self, event):
        try:
            self.__classroom.remove_course(self.__cur_course_id)
            self.__cur_course_id = None
        finally:
            self.fill_course_list()

    def remove_student(self, event):
        try:
            self.__classroom.remove_student(self.__cur_student_id)
            self.__cur_student_id = None
        finally:
            self.fill_students_list()

    def start(self):
        self.clear_student_input()
        self.fill_students_list()
        self.__window.mainloop()
        self.__classroom.wait_sync()


ClassroomManager().start()
