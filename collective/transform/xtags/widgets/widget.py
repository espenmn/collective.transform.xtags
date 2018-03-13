
import zope.component
import zope.interface
import zope.schema.interfaces

from z3c.form import interfaces
from z3c.form import widget
from z3c.form.browser import text

from plone import api
#from collective.transform.xtags.interfaces import IXtagsSettings

from collective.transform.xtags.browser.quark_tagged_text import to_xml
from lxml.etree import tostring



class IXtagsWidget(interfaces.IWidget):
    """Xtags widget."""


class XtagsWidget(text.TextWidget):
    """Xtags Widget"""

    def render_xtags(self):
        """Return the preview as a stringified HTML document."""
        #portal_transforms = api.portal.get_tool(name='portal_transforms')
        value = self.value.encode('utf-8')
        element_tree = to_xml(value)
        serialised_xml = tostring(element_tree, encoding='utf-8')
        return serialised_xml


    zope.interface.implementsOnly(IXtagsWidget)


def XtagsFieldWidget(field, request):
    """IFieldWidget factory for XtagsWidget."""
    return widget.FieldWidget(field, XtagsWidget(request))
