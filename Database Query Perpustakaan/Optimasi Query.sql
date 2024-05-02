-- Membuat indeks pada kolom Judul dan Nama_Penulis tabel Buku untuk meningkatkan pencarian berdasarkan judul atau penulis.
CREATE INDEX index_buku_judul ON Buku(Judul);
CREATE INDEX index_buku_penulis ON Buku(Nama_Penulis);

-- Membuat indeks pada kolom Genre tabel Rak untuk meningkatkan pencarian berdasarkan genre.
CREATE INDEX index_rak_genre ON Rak(Genre);

-- Membuat indeks pada kolom Nama_Anggota tabel Anggota untuk meningkatkan pencarian berdasarkan nama anggota.
CREATE INDEX index_anggota_nama ON Anggota(Nama_Anggota);

-- Membuat indeks pada kolom Tgl_Pinjam tabel Peminjaman untuk meningkatkan pencarian berdasarkan tanggal peminjaman.
CREATE INDEX index_pinjam_tgl_pinjam ON Peminjaman(Tgl_Pinjam);

-- Membuat indeks pada kolom Tgl_Pengembalian tabel Pengembalian untuk meningkatkan pencarian berdasarkan tanggal pengembalian.
CREATE INDEX index_kembali_tgl_kembali ON Pengembalian(Tgl_Pengembalian);

-- Mengambil informasi tentang semua buku beserta informasi rak tempat mereka disimpan, diurutkan berdasarkan ID Buku.
SELECT b.ID_Buku, b.Judul, r.Genre, b.Tahun_Terbit, b.Nama_Penulis, s.Kode_Rak AS Rak, b.Status
FROM Buku b
JOIN Menyimpan s ON b.ID_Buku = s.ID_Buku
JOIN Rak r ON s.Kode_Rak = r.Kode_Rak
ORDER BY ID_Buku;

-- Mencari buku berdasarkan judul, nama penulis, atau genre yang sesuai dengan kueri yang diberikan, diurutkan berdasarkan ID Buku.
SELECT b.ID_Buku, b.Judul, r.Genre, b.Tahun_Terbit, b.Nama_Penulis, s.Kode_Rak AS Rak, b.Status
FROM Buku b
JOIN Menyimpan s ON b.ID_Buku = s.ID_Buku
JOIN Rak r ON s.Kode_Rak = r.Kode_Rak
WHERE b.Judul LIKE '%{query}%' OR b.Nama_Penulis LIKE '%{query}%' OR r.Genre LIKE '%{query}%'
ORDER BY b.ID_Buku;

-- Mengambil informasi tentang semua peminjaman beserta informasi petugas, anggota, dan buku yang dipinjam, diurutkan berdasarkan ID Peminjaman.
SELECT pem.ID_Peminjaman, pem.ID_Petugas, p.Nama_Petugas, pem.ID_Anggota, a.Nama_Anggota, pem.ID_Buku, b.Judul, pem.Tgl_Pinjam, pem.Tenggat_Kembali
FROM Peminjaman pem
JOIN Petugas p ON pem.ID_Petugas = p.ID_Petugas
JOIN Anggota a ON pem.ID_Anggota = a.ID_Anggota
JOIN Buku b ON pem.ID_Buku = b.ID_Buku
ORDER BY ID_Peminjaman;

-- Mencari data peminjaman berdasarkan nama anggota, judul buku, atau tanggal pinjam yang sesuai dengan kueri yang diberikan, diurutkan berdasarkan ID Peminjaman.
SELECT pem.ID_Peminjaman, pem.ID_Petugas, p.Nama_Petugas, pem.ID_Anggota, a.Nama_Anggota, pem.ID_Buku, b.Judul, pem.Tgl_Pinjam, pem.Tenggat_Kembali
FROM Peminjaman pem
JOIN Petugas p ON pem.ID_Petugas = p.ID_Petugas
JOIN Anggota a ON pem.ID_Anggota = a.ID_Anggota
JOIN Buku b ON pem.ID_Buku = b.ID_Buku
WHERE a.Nama_Anggota LIKE '%{query}%' OR b.Judul LIKE '%{query}%' OR pem.Tgl_Pinjam LIKE '%{query}%'
ORDER BY ID_Peminjaman;      

-- Mengambil informasi tentang semua pengembalian beserta informasi petugas, anggota, dan buku yang dikembalikan, diurutkan berdasarkan ID Pengembalian.
SELECT peng.ID_Pengembalian, peng.ID_Petugas, p.Nama_Petugas, peng.ID_Anggota, a.Nama_Anggota, peng.ID_Buku, b.Judul, peng.Tgl_Pengembalian, peng.Denda
FROM Pengembalian peng
JOIN Petugas p ON peng.ID_Petugas = p.ID_Petugas
JOIN Anggota a ON peng.ID_Anggota = a.ID_Anggota
JOIN Buku b ON pem.ID_Buku = b.ID_Buku
ORDER BY ID_Pengembalian;

-- Mencari data pengembalian berdasarkan nama anggota, judul buku, atau tanggal pengembalian yang sesuai dengan kueri yang diberikan, diurutkan berdasarkan ID Pengembalian.
SELECT peng.ID_Pengembalian, peng.ID_Petugas, p.Nama_Petugas, peng.ID_Anggota, a.Nama_Anggota, peng.ID_Buku, b.Judul, peng.Tgl_Pengembalian, peng.Denda
FROM Pengembalian peng
JOIN Petugas p ON peng.ID_Petugas = p.ID_Petugas
JOIN Anggota a ON peng.ID_Anggota = a.ID_Anggota
JOIN Buku b ON peng.ID_Buku = b.ID_Buku
WHERE a.Nama_Anggota LIKE '%{query}%' OR b.Judul LIKE '%{query}%' OR peng.Tgl_Pengembalian LIKE '%{query}%'
ORDER BY ID_Pengembalian;