from django.urls import path, re_path
from legend_blog.views import (PostListView, PostDetailView,
                               PersonListView, PostDeleteView,
                               PostCreateView, PostUpdateView,
                               post_comment,
                               post_reaction)

urlpatterns = [
    path("", PostListView.as_view(), name='home'),
    path("post/create/", PostCreateView.as_view(), name='post_create'),
    path("post/<str:slug>/update/", PostUpdateView.as_view(), name='post_update'),
    path('<int:post_id>/comment', post_comment, name='post_comment'),
    path('<int:post_id>/reaction', post_reaction, name='post_reaction'),
    path("post/<str:slug>/", PostDetailView.as_view(), name='post_detail'),
    re_path(r"^my-posts/$", PersonListView.as_view(), name='person_posts'),
    path("delete-post/<int:post_id>/", PostDeleteView.as_view(), name='delete_post'),
]
