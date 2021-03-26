<p align="center">
  <img src="assets/how-does-it-work.png" width="1200">
</p>

<p align="center">  
  <a href="https://github.com/gnome-pomodoro/gnome-pomodoro-tracking/actions?query=workflow%3APytest">
    <img src="https://github.com/gnome-pomodoro/gnome-pomodoro-tracking/workflows/Pytest/badge.svg">
  </a>
  <a href="LICENSE">  
    <img src="https://img.shields.io/github/license/gnome-pomodoro/gnome-pomodoro-tracking?style=flat-square" />
  </a>
  <a href=".pm/version.yml">
        <img src="https://img.shields.io/badge/dynamic/yaml?color=green&label=version&query=version.*&url=https://raw.githubusercontent.com/gnome-pomodoro/gnome-pomodoro-tracking/master/.pm/version.yml">
  </a>

</p>

# GNOME Pomodoro Tracking
It is a custom action for GNOME Pomodoro, that to connect any Time Tracking Software and create Time Entries.

## Contents

* [Requirements](#requirements)
* [Install](#install)
* [CLI](#cli)
* Plugins
  * [Toggl](./assets/toggl/README.md)
  * [Clockify](./assets/clockify/README.md)
  * [Odoo](./assets/odoo/README.md)
* [GNOME Pomodoro Settings](#gnome-pomodoro-settings)
* [Contributing](./CONTRIBUTING.md)
* [Tests](./tests/README.md)

## Requirements

* python3
* git
* [gnomepomodoro.org](https://gnomepomodoro.org)

## Install

```bash
# Install 
sh -c "$(curl -fsSL https://raw.githubusercontent.com/gnome-pomodoro/gnome-pomodoro-tracking/master/startup.sh)" "" --install

# Upgrade
sh -c "$(curl -fsSL https://raw.githubusercontent.com/gnome-pomodoro/gnome-pomodoro-tracking/master/startup.sh)" "" --upgrade

# Uninstall
sh -c "$(curl -fsSL https://raw.githubusercontent.com/gnome-pomodoro/gnome-pomodoro-tracking/master/startup.sh)" "" --uninstall

```

## CLI

```bash

usage: gnome-pomodoro-tracking [-h] [--plugin {odoo,clockify,toggl}] [-n NAME] 
                               [-r] [-k] [-s] 

optional arguments:
  -h, --help            show this help message and exit
  --plugin {odoo,clockify,toggl}
                        Select Time Tracking Software
  -n NAME, --name NAME  Set the name of the time entry (Pomodoro, short/long
                        break). If there is no active Pomodoro start a new
                        one.
  -r, --restart         Stop the Pomodoro & starts a new
  -k, --stop            Stop the Pomodoro
  -s, --status          Displays the summary of the Pomodoro

```

## GNOME Pomodoro Settings

`Preferences / Plugins ... / Custom Actions(Execute shell scripts) / Add `

```bash
gnome-pomodoro-tracking -gps "$(state)" -gpt "$(triggers)" -gpd "$(duration)" -gpe "$(elapsed)"
```

<p align="center">  
 <img src="assets/gnome-pomodoro-settings.gif" width="400"/>
</p>