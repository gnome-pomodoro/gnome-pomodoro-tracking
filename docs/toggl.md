# Toggl Track Integration


###  Enable plugin

Copy and paste this command in terminal
```bash
gnome-pomodoro-tracking --plugin toggl
```

### Generate Your API Token:

* Visit your Toggl profile: https://track.toggl.com/profile
* Navigate to "API Tokens" and click "Create new token".

![](img/toggl-token.png)

Copy this command and replace `TOKEN` with your API token
```bash
gnome-pomodoro-tracking --token TOKEN
```
  

### Start tracking

Before you start tracking, you need to set up a workspace and project. It is usually set up once. If don't set up, it will use the first workspace and project.
 
Workspaces, you can list and set using this command this command.

List
```bash
gnome-pomodoro-tracking --workspaces
```
Set 
```bash
gnome-pomodoro-tracking --workspaces --set ID
```

Projects, you can list and set using this command this command.
List
```bash
  gnome-pomodoro-tracking --projects
```
Set
```bash 
  gnome-pomodoro-tracking --projects --set ID
```

For advanced CLI usage and customization, please refer to the guide: [introducing.md](introducing.md)
