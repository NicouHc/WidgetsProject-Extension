![Logo](/resources/banner.png)

## Description

**Widgets Project Extension** is an executable that complements [Widgets Project Wallpaper](https://steamcommunity.com/sharedfiles/filedetails/?id=3137947556) of Wallpaper Engine and that allows you to access more options for your widgets, system information, weather updates and to-do notes. These widgets update in real time and are highly configurable through an intuitive settings panel.

## Features

- **CPU and RAM Monitoring**: Displays real-time CPU and RAM usage.
- **Weather Updates**: Get updated weather data using the [Open Meteo API](https://open-meteo.com).
- **Task Notes**: Manage your notes directly from the Extension.
- **Flexible Configuration**: Customize the project settings through a user-friendly graphical interface.

## How It Works

- **On the Script Side**: The script will retrieve the relevant information from the PC and generate a JavaScript file, such as `pc-info.js`. This file will contain a variable called `pc_info`, which will store two values: CPU usage and memory usage. The variable will be structured like this: `var pc_info = [23.4, 31.5];`, where `23.4` represents the percentage of CPU usage, and `31.5` represents the percentage of memory usage.

- **On the Wallpaper Side**: The wallpaper will refresh the content of the JavaScript file at regular intervals, allowing it to receive updates to the variable's values. This ensures that the most current CPU and memory usage information is displayed on the screen in real-time.

- [How to Use Video](https://youtu.be/1s-l17dJ2BE)

## More
if you have any question you can join our [Discord](https://discord.com/invite/63EUyQBZPm) or leave a comment on the wallpaper ❤️
