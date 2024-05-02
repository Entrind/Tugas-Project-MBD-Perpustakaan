USE Perpustakaan;

# Aljabar Relasional pada Database

# 1. SELECTION (Memilih Baris)
SELECT * FROM Pengembalian Where Denda > 0;

# 2. PROJECTION (Meilih Kolom)
SELECT Judul, Nama_Penulis, Nama_Penerbit FROM Buku;

# 3. UNION (Penggabungan)
SELECT ID_Anggota AS ID, Nama_Anggota AS Nama, Kontak_Anggota AS Kontak, Alamat_Anggota AS Alamat FROM Anggota
UNION
SELECT ID_Petugas AS ID, Nama_Petugas AS Nama, Kontak_Petugas AS Kontak, Alamat_Petugas AS Alamat FROM Petugas;

# 4. CARTESIAN PRODUCT (Perkalian)
SELECT * FROM Anggota CROSS JOIN (SELECT ID_Petugas, Nama_Petugas FROM Petugas) AS Petugas;

# 5. INTERSECTION (Perpotongan)
SELECT * FROM Buku INNER JOIN Pengembalian ON Buku.ID_Buku = Pengembalian.ID_Buku;

# 6. DIFFERENCE (Perbedaan)
SELECT ID_Buku FROM Buku WHERE ID_Buku NOT IN (SELECT ID_Buku FROM Peminjaman);