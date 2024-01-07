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
def progress_value(value, arg):
    try:
        return 0.01 if 0 < int(value) / int(arg) < 0.01 else int(value) / int(arg)
    except (ValueError, ZeroDivisionError):
        return None


@register.filter
def dash_length(solved, total):
    return 282 * solved / total


@register.filter
def progress_length(solved, total):
    return solved/total * 100 if solved/total > 0.01 else 1


@register.filter
def get_status(item, user_history):
    if str(item.title) in user_history.keys():
        return user_history[str(item.title)]
    else:
        return ''


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    query = context['request'].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()


@register.simple_tag(takes_context=True)
def take_query(context, **kwargs):
    return context['request'].GET.copy()
