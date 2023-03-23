class Course:
    def __init__(self, name: str):
        self.name = name

    def rename(self, name: str):
        self.name = name
        return self

    def __str__(self):
        return self.name

    def to_dict(self):
        return {"name": self.name}

    @staticmethod
    def from_dict(data):
        return Course(data["name"])
