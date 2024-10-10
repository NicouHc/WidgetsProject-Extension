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

from flask import Flask
from flask_cors import CORS

"""
Latest Changelog (06/10/2024):

[ 2.0.2 ]==========================================
- new todo-list

[ 2.0.3 ]==========================================
- fixed todo-list Style
- small changes on buttons hovers colors
- added debug button to change console visibility and check possible errors
- added open Folder button to open Wallpaper directory
- new checkbox style for settings
- avoid exiting the Settings menu when defining settings for the first time to prevent errors.

[ 2.0.4 ]==========================================
- fixed possible error at Open wallpaper directory
- updated wp-extension tutorial video on readme
- added tutorial button at define settings for first time

[ 2.0.5 ]==========================================
- app run over flask local server so now it dont require add wallpaper folder for work
- todo-notes saved on settings.json
- weather is now integrated inside the wallpaper
- added battery display in usage

"""

# -----------------------
# define var
running = True
global start_on_startup, settings, PcUsage

settings = ""
start_on_startup = False 
tasks = [] 
version = "2.0.5"
PcUsage = [0, 0]

global consoleVisibility
consoleVisibility = False

# GeneralFunctions ########################################################################
def openLink(link):# Open Links
    if "https://" in link: #open links
        os.system(f'start {link}')
    else:#open directory
        os.startfile(os.path.realpath(link))
        
class style():# class styles for console message with colors 
    RED = '\033[31m'
    YELLOW = '\033[33m'
    ENDC = '\033[0m'
    OKBLUE = '\033[94m'
    DIV = '\033[100m \033[90m'

def console_visibility(var): # change consolve visibility
    global consoleVisibility

    if(var == 3):# get oposite
        if(consoleVisibility) == 1: var = 2
        else: var = 1

    consoleVisibility = var

    if(var == 1):
        show = 5#Show Console
    else:
        show = 0#Hide Console

    hwnd = ctypes.windll.kernel32.GetConsoleWindow() 
    if hwnd != 0:
        ctypes.windll.user32.ShowWindow(hwnd, show)  # SW_SHOW = 5

def print_Error(e):# show error with format
    console_visibility(1)
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

def obtain_current_dir():# define current path
    if getattr(sys, 'frozen', False):
        # if the file is .exe
        return os.path.dirname(sys.argv[0])
    else:
        # if file is .py script
        return os.path.dirname(os.path.abspath(__file__))


# Notes Functions #########################################################################
def add_task(task_text):# add new task
    if task_text:
        tasks.append({'text': task_text, 'checked': False})
        save_settings(currentPath + '/settings.json', settings)
        display_tasks()

def delete_task(index):# delete task
    del tasks[index]
    save_settings(currentPath + '/settings.json', settings)
    display_tasks()

def toggle_task(index):# update checked status
    tasks[index]['checked'] = not tasks[index]['checked']
    save_settings(currentPath + '/settings.json', settings)

def display_tasks():# display task in main panel
    global tasks
    icon_close = ctk.CTkImage(Image.open("./resources/close.png"), size=(30, 30))
    
    button_style = {
        "text_color": "white",
        "fg_color": "transparent",
        "hover_color": "#171a21",
        "corner_radius": 0,
        "compound": "left",
        "anchor": "w",
        "image": icon_close,
        "width": 30,
    }
    frame_Style = {
        "fg_color": "#12151a",        
        "corner_radius": 5,
        "border_width": 1.5,
        "border_color": "#565b5e",
        "width": 200,  # Ancho del Frame
        "height": 100,  # Altura del Frame
    }
    

    for widget in task_list.winfo_children():
        widget.destroy()

    
    for index, task in enumerate(tasks):
        
        if isinstance(task, str):# raplace old-todo notes format for new value
            task = ({
                "text": task,
                "checked": False
            })
            tasks[index] = task 
        
        # Checkbox para la tarea
        def wrap_text(text, line_length):
            words = text.split()
            lines = []
            current_line = ""
            for word in words:
                if len(current_line + word) <= line_length:
                    current_line += word + " "
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "
            
            if current_line:
                lines.append(current_line.strip())
            return "\n".join(lines)

        # Verificar si task es un diccionario con la clave 'text'
        if isinstance(task, dict) and 'text' in task:
            task_frame = ctk.CTkFrame(master=task_list, **frame_Style)
            task_frame.pack(pady=5, padx=10, fill="x", expand=True)
            
            checkboxStyle = {
                "master": task_frame, 
                "text": wrap_text(task['text'], 30),
                "variable": ctk.StringVar(value=task['text']),
                "onvalue": True, 
                "offvalue": False, 
                "width": 300,
                "checkmark_color": "#565b5e",
                "fg_color": "#565b5e",
                "hover_color": "#565b5e",
                "corner_radius": 5,
                "text_color": "#ffffff",
                "border_width": 1.5,
                "border_color": "#565b5e"
            }

            # Dentro del código de agregar tareas
            task_checkbox = ctk.CTkCheckBox(**checkboxStyle, command=lambda i=index: toggle_task(i))
            task_checkbox.pack(side="left", padx=15)

            if task['checked']:
                task_checkbox.select()

            # Botón de borrar
            delete_button = ctk.CTkButton(master=task_frame, text="", command=lambda i=index: delete_task(i), **button_style)
            delete_button.pack(side="right", padx=2, pady=3) 
        else:
            print("invalid format: " + str(task))

  
# Settings Functions ######################################################################
def load_settings(file_path):#  load json settings
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            global start_on_startup, tasks, settings

            settings = json.load(file)
            start_on_startup = settings.get('start_on_startup', False)
            tasks = settings.get('todo_list', [])
            return settings
    else:
        return None

def save_settings(file_path, settings):# save json 
    with open(file_path, 'w') as file:
        json.dump(settings, file, indent=4)

def set_startup(enable):# define start program on pc startup
    script_path = currentPath  # Obtain .exe path
    
    key = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
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

        global uso_cpu, uso_ram, battery
        uso_cpu = psutil.cpu_percent(interval=intervalo)
        uso_ram = psutil.virtual_memory().percent
        battery = psutil.sensors_battery()
        
        if(battery):
            battery = battery.percent
        else:
            battery = -1

        # Generate array
        global PcUsage
        PcUsage = f"[{uso_cpu }, {uso_ram}, {battery}]"
        time.sleep(1)  # zzz


# MAIN WINDOW #############################################################################
def mainPanel(mostrar): #ui menu
    def guardar_configuracion():# function save text input in to json
        global start_on_startup, settings
        start_on_startup = var_startup.get()
        
        settings = {
            "start_on_startup": start_on_startup,
            "todo_list": tasks
        }
        save_settings(currentPath + '/settings.json', settings) # save settings json
        set_startup(start_on_startup)  # config startup
        root.destroy()
        
    def show_panel(panel): #function show specific subpanel
        global settings
        if(settings == ""): # Avoid exiting the setup menu when defining settings for the first time
            settings = {
                "start_on_startup": start_on_startup,
                "todo_list": tasks
            }
            save_settings(currentPath + '/settings.json', settings)
            
        for p in [panel_inicio, panel_notas, panel_ajustes]:
            p.pack_forget()
        panel.pack(fill='both', expand=True)
    
        """
        os.remove(wallpaperPath + '/files/info/' + 'weather-data.js')
        os.remove(wallpaperPath + '/files/info/' + 'pc-info.js')
        os.remove(wallpaperPath + '/files/info/' + 'ToDoNotes.js')
        """
        
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
        "hover_color": "#22242b",
        "corner_radius": 10,     
        "height": 40,               
        "anchor": "center",
        "border_width": 2,
        "border_color": "#565b5e"
    }
    mini_Panel_Style = {
        "fg_color": "#171a21",        
        "corner_radius": 0,     
    }
    text_input_Style = {
        "fg_color": "#12151a",        
        "corner_radius": 5,
        "border_width": 1.5,
        "border_color": "#565b5e"
    }
    button_style_new_Version = {
        "text_color": "white",
        "font": ctk.CTkFont(size=14),
        "fg_color": "transparent",  
        "hover_color": "#171a21",    
        "corner_radius": 10,      
        "height": 50,               
        "compound": "left",       
        "anchor": "w",               
        "border_width": 2,
        "border_color": "#565b5e"
    }
    checkboxStyle = {
        "checkmark_color": "#565b5e",
        "fg_color": "#565b5e",
        "hover_color": "#565b5e",
        "corner_radius": 5,
        "text_color": "#ffffff",
        "border_width": 1.5,
        "border_color": "#565b5e"
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
        btn_update = ctk.CTkButton(sidebar, text="New Version", image=icon_new, command=lambda: openLink("https://github.com/NicouHc/WidgetsProject-Extension"), **button_style_new_Version)
        btn_update.pack(fill='x', padx=10, pady=5, side='bottom')


    # Home panel ------------------------------------------------------------------------------------------
    panel_inicio = ctk.CTkFrame(main_container, **mini_Panel_Style)

    # Banner
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


    # Todo-NOTES  ------------------------------------------------------------------------------------------
    global task_list

    panel_notas = ctk.CTkFrame(main_container, **mini_Panel_Style)
    
    # Crear un Canvas para contener solo el frame de tareas (task_list) 171a21
    canvas = ctk.CTkCanvas(panel_notas, width=300, height=290, bg="#171a21", highlightthickness=0)# Limitar el alto para ver el efecto del scroll
    canvas.pack(side="left", fill="x", expand=True, padx=10, pady=10)

    # Agregar una Scrollbar lateral al canvas
    scrollbar = ctk.CTkScrollbar(panel_notas, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="left", fill="y", pady=30)

    # Configurar la scrollbar para el canvas
    canvas.configure(yscrollcommand=scrollbar.set)

    #Task frame
    task_list = ctk.CTkFrame(canvas,  fg_color="transparent")  
    task_list.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Agregar el frame task_list al canvas como una ventana
    canvas.create_window((0, 0), window=task_list, anchor="nw")

    panel_notas_label = ctk.CTkLabel(panel_notas, text="ToDo-Notes", text_color="white",font=ctk.CTkFont(size=20))
    panel_notas_label.pack(pady=10)

    # Textbox para agregar nuevas tareas
    task_entry = ctk.CTkEntry(panel_notas, height=60, **text_input_Style, text_color="#ffffff")
    task_entry.pack(pady=10, padx=10)

    # Botón para agregar tareas
    add_button = ctk.CTkButton(panel_notas, text="+ Add Task", command=lambda: add_task(task_entry.get()), **button_style_2)
    add_button.pack(pady=10)
    
    display_tasks()# show tasks
    

    # Settings Pannel  ------------------------------------------------------------------------------------------
    panel_ajustes = ctk.CTkFrame(main_container, **mini_Panel_Style)

    titleSettings = ctk.CTkLabel(panel_ajustes, text="Settings", text_color="white",font=ctk.CTkFont(size=20))
    titleSettings.grid(row=0, column=0, pady=10, padx=10)
    
    divider = ctk.CTkFrame(panel_ajustes, height=2, fg_color="grey")
    divider.grid(row=3, column=0, sticky="ew", padx=0, pady=10)
    divider = ctk.CTkFrame(panel_ajustes, height=2, fg_color="grey")
    divider.grid(row=3, column=1, sticky="ew", padx=0, pady=10)
    divider = ctk.CTkFrame(panel_ajustes, height=2, fg_color="grey")
    divider.grid(row=3, column=2, sticky="ew", padx=0, pady=10)

    var_startup = ctk.BooleanVar()
    ctk.CTkCheckBox(panel_ajustes, text="Start on PC Startup", variable=var_startup, **checkboxStyle).grid(row=8, column=0, columnspan=2, pady=10)
    
    button_frame = ctk.CTkFrame(panel_ajustes, **mini_Panel_Style)
    button_frame.grid(row=9, column=0, columnspan=2, pady=10, padx=0)
    ctk.CTkButton(button_frame, text="▸ Save Settings", command=guardar_configuracion, **button_style_2).grid(row=9, column=0, pady=10, padx=15)
    
    
    ctk.CTkButton(button_frame, text="▸ Debug Console", command=lambda: console_visibility(3), **button_style_2).grid(row=9, column=1, pady=10, padx=15)
    #ctk.CTkButton(button_frame, text="▸ Tutorial", command=lambda: openLink(f'https://www.youtube.com/watch?v=1s-l17dJ2BE'), **button_style_2).grid(row=9, column=3, pady=10, padx=15)
    

    # --------------------
    var_startup.set(start_on_startup)


    # cpu usage
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
        mainPanel("panel_inicio")  # just open settings if there are no saved settings
    menu()

def start_threads():# start cpu/ram/weather update threads
        global running
        cpuUsage = threading.Thread(target=obtener_info)
        
        if not cpuUsage.is_alive():
            running = True
            cpuUsage.start()
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

    ## start monitor
    start_threads()

    icon.run()

# flask ################################################################################
app = Flask(__name__)
CORS(app)

# display cpu ram usage
@app.route('/usage', methods=['GET'])
def get_usage():
    global PcUsage
    return PcUsage

# display notes
@app.route('/notes', methods=['GET'])
def get_notes():
    global tasks
    return json.dumps(tasks, ensure_ascii=False)

def run_flask_app():
    app.run(host='127.0.0.1', port=5000)

if __name__ == "__main__":
    try:
        console_visibility(2)
        currentPath = obtain_current_dir()
        threading.Thread(target=run_flask_app).start() # start flask thread
        preLoad()  # load settings
        menu()  # display tryicon menu
        

    except Exception as e: 
        print_Error(e)