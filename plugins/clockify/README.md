# Clockify 

* Generate token API in https://clockify.me/

![](img/clockify-token.png)

* Add token 

  ```bash
  gp-tracking -ct XtGTMKauDsdJ/E
  ```

* List workspaces

  ```bash
  gp-tracking -cw
  5e9ca62da2686b689ed5748d | workspace1
  5ec2c95096f46726f62f284d | workspace2
  ```

* Set workspaces

  ```
  gp-tracking -cw -w 5e9ca62da2686b689ed5748d
  ```

  * List projects

  ```bash
  gp-tracking -cp
  5eab188c991f8973bb9a1fa3 | project1
  5ea9c3f3737cf702b8e1d2c7 | project2

  ```

* Set workspaces

  ```
  gp-tracking -cp -w 5eab188c991f8973bb9a1fa3
  ```

