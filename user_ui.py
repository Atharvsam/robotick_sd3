import sys
from typing import Text
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class level2_window(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.create_actions()
        self.setWindowTitle("Find Class")
        self.setGeometry(100, 100, 300, 300)
        self.menu = self.menuBar()
        #self.setMenuBar(self.menu)
        self.menu_file = self.menu.addMenu('File')
        self.menu_file.addAction(self.sign_in_action)
        self.show()

    def create_actions(self):

        self.sign_in_action = QAction('Sign In', self)
        self.sign_in_action.triggered.connect(self.hello)

    def hello(self):
        self.new_window = sign_in_window()
        self.new_window.show()
        #sign_in_w = QApplication(sys.argv)
        #new_window.exec_()


class sign_in_window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign In")
        self.setGeometry(100, 50, 400, 200)
        self.username_textbox = QLabel("Username", self)
        self.username_textbox.setGeometry(100, 100, 200, 50)
        self.password_textbox = QLabel("Password", self)



if __name__ == '__main__':
    main_app = QApplication(sys.argv)
    window = level2_window()
    sys.exit(main_app.exec_())