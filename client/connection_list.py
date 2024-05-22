class ConnectionList:
    def __init__(self):
        self.connections = {}

    def add_connection(self, username, socket):
        self.connections[username] = socket

    def remove_connection(self, username):
        if username in self.connections:
            del self.connections[username]

    def get_connection(self, username):
        return self.connections.get(username)

    def list_connections(self):
        return list(self.connections.keys())
