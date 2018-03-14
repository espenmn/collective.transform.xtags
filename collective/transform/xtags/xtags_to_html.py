# -*- coding: utf-8 -*-
from Products.PortalTransforms.interfaces import itransform
#import xtags
from lxml.etree import tostring

from pypeg2 import *
from pypeg2 import parse as pparse
from pypeg2.xmlast import create_tree
from lxml.etree import strip_tags, tostring, SubElement

from zope.interface import implements
try:
    from Products.PortalTransforms.interfaces import ITransform
    HAS_PLONE3 = False
except ImportError:
    from Products.PortalTransforms.interfaces import itransform
    HAS_PLONE3 = True

class XtagsToHtml:
    """Transform which converts from xtags to html"""

    if HAS_PLONE3:
        __implements__ = itransform
    else:
        implements(ITransform)


    __name__ = "xtags_to_html"
    output = "text/html"


    def __init__(self, name=None, inputs=('text/plain',)):
        self.config = {
            'inputs' : inputs,
        }
        self.config_metadata = {
            'inputs' : ('list',
                        'Inputs',
                        'Input(s) MIME type. Change with care.'),
            }
        if name:
            self.__name__ = name

    def name(self):
        return self.__name__

    def __getattr__(self, attr):
        if attr in self.config:
            return self.config[attr]
        raise AttributeError(attr)

    def convert(self, orig, data, **kwargs):
        pass

def register():
    return XtagsToHtml()
