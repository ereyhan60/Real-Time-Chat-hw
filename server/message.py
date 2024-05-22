class Message:
    def __init__(self, sender, content, timestamp, receiver='all'):
        self.sender = sender
        self.content = content
        self.timestamp = timestamp
        self.receiver = receiver

    def __repr__(self):
        return f"[{self.timestamp}] {self.sender} to {self.receiver}: {self.content}"
