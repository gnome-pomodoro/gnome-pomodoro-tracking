
# Introducing Gnome Pomodoro Tracking CLI

## Command Line
Use the command line to interact with the plugin:


```bash
usage: gnome-pomodoro-tracking [-h] [--plugin {odoo,clockify,toggl}] [-n NAME]
                               [-g TAG] [-r] [-k] [-s] [-w] [-p]
                               [--token TOGGL_TOKEN]
optional arguments:
  -h, --help            show this help message and exit
  --plugin {odoo,clockify,toggl}
                        Time Tracking Service
  -n NAME, --name NAME  Pomodoro name
  -g TAG, --tag TAG     Pomodoro tag
  -r, --restart         Pomodoro restart
  -k, --stop            Pomodoro stop
  -s, --status          Pomodoro status
  -e, --time-entry      Create time entry
  -m, --min-trace       Time minimal elapsed to track
  -d, --debug           Enable debug


```

If you don't have the plugin configured, here you can see how to configure it:
* [Toggl](toggl.md)
* [Clockify](clockify.md)
* [Odoo](odoo.md)


## Usage

### --time-entry

Allow create manually time entry, the time is in minutes.
```
gnome-pomodoro-tracking --time-entry 25
```

### --name
A name for the time entry, if you don't set a name, the plugin will use the default 'Pomodoro'.
```
gnome-pomodoro-tracking --name "My Entry Name"
```
If you want that remove name, execute:
```
gnome-pomodoro-tracking -n " "
```

### --tag
Add tag to the time entry, if you want add many tags, use `,` . e.g  `tag1,tag2,tag3`
```
gnome-pomodoro-tracking --tag "gnome-pomodoro"
```
If you want that remove tag, execute:
```
gnome-pomodoro-tracking -t " "
```
NOTE: 
* Is only supported by Toggl

### --min-trace
Allows you to set the minimum time (minutes) elapsed to be saved in the time tracking service.
```
gnome-pomodoro-tracking --min-trace 2 # 2 minutes elapsed
```
if you want that remove minimal tracking, execute:
```
gnome-pomodoro-tracking --min-trace 0
```