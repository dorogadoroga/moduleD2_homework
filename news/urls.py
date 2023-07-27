from django.urls import path
from .views import *

urlpatterns = [
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