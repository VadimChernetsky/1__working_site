from django import template
from django.http import Http404

from video_clips.models import *

register = template.Library()

@register.simple_tag(name='getcats')
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)

@register.inclusion_tag('video_clips/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    return {"cats": cats, "cat_selected": cat_selected}



# @register.simple_tag()
# def index_x(filter=None):
#     if not filter:
#         posts = Video.objects.all()
#         return {"posts": posts}
#     else:
#         posts = Video.objects.filter(categ_id=filter)
#         if len(posts) == 0:
#             raise Http404()
#         return {"posts": posts, 'cat_selected': filter}

# @register.simple_tag()
# def index_x():
#     posts = Video.objects.all()
#     return {"posts": posts}

