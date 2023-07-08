from django.shortcuts import render,redirect, get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from .models import Post,Comment,UserProfile,Message
from .forms import PostForm,CommentForm
from django.views.generic.edit import UpdateView,DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.db.models import Q


from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator

# Create your views here.
class PostList(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs): # this function lists the views in the post feed
        logged_in_user=request.user
        posts = Post.objects.filter(
            author__profile__followers__in=[logged_in_user.id]
        ).order_by('-created_on')
        # ordering by latest posts

        form = PostForm()
        context = {
            'posts':posts,
            'form':form
        }

        return render(request,'socialfeed/postlist.html',context)
        # postlist template has html code with for loops for showing all posts

    def post(self,request,*args,**kwargs):
        logged_in_user=request.user
        # creating new post and adding to the social feed
        posts = Post.objects.filter(
            author__profile__followers__in=[logged_in_user.id]
        ).order_by('-created_on')
        # ordering by latest posts
        form = PostForm(request.POST,request.FILES)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            # saving the new post

        context = {
            'posts':posts,
            'form':form
        }

        return render(request,'socialfeed/postlist.html',context)


class PostDetails(LoginRequiredMixin,View):# getting the details of the post
    def get(self,request,pk,*args,**kwargs):
        post  = Post.objects.get(pk=pk) # getting the id of the post
        form =  CommentForm() # for adding comments

        comments = Comment.objects.filter(post=post).order_by('-created_on') # ordering by latest comments
        context = {
            'post':post,
            'form':form,
            'comments':comments
        }

        return render(request,'socialfeed/postdetails.html',context)

    def post(self,request,pk,*args,**kwargs):
        post  = Post.objects.get(pk=pk)
        form =  CommentForm(request.POST)

        if form.is_valid():
            new_comment= form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            print('comment saved')
            # adding new comments

        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post':post,
            'form':form,
            'comments':comments
        }

        return render(request,'socialfeed/postdetails.html',context)


class CommentReplyView(LoginRequiredMixin,View):
    def post(self,request,post_pk,pk,*args,**kwargs):
        post = Post.objects.get(pk=post_pk)
        parent_comment = Comment.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.parent =parent_comment
            new_comment.save()

        
        return redirect('post-detail',pk=post_pk)

class PostEditView(LoginRequiredMixin,UserPassesTestMixin,UpdateView): # editing a post
    model = Post
    fields = ['body']
    template_name='socialfeed/editpost.html'
    

    def get_success_url(self):
        pk =self.kwargs['pk']
        return reverse_lazy('post-detail',kwargs={'pk':pk})
    # this function reverts back to the post details page when the post is successfully updated


    def test_func(self):
        post=self.get_object()
        return self.request.user==post.author
    # this function take care of the fact that user cannot update or delete posts which do not belong to him, even by manipulating the urls

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    template_name = 'socialfeed/deletepost.html'
    success_url = reverse_lazy('post-list')
    # reverts to post feed on successful deletion of post

    def test_func(self):
        post=self.get_object()
        return self.request.user==post.author
    # this function take care of the fact that user cannot update or delete posts which do not belong to him, even by manipulating the urls

class CommentDeleteView(LoginRequiredMixin,DeleteView):
    model = Comment
    template_name = 'socialfeed/deletecomment.html'

    def get_success_url(self):
        pk =self.kwargs['post_pk']
        return reverse_lazy('post-detail',kwargs={'pk':pk})
        


class ProfileView(View):
    def get(self,request,pk,*args,**kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user=  profile.user
        posts = Post.objects.filter(author=user).order_by('-created_on')

        followers = profile.followers.all()
        len_followers = len(followers)

        is_following = False

        if len_followers==0:
            is_following=False

        for follower in followers:
            if request.user==follower:
                is_following=True
                break
            else:
                is_following=False

        context = {
            'user':user,
            'profile':profile,
            'posts':posts,
            'len_followers':len_followers,
            'is_following':is_following,
        }

        return render(request,'socialfeed/profile.html',context)


class ProfileEditView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = UserProfile
    fields = ['name','bio','date_of_birth','location','avatar']
    template_name = 'socialfeed/editprofile.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile',kwargs={'pk':pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user==profile.user


class AddFollower(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        profile=UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)

        return redirect('profile',pk= profile.pk)


class RemoveFollower(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        profile=UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)

        return redirect('profile',pk= profile.pk)

class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)




class UserSearch(View):
    def get(self,request,*args,**kwargs):
        query  = self.request.GET.get('query')
        profile_list = UserProfile.objects.filter(
            Q(user__username__icontains=query)
        )


        context = {
            'profile_list':profile_list,
        }

        return render(request,'socialfeed/search.html',context)


class ListFollowers(View):
    def get(self,request,pk,*args,**kwargs):
        profile =UserProfile.objects.get(pk=pk)
        followers = profile.followers.all()

        context={
            'profile':profile,
            'followers':followers
        }

        return render(request,'socialfeed/listfollowers.html',context)  




class AddCommentLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            comment.dislikes.remove(request.user)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            comment.likes.add(request.user)

        if is_like:
            comment.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddCommentDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            comment.likes.remove(request.user)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            comment.dislikes.add(request.user)

        if is_dislike:
            comment.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)






@login_required
def inbox(request):
    user = request.user
    messages = Message.get_message(user=request.user)
    active_direct = None
    directs = None
    userprofile = get_object_or_404(UserProfile, user=user)

    if messages:
        message = messages[0]
        active_direct = message['user'].username
        directs = Message.objects.filter(user=request.user, reciepient=message['user'])
        directs.update(is_read=True)

        for message in messages:
            if message['user'].username == active_direct:
                message['unread'] = 0
    context = {
        'directs':directs,
        'messages': messages,
        'active_direct': active_direct,
        'userprofile': userprofile,
    }
    return render(request, 'socialfeed/inbox.html', context)


@login_required
def Directs(request, username):
    user  = request.user
    messages = Message.get_message(user=user)
    active_direct = username
    directs = Message.objects.filter(user=user, reciepient__username=username)  
    directs.update(is_read=True)

    for message in messages:
            if message['user'].username == username:
                message['unread'] = 0
    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
    }
    return render(request, 'socialfeed/direct.html', context)

def SendDirect(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    body = request.POST.get('body')

    if request.method == "POST":
        to_user = User.objects.get(username=to_user_username)
        Message.sender_message(from_user, to_user, body)
        return redirect('inbox')

def MessageSearch(request):
    query = request.GET.get('q')
    context = {}
    if query:
        users = User.objects.filter(Q(username__icontains=query))

        # Paginator
        paginator = Paginator(users, 8)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)

        context = {
            'users': users_paginator,
            }

    return render(request, 'socialfeed/messagesearch.html', context)
