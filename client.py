import socket

HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!disconnect"

PORT = 5050
# SERVER = input("What host?\n")
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = SERVER, PORT

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    messageLen = len(message)
    sendLen = str(messageLen).encode(FORMAT)
    sendLen += b' ' * (HEADER - len(sendLen))
    s.send(sendLen)
    s.send(message)
    print(s.recv(2048).decode(FORMAT))

send("Hello")
send("Hello, gamer")
send("hi Ian")
send(DISCONNECT_MESSAGE)