# Clockify 

### Clockify 

Generate token API in https://clockify.me/

![](img/clockify-token.png)

Add token in  gp-clockify.cfg

<!-- ![](img/add-token-gp-clockify.png) -->

### Gnome-Pomodoro 

Is required enable Plugins (Custom Actions -- Execute shell scripts)

![](img/plugins.png)

![](img/custom-actions.png)

Add action Clockify  and 

```
python3 ~/.bin/gnome-pomodoro-clockify/gp-clockify.py -e $(state) -t "$(triggers)" -d $(duration) -l $(elapsed)
```

![](img/action-clockify.png)
