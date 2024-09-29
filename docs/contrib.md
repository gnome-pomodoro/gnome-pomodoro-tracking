# Contributtion Guide

## Setup your workspace 
* Install pipenv 
```bash
pip install pipenv
```

* Create a .env and export your python path, replace YOUR_PROJECT_PATH with your project path
```bash
export PYTHONPATH=$PYTHONPATH:YOUR_PROJECT_PATH
```

##  Install dependencies
```bash
pip install -r requirements.dev.txt
```

##  Set up GNOME Pomodoro

Use the below script to run the application, inside script replace YOUR_PROJECT_PATH with your project path.

```bash 
YOUR_PROJECT_PATH/utils/startup-dev.sh gnome-pomodoro-tracking -gps "$(state)" -gpt "$(triggers)" -gpd "$(duration)" -gpe "$(elapsed)"
```

## Lint using flake8
```bash
flake8 . --count --exit-zero --statistics
```

## Test using pytest
```bash
python -m unittest
```

## Publish on pypi

Build
```bash
python setup.py sdist bdist_wheel
``
Upload
```bash
python3 -m twine upload  --verbose dist/*
```