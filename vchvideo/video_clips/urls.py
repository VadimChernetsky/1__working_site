from django.urls import path
from .views import connection, VideoCategory, home
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', home, name='home'),
    path('connection/', connection, name='connection'),
    # path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', cache_page(60 * 15)(VideoCategory.as_view()), name='category'),
]