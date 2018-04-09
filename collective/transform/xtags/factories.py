# -*- coding: utf-8 -*-
from plone.app.dexterity.interfaces import IDXFileFactory
from plone.app.dexterity.factories import DXFileFactory
from Products.CMFCore.interfaces._content import IFolderish
from zope.component import adapter
from zope.interface import implementer
import transaction

from plone import api



@adapter(IFolderish)
@implementer(IDXFileFactory)
class XTagsFileFactory(DXFileFactory):

    def __call__(self, name, content_type, data):

        custom_obj = self.create_custom_stuff(name, content_type, data)

        import pdb; pdb.set_trace()
        if custom_obj:
            pass
        else:
            return super(XTagsFileFactory, self).__call__(name, content_type, data)

    def create_custom_stuff(self, name, content_type, data):
        if name.endswith("xtg"):
            # do your own stuff here like wrap each file in a folder
            objekt = api.content.create(
                type='quarktags',
                title=name,
                container=self.context,
                qrktext = data.read()
            )

    	    api.content.transition(obj=objekt, transition='publish')
            return objekt
        return False
