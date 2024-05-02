# Pengaturan
SET GLOBAL local_infile=1; # Agar bisa memasukkan data dari file lokal
SET SQL_SAFE_UPDATES = 0; # Agar bisa melakukan update yang tidak aman (delete, dll)

USE Perpustakaan;

# Menghapus isi tabel agar tidak terduplikasi
DELETE FROM Petugas;
DELETE FROM Anggota;
DELETE FROM Buku;
DELETE FROM Rak;
DELETE FROM Peminjaman;
DELETE FROM Pengembalian;
DELETE FROM Menyimpan;

# Memasukkan data dari file lokal
LOAD DATA LOCAL INFILE 'C:/Users/dikaa/OneDrive/Documents/Perpustakaan/Petugas.txt' INTO TABLE Petugas LINES TERMINATED BY '\r\n';
LOAD DATA LOCAL INFILE 'C:/Users/dikaa/OneDrive/Documents/Perpustakaan/Anggota.txt' INTO TABLE Anggota LINES TERMINATED BY '\r\n';
LOAD DATA LOCAL INFILE 'C:/Users/dikaa/OneDrive/Documents/Perpustakaan/Buku.txt' INTO TABLE Buku LINES TERMINATED BY '\r\n';
LOAD DATA LOCAL INFILE 'C:/Users/dikaa/OneDrive/Documents/Perpustakaan/Rak.txt' INTO TABLE Rak LINES TERMINATED BY '\r\n';
LOAD DATA LOCAL INFILE 'C:/Users/dikaa/OneDrive/Documents/Perpustakaan/Peminjaman.txt' INTO TABLE Peminjaman LINES TERMINATED BY '\r\n';
LOAD DATA LOCAL INFILE 'C:/Users/dikaa/OneDrive/Documents/Perpustakaan/Pengembalian.txt' INTO TABLE Pengembalian LINES TERMINATED BY '\r\n';
LOAD DATA LOCAL INFILE 'C:/Users/dikaa/OneDrive/Documents/Perpustakaan/Menyimpan.txt' INTO TABLE Menyimpan LINES TERMINATED BY '\r\n';

-- Update status buku dan password_akun petugas yang tidak ada pada file data pertama
UPDATE Buku
SET Status = 'Available'
WHERE Status = '';

UPDATE Petugas
SET Password_Akun = 'passadmin'
WHERE Password_Akun = '';