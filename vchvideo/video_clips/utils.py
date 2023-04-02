from django.db.models import Count
from .models import Category


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        '''выводить список категорий у которых есть посты'''
        cats = Category.objects.annotate(Count('video'))
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context