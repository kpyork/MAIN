from django.conf import settings
from django.conf.urls.static import static
# from django.contrib import admin
# from django.urls import include
# from django.utils.text import slugify
from django.urls import path
from .views import signup,signin,update_profile,logout

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("signin/", signin, name="signin"),
    path("logout/", logout, name="logout"),
    path("update_profile/", update_profile, name="update_profile"),
    # path("create_post", create_post, name="create_post"),
    # path("latest_posts", latest_posts, name="latest_posts"),
    # path("search", search_result, name="search_result"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
