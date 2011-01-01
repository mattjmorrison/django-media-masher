from django import template

import masher

register = template.Library()

class MashNode(template.Node):

    def __init__(self, files):
        self.files = files

    def render(self, context):
        return masher.MashMedia().mash(self.files)

@register.tag
def mash(parser, token):
    bits = token.split_contents()[1:]
    if len(bits) < 1:
        raise template.TemplateSyntaxError("'mash' tag requires at least one argument")

    return MashNode([bit.strip("'" + '"') for bit in bits])