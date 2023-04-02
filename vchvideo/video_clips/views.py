from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView
from django.db.models import Count
from django.views.decorators.cache import cache_page

from .models import Video, Category
from .utils import DataMixin
from .forms import SearchForm


@cache_page(60 * 15)
def home(request):
    # posts = Video.objects.filter(is_active=True)
    '''для оптимизации,
    что бы совмсетно с записями были загружены данные из табл Category'''
    posts = Video.objects.filter(is_active=True).select_related('categ')
    '''выводить список категорий у которых есть посты'''
    cats = Category.objects.annotate(Count('video'))
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        ''' __icontains без учета регистра'''
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        posts = posts.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'form': form, 'cats': cats, 'page_obj': page_obj,
               'posts': page_obj.object_list}
    if 'cat_selected' not in context:
        context['cat_selected'] = 0
    return render(request, 'video_clips/index.html', context)


@cache_page(60 * 15)
def connection(request):
    posts = Video.objects.all()
    cats = Category.objects.annotate(Count('video'))
    context = {
        'posts': posts,
        'cats': cats,
        'cat_selected': 0,
    }
    return render(request, 'video_clips/connection.html', context=context)


def pageNotFound(request, exception):
    '''переопределение ошибки 404'''
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class VideoCategory(DataMixin, ListView):
    # paginate_by = 2
    model = Video
    template_name = 'video_clips/categ.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Video.objects.filter(categ__slug=self.kwargs['cat_slug'],
                                    is_active=True).select_related('categ')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Категория - ' + str(context['posts'][0].categ)
        # context['cat_selected'] = context['posts'][0].categ_id
        '''для оптимизации ,по флагу берем категорию, для который выводим список'''
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        # c_def = self.get_user_context(title='жанр - ' + str(context['posts'][0].categ),
        #                               cat_selected=context['posts'][0].categ_id)
        c_def = self.get_user_context(title='genre - ' + str(c.name),
                                      cat_selected=c.pk)
        context = dict(list(context.items()) + list(c_def.items()))
        return context


'''
#страница категорий
def show_category(request, cat_slug):
    cat = Category.objects.filter(slug=cat_slug)
    posts = Video.objects.filter(categ_id=cat[0].id)
    # cats = Category.objects.all()

    if len(posts) == 0:
        raise Http404()

    context = {
        'posts': posts,
        # 'cats': cats,
        'cat_selected': cat[0].id,
    }
    return render(request, 'video_clips/index.html', context=context)


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


def show_post(request, post_slug):
    post = get_object_or_404(Video, slug=post_slug)
    context = {
        'post': post,
        'title': post.title,
        'cat_selected': post.categ_id,
    }
    return render(request, 'video_clips/post.html', context)
'''
