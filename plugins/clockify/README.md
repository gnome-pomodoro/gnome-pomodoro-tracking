# Clockify 

* Generate token API in https://clockify.me/

![](img/clockify-token.png)

* Add token 

  ```bash
  gp-tracking -ct XtGTMKauDsdJ/E
  ```

* Workspaces
  * List
    ```bash
    gp-tracking -cw
    5e9ca62da2686b689ed5748d | workspace1
    5ec2c95096f46726f62f284d | workspace2
    ```

  * Set
    ```bash
    gp-tracking -cw -w 5e9ca62da2686b689ed5748d
    # short-cut
    cw=2020; gp-tracking -cw | grep $cw | cut -d " " -f1 | xargs -I{} gp-tracking -cw -w {}
  ```
  
* Projects
  * List
    ```bash
    gp-tracking -cp
    5eab188c991f8973bb9a1fa3 | project1
    5ea9c3f3737cf702b8e1d2c7 | project2
    ```

  * Set
  ```bash
    gp-tracking -cp -w 5eab188c991f8973bb9a1fa3
    # short-cut
    cp=me; gp-tracking -cp | grep $ccp | cut -d " " -f1 | xargs -I{} gp-tracking -cp -w {}
  ```

