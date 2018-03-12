from Products.Five.browser import BrowserView
from plone import api


class RenderFromXtags(BrowserView):
    """ quark xtags to html.    """

    def __call__(self, *args, **kw):
        return self.render_xtags()

    def render_markdown(self):
        """Return quark xtags as a stringified HTML document."""
        value = self.context.xtags
        portal_transforms = api.portal.get_tool(name='portal_transforms')
        data = portal_transforms.convertTo('text/html', value, mimetype='text/x-xtags')
        html = data.getData()
        return html
