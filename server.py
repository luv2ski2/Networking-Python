import socket
import threading

HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!disconnect"

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())  # 192.168.4.113
ADDR = SERVER, PORT

# all active connections
connections = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# s.bind(ADDR)

# def handleClient(conn, addr):
#     # print(f"[NEW CONNECTION] {addr} has connected.")
#     sendThread = threading.Thread(target=handleSend, args=(conn,))
#     sendThread.start()
#
#     connected = True
#     while connected:
#         msgLen = conn.recv(HEADER).decode(FORMAT)
#         if msgLen:
#             msgLen = int(msgLen)
#             msg = conn.recv(msgLen).decode(FORMAT)
#             if msg == DISCONNECT_MESSAGE:
#                 connected = False
#
#             print(f"{msg} from {addr}\n")
#             conn.send("Message received".encode(FORMAT))
#
#     conn.close()
#     sendThread.join()

def handleSend(conn):
    while True:
        sendMsg = input(">")
        send(sendMsg, conn)
        if sendMsg == DISCONNECT_MESSAGE:
            break

def handleConnection(conn: socket.socket):
    # sendThread = threading.Thread(target=handleSend, args=(conn,))
    # sendThread.start()
    connections.append(conn)

    connected = True
    while connected:
        msgLen = conn.recv(HEADER).decode(FORMAT)
        if msgLen:
            msgLen = int(msgLen)
            msg = conn.recv(msgLen).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"{conn.getsockname()}> {msg}\n")
            # conn.send("Message received".encode(FORMAT))

    conn.close()
    # sendThread.join()

def send(msg: str, conn: socket.socket):
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
    port = int(input("What port do you want to connect to?\n"))
    addr = serv, port
    print(addr)
    connecter.connect(addr)
    thread = threading.Thread(target=handleConnection, args=(connecter,))
    thread.start()

# Listening
def start(server: str, port: int):
    addr = server, port
    s.bind(addr)
    print(s.getsockname())
    print(f"[Starting] on {port} {server}\n")
    s.listen()
    print("[Listening]\n")
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handleConnection, args=(conn,))
        # Open connection
        thread.start()
        print(f"[NEW CONNECTION] from {addr}\n")

def startCommands():
    global connections
    print("What do you want to do? Type help for a list of commands")
    while True:
        answr = input()
        if answr[0:4] == "send":
            toSend = answr[4:]
            for conn in connections:
                send(toSend, conn)
            if toSend == DISCONNECT_MESSAGE:
                for conn in connections:
                    conn.close()
                connections = []
                break

        if answr == "connect":
            connect()

        if answr == "help":
            print("Commands:\nsend [message]: sends a message\nconnect: connects you to another system")


# print(f"Starting server on host: {SERVER}, port {PORT}")
SERVER = input("What server do you want to run on?\n")
PORT = int(input("What port do you want to run on?\n"))
# start()
threadStart = threading.Thread(target=start, args=(SERVER, PORT))
threadStart.start()
startCommands()