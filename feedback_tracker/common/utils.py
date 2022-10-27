import re

from django.http.request import QueryDict


def get_ordering_object(ordering):
    """
    Returns a map of the field and direction to order by.
    """
    ordering_map = {}
    if ordering.startswith("-"):
        ordering_map[ordering[1:]] = "-"
    else:
        ordering_map[ordering] = ""
    return ordering_map


def get_base_querydict(context, base):
    if base is None and "request" in context:
        return context["request"].GET.copy()
    if isinstance(base, QueryDict):
        return base.copy()
    if isinstance(base, dict):
        return QueryDict.fromkeys(base, mutable=True)
    if isinstance(base, str):
        return QueryDict(base, mutable=True)
    # request not present or base value unsupported
    return QueryDict("", mutable=True)


def string_is_email(string):
    """
    Checks if a string is an email address.
    """
    return re.match(r"[^@]+@[^@]+\.[^@]+", string)
