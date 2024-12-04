# Kelompok 6 Kelas C
# Anggota 
- Fami Wulan Devitasari (I0324115)
- Iskandar Rohman Syah (I0324116)
- Nashwa Cahayaning Atmono (I0324120)

# Tema : Sistem pembelian perlengkapan olahraga

# Deskripsi Ringkas
Program ini menyediakan daftar perlengkapan olahraga seperti bola voli, raket bulu tangkis, sepatu bulutangkis, sepatu voli, sepatu lari, bola basket, sepatu basket, shuttlecock, sepatu bola, sepatu futsal, bola futsal, dan bola sepak. Pengguna juga bisa memilih produk, jumlah yang dibeli, dan melihat total harga. Tambahan lainnya juga bisa berupa kategori olahraga untuk pembelian perlengkapan pada setiap kategorinya (seperti bulu tangkis, sepak bola, basket, voli, futsal, dan lari) dan informasi stoknya.

# Fitur-fitur 
Berikut adalah daftar fitur dari kode di atas untuk sistem pembelian perlengkapan olahraga:

---

### **📋 Fitur Sistem**

#### **1. Manajemen Akun**
- **Registrasi Pengguna Baru**:
  - Pengguna dapat mendaftarkan akun dengan email dan password.
  - Sistem memvalidasi email agar tidak terdaftar ganda.
- **Login Pengguna**:
  - Pengguna dapat masuk ke akun mereka menggunakan email dan password.
  - Sistem memverifikasi kombinasi email dan password.
- **Konfirmasi Password**:
  - Saat mendaftar, pengguna harus memasukkan password dua kali untuk memastikan kecocokan.

---

#### **2. Pengelolaan Peralatan Olahraga**
- **Kategori Peralatan**:
  - Produk dikategorikan berdasarkan jenis olahraga.
  - Contoh kategori: **Bulu tangkis**, **Sepak bola**, **Basket**, dll.
- **Daftar Peralatan**:
  - Menampilkan daftar produk berdasarkan kategori yang dipilih.
  - Menampilkan detail produk seperti nama, kategori, dan jumlah stok.

---

#### **3. Keranjang Belanja**
- **Menambahkan Produk**:
  - Pengguna dapat memilih produk dan jumlah yang ingin dibeli.
  - Sistem memvalidasi input pengguna untuk memastikan data valid.
- **Menampilkan Keranjang**:
  - Menampilkan daftar produk yang telah dipilih beserta jumlahnya.
  - Menghitung total item di keranjang belanja.

---

#### **4. Checkout**
- **Tinjauan Keranjang**:
  - Menampilkan isi keranjang belanja sebelum pengguna melanjutkan pembayaran.
- **Konfirmasi Pembelian**:
  - Pengguna dapat mengonfirmasi pesanan mereka sebelum melanjutkan ke metode pembayaran.

---

#### **5. Pembayaran**
- **Pilihan Metode Pembayaran**:
  - Menyediakan berbagai opsi pembayaran: **BCA**, **BNI**, **BRI**, **Mandiri**, **Gopay**, **Dana**, **OVO**, dan **ShopeePay**.
- **Instruksi Pembayaran**:
  - Menampilkan langkah-langkah pembayaran sesuai metode yang dipilih.
  - Informasi rekening tujuan dan kontak admin untuk konfirmasi pembayaran.

---

#### **6. User Interface (UI)**
- **Tampilan User-Friendly**:
  - Antarmuka berbasis *GUI* menggunakan Tkinter.
  - Elemen seperti menu dropdown, input form, dan tombol navigasi memudahkan interaksi.
- **Pesan Pop-Up**:
  - Memberikan umpan balik kepada pengguna (misalnya, pendaftaran berhasil, produk ditambahkan ke keranjang).

---

#### **7. Validasi Input**
- Validasi email saat registrasi untuk memastikan unik.
- Validasi jumlah pembelian untuk mencegah input non-numerik.

---

#### **8. Data Persistence**
- **Pengelolaan Data Pengguna**:
  - Informasi pengguna disimpan dalam file `users.csv`.
- **Pengelolaan Data Produk**:
  - Data produk diambil dari file `Peralatan.csv`.

---
