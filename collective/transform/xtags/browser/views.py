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

    def render_xtags(self,):
        """Return quark xtags as a stringified HTML document."""
        tagged_text = self.request.tagged_text
        #or self.context.qrktext

        import pdb; pdb.set_trace()
        try:
            element_tree = to_xml(self.request.tagged_text)
            serialised_xml = tostring(element_tree, encoding='utf-8')
            return serialised_xml
        except:
            return '<p class="error">[rendering error]<p>'
