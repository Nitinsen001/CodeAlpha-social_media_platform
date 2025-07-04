# social/urls.py

from django.urls import path
from . import views



urlpatterns = [
    path('', views.main_view, name='main'),  
    path('post_list', views.post_list_view, name='post_list'),  
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/success', views.success_view, name='signup/success'),
  
    path('like/<int:post_id>/', views.like_post_view, name='like_post'),
    path('user/<str:username>/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update_view, name='profile_update'),
    path('follow/<str:username>/', views.toggle_follow_view, name='toggle_follow'),
    
    path('search/', views.search_users_view, name='search_users'),
    path('create/', views.create_post_view, name='create_post'),

    path('post/<int:post_id>/', views.post_detail_view, name='post_detail'),
    # social/urls.py
    path('notifications/', views.notifications_view, name='notifications'),

    path('explore/', views.global_feed_view, name='global_feed'), 
    path('post/<int:post_id>/edit/', views.edit_post_view, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post_view, name='delete_post'),
    path('post/<int:post_id>/save/', views.toggle_save_post_view, name='save_post'),
path('saved/', views.saved_posts_view, name='saved_posts'),
path('github-demo/', views.github_demo, name='github-demo'),
path('LinkedIn-demo/', views.LinkedIn_demo, name='LinkedIn-demo'),


]
