from django import template
from news.models import Category


register = template.Library()

@register.inclusion_tag('navigation.html', takes_context=True)
def show_navigation(context):
    categories = Category.objects.all()
    return {
        "categories": categories,
    }