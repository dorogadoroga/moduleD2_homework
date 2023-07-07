from django.urls import path
from .views import PostList, PostDetail, PostSearh, PostCreate, PostUpdate, PostDelete

urlpatterns = [
    path('', PostList.as_view(), name='news'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search', PostSearh.as_view(), name='search'),
    path('add', PostCreate.as_view(), name='post_add'),
    path('<int:pk>/edit', PostUpdate.as_view(), name='post_edit'),
    path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
]