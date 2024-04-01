import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QStackedWidget, QListWidget, QApplication, QSizePolicy, QGroupBox, QTableView
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQueryModel
import PyQt5.QtGui as qtg
import pymysql  # Install pymysql library (pip install pymysql)

# Database connection details (replace with your credentials)
HOST = '127.0.0.1'
USER = 'root'
PASSWORD = 'anD1ka02_r4hman'
DATABASE = 'Perpustakaan'


class LibraryApp(QWidget):

    def __init__(self):
        super().__init__()

        self.db = self.connect_to_database()  # Connect to database
        self.current_user = None  # Stores currently logged-in user

        self.init_ui()

    def connect_to_database(self):
        try:
            conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
            return conn
        except pymysql.Error as e:
            print(f"Database connection error: {e}")
            sys.exit(1)

    def init_ui(self):
        self.setWindowTitle('Library Management')

        # Stacked widget for switching between login and main app screens
        self.stacked_widget = QStackedWidget()
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.stacked_widget)

        # Login screen
        self.login_screen = self.create_login_screen()
        self.stacked_widget.addWidget(self.login_screen)

        # Main app screen (initially hidden)
        self.main_screens = {
            'admin': self.create_main_screen(admin=True),
            'guest': self.create_main_screen(admin=False)
        }
        self.stacked_widget.addWidget(self.main_screens['guest'])
        self.stacked_widget.addWidget(self.main_screens['admin'])

        self.stacked_widget.setCurrentIndex(0)  # Show login screen first

        self.show()

    def create_login_screen(self):
        login_screen = QWidget()
        login_layout = QVBoxLayout()
        login_screen.setLayout(login_layout)

        username_label = QLabel('Username:')
        login_layout.addWidget(username_label)
        self.username_edit = QLineEdit()
        login_layout.addWidget(self.username_edit)

        password_label = QLabel('Password:')
        login_layout.addWidget(password_label)
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)  # Hide password characters
        login_layout.addWidget(self.password_edit)

        login_button = QPushButton('Login (Admin)')
        login_button.clicked.connect(self.handle_login_admin)
        login_layout.addWidget(login_button)

        guest_button = QPushButton('Continue as Guest')
        guest_button.clicked.connect(self.handle_guest_login)
        login_layout.addWidget(guest_button)

        return login_screen

    def create_title_groupbox(self):
        title_groupbox = QGroupBox()
        title_groupbox.setStyleSheet("QGroupBox { background-color: #E0E0E0; border: 2px solid #808080; }")
        title_layout = QVBoxLayout()
        title_groupbox.setLayout(title_layout)

        message_label = QLabel("Sistem Manajemen Perpustakaan")
        message_label.setFont(QFont('Helvetica', 24))
        message_label.setAlignment(Qt.AlignCenter)  # Align center for title appearance
        title_layout.addWidget(message_label)

        return title_groupbox

    # Main Window (Pencarian Buku)
    def create_main_screen(self, admin=False):
        main_screen = QWidget()
        main_layout = QVBoxLayout()
        main_screen.setLayout(main_layout)

        # App Title
        title_groupbox = self.create_title_groupbox()
        main_layout.addWidget(title_groupbox)

        # Define content_area
        content_area = QVBoxLayout()

        if admin:
            # Admin Main Screen
            admin_layout = QHBoxLayout()
            main_layout.addLayout(admin_layout)

            # Sidebar
            sidebar = self.create_sidebar()
            sidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            admin_layout.addWidget(sidebar)

            # Main content area
            content_area = QVBoxLayout()  # Create content_area layout
            admin_layout.addLayout(content_area)

            # Message above search bar (stick to the right of the sidebar)
            message_label = QLabel("Pencarian Buku Perpustakaan")
            message_label.setFont(qtg.QFont('Helvetica', 18))
            message_label.setAlignment(Qt.AlignLeft)
            content_area.addWidget(message_label)

            # Message above search bar
            message_label = QLabel("Ketiklah Judul Buku atau Nama penulis dari Buku")
            message_label.setAlignment(Qt.AlignCenter)
            content_area.addWidget(message_label)

            # Search bar
            search_layout = QHBoxLayout()
            search_input = QLineEdit()
            search_button = QPushButton("Search")
            search_layout.addWidget(search_input)
            search_layout.addWidget(search_button)

            table_view = QTableView()
            model = QSqlQueryModel()
            model.setQuery("SELECT * FROM Buku")  # Assuming there's a table named Books in your database
            table_view.setModel(model)

            content_area.addLayout(search_layout)
            content_area.addWidget(table_view)

            # Add and delete buttons (just placeholders, you need to implement their functionalities)
            add_button = QPushButton("Add Book")
            delete_button = QPushButton("Delete Book")
            content_area.addWidget(add_button)
            content_area.addWidget(delete_button)

            content_area.addStretch(1)  # Add stretchable space below the search bar

        else:
            # Message above search bar
            message_label = QLabel("Pencarian Buku Perpustakaan")
            message_label.setFont(qtg.QFont('Helvetica', 18))
            message_label.setAlignment(Qt.AlignTop)  # Align the message label to the top
            main_layout.addWidget(message_label)

            # Message below search bar
            message_label = QLabel("Ketiklah Judul Buku atau Nama penulis dari Buku")
            message_label.setAlignment(Qt.AlignTop)
            main_layout.addWidget(message_label)

            # Search bar
            search_layout = QHBoxLayout()
            search_input = QLineEdit()
            search_button = QPushButton("Search")
            search_layout.addWidget(search_input)
            search_layout.addWidget(search_button)

            table_view = QTableView()
            model = QSqlQueryModel()
            model.setQuery("SELECT * FROM Buku")  # Assuming there's a table named Books in your database
            table_view.setModel(model)

            main_layout.addLayout(search_layout)
            main_layout.addWidget(table_view)

            main_layout.addStretch(1)  # Add stretchable space below the search bar

        main_layout.addLayout(content_area)

        return main_screen

    def Peminjaman_Buku(self):
        # Placeholder function for handling the "Peminjaman Buku" section
        pass

    def Pengembalian_Buku(self):
        # Placeholder function for handling the "Pengembalian Buku" section
        pass

    def Anggota_Perpustakaan(self):
        # Placeholder function for handling the "Anggota Perpustakaan" section
        pass

    def Petugas_Perpustakaan(self):
        # Placeholder function for handling the "Petugas Perpustakaan" section
        pass

    def Rak_Buku(self):
        # Placeholder function for handling the "Rak Buku" section
        pass

    def handle_login_admin(self):
        # Placeholder for admin login handling
        print("Admin login clicked")
        # Set current user as admin
        self.current_user = 'admin'
        # Switch to admin main screen
        self.stacked_widget.setCurrentWidget(self.main_screens['admin'])
        self.showMaximized()

    def handle_guest_login(self):
        # Placeholder for guest login handling
        print("Guest login clicked")
        # Set current user as guest
        self.current_user = 'guest'
        # Switch to guest main screen
        self.stacked_widget.setCurrentWidget(self.main_screens['guest'])
        self.showMaximized()

    def create_sidebar(self):
        # Create a widget to contain the sidebar layout
        sidebar_container = QWidget()
        
        # Create a QVBoxLayout for the sidebar
        sidebar_layout = QVBoxLayout()
        
        # Set background color and border for the sidebar container
        sidebar_container.setStyleSheet("background-color: #FFFFFF; border: 1px solid #808080; padding: 5px")
        
        # Assign the layout to the container widget
        sidebar_container.setLayout(sidebar_layout)
        
        # Add a label to describe the sidebar
        sidebar_label = QLabel("Navigation:")
        sidebar_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(sidebar_label)      

        # Create buttons for each sidebar item
        pencarian_button = QPushButton('Pencarian Buku')
        peminjaman_button = QPushButton('Peminjaman Buku')
        pengembalian_button = QPushButton('Pengembalian Buku')
        anggota_button = QPushButton('Anggota')
        petugas_button = QPushButton('Petugas')
        rak_button = QPushButton('Rak')

        # Connect buttons to the sidebar click handler
        pencarian_button.clicked.connect(lambda: self.handle_sidebar_click(pencarian_button.text()))
        peminjaman_button.clicked.connect(lambda: self.handle_sidebar_click(peminjaman_button.text()))
        pengembalian_button.clicked.connect(lambda: self.handle_sidebar_click(pengembalian_button.text()))
        anggota_button.clicked.connect(lambda: self.handle_sidebar_click(anggota_button.text()))
        petugas_button.clicked.connect(lambda: self.handle_sidebar_click(petugas_button.text()))
        rak_button.clicked.connect(lambda: self.handle_sidebar_click(rak_button.text()))

        # Customize button appearance
        buttons = [pencarian_button, peminjaman_button, pengembalian_button, anggota_button, petugas_button, rak_button]
        for button in buttons:
            button.setStyleSheet("QPushButton { background-color: #FFFFFF; border: 1px solid #808080; padding: 5px; }")
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Add buttons to the sidebar layout
        sidebar_layout.addWidget(pencarian_button)
        sidebar_layout.addWidget(peminjaman_button)
        sidebar_layout.addWidget(pengembalian_button)
        sidebar_layout.addWidget(anggota_button)
        sidebar_layout.addWidget(petugas_button)
        sidebar_layout.addWidget(rak_button)

        return sidebar_container



    def handle_sidebar_click(self, item):
        # Placeholder for sidebar item click handling
        print("Sidebar item clicked:", item.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LibraryApp()
    sys.exit(app.exec_())
