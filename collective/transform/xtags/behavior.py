# -*- coding: utf-8 -*-

from zope import schema
from zope.i18nmessageid import MessageFactory
from zope.interface import alsoProvides
from zope.interface import implements
from zope.interface import Interface
from collective import dexteritytextindexer
from plone.autoform.interfaces import IFormFieldProvider
from plone.directives import form
from plone.supermodel.model import Schema

from zope.i18nmessageid import MessageFactory

from collective.transform.xtags.widget import XtagsFieldWidget

_ = MessageFactory('collective.transform.xtags')


class IMarkdownBehavior(form.Schema):
    """ A Quark Xpress Xtags text field"""

    dexteritytextindexer.searchable('bodytext')

    bodytext = schema.Text(
    	title=u"Body text",
    	description=u"Note: You can select text to preview, or preview all",
    )

    form.widget(
          bodytext=XtagsFieldWidget,
    )


alsoProvides(IXtagsBehavior, IFormFieldProvider)
