class GroupManager:
    def __init__(self):
        self.groups = {}

    def create_group(self, group_name):
        if group_name not in self.groups:
            self.groups[group_name] = []

    def add_user_to_group(self, group_name, username):
        if group_name in self.groups and username not in self.groups[group_name]:
            self.groups[group_name].append(username)

    def remove_user_from_group(self, group_name, username):
        if group_name in self.groups and username in self.groups[group_name]:
            self.groups[group_name].remove(username)

    def get_users_in_group(self, group_name):
        return self.groups.get(group_name, [])
