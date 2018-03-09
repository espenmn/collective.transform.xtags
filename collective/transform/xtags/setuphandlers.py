from Products.CMFCore.utils import getToolByName

mimetype = 'text/x-tags'
transform = 'xtags_to_html'

def registerMimetype(portal):
    """Add text/xtags to the mimetype registry"""
    mime_reg = getToolByName(portal, 'mimetypes_registry')
    if not mime_reg.lookup("text/x-tags"):
        mime_reg.manage_addMimeType('text/x-tags',
                               ['text/x-tags'], ['Quark Xpress Tags'], 'text.png')


def uninstallMimetype(portal):
    """Delete the xtags mimetype"""
    mime_reg = getToolByName(portal, 'mimetypes_registry')
    if mimetype in mime_reg.objectIds():
        mime_reg.manage_delObjects([mimetype])

def installTransform(portal):
    """Install xtags to html transform"""
    transforms = getToolByName(portal, 'portal_transforms')
    if transform not in transforms.objectIds():
        transforms.manage_addTransform(
            'xtags_to_html',
            'collective.transform.xtags.xtags_to_html'
        )

def uninstallTransform(portal):
    """Uninstall xtags to html transform"""
    transforms = getToolByName(portal, 'portal_transforms')
    transforms.unregisterTransform(transform)

def importVarious(context):
    """Various import step code"""
    marker_file = 'collective.transform.xtags.txt'
    if context.readDataFile(marker_file) is None:
        return
    portal = context.getSite()
    #registerMimetype(portal)
    installTransform(portal)

def importVariousUninstall(context):
    """Various uninstall step code"""
    marker_file = 'collective.transform.xtags-uninstall.txt'
    if context.readDataFile(marker_file) is None:
        return
    portal = context.getSite()
    #uninstallMimetype(portal)
    uninstallTransform(portal)
