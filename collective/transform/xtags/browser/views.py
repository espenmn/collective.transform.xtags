# -*- coding: utf-8 -*-
#from __future__ import unicode_literals, print_function
from Products.Five.browser import BrowserView
from plone import api
from quark_tagged_text import to_xml
from lxml.etree import tostring


class RenderFromXtags(BrowserView):
    """ quark xtags to html.    """

    def __call__(self, *args, **kw):
        return self.render_xtags()

    def render_xtags(self):
        """Return quark xtags as a stringified HTML document."""
        xtags = self.context.xtags or None
        element_tree = to_xml(xtags)
        serialised_xml = tostring(element_tree, encoding='utf-8')
        return serialised_xml
