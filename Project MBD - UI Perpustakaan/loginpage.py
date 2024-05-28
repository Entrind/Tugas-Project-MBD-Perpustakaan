from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class LoginScreen(QWidget):
    def __init__(self, app_reference, parent=None):
        super(LoginScreen, self).__init__(parent)
        self.app_reference = app_reference
        self.init_ui()

    def init_ui(self):
        login_layout = QVBoxLayout(self)
        self.setLayout(login_layout)

        login_label = QLabel("LOGIN")
        login_label.setFont(QFont('Helvetica', 18))
        login_label.setAlignment(Qt.AlignCenter)
        login_layout.addWidget(login_label)

        login_input = QFont()
        login_input.setPointSize(12)

        username_label = QLabel('Username')
        username_label.setFont(QFont('Helvetica', 10))
        login_layout.addWidget(username_label)
        self.username_edit = QLineEdit()
        self.username_edit.setFont(login_input)
        login_layout.addWidget(self.username_edit)

        password_label = QLabel('Password')
        password_label.setFont(QFont('Helvetica', 10))
        login_layout.addWidget(password_label)
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)  # Hide password characters
        self.password_edit.setFont(login_input)
        login_layout.addWidget(self.password_edit)

        login_layout.addSpacerItem(QSpacerItem(0, 30, QSizePolicy.Ignored, QSizePolicy.Maximum))

        login_button = QPushButton('Login (Admin)')
        login_button.setFont(QFont('Helvetica', 8))
        login_button.clicked.connect(self.handle_login_admin)
        login_layout.addWidget(login_button)

        login_layout.addSpacerItem(QSpacerItem(0, 30, QSizePolicy.Ignored, QSizePolicy.Maximum))

        # Divider
        divider_layout = QHBoxLayout()  # Create a horizontal layout to hold the label and line
        login_layout.addLayout(divider_layout)

        divider_line = QFrame()
        divider_line.setFrameShape(QFrame.HLine)
        divider_line.setFrameShadow(QFrame.Sunken)
        divider_line.setStyleSheet("background-color: #9fa5b1;")  # Set black background color
        divider_line.setLineWidth(2)  # Increase line width to make it more apparent
        divider_layout.addWidget(divider_line)

        divider_label = QLabel("OR")
        divider_label.setFont(QFont('Helvetica', 8))
        divider_label.setAlignment(Qt.AlignCenter)
        divider_layout.addWidget(divider_label)

        divider_line = QFrame()
        divider_line.setFrameShape(QFrame.HLine)
        divider_line.setFrameShadow(QFrame.Sunken)
        divider_line.setStyleSheet("background-color: #9fa5b1;")  # Set black background color
        divider_line.setLineWidth(2)  # Increase line width to make it more apparent
        divider_layout.addWidget(divider_line)

        login_layout.addSpacerItem(QSpacerItem(0, 30, QSizePolicy.Ignored, QSizePolicy.Maximum))

        guest_button = QPushButton('Continue as Guest')
        guest_button.setFont(QFont('Helvetica', 8))
        guest_button.clicked.connect(self.handle_guest_login)
        login_layout.addWidget(guest_button)

    def handle_login_admin(self):
        self.app_reference.handle_login_admin()

    def handle_guest_login(self):
        self.app_reference.handle_guest_login()
