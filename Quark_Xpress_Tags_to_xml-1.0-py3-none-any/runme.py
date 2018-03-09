from quark_tagged_text import get_encoding, to_xml
from lxml.etree import tostring
#encoding = get_encoding('/Users/rolf/Desktop/tezt.xtg')
with open('/Users/rolf/Desktop/tezt.xtg') as tagged_text:
    element_tree = to_xml(tagged_text)
serialised_xml = tostring(element_tree, encoding='utf-8')
