from django import template
from titlecase import titlecase

register = template.Library()


@register.filter
def titleize(string):
    string = string.replace('-', ' ')
    string = titlecase(string)
    return string


@register.simple_tag
def page_limits(curr_page, page_limit, num_pages):
    lower_limit = curr_page // page_limit * page_limit + 1
    higher_limit = (curr_page // page_limit + 1) * page_limit + 1
    if curr_page % page_limit == 0:
        lower_limit = curr_page - page_limit + 1
        higher_limit = curr_page + 1
    higher_limit = num_pages + 1 if higher_limit > num_pages else higher_limit
    if higher_limit == lower_limit:
        higher_limit += 1
    return range(lower_limit, higher_limit)


@register.filter
def stringyfy(var):
    return str(var)


@register.filter
def get_status(item, user_history):
    if str(item.id) in user_history.keys():
        return user_history[str(item.id)]
    else:
        return ''
