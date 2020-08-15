# Gnome Pomodoro Tracking



### Pre-requirements 
* python3
* git 
* gnome-pomodoro

### Install

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/josehbez/gnome-pomodoro-tracking/master/install.sh)"

```

### Uninstall

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/josehbez/gnome-pomodoro-tracking/master/uninstall.sh)"
```



### Set plugin tracking

```bash
gp-tracking -p clockify
```

### Plugins available

* [clockify](./plugins/clockify/README.md)

### CLI short-cut
```bash
    # * if not running pomodoro, start new pomodoro
    gp-tracking -n "Add decription time entry"
    
    # * if running pmodoro, stop current pomodoro and start new
    gp-tracking -r
    # * if running pmodoro, kill current pomodoro
    gp-tracking -k
```

## Gnome-Pomodoro 

* Launch gnome-pomodoro. Preferences / Plugins ... / Custom Actions(Execute shell scripts)

![](img/plugins.png)

![](img/custom-actions.png)

* Launch gnome-pomodoro. Preferences / Custom actions ...  / add Action

```bash
gp-tracking -s $(state)  -t "$(triggers)" -d "$(duration)" -e "$(elapsed)"
```

![](img/action-clockify.png)


## LICENSE

[GPL V3.0]( ./LICENSE)