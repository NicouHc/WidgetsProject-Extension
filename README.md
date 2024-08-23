# Widgets Project Extension

![Logo](icon.ico)

## Description

**Widgets Project Extension** is an executable that complement with [Widgets Project Wallpaper](https://steamcommunity.com/sharedfiles/filedetails/?id=3137947556) that allows you to add customizable widgets to your desktop, such as system information, weather updates, and task notes. These widgets are updated in real-time and are highly configurable through an intuitive settings panel.

## Features

- **CPU and RAM Monitoring**: Displays real-time CPU and RAM usage.
- **Weather Updates**: Get updated weather data every 5 hours using the Open Meteo API.
- **Task Notes**: Manage your task notes directly from the desktop.
- **Flexible Configuration**: Customize the project settings through a user-friendly graphical interface.

## How It Works

- **On the Script Side**: The script will retrieve the relevant information from the PC and generate a JavaScript file, such as `pc-info.js`. This file will contain a variable called `pc_info`, which will store two values: CPU usage and memory usage. The variable will be structured like this: `var pc_info = [23.4, 31.5];`, where `23.4` represents the percentage of CPU usage, and `31.5` represents the percentage of memory usage.
- **On the Wallpaper Side**: The wallpaper will refresh the content of the JavaScript file at regular intervals, allowing it to receive updates to the variable's values. This ensures that the most current CPU and memory usage information is displayed on the screen in real-time.

## More

if u have any question you can join our [Discord](https://discord.com/invite/63EUyQBZPm) or send an comment on the wallpaper <3
