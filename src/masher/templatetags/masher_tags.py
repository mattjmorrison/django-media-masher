from os import path
from django import template

import masher

register = template.Library()

class MashNode(template.Node):

    def __init__(self, media_root, files):
        self.media_root = template.Variable(media_root)
        self.files = files

    def render(self, context):
        media_root_resolve = self.media_root.resolve(context)
        qualified_files = [path.join(media_root_resolve, name) for name in self.files]
        return masher.MashMedia().mash(qualified_files)

@register.tag
def mash(parser, token):
    bits = token.split_contents()[1:]
    if len(bits) < 1:
        raise template.TemplateSyntaxError("'mash' tag requires at least one argument")

    media_root = bits.pop(0).strip("'" + '"')
    return MashNode(media_root, [bit.strip("'" + '"') for bit in bits])