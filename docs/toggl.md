# Toggl Track

* Generate  API Token at https://track.toggl.com/profile

![](img/toggl-token.png)

* Add token

  ```bash
  gnome-pomodoro-tracking --token TOKEN
  ```

* Workspaces

  ```bash
  # List
  gnome-pomodoro-tracking --workspaces
  # Set 
  gnome-pomodoro-tracking --workspaces --set ID
  ```

* Projects

  ```bash
  # List 
  gnome-pomodoro-tracking --projects
  # Set 
  gnome-pomodoro-tracking --projects --set ID
  ```

* Tags

  ```bash
  # Add tag
  gnome-pomodoro-tracking --tag tag-name
  gnome-pomodoro-tracking --tag tag-name,tag-name2
  ```

  
