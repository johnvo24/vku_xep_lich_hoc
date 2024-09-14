

class Subject:
    def __init__(self, group, name, day, time_from, time_to, lecturer):
        self.name = name
        self.group = group
        self.day = day
        self.period = range(time_from, time_to + 1)
        self.lecturer = lecturer

    def getSubject(self):
        return f"   Thứ {self.day} ({self.period[0]}->{self.period[-1]}) - {self.name} ({self.group}) - {self.lecturer}"