from schedule import Schedule
from subject import Subject
import sys
from PyQt5 import QtWidgets
from ui import Ui_Form
from functools import partial
from itertools import product

class Main:
    def __init__(self):
        self.schedule_list = []
        self.subject_list = {}

    def demo(self):
        self.subject_list = {"AA": [], "BB": [], "CC": []}
        self.subject_list["AA"].append(Subject(1, "AA", 2, 1, 4, "Nguyễn Văn Bình"))
        self.subject_list["BB"].append(Subject(1, "BB", 3, 1, 2, "Nguyễn Văn Bình"))
        self.subject_list["CC"].append(Subject(1, "CC", 4, 6, 9, "Nguyễn Văn Bình"))

        self.subject_list["AA"].append(Subject(2, "AA", 3, 1, 4, "Nguyễn Văn Bình"))
        self.subject_list["BB"].append(Subject(2, "BB", 4, 3, 4, "Nguyễn Văn Bình"))
        self.subject_list["CC"].append(Subject(2, "CC", 5, 1, 4, "Nguyễn Văn Bình"))

    def buildSchedules(self):
        # self.schedule_list = []
        array_values = list(self.subject_list.values())
        # Sử dụng itertools.product để tạo ra tất cả các kết hợp
        all_combinations = list(product(*array_values))
        # In ra các bộ 3 phần tử từ mỗi khóa
        for combination in all_combinations:
            schedule = Schedule(True)
            isFeasible = True
            for subject in combination:
                if not schedule.addSubject(subject):
                    isFeasible = False
                    break
            if isFeasible: self.schedule_list.append((schedule, schedule.getSchedlePoint()))

    def printSchedles(self):
        print(f"> SCHEDULE RANK ==================================================")
        self.schedule_list = sorted(self.schedule_list, key=lambda x: x[1], reverse=True)
        for schedule, point in self.schedule_list[:15]:
            print(f"> POINT: {point} -----------------------------")
            schedule.printSchedule()

def setUpEvent(ui: Ui_Form, main: Main):
    ui.btnInsertSubject.clicked.connect(partial(addSubject, ui, main))# Kết nối sự kiện returnPressed của các QLineEdit với sự kiện clicked của btnInsertSubject
    ui.inputGroup.returnPressed.connect(ui.btnInsertSubject.click)
    ui.inputSubjectName.returnPressed.connect(ui.btnInsertSubject.click)
    ui.inputDay.returnPressed.connect(ui.btnInsertSubject.click)
    ui.inputPeriodFrom.returnPressed.connect(ui.btnInsertSubject.click)
    ui.inputPeriodTo.returnPressed.connect(ui.btnInsertSubject.click)
    ui.inputLecturer.returnPressed.connect(ui.btnInsertSubject.click)
    ui.btnPrintSchedules.clicked.connect(partial(printSchedules, main))

def addSubject(ui: Ui_Form, main: Main):
    subject = Subject(int(ui.inputGroup.text()), 
                      ui.inputSubjectName.text(), 
                      int(ui.inputDay.text()), 
                      int(ui.inputPeriodFrom.text()), 
                      int(ui.inputPeriodTo.text()), 
                      ui.inputLecturer.text())
    subject_name = ui.inputSubjectName.text()
    if subject_name not in main.subject_list:
        main.subject_list[subject_name] = []
    main.subject_list[subject_name].append(subject)
    print("Added Subject[" + subject.getSubject() + "] ")
    print("--------" + str(len(main.subject_list)))
def printSchedules(main: Main):
    main.buildSchedules()
    main.printSchedles()


if __name__ == "__main__":
    main = Main()
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()

    ui = Ui_Form()
    ui.setupUi(Form)
    setUpEvent(ui, main)

    Form.show()
    sys.exit(app.exec_())