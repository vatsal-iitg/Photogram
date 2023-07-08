from django.urls import path
from .views import PostList,PostDetails,PostEditView,PostDeleteView,CommentDeleteView,ProfileView,ProfileEditView,AddFollower,RemoveFollower,AddLike,AddDislike,UserSearch,ListFollowers,AddCommentDislike,AddCommentLike,CommentReplyView, inbox , Directs, SendDirect, MessageSearch
# imported all the views created in views.py


urlpatterns = [
    path('',PostList.as_view(),name='post-list'), # directing to post_feed at localhost:{port}/socialfeed
    path('post/<int:pk>',PostDetails.as_view(),name='post-detail'),
    # directing to the post with the id = pk (primary key) for viewing that post
    path('post/edit/<int:pk>',PostEditView.as_view(),name='post-edit'),# directing to the post with the id = pk (primary key) for editing that post, (a user can edit only his own post, taken care in templates folder's files)
    path('post/delete/<int:pk>',PostDeleteView.as_view(),name='post-delete'),# directing to the post with the id = pk (primary key) for deleting that post, (a user can delete only his own post, taken care in templates folder's files)
    path('post/<int:post_pk>/comment/delete/<int:pk>',CommentDeleteView.as_view(),name='comment-delete'),
    # directing to the post with the id = post_pk (primary key) and comment id = pk, for deleting that comment, (a user can delete only comments on his own post, taken care in templates folder's files)

    path('profile/<int:pk>',ProfileView.as_view(),name='profile'),
    path('profile/edit/<int:pk>',ProfileEditView.as_view(),name='profile-edit'),
    path('profile/<int:pk>/followers/add',AddFollower.as_view(),name='add-follower'),
    path('profile/<int:pk>/followers/remove',RemoveFollower.as_view(),name='remove-follower'),    




    # these are the different urls added
    path('post/<int:pk>/like',AddLike.as_view(),name='like'),    
    path('post/<int:pk>/dislike',AddDislike.as_view(),name='dislike'),    
    path('search/',UserSearch.as_view(),name='profile-search'),
    path('profile/<int:pk>/followers/',ListFollowers.as_view(),name='followers-list'),
    path('post/<int:post_pk>/comment/<int:pk>/like',AddCommentLike.as_view(),name='comment-like'),
    path('post/<int:post_pk>/comment/<int:pk>/dislike',AddCommentDislike.as_view(),name='comment-dislike'),
    path('post/<int:post_pk>/comment/<int:pk>/reply',CommentReplyView.as_view(),name='comment-reply'),


    path('inbox/', inbox, name="inbox"),
    path('directs/<username>', Directs, name="directs"),
    path('send/', SendDirect, name="send-directs"),
    path('searchmessage/', MessageSearch, name="search-users"),

]