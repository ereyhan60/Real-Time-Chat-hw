import socket
import threading
import pickle
from user import User
from message import Message
from group import GroupManager
from datetime import datetime

class MessagingServer:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.users = {}
        self.messages = []
        self.group_manager = GroupManager()

    def start_server(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection from {client_address}")
            threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()

    def handle_client(self, client_socket, client_address):
        try:
            username = client_socket.recv(1024).decode('utf-8')
            self.users[username] = User(username, client_socket)
            self.send_past_messages(client_socket, username)
    
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                message = pickle.loads(data)
                if isinstance(message, Message):
                    self.messages.append(message)
                    self.route_message(message)
                elif isinstance(message, dict):
                    if 'command' in message:
                        if message['command'] == 'search':
                            self.handle_search(client_socket, username, message['keyword'])
                        elif message['command'] == 'group':
                            self.handle_group_command(message)
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
        finally:
            client_socket.close()
            if username in self.users:
                del self.users[username]
            print(f"Connection closed from {client_address}")

    def handle_group_command(self, message):
        action = message['action']
        group_name = message['group_name']
        username = message['username']
    
        if action == 'create':
            self.group_manager.create_group(group_name)
        elif action == 'add' and username:
            self.group_manager.add_user_to_group(group_name, username)
        elif action == 'remove' and username:
            self.group_manager.remove_user_from_group(group_name, username)

    def route_message(self, message):
        if message.receiver in self.users:
            self.users[message.receiver].socket.send(pickle.dumps(message))
        elif message.receiver in self.group_manager.groups:
            for user in self.group_manager.get_users_in_group(message.receiver):
                if user in self.users and user != message.sender:
                    self.users[user].socket.send(pickle.dumps(message))
    

    def send_past_messages(self, client_socket, username):
        user_messages = [msg for msg in self.messages if msg.sender == username or msg.receiver == username or (msg.receiver in self.group_manager.groups and username in self.group_manager.get_users_in_group(msg.receiver))]
        client_socket.send(pickle.dumps(user_messages))

    def handle_search(self, client_socket, username, keyword):
        search_results = [msg for msg in self.messages if (msg.sender == username or msg.receiver == username or (msg.receiver in self.group_manager.groups and username in self.group_manager.get_users_in_group(msg.receiver))) and keyword in msg.content]
        client_socket.send(pickle.dumps(search_results))

if __name__ == "__main__":
    server = MessagingServer()
    server.start_server()
