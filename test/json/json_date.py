#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This module is used to provide a json-extend part for 
    datetime/date serialization.
    @author Alex
    @date 2015/03/29
"""
import json
from datetime import date
from datetime import datetime

class JsonExtendEncoder(json.JSONEncoder):
    """
        This class provide an extension to json serialization for datetime/date.
    """
    def default(self, o):
        """
            provide a interface for datetime/date
        """
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, o)

if __name__ == '__main__':
    d = {'now': datetime.now(), 'today': date.today(), 'i': 100}
    ds = json.dumps(d, cls=JsonExtendEncoder)
    print ("ds type:", type(ds), "ds:", ds)
    l = json.loads(ds)
    print ("l  type:", type(l), "ds:", l)