from django.urls import path
from post import views

urlpatterns = [
    path('', views.index, name='index'),
    path('newpost/', views.NewPost, name='newpost'),
    path('<uuid:post_id>/', views.postDetail, name='post-details'),
    path('<uuid:post_id>/like', views.like, name='post-like'),
    path('<uuid:post_id>/favourite', views.favourite, name='favourite'),
]
