# -*- coding: utf-8 -*-
# Copyright (c) 2021 The Project GNOME Pomodoro Tracking Authors
import re
import requests

def join_url(url, *paths):
    for path in paths:
        url = re.sub(r'/?$', re.sub(r'^/?', '/', path), url)
    return url

def printtbl(rows, header=False):

    def val(v):
        return "{:<12} ".format(v)

    if len(rows) > 0 and header:
        line = ""
        for key in rows[0].keys():
            line += val(str(key).title())
        print(line)

    for row in rows:
        line = ""
        for key in row.keys():
            line += val(row.get(key))
        print(line)

def make_request(method, url, **kwargs):
    """
        Deprecated: use instanced GTPPlugin,make_request
    """
    response = requests.request(method, url, **kwargs)
    if response.ok:
        return response.json()
    raise Exception(response.text)
