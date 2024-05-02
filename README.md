# Tugas-Project-MBD-Perpustakaan
Tugas-Project-MBD

Membuat GUI untuk Database MySQL dengan Python untuk integrasi dengan database MySQL.

Link Repository Github
Kelompok 8: Sistem Manajemen Perpustakaan

    D121221071 | Andika Arif Rahman
    D121221089 | Muhammad Rifqi

Library Python yang digunakan:

    PyQt5: Digunakan untuk membuat antarmuka grafis (GUI) pada aplikasi Python.
    mysql.connector: Digunakan untuk menghubungkan program Python dengan database MySQL.

Note

Penginstalan library tersebut dapat dilakukan melalui command-line interface (CLI):

    Instalasi PyQt5

pip install PyQt5

    Instalasi mysql.connector

pip install mysql-connector-python

Fungsi Program:

    Mengakses Tabel-tabel dari Database Perpustakaan di MySQL.
    Login page untuk memisahkan admin(petugas perpustakaan) dengan umum.
    Search Function untuk pada halaman Pencarian Buku, Peminjaman Buku, dan Pengembalian Buku.
    Insert Function untuk memasukkan data peminjaman dan pengembalian buku.
    Delete Function untuk menghapus peminjaman dan pengembalian buku.

Note
Program hanya bisa berjalan jika sudah terkoneksi dengan host database MySQL yang digunakan.

Berikut segment kode program yang digunakan untuk inisialisi koneksi database MySQL:
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
