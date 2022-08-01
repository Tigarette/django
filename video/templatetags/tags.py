from django import template
register = template.Library()


@register.simple_tag
def getRank(a, b, c):
    return a + (b - 1) * c


@register.simple_tag
def getId(a):
    if len(a) > 3:
        return a[0] + a[1] + a[2]
    else:
        return a[0] + a[1]
