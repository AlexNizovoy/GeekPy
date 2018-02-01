from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def get_cat_records(context, category_name):
    return context['records'].get(category_name)
