from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect

from post.models import Stream, Post, Follow, Tag, Likes
from authuser.models import Profile
from post.forms import NewPostForm

from django.contrib.auth.decorators import login_required

def index(request):
    user = request.user
    posts = Stream.objects.filter(user=user)
    group_ids = []
    for post in posts:
        group_ids.append(post.post_id)
    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')
    user = request.user
    context = {
        'post_items':post_items,
        'user': user
    }
    return render(request, 'index.html', context)

def NewPost(request):
    user = request.user
    tags_obj = []
    
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tag_form = form.cleaned_data.get('tag')
            tag_list = list(tag_form.split(','))    
            for tag in tag_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_obj.append(t)
            
            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user=user)
            p.tag.set(tags_obj)
            p.save()
            return redirect('index')
    else:
        form = NewPostForm()
    context = {
    'form': form
    }
    return render(request, 'newpost.html', context)

def postDetail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post':post
    }
    return render(request, 'post-details.html', context)

def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()

    if not liked:
        liked = Likes.objects.create(user=user, post=post)
        current_likes = current_likes + 1
    else:
        liked = Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1
        
    post.likes = current_likes
    post.save()
    return HttpResponseRedirect(reverse('post-details', args=[post_id]))

def favourite(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)

    if profile.favourite.filter(id=post_id).exists():
        profile.favourite.remove(post)
    else:
        profile.favourite.add(post)
    return HttpResponseRedirect(reverse('post-details', args=[post_id]))