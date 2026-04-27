from django import template


register = template.Library()


@register.filter
def date_dmy(value):
    if not value:
        return ""
    text = str(value)
    if len(text) >= 10:
        return f"{text[8:10]}/{text[5:7]}/{text[0:4]}"
    return text


@register.filter
def date_dm(value):
    if not value:
        return ""
    text = str(value)
    if len(text) >= 10:
        return f"{text[8:10]}/{text[5:7]}"
    return text


@register.filter
def initial(value):
    text = str(value or "")
    return text[:1]


@register.filter
def si_no(value):
    return "SI" if value else "NO"
