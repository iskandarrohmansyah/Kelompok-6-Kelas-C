import csv
import os
from shopping_module import start_purchase, checkout  # Pindahkan impor ke atas
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from data_utils import is_email_registered, register_user, authenticate_user
from tkinter import Toplevel, Canvas, Label, Frame, Button, messagebox
from PIL import Image, ImageTk

USER_DATA_FILE = 'users.csv'

def initialize_user_data_file():
    try:
        with open(USER_DATA_FILE, 'x') as file:
            writer = csv.writer(file)
            writer.writerow(['email', 'password'])  # Header file CSV
    except FileExistsError:
        pass

def open_login_window():
    login_window = Tk()
    login_window.title("Login Sistem")
    login_window.state("zoomed")  # Membuat jendela fullscreen

    # Load background image
    try:
        bg_image_path = "D:/Kelompok-6-Kelas-C/images/background.png"  # Ganti dengan path file Anda
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
        frame_bg_path = "D:/Kelompok-6-Kelas-C/images/biru.png"  # Path gambar untuk frame
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
        eye_open_img = PhotoImage(file="D:/Kelompok-6-Kelas-C/images/eye_open_image.png").subsample(3, 3)
        eye_closed_img = PhotoImage(file="D:/Kelompok-6-Kelas-C/images/eye_closed_image.png").subsample(3, 3)
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
        bg_image_path = "D:/Kelompok-6-Kelas-C/images/background2.png"  # Ganti dengan path file Anda
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
        frame_bg_path = "D:/Kelompok-6-Kelas-C/images/biru.png"  # Path gambar untuk frame
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
        eye_open_img = PhotoImage(file="D:/Kelompok-6-Kelas-C/images/eye_open_image.png").subsample(3, 3)
        eye_closed_img = PhotoImage(file="D:/Kelompok-6-Kelas-C/images/eye_closed_image.png").subsample(3, 3)
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
            bg_image_path = "D:/Kelompok-6-Kelas-C/images/bg3.png"  # Path file latar belakang untuk menu utama
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
            frame_bg_path = "D:/Kelompok-6-Kelas-C/images/biru.png"  # Path gambar untuk frame
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
