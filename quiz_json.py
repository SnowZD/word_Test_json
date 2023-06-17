import tkinter
from tkinter import messagebox
from tkinter import filedialog
import tkinter.font as tkFont
from tkinter import *
import random
import json
from threading import Timer
import datetime

window = Tk()
window.title("Practice")

w = 400
h = 410
x = 300
y = 200
window.geometry('%dx%d+%d+%d' % (w, h, x, y))
window.resizable(False,False)

fontStyle = tkFont.Font(size=24)

left_frame = Frame(window, width=0, height=0, bg='grey')
left_frame.grid(row=1, column=0, padx=10, pady=0)

overright_frame = Frame(window, width=0, height=0)
overright_frame.grid(row=0, column=1, padx=5, pady=20)

right_frame = Frame(window, width=0, height=0, bg='grey')
right_frame.grid(row=1, column=1, padx=5, pady=0)


def timer_counter():
    global t, m, start_time
    t = Timer(1, timer_counter)
    cur_time = datetime.datetime.now()
    dif = cur_time-start_time
    if dif.seconds == 60:
        start_time = datetime.datetime.now()
        dif = cur_time-start_time
        m = m+1
    t.start()
    try:
        window.title('Practice: %d:%d' % (m, dif.seconds))
    except:
        t.cancel()

def EventShowNext(event):
    i = 0
    recode = {}
    recode['Quiz'] = WordQuiz[n]
    recode['Answer'] = WordAnswer[n]
    if E1.get() in WordAnswer[n]:
        E1.delete(0, END)
        if recode not in Wrong and recode not in Right:
            Right.append(recode)
        del WordAnswer[n]
        del WordQuiz[n]
        ShowQuiz()
    else:
        a1.set(WordAnswer[n])
        WordQuiz.append(WordQuiz[n])
        WordAnswer.append(WordAnswer[n])
        if recode not in Wrong:
            Wrong.append(recode)


def clozemode():
    w = 400
    window.geometry('%dx%d' % (w, h))


def choicemode():
    w = 1200
    window.geometry('%dx%d' % (w, h))


def choice_answer(answer):
    E1.delete(0, END)
    E1.insert(0, answer)
    EventShowNext('<Return>')


E1 = Entry(left_frame, width=23, bd=5, font=fontStyle)
E1.pack(side=TOP)
E1.bind('<Return>', EventShowNext)

a1 = StringVar()
a2 = StringVar()
c1 = StringVar()
c2 = StringVar()
c3 = StringVar()
c4 = StringVar()

AN1 = Label(left_frame, textvariable=a1, font=fontStyle, fg='red')
AN1.pack(side=TOP, pady=5)
AN2 = Label(left_frame, textvariable=a2, font=fontStyle)
AN2.pack(side=TOP)
AN3 = Label(overright_frame, text='Choice Mode', font=fontStyle)
AN3.pack(side=TOP)
AN4 = Label(right_frame, textvariable=a2, font=fontStyle,
            width=30, height=2, pady=1)
AN4.grid(row=0, columnspan=2, padx=0, pady=10)

WordQuiz = []
WordAnswer = []
Wrong = []
Right = []
Change = []
ChangeexamQuiz = []
ChangeexamAnswer = []
t = Timer(0, timer_counter)


def Start():
    global t, m, start_time
    start_time = datetime.datetime.now()
    t = Timer(0, timer_counter)
    m = 0
    t.start()
    ShowQuiz()


def ShowQuiz():
    global n, choiceanswer
    choiceanswer = []
    E1.delete(0, END)
    if len(WordQuiz) > 0:
        n = random.randint(0, len(WordQuiz)-1)
        i = random.randint(0, len(WordQuiz[n])-1)
        a2.set(WordQuiz[n][i])
        a1.set('')
        if len(Change)-1 >= 3:
            while len(choiceanswer) < 4:
                i = random.randint(0, len(Change)-1)
                k = 0
                while k <= len(Change[i]['Quiz'])-1:
                    if Change[i]['Quiz'][k] in choiceanswer:
                        break
                    if k == (len(ChangeexamQuiz[i])-1):
                        k = random.randint(0, len(Change[i]['Quiz'])-1)
                        choiceanswer.append(Change[i]['Quiz'][k])
                        break
                    k = k+1
            k = 0
            while k <= len(WordAnswer[n])-1:
                if WordAnswer[n][k] in choiceanswer:
                    break
                if k == len(WordAnswer[n])-1:
                    i = random.randint(0, 3)
                    k = random.randint(0, len(WordAnswer[n])-1)
                    choiceanswer[i] = WordAnswer[n][k]
                    break
                k = k+1
            c1.set(choiceanswer[0])
            c2.set(choiceanswer[1])
            c3.set(choiceanswer[2])
            c4.set(choiceanswer[3])
            choice01.config(state=NORMAL)
            choice02.config(state=NORMAL)
            choice03.config(state=NORMAL)
            choice04.config(state=NORMAL)
    else:
        t.cancel()
        AN2.configure(fg='red')
        a2.set('End')
        a1.set('')
        c1.set('')
        c2.set('')
        c3.set('')
        c4.set('')
        choice01.config(state=DISABLED)
        choice02.config(state=DISABLED)
        choice03.config(state=DISABLED)
        choice04.config(state=DISABLED)


def input():
    global ChangeexamQuiz, ChangeexamAnswer, WordQuiz, WordAnswer, Wrong, Right
    WordQuiz = []
    WordAnswer = []
    Wrong = []
    Right = []
    AN2.configure(fg='black')
    for n in examdata:
        try:
            with open(n, 'r', encoding='utf-8') as f:
                jsonread = json.load(f)
                for i in jsonread:
                    if i['Answer'] in ChangeexamQuiz:
                        continue
                    ChangeexamQuiz.append(i['Answer'])
                    ChangeexamAnswer.append(i['Quiz'])
                    recode = {}
                    recode['Quiz'] = i['Answer']
                    recode['Answer'] = i['Quiz']
                    Change.append(recode)
            a1.set('Answer')
            a2.set('Quiz')
            startbutton.config(state=NORMAL)
        except:
            messagebox.showinfo(
                'Error', 'File error.(Not the [.json] file, or cannot find the file.)')
    WordQuiz.extend(ChangeexamAnswer)
    WordAnswer.extend(ChangeexamQuiz)


def Readjson():
    global examdata, ChangeexamQuiz, ChangeexamAnswer, WordQuiz, WordAnswer
    ChangeexamQuiz = []
    ChangeexamAnswer = []
    examdata = filedialog.askopenfilenames(
        filetypes=(("json Files", "*.json"), ("All", "*.*")))
    if examdata != "":
        input()
        resetbutton.config(state=NORMAL)


def Reset():
    t.cancel()
    input()


def Exit():
    t.cancel()
    exit()


def Export():
    exportfolder = filedialog.askdirectory()
    with open(exportfolder+'/wrongword.json', 'w', encoding='utf-8')as w:
        jsonString = json.dumps(Wrong, indent=4, ensure_ascii=False)
        w.write(jsonString)
    with open(exportfolder+'/rightword.json', 'w', encoding='utf-8')as w:
        jsonString = json.dumps(Right, indent=4, ensure_ascii=False)
        w.write(jsonString)
    with open(exportfolder+'/changeexam.json', 'w', encoding='utf-8')as w:
        jsonString = json.dumps(Change, indent=4, ensure_ascii=False)
        w.write(jsonString)


startbutton = tkinter.Button(
    left_frame, text="Start", command=Start, font=fontStyle, state=DISABLED)
readbutton = tkinter.Button(
    left_frame, text="Read「.json」", command=Readjson, font=fontStyle)
resetbutton = tkinter.Button(
    left_frame, text="Reset", command=Reset, font=fontStyle, state=DISABLED)
outputbutton = tkinter.Button(
    left_frame, text="Export", command=Export, font=fontStyle)
clozemodebutton = tkinter.Button(
    window, text="ClozeMode", command=clozemode, font=fontStyle)
choicemodebutton = tkinter.Button(
    window, text="ChoiceMode", command=choicemode, font=fontStyle)
exitbutton = tkinter.Button(
    left_frame, text="Exit", command=Exit, font=fontStyle)

choice01 = tkinter.Button(
    right_frame, textvariable=c1, width=20, command=lambda: choice_answer(c1.get()), font=fontStyle, state=DISABLED)
choice02 = tkinter.Button(
    right_frame, textvariable=c2, width=20, command=lambda: choice_answer(c2.get()), font=fontStyle, state=DISABLED)
choice03 = tkinter.Button(
    right_frame, textvariable=c3, width=20, command=lambda: choice_answer(c3.get()), font=fontStyle, state=DISABLED)
choice04 = tkinter.Button(
    right_frame, textvariable=c4, width=20, command=lambda: choice_answer(c4.get()), font=fontStyle, state=DISABLED)

clozemodebutton.place(x=15, y=10)
choicemodebutton.place(x=195, y=10)
startbutton.pack(side=TOP, pady=5)
readbutton.pack(side=TOP)
resetbutton.pack(side=RIGHT, padx=3)
outputbutton.pack(side=RIGHT, pady=5, padx=20)
exitbutton.pack(side=LEFT, padx=3)

choice01.grid(row=1, column=0, padx=20, pady=30)
choice02.grid(row=1, column=1, padx=20, pady=30)
choice03.grid(row=2, column=0, padx=20, pady=30)
choice04.grid(row=2, column=1, padx=20, pady=30)

window.mainloop()
