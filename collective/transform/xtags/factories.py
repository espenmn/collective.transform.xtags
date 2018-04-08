# -*- coding: utf-8 -*-
from plone.app.dexterity.interfaces import IDXFileFactory
from plone.app.dexterity.factories import DXFileFactory
from Products.CMFCore.interfaces._content import IFolderish
from zope.component import adapter
from zope.interface import implementer


@adapter(IFolderish)
@implementer(IDXFileFactory)
class XTagsFileFactory(DXFileFactory):

    def __call__(self, name, content_type, data):
        import pdb; pdb.set_trace()
        custom_obj = self.create_custom_stuff(name, content_type, data)
        if custom_obj:
            return custom_obj

        return super(XTagsFileFactory, self).__call__(name, content_type, data)

    def create_custom_stuff(self, name, content_type, data):
        if name == 'quarktags':
            # do you own stuff here like wrap each file in a folder
            self.qrktext = data()
        return