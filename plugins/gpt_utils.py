import re
import logging
import requests
import os 
import sys 

logging.basicConfig(
    filename="/tmp/gnome-pomodoro-tracking.log",
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG
)

logger = logging.getLogger("gnome-pomodoro-tracking")

def join_url(url, *paths):
    for path in paths:
        url = re.sub(r'/?$', re.sub(r'^/?', '/', path), url)
    return url

def println(*args):
    print(*args)
    
    if str(os.getenv("GP_TRACKING_ENV", "")).lower() == 'test':
        original_stdout = sys.stdout
        with open('/tmp/gnome-pomodoro-tracking.stdout', 'w') as f:
            sys.stdout = f
            print(*args)
            sys.stdout = original_stdout 


def printlg(info=None, warning=None, error=None, critical=None, debug=None, exception=None, *args,**kwargs):
    if info:
        logger.info(info, *args, **kwargs)
    elif warning:
        logger.warning(warning, *args, **kwargs)
    elif error:
        logger.error(error, *args, **kwargs)
    elif critical:
        logger.critical(critical, *args, **kwargs)
    elif debug:
        logger.debug(debug, *args, **kwargs)
    elif exception:
        logger.exception(exception, *args, True, **kwargs)
    else:
        raise Exception("Missing arg : info or warning or error or critical or debug")

def printtbl(rows, header=False):

    val = lambda v: "{:<12} ".format(v)

    if len(rows)>0 and header:
        line = ""
        for key in rows[0].keys():
            line += val(str(key).title())
        println(line)

    for row in rows:
        line =""
        for key in row.keys():
            line += val(row.get(key))
        println(line)

def make_request(method, url, **kwargs): 
        response = requests.request(method, url, **kwargs)
        if response.ok:
            return response.json()
        raise Exception(response.text)


