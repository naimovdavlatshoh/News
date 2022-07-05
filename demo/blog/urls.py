from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name ='index'),

    # Category
    path('category/', views.category, name ='category'),
    path('category-detail/<int:id>', views.category_detail, name ='category_detail'),

    # Post detail
    path('post-detail/<int:id>', views.post_detail, name ='post_detail'),
    path('add-favourite/<int:postId>', views.add_favourite, name ='add_favourite'),

    # Like & Dislike
    path('like/<int:id>', views.like, name ='like'),
    path('dislike/<int:id>', views.dislike, name ='dislike'),
    path('likePages/', views.likePages, name='likePages'),
    # Profile
    path('profile/', views.profile_index, name='profile'),
    path('profile-data/', views.profile_data, name='profile_data'),
    path('profile-data-edit/', views.profile_data_edit, name='profile_data_edit'),
    path('profile-favourite/', views.profile_favourite, name='profile_favourite'),


    # Admin
    path('profile-admin1/', views.profile_admin1, name ='profile_admin1'),
    path('categories/', views.categories, name='categories'),
    path('categories-edit/<int:id>', views.categories_edit, name='categories_edit'),
    path('posts/', views.posts, name='posts'),
    path('post-edit/<int:id>', views.post_edit, name='post_edit'),
    #Create
    path('create/', views.create, name='create'),
    path('createCategory/', views.createCategory, name='createCategory'),
    path('remove-post/<int:id>', views.remove_post, name='remove_post'),
    path('remove-posts/', views.remove_posts, name='remove_posts'),
    path('remove-category/', views.remove_category, name='remove_category'),
    

    # Search
    path('search/', views.search, name ='search'),

    # Comment
    path('comment/<int:id>', views.comment, name ='comment'),

    path('comment-remove/<int:id>', views.remove_comment, name ='remove_comment'),
    
    # Auth
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),

    # Register
    path('signup/', views.signup, name ='signup'),

]