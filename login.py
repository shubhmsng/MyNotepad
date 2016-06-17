from tkinter import *
import tkinter
import tkinter.messagebox

root = Tk()
root.geometry('451x181+451+151')
root.title("Log In")
root.wm_iconbitmap('Notepad++.ico')
root.configure(background='#3f3f3f')

def login():
    print(username, password)
    if user == "admin" and password == "admin":
        import MyNotepad



Label(root, text="Username").place(x=30, y=45)
user = StringVar()
u = Entry(root, width=30, textvariable=user).place(x=150, y=45)
username = user.get()
Label(root, text="Password").place(x=30, y=85)
password = StringVar()
Entry(root, width=30, textvariable=password, show="*").place(x=150, y=85)
password = password.get()

b = Button(root, text="OK", relief='groove', underline=0, command=login).place(x=150, y=125)

root.mainloop()