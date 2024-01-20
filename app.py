import os
import customtkinter
import configparser
import minecraft_launcher_lib
import uuid
import threading
import sys
import base64
import requests
from zipfile import ZipFile
from PIL import Image
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import Label
from subprocess import call
from cryptography.fernet import Fernet
import base64

code = b"""
#Game variables
config = configparser.ConfigParser()
config_file = config.read('config.ini')
java_path = "jdk17/bin/javaw"
version = "fabric-loader-0.15.6-1.20.1"
game_files = "game_data.zip"
minecraft_directory = ".originmc"


#Functions
def disable_ui():
    play_button.configure(state="disabled", fg_color = "#161616", image=None)
    settings_button.configure(state="disabled", fg_color = "#161616", image=None)
    close_button.configure(state="disabled", fg_color = "#161616", image=None)
    progressbar = customtkinter.CTkProgressBar(app, orientation="horizontal", width = 380, indeterminate_speed=2, progress_color="#ff6600")
    progressbar.configure(mode="indeterminate")
    progressbar.place(y=550, x=450)
    progressbar.start()
    info_txt = customtkinter.CTkLabel(app, text="Downloading files, this can take a long time...", font=("Helvetica", 14, "bold"), width=380, height=2)
    info_txt.configure(fg_color="#161616")
    info_txt.place(y=565, x=450)

def settings():
    dialog = customtkinter.CTkInputDialog(text=("Choose a new nickname:"), title="Preferences", button_fg_color="#ff6600", button_hover_color="#904a00", fg_color="#191919")
    new_nick = dialog.get_input()
    try:
        if new_nick != "":
            config['SETTINGS'] = {
            'nickname': new_nick,}
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
    except TypeError:
        print("//ERROR//")

def download_files():
    print("//DOWNLOADING FILES//")
    url = "https://www.dropbox.com/scl/fi/8gtsofphw6hxneook41yd/game_data.zip?rlkey=x9l6cpqsmcygf4hftvouko2wi&dl=1"
    r = requests.get(url, allow_redirects=True)
    with open(game_files, 'wb') as f:
        f.write(r.content)
    checkfiles()

def checkfiles():
    if os.path.isfile(game_files):
        with ZipFile(game_files, 'r') as zip: 
            zip.printdir() 
            print('//EXTRACING FILES//')
            zip.extractall() 
            print('//FILES ARE EXTRACTED//')
        os.remove('game_data.zip')
        launch()
    else:
        download_files()

def play():
    disable_ui()
    threading.Thread(target=launch).start()

def launch():
    print("//DISABLING UI//")
    print("//FILES VERIFICATION//")
    fileName = r"info.txt"
    if os.path.isfile(fileName):
        print('//FILES ARE OK//')
    else:
        checkfiles()
    print("//LAUNCHING//")
    options = {"username": config['SETTINGS'].get('nickname'), "uuid": str(uuid.uuid4()),"token": "", "executablePath": java_path}
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directory, options)
    app.withdraw()
    call(minecraft_command)
    print("//CLOSING APP//")
    os._exit(1)

#Window Settings
app = customtkinter.CTk()
customtkinter.set_appearance_mode("dark")
app.geometry("1280x720")
app.title("OriginMC Launcher")
app.configure(fg_color="#161616")
app.iconbitmap("assets/logo.ico")
app.resizable(False, False)
app.grab_set()

#Images and background
bg_img= PhotoImage(file = "assets/background_low.png")
img1 = Image.open("assets/cancel.png")
img2 = Image.open("assets/settings.png")
img3 = Image.open("assets/play.png")
bg= Label(app, image = bg_img)
bg.pack()

#Buttons
play_button = customtkinter.CTkButton(app, command=play, text="", image=customtkinter.CTkImage(img3, size=(70, 70)), fg_color="#ff6600", anchor="center", height=100, width=100, corner_radius = 100, hover_color="#904a00", )
settings_button = customtkinter.CTkButton(app, command=settings, text="", image=customtkinter.CTkImage(img2, size=(50, 50)), fg_color="#ff6600", anchor="center", height=50, width=40, corner_radius = 100, hover_color="#904a00",)
close_button = customtkinter.CTkButton(app, command=sys.exit, text="", image=customtkinter.CTkImage(img1, size=(50, 50)), fg_color="#ff6600", anchor="center", height=50, width=40, corner_radius = 100, hover_color="#904a00",)

play_button.place(y=480, x=555)
settings_button.place(y=500, x=420)
close_button.place(y=500, x=755)

#Showing window
app.mainloop()

"""

key = Fernet.generate_key()
encryption_type = Fernet(key)
encrypted_message = encryption_type.encrypt(code)

decrypted_message = encryption_type.decrypt(encrypted_message)

exec(decrypted_message)