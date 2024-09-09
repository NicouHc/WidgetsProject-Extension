# Widgets Project Extension

import psutil
import threading
import time
import requests
import json
import os
import pystray
from pystray import MenuItem as item
import ctypes
import customtkinter as ctk
from PIL import Image
import winreg
import sys

running = True

global latitude, longitude, wallpaperPath, notes_text, start_on_startup, currentPath
latitude = ""
longitude = ""
wallpaperPath = ""
notes_text = ""
start_on_startup = False 

# -----------------------
# define current path

def obtain_current_dir():
    if getattr(sys, 'frozen', False):
        # if the file is .exe
        return os.path.dirname(sys.argv[0])
    else:
        # if file is .py script
        return os.path.dirname(os.path.abspath(__file__))
currentPath = obtain_current_dir()

# -----------------------
# console

class style(): 
    # class styles for console message with colors
    RED = '\033[31m'
    YELLOW = '\033[33m'
    ENDC = '\033[0m'
    OKBLUE = '\033[94m'
    DIV = '\033[100m \033[90m'

def hide_console():
    #Hidde window console
    
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd != 0:
        ctypes.windll.user32.ShowWindow(hwnd, 0)  # SW_HIDE = 0

def show_console():
    #Show Console
   
    hwnd = ctypes.windll.kernel32.GetConsoleWindow() 
    if hwnd != 0:
        ctypes.windll.user32.ShowWindow(hwnd, 5)  # SW_SHOW = 5

def print_Error(e):
    show_console()
    os.system("title Widgets Project && cls")
    print("")
    print(style.RED + " [i] An error occurred " + style.ENDC);
    print("")
    print(style.DIV + "|                                                                            |"+ style.ENDC)
    print("")
    print(f"{e}")
    print("")
    print(style.DIV + "|                                                                            |"+ style.ENDC)
    input("Press Enter to exit...")

# -----------------------
# CUP RAM Usage
def obtener_info(intervalo=1):
    global running
    while running:

        uso_cpu = psutil.cpu_percent(interval=intervalo)
        uso_ram = psutil.virtual_memory().percent
        

        # Generate the content on js
        js_content = f"var pc_info = [{uso_cpu }, {uso_ram}];\n"

        os.makedirs(os.path.dirname(wallpaperPath + '/files/info/'+ 'pc-info.js'), exist_ok=True)

        # write values on the file pc-info.js
        with open(wallpaperPath + '/files/info/' + 'pc-info.js', 'w') as file:
            file.write(js_content)

        time.sleep(1)  # zzz

# -----------------------
# weather
def weather():
    global latitude, longitude
    api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,rain,snowfall,wind_speed_10m&daily=&past_days=1"
    contador = 0

    global running
    while running:
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # display error if fail
            weather_data = response.json()
            
            # convert JSON to js format
            js_content = f"var weather_data = [{json.dumps(weather_data, indent=4)}];\n"
            
            # save js as file
            with open(wallpaperPath + '/files/info/' + 'weather-data.js', 'w') as file:
                file.write(js_content)
            
            time.sleep(18000)  # refresh every 5hs
        except requests.RequestException as e:
            time.sleep(10)
            contador += 1
            if(contador == 5):
                print("(i) Weather Update Stopped")
                break

# -----------------------
#  load json settings
def load_settings(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            settings = json.load(file)

            global wallpaperPath, latitude, longitude, start_on_startup
            wallpaperPath = settings['directory']
            latitude = settings['latitud']
            longitude = settings['longitud']
            start_on_startup = settings.get('start_on_startup', False)
            return settings
    else:
        return None

def save_settings(file_path, settings):
    with open(file_path, 'w') as file:
        json.dump(settings, file, indent=4)

def abrir_configuracion():
    def guardar_configuracion():
        global wallpaperPath, latitude, longitude, start_on_startup
        wallpaperPath = entry_directory.get()
        latitude = entry_latitude.get()
        longitude = entry_longitude.get()
        start_on_startup = var_startup.get()


        if os.path.exists(wallpaperPath + "/files/info"):
            settings = {
                "directory": wallpaperPath,
                "longitud": longitude,
                "latitud": latitude,
                "start_on_startup": start_on_startup
            }
            save_settings(currentPath + '/settings.json', settings) # save settings json
            set_startup(start_on_startup)  # config startup
            ventana.destroy()

        elif (os.path.exists(wallpaperPath + "/a.html") == False and  os.path.exists(wallpaperPath + "/files") == True):
            # preset error
            show_console()
            os.system("title Widgets Project && cls")
            print("")
            print(style.RED + " [i] Error - Invalid Path. " + style.ENDC);
            print("")
            print(style.ENDC + " This is a " + style.RED + "Preset Folder"+ style.ENDC + ", find "+ style.OKBLUE +" WidgetsProject"+ style.ENDC +" folder. " + style.ENDC)
            print("")
            print(" Simple Tutorial: "+ style.ENDC)
            print(" 1- Open " + style.OKBLUE + "Wallpaper Engine."  + style.ENDC)
            print(" 2- Find the wallpaper called " + style.OKBLUE + "Widgets Project." + style.ENDC)
            print(" 3- Second Click over it and select the option " + style.YELLOW + "'Open in Explorer'. " + style.ENDC)
            print("")
            os.system("pause")
            os._exit(0)
        else:
            # invalid path
            show_console()
            os.system("title Widgets Project && cls")
            print("")
            print(style.RED + " [i] Error - Invalid Path. " + style.ENDC);
            print("")
            print(" Simple Tutorial: "+ style.ENDC)
            print(" 1- Open " + style.OKBLUE + "Wallpaper Engine."  + style.ENDC)
            print(" 2- Find the wallpaper called " + style.OKBLUE + "Widgets Project." + style.ENDC)
            print(" 3- Second Click over it and select the option " + style.YELLOW + "'Open in Explorer'. " + style.ENDC)
            print("")
            os.system("pause")
            os._exit(0)

    ventana = ctk.CTk()
    ventana.title("Widgets Project - Settings")
    ventana.iconbitmap(currentPath + "/icon.ico")  
    
    ventana.geometry("430x200")  

    ctk.CTkLabel(ventana, text="Wallpaper Directory:").grid(row=0, column=0, padx=10, pady=5)
    entry_directory = ctk.CTkEntry(ventana, width=250) 
    entry_directory.grid(row=0, column=1, padx=10, pady=5)

    ctk.CTkLabel(ventana, text="Latitude:").grid(row=1, column=0, padx=10, pady=5)
    entry_latitude = ctk.CTkEntry(ventana, width=250)  
    entry_latitude.grid(row=1, column=1, padx=10, pady=5)

    ctk.CTkLabel(ventana, text="Longitude:").grid(row=2, column=0, padx=10, pady=5)
    entry_longitude = ctk.CTkEntry(ventana, width=250)
    entry_longitude.grid(row=2, column=1, padx=10, pady=5)

    var_startup = ctk.BooleanVar()
    ctk.CTkCheckBox(ventana, text="Start on Windows Startup", variable=var_startup).grid(row=3, column=0, columnspan=2, pady=10)

    ctk.CTkButton(ventana, text="Save", command=guardar_configuracion).grid(row=4, column=0, columnspan=2, pady=10)

    # 
    entry_directory.insert(0, wallpaperPath)
    entry_latitude.insert(0, latitude)
    entry_longitude.insert(0, longitude)
    var_startup.set(start_on_startup)

    ventana.mainloop()

def set_startup(enable):
    # define start program on pc startup

    script_path = sys.argv[0]  # Obtain .exe path
    
    key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    value = "WidgetsProjectExtension"  # define registry name

    try:
        # open registry key
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE)
        
        if enable:
            # define value
            winreg.SetValueEx(reg_key, value, 0, winreg.REG_SZ, script_path)
            print("Program set to start with Windows.")
        else:
            # delete the registry if is false
            winreg.DeleteValue(reg_key, value)
            print("Program removed from startup.")
        
        # close registry
        winreg.CloseKey(reg_key)
    except Exception as e:
        print_Error(e)


# -----------------------
# todo notes
def open_notes():
    leer_notas_js()
    crear_ventana_notas()

def crear_ventana_notas():
    # create window to change notes
    global text_area

    ventana = ctk.CTk()
    ventana.title("Widgets Project - Notes")
    ventana.iconbitmap(currentPath + "/icon.ico")  
    ventana.geometry("350x260")

    text_area = ctk.CTkTextbox(ventana, width=300, height=200)
    text_area.pack(padx=10, pady=10)

    boton_guardar = ctk.CTkButton(ventana, text="Save Notes", command=guardar_notas)
    boton_guardar.pack(pady=5)

    # Fill textarea with the content
    if isinstance(notes_text, list):
        text_area.insert("1.0", "\n".join(notes_text))
    else:
        text_area.insert("1.0", notes_text)

    ventana.mainloop()

def leer_notas_js():
    # read notes.json and update globals
    global notes_text
    try:
        with open(wallpaperPath + "/files/info/" + "ToDoNotes.js", "r") as file:
            contenido = file.read()
            # start and end array
            start = contenido.find('[')
            end = contenido.rfind(']')
            
            if start != -1 and end != -1:
                # obtain text content
                array_texto = contenido[start:end + 1]
                try:
                    # Usa json.loads to convert the content in list
                    notes_text = json.loads(array_texto)
                except json.JSONDecodeError:
                    notes_text = []
            else:
                notes_text = []
    except FileNotFoundError:
        notes_text = []

def actualizar_notas_js(array_notas):
    # save array in js
    with open(wallpaperPath + "/files/info/" + "ToDoNotes.js", "w") as file:
        # Convert the notes array to a text string in JavaScript array format
        notas_js = json.dumps(array_notas, ensure_ascii=False)
        file.write(f'var todoNotes = {notas_js};\n')

def guardar_notas():
    # Gets the widget text and updates the JS file
    global notes_text
    notas_texto = text_area.get("1.0", "end").strip()
    # Splits text into lines and converts them into an array of notes
    notas_array = notas_texto.split('\n')
    if notas_array:
        notes_text = notas_texto
        actualizar_notas_js(notas_array)

# -----------------------

def show_help_window():
    help_window = ctk.CTk()
    help_window.title("Widgets Project - Help")
    help_window.geometry("420x130")
    help_window.iconbitmap(currentPath + "/icon.ico")  

    # Title
    description_label = ctk.CTkLabel(help_window, text="Widgets Project Extension for WallpaperEngine ")
    description_label.pack(pady=20)

    # open link
    def openLink(link):
        if link:
            os.system(f'start {link}')

    button_frame = ctk.CTkFrame(help_window)
    button_frame.pack(pady=10)

    # <4
    join_button = ctk.CTkButton(button_frame, text="Join our Discord", command=lambda: openLink("https://discord.com/invite/63EUyQBZPm"))
    join_button.pack(side="left", padx=10)

    # ;)
    join_button2 = ctk.CTkButton(button_frame, text="Buy me a Coffee", command=lambda: openLink("https://www.paypal.com/donate/?hosted_button_id=UBDDRKEZ4XABE"))
    join_button2.pack(side="left", padx=10)

    help_window.mainloop()

# -----------------------

def preLoad():
    file_path = currentPath + '/settings.json'
    settings = load_settings(file_path)

    if not settings:
        abrir_configuracion()  # just open settings if there are no saved settings
    menu()

def exit_app(icon):
    global running
    running = False
    icon.stop()
    
    os._exit(0)

def menu():
    cpuUsage = threading.Thread(target=obtener_info)
    weatherRefresh = threading.Thread(target=weather)
    
    os.system("title Widgets Project && cls")

    def start_threads():
        global running
        if not cpuUsage.is_alive():
            running = True
            cpuUsage.start()
            weatherRefresh.start()
        else:
            pass

    menu = (
        item('Notes', open_notes),
        item('Settings', abrir_configuracion),
        item('About Us', show_help_window),
        item('Exit', exit_app)
    )

    icon_image = Image.open(currentPath + "/icon.ico")
    icon = pystray.Icon("name", icon_image, "Widgets Project", menu)

    #icon = pystray.Icon("name", Image.new("RGB", (64, 64), (255, 0, 0)), "Widgets Project", menu)
    
    start_threads()

    icon.run()

# -----------------------
#hide_console()
#preLoad()  # load settings
#menu()  # display menu

if __name__ == "__main__":
    try:
        hide_console()
        preLoad()  # load settings
        menu()  # display menu
    except Exception as e: 
        print_Error(e)
