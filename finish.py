import csv
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Nama file untuk data pengguna dan peralatan
USER_DATA_FILE = 'users.csv'
PERALATAN_FILE = 'Peralatan.csv'

# Variabel global untuk menyimpan keranjang belanja
shopping_cart = []
base_image_path = "D:/Kelompok-6-Kelas-C/Gambar Peralatan"  # Ganti dengan path folder yang sesuai

# Membuat file CSV jika belum ada
def initialize_user_data_file():
    try:
        with open(USER_DATA_FILE, 'x') as file:
            writer = csv.writer(file)
            writer.writerow(['email', 'password'])  # Header file CSV
    except FileExistsError:
        pass

# Fungsi untuk memeriksa apakah email sudah terdaftar
def is_email_registered(email):
    with open(USER_DATA_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['email'] == email:
                return True
    return False

# Fungsi untuk menambahkan pengguna baru ke file
def register_user(email, password):
    if is_email_registered(email):
        return False
    with open(USER_DATA_FILE, 'a') as file:
        writer = csv.writer(file)
        writer.writerow([email, password])
    return True

# Fungsi untuk autentikasi pengguna
def authenticate_user(email, password):
    with open(USER_DATA_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['email'] == email and row['password'] == password:
                return True
    return False

# Fungsi untuk membaca data dari file CSV
def load_data_from_csv(file_path):
    try:
        with open(file_path, mode="r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            return [row for row in reader]
    except FileNotFoundError:
        messagebox.showerror("Error", f"File {file_path} tidak ditemukan.")
        return []

# Fungsi untuk menampilkan menu kategori
def start_purchase():
    data = load_data_from_csv(PERALATAN_FILE)
    if not data:
        messagebox.showerror("Error", "Data peralatan tidak ditemukan.")
        return

    category_window = Toplevel()
    category_window.title("Pilih Kategori Olahraga")
    category_window.state("zoomed")  # Membuat jendela fullscreen

    # Load background image
    try:
        bg_image_path = "D:/Kelompok-6-Kelas-C/bg5.png"  # Path gambar latar belakang
        bg_image = Image.open(bg_image_path)
        bg_image = bg_image.resize((category_window.winfo_screenwidth(), category_window.winfo_screenheight()), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
    except Exception as e:
        messagebox.showerror("Error", f"Error memuat gambar latar belakang: {str(e)}")
        category_window.destroy()
        return

    # Tambahkan Canvas sebagai background
    canvas = Canvas(category_window, width=category_window.winfo_screenwidth(), height=category_window.winfo_screenheight())
    canvas.pack(fill=BOTH, expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor=NW)

    # Tambahkan frame untuk komponen
    frame = Frame(category_window, width=500, height=300, bg="#FFFFFF", bd=2, relief="ridge")
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Judul dan menu kategori
    Label(frame, text="Pilih Kategori Olahraga:", font=("Arial", 14), bg="#FFFFFF").pack(pady=10)
    categories = list(set(row[0] for row in data))
    category_var = StringVar(value="Pilih Kategori")
    category_menu = ttk.Combobox(frame, textvariable=category_var, values=categories, state="readonly", font=("Arial", 12))
    category_menu.pack(pady=5)

    # Fungsi untuk membuka menu peralatan
    def open_selected_category():
        selected_category = category_var.get()
        if selected_category == "Pilih Kategori":
            messagebox.showerror("Error", "Pilih kategori terlebih dahulu.")
            return
        category_window.destroy()
        open_equipment_menu(selected_category, data)

    # Tombol Lanjutkan
    Button(frame, text="Lanjutkan", font=("Arial", 12), command=open_selected_category, bg="#FFA500", fg="white").pack(pady=10)

    # Simpan referensi gambar agar tidak dihapus
    category_window.bg_photo = bg_photo

# Fungsi untuk menampilkan perlengkapan berdasarkan kategori
def open_equipment_menu(selected_category, data):
    equipment_window = Toplevel()
    equipment_window.title(f"Perlengkapan {selected_category}")
    equipment_window.state("zoomed")  # Membuat jendela fullscreen

    # Load background image
    try:
        bg_image_path = "D:/Kelompok-6-Kelas-C/bg4.png"  # Path gambar latar belakang
        bg_image = Image.open(bg_image_path)
        bg_image = bg_image.resize((equipment_window.winfo_screenwidth(), equipment_window.winfo_screenheight()), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
    except Exception as e:
        messagebox.showerror("Error", f"Error memuat gambar latar belakang: {str(e)}")
        equipment_window.destroy()
        return

    # Tambahkan Canvas sebagai background
    canvas = Canvas(equipment_window, width=equipment_window.winfo_screenwidth(), height=equipment_window.winfo_screenheight())
    canvas.pack(fill=BOTH, expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor=NW)

    # Filter data berdasarkan kategori
    filtered_data = [row for row in data if row[0] == selected_category]

    if not filtered_data:
        messagebox.showinfo("Info", f"Tidak ada perlengkapan di kategori {selected_category}.")
        equipment_window.destroy()
        return

    # Frame utama untuk daftar barang
    frame = Frame(equipment_window, bg="#FFFFFF", bd=2, relief="ridge")
    frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=800, height=600)

    # Canvas dan Scrollbar untuk daftar barang
    scroll_canvas = Canvas(frame, bg="#FFFFFF")
    scrollbar = Scrollbar(frame, orient=VERTICAL, command=scroll_canvas.yview)
    scrollable_frame = Frame(scroll_canvas, bg="#FFFFFF")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
    )

    scroll_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Menambahkan daftar barang
    for item in filtered_data:
        equipment_frame = Frame(scrollable_frame, bg="#F9F9F9", bd=2, relief=SOLID, padx=5, pady=5)
        equipment_frame.pack(fill=X, padx=10, pady=5)

        try:
            image_path = os.path.join(base_image_path, item[2])  # Path gambar barang
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"File '{image_path}' tidak ditemukan.")
            image = Image.open(image_path)
            image = image.resize((100, 100), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            img_label = Label(equipment_frame, image=photo, bg="#F9F9F9")
            img_label.image = photo
            img_label.pack(side=LEFT, padx=10)
        except Exception as e:
            Label(equipment_frame, text=f"(Gambar Tidak Tersedia: {str(e)})", fg="red", bg="#F9F9F9").pack(side=LEFT, padx=10)

        # Informasi barang
        info = f"Nama: {item[1]}\nStok: {item[3]} pcs\nHarga: Rp {item[4]}"
        Label(equipment_frame, text=info, font=("Arial", 12), justify=LEFT, bg="#F9F9F9").pack(side=LEFT, padx=10)

        Button(equipment_frame, text="Tambah ke Keranjang", command=lambda i=item: prompt_quantity(i), bg="#FFA500", fg="white").pack(side=RIGHT, padx=10)

    # Simpan referensi gambar agar tidak dihapus
    equipment_window.bg_photo = bg_photo

    equipment_window.mainloop()

def prompt_quantity(item):
    quantity_window = Toplevel()
    quantity_window.title("Masukkan Jumlah")
    quantity_window.state("zoomed")  # Membuat jendela fullscreen

    # Load background image
    try:
        bg_image_path = "D:/Kelompok-6-Kelas-C/bg9.png"  # Path gambar latar belakang
        bg_image = Image.open(bg_image_path)
        bg_image = bg_image.resize((quantity_window.winfo_screenwidth(), quantity_window.winfo_screenheight()), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
    except Exception as e:
        messagebox.showerror("Error", f"Error memuat gambar latar belakang: {str(e)}")
        quantity_window.destroy()
        return

    # Tambahkan Canvas sebagai background
    canvas = Canvas(quantity_window, width=quantity_window.winfo_screenwidth(), height=quantity_window.winfo_screenheight())
    canvas.pack(fill=BOTH, expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor=NW)

    # Tambahkan frame untuk input jumlah
    frame = Frame(quantity_window, width=400, height=200, bg="#FFFFFF", bd=2, relief="ridge")
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    Label(frame, text=f"Masukkan jumlah untuk {item[1]}", font=("Arial", 14), bg="#FFFFFF", fg="#333333").pack(pady=10)

    quantity_entry = Entry(frame, font=("Arial", 12), justify="center")
    quantity_entry.pack(pady=10)

    def add_to_cart_with_quantity():
        quantity = quantity_entry.get()
        try:
            quantity = int(quantity)
            # Validasi stok
            if quantity <= 0:
                raise ValueError("Jumlah harus lebih besar dari 0.")
            if quantity > int(item[3]):  # Bandingkan dengan stok yang tersedia
                raise ValueError(f"Jumlah yang dimasukkan melebihi stok. Stok tersedia: {item[3]} pcs.")
            item[3] = quantity
            shopping_cart.append(item)
            messagebox.showinfo("Sukses", f"{item[1]} berhasil ditambahkan ke keranjang.")
            quantity_window.destroy()
        except ValueError as ve:
            messagebox.showerror("Error", f"Input tidak valid: {str(ve)}")

    Button(frame, text="Tambahkan ke Keranjang", font=("Arial", 12), bg="#FFA500", fg="white", command=add_to_cart_with_quantity).pack(pady=10)

    # Simpan referensi gambar agar tidak dihapus
    quantity_window.bg_photo = bg_photo

def checkout():
    if not shopping_cart:
        messagebox.showinfo("Info", "Keranjang belanja Anda kosong.")
        return

    checkout_window = Toplevel()
    checkout_window.title("Checkout")
    checkout_window.state("zoomed")  # Membuat jendela fullscreen
    
    # Load background image
    try:
        bg_image_path = "D:/Kelompok-6-Kelas-C/bg8.png"  # Path gambar latar belakang
        bg_image = Image.open(bg_image_path)
        bg_image = bg_image.resize((checkout_window.winfo_screenwidth(), checkout_window.winfo_screenheight()), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
    except Exception as e:
        messagebox.showerror("Error", f"Error memuat gambar latar belakang: {str(e)}")
        checkout_window.destroy()
        return

    # Tambahkan Canvas sebagai background
    canvas = Canvas(checkout_window, width=checkout_window.winfo_screenwidth(), height=checkout_window.winfo_screenheight())
    canvas.pack(fill=BOTH, expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor=NW)

    # Tambahkan frame untuk keranjang belanja
    frame = Frame(checkout_window, width=500, height=400, bg="#FFFFFF", bd=2, relief="ridge")
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    Label(frame, text="Keranjang Belanja:", font=("Arial", 14, "bold"), bg="#FFFFFF", fg="#333333").pack(pady=10)

    total_price = 0
    for idx, item in enumerate(shopping_cart, start=1):
        item_price = int(item[4])  # Ambil harga dari kolom harga
        total_item_price = item_price * item[3]  # Menghitung total harga per item
        Label(frame, text=f"{idx}. {item[1]} ({item[0]}): {item[3]} pcs - Rp {total_item_price}", font=("Arial", 12), bg="#FFFFFF", fg="#333333").pack(anchor="w")
        total_price += total_item_price  # Menambahkan harga total ke total keseluruhan

    Label(frame, text=f"Total Harga: Rp {total_price}", font=("Arial", 14), fg="green", bg="#FFFFFF").pack(pady=10)

    # Tombol untuk memilih metode pembayaran
    Button(frame, text="Pilih Metode Pembayaran", font=("Arial", 12), bg="#FFA500", fg="white", command=lambda: open_payment_method(total_price)).pack(pady=10)

    # Simpan referensi gambar agar tidak dihapus
    checkout_window.bg_photo = bg_photo

def open_payment_method(total_price):
    payment_window = Toplevel()
    payment_window.title("Pilih Metode Pembayaran")
    payment_window.state("zoomed")  # Membuat jendela fullscreen
    
    # Load background image
    try:
        bg_image_path = "D:/Kelompok-6-Kelas-C/bgg7.png"  # Path gambar latar belakang
        bg_image = Image.open(bg_image_path)
        bg_image = bg_image.resize((payment_window.winfo_screenwidth(), payment_window.winfo_screenheight()), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
    except Exception as e:
        messagebox.showerror("Error", f"Error memuat gambar latar belakang: {str(e)}")
        payment_window.destroy()
        return

    # Tambahkan Canvas sebagai background
    canvas = Canvas(payment_window, width=payment_window.winfo_screenwidth(), height=payment_window.winfo_screenheight())
    canvas.pack(fill=BOTH, expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor=NW)

    frame = Frame(payment_window)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)  # Menempatkan frame di tengah

    payment_methods = ["OVO", "DANA", "GoPay", "ShopeePay"]
    payment_var = StringVar(value="Pilih Metode Pembayaran")
    payment_menu = ttk.Combobox(frame, textvariable=payment_var, values=payment_methods, state="readonly", font=("Arial", 12))
    payment_menu.pack(pady=10)

    def confirm_payment():
        selected_method = payment_var.get()
        if selected_method == "Pilih Metode Pembayaran":
            messagebox.showerror("Error", "Pilih metode pembayaran terlebih dahulu.")
            return
        payment_window.destroy()
        show_receipt(selected_method, total_price)

    Button(frame, text="Konfirmasi Pembayaran", font=("Arial", 12), command=confirm_payment, bg="#FFA500", fg="white").pack(pady=10)
    
    # Simpan referensi gambar agar tidak dihapus
    payment_window.bg_photo = bg_photo

# Fungsi untuk menampilkan nota (struk)
def show_receipt(payment_method, total_price):
    receipt_window = Toplevel()
    receipt_window.title("Nota Pembelian")
    receipt_window.state("zoomed")  # Membuat jendela fullscreen
    
    # Load background image
    try:
        bg_image_path = "D:/Kelompok-6-Kelas-C/bg6.png"  # Path gambar latar belakang
        bg_image = Image.open(bg_image_path)
        bg_image = bg_image.resize((receipt_window.winfo_screenwidth(), receipt_window.winfo_screenheight()), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
    except Exception as e:
        messagebox.showerror("Error", f"Error memuat gambar latar belakang: {str(e)}")
        receipt_window.destroy()
        return

    # Tambahkan Canvas sebagai background
    canvas = Canvas(receipt_window, width=receipt_window.winfo_screenwidth(), height=receipt_window.winfo_screenheight())
    canvas.pack(fill=BOTH, expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor=NW)

    frame = Frame(receipt_window)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)  # Menempatkan frame di tengah

    Label(frame, text="Nota Pembelian", font=("Arial", 16), fg="green").pack(pady=10)
    Label(frame, text=f"Metode Pembayaran: {payment_method}", font=("Arial", 14)).pack(pady=5)
    Label(frame, text=f"Total Harga: Rp {total_price}", font=("Arial", 14), fg="green").pack(pady=5)

    Label(frame, text="Tolong transfer melalui nomor 088216425178 An Iskandar Rohman Syah", font=("Arial", 12)).pack(pady=10)
    Label(frame, text="Setelah itu kirim bukti pembayaran melalui no WhatsApp 083874021091", font=("Arial", 12)).pack(pady=10)
    Label(frame, text="Terima kasih telah berbelanja!", font=("Arial", 14)).pack(pady=10)

    Button(frame, text="Tutup", font=("Arial", 12), command=receipt_window.destroy, bg="#FFA500", fg="white").pack(pady=10)
    
    # Simpan referensi gambar agar tidak dihapus
    receipt_window.bg_photo = bg_photo

def open_login_window():
    login_window = Tk()
    login_window.title("Login Sistem")
    login_window.state("zoomed")  # Membuat jendela fullscreen

    # Load background image
    try:
        bg_image_path = "D:/Kelompok-6-Kelas-C/background.png"  # Ganti dengan path file Anda
        bg_image = Image.open(bg_image_path)
        bg_image = bg_image.resize((login_window.winfo_screenwidth(), login_window.winfo_screenheight()), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
    except Exception as e:
        messagebox.showerror("Error", f"Error memuat gambar latar belakang: {str(e)}")
        return
    
    # Tambahkan Canvas sebagai background
    canvas = Canvas(login_window, width=login_window.winfo_screenwidth(), height=login_window.winfo_screenheight())
    canvas.pack(fill=BOTH, expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor=NW)

    # Load gambar biru.png untuk frame
    try:
        frame_bg_path = "D:/Kelompok-6-Kelas-C/biru.png"  # Path gambar untuk frame
        frame_bg_image = Image.open(frame_bg_path)
        frame_bg_image = frame_bg_image.resize((400, 300), Image.Resampling.LANCZOS)  # Resize sesuai ukuran frame
        frame_bg_photo = ImageTk.PhotoImage(frame_bg_image)
    except Exception as e:
        messagebox.showerror("Error", f"Error memuat gambar latar belakang frame: {str(e)}")
        return

    # Tambahkan frame untuk komponen login
    frame = Frame(login_window, width=400, height=300, bd=2, relief="ridge")
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)  # Tempatkan di tengah

    # Tambahkan Label untuk gambar latar belakang frame
    bg_label = Label(frame, image=frame_bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Pastikan gambar memenuhi frame

    # Tambahkan komponen di atas frame
    Label(frame, text="Selamat Datang di Sixma Sports Official", font=("Arial", 16), fg="white", bg="#A9A9A9").place(relx=0.5, rely=0.1, anchor=CENTER)
    Label(frame, text="Sing In", font=("Arial", 16), fg="white", bg="#A9A9A9").place(relx=0.5, rely=0.25, anchor=CENTER)
    Label(frame, text="Email:", font=("Arial", 12), bg="#A9A9A9").place(relx=0.04, rely=0.4, anchor=W)

    email_entry = Entry(frame, font=("Arial", 12))
    email_entry.place(relx=0.5, rely=0.4, anchor=CENTER)

    Label(frame, text="Password:", font=("Arial", 12), bg="#A9A9A9").place(relx=0.04, rely=0.6, anchor=W)
    password_entry = Entry(frame, font=("Arial", 12), show="*")
    password_entry.place(relx=0.5, rely=0.6, anchor=CENTER)
    
    # Frame untuk password dan tombol mata
    password_frame = Frame(frame, bg="#ffffff")
    password_frame.place(relx=0.54, rely=0.6, anchor=CENTER)

    password_entry = Entry(password_frame, font=("Arial", 12), show="*", width=20)
    password_entry.pack(side="left", padx=0)

    # Gambar tombol mata
    try:
        eye_open_img = PhotoImage(file="D:/Kelompok-6-Kelas-C/eye_open_image.png").subsample(3, 3)
        eye_closed_img = PhotoImage(file="D:/Kelompok-6-Kelas-C/eye_closed_image.png").subsample(3, 3)
    except Exception as e:
        messagebox.showerror("Error", f"Error memuat gambar tombol mata: {str(e)}")
        return

    # Fungsi toggle visibility password
    def toggle_password_visibility():
        if password_entry.cget('show') == '*':
            password_entry.config(show='')
            eye_button.config(image=eye_open_img)
        else:
            password_entry.config(show='*')
            eye_button.config(image=eye_closed_img)

    # Tombol mata untuk toggle password
    eye_button = Button(password_frame, image=eye_closed_img, command=toggle_password_visibility, bd=0)
    eye_button.pack(side="left")


    # Tombol Login
    login_button = Button(frame, text="Login", command=lambda: show_main_menu(email_entry.get(), password_entry.get(), login_window), bg="#FFA500", fg="white")
    login_button.place(relx=0.5, rely=0.75, anchor=CENTER)
    
    # Tombol Daftar
    daftar_button = Button(frame, text="Daftar", command=lambda: open_register_window(login_window), bg="#FFA500", fg="white")
    daftar_button.place(relx=0.5, rely=0.9, anchor=CENTER)

    # Simpan referensi gambar agar tidak dihapus
    frame.bg_photo = frame_bg_photo
    login_window.bg_photo = bg_photo

    login_window.mainloop()

def open_register_window(parent_window):
    register_window = Toplevel(parent_window)
    register_window.title("Daftar Akun Baru")
    register_window.state("zoomed")  # Membuat jendela fullscreen

    # Load background image
    try:
        bg_image_path = "D:/Kelompok-6-Kelas-C/background2.png"  # Ganti dengan path file Anda
        bg_image = Image.open(bg_image_path)
        bg_image = bg_image.resize((register_window.winfo_screenwidth(), register_window.winfo_screenheight()), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
    except Exception as e:
        messagebox.showerror("Error", f"Error memuat gambar latar belakang: {str(e)}")
        return

    # Tambahkan Canvas sebagai background
    canvas = Canvas(register_window, width=register_window.winfo_screenwidth(), height=register_window.winfo_screenheight())
    canvas.pack(fill=BOTH, expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor=NW)

    # Load gambar biru.png untuk frame
    try:
        frame_bg_path = "D:/Kelompok-6-Kelas-C/biru.png"  # Path gambar untuk frame
        frame_bg_image = Image.open(frame_bg_path)
        frame_bg_image = frame_bg_image.resize((400, 300), Image.Resampling.LANCZOS)  # Resize sesuai ukuran frame
        frame_bg_photo = ImageTk.PhotoImage(frame_bg_image)
    except Exception as e:
        messagebox.showerror("Error", f"Error memuat gambar latar belakang frame: {str(e)}")
        return

    # Tambahkan frame untuk komponen registrasi
    frame = Frame(register_window, width=400, height=300, bd=2, relief="ridge")
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)  # Tempatkan di tengah

    # Tambahkan Label untuk gambar latar belakang frame
    bg_label = Label(frame, image=frame_bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Pastikan gambar memenuhi frame

    # Tambahkan komponen di atas frame
    Label(frame, text="Daftar Akun Baru", font=("Arial", 16), bg="#A9A9A9", fg="white").place(relx=0.5, rely=0.1, anchor=CENTER)
    Label(frame, text="Email:", font=("Arial", 12), bg="#A9A9A9").place(relx=0.1, rely=0.3, anchor=W)
    
    email_entry = Entry(frame, font=("Arial", 12))
    email_entry.place(relx=0.5, rely=0.3, anchor=CENTER)

    Label(frame, text="Password:", font=("Arial", 12), bg="#A9A9A9").place(relx=0.044, rely=0.5, anchor=W)

    # Frame untuk password dan tombol mata
    password_frame = Frame(frame, bg="#ffffff")
    password_frame.place(relx=0.55, rely=0.5, anchor=CENTER)

    password_entry = Entry(password_frame, font=("Arial", 12), show="*", width=20)
    password_entry.pack(side="left", padx=0)

    # Gambar tombol mata
    try:
        eye_open_img = PhotoImage(file="D:/Kelompok-6-Kelas-C/eye_open_image.png").subsample(3, 3)
        eye_closed_img = PhotoImage(file="D:/Kelompok-6-Kelas-C/eye_closed_image.png").subsample(3, 3)
    except Exception as e:
        messagebox.showerror("Error", f"Error memuat gambar tombol mata: {str(e)}")
        return

    # Fungsi toggle visibility password
    def toggle_password_visibility():
        if password_entry.cget('show') == '*':
            password_entry.config(show='')
            eye_button.config(image=eye_open_img)
        else:
            password_entry.config(show='*')
            eye_button.config(image=eye_closed_img)

    # Tombol mata untuk toggle password
    eye_button = Button(password_frame, image=eye_closed_img, command=toggle_password_visibility, bd=0)
    eye_button.pack(side="left")

    # Tombol Daftar
    Button(frame, text="Daftar", font=("Arial", 12), command=lambda: register_user_action(email_entry, password_entry, register_window),bg="#FFA500", fg="white").place(relx=0.5, rely=0.8, anchor=CENTER)

    # Simpan referensi gambar agar tidak hilang
    register_window.bg_photo = bg_photo
    frame.bg_photo = frame_bg_photo

def register_user_action(email_entry, password_entry, register_window):
    email = email_entry.get()
    password = password_entry.get()

    if not email or not password:
        messagebox.showerror("Error", "Semua field harus diisi!")
        return

    if register_user(email, password):
        messagebox.showinfo("Sukses", "Akun berhasil didaftarkan!")
        register_window.destroy()
    else:
        messagebox.showerror("Error", "Email sudah terdaftar.")

def show_main_menu(email, password, login_window):
    if authenticate_user(email, password):
        messagebox.showinfo("Sukses", "Login berhasil!")
        login_window.destroy()

        main_menu = Tk()
        main_menu.title("Sixma Sport Official")
        main_menu.state("zoomed")  # Membuat jendela fullscreen
        
        # Load background image
        try:
            bg_image_path = "D:/Kelompok-6-Kelas-C/bg3.png"  # Path file latar belakang untuk menu utama
            bg_image = Image.open(bg_image_path)
            bg_image = bg_image.resize((main_menu.winfo_screenwidth(), main_menu.winfo_screenheight()), Image.Resampling.LANCZOS)
            bg_photo = ImageTk.PhotoImage(bg_image)
        except Exception as e:
            messagebox.showerror("Error", f"Error memuat gambar latar belakang: {str(e)}")
            return

        # Tambahkan Canvas sebagai background
        canvas = Canvas(main_menu, width=main_menu.winfo_screenwidth(), height=main_menu.winfo_screenheight())
        canvas.pack(fill=BOTH, expand=True)
        canvas.create_image(0, 0, image=bg_photo, anchor=NW)

        # Load gambar biru.png untuk frame
        try:
            frame_bg_path = "D:/Kelompok-6-Kelas-C/biru.png"  # Path gambar untuk frame
            frame_bg_image = Image.open(frame_bg_path)
            frame_bg_image = frame_bg_image.resize((500, 400), Image.Resampling.LANCZOS)  # Resize sesuai ukuran frame
            frame_bg_photo = ImageTk.PhotoImage(frame_bg_image)
        except Exception as e:
            messagebox.showerror("Error", f"Error memuat gambar latar belakang frame: {str(e)}")
            return

        # Tambahkan frame untuk komponen menu utama
        frame = Frame(main_menu, width=500, height=400, bd=2, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor=CENTER)  # Tempatkan di tengah

        # Tambahkan Label untuk gambar latar belakang frame
        bg_label = Label(frame, image=frame_bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Pastikan gambar memenuhi frame

        # Tambahkan komponen di atas frame
        Label(frame, text="Sixma Sports Official", font=("Arial", 20), bg="#A9A9A9", fg="white").place(relx=0.5, rely=0.2, anchor=CENTER)

        Button(frame, text="Mulai Membeli", font=("Arial", 14), command=start_purchase, bg="#FFA500", fg="white").place(relx=0.5, rely=0.5, anchor=CENTER)
        Button(frame, text="Lihat Keranjang", font=("Arial", 14), command=checkout, bg="#FFA500", fg="white").place(relx=0.5, rely=0.7, anchor=CENTER)

        # Simpan referensi gambar agar tidak dihapus
        main_menu.bg_photo = bg_photo
        frame.bg_photo = frame_bg_photo

        main_menu.mainloop()
    else:
        messagebox.showerror("Error", "Email atau password salah.")

if __name__ == "__main__":
    initialize_user_data_file()
    open_login_window()
