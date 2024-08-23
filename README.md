<h3>Download</h3>
$${\color{red}<b>WP-Extension.exe</b>}$$

<h3>Description</h3>
The <b>Widgets Project Extension</b> its an open source executable which works as an intermediary between the wallpaper and your pc and allows you to display information like <b>CPU usage</b>, <b>RAM usage</b>, or put your <b color="purple">ToDo-Notes</b> in to the wallpaper.

> On the <b href="https://steamcommunity.com/sharedfiles/filedetails/?id=3137947556">Script</b> side, it will obtain the corresponding information from the pc and will generate a js file that will contain a variable such as pc-info.js will generate a variable called var <b>pc_info</b> that will store 2 values, on the one hand the cpu usage and on the other hand. else the memory usage <b>pc_info = [23.4, 31.5];</b>.
> On the <b href="https://steamcommunity.com/sharedfiles/filedetails/?id=3137947556">Wallpaper</b> side, this will refresh the content of the js file every x time, allowing it to receive updates to the content of the variables and thus display them on the screen.

The script includes:
* <b>Configuration Menu</b> accessible from a system tray icon, allowing you to adjust settings such as the wallpaper directory and geographical coordinates for weather updates. This provides a personalized and dynamic experience for displaying information on your wallpaper.
* Additionally, extension allows you to manage <b>Personal Notes</b> directly from the wallpaper interface. Notes can be created, edited, and saved, and are stored in a JavaScript file (<b>ToDoNotes.js</b>), making it easy to view and manage them on the wallpaper.                                          
* The Extension Continuously monitors <b>CPU</b> and <b>RAM</b> usage using the <b>psutil</b> library. This data is recorded in a JavaScript file (<b>pc-info.js</b>), which the wallpaper uses to show real-time system performance information.
* This ensures that the wallpaper accurately reflects the current performance of your machine.
* Finally, the script integrates <b>Weather</b> data retrieval through the <b href="https://open-meteo.com">Open-Meteo API</b>. Based on the provided <b>latitude</b> and <b>longitude</b>, the script fetches and stores weather information in a JavaScript file (<b>weather-data.js</b>). This information is automatically updated every five hours, keeping the wallpaper up-to-date with the latest weather conditions.
