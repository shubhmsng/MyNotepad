from tkinter import *
import tkinter.filedialog
import os
import tkinter.font
import tkinter.messagebox
from gtts import gTTS
import speech_recognition as sr
from pygame import mixer

root = Tk()
helv = tkinter.font.Font(family='Lucida Bright', size=12, weight='normal')
hel = tkinter.font.Font(family='Arial', size=10, weight='normal')
showlen = BooleanVar()
showlen.set(True)
theme = StringVar()

helpimage = PhotoImage(file='help.gif')

clrschms = {
    'Default White': 'E2FFFF.FFFFFF',
    'White': '000000.FFFFFF',
    'Greygarious Grey': '83406A.D1D4D1',
    'Lovely Lavender': '202B4B.E1E1FF',
    'Aquamarine': '5B8340.D1E7E0',
    'Bold Beige': '4B4620.FFF0E1',
    'Cobalt Blue': 'ffffBB.3333aa',
    'Olive Green': 'D1E7E0.5B8340',
}


# root designing

root.geometry('651x481+51+51')
root.title("*Untitled - My Notepad")
root.wm_iconbitmap('Notepad++.ico')
root.configure(background='#1f1f1f')


# menubar functions

def speech():
    r = sr.Recognizer()
    tkinter.messagebox.showinfo("Speech", "press enter to start speaking and say stop to quit!!")

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("set min threshold energy to {}".format(r.energy_threshold))

        print("Say something")
        audio = r.listen(source)
    try:
        a = r.recognize_google(audio)

    except:
        print("speech error")
        tkinter.messagebox.showinfo("Error", "An error occurred make sure you have connected to internet!!.")

    try:
        if a == 'exit':
            doSomething()

        elif a == 'new + line':
            textPad.insert(textPad.index(INSERT), '\n')

        elif a == 'back + space':
            a = textPad.index(INSERT)
            i, j = a.split('.')
            j = str(int(j) - 1)
            b = str(i) + '.' + str(j)
            print(a, b)
            textPad.delete(b, a)

        elif a == 'stop':
            tkinter.messagebox.showinfo("Stop", "Speech to text function has been stopped")
            return
        else:
            i, j = textPad.index(INSERT).split('.')
            if j != '0':
                textPad.insert(textPad.index(INSERT), " ")
            textPad.insert(textPad.index(INSERT), a)
    except:
        pass

    speech()


def text_to_speech():

    s = textPad.get('1.0', textPad.index(INSERT))

    try:
        tts = gTTS(text=s, lang='en')

    except:
        tkinter.messagebox.showinfo("Error", "An error occured make sure you have connected to internet!!")

    try:
        tts.save("temp.mp3")
        mixer.init()
        mixer.music.load("temp.mp3")
        mixer.music.play()

        try:
            os.remove("temp2.mp3")

        except:
            pass

    except:
        tts.save("temp2.mp3")
        mixer.music.load("temp2.mp3")
        mixer.music.play()
        os.remove("temp.mp3")


def search_for(needle, textPad, t2, e):
    textPad.tag_remove('match', '1.0', END)
    count = 0
    if needle:
        pos = '1.0'
        while True:
            pos = textPad.search(needle, pos, stopindex=END)
            if not pos: break
            lastpos = '%s+%dc' % (pos, len(needle))
            textPad.tag_add('match', pos, lastpos)
            count += 1
            pos = lastpos
            textPad.tag_config('match', foreground='red', background='yellow')
        e.focus_set()
        t2.title('%d matches found' % count)


def on_find():
    t2 = Toplevel(root)
    t2.title('Find')
    t2.wm_iconbitmap('find.ico')
    t2.geometry('280x100+200+250')

    t2.transient(root)
    Label(t2, text="Find What:").place(x=10, y=25)
    v = StringVar()
    e = Entry(t2, width=25, textvariable=v)
    e.place(x=80, y=25)
    e.focus_set()
    Button(t2, text="Find All", relief='groove', underline=0,
           command=lambda: search_for(v.get(), textPad, t2, e)).place(x=120, y=60)

    def close_search():
        textPad.tag_remove('match', '1.0', END)
        t2.destroy()

    t2.protocol('WM_DELETE_WINDOW', close_search)


def search(event):
    on_find()


def save():
    global filename
    try:
        # f = tkinter.filedialog.asksaveasfile(initialfile =filename, filetypes=[("AllFiles","*.*"),("Text Documents","*.txt")])
        f = open(filename, 'w')
        letter = textPad.get(1.0, 'end')
        f.write(letter)
        f.close()
        root.title(filename + " - My Notepad")

    except:
        f = tkinter.filedialog.asksaveasfile(initialfile="Untitled.txt",
                                             filetypes=[("AllFiles", "*.*"), ("Text Documents", "*.txt")])
        f = open(filename, 'w')
        letter = textPad.get(1.0, 'end')
        f.write(letter)
        f.close()
        root.title(filename + " - My Notepad")
    update_line()


def open_file():
    v = textPad.index(INSERT)
    if v != '1.0':
        if tkinter.messagebox.askokcancel("Save", "Do you want to save current file?"):
            save()
    global filename
    filename = tkinter.filedialog.askopenfilename(defaultextension=".txt",
                                                  filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if filename == "":
        filename = None
    else:
        root.title("*" + os.path.basename(filename) + " - My Notepad")
        textPad.delete(1.0, END)
        fh = open(filename, "r")
        textPad.insert(1.0, fh.read())
        fh.close()
    update_line()


def save_as():
    try:
        f = tkinter.filedialog.asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt",
                                                 filetypes=[("AllFiles", "*.*"), ("Text Documents", "*.txt")])
        fh = open(f, 'w')
        textoutput = textPad.get(1.0, END)
        fh.write(textoutput)
        fh.close()
        root.title(os.path.basename(f) + " - My Notepad")
    except:
        pass
    update_line()


def new_file():
    v = textPad.index(INSERT)
    if v != '1.0':
        if tkinter.messagebox.askokcancel("Save", "Do you want to save current file?"):
            save()
    root.title("*Untitled" + " - My Notepad")
    global filename
    filename = None
    textPad.delete(1.0, END)
    update_line()


def open_f(event):
    open_file()
    update_line()


def save_f(event):
    save()
    update_line()


def save_as_f(event):
    save_as()
    update_line()


def new_f(event):
    new_file()
    update_line()


def update_line():
    if showlen.get():
        currline, curcolumn = textPad.index("insert").split('.')
        infobar.config(text='Line: %s | Column: %s' % (currline, curcolumn), bg='#e2ffff', relief='groove')
    else:
        infobar.config(text='', bg='#e2ffff', relief='groove')


def update_ln(event):
    update_line()


def sel_theme():
    global bgc, fgc
    val = theme.get()
    clrs = clrschms.get(val)
    fgc, bgc = clrs.split('.')
    fgc, bgc = '#' + fgc, '#' + bgc
    textPad.config(bg=bgc, fg=fgc)
    update_line()


def replace(a, text, textPad, t3, e1, e2):
    count = 0
    if a:
        pos = '1.0'
        while True:

            pos = textPad.search(a, pos, stopindex=END)
            if not pos: break
            lastpos = '%s+%dc' % (pos, len(a))
            textPad.delete(pos, lastpos)

            count += 1
            textPad.insert(pos, text)
            lastpos = '%s+%dc' % (pos, len(text))
            textPad.tag_add('match', pos, lastpos)
            pos = lastpos
            textPad.tag_config('match', foreground='red', background='yellow')
        e1.focus_set()
        e2.focus_set()
        t3.title('%d matches found' % count)


def on_replace(event=NONE):
    t3 = Toplevel(root)
    t3.title('Replace')
    t3.wm_iconbitmap('find.ico')
    t3.geometry('350x100+200+250')

    t3.transient(root)
    Label(t3, text="Find What:     ").grid(row=0, column=0, sticky='w')
    Label(t3, text="Replace With:   ").grid(row=1, column=0, sticky='w')
    v1 = StringVar()
    v2 = StringVar()
    e1 = Entry(t3, width=25, textvariable=v1)
    e1.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    e1.focus_set()
    e2 = Entry(t3, width=25, textvariable=v2)
    e2.grid(row=1, column=1, padx=2, pady=2, sticky='we')
    e2.focus_set()
    Button(t3, text="Replace All", underline=0, relief='groove',
           command=lambda: replace(v1.get(), v2.get(), textPad, t3, e1, e2)).place(x=120, y=60)

    def close_search():
        textPad.tag_remove('match', '1.0', END)
        t3.destroy()

    t3.protocol('WM_DELETE_WINDOW', close_search)

    update_line()


def cut():
    textPad.event_generate("<<Cut>>")
    update_line()


def copy():
    textPad.event_generate("<<Copy>>")
    update_line()


def paste():
    textPad.event_generate("<<Paste>>")
    update_line()


def clear():
    textPad.delete(0.0, 'end')
    update_line()


def delete():
    textPad.delete(INSERT, None)
    update_line()


def undo():
    textPad.event_generate("<<Undo>>")
    update_line()


def redo():
    textPad.event_generate("<<Redo>>")
    update_line()


def select():
    textPad.tag_add("sel", '1.0', 'end')
    update_line()


def pop_up(event):
    cmenu.tk_popup(event.x_root, event.y_root, 0)
    update_line()


def help_(event=None):
    tkinter.messagebox.showinfo("Help",
                                "What is Notepad?\nNotepad is a basic text-editing program and it's most commonly used to view or edit text files.\nA text file is a file type typically identified by the .txt file name extension.\nNot only .txt file you open , edit  and save any type of file.")


def about(event=None):
    tkinter.messagebox.showinfo("About",
                                "\n\t      My Notepad\n\n\n This notepad is developed by shubham singh\n Btech(CSE)(2013-17) student at IERT Alld.\n You can follow me on facebook: \n facebook.com/shubhamatiert\n Email-id: shubhmsing@gmail.com \n Mob.No. 7783984676")


def quit_(event=None):
    root.destroy()


def doSomething():
    mixer.quit()
    try:
        os.remove("temp.mp3")
    except:
        pass
    try:
        os.remove("temp2.mp3")
    except:
        pass

    v = textPad.index(INSERT)
    if v != '1.0':
        t4 = Toplevel(root)
        t4.title("Save")
        t4.iconbitmap('help.ico')
        t4.geometry('290x140+200+250')
        t4.configure(background='#ffffff')
        t4.transient(root)

        def nt():
            t4.destroy()

        def sve():
            save()
            t4.destroy()
            qt()

        def qt():
            quit_()

        Label(t4, text="     ", image=helpimage).place(x=20, y=20)
        Label(t4, text="Do you want save this file ?", bg='#ffffff', font=hel).place(x=70, y=25)
        frm = Frame(t4, bg='#efefef', height='40')
        frm.pack(side=BOTTOM, anchor='sw', fill=X)
        Button(frm, text="Save", relief='groove', command=sve).place(x=10, y=5, width=80)
        Button(frm, text="Don't Save", relief='groove', command=qt).place(x=105, y=5, width=80)
        Button(frm, text="Cancel", relief='groove', command=nt).place(x=200, y=5, width=80)
    else:
        root.destroy()


# menubar
menubar = Menu(root)

filemenu = Menu(menubar, tearoff=1)
filemenu.add_command(label="New  ", accelerator='Ctrl+N', command=new_file)
filemenu.add_command(label="Open...  ", accelerator='Ctrl+O', command=open_file)
filemenu.add_command(label="Save  ", accelerator='Ctrl+S', command=save)
filemenu.add_command(label="Save As...  ", accelerator='Shift+Ctrl+S', command=save_as)
filemenu.add_separator()
filemenu.add_command(label="Exit  ", accelerator='Alt+F4', command=doSomething)
menubar.add_cascade(label="File  ", menu=filemenu)

editmenu = Menu(menubar, tearoff=1)
editmenu.add_command(label="Undo", accelerator='Ctrl+Z', command=undo)
editmenu.add_command(label="Redo", accelerator='Ctrl+Y', command=redo)
editmenu.add_separator()
editmenu.add_command(label="Cut", accelerator='Ctrl+X', command=cut)
editmenu.add_command(label="Copy", accelerator='Ctrl+C', command=copy)
editmenu.add_command(label="Paste", accelerator='Ctrl+V', command=paste)
editmenu.add_command(label="Delete", accelerator='Del', command=delete)
editmenu.add_command(label="Clear", command=clear)
editmenu.add_separator()
editmenu.add_command(label="Find...", accelerator='Ctrl+F', command=on_find)
editmenu.add_command(label="Replace...", accelerator='Ctrl+H', command=on_replace)
editmenu.add_separator()
editmenu.add_command(label="Select All", accelerator='Ctrl+A', command=select)
editmenu.add_command(label="Speech to text", command=speech)
editmenu.add_command(label="Text to speech", command=text_to_speech)

menubar.add_cascade(label="Edit", menu=editmenu)

viewmenu = Menu(menubar, tearoff=1)
viewmenu.add_checkbutton(label="Show Status Bar  ", variable=showlen, command=update_line)
themesmenu = Menu(viewmenu, tearoff=1)
themesmenu.add_radiobutton(label="White", variable=theme, command=sel_theme)
themesmenu.add_radiobutton(label="Greygarious Grey", variable=theme, command=sel_theme)
themesmenu.add_radiobutton(label="Lovely Lavender", variable=theme, command=sel_theme)
themesmenu.add_radiobutton(label="Aquamarine", variable=theme, command=sel_theme)
themesmenu.add_radiobutton(label="Bold Beige", variable=theme, command=sel_theme)
themesmenu.add_radiobutton(label="Cobalt Blue", variable=theme, command=sel_theme)
themesmenu.add_radiobutton(label="Olive Green", variable=theme, command=sel_theme)
viewmenu.add_cascade(label="Themes  ", menu=themesmenu)
menubar.add_cascade(label="View", menu=viewmenu)

helpbar = Menu(menubar, tearoff=1)
helpbar.add_command(label="View Help ", command=help_)
helpbar.add_command(label="About My Notepad", command=about)
menubar.add_cascade(label="Help", menu=helpbar)

root.config(menu=menubar)  # show menubar

label1 = Label(root, bg='#e2ffff')
label1.pack(side=TOP, anchor='nw', fill=X)
lnlabel2 = Label(root, bg='#e2ffff')
lnlabel2.pack(side=BOTTOM, anchor='sw', fill=X)

lnlabel = Label(root, width=2, bg='#e2ffff')
lnlabel.pack(side=RIGHT, anchor='ne', fill=Y)

lnlabel1 = Label(root, width=1, bg='#e2ffff')
lnlabel1.pack(side=LEFT, anchor='nw', fill=Y)

textPad = Text(root, undo=True, bg="light yellow", wrap=NONE, font=helv, padx=10, pady=10)
textPad.pack(expand=YES, fill=BOTH)
scroll = Scrollbar(lnlabel, orient=VERTICAL)
scroll2 = Scrollbar(lnlabel2, orient=HORIZONTAL)
textPad.configure(yscrollcommand=scroll.set, xscrollcommand=scroll2.set)
scroll.config(command=textPad.yview)
scroll2.config(command=textPad.xview)
scroll.pack(side=RIGHT, fill=Y)
scroll2.pack(side=BOTTOM, fill=X)

infobar = Label(label1)
infobar.pack(expand=NO, fill=None, side=RIGHT, anchor='ne')

update_line()

cmenu = Menu(textPad, tearoff=0, font=hel)
for i in ('cut', 'copy', 'paste', 'undo', 'redo'):
    cmd = eval(i)
    cmenu.add_command(label=i, compound=LEFT, command=cmd)
cmenu.add_separator()
cmenu.add_command(label='Select All', underline=7, command=select)

# shortcut binding
root.protocol('WM_DELETE_WINDOW', doSomething)
root.bind("<Alt-F4>", doSomething)
root.bind("<Button-3>", pop_up)
root.bind("<Any-KeyPress>", update_ln)
root.bind("<Control-f>", search)
root.bind("<Control-F>", search)
root.bind("<Control-N>", new_f)
root.bind("<Control-n>", new_f)
root.bind("<Control-O>", open_f)
root.bind("<Control-o>", open_f)
root.bind("<Control-H>", on_replace)
root.bind("<Control-h>", on_replace)
root.bind("<Control-s>", save_f)
root.bind("<Control-S>", save_f)
root.bind("<Shift-Control-s>", save_as_f)
root.bind("<Shift-Control-S>", save_as_f)

root.mainloop()
