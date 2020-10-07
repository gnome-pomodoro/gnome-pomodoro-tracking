
<p align="center"><img src="docs/assets/DigbyShadows.png" width="360"></p>
<p align="center">  
  
  <a href="LICENSE">  
    <img src="https://img.shields.io/github/license/josehbez/gp-tracking?style=flat-square" />
  </a>
</p>


## Gnome Pomodoro Tracking


### Requirements 
* python3
* git 
* gnome-pomodoro

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



### Set plugin tracking

```bash
gp-tracking -p clockify
```

### Plugins available

* [Clockify](./plugins/clockify/README.md)
* [Odoo](./plugins/odoo/README.md)

### Build a plugin
[See guide build a plugin ](./plugins/README.md)

### CLI short-cut
* Resume 
```bash
    # print resume current pomodoro
    gp-tracking -s 
```
* Add description
```bash
    # * if not running pomodoro, start new pomodoro
    gp-tracking -n "Add decription time entry"
```
* Restart 
```bash
    # * if running pmodoro, stop current pomodoro and start new
    gp-tracking -r
```
* Kill 
```bash
    # * if running pmodoro, kill current pomodoro
    gp-tracking -k
```

## Gnome-Pomodoro 

* Launch gnome-pomodoro. Preferences / Plugins ... / Custom Actions(Execute shell scripts) / Add 

```bash
gp-tracking -gps $(state) -gpt "$(triggers)" -gpd $(duration) -gpe $(elapsed)
```

![](gp-tracking-settings.gif)


