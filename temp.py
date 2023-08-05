
def write():
    while True:
        message="{}: {}".format(nickname,input(""))
        client.send(message.encode("utf-8"))

recieveThread=Thread(target=recieve)
recieveThread.start()
writeThread=Thread(target=write)
writeThread.start()