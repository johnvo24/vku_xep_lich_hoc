from subject import Subject

class Schedule:
    def __init__(self, morning):
        self.table = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],]
        self.subjects = []
        self.morning_point = 2 if morning == True else 0.5

    def getSchedlePoint(self):
        point = 0
        for i in range(2, 8):
            for j in range(1, 10):
                if self.table[i-2][j-1] != 0:
                    if j <= 5:
                        point += 2
                    else:
                        point += 1
        return point
                
    def addSubject(self, subject: Subject):
        self.subjects.append(subject)
        self.subjects = sorted(self.subjects, key=lambda x: (x.day, x.period[0]))
        for i in subject.period:
            if self.table[subject.day - 2][i-1] == 1:
                return False
            self.table[subject.day - 2][i-1] = 1
        return True
    
    def printSchedule(self):
        for subject in self.subjects:
            print(subject.getSubject())