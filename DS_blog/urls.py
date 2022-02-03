from django.urls import path
from .views import PostList, PostDetail, UserPost_Create

urlpatterns = [
    path('', PostList.as_view(), name='home'),
    path('<slug:slug>/', PostDetail.as_view(), name='user_post'),
    path('post_blog', UserPost_Create, name='post_blog'),
]
