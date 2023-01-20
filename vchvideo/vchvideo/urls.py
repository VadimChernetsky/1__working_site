"""vchvideo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.urls import path, include
from django.views.decorators.cache import never_cache

from video_clips.views import pageNotFound

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('video_clips/', index),  # 1 http://127.0.0.1:8000/video_clips/
    # path('categories/', categories),    # 2 http://127.0.0.1:8000/categories/
    # path('', index),              # 1 http://127.0.0.1:8000/
    path('', include('video_clips.urls')),
]

if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# обработчик для страницы 404
handler404 = pageNotFound