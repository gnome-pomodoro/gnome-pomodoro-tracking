
# Introducing

### Set/Switching between time tracking services

```
gnome-pomodoro-tracking --plugin toggl
```

``` 
gnome-pomodoro-tracking --plugin clockify
```

### Try credentials
Review the plugin documentation to configure the token.
* [Toggl](toggl.md)
* [Clockify](clockify.md)
* [Odoo](odoo.md)

Finally run this command to create a time entry.
```
gnome-pomodoro-tracking --time-entry 25
```

### Add name
```
gnome-pomodoro-tracking --name "My Entry Name"
```
If you want that remove name, execute:
```
gnome-pomodoro-tracking -n " "
```

### Add tag
Admit one tag or many tags using `,` . e.g  `tag1,tag2,tag3`
```
gnome-pomodoro-tracking --tag "gnome-pomodoro"
```
If you want that remove tag, execute:
```
gnome-pomodoro-tracking -t " "
```
NOTE: Check the plugin documentation if it supports tags.

### Minimal tracking
Allows you to set the minimum time (minutes) elapsed to be saved in the time tracking service.

```
gnome-pomodoro-tracking --min-trace 2 # 2 minutes elapsed
```
If you want that remove minimal tracking, execute:
```
gnome-pomodoro-tracking --min-trace 0
```