from django import template

register = template.Library()


@register.filter()
def inc(value, arg):
    return int(value) + int(arg)


@register.simple_tag()
def division(value, div, to_int=False):
    res = int(value) / int(div)
    if to_int:
        return int(res)
    return res
