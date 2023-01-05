import threading
import socket
from pyngrok import ngrok

with open("authtoken.txt", "r") as f:
	authtoken = f.readline()
ngrok.set_auth_token(authtoken)

class Client:
	def __init__(self, sock, addr):
		self.sock = sock
		self.addr = addr
		self.username = None

class App:
	def __init__(self):
		self.clients = []
		self.messages = []

	def broadcast(self, message):
		for client in self.clients:
			client.sock.sendall(message.encode())

	def add_client(self, client):
		self.clients.append(client)
		self.broadcast(f"{client.username} has joined!")

	def remove(self, client):
		self.clients.remove(client)
		print(f"{client.username} has left the chatroom")
		self.broadcast(f"{client.username} has left the chatroom")


def handle_client(client, chat_room):
	while True:
		message = client.sock.recv(1024).decode()

		if not client.username:
			client.username = message
			chat_room.add_client(client)
			continue

		if not message:
			chat_room.remove(client)
			break

		chat_room.broadcast(f"{client.username}: {message}")

chat_room = App()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 8000))
server.listen()
public_url = ngrok.connect(8000, "tcp")
print(f" * server forwarded to ngrok at \"{public_url}\" : bound to localhost:8000 *")

while True:
	sock, addr = server.accept()
	client = Client(sock, addr)
	thread = threading.Thread(target=handle_client, args=(client, chat_room))
	thread.start()