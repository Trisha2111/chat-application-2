import socket
from threading import Thread
from tkinter import *


client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip="127.0.0.1"
port=8000
client.connect((ip,port))
print("Connected with the server")

class GUI:
    def __init__(self):
        self.Window=Tk()
        self.Window.withdraw()
        self.login=Toplevel()
        self.login.title("Login")
        self.login.resizable(width=False,height=False)
        self.login.configure(width=400,height=300)
        self.header=Label(self.login,text="PLEASE LOGIN TO CONTINUE!",justify=CENTER,font="Helvetica 14 bold")
        self.header.place(relheight=0.15,relx=0.15,rely=0.07)

        self.labelname=Label(self.login,text="NAME: ",font="Helvetica 14 ")
        self.labelname.place(relheight=0.2,relx=0.1,rely=0.2)

        self.name=Entry(self.login,font="Helvetica 14")
        self.name.place(relwidth=0.4,relheight=0.15,relx=0.4,rely=0.2)
        self.name.focus()

        self.button=Button(self.login,text="LOGIN",font="Helvetica 14 bold",command=lambda: self.goahead(self.name.get()))
        self.button.place(relx=0.4,rely=0.55)


        self.Window.mainloop()
    
    def goahead(self,name):
        self.login.destroy()
        self.layout(name)
        rcv=Thread(target=self.recieve)
        rcv.start()

    def layout(self,name):
        self.name=name
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False,height=False)
        self.Window.configure(width=470,height=550,bg="#17202a")

        self.labelhead=Label(self.Window,bg="#17202a",fg="#Eaecee",text=self.name,font="Helvetica 14 bold",pady=5)
        self.labelhead.place(relwidth=1)

        self.line=Label(self.Window,width=450,bg="#abb289")
        self.line.place(relwidth=1,relheight=0.012,rely=0.07)

        self.textarea=Text(self.Window,width=20,height=2,bg="#17202a",fg="#eaecee",font="Helvetica 14",padx=5,pady=5)
        self.textarea.place(relheight=0.745,relwidth=1,rely=0.08)

        self.labelbottom=Label(self.Window,bg="#abb289",height=80)
        self.labelbottom.place(relwidth=1,rely=0.825)

        self.entrymessage=Entry(self.labelbottom,bg="#2c3e50",fg="#eaecee",font="Helvetica 13")
        self.entrymessage.place(relwidth=0.74,relheight=0.06,rely=0.008,relx=0.011)

        self.sendbutton=Button(self.labelbottom,text="Send",font="Helvetica 10 bold",width=20,bg="#abb289",command=lambda:self.sendmessage(self.entrymessage.get()))
        self.sendbutton.place(relx=0.77,rely=0.008,relheight=0.06,relwidth=0.22)
        self.textarea.config(cursor="arrow")

        scrollbar=Scrollbar(self.textarea)
        scrollbar.place(relheight=1,relx=0.974)
        scrollbar.config(command=self.textarea.yview)
        self.textarea.config(state=DISABLED)

        
    def sendmessage(self,msg):
        self.textarea.config(state=DISABLED)
        self.msg=msg
        self.entrymessage.delete(0,END)
        sendtext=Thread(target=self.write)
        sendtext.start()

    def showmessage(self,message):
        self.textarea.config(state=NORMAL)
        self.textarea.insert(END,message+"\n\n")
        self.textarea.config(state=DISABLED)
        self.textarea.see(END)


    def recieve(self):
        while True:
            try:
                message=client.recv(2048).decode("utf-8")
                if message =="NICKNAME":
                    client.send(self.name.encode("utf-8"))
                else:
                    self.showmessage(message)
            except:
                print("An Error occured")
                client.close()
                break
        
    def write(self):
        self.textarea.config(state=DISABLED)
        while True:
            message=f"{self.name}: {self.msg}"
            client.send(message.encode("utf-8"))
            self.showmessage(message)
            break


g=GUI()