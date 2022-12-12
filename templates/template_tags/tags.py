from urllib.parse import parse_qs, parse_qsl, urlencode, urlparse

from django import template

register = template.Library()


@register.filter
def load_more_rows(value):
    parsed_url = urlparse(value)
    params = dict(parse_qsl(parsed_url.query))
    limit = params.get("limit", 10)
    limit = int(limit) + 10
    params["limit"] = limit
    return f"{parsed_url.path}?{urlencode(params)}"
