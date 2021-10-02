# Clockify

* Generate API Token at https://clockify.me/user/settings

![](img/clockify-token.png)

* Add token

  ```bash
  gnome-pomodoro-tracking --token TOKEN
  ```

* Workspaces

  ```bash
  # List
  gnome-pomodoro-tracking --workspaces
  # set 
  gnome-pomodoro-tracking --workspaces --set ID
  ```
  
* Projects

  ```bash
  # List
  gnome-pomodoro-tracking --projects
  # Set 
  gnome-pomodoro-tracking --projects --set ID
  ```