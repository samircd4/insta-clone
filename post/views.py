from django.shortcuts import render, redirect, get_object_or_404

from post.models import Stream, Post, Follow, Tag
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