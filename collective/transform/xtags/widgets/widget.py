
import zope.component
import zope.interface
import zope.schema.interfaces

from z3c.form import interfaces
from z3c.form import widget
from z3c.form.browser import text

from plone import api
#from collective.transform.xtags.interfaces import IXtagsSettings


class IXtagsWidget(interfaces.IWidget):
    """Xtags widget."""


class XtagsWidget(text.TextWidget):
    """Xtags Widget"""

    def render_xtags(self):
        """Return the preview as a stringified HTML document."""
        portal_transforms = api.portal.get_tool(name='portal_transforms')
        value = self.value.encode('utf-8')
        data = portal_transforms.convertTo('text/html', value, mimetype='text/x-web-markdown')
        html = data.getData()
        return html


    #def live_preview(self):
    #    return api.portal.get_registry_record(name="live_preview", interface=IXtagsSettings)


    zope.interface.implementsOnly(IXtagsWidget)


def XtagsFieldWidget(field, request):
    """IFieldWidget factory for XtagsWidget."""
    return widget.FieldWidget(field, XtagsWidget(request))
