import socket 
from threading import Thread

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip="127.0.0.1"
port=8000
server.bind((ip,port))
server.listen()

clients=[]
nicknames=[]
print("Server has Started")

def clientthread(con,nickname):
    con.send("Welcome to ChatRoom".encode("utf-8"))
    while True:
        try:
            message=con.recv(2048).decode("utf-8")
            if message:
                print(message)
                broadcast(message,con)
            else:
                remove(con)
                removenickname(nickname)

        except:
            continue

def broadcast(message,con):
    for i in clients:
        if i !=con:
            try:
                i.send(message.encode("utf-8"))
            except:
                remove(i)

def remove(con):
    if con in clients:
        clients.remove(con)
def removenickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)

while True:
    con,adr=server.accept()
    con.send("NICKNAME".encode("utf-8"))
    nickname=con.recv(2048).decode("utf-8")
    nicknames.append(nickname)
    clients.append(con)

    message="{} joined!".format(nickname)
    print(message)
    broadcast(message,con)
    newthread=Thread(target=clientthread,args=(con,nickname))
    newthread.start()