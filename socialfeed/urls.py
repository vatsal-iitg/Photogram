from django.urls import path
from .views import PostList,PostDetails,PostEditView,PostDeleteView,CommentDeleteView # imported all the views created in views.py


urlpatterns = [
    path('',PostList.as_view(),name='post-list'), # directing to post_feed at localhost:{port}/socialfeed
    path('post/<int:pk>',PostDetails.as_view(),name='post-detail'),
    # directing to the post with the id = pk (primary key) for viewing that post
    path('post/edit/<int:pk>',PostEditView.as_view(),name='post-edit'),# directing to the post with the id = pk (primary key) for editing that post, (a user can edit only his own post, taken care in templates folder's files)
    path('post/delete/<int:pk>',PostDeleteView.as_view(),name='post-delete'),# directing to the post with the id = pk (primary key) for deleting that post, (a user can delete only his own post, taken care in templates folder's files)
    path('post/<int:post_pk>/comment/delete/<int:pk>',CommentDeleteView.as_view(),name='comment-delete'),
    # directing to the post with the id = post_pk (primary key) and comment id = pk, for deleting that comment, (a user can delete only comments on his own post, taken care in templates folder's files)
]