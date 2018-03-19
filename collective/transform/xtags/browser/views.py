# -*- coding: utf-8 -*-
#from __future__ import unicode_literals, print_function
from Products.Five.browser import BrowserView
from plone import api
from lxml.etree import tostring
from collective.transform.xtags.quark_tagged_text import to_xml


class RenderFromXtags(BrowserView):
    """ quark xtags to html.    """

    def __call__(self, *args, **kw):
        return self.render_xtags()

    def render_xtags(self, tagged_text=""):
        """Return quark xtags as a stringified HTML document."""
        tagged_text = self.request.tagged_text
        #or self.context.qrktext
        #xtags = self.context.qrktext.encode('utf-8')

        try:
            element_tree = to_xml(tagged_text.decode('utf-8'))
            serialised_xml = tostring(element_tree, encoding='utf-8')
            return serialised_xml
            
        except:
            return '<p class="error">[rendering error]<p>'
