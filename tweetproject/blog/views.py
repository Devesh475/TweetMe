from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponseRedirect, reverse, redirect
from .models import Blog, BlogComment
from .forms import postform, commentform
from user.models import userform
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

def util():
    users = userform.objects.all()
    famoususers = {}
    for x in users:
        name = x.user.username
        followersCount = x.followers.all().count()
        famoususers[name] = followersCount
    newlist = sorted(famoususers.items(), key = lambda kv:(kv[1], kv[0]))
    famoususers = []
    top3 = len(newlist)
    for x in range(top3-3,top3):
        for y in newlist[x]:
            if type(y) == str:
                famoususers.append(y)
    users = []
    for x in famoususers:
        u = User.objects.get(username=x)
        users.append({u : userform.objects.get(user=u)})
    return users

def home(request):
    posts = Blog.objects.all()
    posts = posts.order_by('-dateTime')
    allposts = []
    for post in posts:
        pro = userform.objects.get(user=post.user)
        allposts.append({post:pro})
    template_name = "home.html"
    context = {"posts":allposts}
    return render(request, template_name, context)

@login_required
def bloglist(request):
    context = {}
    user = User.objects.get(id=request.user.id)
    if userform.objects.filter(user=user).exists():
        obj = userform.objects.get(user=user)
        username = obj.user
        followers = obj.followers.all()
        followerslst = []
        for x in followers:
            followerslst.append(x)
        following = obj.following.all()
        followinglst = []
        for x in following:
            followinglst.append(x)
        bio = obj.bio
        context['obj'] = obj
        context['username'] = username
        context['followersCount'] = len(followerslst)
        context['followingCount'] = len(followinglst)
        context['bio'] = bio
    else:
        context['username'] = user
    posts = Blog.objects.filter(user=request.user)
    if userform.objects.filter(user=request.user).exists():
        obj = userform.objects.get(user=request.user)
        following = obj.following.all()
        for x in following:
            posts = posts | Blog.objects.filter(user=x)
    
    posts = posts.order_by('-dateTime')
    allposts = []
    for post in posts:
        pro = userform.objects.get(user=post.user)
        allposts.append({post:pro})
        
    f = util()
    template_name = "allposts.html"
    context["posts"] = allposts
    context["whotofollow"] = f
    return render(request, template_name, context)

@login_required
def blogdetail(request, pk):
    post = get_object_or_404(Blog, id=pk)
    form = commentform(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.post = post
        obj.user = request.user
        obj.save()
    
    comments = BlogComment.objects.filter(post=post)
    total_likes = post.total_likes()
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = False
    else:
        liked = True
    form = commentform()
    template_name = "postdetail.html"
    context = {"liked":liked, "post":post, "total_likes":total_likes, "comments":comments, "form":form}
    return render(request, template_name, context)

@login_required
def postlike(request, pk):
    post = get_object_or_404(Blog,id=pk)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('blogdetail', args=[str(pk)]))

@login_required
def postcreate(request):
    form = postform(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect('/detail/'+str(obj.id))

    form = postform()
    template_name = "postcreate.html"
    context = {'form':form}
    return render(request, template_name, context)

@login_required
def postdelete(request, pk):
    post = Blog.objects.filter(id=pk)
    if post is not None:
        post.delete()
        return redirect('/all')
    template_name = "postdelete.html"
    context = {}
    return render(request, template_name, context)

@login_required
def postupdate(request, pk):
    obj = get_object_or_404(Blog, id=pk)
    form = postform(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("/detail/"+str(pk))
    context = {"form":form,"update":True}
    template_name = "postupdate.html"
    return render(request, template_name, context)

@login_required
def deletecomment(request, pk):
    obj = BlogComment.objects.get(id=pk)
    post = obj.post
    print(post)
    obj.delete()
    return redirect('/detail/'+str(post.id))

@login_required
def postretweet(request, pk):
    parentpost = Blog.objects.get(id=pk)
    user = request.user
    if request.method == "POST":
        print(parentpost.captions)
        newBlog = Blog.objects.create(user=user, parent=parentpost, captions=parentpost.captions)
        return redirect('/detail/'+str(newBlog.pk))
    return redirect('/detail/'+str(pk))