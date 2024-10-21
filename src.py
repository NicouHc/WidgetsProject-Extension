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
import logging


from flask import Flask, request
from flask_cors import CORS

from tkinter import colorchooser


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

[ 2.0.6 ]==========================================
- Added some prints in __main__ to more easily monitor possible errors
- Removed LocalHost request prints 
- small style changes in menu
- added version on window title
- added Search browser function
- added Shortcuts menu
"""

# -----------------------
# define var
running = True
global start_on_startup, settings, PcUsage, start_time, color_shortcut

settings = ""
start_on_startup = False 
tasks = [] 
shortcuts = [] 
version = "2.0.6"
PcUsage = [0, 0]
color_shortcut = "#AB886D"

global consoleVisibility, broweserSearch
consoleVisibility = False

broweserSearch = "https://www.google.com/search?q=" 
# some examples:  https://duckduckgo.com/?&q= | https://www.bing.com/search?q= | https://search.yahoo.com/search?p= | https://search.aol.com/aol/search?q=



# GeneralFunctions ########################################################################
def openLink(link):# Open stuff
    if ("https://" in link or "http://" in link): #open links
        os.system(f'start "" "{link}"')
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
    os.system(f"title Widgets Project v{version} && cls")
    print(style.RED + "\n *" + style.ENDC +" An error occurred " + style.RED + f"\n ------------------------------------" + style.ENDC);
    
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

def defineStartupTime():# define the PC startup time 
    def Get_Pid():
        # note: use the sihost process start time to define when the pc startup because psutil.boot_time() display the time wrong 
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'sihost.exe':
                return proc.info['pid']

    global start_time
    start_time = psutil.Process(Get_Pid()).create_time()

def wrap_text(text, line_length):# prevent text overflows (tasklist / shortcuts)
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



# Notes Functions #########################################################################
def add_shortcut(icon, directory, shortcut_name, color):
    global shortcuts
    if directory and shortcut_name and icon:
        directory = directory.replace("\\", "/")
        shortcuts.append({'icon': icon, 'name': f"{shortcut_name}", 'directory': f'{directory}', 'color':  f'{color}'})

        save_settings(currentPath + '/settings.json', settings)
        display_shortcut()

def delete_shortcut(index):# delete task
    del shortcuts[index]

    save_settings(currentPath + '/settings.json', settings)
    display_shortcut()

def display_shortcut():
    global shortcuts
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
        "width": 300,  # Ancho del Frame
        "height": 100,  # Altura del Frame
    }


    for e in shortcuts_list.winfo_children():
        e.destroy()

    for index, shortcut in enumerate(shortcuts):
        
        # Verificar si task es un diccionario con la clave 'text'
        if isinstance(shortcut, dict) and 'directory' in shortcut:
            shrcut_frame = ctk.CTkFrame(shortcuts_list, **frame_Style)
            shrcut_frame.pack(pady=5, padx=10, fill="x", expand=False)

            #shrcut_text = wrap_text(f"{shortcut['name']} - {shortcut['directory']}", 80)

            ee = ctk.CTkLabel(shrcut_frame, text=wrap_text(shortcut['name'], 50), text_color="#ffffff", font=ctk.CTkFont(size=13), width=370)
            ee.pack(side="left", padx=15, pady=3) 

            #ee = ctk.CTkLabel(master=shrcut_frame, text=wrap_text(shortcut['directory'], 80), text_color="#ffffff", font=ctk.CTkFont(size=9))
            #ee.pack(side="left", padx=0, pady=3) 


            delete_button = ctk.CTkButton(shrcut_frame, text="", command=lambda i=index: delete_shortcut(i), **button_style)
            delete_button.pack(side="right", padx=2, pady=3) 
        else:
            print("invalid format: " + str(shortcut))

# Settings Functions ######################################################################
def load_settings(file_path):#  load json settings
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            global start_on_startup, tasks, settings, broweserSearch, shortcuts

            settings = json.load(file)
            start_on_startup = settings.get('start_on_startup', False)
            tasks = settings.get('todo_list', [])
            shortcuts = settings.get('shortcuts_list', [])
            broweserSearch = settings.get('browser', "https://www.google.com/search?q=")
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
    def startup():
        global start_time
        current_time = time.time()
        
        # Calcular el tiempo transcurrido desde el arranque
        elapsed_time = current_time - start_time
        
        # Convertir a horas y minutos
        mins, sec = divmod(elapsed_time, 60)
        hour, mins = divmod(mins, 60)
        return hour, mins
    
    while running:
        uso_cpu = psutil.cpu_percent(interval=intervalo)
        uso_ram = psutil.virtual_memory().percent
        battery = psutil.sensors_battery()
        upTime = startup()

        
        if(battery):
            battery = battery.percent
        else:
            battery = -1

        # Generate array
        global PcUsage
        PcUsage = f"[{uso_cpu}, {uso_ram}, {battery}, {upTime[0]}, {upTime[1]}]"
        time.sleep(1)  # zzz



# MAIN WINDOW #############################################################################
def mainPanel(mostrar): #ui menu
    def guardar_configuracion():# function save text input in to json
        global start_on_startup, settings, broweserSearch, shortcuts
        start_on_startup = var_startup.get()
        broweserSearch = entry_browser.get()
        
        settings = {
            "start_on_startup": start_on_startup,
            "browser": broweserSearch,
            "todo_list": tasks,
            "shortcuts_list": shortcuts
        }
        save_settings(currentPath + '/settings.json', settings) # save settings json
        set_startup(start_on_startup)  # config startup
        root.destroy()
        
    def show_panel(panel): #function show specific subpanel
        global settings
        if(settings == ""): # Avoid exiting the setup menu when defining settings for the first time
            settings = {
                "start_on_startup": start_on_startup,
                "browser": broweserSearch,
                "todo_list": tasks,
                "shortcuts_list": shortcuts
            }
            save_settings(currentPath + '/settings.json', settings)
            
        for p in [panel_inicio, panel_notas, panel_ajustes, panel_shortcuts]:
            p.pack_forget()
        panel.pack(fill='both', expand=True)
    
        """
        os.remove(wallpaperPath + '/files/info/' + 'weather-data.js')
        os.remove(wallpaperPath + '/files/info/' + 'pc-info.js')
        os.remove(wallpaperPath + '/files/info/' + 'ToDoNotes.js')
        """
        
    root = ctk.CTk()
    root.title(f"WidgetsProject Extension v{version}")
    root.geometry("750x400")
    root.resizable(False, False)
    root.iconbitmap(currentPath + "./resources/icon.ico") 
    
    
    main_container = ctk.CTkFrame(root)
    main_container.pack(fill='both', expand=True)
    main_container._fg_color = "#12151a"

    # lateral bar
    sidebar = ctk.CTkFrame(main_container, width=200, corner_radius=0, fg_color="#12151a")
    sidebar.pack(side='left', fill='y')

    rbar = ctk.CTkFrame(main_container, width=10, corner_radius=0, fg_color="#12151a")
    rbar.pack(side='right', fill='y')

    topbar = ctk.CTkFrame(main_container, height=10, corner_radius=0, fg_color="#12151a")
    topbar.pack(side='top', fill='x')

    bottombar = ctk.CTkFrame(main_container, height=10, corner_radius=0, fg_color="#12151a")
    bottombar.pack(side='bottom', fill='x')

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
        "height": 40,                # button height
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
        "corner_radius": 10,     
    }
    text_input_Style = {
        "fg_color": "#12151a",        
        "corner_radius": 5,
        "border_width": 1.5,
        "border_color": "#565b5e",
        "text_color": "#ffffff"
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
    comboBoxStyle ={
        "fg_color": "#12151a",        
        "corner_radius": 5,
        "border_width": 1.5,
        "border_color": "#565b5e",
        "text_color": "#ffffff",
        "dropdown_fg_color": "#12151a",
        "dropdown_text_color": "#ffffff",
        "dropdown_hover_color": "#565b5e",
     
    }
    
    # define icons
    icon_inicio = ctk.CTkImage(Image.open("./resources/icon_inicio.png"), size=(20, 20))
    icon_notas = ctk.CTkImage(Image.open("./resources/icon_notas.png"), size=(20, 20))
    icon_ajustes = ctk.CTkImage(Image.open("./resources/icon_ajustes.png"), size=(20, 20))
    icon_exit = ctk.CTkImage(Image.open("./resources/icon_exit.png"), size=(20, 20))
    icon_new = ctk.CTkImage(Image.open("./resources/new.png"), size=(20, 20))
    icon_folder = ctk.CTkImage(Image.open("./resources/icon_folder.png"), size=(20, 20))
    
    # Crear los botones de la barra lateral con estilo personalizado 
    btn_inicio = ctk.CTkButton(sidebar, text="Home", image=icon_inicio, command=lambda: show_panel(panel_inicio), **button_style)
    btn_inicio.pack(fill='x', padx=10, pady=5)

    btn_notas = ctk.CTkButton(sidebar, text="Notes", image=icon_notas, command=lambda: show_panel(panel_notas), **button_style)
    btn_notas.pack(fill='x', padx=10, pady=5)

    btn_notas = ctk.CTkButton(sidebar, text="Shortcuts", image=icon_folder, command=lambda: show_panel(panel_shortcuts), **button_style)
    btn_notas.pack(fill='x', padx=10, pady=5)

    btn_ajustes = ctk.CTkButton(sidebar, text="Settings", image=icon_ajustes, command=lambda: show_panel(panel_ajustes), **button_style)
    btn_ajustes.pack(fill='x', padx=10, pady=5)

    btn_exit = ctk.CTkButton(sidebar, text="",   fg_color="#12151a", hover_color="#12151a", height=2)
    btn_exit.pack(fill='x', padx=10, pady=5, side='bottom')

    btn_exit = ctk.CTkButton(sidebar, text="EXIT APP", image=icon_exit, command=exit_app,  **button_style)
    btn_exit.pack(fill='x', padx=10, pady=3, side='bottom')
    

    if(version != getCurrentVersion()): # if version is diferent than latest version -> display button
        btn_update = ctk.CTkButton(sidebar, text="New Version", image=icon_new, command=lambda: openLink("https://github.com/NicouHc/WidgetsProject-Extension"), **button_style_new_Version)
        btn_update.pack(fill='x', padx=10, pady=3, side='bottom')


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
    task_entry = ctk.CTkEntry(panel_notas, height=60, **text_input_Style)
    task_entry.pack(pady=10, padx=10)

    # Botón para agregar tareas
    add_button = ctk.CTkButton(panel_notas, text="+ Add Task", command=lambda: add_task(task_entry.get()), **button_style_2)
    add_button.pack(pady=10)
    
    display_tasks()# show tasks
    

    # shortcuts Pannel  ------------------------------------------------------------------------------------------
    
    panel_shortcuts = ctk.CTkFrame(main_container, **mini_Panel_Style)
    panel_shortcuts.pack(pady=10, padx=10, fill="both", expand=True)

    # Título del panel
    titleSettings = ctk.CTkLabel(panel_shortcuts, text="ShortCuts", text_color="white", font=ctk.CTkFont(size=20))
    titleSettings.grid(row=0, column=0, pady=10, padx=10)  # Coloca el título en la primera fila y ocupa 3 columnas

    # Frame para el canvas
    canvas = ctk.CTkCanvas(panel_shortcuts, width=300, height=240, bg="#171a21", highlightthickness=0)
    canvas.grid(row=1, column=0, columnspan=3, padx=20, pady=10, sticky="nsew")  # Usar columnspan para ocupar espacio

    # Agregar una Scrollbar lateral al canvas
    scrollbar = ctk.CTkScrollbar(panel_shortcuts, orientation="vertical", command=canvas.yview)
    scrollbar.grid(row=1, column=2, sticky="ns")  # Coloca la scrollbar al lado derecho

    # Configurar la scrollbar para el canvas
    canvas.configure(yscrollcommand=scrollbar.set)

    # Task frame
    global shortcuts_list
    shortcuts_list = ctk.CTkFrame(canvas, fg_color="transparent")  
    shortcuts_list.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Agregar el frame shortcuts_list al canvas como una ventana
    canvas.create_window((0, 0), window=shortcuts_list, anchor="nw")

    icons_shortcuts = ["Folder", "File", "Star", "Heart", "Pin", "Location", "Zap", "Trash", "Flower", "Coffe", "Bookmark", "Skull", "Lemon"]
    shortcut_combo_box = ctk.CTkComboBox(panel_shortcuts, values=icons_shortcuts, **comboBoxStyle)
    shortcut_combo_box.grid(row=2, column=0, pady=10, padx=10)

    # name for shortcut
    shortcut_name = ctk.CTkEntry(panel_shortcuts, height=30, **text_input_Style, placeholder_text="Shortcut Name")
    shortcut_name.grid(row=2, column=1, pady=10, padx=10)

    # shortcut color
    def choose_color():
        global color_shortcut
        # open color selector
        color_shortcut = colorchooser.askcolor()[1]
        if color_shortcut:
            color_button.configure(text=f"{color_shortcut}", text_color=color_shortcut)

    color_button = ctk.CTkButton(panel_shortcuts, text="Choose Color", command=choose_color, **button_style_2)
    color_button.grid(row=3, column=0, pady=10, padx=10)

    # directory shortcut
    shortcut_directory = ctk.CTkEntry(panel_shortcuts, height=30, **text_input_Style, placeholder_text="Directory")
    shortcut_directory.grid(row=3, column=1, pady=10, padx=10)

    # add shortcut
    global color_shortcut
    add_button = ctk.CTkButton(panel_shortcuts, text="+ Add Shortcut", **button_style_2, command=lambda: add_shortcut(shortcut_combo_box.get(), shortcut_directory.get(), shortcut_name.get(), color_shortcut))
    add_button.grid(row=3, column=2, pady=10, padx=10)

    panel_shortcuts.grid_rowconfigure(1, weight=1)  
    panel_shortcuts.grid_columnconfigure(0, weight=1) 

    display_shortcut()



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
    ctk.CTkCheckBox(panel_ajustes, text="Start on PC Startup", variable=var_startup, **checkboxStyle).grid(row=6, column=0, columnspan=2, pady=10)

    # browser setting
    ctk.CTkLabel(panel_ajustes, text="Browser:", text_color="white").grid(row=4, column=0, padx=10, pady=5)
    entry_browser = ctk.CTkEntry(panel_ajustes, width=250, **text_input_Style)  
    entry_browser.grid(row=4, column=1, padx=10, pady=5)
    
    global broweserSearch
    entry_browser.insert(0, broweserSearch)

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

def searchPanel():

    def search_info():
        global broweserSearch
        openLink(f'{broweserSearch}{search_entry.get()}')
        root.destroy()

    # Crear la ventana principal
    root = ctk.CTk()
    root.title(f"WidgetsProject Extension v{version} - Search")
    root.geometry("400x80")
    root.resizable(False, False)
    root.iconbitmap(currentPath + "./resources/icon.ico") 
    
    main_container2 = ctk.CTkFrame(root, fg_color="#12151a")
    main_container2.pack(fill='both', expand=True)


    # Campo de entrada de búsqueda
    text_input_Style = {
        "fg_color": "#12151a",        
        "corner_radius": 5,
        "border_width": 1.5,
        "border_color": "#565b5e",
        "text_color": "white",
    }

    search_buton = {
        "width": 40, 
        "height": 40, 
        "fg_color": "#12151a",

        "border_width": 1.5,
        "border_color": "#565b5e",

        "hover_color": "#22242b"
    }

    search_entry = ctk.CTkEntry(main_container2, width=300, height=40, placeholder_text="Search...", **text_input_Style)
    search_entry.grid(row=1, column=0, pady=20, padx=20)

    # Botón de búsqueda
    icon_search = ctk.CTkImage(Image.open("./resources/icon_search.png"), size=(20, 20))
    search_button = ctk.CTkButton(main_container2, text="", image=icon_search, command=search_info, **search_buton)
    search_button.grid(row=1, column=1, pady=10, padx=0)

    # Iniciar la ventana
    root.mainloop()

# START ALL ################################################################################
def preLoad():#load settings before start the program
    file_path = currentPath + '/settings.json'
    settings = load_settings(file_path)

    if not settings:
        print(style.RED + " *  ? " + style.ENDC + " Settings Not Found\n")
        mainPanel("panel_inicio")  # just open settings if there are no saved settings
    
def start_threads():# start cpu/ram/weather update threads
        global running
        cpuUsage = threading.Thread(target=obtener_info)
        
        if not cpuUsage.is_alive():
            running = True
            cpuUsage.start()
        else:
            pass

def tricon():# generate try icon 
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

# display shortcuts
@app.route('/shortcuts', methods=['GET'])
def get_shortcuts():
    global shortcuts
    return json.dumps(shortcuts, ensure_ascii=False)

# open folders
@app.route('/openStuff', methods=['POST'])
def open_stuff():
    data = request.get_json().get("data")  # obtain folder to open

    if(data == "Search"): #open mini browser
        searchPanel()

    elif(data == "Desktop"):
        path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        openLink(path)

    elif(data == "Documents"):
        path = os.path.join(os.environ['USERPROFILE'], 'Documents')
        openLink(path)

    elif(data == "Downloads"):
        path = os.path.join(os.environ['USERPROFILE'], 'Downloads')
        openLink(path)
    
    elif(data == "Terminal"):
        os.system("start cmd")

    else:
        openLink(data)

    return("1")

# run localhost
def run_flask_app():
    app.run(host='127.0.0.1', port=5000)



# main ################################################################################
if __name__ == "__main__":
    try:
   
        os.system(f"title Widgets Project v{version} && cls")
        print(style.RED + f"\n - Widgets Project Extension v{version}\n ------------------------------------ \n" + style.ENDC)

        print(style.RED + " * 1/6" + style.ENDC + " Console Visibility")
        console_visibility(2)

        print(style.RED + " * 2/6" + style.ENDC +  " Current Path")
        currentPath = obtain_current_dir()

        print(style.RED + " * 3/6" + style.ENDC +  " Define Startup Time")
        defineStartupTime()

        print(style.RED + " * 4/6" + style.ENDC +  " LocalHost sv")
        logger = logging.getLogger('werkzeug')
        logger.setLevel(logging.ERROR)  # prevent show  flask requests messages in debug console
        threading.Thread(target=run_flask_app).start() # start flask thread

        print(style.RED + " * 5/6" + style.ENDC +  " .json settings")
        preLoad()  # load settings

        print(style.RED + "\n * 6/6" + style.ENDC +  " tryicon menu\n")
        tricon()  # display tryicon menu

    except Exception as e: 
        print_Error(e)