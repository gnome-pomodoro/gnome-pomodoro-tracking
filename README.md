<p align="center">
  <img src="assets/how-does-it-work.png" width="1200">
</p>

<p align="center">  
  <a href="https://github.com/actions/toolkit/actions?query=Python test">
    <img src="https://github.com/josehbez/gp-tracking/workflows/Python test/badge.svg">
  </a>
  <a href="LICENSE">  
    <img src="https://img.shields.io/github/license/josehbez/gp-tracking?style=flat-square" />
  </a>
   <a href="semv.toml">
    <img src="https://img.shields.io/badge/semv-2.2.0.beta.0-green">
  </a>
  

</p>

## Gnome Pomodoro Tracking (gp-tracking)
It is a custom action for Gnome Pomodoro, whose main function is to connect with Time Tracking Software and create Time Entries.

### Plugins available

* [Clockify](assets/clockify/readme.md)
* [Odoo](assets/odoo/readme.md)
* [Toggl](assets/toggl/readme.md)

### Pre-requirements 

* python3 
* git 
* [gnomepomodoro.org](https://gnomepomodoro.org)


### Startup 

```bash
# Install 
sh -c "$(curl -fsSL https://raw.githubusercontent.com/josehbez/gp-tracking/v2.2/startup.sh)" "" --install

# Upgrade
sh -c "$(curl -fsSL https://raw.githubusercontent.com/josehbez/gp-tracking/v2.2/startup.sh)" "" 
--upgrade

# Uninstall
sh -c "$(curl -fsSL https://raw.githubusercontent.com/josehbez/gp-tracking/v2.2/startup.sh)" "" --uninstall

```

### CLI

```bash
# Select Time Tracking Software
gp-tracking --plugin NAME  

#Enter the name of the time entry. If there is no active Pomodoro start a new one.
gp-tracking --name NAME

# Displays the summary of the time entry 
gp-tracking --state

# Stop the active Pomodoro starts a new time entry
gp-tracking --reset

# Stop the active Pomodoro
gp-tracking --kill

```


## Gnome Pomodoro Settings 

`Preferences / Plugins ... / Custom Actions(Execute shell scripts) / Add `

```bash
gp-tracking -gps "$(state)" -gpt "$(triggers)" -gpd "$(duration)" -gpe "$(elapsed)"
```

<p align="center">  
 <img src="assets/gnome-pomodoro-settings.gif" width="400"/>
</p>



## Contributing
* [Build a plugin](./PLUGIN.md)

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