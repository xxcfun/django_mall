from django import template

register = template.Library()


def warning(value):
    if value:
        return '<span class="text-red">' + value[0] + '</span>' + value[1:]
    return value


register.filter('warning', warning)
