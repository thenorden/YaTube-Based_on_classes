from django import template


register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter()
def count_comments(count):
    if count in (1, 11, 21, 31):
        field = f'{count} комментарий'
        return field
    elif count in (2, 3, 4):
        field = f'{count} комментария'
        return field
    else:
        field = f'{count} комментариев'
        return field

