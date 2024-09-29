<p align="center">
  <img src="docs/img/how-does-it-workv4.png" width="1200">
</p>

<p align="center">  
  <!--a href="https://github.com/gnome-pomodoro/gnome-pomodoro-tracking/actions?query=workflow%3APytest">
    <img src="https://github.com/gnome-pomodoro/gnome-pomodoro-tracking/workflows/Pytest/badge.svg">
  </a-->
  <a href="LICENSE">  
    <img src="https://img.shields.io/github/license/gnome-pomodoro/gnome-pomodoro-tracking?style=flat-square" />
  </a>
  <a>
       <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gnome-pomodoro-tracking">

  </a>
</p>

# Welcome to Gnome Pomodoro Tracking!
Our plugin integrates with Toggl, Clockify, and Odoo to provide accurate time logging for your tasks and projects.


----
## Getting Started

### 1. Install
To get started, simply install the plugin using pip:

```bash
pip3 install -U gnome-pomodoro-tracking
```
 


### 2. Set Up GNOME Pomodoro:


* Open Gnome Pomodoro Preferences.
* Navigate to "Plugins" > "Custom Actions (Execute shell scripts)".
* Click "Add" and paste the following command:

```bash
gnome-pomodoro-tracking -gps "$(state)" -gpt "$(triggers)" -gpd "$(duration)" -gpe "$(elapsed)"
```

<p align="center">  
 <img src="docs/img/gnome-pomodoro-settings.gif" width="400"/>
</p>

### 3. Choose Your Time Tracking Service

We support three popular services:
* **Toggl**:  [Learn More](docs/toggl.md)
* **Clockify**: [Learn More](docs/clockify.md)
* **Odoo**: [Learn More](docs/odoo.md)



### 4. Command line 

For advanced CLI usage and customization, please refer to the guide: [introducing.md](docs/introducing.md)




