from __future__ import unicode_literals, print_function

import zope.component
import zope.interface
import zope.schema.interfaces

from z3c.form import interfaces
from z3c.form import widget
from z3c.form.browser import text

#from plone import api
#from collective.transform.xtags.interfaces import IXtagsSettings



class IXtagsWidget(interfaces.IWidget):
    """Xtags widget."""


class XtagsWidget(text.TextWidget):
    """Xtags Widget"""

    def get_xtags(self):
        xtags = self.value

    zope.interface.implementsOnly(IXtagsWidget)


def XtagsFieldWidget(field, request):
    """IFieldWidget factory for XtagsWidget."""
    return widget.FieldWidget(field, XtagsWidget(request))
