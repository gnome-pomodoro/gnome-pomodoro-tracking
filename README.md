<p align="center">
  <img src="assets/how-does-it-work.png" width="1200">
</p>

<p align="center">  
  <a href="https://github.com/josehbez/gp-tracking/actions?query=workflow%3APytest">
    <img src="https://github.com/josehbez/gp-tracking/workflows/Pytest/badge.svg">
  </a>
  <a href="LICENSE">  
    <img src="https://img.shields.io/github/license/josehbez/gp-tracking?style=flat-square" />
  </a>
   <a href="semv.toml">
    <img src="https://img.shields.io/badge/semv-3.0.0-green">
  </a>
  

</p>

## Gnome Pomodoro Tracking (gp-tracking)
It is a custom action for Gnome Pomodoro, that to connect any Time Tracking Software and create Time Entries.

## Contents

* Requirements
* Install
* CLI
* Plugins
  * Clockify
  * Toggl
  * Odoo 
* Settings gnome-pomodoro 
* Contributing
* Tests

## Requirements

* python3
* git 
* [gnomepomodoro.org](https://gnomepomodoro.org)

## Install

```bash
# Install 
sh -c "$(curl -fsSL https://raw.githubusercontent.com/josehbez/gp-tracking/master/startup.sh)" "" --install

# Upgrade
sh -c "$(curl -fsSL https://raw.githubusercontent.com/josehbez/gp-tracking/master/startup.sh)" "" --upgrade

# Uninstall
sh -c "$(curl -fsSL https://raw.githubusercontent.com/josehbez/gp-tracking/master/startup.sh)" "" --uninstall

```

## CLI

```bash
# Select Time Tracking Software
gp-tracking --plugin NAME  

#Enter the name of the time entry. If there is no active Pomodoro start a new one.
gp-tracking --name NAME

# Displays the summary of the time entry 
gp-tracking --status

# Stop the active Pomodoro, starts a new time entry
gp-tracking --restart

# Stop the active Pomodoro
gp-tracking --stop

```

## Plugins

### Clockify

[Guidelines](./assets/clockify/readme.md) 

### Toggl

[Guidelines](./assets/toggl/readme.md) 

### Odoo

[Guidelines](./assets/odoo/readme.md) 

## Gnome Pomodoro Settings 

`Preferences / Plugins ... / Custom Actions(Execute shell scripts) / Add `

```bash
gp-tracking -gps "$(state)" -gpt "$(triggers)" -gpd "$(duration)" -gpe "$(elapsed)"
```

<p align="center">  
 <img src="assets/gnome-pomodoro-settings.gif" width="400"/>
</p>


## Contributing

[Guidelines](./CONTRIBUTING.md) 

## Tests 
```bash
export GP_TRACKING_ENV=Test

# Params clockify
export GP_TRACKING_CLOCKIFY_TOKEN=Token
# Params toggl
export GP_TRACKING_TOGGL_TOKEN=Token
# Params odoo
export GP_TRACKING_ODOO_URL=Url
export GP_TRACKING_ODOO_PASSWORD=Password
export GP_TRACKING_ODOO_USERNAME=User
export GP_TRACKING_ODOO_DATABASE=Db

# run tests
pytest
```