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

"""
Latest Changelog (11/09/2024):

- Fixed error in set_startup when trying to delete a non-existent registry key
- New ui and icon
- added 'Report on discord' on print_Error
- added 'New version avaible' notification

"""

# -----------------------
# define var
running = True
global latitude, longitude, wallpaperPath, notes_text, start_on_startup
latitude = ""
longitude = ""
wallpaperPath = ""
notes_text = ""
start_on_startup = False 

version = "2.0.0"

def obtain_current_dir():# define current path
    if getattr(sys, 'frozen', False):
        # if the file is .exe
        return os.path.dirname(sys.argv[0])
    else:
        # if file is .py script
        return os.path.dirname(os.path.abspath(__file__))
currentPath = obtain_current_dir()

# GeneralFunctions ########################################################################
def openLink(link):# Open Links
    if link:
        os.system(f'start {link}')

class style():# class styles for console message with colors 
    RED = '\033[31m'
    YELLOW = '\033[33m'
    ENDC = '\033[0m'
    OKBLUE = '\033[94m'
    DIV = '\033[100m \033[90m'

def hide_console():# show hide console functions
    #Hidde window console
    
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd != 0:
        ctypes.windll.user32.ShowWindow(hwnd, 0)  # SW_HIDE = 0
def show_console():
    #Show Console
   
    hwnd = ctypes.windll.kernel32.GetConsoleWindow() 
    if hwnd != 0:
        ctypes.windll.user32.ShowWindow(hwnd, 5)  # SW_SHOW = 5

def print_Error(e):# show error with format
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
    print("\n - Report error on Discord: " + style.OKBLUE + " https://discord.com/invite/63EUyQBZPm"+ style.ENDC)
    print("")
    input("Press Enter to exit...")
    exit_app()

def exit_app():# exit function
    os._exit(0)

def getCurrentVersion():# return current version for notify updates
    url = "https://raw.githubusercontent.com/NicouHc/WidgetsProject-Extension/main/resources/version.txt"
    try:
        content = requests.get(url).text
    except:
        pass
    return(content)


# Notes Functions #########################################################################
def leer_notas_js():# read notes.json and update globals
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

def actualizar_notas_js(array_notas):# save notes
    # save array in js
    with open(wallpaperPath + "/files/info/" + "ToDoNotes.js", "w") as file:
        # Convert the notes array to a text string in JavaScript array format
        notas_js = json.dumps(array_notas, ensure_ascii=False)
        file.write(f'var todoNotes = {notas_js};\n')

def guardar_notas():  # Gets the widget text and updates the JS file
    global notes_text
    notas_texto = text_area.get("1.0", "end").strip()
    # Splits text into lines and converts them into an array of notes
    notas_array = notas_texto.split('\n')
    if notas_array:
        notes_text = notas_texto
        actualizar_notas_js(notas_array)


# Settings Functions ######################################################################
def load_settings(file_path):#  load json settings
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

def save_settings(file_path, settings):# save json 
    with open(file_path, 'w') as file:
        json.dump(settings, file, indent=4)

def set_startup(enable):# define start program on pc startup
    script_path = currentPath  # Obtain .exe path
    
    key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    value = "WidgetsProjectExtension"  # define registry name

    try:
        # open registry key
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE)
        
        if enable:
            # define value
            winreg.SetValueEx(reg_key, value, 0, winreg.REG_SZ, script_path)
            print("[i] Program startup 1.")
        else:
            # try delete the registry 
            try:
                winreg.DeleteValue(reg_key, value)
                print("[i] Program startup 0.")
            except:
                # key dont exist
                pass
            
        
        # close registry
        winreg.CloseKey(reg_key)
    except Exception as e:
        print_Error("Startup setting error - Reg key not found \n" + str(e))


# Update Info functions ###################################################################
def obtener_info(intervalo=1):# computer usage
    global running
    while running:

        global uso_cpu, uso_ram
        uso_cpu = psutil.cpu_percent(interval=intervalo)
        uso_ram = psutil.virtual_memory().percent

        # Generate the content on js
        js_content = f"var pc_info = [{uso_cpu }, {uso_ram}];\n"

        os.makedirs(os.path.dirname(wallpaperPath + '/files/info/'+ 'pc-info.js'), exist_ok=True)

        # write values on the file pc-info.js
        with open(wallpaperPath + '/files/info/' + 'pc-info.js', 'w') as file:
            file.write(js_content)

        time.sleep(1)  # zzz

def weather():# weather
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


# MAIN WINDOW #############################################################################
def mainPanel(mostrar): #ui menu
    def guardar_configuracion():# function save text input in to json
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
            root.destroy()
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
   
    def show_panel(panel): #function show specific subpanel
        for p in [panel_inicio, panel_notas, panel_ajustes]:
            p.pack_forget()
        panel.pack(fill='both', expand=True)

    root = ctk.CTk()
    root.title("WidgetsProject Extension")
    root.geometry("750x400")
    root.resizable(False, False)
    root.iconbitmap(currentPath + "./resources/icon.ico") 
    root._fg_color = "#171a21"
    
    main_container = ctk.CTkFrame(root)
    main_container.pack(fill='both', expand=True)

    # lateral bar
    sidebar = ctk.CTkFrame(main_container, width=200, corner_radius=0, fg_color="#12151a")
    sidebar.pack(side='left', fill='y')

    # logo
    logo_image = ctk.CTkImage(Image.open("./resources/icon.ico"), size=(40, 40))
    logo_label = ctk.CTkLabel(sidebar, image=logo_image, text="")
    logo_label.pack(pady=(20, 10))


    # lateral bar style
    button_style = {
        "text_color": "white",
        "font": ctk.CTkFont(size=14),
        "fg_color": "transparent",   # Color de fondo 
        "hover_color": "#171a21",    # Color mouse hover
        "corner_radius": 10,         # Border radius
        "height": 50,                # button height
        "compound": "left",          # Icon position
        "anchor": "w",               # Text Align
    }
    button_style_2 = {
        "text_color": "white",
        "font": ctk.CTkFont( size=14),
        "fg_color": "#12151a",        
        "hover_color": "#763636",
        "corner_radius": 10,     
        "height": 40,               
        "anchor": "center",
        "border_width": 2
    }
    mini_Panel_Style = {
        "fg_color": "#171a21",        
        "corner_radius": 0,     
    }
    text_input_Style = {
        "fg_color": "#12151a",        
        "corner_radius": 5,
        "border_width": 1.5

    }
    button_style_new_Version = {
        "text_color": "white",
        "font": ctk.CTkFont(size=14),
        "fg_color": "transparent",   # Color de fondo 
        "hover_color": "#171a21",    # Color mouse hover
        "corner_radius": 10,         # Border radius
        "height": 50,                # button height
        "compound": "left",          # Icon position
        "anchor": "w",               # Text Align
        "border_width": 2
    }
    
    # define icons
    icon_inicio = ctk.CTkImage(Image.open("./resources/icon_inicio.png"), size=(20, 20))
    icon_notas = ctk.CTkImage(Image.open("./resources/icon_notas.png"), size=(20, 20))
    icon_ajustes = ctk.CTkImage(Image.open("./resources/icon_ajustes.png"), size=(20, 20))
    icon_exit = ctk.CTkImage(Image.open("./resources/icon_exit.png"), size=(20, 20))
    icon_new = ctk.CTkImage(Image.open("./resources/new.png"), size=(20, 20))

    # Crear los botones de la barra lateral con estilo personalizado 
    btn_inicio = ctk.CTkButton(sidebar, text="Home", image=icon_inicio, command=lambda: show_panel(panel_inicio), **button_style)
    btn_inicio.pack(fill='x', padx=10, pady=5)

    btn_notas = ctk.CTkButton(sidebar, text="Notes", image=icon_notas, command=lambda: show_panel(panel_notas), **button_style)
    btn_notas.pack(fill='x', padx=10, pady=5)

    btn_ajustes = ctk.CTkButton(sidebar, text="Settings", image=icon_ajustes, command=lambda: show_panel(panel_ajustes), **button_style)
    btn_ajustes.pack(fill='x', padx=10, pady=5)

    btn_exit = ctk.CTkButton(sidebar, text="EXIT APP", image=icon_exit, command=exit_app,  **button_style)
    btn_exit.pack(fill='x', padx=10, pady=5, side='bottom')

    if(version != getCurrentVersion()): # if version is diferent than latest version -> display button
        btn_update = ctk.CTkButton(sidebar, text="New Version Avaible", image=icon_new, command=lambda: openLink("https://github.com/NicouHc/WidgetsProject-Extension"), **button_style_new_Version)
        btn_update.pack(fill='x', padx=10, pady=5, side='bottom')


    # Home panel -----
    panel_inicio = ctk.CTkFrame(main_container, **mini_Panel_Style)

    # Banner en el panel de inicio
    banner_image = ctk.CTkImage(Image.open("./resources/banner.png"), size=(520, 150))
    banner_label = ctk.CTkLabel(panel_inicio, image=banner_image, text=f"Version: {version}", text_color="white", font=ctk.CTkFont(family="Courier", size=16))
    banner_label.pack(pady=(30, 20))

    # Crear un marco para los botones en el panel de inicio
    button_frame = ctk.CTkFrame(panel_inicio, **mini_Panel_Style)
    button_frame.pack(pady=10)
    
    # Botones con enlaces en el panel de inicio
    btn_discord = ctk.CTkButton(button_frame, text="↗ Join our Discord", command=lambda: openLink("https://discord.com/invite/63EUyQBZPm"), **button_style_2)
    btn_discord.pack(side="left", padx=10)

    btn_coffee = ctk.CTkButton(button_frame, text="↗ Buy me a Coffee", command=lambda: openLink("https://www.paypal.com/donate/?hosted_button_id=UBDDRKEZ4XABE"), **button_style_2)
    btn_coffee.pack(side="left", padx=10)

    btn_github = ctk.CTkButton(button_frame, text="↗ GitHub Source", command=lambda: openLink("https://github.com/NicouHc/WidgetsProject-Extension"), **button_style_2)
    btn_github.pack(side="left", padx=10)

    # Todo-NOTES  -----
    panel_notas = ctk.CTkFrame(main_container, **mini_Panel_Style)
    panel_notas_label = ctk.CTkLabel(panel_notas, text="ToDo-Notes", text_color="white",font=ctk.CTkFont(size=20))
    panel_notas_label.pack(pady=10)

    global text_area
    text_area = ctk.CTkTextbox(panel_notas, width=500, height=270, **text_input_Style)
    text_area.pack(padx=10, pady=10)

    boton_guardar = ctk.CTkButton(panel_notas, text="Save Notes", command=guardar_notas, **button_style_2)
    boton_guardar.pack(pady=5)

    # Fill textarea with the content
    if isinstance(notes_text, list):
        text_area.insert("1.0", "\n".join(notes_text))
    else:
        text_area.insert("1.0", notes_text)

    # Settings Pannel  -----
    panel_ajustes = ctk.CTkFrame(main_container, **mini_Panel_Style)

    titleSettings = ctk.CTkLabel(panel_ajustes, text="Settings", text_color="white",font=ctk.CTkFont(size=20))
    titleSettings.grid(row=0, column=0, pady=10, padx=10)

    divider = ctk.CTkFrame(panel_ajustes, height=2, fg_color="grey")
    divider.grid(row=1, column=0, sticky="ew", padx=0, pady=10)
    divider = ctk.CTkFrame(panel_ajustes, height=2, fg_color="grey")
    divider.grid(row=1, column=1, sticky="ew", padx=0, pady=10)
    divider = ctk.CTkFrame(panel_ajustes, height=2, fg_color="grey")
    divider.grid(row=1, column=2, sticky="ew", padx=0, pady=10)

    ctk.CTkLabel(panel_ajustes, text="Wallpaper Directory:").grid(row=2, column=0, padx=10, pady=5)
    entry_directory = ctk.CTkEntry(panel_ajustes, width=250, **text_input_Style) 
    entry_directory.grid(row=2, column=1, padx=10, pady=5)
    
    divider = ctk.CTkFrame(panel_ajustes, height=2, fg_color="grey")
    divider.grid(row=3, column=0, sticky="ew", padx=0, pady=10)
    divider = ctk.CTkFrame(panel_ajustes, height=2, fg_color="grey")
    divider.grid(row=3, column=1, sticky="ew", padx=0, pady=10)
    divider = ctk.CTkFrame(panel_ajustes, height=2, fg_color="grey")
    divider.grid(row=3, column=2, sticky="ew", padx=0, pady=10)

    ctk.CTkLabel(panel_ajustes, text="Latitude:").grid(row=4, column=0, padx=10, pady=5)
    entry_latitude = ctk.CTkEntry(panel_ajustes, width=250, **text_input_Style)  
    entry_latitude.grid(row=4, column=1, padx=10, pady=5)

    ctk.CTkLabel(panel_ajustes, text="Longitude:").grid(row=5, column=0, padx=10, pady=5)
    entry_longitude = ctk.CTkEntry(panel_ajustes, width=250, **text_input_Style)
    entry_longitude.grid(row=5, column=1, padx=10, pady=5)

    divider = ctk.CTkFrame(panel_ajustes, height=2, fg_color="grey")
    divider.grid(row=6, column=0, sticky="ew", padx=0, pady=10)
    divider = ctk.CTkFrame(panel_ajustes, height=2, fg_color="grey")
    divider.grid(row=6, column=1, sticky="ew", padx=0, pady=10)
    divider = ctk.CTkFrame(panel_ajustes, height=2, fg_color="grey")
    divider.grid(row=6, column=2, sticky="ew", padx=0, pady=10)

    var_startup = ctk.BooleanVar()
    ctk.CTkCheckBox(panel_ajustes, text="Start on Windows Startup", variable=var_startup).grid(row=7, column=0, columnspan=2, pady=10)
    
    ctk.CTkButton(panel_ajustes, text="Save", command=guardar_configuracion, **button_style_2).grid(row=8, column=0, columnspan=2, pady=10)
    # --------------------
    entry_directory.insert(0, wallpaperPath)
    entry_latitude.insert(0, latitude)
    entry_longitude.insert(0, longitude)
    var_startup.set(start_on_startup)

    # cup usage
    threading.Thread(target=obtener_info, daemon=True).start()

    if (mostrar):# show specific panel
        if (mostrar == "panel_ajustes"):
            mostrar = panel_ajustes
        elif (mostrar == "panel_notas"):
            mostrar = panel_notas
        elif (mostrar == "panel_inicio"):
            mostrar = panel_inicio
        show_panel(mostrar)

    root.mainloop()


# START ALL ################################################################################
def preLoad():#load settings before start the program
    file_path = currentPath + '/settings.json'
    settings = load_settings(file_path)

    if not settings:
        mainPanel("panel_ajustes")  # just open settings if there are no saved settings
    menu()

def start_threads():# start cpu/ram/weather update threads
        global running
        cpuUsage = threading.Thread(target=obtener_info)
        weatherRefresh = threading.Thread(target=weather)
        
        if not cpuUsage.is_alive():
            running = True
            cpuUsage.start()
            weatherRefresh.start()
        else:
            pass

def menu():# generate try icon 
    os.system("title Widgets Project && cls")

    # tryicon
    menu = (
        item('Info',  lambda:mainPanel("panel_inicio")),
        item('Notes',   lambda:mainPanel("panel_notas")),
        item('Settings', lambda:mainPanel("panel_ajustes")),
        item('Exit',   exit_app)
    )

    try:
        icon_image = Image.open(currentPath + "./resources/icon.ico")
        icon = pystray.Icon("name", icon_image, "Widgets Project", menu)
    except:
        print_Error("Resource 'icon.ico' not found")
    #icon = pystray.Icon("name", Image.new("RGB", (64, 64), (255, 0, 0)), "Widgets Project", menu)

    ## start monitor and weather threads
    start_threads()

    icon.run()


if __name__ == "__main__":
    try:
        hide_console()
        preLoad()  # load settings
        menu()  # display tryicon menu
    except Exception as e: 
        print_Error(e)