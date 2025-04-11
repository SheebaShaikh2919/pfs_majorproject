from django import template
register = template.Library()

@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    # you would need to do any localization of the result here
    total_price = qty * unit_price
    return total_price

@register.simple_tag()
def access(listEle, idx, *args, **kwargs):
    accessed_element = listEle[str(idx)]
    return accessed_element

