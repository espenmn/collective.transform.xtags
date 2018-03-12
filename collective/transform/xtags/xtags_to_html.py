# -*- coding: utf-8 -*-
from Products.PortalTransforms.interfaces import itransform
#import xtags

from zope.interface import implements
try:
    from Products.PortalTransforms.interfaces import ITransform
    HAS_PLONE3 = False
except ImportError:
    from Products.PortalTransforms.interfaces import itransform
    HAS_PLONE3 = True


def _safe_unicode(text):
    if not isinstance(text, unicode):
        text = unicode(text, 'utf-8', 'replace')
    return text


class XtagsToHtml:
    """Transform which converts from xtags to html"""

    if HAS_PLONE3:
        __implements__ = itransform
    else:
        implements(ITransform)


    __name__ = "xtags_to_html"
    output = "text/html"

    def __init__(self, name=None, inputs=('text/plain',), tab_width = 4):
        self.config = {
            'inputs' : inputs,
            'tab_width' : 4
        }
        self.config_metadata = {
            'inputs' : ('list',
                        'Inputs',
                        'Input(s) MIME type. Change with care.'),
            'tab_width' : ('string',
                           'Tab width',
                           'Number of spaces for a tab in the input')
            }
        if name:
            self.__name__ = name

    def name(self):
        return self.__name__

    def __getattr__(self, attr):
        if attr in self.config:
            return self.config[attr]
        raise AttributeError(attr)

    def convert(self, orig, data, **kwargs):
        #text = _safe_unicode(orig)
        #if not isinstance(text, unicode):
        #    text = unicode(text, 'utf-8', 'replace')
        text = _safe_unicode(orig)

        lines = text.split("\n")
        config = xtags.ConfigMaster()._get_defaults()
        config['headers']=0
        config['target']='html'
        config['encoding']='utf-8'
        config['toc-level']=3
        config['outfile']=xtags.MODULEOUT

        try:
            body, toc = xtags.convert(lines[3:], config)
            footer    = xtags.doFooter(config)
            toc       = xtags.toc_tagger(toc, config)
            toc       = xtags.toc_formatter(toc, config)
            full_doc  = toc + body + footer
            finished  = xtags.finish_him(full_doc, config)
            text = '\n'.join(finished)

        # xtags error, show the messsage to the user
        except xtags.error, msg:
            text = msg

        # Unknown error, show the traceback to the user
        except:
            text = xtags.getUnknownErrorMessage()

        data.setData(text)
        return data

def register():
    return XtagsToHtml()
