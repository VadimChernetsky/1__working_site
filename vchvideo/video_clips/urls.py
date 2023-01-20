from django.urls import path, re_path

from .views import VideoList, connection, ShowPost, VideoCategory

urlpatterns = [
    path('', VideoList.as_view(), name='home'),        # 1 http://127.0.0.1:8000/
    # path('categories/', categories),   # 2 http://127.0.0.1:8000/categories/
    # path('', categories),
    # path('categories/<int:catid>/', categories),
    # path('categories/<slug:categ>/', categories),
    # re_path(r'^archive/(?P<year>[0-9]{4})/', archive)  # url в котором нужно указать год в 4 числах
    path('connection/', connection, name='connection'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', VideoCategory.as_view(), name='category')
]