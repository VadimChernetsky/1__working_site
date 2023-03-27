from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.db.models import Q

from .models import Video, Category, AdditionalImage
from django.views.generic import ListView
from .utils import DataMixin
from .forms import SearchForm
from django.db.models import Count

# # 1 содержимое главной страницы
# def index(request):
#     posts = Video.objects.all()
#     # cats = Category.objects.all()
#     context = {
#         'posts': posts,
#         # 'cats': cats,
#         'cat_selected': 0,
#     }
#     return render(request, 'video_clips/index.html', context=context)

# class VideoList(DataMixin, ListView):
#     # paginate_by = 2
#     model = Video
#     template_name = 'video_clips/index.html'
#     context_object_name = 'posts'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context['title'] = 'Главная станица'
#         # context['cat_selected'] = 0
#
#         c_def = self.get_user_context(title='Главная страница')
#         context = dict(list(context.items()) + list(c_def.items()))
#         return context
#
#     def get_queryset(self):
#         return Video.objects.filter(is_active=True)



# содержание страницы связи со мной
def connection(request):
    '''
    #для примера: как использовать пагинацию в функциях
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.Get.get('page')        #получаем номер текущей страницы
    page_obj = paginator.get_page(page_number)   #список элементов текущей страницы
    return render(request, 'video_clips/connection.html', {'page_obj': page_obj})
    '''
    posts = Video.objects.all()
    cats = Category.objects.annotate(Count('video'))
    context = {
        'posts': posts,
        'cats': cats,
        'cat_selected': 0,
    }
    return render(request, 'video_clips/connection.html', context=context)



#страница перенаправление ошибки
def pageNotFound(request, exception):
    '''переопределение ошибки 404'''
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
    # return HttpResponseNotFound('<img src="icons/ava1.png">')



# #страница поста
# def show_post(request, post_slug):
#     post = get_object_or_404(Video, slug=post_slug)
#
#     context = {
#         'post': post,
#         'title': post.title,
#         'cat_selected': post.categ_id,
#     }
#     return render(request, 'video_clips/post.html', context)

class ShowPost(DataMixin, DetailView):
    model = Video
    template_name = 'video_clips/post.html'
    slug_url_kwarg = 'post_slug'     #по умолчанию просто 'slug'
    # pk_url_kwarg = 'post_pk'       #по умолчанию просто 'pk'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = context['post']
        c_def = self.get_user_context(title=context['post'])
        context = dict(list(context.items()) + list(c_def.items()))
        return context


# #страница категорий
# def show_category(request, cat_slug):
#     cat = Category.objects.filter(slug=cat_slug)
#     posts = Video.objects.filter(categ_id=cat[0].id)
#     # cats = Category.objects.all()
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'posts': posts,
#         # 'cats': cats,
#         'cat_selected': cat[0].id,
#     }
#     return render(request, 'video_clips/index.html', context=context)

class VideoCategory(DataMixin, ListView):
    # paginate_by = 2
    model = Video
    template_name = 'video_clips/categ.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Video.objects.filter(categ__slug=self.kwargs['cat_slug'], is_active=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Категория - ' + str(context['posts'][0].categ)
        # context['cat_selected'] = context['posts'][0].categ_id
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].categ),
                                      cat_selected=context['posts'][0].categ_id)
        context = dict(list(context.items()) + list(c_def.items()))
        return context

def v_search(request):
    # categ = get_object_or_404(Category, pk=pk)
    posts = Video.objects.filter(is_active=True)
    cats = Category.objects.annotate(Count('video'))  # выводить список категорий у которых есть посты
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)   # __icontains без учета регистра
        posts = posts.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    paginator = Paginator(posts, 3)
    # if 'page' in request.GET:
    #     page_number = request.Get['page']  # получаем номер текущей страницы
    # else:
    #     page_number = 1
    # page = paginator.get_page(page_number)  # список элементов текущей страницы
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'form': form, 'cats': cats, 'page_obj': page_obj, 'posts': page_obj.object_list}
    if 'cat_selected' not in context:
        context['cat_selected'] = 0
    return render(request, 'video_clips/index.html', context)
