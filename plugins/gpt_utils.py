# -*- coding: utf-8 -*-
# Copyright (c) 2021 The Project GNOME Pomodoro Tracking Authors
import re
from datetime import datetime

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

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

def find_by_id(rows: list, id: str):
    """
        params:
            rows: [{'id': 2},{'id': 1}]
            id: 1
        return:
            None,dict
    """
    for row in rows:
        for key in row.keys():
            if key == 'id' and str(row.get(key)) == id:
                return row
    return None

def only_columns(rows: list, colums: list = ['id', 'name']):
    """
        params:
            rows: [{'id': 2, 'name': 'A'},{'id': 1, 'name': 'B'}]
            id: 1
        return:
            list
    """
    new_rows = []
    for row in rows:
        new_row = {}
        for column in colums:
            new_row.update({ column: row.get(column, None)})
        new_rows.append(new_row)
    return new_rows

def config_attrs(gpt, section: str, attrs: list, formatter=None):
    """
        params:
            gpt: GPTracking
            section: pomodoro
            attrs: ['name', 'type']
            formatter: status
        return:
            list
    """
    rows = []
    for attr in attrs:
        try:
            val = gpt.config.get(section, attr)
            if formatter is not None and formatter == 'status':
                key = str(str(attr).split('_')[0]).title()
                rows.append({'key': key, 'value': val})
            else:
                rows.append({'key': attr, 'value': val})
        except Exception as e:
            pass
    return rows

def config_attr(gpt, section: str, attr: str, val: any = False):

    def add_attr():
        gpt.config.set(section, attr, val)
        gpt._write_config()

    try:
        if val is False:
            return {'key': attr, 'value': gpt.config.get(section, attr)}

        if section in gpt.config.sections():
            add_attr()
        else:
            gpt.config.add_section(section)
            gpt._write_config()
            add_attr()
        return {'key': attr, 'value': val}
    except Exception as e:
        gpt.logger.critical(e)
    return None

def time_elapsed(dtstart, dtend, formatter="seconds"):
    try:
        if isinstance(dtstart, str) and isinstance(dtend, str):
            dt_start = datetime.strptime(dtstart, DATETIME_FORMAT)
            dt_end = datetime.strptime(dtend, DATETIME_FORMAT)
        elapsed = dt_end - dt_start
        seconds = elapsed.total_seconds()
        if formatter == 'minutes':
            return seconds / 60.0
        return seconds
    except Exception as e:
        pass
    return 0

def now():
    return datetime.utcnow().strftime(DATETIME_FORMAT)