from django.urls import path
from django.views.decorators.cache import cache_page
from .views import *

urlpatterns = [
    # path('', cache_page(60)(PostList.as_view()), name='news'),
    # path('<int:pk>', cache_page(60*5)(PostDetail.as_view()), name='post_detail'),
    path('', PostList.as_view(), name='news'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search', PostSearh.as_view(), name='search'),
    path('add', PostCreate.as_view(), name='post_add'),
    path('become-author', become_author, name='become_author'),
    path('<int:pk>/edit', PostUpdate.as_view(), name='post_edit'),
    path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('<slug:slug>', PostsByCategory.as_view(), name='categories'),
    path('<slug:slug>/become_subscriber', become_subscriber, name='become_subscriber'),
    path('<slug:slug>/delete_subscription', delete_subscription, name='delete_subscription')
]