import sys
import threading
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import request_generator
import database as db

# HHMM   HHMM
# 0000   0000

db.database, db.cur = db.ConnectDatabase()

class level2_window(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.sign_in_win = sign_in_window()
        self.approved_win = approved_window()
        self.username = ""
        self.auth = True
        self.approved_list = [["Token", "Room", "Reason"]]
        self.room_type = ""

        self.err_box = QMessageBox()
        self.err_box.setWindowTitle("Error")
        self.err_box.setText("No room available with the given description!")
        
        self.create_actions()
        self.setWindowTitle("RAD-MaS")
        self.setGeometry(100, 100, 600, 400)
        self.sign_in = False
        self.menu = self.menuBar()

        self.menu_file = self.menu.addMenu('File')
        self.menu_file.addAction(self.sign_in_action)

        self.menu_approved = self.menu.addMenu('Approved')
        self.menu_approved.addAction(self.approved_action)

        self.gen_req_button = QPushButton("Generate new Request", self)
        self.gen_req_button.clicked.connect(self.gen_req_button_action)
        self.gen_req_button.setGeometry(0, 30, 200, 40)

        self.username_label = QLabel("Please Sign-In", self)
        self.username_label.setGeometry(500, 30, 100, 20)

        self.token_no = QLabel("Token No.: ", self)
        self.token_no.setGeometry(20, 100, 75, 20)
        self.token_no_textbox = QLineEdit("", self)
        self.token_no_textbox.setGeometry(100, 100, 200, 20)

        self.choose_label = QLabel("Choose Any One Type: ", self)
        self.choose_label.setGeometry(400, 80, 150, 20)

        self.classroom_checkbox1 = QRadioButton("Classroom", self)
        self.classroom_checkbox1.setGeometry(450, 100, 100, 20)
        self.classroom_checkbox1.clicked.connect(self.classroom_checkbox1_action)

        self.classroom_checkbox2 = QRadioButton("Seminar Hall", self)
        self.classroom_checkbox2.setGeometry(450, 130, 100, 20)
        self.classroom_checkbox2.clicked.connect(self.classroom_checkbox2_action)

        self.classroom_checkbox3 = QRadioButton("Lab", self)
        self.classroom_checkbox3.setGeometry(450, 160, 100, 20)
        self.classroom_checkbox3.clicked.connect(self.classroom_checkbox3_action)

        self.building_no_label = QLabel("Building Number: ", self)
        self.building_no_label.setGeometry(80, 190, 100, 20)

        self.building_no_textbox = QLineEdit("1", self)
        self.building_no_textbox.setGeometry(190, 190, 60, 20)

        self.time_label = QLabel("Time (24hr): ", self)
        self.time_label.setGeometry(270, 190, 80, 20)

        self.time_textbox = QLineEdit("0000", self)
        self.time_textbox.setGeometry(350, 190, 60, 20)

        self.duration_label = QLabel("Duration:", self)
        self.duration_label.setGeometry(430, 190, 80, 20)

        self.duration_textbox = QLineEdit("0000", self)
        self.duration_textbox.setGeometry(490, 190, 40, 20)

        self.reason_label = QLabel("Reason for allotment: ", self)
        self.reason_label.setGeometry(120, 220, 200, 20)

        self.reason_text = QTextEdit("", self)
        self.reason_text.setGeometry(120, 250, 320, 100)

        self.send_req_button = QPushButton("Send Request", self)
        self.send_req_button.setGeometry(0, 130, 100, 40)
        self.send_req_button.clicked.connect(self.send_req_button_action)

        self.dealloc_req_button = QPushButton("Deallocate Token", self)
        self.dealloc_req_button.setGeometry(130, 130, 140, 40)
        self.dealloc_req_button.clicked.connect(self.dealloc_req_button_action)

        self.show()

    def dealloc_req_button_action(self, click):
        if self.token_no_textbox.text() != "":
            db.Deallocate(TokenID=self.token_no_textbox.text())
            i = 0
            for val in self.approved_list:
                if self.token_no_textbox.text() in val:
                    self.approved_list.pop(i)
                i+=1

    def send_req_button_action(self, click):
        if self.sign_in:
            room = db.BookRoom(TokenNo=self.token_no_textbox.text(), Building=self.building_no_textbox.text(), RoomType=self.room_type, StartTime=self.time_textbox.text(), Duration=self.duration_textbox.text(), Reason=self.reason_text.toPlainText())
            if room != -1:
                self.approved_list.append([self.token_no_textbox.text(), room, self.reason_text.toPlainText()])
                self.err_box.setWindowTitle("Success")
                self.err_box.setText(f"Room {room} has been alloted for {self.token_no_textbox.text()}!")
                self.err_box.exec_()
            else:
                self.err_box.setWindowTitle("Error")
                self.err_box.setText("No room available with the given description!")
                self.err_box.exec_()
            print(room)
            db.CommitDatabase()
            self.token_no_textbox.setText("")
            self.time_textbox.setText("0000")
            self.duration_textbox.setText("0000")
            self.classroom_checkbox1.setChecked(False)
            self.classroom_checkbox2.setChecked(False)
            self.classroom_checkbox3.setChecked(False)
        else:
            print("Sign In")

    def gen_req_button_action(self, click):
        self.token_no_textbox.setText(request_generator.GenerateID())

    def classroom_checkbox1_action(self):
        self.room_type = "Classroom"

    def classroom_checkbox2_action(self):
        self.room_type = "Seminar Hall"

    def classroom_checkbox3_action(self):
        self.room_type = "Lab"

    def create_actions(self):
        self.sign_in_action = QAction('Sign In', self)
        self.sign_in_action.triggered.connect(self.sign_in)

        self.approved_action = QAction('Approved Requests', self)
        self.approved_action.triggered.connect(self.approved)
        

    def authenticator(self):
        self.thr1 = threading.Thread(target=self.check_sign_in)
        self.thr1.start()

    def stop_autheticator(self):
        self.auth = False
        self.thr1.join()

    def check_sign_in(self):
        while self.auth:
            if self.sign_in_win.signed_in:
                self.sign_in = self.sign_in_win.signed_in
                self.username = self.sign_in_win.username_textbox.text()
                self.username_label.setText(self.username)
                print(self.username)
                self.sign_in_win.signed_in = False
                break

    def sign_in(self):
        self.authenticator()
        self.sign_in_win.show()

    def approved(self):
        self.approved_win.create_table(self.approved_list)
        self.approved_win.show()

class approved_tabel_model(QAbstractTableModel):
    def __init__(self, data):
        super(approved_tabel_model, self).__init__()
        self.approved_list = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.approved_list[index.row()][index.column()]

    def rowCount(self, index):
        return len(self.approved_list)

    def columnCount(self, index):
        return len(self.approved_list[0])


class approved_window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Approved Rooms")
        self.setGeometry(100, 100, 650, 400)

        self.approved_tab = QTableView(self)
        self.approved_tab.setGeometry(0, 0, 650, 400)

    def create_table(self, data):
        self.model = approved_tabel_model(data)
        self.approved_tab.setModel(self.model)
        


class sign_in_window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign In")
        self.setGeometry(100, 100, 300, 150)
        self.signed_in = False
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.username_label = QLabel("Username", self)
        self.grid.addWidget(self.username_label, 0, 0)
        self.username_textbox = QLineEdit("username", self)
        self.grid.addWidget(self.username_textbox, 0, 1)
        self.password_label = QLabel("Password", self)
        self.grid.addWidget(self.password_label, 1, 0)
        self.password_textbox = QLineEdit("password", self)
        self.grid.addWidget(self.password_textbox, 1, 1)
        self.sign_in_button = QPushButton("Sign In", self)
        self.sign_in_button.clicked.connect(self.sign_in_button_action)
        self.grid.addWidget(self.sign_in_button, 2, 1)

    def sign_in_button_action(self, click):
        self.signed_in = True
        self.close()


if __name__ == '__main__':
    db.MakeTables()
    db.InitDatabase(4, 4, 4)
    db.CommitDatabase()
    main_app = QApplication(sys.argv)
    window = level2_window()
    #window.stop_autheticator()
    sys.exit(main_app.exec_())