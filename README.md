# Tugas Project MBD Perpustakaan

## Kelompok 8: Sistem Manajemen Perpustakaan

- **D121221071 | Andika Arif Rahman**
- **D121221089 | Muhammad Rifqi**

## Deskripsi Proyek

Proyek ini bertujuan untuk membuat antarmuka grafis (GUI) menggunakan Python yang terintegrasi dengan database MySQL untuk sistem manajemen perpustakaan. Aplikasi ini memungkinkan pengguna untuk mengakses tabel-tabel dari database Perpustakaan, serta menyediakan fitur login untuk memisahkan peran admin (petugas perpustakaan) dengan pengguna umum.

## Fitur Program

1. **Mengakses Tabel Database Perpustakaan**:
    - Menampilkan data dari tabel yang ada dalam database Perpustakaan di MySQL.

2. **Login Page**:
    - Memisahkan peran admin (petugas perpustakaan) dengan pengguna umum.

3. **Search Function**:
    - Mencari buku pada halaman pencarian buku, peminjaman buku, dan pengembalian buku.

4. **Add Function**:
    - Menambah data peminjaman dan pengembalian buku ke dalam database.

5. **Delete Function**:
    - Menghapus data peminjaman dan pengembalian buku dari database.

## Struktur Proyek

Repositori ini terdiri dari tiga folder utama:

### 1. Folder Data Perpustakaan

Folder ini berisi data teks yang digunakan dalam database perpustakaan.

- `Anggota.txt`
- `Buku.txt`
- `Menyimpan.txt`
- `Peminjaman.txt`
- `Pengembalian.txt`
- `Petugas.txt`
- `Rak.txt`

### 2. Folder Database Query Perpustakaan

Folder ini berisi skrip SQL yang digunakan untuk membuat dan mengelola database perpustakaan.

- `Pembuatan Tabel Perpustakaan.sql`
- `Pengecekan Isi Tabel Perpustakaan.sql`
- `Pengisian Data Perpustakaan.sql`
- `Optimasi Query.sql`

### 3. Folder Project MBD - UI Perpustakaan

Folder ini berisi kode sumber untuk antarmuka pengguna perpustakaan yang dibuat dengan PyQt5.

- `Interface_Perpustakaan.py`
- `loginpage.py`
- `dialogs.py`

## Instalasi Library Python

### PyQt5

PyQt5 digunakan untuk membuat antarmuka grafis (GUI) pada aplikasi Python.

```sh
pip install PyQt5
```

### mysql.connector

mysql.connector digunakan untuk menghubungkan program Python dengan database MySQL.

```sh
pip install mysql-connector-python
```

## Inisialisasi Koneksi Database MySQL

Program ini hanya bisa berjalan jika sudah terkoneksi dengan host database MySQL yang digunakan. Berikut adalah segmen kode program yang digunakan untuk inisialisasi koneksi database MySQL:

```python
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
```

## Cara Menjalankan Program

1. **Pastikan MySQL server sudah berjalan dan database Perpustakaan sudah dibuat.**
2. **Install library PyQt5 dan mysql.connector sesuai dengan perintah di atas.**
3. **Jalankan program Python Anda yang telah terhubung dengan database MySQL.**

Program ini diharapkan dapat membantu dalam pengelolaan data perpustakaan, baik untuk admin maupun pengguna umum.

## Tampilan Antarmuka Pengguna

### Halaman Login
![image](https://github.com/Entrind/Tugas-Project-MBD-Perpustakaan/assets/140675316/17a3631c-3f22-4f5d-819b-da5616b5e338)

### Halaman Pencarian Buku
![image](https://github.com/Entrind/Tugas-Project-MBD-Perpustakaan/assets/140675316/3c12add4-397e-48d4-b7c4-fb631a315f15)

### Halaman Peminjaman Buku
![image](https://github.com/Entrind/Tugas-Project-MBD-Perpustakaan/assets/140675316/340c9128-8a0f-4ea8-b5f4-956142862c3e)

### Halaman Pengembalian Buku
![image](https://github.com/Entrind/Tugas-Project-MBD-Perpustakaan/assets/140675316/6a0ab0d0-7d2a-498a-a52e-5bfdeac964c8)

### Halaman Pencarian Buku (Guest)
![image](https://github.com/Entrind/Tugas-Project-MBD-Perpustakaan/assets/140675316/a6336514-73b1-44ee-9104-0335dd58e412)


## Catatan

Jika Anda mengalami masalah dalam menghubungkan program ke database MySQL, pastikan host, user, password, dan nama database sudah benar dan MySQL server dalam kondisi aktif.

---
