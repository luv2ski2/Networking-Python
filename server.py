import socket
import threading

HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!disconnect"

PORT = 5050
SERVER = "127.0.0.1"# socket.gethostbyname(socket.gethostname())  # 192.168.4.113
ADDR = SERVER, PORT

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# s.bind(ADDR)

def handleClient(conn, addr):
    # print(f"[NEW CONNECTION] {addr} has connected.")
    sendThread = threading.Thread(target=handleSend, args=(conn,))
    sendThread.start()

    connected = True
    while connected:
        msgLen = conn.recv(HEADER).decode(FORMAT)
        if msgLen:
            msgLen = int(msgLen)
            msg = conn.recv(msgLen).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"{msg} from {addr}\n")
            conn.send("Message received".encode(FORMAT))

    conn.close()
    sendThread.join()

def handleSend(conn):
    while True:
        sendMsg = input()
        send(sendMsg, conn)
        if sendMsg == DISCONNECT_MESSAGE:
            break

def handleConnection(conn):
    sendThread = threading.Thread(target=handleSend, args=(conn,))
    sendThread.start()

    connected = True
    while connected:
        msgLen = conn.recv(HEADER).decode(FORMAT)
        if msgLen:
            msgLen = int(msgLen)
            msg = conn.recv(msgLen).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"{msg}\n")
            # conn.send("Message received".encode(FORMAT))

    conn.close()
    sendThread.join()

def send(msg, conn):
    message = msg.encode(FORMAT)
    messageLen = len(message)
    sendLen = str(messageLen).encode(FORMAT)
    sendLen += b' ' * (HEADER - len(sendLen))
    conn.send(sendLen)
    conn.send(message)
    # print(s.recv(2048).decode(FORMAT))

def connect():
    connecter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv = input("Who do you want to connect with?\n")
    port = int(input("What port do you want to connect to?"))
    addr = serv, port
    print(addr)
    connecter.connect(addr)
    thread = threading.Thread(target=handleConnection, args=(connecter,))
    thread.start()

# Listening
def start(server, port):
    addr = server, port
    s.bind(addr)
    print(f"[Starting on {port} {server}")
    s.listen()
    print("[Listening]")
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handleConnection, args=(conn,))
        # Open connection
        thread.start()
        print(f"\nACTIVE CONNECTIONS: {threading.activeCount() - 1}\n")

def startCommands():
    answr = input("What do you want to do?\n1. Connect to another system")
    if answr == "1":
        connect()

# print(f"Starting server on host: {SERVER}, port {PORT}")
# SERVER = input("What server do you want to run on?\n")
PORT = int(input("What port do you want to run on?\n"))
# start()
threadStart = threading.Thread(target=start, args=(SERVER, PORT))
threadStart.start()
startCommands()