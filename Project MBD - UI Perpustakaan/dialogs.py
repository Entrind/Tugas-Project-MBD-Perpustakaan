import mysql.connector
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QDate
from datetime import datetime


class BaseDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="anD1ka02_r4hman",
            database="Perpustakaan"
        )

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

    def has_active_borrowings(self, book_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Peminjaman WHERE ID_Buku = %s", (book_id,))
        borrow_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Pengembalian WHERE ID_Buku = %s", (book_id,))
        return borrow_count > cursor.fetchone()[0]


class TambahPeminjamanDialog(BaseDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tambah Peminjaman")
        self.setMinimumSize(600, 300)

        layout = QVBoxLayout(self)

        # Label Input
        label_input = QLabel("Tambah Peminjaman")
        font = QFont("Helvetica", 15)
        font.setBold(True)
        label_input.setFont(font)
        layout.addWidget(label_input, alignment=Qt.AlignCenter)

        # Separator Line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(separator)

        grid_layout = QGridLayout()

        # Label
        labels = ["Nama Petugas", "Nama Anggota", "Judul Buku", "Tanggal Pinjam", "Tenggat Kembali"]
        for i, label_text in enumerate(labels):
            label = QLabel(label_text)
            label.setFont(QFont("Helvetica", 10))
            grid_layout.addWidget(label, i, 0, Qt.AlignLeft)

            # Separator Kolon
            colon_label = QLabel(":")
            grid_layout.addWidget(colon_label, i, 1, Qt.AlignCenter)

        # Inputan
        self.nama_petugas_entry = QLineEdit()
        self.nama_anggota_entry = QLineEdit()
        self.judul_buku_entry = QLineEdit()
        self.tanggal_pinjam_entry = QDateEdit()  # Change to QDateEdit
        self.tanggal_pinjam_entry.setCalendarPopup(True)  # Enable calendar popup
        self.tanggal_pinjam_entry.setDate(QDate.currentDate())  # Set default date to current date
        self.tenggat_kembali_entry = QDateEdit()  # Change to QDateEdit
        self.tenggat_kembali_entry.setCalendarPopup(True)  # Enable calendar popup
        self.tenggat_kembali_entry.setDate(QDate.currentDate())  # Set default date to current date

        inputan = [self.nama_petugas_entry, self.nama_anggota_entry,
                   self.judul_buku_entry, self.tanggal_pinjam_entry, self.tenggat_kembali_entry]
        for i, input in enumerate(inputan):
            grid_layout.addWidget(input, i, 2)

        layout.addLayout(grid_layout)

        # Separator Line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(separator)

        # Submit Button
        tombol_submit = QPushButton("Submit")
        tombol_submit.setFont(QFont("Helvetica", 10))
        tombol_submit.clicked.connect(self.submit_catatan)
        layout.addWidget(tombol_submit, alignment=Qt.AlignRight)

    def submit_catatan(self):
        nama_petugas = self.nama_petugas_entry.text()
        nama_anggota = self.nama_anggota_entry.text()
        judul_buku = self.judul_buku_entry.text()
        tanggal_pinjam = self.tanggal_pinjam_entry.date().toString("yyyy-MM-dd")
        tenggat_kembali = self.tenggat_kembali_entry.date().toString("yyyy-MM-dd")

        cursor = self.conn.cursor()

        # Get ID of petugas based on nama_petugas
        cursor.execute("SELECT ID_Petugas FROM Petugas WHERE Nama_Petugas = %s", (nama_petugas,))
        result = cursor.fetchone()
        if result:
            id_petugas = result[0]
        else:
            QMessageBox.critical(self, "Error", "Petugas not found.")
            return

        # Get ID of anggota based on nama_anggota
        cursor.execute("SELECT ID_Anggota FROM Anggota WHERE Nama_Anggota = %s", (nama_anggota,))
        result = cursor.fetchone()
        if result:
            id_anggota = result[0]
        else:
            QMessageBox.critical(self, "Error", "Anggota not found.")
            return

        # Get ID of buku based on judul_buku
        cursor.execute("SELECT ID_Buku FROM Buku WHERE Judul = %s", (judul_buku,))
        result = cursor.fetchone()
        if result:
            id_buku = result[0]
        else:
            QMessageBox.critical(self, "Error", "Buku not found.")
            return

        # Generate ID_Peminjaman
        cursor.execute("SELECT MAX(ID_Peminjaman) FROM Peminjaman")
        result = cursor.fetchone()
        if result and result[0]:
            last_id = int(result[0][3:])  # Extract the numeric part
            new_id = f"PMJ{last_id + 1:03d}"  # Increment and format
        else:
            new_id = "PMJ001"

        # Insert data into the table
        insert_query = "INSERT INTO Peminjaman (ID_Petugas, ID_Anggota, ID_Buku, ID_Peminjaman, Tgl_Pinjam, Tenggat_Kembali) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (id_petugas, id_anggota, id_buku, new_id, tanggal_pinjam, tenggat_kembali)
        cursor.execute(insert_query, data)

        cursor.execute("UPDATE Buku SET Status = 'borrowed' WHERE ID_Buku = %s", (id_buku,))

        self.conn.commit()
        cursor.close()

        QMessageBox.information(self, "Success", "Data inserted successfully.")
        self.accept()  # Close the dialog


class HapusPeminjamanDialog(BaseDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hapus Peminjaman")
        self.setMinimumSize(600, 300)

        layout = QVBoxLayout(self)

        # Label Input
        label_input = QLabel("Hapus Peminjaman")
        font = QFont("Helvetica", 15)
        font.setBold(True)
        label_input.setFont(font)
        layout.addWidget(label_input, alignment=Qt.AlignCenter)

        # Add explanatory text to guide users
        info_label = QLabel("Silakan isi salah satu ID Peminjaman atau berikan Nama Anggota, Judul Buku, dan Tanggal Pinjam.")
        layout.addWidget(info_label)

        # Garis Pemisah
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(separator)

        grid_layout = QGridLayout()

        # Label
        labels = ["ID Peminjaman", "Nama Anggota", "Judul Buku", "Tanggal Pinjam"]
        for i, label_text in enumerate(labels):
            label = QLabel(label_text)
            label.setFont(QFont("Helvetica", 10))
            grid_layout.addWidget(label, i, 0, Qt.AlignLeft)

            # Separator Kolon
            colon_label = QLabel(":")
            grid_layout.addWidget(colon_label, i, 1, Qt.AlignCenter)

        # Input
        self.id_peminjaman_entry = QLineEdit()
        self.nama_anggota_entry = QLineEdit()
        self.judul_buku_entry = QLineEdit()
        self.tanggal_pinjam_entry = QDateEdit()  # Change to QDateEdit
        self.tanggal_pinjam_entry.setCalendarPopup(True)  # Enable calendar popup
        self.tanggal_pinjam_entry.setDate(QDate.currentDate())  # Set default date to current date

        inputan = [self.id_peminjaman_entry, self.nama_anggota_entry, self.judul_buku_entry, self.tanggal_pinjam_entry]
        for i, input in enumerate(inputan):
            grid_layout.addWidget(input, i, 2)

        layout.addLayout(grid_layout)

        # Separator Line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(separator)

        # Submit Button
        tombol_submit = QPushButton("Submit")
        tombol_submit.setFont(QFont("Helvetica", 10))
        tombol_submit.clicked.connect(self.hapus_catatan)
        layout.addWidget(tombol_submit, alignment=Qt.AlignRight)

    def hapus_catatan(self):
        # Get input values
        id_peminjaman = self.id_peminjaman_entry.text()
        nama_anggota = self.nama_anggota_entry.text()
        judul_buku = self.judul_buku_entry.text()
        tanggal_pinjam = self.tanggal_pinjam_entry.date().toString("yyyy-MM-dd")

        # Validate input
        if not (id_peminjaman or (nama_anggota and judul_buku and tanggal_pinjam)):
            QMessageBox.warning(
                self, "Error", "Please fill either the ID Peminjaman or provide Nama Anggota, Judul Buku, and Tanggal Pinjam.")
            return

        # Check if the entry exists
        cursor = self.conn.cursor()
        if id_peminjaman:
            query = "SELECT ID_Buku FROM Peminjaman WHERE ID_Peminjaman = %s"
            data = (id_peminjaman,)
        else:
            query = "SELECT ID_Buku FROM Peminjaman WHERE ID_Anggota = (SELECT ID_Anggota FROM Anggota WHERE Nama_Anggota = %s) AND ID_Buku = (SELECT ID_Buku FROM Buku WHERE Judul = %s) AND Tgl_Pinjam = %s"
            data = (nama_anggota, judul_buku, tanggal_pinjam)

        cursor.execute(query, data)
        result = cursor.fetchone()
        if not result:
            QMessageBox.warning(self, "Error", "No matching entry found.")
            cursor.close()
            return

        id_buku = result[0]  # Extracting id_buku from the query result

        # Construct SQL query based on input
        if id_peminjaman:
            query = "DELETE FROM Peminjaman WHERE ID_Peminjaman = %s"
            data = (id_peminjaman,)
        else:
            query = "DELETE FROM Peminjaman WHERE ID_Anggota = (SELECT ID_Anggota FROM Anggota WHERE Nama_Anggota = %s) AND ID_Buku = (SELECT ID_Buku FROM Buku WHERE Judul = %s) AND Tgl_Pinjam = %s"
            data = (nama_anggota, judul_buku, tanggal_pinjam)

        # Execute deletion
        cursor.execute(query, data)
        self.conn.commit()

        # Check if there are no more active borrowings for the book
        if not self.has_active_borrowings(id_buku):
            # Update the status of the book to "available"
            cursor.execute("UPDATE Buku SET Status = 'available' WHERE ID_Buku = %s", (id_buku,))
            self.conn.commit()
        cursor.close()

        QMessageBox.information(self, "Success", "Data deleted successfully.")
        self.accept()  # Close the dialog


class TambahPengembalianDialog(BaseDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tambah Pengembalian")
        self.setMinimumSize(600, 300)

        layout = QVBoxLayout(self)

        # Label Input
        label_input = QLabel("Tambah Pengembalian")
        font = QFont("Helvetica", 15)
        font.setBold(True)
        label_input.setFont(font)
        layout.addWidget(label_input, alignment=Qt.AlignCenter)

        # Separator Line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(separator)

        grid_layout = QGridLayout()

        # Label
        labels = ["Nama Petugas", "Nama Anggota", "Judul Buku", "Tanggal Pengembalian"]
        for i, label_text in enumerate(labels):
            label = QLabel(label_text)
            label.setFont(QFont("Helvetica", 10))
            grid_layout.addWidget(label, i, 0, Qt.AlignLeft)

            # Separator Kolon
            colon_label = QLabel(":")
            grid_layout.addWidget(colon_label, i, 1, Qt.AlignCenter)

        # Inputan
        self.nama_petugas_entry = QLineEdit()
        self.nama_anggota_entry = QLineEdit()
        self.judul_buku_entry = QLineEdit()
        self.tanggal_pengembalian_entry = QDateEdit()  # Change to QDateEdit
        self.tanggal_pengembalian_entry.setCalendarPopup(True)  # Enable calendar popup
        self.tanggal_pengembalian_entry.setDate(QDate.currentDate())  # Set default date to current date

        inputan = [self.nama_petugas_entry, self.nama_anggota_entry, self.judul_buku_entry, self.tanggal_pengembalian_entry]
        for i, input in enumerate(inputan):
            grid_layout.addWidget(input, i, 2)

        layout.addLayout(grid_layout)

        # Separator Line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(separator)

        # Submit Button
        tombol_submit = QPushButton("Submit")
        tombol_submit.setFont(QFont("Helvetica", 10))
        tombol_submit.clicked.connect(self.submit_catatan)
        layout.addWidget(tombol_submit, alignment=Qt.AlignRight)

    def submit_catatan(self):
        nama_petugas = self.nama_petugas_entry.text()
        nama_anggota = self.nama_anggota_entry.text()
        judul_buku = self.judul_buku_entry.text()
        tanggal_pengembalian = self.tanggal_pengembalian_entry.date().toString("yyyy-MM-dd")

        cursor = self.conn.cursor()

        # Get ID of petugas based on nama_petugas
        cursor.execute("SELECT ID_Petugas FROM Petugas WHERE Nama_Petugas = %s", (nama_petugas,))
        result = cursor.fetchone()
        if result:
            id_petugas = result[0]
        else:
            QMessageBox.critical(self, "Error", "Petugas not found.")
            return

        # Get ID of anggota based on nama_anggota
        cursor.execute("SELECT ID_Anggota FROM Anggota WHERE Nama_Anggota = %s", (nama_anggota,))
        result = cursor.fetchone()
        if result:
            id_anggota = result[0]
        else:
            QMessageBox.critical(self, "Error", "Anggota not found.")
            return

        # Get ID of buku based on judul_buku
        cursor.execute("SELECT ID_Buku FROM Buku WHERE Judul = %s", (judul_buku,))
        result = cursor.fetchone()
        if result:
            id_buku = result[0]
        else:
            QMessageBox.critical(self, "Error", "Buku not found.")
            return

        # Calculate Denda
        cursor.execute("SELECT Tenggat_Kembali FROM Peminjaman WHERE ID_Anggota = (SELECT ID_Anggota FROM Anggota WHERE Nama_Anggota = %s) AND ID_Buku = (SELECT ID_Buku FROM Buku WHERE Judul = %s)", (nama_anggota, judul_buku))
        tenggat_kembali = cursor.fetchone()
        print("Tenggat Kembali:", tenggat_kembali)  # Add this line to check the value
        if tenggat_kembali:
            tenggat_kembali = tenggat_kembali[0]
            print("Tenggat Kembali (before conversion):", tenggat_kembali)  # Add this line to check the value before conversion
            # Convert tanggal_pengembalian and tenggat_kembali to datetime objects
            tanggal_pengembalian_date = datetime.strptime(tanggal_pengembalian, "%Y-%m-%d")
            tenggat_kembali_date = datetime.strptime(str(tenggat_kembali), "%Y-%m-%d")
            # Calculate difference in days
            difference = (tanggal_pengembalian_date - tenggat_kembali_date).days
            print("Difference (days):", difference)  # Add this line to check the difference
            # Calculate denda (assuming 2000 per day)
            denda = max(difference, 0) * 2000
            print("Denda:", denda)  # Add this line to check the calculated denda
        else:
            QMessageBox.critical(self, "Error", "No matching entry found in Peminjaman table.")
            return

        # Generate ID_Pengembalian
        cursor.execute("SELECT MAX(ID_Pengembalian) FROM Pengembalian")
        result = cursor.fetchone()
        if result and result[0]:
            last_id = int(result[0][4:])  # Extract the numeric part
            new_id = f"PENG{last_id + 1:03d}"  # Increment and format
        else:
            new_id = "PENG001"

        # Insert data into the table
        insert_query = "INSERT INTO Pengembalian (ID_Petugas, ID_Anggota, ID_Buku, ID_Pengembalian, Tgl_Pengembalian, Denda) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (id_petugas, id_anggota, id_buku, new_id, tanggal_pengembalian, denda)
        cursor.execute(insert_query, data)

        cursor.execute("UPDATE Buku SET Status = 'available' WHERE ID_Buku = %s", (id_buku,))

        self.conn.commit()
        cursor.close()

        QMessageBox.information(self, "Success", "Data inserted successfully.")
        self.accept()  # Close the dialog

    def closeEvent(self, event):
        self.conn.close()
        event.accept()


class HapusPengembalianDialog(BaseDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hapus Pengembalian")
        self.setMinimumSize(600, 300)

        layout = QVBoxLayout(self)

        # Label Input
        label_input = QLabel("Hapus Pengembalian")
        font = QFont("Helvetica", 15)
        font.setBold(True)
        label_input.setFont(font)
        layout.addWidget(label_input, alignment=Qt.AlignCenter)

        # Add explanatory text to guide users
        info_label = QLabel("Silakan isi salah satu ID Pengembalian atau berikan Nama Anggota, Judul Buku, dan Tanggal Pengembalian.")
        layout.addWidget(info_label)

        # Separator Line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(separator)

        grid_layout = QGridLayout()

        # Label
        labels = ["ID Pengembalian", "Nama Anggota", "Judul Buku", "Tanggal Pengembalian"]
        for i, label_text in enumerate(labels):
            label = QLabel(label_text)
            label.setFont(QFont("Helvetica", 10))
            grid_layout.addWidget(label, i, 0, Qt.AlignLeft)

            # Separator Kolon
            colon_label = QLabel(":")
            grid_layout.addWidget(colon_label, i, 1, Qt.AlignCenter)

        # Inputan
        self.id_pengembalian_entry = QLineEdit()
        self.nama_anggota_entry = QLineEdit()
        self.judul_buku_entry = QLineEdit()
        self.tanggal_pengembalian_entry = QDateEdit()  # Change to QDateEdit
        self.tanggal_pengembalian_entry.setCalendarPopup(True)  # Enable calendar popup
        self.tanggal_pengembalian_entry.setDate(QDate.currentDate())  # Set default date to current date

        inputan = [self.id_pengembalian_entry, self.nama_anggota_entry, self.judul_buku_entry, self.tanggal_pengembalian_entry]
        for i, input in enumerate(inputan):
            grid_layout.addWidget(input, i, 2)

        layout.addLayout(grid_layout)

        # Separator Line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(separator)

        # Submit Button
        tombol_submit = QPushButton("Submit")
        tombol_submit.setFont(QFont("Helvetica", 10))
        tombol_submit.clicked.connect(self.hapus_catatan)
        layout.addWidget(tombol_submit, alignment=Qt.AlignRight)

    def hapus_catatan(self):
        # Get input values
        id_pengembalian = self.id_pengembalian_entry.text()
        nama_anggota = self.nama_anggota_entry.text()
        judul_buku = self.judul_buku_entry.text()
        tanggal_pengembalian = self.tanggal_pengembalian_entry.date().toString("yyyy-MM-dd")

        # Validate input
        if not (id_pengembalian or (nama_anggota and judul_buku and tanggal_pengembalian)):
            QMessageBox.warning(
                self, "Error", "Please fill either the ID Pengembalian or provide Nama Anggota, Judul Buku, and Tanggal Pengembalian.")
            return

        # Check if the entry exists
        cursor = self.conn.cursor()
        if id_pengembalian:
            query = "SELECT ID_Buku FROM Pengembalian WHERE ID_Pengembalian = %s"
            data = (id_pengembalian,)
        else:
            query = "SELECT ID_Buku FROM Pengembalian WHERE ID_Anggota = (SELECT ID_Anggota FROM Anggota WHERE Nama_Anggota = %s) AND ID_Buku = (SELECT ID_Buku FROM Buku WHERE Judul = %s) AND Tgl_Pengembalian = %s"
            data = (nama_anggota, judul_buku, tanggal_pengembalian)

        cursor.execute(query, data)
        result = cursor.fetchone()
        if not result:
            QMessageBox.warning(self, "Error", "No matching entry found.")
            cursor.close()
            return

        id_buku = result[0]  # Extracting id_buku from the query result

        # Construct SQL query based on input
        if id_pengembalian:
            query = "DELETE FROM Pengembalian WHERE ID_Pengembalian = %s"
            data = (id_pengembalian,)
        else:
            query = "DELETE FROM Pengembalian WHERE ID_Anggota = (SELECT ID_Anggota FROM Anggota WHERE Nama_Anggota = %s) AND ID_Buku = (SELECT ID_Buku FROM Buku WHERE Judul = %s) AND Tgl_Pengembalian = %s"
            data = (nama_anggota, judul_buku, tanggal_pengembalian)

        # Execute deletion
        cursor.execute(query, data)
        self.conn.commit()

        # Check if there are no more active borrowings for the book
        if not self.has_active_borrowings(id_buku):
            # Update the status of the book to "available"
            cursor.execute("UPDATE Buku SET Status = 'available' WHERE ID_Buku = %s", (id_buku,))
            self.conn.commit()
        cursor.close()

        QMessageBox.information(self, "Success", "Data deleted successfully.")
        self.accept()  # Close the dialog


if __name__ == "__main__":
    app = QApplication([])
    tambah_peminjaman_dialog = TambahPeminjamanDialog()
    tambah_peminjaman_dialog.show()
    app.exec_()
