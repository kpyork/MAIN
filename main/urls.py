from .views import (
    home,detail,posts,create_post)

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.utils.text import slugify

urlpatterns = [
    path("", home, name="home"),
    # path("detail", detail, name="detail"),
    # path("posts", posts, name="posts"),
    path("detail/<slug>/", detail, name="detail"),
    path("posts/<slug>/", posts, name="posts"),
    path("create_post", create_post, name="create_post"),
    # path("latest_posts", latest_posts, name="latest_posts"),
    # path("search", search_result, name="search_result"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
