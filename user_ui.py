import sys
import threading
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import random

class level2_window(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.sign_in_win = sign_in_window()
        self.username = ""
        self.auth = True
        self.approved_list = []
        
        self.create_actions()
        self.setWindowTitle("Find Class")
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

        self.classroom_checkbox = QCheckBox("Classroom", self)
        self.classroom_checkbox.setGeometry(450, 100, 100, 20)

        self.classroom_checkbox = QCheckBox("Seminar Hall", self)
        self.classroom_checkbox.setGeometry(450, 130, 100, 20)

        self.classroom_checkbox = QCheckBox("Lab", self)
        self.classroom_checkbox.setGeometry(450, 160, 100, 20)

        self.time_label = QLabel("Time (24hr): ", self)
        self.time_label.setGeometry(350, 190, 80, 20)

        self.time_textbox = QLineEdit("0000", self)
        self.time_textbox.setGeometry(450, 190, 100, 20)

        self.reason_label = QLabel("Reason for allotment: ", self)
        self.reason_label.setGeometry(300, 220, 200, 20)

        self.reason_text = QTextEdit("", self)
        self.reason_text.setGeometry(300, 250, 280, 100)

        self.send_req_button = QPushButton("Send Request", self)
        self.send_req_button.setGeometry(0, 130, 100, 40)
        self.send_req_button.clicked.connect(self.send_req_button_action)

        self.show()

    def random_token(self):
        return random.random(100, 200)

    def send_req_button_action(self, click):
        pass

    def gen_req_button_action(self, click):
        pass

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
        pass


class approved_window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Approved Rooms")
        self.setGeometry(100, 100, 300, 150)
        
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        
        self.approved_list = QLabel("Approved Requests: ", self)
        self.grid.addWidget(self.approved_list, 0, 0)

        self.approved_list = QComboBox(self)
        self.grid.addWidget(self.approved_list, 0, 1)


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
    main_app = QApplication(sys.argv)
    window = level2_window()
    #window.stop_autheticator()
    sys.exit(main_app.exec_())