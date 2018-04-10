# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import zope.component
import zope.interface
import zope.schema.interfaces
from z3c.form import interfaces
from z3c.form import widget
from z3c.form.browser import text

from lxml.etree import tostring, fromstring
from collective.transform.xtags.quark_tagged_text import to_xml
#from collective.transform.xtags.interfaces import IXtagsSettings

#from plone.memoize import forever
from plone.memoize.view import memoize, memoize_contextless


import logging as log

#import re

class IXtagsWidget(interfaces.IWidget):
    """Xtags widget."""


class XtagsWidget(text.TextWidget):
    """Xtags Widget"""
    
    #@forever.memoize
    @memoize
    def get_xtags(self):
        tagged_text = self.value
        log.info('getting xtags!')
        try:
            element_tree = to_xml(tagged_text, extra_tags_to_keep={}, css=True)
            serialised_xml = tostring(element_tree, encoding='utf-8')
            return serialised_xml

        except:
            return '<p class="error">[rendering error]<p>'

    zope.interface.implementsOnly(IXtagsWidget)

def XtagsFieldWidget(field, request):
    """IFieldWidget factory for XtagsWidget."""
    return widget.FieldWidget(field, XtagsWidget(request))