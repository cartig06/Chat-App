import socket, threading

HOST = input("enter tunnel address: ")
try:
    PORT = int(input("tunnel port: "))
except:
    print("invalid port... exiting")
    exit()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

username = input("Enter your username: ")

sock.sendall(username.encode())

def receive_messages():
    while True:
        message = sock.recv(1024).decode()
        print(message)

thread = threading.Thread(target=receive_messages)
thread.start()

while True:
    message = input()
    sock.sendall(message.encode())