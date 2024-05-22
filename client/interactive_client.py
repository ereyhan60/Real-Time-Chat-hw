import socket
import threading
import pickle
from datetime import datetime
import shlex
from cmd import Cmd
from message import Message
from connection_list import ConnectionList
from group import GroupManager

class MessagingClient(Cmd):
    prompt = '> '
    intro = "Welcome to the Messaging Client. Type help or ? to list commands.\n"

    def __init__(self, host='localhost', port=5000):
        super().__init__()
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = input("Enter your username: ")
        self.connection_list = ConnectionList()
        self.group_manager = GroupManager()
        self.client_socket.connect((self.host, self.port))
        self.client_socket.send(self.username.encode('utf-8'))
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                message_data = self.client_socket.recv(4096)
                if not message_data:
                    break
                message = pickle.loads(message_data)
                if isinstance(message, list):
                    print("Past messages:")
                    for msg in message:
                        print(msg)
                else:
                    print(message)
            except:
                break

    def send_message(self, content, receiver):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = Message(self.username, content, timestamp, receiver)
        self.client_socket.send(pickle.dumps(message))

    def search_messages(self, keyword):
        search_request = {'command': 'search', 'keyword': keyword}
        self.client_socket.send(pickle.dumps(search_request))

    def do_message(self, args):
        args = shlex.split(args)
        if len(args) >= 2:
            receiver = args[0]
            content = ' '.join(args[1:])
            self.send_message(content, receiver)

    def do_search(self, args):
        args = shlex.split(args)
        if args:
            keyword = args[0]
            self.search_messages(keyword)

    def do_group(self, args):
        args = shlex.split(args)
        if len(args) >= 2:
            command = args[0]
            group_name = args[1]
            username = args[2] if len(args) > 2 else None
    
            group_command = {
                'command': 'group',
                'action': command,
                'group_name': group_name,
                'username': username
            }
            self.client_socket.send(pickle.dumps(group_command))


    def do_exit(self, args):
        print("Exiting...")
        return True

if __name__ == "__main__":
    client = MessagingClient()
    client.cmdloop()
