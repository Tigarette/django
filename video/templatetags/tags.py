from django import template
register = template.Library()


@register.simple_tag
def getRank(a, b, c):
    return a + (b - 1) * c
