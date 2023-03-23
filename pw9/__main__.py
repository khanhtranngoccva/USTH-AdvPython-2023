import os
import time
import tkinter
import typing

from .domains.classroom import Classroom


class ClassroomManager:

    def __init__(self):
        self.__classroom = Classroom()
        self.__window = tkinter.Tk()
        self.__window.geometry("1280x720")
        self.__window_entities = {}


        window_entities = self.__window_entities
        window_entities["frame1"] = tkinter.Frame(master=self.__window)
        window_entities["frame1"].pack(fill=tkinter.X, padx=24, pady=16)

        window_entities["title_label"] = tkinter.Label(master=window_entities["frame1"], text="Classroom Manager", font=("Lato", 24, "bold"))
        window_entities["title_label"].pack(side=tkinter.LEFT)

        window_entities["frame2"] = tkinter.Frame(master=self.__window)
        window_entities["frame2"].pack(fill=tkinter.BOTH, expand=True, padx=24, pady=(0, 16))

        window_entities["student_list"] = tkinter.Listbox(master=window_entities["frame2"], width=20)
        window_entities["student_list"].pack(side=tkinter.LEFT, fill=tkinter.Y)

    def fill_students(self):
        student_list = self.__window_entities["student_list"]
        student_list.delete(0, student_list.size())
        student_list.insert(tkinter.END, *(str(student) for student in self.__classroom.list_students()))

    def start(self):
        self.fill_students()
        self.__window.mainloop()
        self.__classroom.wait_sync()






ClassroomManager().start()
