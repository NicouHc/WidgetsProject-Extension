![Logo](/resources/banner.png)

## Description

**Widgets Project Extension** is an executable that complements [Widgets Project Wallpaper](https://steamcommunity.com/sharedfiles/filedetails/?id=3137947556) of Wallpaper Engine and that allows you to access more options for your widgets, system information and to-do notes. These widgets update in real time and are highly configurable through an intuitive settings panel.

## Features

- **CPU, GPU and RAM Monitoring**: Displays real-time CPU, GPU and RAM usage.
- **Battery Charge**: Displays current Battery Charge percent.
- **ToDo Notes**: Manage your notes directly from the Extension.
- **Shortcuts**: Create and display your own shortcuts inside the wallpaper.
- **Search Bar**: Just a search bar for find information.
- **Easy Configuration**: Customize the project settings through a user-friendly graphical interface.

## How It Works

- **On the Script Side**: It retrieves system information using the `psutil` library, such as CPU usage, RAM usage, and battery charge. It also manages a to-do list and can display custom notes or other relevant data that the user wants to track. Using `Flask` as a local server, the script sends this information via localhost, allowing the wallpaper to fetch and display it in real-time.

- **On the Wallpaper Side**:  The wallpaper uses javaScripts `fetch` to periodically request the system information from the LocalHost. This enables the wallpaper to dynamically update and display CPU, memory, battery usage, and any user-defined notes or to-do items, providing a real-time system monitor right on the desktop.

## More
- [Video Review v2.0.4 (outdated)](https://youtu.be/1s-l17dJ2BE)
- if you have any question you can join our [Discord](https://discord.com/invite/63EUyQBZPm) or leave a comment on the wallpaper ❤️
