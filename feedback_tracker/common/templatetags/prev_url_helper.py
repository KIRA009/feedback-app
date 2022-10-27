from django import template

from feedback_tracker.common.utils import get_base_querydict

register = template.Library()


@register.simple_tag(takes_context=True)
def prev_url_helper(context):
    """
    Returns a querystring with the current page and the current filters.
    """
    curr_url = context["request"].path
    querydict = get_base_querydict(context, None)
    if querydict:
        return f"{curr_url}?{querydict.urlencode()}"
    return f"{curr_url}"
