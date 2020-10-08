
<p align="center">  
  <a href="LICENSE">  
    <img src="https://img.shields.io/github/license/josehbez/gp-tracking?style=flat-square" />
  </a>
   <a href="semv.toml">
    <img src="https://img.shields.io/badge/semv-2.0.1-green">
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
sh -c "$(curl -fsSL https://raw.githubusercontent.com/josehbez/gp-tracking/master/install.sh)"
```
### Upgrade

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/josehbez/gp-tracking/master/install.sh)" "" --upgrade
```

### Uninstall

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/josehbez/gp-tracking/master/uninstall.sh)"
```

### Plugins available

* [Clockify](./plugins/clockify/README.md)
* [Odoo](./plugins/odoo/README.md)
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
 <img src="gp-tracking-settings.gif"/>
</p>



