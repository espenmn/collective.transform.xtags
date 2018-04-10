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

        if custom_obj:
            return custom_obj

        return super(XTagsFileFactory, self).__call__(name, content_type, data)

    def create_custom_stuff(self, name, content_type, data):
        type_ = 'quarktags'
        name = name.decode('utf8')
        if name.endswith("xtg"):
            qrktext=(data.read()).replace("\xef\xbb\xbf", "", 1)
            obj = api.content.create(
                    self.context,
                    type_,
                    qrktext=qrktext,
                    title = name,
            )
            obj.reindexObject()
            return obj

        return False
