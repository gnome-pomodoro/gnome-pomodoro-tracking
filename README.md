<p align="center">
  <img src="assets/how-does-it-work.png" width="1200">
</p>

<p align="center">  
  <a href="LICENSE">  
    <img src="https://img.shields.io/github/license/josehbez/gp-tracking?style=flat-square" />
  </a>
   <a href="semv.toml">
    <img src="https://img.shields.io/badge/semv-2.2.0.beta.0-green">
  </a>
</p>

## Gnome Pomodoro Tracking

`gp-tracking` is a plugin for gnomepomodoro.org, connecting external time tracking providers.


### Requirements 

* python3 
* git 
* gnomepomodoro.org


### Install

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/josehbez/gp-tracking/v2.2/startup.sh)" "" --install
```
### Upgrade

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/josehbez/gp-tracking/v2.2/startup.sh)" "" --upgrade
```

### Uninstall

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/josehbez/gp-tracking/v2.2/startup.sh)" "" --uninstall
```

### Plugins available

* [Clockify](clockify.md)
* [Odoo](odoo.md)
* [Toggl](toggl.md)
* [Build a plugin](./plugins/README.md)



### Command line

* Set plugin 
```bash
gp-tracking --plugin NAME  
```

* Print resume pomodoro
```bash
gp-tracking --state 
```

* Add description, or if not running pomodoro start new pomodoro
```bash
gp-tracking --name "Add decription"
```

* Stop and start new pomodoro
```bash
gp-tracking --reset
```

* Kill  current pomodoro
```bash
gp-tracking --kill
```


## Gnome Pomodoro Settings 

* Launch gnome-pomodoro. `Preferences / Plugins ... / Custom Actions(Execute shell scripts) / Add `

```bash
gp-tracking -gps "$(state)" -gpt "$(triggers)" -gpd "$(duration)" -gpe "$(elapsed)"
```

<p align="center">  
 <img src="assets/gnome-pomodoro-settings.gif"/>
</p>



## Tests 
```bash
export GP_TRACKING_ENV=Test

export GP_TRACKING_CLOCKIFY_TOKEN=Token

export GP_TRACKING_TOGGL_TOKEN=Token

export GP_TRACKING_ODOO_URL=Url
export GP_TRACKING_ODOO_PASSWORD=Password
export GP_TRACKING_ODOO_USERNAME=User
export GP_TRACKING_ODOO_DATABASE=Db

pytest

```