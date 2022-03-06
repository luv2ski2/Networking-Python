import socket
import threading

HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!disconnect"

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())  # 192.168.4.113
ADDR = SERVER, PORT

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(ADDR)

def handleClient(conn, addr):
    print(f"[NEW CONNECTION] {addr} has connected.")

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

def start():
    s.listen()
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handleClient, args=(conn, addr))
        thread.start()
        print(f"\nACTIVE CONNECTIONS: {threading.activeCount() - 1}\n")

print(f"Starting server on host: {SERVER}, port {PORT}")
start()