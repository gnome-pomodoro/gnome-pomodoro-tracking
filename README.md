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

![](images/clockify-token.png)

Add token in  gp-clockify.cfg

![](images/add-token-gp-clockify.png)

### Gnome-Pomodoro 

Is required enable Plugins (Custom Actions -- Execute shell scripts)

![](images/plugins.png)

![](images/custom-actions.png)

Add action Clockify  and 

```
python3 ~/.bin/gnome-pomodoro-clockify/gp-clockify.py -e $(state) -t "$(triggers)" -d $(duration) -l $(elapsed)
```

![](images/action-clockify.png)

## LICENSE

[GNU General Public License v3.0]( ./LICENSE)