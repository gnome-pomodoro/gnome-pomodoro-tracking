# Gnome-pomodoro & Clockify 





## Installation 

Clone 

```
git clone git@github.com:josehbez/gnome-pomodoro-clockify.git ~/.bin/gnome-pomodoro-clockify
```

Optional 

```
cd ~/.bin 
ln -s gnome-pomodoro-clockify/gp-clockify gp-clockify
```

### Clockify 

Generate token API in https://clockify.me/

![](/home/jhbez/soft/gnome-pomodoro-clockify/images/clockify-token.png)

Add token in  gp-clockify.cfg

![](/home/jhbez/soft/gnome-pomodoro-clockify/images/add-token-gp-clockify.png)

### Gnome-Pomodoro 

Is required enable Plugins (Custom Actions -- Execute shell scripts)

![](/home/jhbez/soft/gnome-pomodoro-clockify/images/plugins.png)

![](/home/jhbez/soft/gnome-pomodoro-clockify/images/custom-actions.png)

Add action Clockify  and 

```
python3 ~/.bin/gnome-pomodoro-clockify/gp-clockify.py -e $(state) -t "$(triggers)" -d $(duration) -l $(elapsed)
```

![](/home/jhbez/soft/gnome-pomodoro-clockify/images/action-clockify.png)

## LICENSE

[GNU General Public License v3.0]: ./LICENSE

