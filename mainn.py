from tkinter import *
from user_authh import initialize_user_data_file, open_login_window

if __name__ == "__main__":
    # Inisialisasi data pengguna
    initialize_user_data_file()

    # Membuka jendela login utama
    open_login_window()