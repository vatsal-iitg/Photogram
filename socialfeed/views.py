from django.shortcuts import render

from django.views import View # view imported

from django.urls import reverse_lazy # for directing back to previous urls

from .models import Post,Comment

from .forms import PostForm,CommentForm # imported forms

from django.views.generic.edit import UpdateView,DeleteView # these views are imported for east updation and deletion

from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin # these views take care of the fact that user cannot update or delete posts which do not belong to him, even by manipulating the urls

# Create your views here.
class PostList(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs): # this function lists the views in the post feed
        posts = Post.objects.all().order_by('-created_on')
        # ordering by latest posts

        form = PostForm()
        context = {
            'posts':posts,
            'form':form
        }

        return render(request,'socialfeed/postlist.html',context)
        # postlist template has html code with for loops for showing all posts

    def post(self,request,*args,**kwargs):
        # creating new post and adding to the social feed
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm(request.POST)

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
        