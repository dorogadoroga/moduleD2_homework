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
    path('economics', PostEconomics.as_view()),
    path('politics', PostPolitics.as_view()),
    path('technologies', PostTechnologies.as_view()),
    path('sport', PostSport.as_view()),
    path('tourism', PostTourism.as_view()),
    path('opinions', PostOpinions.as_view()),
]