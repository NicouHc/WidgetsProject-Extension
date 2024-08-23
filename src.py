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
currentPath =  os.path.dirname(sys.argv[0])


# -----------------------


def hide_console():
    #Oculta la ventana de la consola en Windows.
    
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()  # Obtiene el identificador de la ventana de la consola
    if hwnd != 0:
        ctypes.windll.user32.ShowWindow(hwnd, 0)  # SW_HIDE = 0

def show_console():
    #Muestra la ventana de la consola en Windows.
   
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()  # Obtiene el identificador de la ventana de la consola
    if hwnd != 0:
        ctypes.windll.user32.ShowWindow(hwnd, 5)  # SW_SHOW = 5

# -----------------------
# CUP RAM Usage
def obtener_info(intervalo=1):
    global running
    while running:

        uso_cpu = psutil.cpu_percent(interval=intervalo)
        uso_ram = psutil.virtual_memory().percent
        

        # Generar el contenido del archivo JS
        js_content = f"var pc_info = [{uso_cpu }, {uso_ram}];\n"

        # Escribir los valores en el archivo pc-info.js
        with open(wallpaperPath + '/files/info/' + 'pc-info.js', 'w') as file:
            file.write(js_content)

        time.sleep(1)  # Pausa de x segundos

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
            response.raise_for_status()  # Lanza un error si la solicitud falla
            weather_data = response.json()
            
            # Convertir el JSON a un formato JavaScript
            js_content = f"var weather_data = {json.dumps(weather_data, indent=4)};\n"
            
            # Guardar el JS en un archivo
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
        directory = entry_directory.get()
        latitud = entry_latitude.get()
        longitud = entry_longitude.get()
        start_on_startup = var_startup.get()

        if os.path.exists(directory + "/files/info"):
            settings = {
                "directory": directory,
                "longitud": longitud,
                "latitud": latitud,
                "start_on_startup": start_on_startup
            }
            save_settings(currentPath + '/settings.json', settings)
            set_startup(start_on_startup)  # Configura el inicio automático
            ventana.destroy()
        else:
            ctk.CTkMessageBox.show_error("Error", "Invalid Path.")

    ventana = ctk.CTk()
    ventana.title("Widgets Project - Settings")
    ventana.iconbitmap(currentPath + "/icon.ico")  
    
    # Ajusta el tamaño de la ventana
    ventana.geometry("430x200")  # Aumenta el tamaño para incluir el checkbox

    ctk.CTkLabel(ventana, text="Wallpaper Directory:").grid(row=0, column=0, padx=10, pady=5)
    entry_directory = ctk.CTkEntry(ventana, width=250)  # Aumenta el ancho del campo de entrada
    entry_directory.grid(row=0, column=1, padx=10, pady=5)

    ctk.CTkLabel(ventana, text="Latitude:").grid(row=1, column=0, padx=10, pady=5)
    entry_latitude = ctk.CTkEntry(ventana, width=250)  # Aumenta el ancho del campo de entrada
    entry_latitude.grid(row=1, column=1, padx=10, pady=5)

    ctk.CTkLabel(ventana, text="Longitude:").grid(row=2, column=0, padx=10, pady=5)
    entry_longitude = ctk.CTkEntry(ventana, width=250)  # Aumenta el ancho del campo de entrada
    entry_longitude.grid(row=2, column=1, padx=10, pady=5)

    var_startup = ctk.BooleanVar()
    ctk.CTkCheckBox(ventana, text="Start on Windows Startup", variable=var_startup).grid(row=3, column=0, columnspan=2, pady=10)

    ctk.CTkButton(ventana, text="Save", command=guardar_configuracion).grid(row=4, column=0, columnspan=2, pady=10)

    # Rellena los campos con los valores actuales
    entry_directory.insert(0, wallpaperPath)
    entry_latitude.insert(0, latitude)
    entry_longitude.insert(0, longitude)
    var_startup.set(start_on_startup)

    ventana.mainloop()

def set_startup(enable):
    #Configura el programa para que inicie con Windows o desactiva el inicio automático.

    script_path = sys.argv[0]  # Obtiene la ruta absoluta del script
    
    key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    value = "WidgetsProjectExtension"  # Nombre que aparecerá en el registro

    try:
        # Abre la clave del registro
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE)
        
        if enable:
            # Establece el valor del registro para que el programa inicie con Windows
            winreg.SetValueEx(reg_key, value, 0, winreg.REG_SZ, script_path)
            print("Program set to start with Windows.")
        else:
            # Elimina el valor del registro para desactivar el inicio automático
            winreg.DeleteValue(reg_key, value)
            print("Program removed from startup.")
        
        # Cierra la clave del registro
        winreg.CloseKey(reg_key)
    except Exception as e:
        print(f"Error: {e}")


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

    # Rellena el área de texto con el contenido actual
    if isinstance(notes_text, list):
        text_area.insert("1.0", "\n".join(notes_text))
    else:
        text_area.insert("1.0", notes_text)

    ventana.mainloop()

def leer_notas_js():
    #Lee el archivo notas.js y actualiza la variable global notes_text
    global notes_text
    try:
        with open(wallpaperPath + "/files/info/" + "ToDoNotes.js", "r") as file:
            contenido = file.read()
            # Encuentra el inicio y fin del contenido del array
            start = contenido.find('[')
            end = contenido.rfind(']')
            
            if start != -1 and end != -1:
                # Extrae el contenido del array
                array_texto = contenido[start:end + 1]
                try:
                    # Usa json.loads para convertir el contenido en una lista
                    notes_text = json.loads(array_texto)
                except json.JSONDecodeError:
                    notes_text = []
            else:
                notes_text = []
    except FileNotFoundError:
        notes_text = []

def actualizar_notas_js(array_notas):
    #Guarda un array de notas en un archivo JS
    with open(wallpaperPath + "/files/info/" + "ToDoNotes.js", "w") as file:
        # Convierte el array de notas a una cadena de texto en formato de array JavaScript
        notas_js = json.dumps(array_notas, ensure_ascii=False)
        file.write(f'var todoNotes = {notas_js};\n')

def guardar_notas():
    #Obtiene el texto del widget y actualiza el archivo JS
    global notes_text
    notas_texto = text_area.get("1.0", "end").strip()
    # Divide el texto en líneas y las convierte en un array de notas
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

    # Descripción de la aplicación
    description_label = ctk.CTkLabel(help_window, text="Widgets Project Extension for WallpaperEngine ")
    description_label.pack(pady=20)

    # open link
    def openLink(link):
        if link:
            os.system(f'start {link}')

    button_frame = ctk.CTkFrame(help_window)
    button_frame.pack(pady=10)

    join_button = ctk.CTkButton(button_frame, text="Join our Discord", command=lambda: openLink("https://discord.com/invite/63EUyQBZPm"))
    join_button.pack(side="left", padx=10)

    join_button2 = ctk.CTkButton(button_frame, text="Buy me a Coffee", command=lambda: openLink("https://www.paypal.com/donate/?hosted_button_id=UBDDRKEZ4XABE"))
    join_button2.pack(side="left", padx=10)

    help_window.mainloop()

# -----------------------

def preLoad():
    file_path = currentPath + '/settings.json'
    settings = load_settings(file_path)

    if not settings:
        abrir_configuracion()  # Solo abre la configuración si no hay configuraciones guardadas
    menu()

def exit_app(icon):
    global running
    running = False
    icon.stop()
    
    os._exit(0)

def menu():
    cpuUsage = threading.Thread(target=obtener_info)
    weatherRefresh = threading.Thread(target=weather)
    
    os.system("title . && cls")

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
        show_console()
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")
