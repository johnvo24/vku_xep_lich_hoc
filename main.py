from schedule import Schedule
from subject import Subject
import sys
from PyQt5 import QtWidgets
from ui import Ui_Form
from functools import partial
from itertools import product
import pandas as pd

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
        # Sử dụng itertools.product trực tiếp thay vì list() để tiết kiệm bộ nhớ
        all_combinations = product(*self.subject_list.values())
        for combination in all_combinations:
            schedule = Schedule(True)  # Khởi tạo lịch mới cho mỗi tổ hợp
            isFeasible = True  # Biến kiểm tra tính khả thi của lịch học

            # Kiểm tra tính khả thi của mỗi môn học trong tổ hợp
            for subject in combination:
                if not schedule.addSubject(subject):  # Nếu không thể thêm môn học
                    isFeasible = False  # Đánh dấu là không khả thi
                    break  # Dừng kiểm tra các môn học còn lại
            # Nếu tất cả các môn học trong tổ hợp có thể thêm được vào lịch học, thêm vào danh sách
            if isFeasible:
                self.schedule_list.append((schedule, schedule.getSchedlePoint()))

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
    if (not ui.inputDay.text()
        or not ui.inputSubjectName.text() 
        or not ui.inputDay.text()
        or not ui.inputPeriodFrom.text() 
        or not ui.inputPeriodTo.text() 
        or not ui.inputLecturer.text()):
        if (not ui.inputDay.text()
            and not ui.inputSubjectName.text() 
            and not ui.inputDay.text()
            and not ui.inputPeriodFrom.text() 
            and not ui.inputPeriodTo.text() 
            and not ui.inputLecturer.text()):
                addSubjectFromCSV(main)
        else:
            print(f"[JV] No change")
            return
    else:
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
def addSubjectFromCSV(main: Main, csv_file: str='data.csv'):
    try:
        data = pd.read_csv(csv_file)
    except Exception as e:
        print(f"[JV] ERROR")
        return            
    for _, row in data.iterrows():
        try:
            subject = Subject(
                int(row['Group']),
                row['SubjectName'],
                int(row['Day']),
                int(row['PeriodFrom']),
                int(row['PeriodTo']),
                row['Lecturer']
            )
            subject_name = row['SubjectName']
            if subject_name not in main.subject_list:
                main.subject_list[subject_name] = []
            main.subject_list[subject_name].append(subject)
            print(f"Added Subject[{subject.getSubject()}]")
        except Exception as e:
            print(f"Error adding subject from row {row}: {e}")

    # print(main.subject_list)
    print(f"Total subjects added: {len(main.subject_list)}")

def printSchedules(main: Main):
    main.buildSchedules()
    main.printSchedles()

if __name__ == "__main__":
    main = Main()
    # app = QtWidgets.QApplication(sys.argv)
    # Form = QtWidgets.QWidget()

    # ui = Ui_Form()
    # ui.setupUi(Form)
    # setUpEvent(ui, main)

    # Form.show()
    # sys.exit(app.exec_())

    ## No UI
    while True:
        print("MENU")
        print("1. Add subjects from data.csv")
        print("2. Print Schedules")
        print("3. Quit")
        choice = input("Your choice: ")
        
        if choice == "1":
            print(f"You chosen {choice}")
            addSubjectFromCSV(main)
        if choice == "2":
            print(f"You chosen {choice}")
            main.buildSchedules()
            main.printSchedles()
        if choice == "3":
            break
        else:
            continue