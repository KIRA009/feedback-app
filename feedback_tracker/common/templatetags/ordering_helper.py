from django import template

from feedback_tracker.common.utils import get_base_querydict

register = template.Library()


@register.simple_tag(takes_context=True)
def ordering_helper(context, field_name):
    """
    Returns a querystring with the modified ordering for the given field.
    """

    curr_ordering = context["curr_ordering"]
    next_ordering = context["next_ordering"]
    default_ordering_preference = context["default_ordering_preference"]
    querydict = get_base_querydict(context, None)
    ordering_string = ""
    if field_name in curr_ordering:
        ordering_string = f"{next_ordering[field_name]}{field_name}"
    else:
        new_preference = ""
        if default_ordering_preference[field_name] == "":
            new_preference = "-"
        ordering_string = f"{new_preference}{field_name}"
    querydict["ordering"] = ordering_string
    return f"?{querydict.urlencode()}"
