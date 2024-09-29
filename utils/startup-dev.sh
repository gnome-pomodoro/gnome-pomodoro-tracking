#!/bin/bash

cd YOUR_PROJECT_PATH
pipenv shell

echo "Custom action args"
for param in "$@"; do
    echo "arg: $param"
done
echo "--------------------"

python3 gnome_pomodoro_tracking/__main__.py "$@"

