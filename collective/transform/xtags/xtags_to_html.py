# -*- coding: utf-8 -*-
from Products.PortalTransforms.interfaces import itransform
#import xtags
from lxml.etree import tostring

from pypeg2 import *
from pypeg2 import parse as pparse
from pypeg2.xmlast import create_tree
from lxml.etree import strip_tags, tostring, SubElement

from zope.interface import implements
try:
    from Products.PortalTransforms.interfaces import ITransform
    HAS_PLONE3 = False
except ImportError:
    from Products.PortalTransforms.interfaces import itransform
    HAS_PLONE3 = True

class XtagsToHtml:
    """Transform which converts from xtags to html"""

    if HAS_PLONE3:
        __implements__ = itransform
    else:
        implements(ITransform)


    __name__ = "xtags_to_html"
    output = "text/html"

    import pdb; pdb.set_trace()

    def __init__(self, name=None, inputs=('text/plain',)):
        self.config = {
            'inputs' : inputs,
            'tab_width' : 4
        }
        self.config_metadata = {
            'inputs' : ('list',
                        'Inputs',
                        'Input(s) MIME type. Change with care.'),
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
        import pdb; pdb.set_trace()
        tagged_text = replace_unicode(orig)
        lines = text.split("\n")
        config = xtags.ConfigMaster()._get_defaults()
        tree = create_tree(pparse(replace_unicode(tagged_text), Article))
        strip_tags(tree, 'Text') # Text tags are unstyled text and can be stripped
        propagate_class(tree)
        fix_character_attributes(tree, extra_tags_to_keep)

        import pdb; pdb.set_trace()
        return tree

        # xtags error, show the messsage to the user
        except xtags.error, msg:
            text = msg

        # Unknown error, show the traceback to the user
        except:
            text = xtags.getUnknownErrorMessage()

        #data.setData(text)
        #return data




    #UNICODE STUFF

    # See "A GUIDE TO XPRESS TAGS 8", section "Special characters"
    # Note we have a problem with "@": we can't replace it here without breaking everything...
    #unicode_lookup = {"f": "\u202F", "_": "\u2014", "a": "\u2013", "h": "\u00AD", 's': ' ', 'n': ' ', 'p': ' ', 'e': ' ', '@': ' at '}#"\u0040"}

    # Make list of special characters - have to manually escaped some of them for regex
    #In [4]: "".join(list(q.QUARK_SPECIAL_CHARACTERS))
    #Out[4]: '@<\\nd-tsepf_ahm#$^*{}jo'

    def replace_unicode(tagged_text):
        """Replace Quark escaped character by their unicode codepoint."""
        escaped_chars_regex = re.compile(r'<\\!{0,1}([@<\\nd\-tsepf_ahm#\$\^\*{}jo])>')    #'<\\!{0,1}([fhsnpea@_])>')
        ket_regex = re.compile(r' >(\w)')
        t = ket_regex.sub(lambda match: ' '+match.group(1), tagged_text) # hack -- apparently a solitary ">" before a word is a soft hyphen (undocumented?)
        return escaped_chars_regex.sub(lambda match: QUARK_SPECIAL_CHARACTERS[match.group(1)], t)


    class StylesheetDefinition(str):
        grammar = '@' , attr('name', re.compile(r'[^<>:=]+')), '=', restline

    class Text(str):
        grammar = re.compile(r'[^<\n]+')  # @ is OK?

    # PARAGRAPH STYLE SHEETS AND ATTRIBUTES
    #• Apply Normal paragraph style sheet:   @$:paragraph text
    #• Apply No Style paragraph style sheet: @:paragraph text
    #• Apply defined paragraph style sheet:  @stylesheetname:paragraph text
    para_stylesheet = ('@', attr('class', re.compile(r'[^:]*')) , ':')
    para_attributes = ('<*', attr('para_attributes', re.compile(r'[^<>]+')), '>')

    # CHARACTER STYLE SHEETS AND ATTRIBUTES
    #• Apply Normal character style sheet:          <@$>
    #• Apply the paragraph's character style sheet: <@$p>
    #• Apply No Style character style sheet:        <@>
    #• Apply defined character style sheet:         <@stylesheetname>
    # Use <x@... to reset all previously set character attributes overrides
    char_stylesheet = ['<x@', '<@'], attr('char_stylesheet', re.compile(r'[^<>:]*')), '>'  # '<a',
    #reset_char_attributes = '<a', attr('char_attributes', re.compile(r'\${1,2}')), '>'  # "<a$$>",
    char_attributes = '<', attr('char_attributes', re.compile('[^@<>\*]+')), '>'


    #• Set type style according to character attributes in the applied paragraph style sheet:               <$>
    #• Set type style according to character attributes in the currently applied character style sheet:     <$$>
    #• Set all character attributes according to character attributes in the applied paragraph style sheet: <a$>
    #• Set all character attributes to character attributes in the currently applied character style sheet: <a$$>

    class CharStyle(str):
        grammar = (maybe_some(char_stylesheet),
                   maybe_some(char_attributes),
                   Text)
                  #maybe_some([char_stylesheet, char_attributes], Text)

    #class EscapeCharacter(str):
    #   grammar = "<\\", re.compile(r'[@<\\]'), ">"

    # Paragraph
    class P(List):
        grammar = (maybe_some(char_stylesheet),
                   omit(maybe_some(char_attributes)), # omit() because char attrs are reset on each new para anyway.
                   '\n',
                   maybe_some(para_stylesheet),
                   maybe_some(char_stylesheet),
                   omit(maybe_some(para_attributes)),
                   maybe_some([Text, CharStyle]),
                   )

    class Article(List):
        grammar = contiguous(omit(version, encoding),
                             omit(some(('\n', StylesheetDefinition))),
                             some(P),
                             omit(maybe_some([char_stylesheet, char_attributes])))

    ###########################################
    ### PART 3a: PARSE CHARACTER ATTRIBUTES ###
    ###########################################

    XTG_BOOLEAN_CHARACTER_ATTRIBUTES = 'PBIOSUWRKHVp\+\-'
    XTG_NUMERIC_CHARACTER_ATTRIBUTES = 'Gshktbypnfcz'

    class BooleanCharacterAttribute(str):
        grammar = attr('name', re.compile('(a$|a\$\$|[\$PBIOSUWRKHV\+\-])')) #'((a{0,1}\${0,1,2})|[\$PBIOSUWRKHV\+\-])'  # '([\$PBIOSUWRKHV\+\-]|@\$p|o\(\$\))' Move o($) to StringCharacterAttribute
    class NumericCharacterAttribute(str):
        grammar = attr('name', re.compile('[Gshktbypnfcaz]')), attr('value', re.compile('[0-9\.\$\-]+'))
    class StringCharacterAttribute(str):
        grammar = attr('name', re.compile('[fco]')), attr('value', re.compile('(\"[a-zA-Z_\-0-9 ]+\")|([CMYKW])|\(((\${0,2})|(\"[a-zA-Z]+\",{0,1}))+\)|(\$)'))
        #                                                                             font (f)       |color (c)| OpenType (o)

    class CharacterAttributes(List):
        grammar = some([BooleanCharacterAttribute,
                        NumericCharacterAttribute,
                        StringCharacterAttribute])

    #############################################
    ### PART 3b: PROCESS CHARACTER ATTRIBUTES ###
    #############################################

    class CharacterAttributesTracker:
        """A "counter" that keep track of the style as we walk the tree.
        """
        def __init__(self): #, mapping):
            self.attributes = {}
            self.character_stylesheet = None
            self.reset_all()
            #self.cmap = sorted(mapping.character.items(), key = lambda p: len(p[0]), reverse=True)

        def reset_type_styles(self):
            log.debug("RESET type styles")
            for name in "".join(list(QUARK_CHAR_ATTRIBUTES_TYPE_STYLE)):
                self.attributes[name] = False

        def reset_all(self):
            """Reset all attributes, e.g. upon encountering a <$> tag."""
            log.debug("RESET all styles")
            for name in XTG_BOOLEAN_CHARACTER_ATTRIBUTES + XTG_NUMERIC_CHARACTER_ATTRIBUTES:
                self.attributes[name] = False

        def update_attribute(self, a):
            log.debug("Updating character attribute " + a.name)
            if a.name in ('$' , '$$', 'P'):
                self.reset_type_styles()
            elif a.name in('a$', 'a$$'):
                self.reset_all()
            elif isinstance(a, BooleanCharacterAttribute):
                self.attributes[a.name] = not self.attributes[a.name]
            elif isinstance(a, NumericCharacterAttribute):
                self.attributes[a.name] = a.value if a.value is not '$' else False
            else:
                pass # placeholder for handling StringCharacterAttributes if and when required.


        def update(self, tag):
            """Update the counter from tag."""
            log.debug(str(tag) +  str(tag.text) + str(tag.attrib))
            # First process the character stylesheet, if present. <@$>, <@$p> and <@> mean 'Normal', 'Paragraph' and 'No styleseet'
            # respectively; for our purpose they are all equivalent to 'No stylesheet'.
            try:
                stylesheet = tag.attrib['char_stylesheet']
                if stylesheet == "$p":
                    # This should the paragraph's character stylesheet but
                    # but we don't parse definitions yet...
                    # Used to set all to None. Revert?
                    self.character_stylesheet = 'Normal'
                elif stylesheet == "$":
                    self.character_stylesheet = 'Normal'
                elif stylesheet == "":
                    self.character_stylesheet = 'No Style'
                else:
                    self.character_stylesheet = stylesheet
            except KeyError:
                pass  # No character stylesheet

            # Then process the character attributes:
            try:
                for a in pparse(tag.attrib['char_attributes'], CharacterAttributes):
                  self.update_attribute(a)
            except KeyError:
              pass  # No character attributes

    def propagate_class(tree):
        """Propagate the "class" attribute to <p> tags that don't have one."""
        for t in tree.iter('P'):
            try:
                # If there is a "class" already make a note of it
                new_class =  t.attrib['class']
                if new_class == '$':
                    _class = 'Normal'
                    t.attrib['class'] = _class
                elif new_class == '':
                    _class = 'No Style'
                    t.attrib['class'] = _class
                else:
                    _class = new_class
                #else:
                #   del t.attrib['class']
                #   _class = None
            except KeyError:
                # If there is no "class" attribute add the last (current) one
                #if _class is not None:
                    t.attrib['class'] = _class


    def fix_character_attributes(tree, keep={}):
        """Walk the DOM to keep track of characater attributes and replace the xtag with XML tags.
        The "keep" argument determine which xtags to retain in the XML: if True, keep all; if a dict of {"xtags": xmltag}
        pairs, add this dict to QUARK_CHAR_ATTRIBUTES and only attributes with an explicit mapping will be preserved."""
        log.info('Processing character attributes...')
        QUARK_CHAR_ATTRIBUTES.update(keep)
        tracker = CharacterAttributesTracker()
        for p in tree.iter('P'):
            tracker.reset_all() # I *think* we reset all character attributes with a new paragraph.
            tracker.update(p)
            log.info('p:+str: ' + str(p.text))
            log.info('  |atr: ' + str(p.attrib))
            log.info('  |trk: ' + ''.join([k for k, v in tracker.attributes.items() if v is not False]))
            # attributes other than 'class', if present, are no longer needed:
            try:
                del(p.attrib['char_attributes'])
            except KeyError:
                pass
            try:
                del(p.attrib['char_stylesheet'])
            except KeyError:
                pass
            for t in p.iter('CharStyle'):
                tracker.update(t)
                log.info('t:+str: ' + str(t.text))
                log.info('  |atr: ' + str(t.attrib))
                log.info('  |trk: ' + ''.join([k for k, v in tracker.attributes.items() if v is not False]))
                t.attrib.clear()  # remove existing attributes before setting our own

                if tracker.character_stylesheet is not None:
                    # There is a stylesheet applied. Rename the tag and set the style attribute.
                    t.tag = 'StyledText'
                    t.attrib["style"] = tracker.character_stylesheet
                # Wrap the tag's text into a subtag for each attribute, recursively
                sub = t
                t_text = t.text
                for a, v in tracker.attributes.items():
                    if v and QUARK_CHAR_ATTRIBUTES[a] != "":
                        #print('  |atr1: ' + a+ ' '+ str(v))
                        log.info('  |atr1: ' + a+ ' '+ str(v))
                        sub.text = None
                        sub = SubElement(sub, a)
                        sub.text = t_text
                        if v is not True:
                            # For non-boolean attributes, set the value.
                            sub.attrib['value'] = v
        # All CharStyle tags are now empty and can be deleted
        strip_tags(tree, 'CharStyle')


    # Consider replacing the code above with the following function
    def recursive_wrap(tag, tag_list):
        if len(tag_list) == 0:
            return tag
        else:
            text = tag.text
            tag.text = ''
            sub = SubElement(tag, tag_list[-1])
            sub.text = text
            recursive_wrap(tag, tag_list[0::-2])


def register():
    return XtagsToHtml()
