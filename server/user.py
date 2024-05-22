class User:
    def __init__(self, username, socket):
        self.username = username
        self.socket = socket
        self.groups = []

    def add_to_group(self, group_name):
        self.groups.append(group_name)

    def remove_from_group(self, group_name):
        self.groups.remove(group_name)
