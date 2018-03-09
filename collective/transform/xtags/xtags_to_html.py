# -*- coding: utf-8 -*-
from zope.interface import implements

from elementtree.ElementTree import XML, tostring, Element

from htmllaundry import sanitize


class XTAGS_to_HTML():
    """Transform which converts from XTAGS to HTML"""

    implements(ITransform)

    __name__ = "xtags_to_html"
    inputs   = ("text/xtags",)
    output   = "text/html"

    def __init__(self,name=None):
        if name:
            self.__name__=name

    def name(self):
        return self.__name__

    def convert(self, data, cache, **kwargs):
        bodydom = Element('div')
        xtagsdom = XML(data)
        ns = xtagsdom.tag.strip('xtags')
        placemarks = xtagsdom.findall('.//%sPlacemark' % ns)
        for placemark in placemarks:
            titles = placemark.findall(ns + 'name')
            for title in titles:
                t = Element('h2')
                t.text = title.text
                bodydom.append(t)

            descriptions = placemark.findall(ns+'description')
            for desc in descriptions:
                if desc.text:
                    text = sanitize(desc.text.strip())
                    d = XML('<div>' + text + '</div>')
                    bodydom.append(d)

        body = tostring(bodydom)
        cache.setData(body)
        return cache

def register():
    return xtags_to_HTML()
