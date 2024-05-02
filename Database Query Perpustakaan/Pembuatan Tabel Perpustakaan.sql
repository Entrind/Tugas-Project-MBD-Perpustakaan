# Membuat Database Perpustakaan
DROP DATABASE Perpustakaan; # Agar Query bisa berjalan berulangkali
CREATE DATABASE Perpustakaan;
USE Perpustakaan;

# Pembuatan Tabel-Tabel
CREATE TABLE Petugas
(ID_Petugas VARCHAR(10) PRIMARY KEY, 
Nama_Petugas VARCHAR(20), 
Kontak_Petugas VARCHAR(12), 
Alamat_Petugas VARCHAR(100),
Password_Akun VARCHAR(255)DEFAULT 'adminpass');

CREATE TABLE Anggota
(ID_Anggota VARCHAR(10) PRIMARY KEY, 
Nama_Anggota VARCHAR(20), 
Kontak_Anggota VARCHAR(12), 
Alamat_Anggota VARCHAR(100));

CREATE TABLE Buku
(ID_Buku VARCHAR(10) PRIMARY KEY, 
Judul VARCHAR(50), 
ISBN VARCHAR(13), 
Tahun_Terbit YEAR, 
Nama_Penulis VARCHAR(50), 
Nama_Penerbit VARCHAR(50),
Status ENUM('Available', 'Borrowed') DEFAULT 'Available');

CREATE TABLE Rak
(Kode_Rak VARCHAR(10) PRIMARY KEY, 
Genre Varchar(30));

CREATE TABLE Peminjaman
(ID_Petugas VARCHAR(10), 
FOREIGN KEY (ID_Petugas) REFERENCES Petugas(ID_Petugas), 
ID_Anggota VARCHAR(10), 
FOREIGN KEY (ID_Anggota) REFERENCES Anggota(ID_Anggota), 
ID_Buku VARCHAR(10), 
FOREIGN KEY (ID_Buku) REFERENCES Buku(ID_Buku), 
ID_Peminjaman VARCHAR(10) PRIMARY KEY, 
Tgl_Pinjam DATE, 
Tenggat_Kembali DATE);

CREATE TABLE Pengembalian
(ID_Petugas VARCHAR(10), 
FOREIGN KEY (ID_Petugas) REFERENCES Petugas(ID_Petugas), 
ID_Anggota VARCHAR(10), 
FOREIGN KEY (ID_Anggota) REFERENCES Anggota(ID_Anggota), 
ID_Buku VARCHAR(10), 
FOREIGN KEY (ID_Buku) REFERENCES Buku(ID_Buku), 
ID_Pengembalian VARCHAR(10) PRIMARY KEY, 
Tgl_Pengembalian DATE, 
Denda INT);

CREATE TABLE Menyimpan
(ID_Buku VARCHAR(10) NOT NULL, 
FOREIGN KEY (ID_Buku) REFERENCES Buku(ID_Buku), 
Kode_Rak VARCHAR(10) NOT NULL, 
FOREIGN KEY (Kode_Rak) REFERENCES Rak(Kode_Rak));

SHOW TABLES; # Memunculkan apa saja tabel yang ada di Perpustakaan