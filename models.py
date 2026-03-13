class Entry:
    def __init__(self, service, login, password):
        self.service = service
        self.login = login
        self.password = password

    def to_dict(self):
        return {
            "service": self.service,
            "login": self.login,
            "password": self.password
        }

    @staticmethod
    def from_dict(data):
        return Entry(
            data["service"],
            data["login"],
            data["password"]
        )
