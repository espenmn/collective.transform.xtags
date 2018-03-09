# -*- coding: utf-8 -*-
from zope.interface import implements
from xml.etree.ElementTree import XML, tostring, Element
from htmllaundry import sanitize

from Products.PortalTransforms.interfaces import ITransform
from Products.PortalTransforms.utils import log



class xtags_to_html():
    """Transform which converts from XTAGS to HTML"""

    implements(ITransform)

    __name__ = "xtags_to_html"
    output   = "text/html"

    def __init__(self,name=None):
        if name:
            self.__name__=name

    def name(self):
        return self.__name__

    def convert(self, data, cache, **kwargs):
        bodydom = Element('div')
        xtagsdom = XML(data)
        ns = xtagsdom.tag.strip('x-tags')
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
    return xtags_to_html()
