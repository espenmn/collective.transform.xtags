# -*- coding: utf-8 -*-
#from __future__ import unicode_literals, print_function
from Products.Five.browser import BrowserView
#from plone import api
from lxml.etree import tostring
from collective.transform.xtags.quark_tagged_text import to_xml

import re

class RenderFromXtags(BrowserView):
    """ quark xtags to html.    """

    def __call__(self, *args, **kw):
        return self.render_xtags()

    def render_xtags(self, tagged_text=""):
        """Return quark xtags as a stringified HTML document."""
        #tagged_text = self.request.tagged_text

        #remove * in tags
        #pattern = re.compile(r"\<.*?\>")
        #tagged_text = pattern.sub(lambda match: match.group(0).replace('*', "") ,self.request.tagged_text)

        #remove spaces in style sheets
        pattern = re.compile(r"\@.\ ?\:")
        tagged_text = pattern.sub(lambda match: match.group(0).replace(" ", ""), tagged_text)


        #not sure why this is needed,
        #tagged_text = tagged_text.replace("\r", "")
        #tagged_text = tagged_text.replace(">@", "> \n@")
        #tagged_text = tagged_text.replace("\<\\c\>", "\<\\c\> \\n")
        #tagged_text = tagged_text.replace("\<\\b\>", "\<\\b\> \\n")
        #tagged_text = tagged_text.replace("@\\ :", "@")


        try:
            element_tree = to_xml(tagged_text.decode('utf-8'))
            serialised_xml = tostring(element_tree, encoding='utf-8')
            return serialised_xml

        except:
            return '<p class="error">[rendering error]<p>'
