import os
import subprocess
import minecraft_launcher_lib
import uuid
import webview
import configparser
from zipfile import ZipFile 

#Variables
config = configparser.ConfigParser()
title = "OriginMC"
version = "1.19.2-forge-43.2.21"
minecraft_directory = "data/.minecraft" 
file = "game_data.zip"

#Configuration
config.read('config.ini')
nickname  = config['SETTINGS'].get('Nickname')
java_path = config['SETTINGS'].get('Java path')

#Account
options = {"username": nickname,
            "uuid": str(uuid.uuid4()),
            "token": "",
            "executablePath": java_path}

#Functions
def dl():
    print("//FILES VERIFICATION//")
    fileName = r"info.txt"
    if os.path.isfile(fileName):
        print('//FILES ARE OK//')
    else:
        print('//DOWNLOADING FILES//')
        with ZipFile(file, 'r') as zip: 
            zip.printdir() 
            print('extraction...') 
            zip.extractall() 
            print('Done!')

class Api():
    def stop(self):
        window.destroy()
        exit()

    def mc(self):
        dl()
        print("//LAUNCHING THE GAME//")
        minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directory, options)
        window.destroy()
        subprocess.call(minecraft_command)
        exit()

    def settings(self):
        os.popen("config.ini")

#UI
print("//STARTING THE LAUNCHER//")
api = Api()
window = webview.create_window('OriginMC',"web/index.html", width=1000, height=630, resizable=(False), js_api=api)
webview.start()