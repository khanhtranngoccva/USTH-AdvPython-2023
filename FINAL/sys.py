from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import pymysql
import mysql.connector


root = Tk()
root.title("SYLLABUS MANAGEMENT SYSTEM")
root.geometry("1500x780+0+0")
root.resizable(False, False)

logo=Label(root,bd=15,relief=RIDGE,text="SYLLABUS MANAGEMENT SYSTEM",fg="red",bg='#FFEBCD',font=("times new roman",30,"bold"))
logo.pack(side=TOP,fill=X)

#input bolder   
MainFrame=Frame(root,bd=20,relief=RIDGE,bg='#FFEBCD').place(x=0,y=80,width=1499,height=700)
InputCourseFrame=Frame(root,bd=10,relief=RIDGE,bg='#FFEBCD').place(x=20,y=100,width=510,height=460)
TimeCommitmentFrame=Frame(root,bd=10,relief=RIDGE,bg='#FFEBCD').place(x=530,y=100,width=949,height=170)
AssessmentFrame=Frame(root,bd=10,relief=RIDGE,bg='#FFEBCD').place(x=530,y=270,width=949,height=290)
Button_Frame=Frame(root,bd=10,relief=RIDGE,bg='#FFEBCD').place(x=20,y=560,width=1459,height=200)

#Function
def list():
    global cur, con
    con=pymysql.connect(host = '127.0.0.1', user = 'root', passwd= '123456', database= 'Syllabus_management_system')
    cur = con.cursor()
    query = 'select * from syllabus'
    cur.execute(query)
    fetched_data = cur.fetchall() #fetchall() method, which fetches all rows from the last executed statement
    Syllabus_table.delete(*Syllabus_table.get_children())
    for data in fetched_data:
        Syllabus_table.insert('', END, values=data)

    
def search():
    cur.execute('select * from syllabus where id=%s or major_id=%s or course_name=%s or credit_points_inECTs=%s or background_knowledge=%s or background_knowledge=%s or textbook=%s or course_content=%s or objectives=%s',(Id.get(), major.get(), nameCourse.get(), credit.get(), background.get(), textbook.get(), reference.get(), content.get(), objectives.get()))
    Syllabus_table.delete(*Syllabus_table.get_children())
    fetched_data=cur.fetchall()
    for data in fetched_data:
        Syllabus_table.insert('',END,values=data)
    
def Add():
    if nameCourse.get()=='' or major.get()=='' or credit.get()=='' or background.get()=='' or textbook.get()=='' or reference.get()=='' or content.get()=='' or objectives.get()=='' or lecture.get()=='' or tutor.get()=='' or pract.get()=='' or atten.get()=='' or exe.get()=='' or assign.get()=='' or report.get()=='' or mid.get()=='' or final.get()=='':
        messagebox.showerror('Error','All Feilds are required')
    else:
        cur.execute('insert into syllabus values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)', (Id.get(), nameCourse.get() , major.get() , credit.get() , background.get() , textbook.get() , reference.get() , content.get() , objectives.get() , lecture.get() , tutor.get() , pract.get() , atten.get() , exe.get() , assign.get() , report.get() , mid.get() , final.get()))
        con.commit()

    query='select *from syllabus'
    cur.execute(query)
    fetched_data = cur.fetchall()
    Syllabus_table.delete(*Syllabus_table.get_children())
    for data in fetched_data:
            Syllabus_table.insert('',END,values=data)

def delete():
    indexing=Syllabus_table.focus()
    print(indexing)
    cont=Syllabus_table.item(indexing)
    cont_id=cont["values"][0]
    cur.execute('delete from syllabus where id = %s', cont_id)
    con.commit()
    messagebox.showinfo('Deleted', f'Id {cont_id} is delete succesfully') 	
    show()

def reset():
    result=messagebox.askyesno('Confirm', 'Do you want to clean the form?')
    if result:
        Id.set("")
        nameCourse.set("")
        major.set("")
        credit.set("")
        background.set("")
        textbook.set("")
        reference.set("")
        content.set("")
        objectives.set("")
        lecture.set("")
        tutor.set("")
        pract.set("")
        atten.set("")
        exe.set("")
        assign.set("")
        report.set("")
        mid.set("")
        final.set("")
    else:
        pass

def show():
    cur.execute('select *from syllabus')
    fetched_data = cur.fetchall()
    Syllabus_table.delete(*Syllabus_table.get_children())
    for data in fetched_data:
        Syllabus_table.insert('', END, values=data)

def view():
    indexing=Syllabus_table.focus()
    cont=Syllabus_table.item(indexing)
    row=cont['values']
    Id.set(row[0])
    nameCourse.set(row[1])
    major.set(row[2])
    credit.set(row[3])
    background.set(row[4])
    textbook.set(row[5])
    reference.set(row[6])
    content.set(row[7])
    objectives.set(row[8])
    lecture.set(row[9])
    tutor.set(row[10])
    pract.set(row[11])
    atten.set(row[12])
    exe.set(row[13])
    assign.set(row[14])
    report.set(row[15])
    mid.set(row[16])
    final.set(row[17])

def update():

    cur.execute("update syllabus set major_id=%s, course_name=%s, credit_points_inECTs=%s, background_knowledge=%s, textbook=%s, ref_literature=%s, course_content=%s, objectives=%s, lecture=%s, tutorial=%s, practical=%s, attendance=%s, exercise=%s, assignment=%s, report=%s, midterm=%s, final=%s where id=%s",
                                    ( major.get() , nameCourse.get(), credit.get() , background.get() , textbook.get() , reference.get() , content.get() , objectives.get() , lecture.get() , tutor.get() , pract.get() , atten.get() , exe.get() , assign.get() , report.get() , mid.get() , final.get(), Id.get()))
    con.commit()
    show()

    
#input bolder   


Id = tk.StringVar()
nameCourse = tk.StringVar()
major = tk.StringVar()
credit = tk.StringVar()
background = tk.StringVar()
textbook = tk.StringVar()
reference = tk.StringVar()
content = tk.StringVar()
objectives = tk.StringVar()
lecture = tk.StringVar()
tutor = tk.StringVar()
pract = tk.StringVar()
atten = tk.StringVar()
exe = tk.StringVar()
assign = tk.StringVar()
report = tk.StringVar()
mid = tk.StringVar()
final = tk.StringVar()

LbId=Label(font=("times new roman",13,"bold"),text="Id:",bg='#FFEBCD').place(x=40,y=115,width=200,height=30)
IpId=Entry(font=("times new roman",13,"bold"),textvariable=Id).place(x=250,y=115,width=250,height=30)

LbName=Label(font=("times new roman",13,"bold"),text="Name Course:",bg='#FFEBCD').place(x=40,y=165,width=200,height=30)
IpName=Entry(font=("times new roman",13,"bold"),textvariable= nameCourse).place(x=250,y=165,width=250,height=30)

LbMajor=Label(font=("times new roman",13,"bold"),text="Major:",bg='#FFEBCD').place(x=40,y=215,width=200,height=30)
IpMajor=ttk.Combobox(font=("times new roman",13,"bold"),textvariable= major).place(x=250,y=215,width=250,height=30)

LbCredit=Label(font=("times new roman",13,"bold"),text="Credit Points:",bg='#FFEBCD').place(x=40,y=265,width=200,height=30)
IpCredit=Entry(font=("times new roman",13,"bold"),textvariable= credit).place(x=250,y=265,width=250,height=30)

LbBacK=Label(font=("times new roman",13,"bold"),text="BackGround Knowledge:",bg='#FFEBCD').place(x=40,y=315,width=200,height=30)
IpBacK=Entry(font=("times new roman",13,"bold"),textvariable= background).place(x=250,y=315,width=250,height=30)

LbTexB=Label(font=("times new roman",13,"bold"),text="TextBook:",bg='#FFEBCD').place(x=40,y=365,width=200,height=30)
IpTexB=Entry(font=("times new roman",13,"bold"),textvariable= textbook).place(x=250,y=365,width=250,height=30)

LbRefL=Label(font=("times new roman",13,"bold"),text="Reference Literature:",bg='#FFEBCD').place(x=40,y=415,width=200,height=30)
IpRefL=Entry(font=("times new roman",13,"bold"),textvariable=reference).place(x=250,y=415,width=250,height=30)

LbCouContent=Label(font=("times new roman",13,"bold"),text="Course Content:",bg='#FFEBCD').place(x=40,y=465,width=200,height=30)
IpCouContent=Entry(font=("times new roman",13,"bold"),textvariable=content).place(x=250,y=465,width=250,height=30)

LbObj=Label(font=("times new roman",13,"bold"),text="Objectives:",bg='#FFEBCD').place(x=40,y=515,width=200,height=30)
IpObj=Entry(font=("times new roman",13,"bold"),textvariable=objectives).place(x=250,y=515,width=250,height=30)

LbCredit=Label(font=("times new roman",13,"bold"),text="Time Commitement:",bg='#FFEBCD').place(x=550,y=185,width=200,height=30)

LbTLecture=Label(font=("times new roman",13,"bold"),text="Lecture:",bg='#FFEBCD').place(x=770,y=150,width=120,height=30)
IpTLecture=Entry(font=("times new roman",13,"bold"),textvariable=lecture).place(x=900,y=150,width=150,height=30)

LbTTutor=Label(font=("times new roman",13,"bold"),text="Tutorial:",bg='#FFEBCD').place(x=770,y=205,width=120,height=30)
IpTTutor=Entry(font=("times new roman",13,"bold"),textvariable=tutor).place(x=900,y=205,width=150,height=30)

LbTPract=Label(font=("times new roman",13,"bold"),text="Practical:",bg='#FFEBCD').place(x=1070,y=150,width=120,height=30)
IpTPract=Entry(font=("times new roman",13,"bold"),textvariable=pract).place(x=1200,y=150,width=150,height=30)

LbAsses=Label(font=("times new roman",13,"bold"),text="Assessment:",bg='#FFEBCD').place(x=550,y=355,width=200,height=30)

LbAtten=Label(font=("times new roman",13,"bold"),text="Attendance:",bg='#FFEBCD').place(x=770,y=300,width=120,height=30)
IpAtten=Entry(font=("times new roman",13,"bold"),textvariable=atten).place(x=900,y=300,width=150,height=30)

LbExe=Label(font=("times new roman",13,"bold"),text="Exercises:",bg='#FFEBCD').place(x=770,y=360,width=120,height=30)
IpExe=Entry(font=("times new roman",13,"bold"),textvariable=exe).place(x=900,y=360,width=150,height=30)

LbAssign=Label(font=("times new roman",13,"bold"),text="Assignments:",bg='#FFEBCD').place(x=770,y=420,width=120,height=30)
IpAssign=Entry(font=("times new roman",13,"bold"),textvariable=assign).place(x=900,y=420,width=150,height=30)

LbReports=Label(font=("times new roman",13,"bold"),text="Reports:",bg='#FFEBCD').place(x=1070,y=300,width=120,height=30)
IpReports=Entry(font=("times new roman",13,"bold"),textvariable=report).place(x=1200,y=300,width=150,height=30)

LbMid=Label(font=("times new roman",13,"bold"),text="Midterm:",bg='#FFEBCD').place(x=1070,y=360,width=120,height=30)
IpMid=Entry(font=("times new roman",13,"bold"),textvariable= mid).place(x=1200,y=360,width=150,height=30)

LbFinal=Label(font=("times new roman",13,"bold"),text="Final:",bg='#FFEBCD').place(x=1070,y=420,width=120,height=30)
IpFinal=Entry(font=("times new roman",13,"bold"),textvariable= final).place(x=1200,y=420,width=150,height=30)


#creat button
BtSearch=Button(font=("times new roman",13,"bold"),text="SEARCH", command=search).place(x=580,y=500,width=100)
BtAdd=Button(font=("times new roman",13,"bold"),text="ADD",command=Add).place(x=700,y=500,width=100)
BtReset=Button(font=("times new roman",13,"bold"),text="RESET", command=reset).place(x=820,y=500,width=100)
BtDelete=Button(font=("times new roman",13,"bold"),text="DELETE", command=delete).place(x=940,y=500,width=100)
BtUpdate=Button(font=("times new roman",13,"bold"),text="UPDATE", command=update).place(x=1110,y=500,width=100)
BtView=Button(font=("times new roman",13,"bold"),text="VIEW", command=view).place(x=1230,y=500,width=100)
BtList=Button(font=("times new roman",13,"bold"),text="LIST", command=list).place(x=1350,y=500,width=100)


#create table
scrollBarX=Scrollbar(Button_Frame, orient=HORIZONTAL)
scrollBarY=Scrollbar(Button_Frame, orient=VERTICAL)

Syllabus_table=ttk.Treeview(Button_Frame, columns=('id', 'major_id', 'course_name', 'credit_points_inECTs', 'background_knowledge', 'textbook', 'ref_literature', 'course_content', 'objectives',\
                                        'lecture', 'tutorial', 'practical', 'attendance', 'exercise', 'assignment', 'report', 'midterm', 'final'),
                            xscrollcommand=scrollBarX.set,yscrollcommand=scrollBarY.set)

Syllabus_table.place(x=27,y=567,width=1450,height=190)
scrollBarX.config(command=Syllabus_table.xview)
scrollBarY.config(command=Syllabus_table.yview)

scrollBarX.pack(side=BOTTOM,fill=X)
scrollBarY.pack(side=RIGHT,fill=Y)

Syllabus_table.heading('id', text='ID')
Syllabus_table.heading('course_name', text='Name Course')
Syllabus_table.heading('major_id', text='Major')
Syllabus_table.heading('credit_points_inECTs', text='Credit points')
Syllabus_table.heading('background_knowledge', text='Background knowledge')
Syllabus_table.heading('textbook', text='TextBook')
Syllabus_table.heading('ref_literature', text='Reference Literature')
Syllabus_table.heading('course_content', text='Course Content')
Syllabus_table.heading('objectives', text='Objectives')
Syllabus_table.heading('lecture', text='Lecture')
Syllabus_table.heading('tutorial', text='Tutorial')
Syllabus_table.heading('practical', text='Practical')
Syllabus_table.heading('attendance', text='Attendance')
Syllabus_table.heading('exercise', text='Exercise')
Syllabus_table.heading('assignment', text='Assignment')
Syllabus_table.heading('report', text='Report')
Syllabus_table.heading('midterm', text='Midterm')
Syllabus_table.heading('final', text='Final')

Syllabus_table.column('id', width=30, anchor=CENTER)
Syllabus_table.column('major_id', width=80, anchor=CENTER)
Syllabus_table.column('credit_points_inECTs', width=80, anchor=CENTER)
Syllabus_table.column('lecture', width=80, anchor=CENTER)
Syllabus_table.column('tutorial', width=80, anchor=CENTER)
Syllabus_table.column('practical', width=80, anchor=CENTER)
Syllabus_table.column('attendance', width=80, anchor=CENTER)
Syllabus_table.column('exercise', width=80, anchor=CENTER)
Syllabus_table.column('assignment', width=80, anchor=CENTER)
Syllabus_table.column('report', width=80, anchor=CENTER)
Syllabus_table.column('midterm', width=80, anchor=CENTER)
Syllabus_table.column('final', width=80, anchor=CENTER)



Syllabus_table.config(show='headings')


root.mainloop()