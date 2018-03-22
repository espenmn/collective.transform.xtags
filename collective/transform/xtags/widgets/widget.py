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


#import lxml.html
#from lxml.html.clean import Cleaner

class IXtagsWidget(interfaces.IWidget):
    """Xtags widget."""


class XtagsWidget(text.TextWidget):
    """Xtags Widget"""

    def get_xtags(self):
        #there must be a quicker way to do this (?)
        tagged_text = self.value.replace("\r", "")
        #not sure why this is needed,
        #but <* on same line breaks the rendering
        #tagged_text = tagged_text.replace("<*", "\n<*")
        tagged_text = tagged_text.replace("<*", " <*")
        tagged_text = tagged_text.replace(">@", "> \n@")
        tagged_text = tagged_text.replace("<*", "<")
        #tagged_text = tagged_text.replace(" <*", "\n<*")
        #tagged_text = tagged_text.replace("<", "\n<")


        try:
            element_tree = to_xml(tagged_text)
            serialised_xml = tostring(element_tree, encoding='utf-8')
            return serialised_xml

        except:
            return '<p class="error">[rendering error]<p>'

    zope.interface.implementsOnly(IXtagsWidget)


def XtagsFieldWidget(field, request):
    """IFieldWidget factory for XtagsWidget."""
    return widget.FieldWidget(field, XtagsWidget(request))
