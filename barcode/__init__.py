#!/usr/bin/env python
# -*- coding: utf-8 --

from ean import *
from primitives import *
from imgs import *
from errors import *

def render(type_result, size, *arg):
    if not arg: raise EZekNoData()
    
    if type_result == 'svg':
        return '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1"
     baseProfile="full"
     xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     xmlns:ev="http://www.w3.org/2001/xml-events"
     width="%smm" height="%smm">
%s
</svg>''' % (size[0], size[1], '\n'.join(i.content_svg() for i in arg))

    else:
        raise EZUnknownFormat()
