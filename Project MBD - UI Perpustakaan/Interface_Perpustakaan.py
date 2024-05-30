import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
import mysql.connector
from loginpage import LoginScreen
from dialogs import *


class LibraryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def connect_to_database(self):
        try:
            connection = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="Perpustakaan"
            )
            return connection
        except mysql.connector.Error as error:
            QMessageBox.critical(self, "Error", f"Failed to connect to database: {error}")
            return None

    def init_ui(self):
        self.setWindowTitle('Library Management')

        # Stacked widget for switching between login and main app screens
        self.stacked_widget = QStackedWidget()
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.stacked_widget)

        # Establish database connection
        self.db_connection = self.connect_to_database()

        if self.db_connection is None:
            sys.exit(1)  # Exit the application if failed to connect to the database

        # Login screen
        self.login_screen = LoginScreen(self)
        self.stacked_widget.addWidget(self.login_screen)

        # Main app screen (initially hidden)
        self.main_screens = {
            'admin': self.create_main_screen(admin=True),
            'guest': self.create_main_screen(admin=False)
        }
        self.stacked_widget.addWidget(self.main_screens['guest'])
        self.stacked_widget.addWidget(self.main_screens['admin'])

        # other screens
        self.peminjaman_screen = self.Peminjaman_buku_screen()
        self.pengembalian_screen = self.Pengembalian_buku_screen()
        self.stacked_widget.addWidget(self.peminjaman_screen)
        self.stacked_widget.addWidget(self.pengembalian_screen)

        self.setFixedSize(650, 700)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.stacked_widget.setCurrentIndex(0)  # Show login screen first

        # Create context menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.show()

    def create_title_groupbox(self):
        title_groupbox = QGroupBox()
        title_groupbox.setStyleSheet("QGroupBox { background-color: #A79277; border: 2px solid #808080; }")
        title_layout = QVBoxLayout()
        title_groupbox.setLayout(title_layout)

        message_label = QLabel("Sistem Manajemen Perpustakaan")
        message_label.setFont(QFont('Helvetica', 24))
        message_label.setAlignment(Qt.AlignCenter)  # Align center for title appearance
        message_label.setStyleSheet("background-color: #A79277;")
        title_layout.addWidget(message_label)

        return title_groupbox

    # Main Window (Pencarian Buku)
    def create_main_screen(self, admin=False):
        main_screen = QWidget()
        main_layout = QVBoxLayout()
        main_screen.setLayout(main_layout)
        main_screen.setStyleSheet("QWidget { background-color: #D1BB9E; }")

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

            # Adjusting main content area size and widget spacing
            content_area.setContentsMargins(10, 10, 10, 10)  # Set 10-pixel padding on all sides
            content_area.setSpacing(10)  # Set 10-pixel spacing between widgets

            # Message above search bar (stick to the right of the sidebar)
            message_label = QLabel("Pencarian Buku Perpustakaan")
            message_label.setFont(QFont('Helvetica', 18))
            message_label.setAlignment(Qt.AlignLeft)
            content_area.addWidget(message_label)
            content_area.addSpacerItem(QSpacerItem(50, 25, QSizePolicy.Ignored, QSizePolicy.Fixed))

            # Hint message above search bar
            message_label = QLabel("Ketiklah Judul Buku, Genre, atau Nama penulis dari Buku")
            message_label.setFont(QFont('Helvetica', 12))
            message_label.setAlignment(Qt.AlignCenter)
            content_area.addWidget(message_label)

            # Search bar
            search_layout = QHBoxLayout()
            search_layout.addSpacerItem(QSpacerItem(600, 20, QSizePolicy.Ignored, QSizePolicy.Fixed))
            search_input = QLineEdit()
            search_input.setStyleSheet("background-color: #ffffff;")
            search_input.setFont(QFont('Helvetica', 12))
            search_button = QPushButton("Search")
            search_button.setStyleSheet("""
                QPushButton {
                    background-color: #FFFFFF;
                }
                QPushButton:hover {
                    background-color: #E0EEF9; /* Change to the accent color on hover */
                }""")
            search_button.clicked.connect(lambda: self.search_books(search_input.text(), buku_table)
                                          )  # Connect search button to search function
            search_layout.addWidget(search_input)
            search_layout.addWidget(search_button)
            search_layout.addSpacerItem(QSpacerItem(600, 20, QSizePolicy.Ignored, QSizePolicy.Fixed))
            content_area.addLayout(search_layout)

            # Table
            table_headers = ["ID", "Judul", "Genre", "Tahun Terbit", "Penulis", "Rak", "Status"]
            buku_table = self.create_table(table_headers)  # Create the table
            buku_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            content_area.addWidget(buku_table)  # Add the table to the desired layout

            # Populate the table with data (using a custom query)
            buku_query = '''
            SELECT b.ID_Buku, b.Judul, r.Genre, b.Tahun_Terbit, b.Nama_Penulis, s.Kode_Rak AS Rak, b.Status
            FROM Buku b
            JOIN Menyimpan s ON b.ID_Buku = s.ID_Buku
            JOIN Rak r ON s.Kode_Rak = r.Kode_Rak
            ORDER BY ID_Buku;
            '''
            self.populate_table(buku_table, buku_query)

        else:
            # Message above search bar
            main_layout.addSpacerItem(QSpacerItem(25, 10, QSizePolicy.Ignored, QSizePolicy.Fixed))
            message_label = QLabel("Pencarian Buku Perpustakaan")
            message_label.setFont(QFont('Helvetica', 18))
            message_label.setAlignment(Qt.AlignTop)  # Align the message label to the top
            main_layout.addWidget(message_label)
            main_layout.addSpacerItem(QSpacerItem(50, 25, QSizePolicy.Ignored, QSizePolicy.Fixed))

            # Message below search bar
            message_label = QLabel("Ketiklah Judul Buku, Genre, atau Nama penulis dari Buku")
            message_label.setFont(QFont('Helvetica', 12))
            message_label.setAlignment(Qt.AlignTop)
            main_layout.addWidget(message_label)

            # Search bar
            search_layout = QHBoxLayout()
            search_input = QLineEdit()
            search_input.setFixedWidth(2500)
            search_input.setStyleSheet("background-color: #ffffff;")
            search_input.setFont(QFont('Helvetica', 12))
            search_button = QPushButton("Search")
            search_button.setStyleSheet("""
                QPushButton {
                    background-color: #FFFFFF;
                }
                QPushButton:hover {
                    background-color: #E0EEF9; /* Change to the accent color on hover */
                }""")
            search_button.clicked.connect(lambda: self.search_books(search_input.text(), buku_table)
                                          )  # Connect search button to search function
            search_layout.addWidget(search_input)
            search_layout.addWidget(search_button)
            main_layout.addLayout(search_layout)

            # Table
            table_headers = ["ID", "Judul", "Genre", "Tahun Terbit", "Penulis", "Rak", "Status"]
            buku_table = self.create_table(table_headers)  # Create the table
            buku_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            main_layout.addWidget(buku_table)  # Add the table to the desired layout

            # Populate the table with data (using a custom query)
            buku_query = '''
            SELECT b.ID_Buku, b.Judul, r.Genre, b.Tahun_Terbit, b.Nama_Penulis, s.Kode_Rak AS Rak, b.Status
            FROM Buku b
            JOIN Menyimpan s ON b.ID_Buku = s.ID_Buku
            JOIN Rak r ON s.Kode_Rak = r.Kode_Rak
            ORDER BY ID_Buku;
            '''
            self.populate_table(buku_table, buku_query)

        main_layout.addLayout(content_area)

        return main_screen

    def Peminjaman_buku_screen(self):
        peminjaman_screen = QWidget()
        peminjaman_layout = QVBoxLayout()
        peminjaman_screen.setLayout(peminjaman_layout)
        peminjaman_screen.setStyleSheet("QWidget { background-color: #D1BB9E; }")

        # App Title
        title_groupbox = self.create_title_groupbox()
        peminjaman_layout.addWidget(title_groupbox)

        # Define content_area
        content_area = QVBoxLayout()

        # Admin Main Screen
        admin_layout = QHBoxLayout()
        peminjaman_layout.addLayout(admin_layout)

        # Sidebar
        sidebar = self.create_sidebar()
        sidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        admin_layout.addWidget(sidebar)

        # Main content area
        content_area = QVBoxLayout()  # Create content_area layout
        admin_layout.addLayout(content_area)

        # Adjusting main content area size and widget spacing
        content_area.setContentsMargins(10, 10, 10, 10)  # Set 10-pixel padding on all sides
        content_area.setSpacing(10)  # Set 10-pixel spacing between widgets

        # Message above search bar (stick to the right of the sidebar)
        message_label = QLabel("Peminjaman Buku Perpustakaan")
        message_label.setFont(QFont('Helvetica', 18))
        message_label.setAlignment(Qt.AlignLeft)
        content_area.addWidget(message_label)
        content_area.addSpacerItem(QSpacerItem(50, 25, QSizePolicy.Ignored, QSizePolicy.Fixed))

        # Hint message above search bar
        message_label = QLabel("Ketiklah Judul Buku, Nama Anggota, atau Tanggal Peminjaman Buku")
        message_label.setFont(QFont('Helvetica', 12))
        message_label.setAlignment(Qt.AlignCenter)
        content_area.addWidget(message_label)

        # Search bar
        search_layout = QHBoxLayout()
        search_layout.addSpacerItem(QSpacerItem(600, 20, QSizePolicy.Ignored, QSizePolicy.Fixed))
        search_input = QLineEdit()
        search_input.setStyleSheet("background-color: #ffffff;")
        search_input.setFont(QFont('Helvetica', 12))
        search_button = QPushButton("Search")
        search_button.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
            }
            QPushButton:hover {
                background-color: #E0EEF9; /* Change to the accent color on hover */
            }""")
        search_button.clicked.connect(lambda: self.search_peminjaman(search_input.text(), self.peminjaman_table))
        search_layout.addWidget(search_input)
        search_layout.addWidget(search_button)
        search_layout.addSpacerItem(QSpacerItem(600, 20, QSizePolicy.Ignored, QSizePolicy.Fixed))
        content_area.addLayout(search_layout)

        # table
        table_headers = ["ID Peminjaman", "ID Petugas", "Petugas", "ID Anggota",
                         "Anggota", "ID Buku", "Judul", "Tanggal pinjam", "Tenggat"]
        self.peminjaman_table = self.create_table(table_headers)  # Create the table and get its header
        self.peminjaman_table.setMaximumHeight(1500)

        content_area.addWidget(self.peminjaman_table)  # Add the table to the layout

        # Populate the table with data (using a custom query)
        peminjaman_query = '''
        SELECT pem.ID_Peminjaman, pem.ID_Petugas, p.Nama_Petugas, pem.ID_Anggota, a.Nama_Anggota, pem.ID_Buku, b.Judul, pem.Tgl_Pinjam, pem.Tenggat_Kembali
        FROM Peminjaman pem
        JOIN Petugas p ON pem.ID_Petugas = p.ID_Petugas
        JOIN Anggota a ON pem.ID_Anggota = a.ID_Anggota
        JOIN Buku b ON pem.ID_Buku = b.ID_Buku
        ORDER BY ID_Peminjaman;
        '''
        self.populate_table(self.peminjaman_table, peminjaman_query)

        # Add and delete buttons (just placeholders, you need to implement their functionalities)
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignBottom)
        add_button = QPushButton("Tambah Peminjaman")
        add_button.clicked.connect(lambda: self.open_dialog("add_button", "peminjaman"))
        delete_button = QPushButton("Hapus Peminjaman")
        delete_button.clicked.connect(lambda: self.open_dialog("delete_button", "peminjaman"))
        buttons_layout.addSpacerItem(QSpacerItem(100, 50, QSizePolicy.Ignored, QSizePolicy.Fixed))
        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(delete_button)
        buttons_layout.addSpacerItem(QSpacerItem(100, 50, QSizePolicy.Ignored, QSizePolicy.Fixed))
        content_area.addLayout(buttons_layout)

        # Customize button appearance
        buttons = [add_button, delete_button]
        for button in buttons:
            button.setStyleSheet(
                """
                QPushButton {
                    background-color: #FFF2E1;
                    border: 1px solid #808080;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #CCC1B4; /* Change to the accent color on hover */
                }
                QPushButton:pressed {
                    background-color: #999087;
                }
                """
            )
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        return peminjaman_screen

    def Pengembalian_buku_screen(self):
        pengembalian_screen = QWidget()
        pengembalian_layout = QVBoxLayout()
        pengembalian_screen.setLayout(pengembalian_layout)
        pengembalian_screen.setStyleSheet("QWidget { background-color: #D1BB9E; }")

        # App Title
        title_groupbox = self.create_title_groupbox()
        pengembalian_layout.addWidget(title_groupbox)

        # Define content_area
        content_area = QVBoxLayout()

        # Admin Main Screen
        admin_layout = QHBoxLayout()
        pengembalian_layout.addLayout(admin_layout)

        # Sidebar
        sidebar = self.create_sidebar()
        sidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        admin_layout.addWidget(sidebar)

        # Main content area
        content_area = QVBoxLayout()  # Create content_area layout
        admin_layout.addLayout(content_area)

        # Adjusting main content area size and widget spacing
        content_area.setContentsMargins(10, 10, 10, 10)  # Set 10-pixel padding on all sides
        content_area.setSpacing(10)  # Set 10-pixel spacing between widgets

        # Message above search bar (stick to the right of the sidebar)
        message_label = QLabel("Pengembalian Buku Perpustakaan")
        message_label.setFont(QFont('Helvetica', 18))
        message_label.setAlignment(Qt.AlignLeft)
        content_area.addWidget(message_label)
        content_area.addSpacerItem(QSpacerItem(50, 25, QSizePolicy.Ignored, QSizePolicy.Fixed))

        # Hint message above search bar
        message_label = QLabel("Ketiklah Judul Buku, Nama Anggota, atau Tanggal Pengembalian Buku")
        message_label.setFont(QFont('Helvetica', 12))
        message_label.setAlignment(Qt.AlignCenter)
        content_area.addWidget(message_label)

        # Search bar
        search_layout = QHBoxLayout()
        search_layout.addSpacerItem(QSpacerItem(600, 20, QSizePolicy.Ignored, QSizePolicy.Fixed))
        search_input = QLineEdit()
        search_input.setStyleSheet("background-color: #ffffff;")
        search_input.setFont(QFont('Helvetica', 12))
        search_button = QPushButton("Search")
        search_button.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
            }
            QPushButton:hover {
                background-color: #E0EEF9; /* Change to the accent color on hover */
            }""")
        search_button.clicked.connect(lambda: self.search_pengembalian(search_input.text(), self.pengembalian_table))
        search_layout.addWidget(search_input)
        search_layout.addWidget(search_button)
        search_layout.addSpacerItem(QSpacerItem(600, 20, QSizePolicy.Ignored, QSizePolicy.Fixed))
        content_area.addLayout(search_layout)

        # table
        table_headers = ["ID pengembalian", "ID Petugas", "Petugas", "ID Anggota",
                         "Anggota", "ID Buku", "Judul", "Tanggal Kembali", "Denda"]
        self.pengembalian_table = self.create_table(table_headers)  # Create the table and get its header
        self.pengembalian_table.setMaximumHeight(1500)

        content_area.addWidget(self.pengembalian_table)  # Add the table to the layout

        # Populate the table with data (using a custom query)
        pengembalian_query = '''
        SELECT peng.ID_Pengembalian, peng.ID_Petugas, p.Nama_Petugas, peng.ID_Anggota, a.Nama_Anggota, peng.ID_Buku, b.Judul, peng.Tgl_Pengembalian, peng.Denda
        FROM Pengembalian peng
        JOIN Petugas p ON peng.ID_Petugas = p.ID_Petugas
        JOIN Anggota a ON peng.ID_Anggota = a.ID_Anggota
        JOIN Buku b ON peng.ID_Buku = b.ID_Buku
        ORDER BY ID_Pengembalian;
        '''
        self.populate_table(self.pengembalian_table, pengembalian_query)

        # Add and delete buttons (just placeholders, you need to implement their functionalities)
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignBottom)
        add_button = QPushButton("Tambah Pengembalian")
        add_button.clicked.connect(lambda: self.open_dialog("add_button", "pengembalian"))
        delete_button = QPushButton("Hapus Pengembalian")
        delete_button.clicked.connect(lambda: self.open_dialog("delete_button", "pengembalian"))
        buttons_layout.addSpacerItem(QSpacerItem(100, 50, QSizePolicy.Ignored, QSizePolicy.Fixed))
        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(delete_button)
        buttons_layout.addSpacerItem(QSpacerItem(100, 50, QSizePolicy.Ignored, QSizePolicy.Fixed))
        content_area.addLayout(buttons_layout)

        # Customize button appearance
        buttons = [add_button, delete_button]
        for button in buttons:
            button.setStyleSheet(
                """
                QPushButton {
                    background-color: #FFF2E1;
                    border: 1px solid #808080;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #CCC1B4; /* Change to the accent color on hover */
                }
                QPushButton:pressed {
                    background-color: #999087;
                }
                """
            )
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        return pengembalian_screen

    def handle_login_admin(self):
        # Placeholder for admin login handling
        print("Admin login clicked")
        # Set current user as admin
        self.current_user = 'admin'
        # Switch to admin main screen
        self.stacked_widget.setCurrentWidget(self.main_screens['admin'])
        self.showFullScreen()

    def handle_guest_login(self):
        # Placeholder for guest login handling
        print("Guest login clicked")
        # Set current user as guest
        self.current_user = 'guest'
        # Switch to guest main screen
        self.stacked_widget.setCurrentWidget(self.main_screens['guest'])
        self.showFullScreen()

    def create_sidebar(self):
        # Create a widget to contain the sidebar layout
        sidebar_container = QWidget()

        # Create a QVBoxLayout for the sidebar
        sidebar_layout = QVBoxLayout()

        # Set background color and border for the sidebar container
        sidebar_container.setStyleSheet("background-color: #EAD8C0; border: 1px solid #808080; padding: 5px")

        # Assign the layout to the container widget
        sidebar_container.setLayout(sidebar_layout)

        sidebar_layout.addSpacerItem(QSpacerItem(10, 15, QSizePolicy.Ignored, QSizePolicy.Fixed))

        # Add a title label with appropriate height
        sidebar_label = QLabel("MENU")
        sidebar_label.setFont(QFont('Helvetica', 20))
        sidebar_label.setStyleSheet("border: 1px;")
        sidebar_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(sidebar_label)

        sidebar_layout.addSpacerItem(QSpacerItem(10, 20, QSizePolicy.Ignored, QSizePolicy.Fixed))

        # Create buttons for each sidebar item
        pencarian_button = QPushButton('Pencarian Buku')
        peminjaman_button = QPushButton('Peminjaman Buku')
        pengembalian_button = QPushButton('Pengembalian Buku')
        anggota_button = QPushButton('Anggota')
        petugas_button = QPushButton('Petugas')
        rak_button = QPushButton('Rak')
        exit_button = QPushButton("Exit")

        # Set font for all buttons at once
        side_button_font = QFont('Helvetica', 12)  # Adjust font family and size as desired
        buttons = [pencarian_button, peminjaman_button, pengembalian_button,
                   anggota_button, petugas_button, rak_button, exit_button]
        for button in buttons:
            button.setFont(side_button_font)

        # Connect buttons to the appropriate actions
        pencarian_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_screens['admin']))
        peminjaman_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.peminjaman_screen))
        pengembalian_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.pengembalian_screen))
        anggota_button.clicked.connect(lambda: self.handle_sidebar_click(anggota_button.text()))
        petugas_button.clicked.connect(lambda: self.handle_sidebar_click(petugas_button.text()))
        rak_button.clicked.connect(lambda: self.handle_sidebar_click(rak_button.text()))
        exit_button.clicked.connect(QApplication.quit)

        # Customize button appearance
        buttons = [pencarian_button, peminjaman_button, pengembalian_button,
                   anggota_button, petugas_button, rak_button, exit_button]
        for button in buttons:
            button.setStyleSheet(
                """
                QPushButton {
                    background-color: #FFF2E1;
                    border: 1px solid #808080;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #CCC1B4; /* Change to the accent color on hover */
                }
                QPushButton:pressed {
                    background-color: #999087;
                }
                """
            )
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Add buttons to the layout
        sidebar_layout.addWidget(pencarian_button)
        sidebar_layout.addWidget(peminjaman_button)
        sidebar_layout.addWidget(pengembalian_button)
        sidebar_layout.addWidget(anggota_button)
        sidebar_layout.addWidget(petugas_button)
        sidebar_layout.addWidget(rak_button)
        sidebar_layout.addWidget(exit_button)

        # Optional spacer to push content to the top
        sidebar_layout.addSpacerItem(QSpacerItem(20, 100, QSizePolicy.Ignored, QSizePolicy.Expanding))

        return sidebar_container

    def handle_sidebar_click(self, item):
        print("Sidebar item clicked:", item)

    def create_table(self, column_headers):
        table = QTableWidget()
        table.setColumnCount(len(column_headers))  # Set the number of columns in the table
        table.setHorizontalHeaderLabels(column_headers)  # Set column headers

        # Set styles for the table header
        header_style = """
            QHeaderView::section {
                background-color: #A79277;
                font-weight: bold;
            }
        """
        table.horizontalHeader().setStyleSheet(header_style)
        table.verticalHeader().setStyleSheet(header_style)

        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Set resize mode
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Make the table read-only
        return table  # Only return the table object

    def populate_table(self, table, query):
        cursor = self.db_connection.cursor()

        # Execute the custom query to fetch data from the database
        cursor.execute(query)

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Clear existing rows in the table
        table.setRowCount(0)

        # Iterate over the rows and populate the table
        for row_index, row_data in enumerate(rows):
            # Insert a new row in the table
            table.insertRow(row_index)

            # Populate the cells in the row with data from the database
            for column_index, column_data in enumerate(row_data):
                item = QTableWidgetItem(str(column_data))  # Convert the value to a string and create a QTableWidgetItem

                # Set the background and foreground color for the item
                item.setForeground(QColor("#000000"))
                item.setBackground(QColor("#EAD8C0"))

                table.setItem(row_index, column_index, item)  # Set the item in the table

    # Search Buku function
    def search_books(self, query, table):
        # Construct SQL query to search for books
        search_query = f'''
            SELECT b.ID_Buku, b.Judul, r.Genre, b.Tahun_Terbit, b.Nama_Penulis, s.Kode_Rak AS Rak, b.Status
            FROM Buku b
            JOIN Menyimpan s ON b.ID_Buku = s.ID_Buku
            JOIN Rak r ON s.Kode_Rak = r.Kode_Rak
            WHERE b.Judul LIKE '%{query}%' OR b.Nama_Penulis LIKE '%{query}%' OR r.Genre LIKE '%{query}%'
            ORDER BY b.ID_Buku;
        '''

        # Execute the search query
        cursor = self.db_connection.cursor()
        cursor.execute(search_query)

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        if not rows:
            QMessageBox.information(self, "Search Results", "No results found for the given query.")
        else:
            # Populate the table with search results
            self.populate_table(table, search_query)

    # Search Peminjaman function
    def search_peminjaman(self, query, table):
        # Construct SQL query to search for books
        search_query = f'''
        SELECT pem.ID_Peminjaman, pem.ID_Petugas, p.Nama_Petugas, pem.ID_Anggota, a.Nama_Anggota, pem.ID_Buku, b.Judul, pem.Tgl_Pinjam, pem.Tenggat_Kembali
        FROM Peminjaman pem
        JOIN Petugas p ON pem.ID_Petugas = p.ID_Petugas
        JOIN Anggota a ON pem.ID_Anggota = a.ID_Anggota
        JOIN Buku b ON pem.ID_Buku = b.ID_Buku
        WHERE a.Nama_Anggota LIKE '%{query}%' OR b.Judul LIKE '%{query}%' OR pem.Tgl_Pinjam LIKE '%{query}%'
        ORDER BY ID_Peminjaman;
        '''
        # Execute the search query
        cursor = self.db_connection.cursor()
        cursor.execute(search_query)

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        if not rows:
            QMessageBox.information(self, "Search Results", "No results found for the given query.")
        else:
            # Populate the table with search results
            self.populate_table(table, search_query)

    # Search Pengmbalian function
    def search_pengembalian(self, query, table):
        # Construct SQL query to search for books
        search_query = f'''
        SELECT peng.ID_Pengembalian, peng.ID_Petugas, p.Nama_Petugas, peng.ID_Anggota, a.Nama_Anggota, peng.ID_Buku, b.Judul, peng.Tgl_Pengembalian, peng.Denda
        FROM Pengembalian peng
        JOIN Petugas p ON peng.ID_Petugas = p.ID_Petugas
        JOIN Anggota a ON peng.ID_Anggota = a.ID_Anggota
        JOIN Buku b ON peng.ID_Buku = b.ID_Buku
        WHERE a.Nama_Anggota LIKE '%{query}%' OR b.Judul LIKE '%{query}%' OR peng.Tgl_Pengembalian LIKE '%{query}%'
        ORDER BY ID_Pengembalian;
        '''
        # Execute the search query
        cursor = self.db_connection.cursor()
        cursor.execute(search_query)

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        if not rows:
            QMessageBox.information(self, "Search Results", "No results found for the given query.")
        else:
            # Populate the table with search results
            self.populate_table(table, search_query)

    def open_dialog(self, item, dialog_type):
        dialog = None
        if item == "add_button":
            if dialog_type == "peminjaman":
                dialog = TambahPeminjamanDialog()
            elif dialog_type == "pengembalian":
                dialog = TambahPengembalianDialog()

        elif item == "delete_button":
            if dialog_type == "peminjaman":
                dialog = HapusPeminjamanDialog()
            elif dialog_type == "pengembalian":
                dialog = HapusPengembalianDialog()

        if dialog and dialog.exec_() == QDialog.Accepted:
            # Reconnect to the database
            self.db_connection = self.connect_to_database()

            # Determine table to populate based on dialog type
            table = self.peminjaman_table if dialog_type == "peminjaman" else self.pengembalian_table

            # Repopulate the table
            if dialog_type == "peminjaman":
                query = '''
                    SELECT pem.ID_Peminjaman, pem.ID_Petugas, p.Nama_Petugas, pem.ID_Anggota, a.Nama_Anggota, pem.ID_Buku, b.Judul, pem.Tgl_Pinjam, pem.Tenggat_Kembali
                    FROM Peminjaman pem
                    JOIN Petugas p ON pem.ID_Petugas = p.ID_Petugas
                    JOIN Anggota a ON pem.ID_Anggota = a.ID_Anggota
                    JOIN Buku b ON pem.ID_Buku = b.ID_Buku
                    ORDER BY ID_Peminjaman;
                '''
            elif dialog_type == "pengembalian":
                query = '''
                    SELECT peng.ID_Pengembalian, peng.ID_Petugas, p.Nama_Petugas, peng.ID_Anggota, a.Nama_Anggota, peng.ID_Buku, b.Judul, peng.Tgl_Pengembalian, peng.Denda
                    FROM Pengembalian peng
                    JOIN Petugas p ON peng.ID_Petugas = p.ID_Petugas
                    JOIN Anggota a ON peng.ID_Anggota = a.ID_Anggota
                    JOIN Buku b ON peng.ID_Buku = b.ID_Buku
                    ORDER BY ID_Pengembalian;
                '''

            self.populate_table(table, query)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def show_context_menu(self, pos):
        menu = QMenu(self)
        exit_action = menu.addAction('Exit')
        exit_action.triggered.connect(self.close)
        menu.exec_(self.mapToGlobal(pos))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LibraryApp()

    sys.exit(app.exec_())
