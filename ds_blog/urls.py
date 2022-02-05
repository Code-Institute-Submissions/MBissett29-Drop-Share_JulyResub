from django.urls import path
from .views import PostList, PostDetail, UserPost_Create, PostLike

urlpatterns = [
    path('', PostList.as_view(), name='home'),
    path('<slug:slug>/', PostDetail.as_view(), name='user_post'),
    path('post_blog', UserPost_Create.as_view(), name='post_blog'),
    path('like/<slug:slug>', PostLike.as_view(), name='post_like'),
]
