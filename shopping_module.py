from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
import csv
from PIL import Image, ImageTk
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

PERALATAN_FILE = 'Peralatan.csv'
shopping_cart = []
base_image_path = "D:/Kelompok-6-Kelas-C/Gambar Peralatan"  # Ganti dengan path folder yang sesuai

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
        bg_image_path = "D:/Kelompok-6-Kelas-C/images/bg5.png"  # Path gambar latar belakang
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
        bg_image_path = "D:/Kelompok-6-Kelas-C/images/bg4.png"  # Path gambar latar belakang
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
        bg_image_path = "D:/Kelompok-6-Kelas-C/images/bg9.png"  # Path gambar latar belakang
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
        bg_image_path = "D:/Kelompok-6-Kelas-C/images/bg8.png"  # Path gambar latar belakang
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
        bg_image_path = "D:/Kelompok-6-Kelas-C/images/bgg7.png"  # Path gambar latar belakang
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
    
def show_receipt(payment_method, total_price):
    receipt_window = Toplevel()
    receipt_window.title("Nota Pembelian")
    receipt_window.state("zoomed")  # Membuat jendela fullscreen
    
    # Load background image
    try:
        bg_image_path = "D:/Kelompok-6-Kelas-C/images/bg6.png"  # Path gambar latar belakang
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

# # Fungsi untuk membaca email pengguna yang sedang login dari CSV
# def get_user_email(email):
#     USER_DATA_FILE = 'users.csv'

#     try:
#         with open(USER_DATA_FILE, 'r') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 if row['email'] == email:
#                     return row['email']
#         return None
#     except FileNotFoundError:
#         messagebox.showerror("Error", "File users.csv tidak ditemukan.")
#         return None

# # Fungsi untuk mengirim email konfirmasi pesanan
# def send_order_confirmation_email(user_email, payment_method):
#     sender_email = "6masports@gmail.com"  # Ganti dengan email pengirim
#     password = "sixmaskibidi"  # Ganti dengan password aplikasi email

#     subject = "Konfirmasi Pembelian"
#     body = f"Terima kasih telah berbelanja! Metode Pembayaran: {payment_method}. Kami akan segera memproses pesanan Anda."

#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = user_email
#     msg['Subject'] = subject
#     msg.attach(MIMEText(body, 'plain'))

#     try:
#         with smtplib.SMTP('smtp.example.com', 587) as server:  # Ganti dengan server SMTP yang sesuai
#             server.starttls()
#             server.login(sender_email, password)
#             server.sendmail(sender_email, user_email, msg.as_string())
#         messagebox.showinfo("Sukses", "Email konfirmasi telah dikirim.")
#     except Exception as e:
#         messagebox.showerror("Error", f"Gagal mengirim email: {e}")