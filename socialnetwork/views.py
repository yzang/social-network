import json
import sys
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from socialnetwork.forms import *
from socialnetwork.models import *
from socialnetwork.s3 import s3_upload


@login_required
def home(request):
    context = {}
    posts = Post.objects.all().order_by('-post_date')
    context['posts'] = posts
    context['profile'] = Profile.objects.get(account=request.user);
    return render(request, 'home.html', context)


@transaction.atomic
def register(request):
    context = {}
    errors = []
    # Just display the register form
    if request.method == 'GET':
        return render(request, 'register_form.html', context)
    form = RegistrationForm(request.POST)
    context['form'] = form
    # If the form is not valid
    if not form.is_valid():
        return render(request, 'register_form.html', context)
    # If we get here the form data was valid.  Register and login the user.
    try:
        new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password'],
                                            email=form.cleaned_data['email'])
        new_user.is_active = False
        profile = Profile.objects.create(account=new_user,
                                         first_name=form.cleaned_data['first_name'],
                                         last_name=form.cleaned_data['last_name'])
        new_user.save()
        profile.save()
        token = default_token_generator.make_token(new_user)
        email_body = """
        Welcome to the SocialNetwork.  Please click the link below to
        verify your email address and complete the registration of your account: http://%s%s""" % (
        request.get_host(), reverse('confirm', args=(new_user.username, token)))
        send_mail(subject="Verify your email address",
              message=email_body,
              from_email="yzang@andrew.cmu.edu",
              recipient_list=[new_user.email])

        context['email'] = form.cleaned_data['email']
        # user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        # login(request, user)
    except:
        print sys.exc_info()
        errors.append("Error during register")
        context['errors'] = errors
        return render(request, 'register_form.html', context)
    return render(request,'needs-confirmation.html',context)


@login_required
def profile(request, user_id):
    context = {}
    user = get_object_or_404(User, id=user_id)
    if user:
        profile = Profile.objects.get(account=user)
        user_posts = Post.objects.filter(owner=profile).order_by('-post_date')
        followers = Profile.objects.filter(followee=user)
        followees = Profile.objects.filter(account=request.user, followee=user)
        context['posts'] = user_posts
        context['profile'] = Profile.objects.get(account=user);
        context['followers'] = followers
        context['followees'] = followees
    return render(request, 'profile.html', context)


@login_required
def edit_profile(request):
    context = {}
    profile = Profile.objects.get(account=request.user)
    context['profile'] = profile
    if request.method == 'GET':
        return render(request, 'edit_profile.html', context)
    form = EditProfileForm(request.POST, request.FILES, instance=profile)
    if not form.is_valid():
        context['form'] = form
        return render(request, 'edit_profile.html', context)
    if form.cleaned_data['avatar']:
        url = s3_upload(form.cleaned_data['avatar'], profile.id)
        profile.picture_url = url
    form.save()
    return redirect(reverse('profile', kwargs={'user_id': request.user.id}))


@login_required
def follow(request, id):
    friend = User.objects.get(id=id)
    user_profile = Profile.objects.get(account=request.user)
    user_profile.followee.add(friend)
    user_profile.save()
    return redirect(reverse('profile', kwargs={'user_id': id}))


@login_required
def unfollow(request, id):
    friend = User.objects.get(id=id)
    user_profile = Profile.objects.get(account=request.user)
    user_profile.followee.remove(friend)
    return redirect(reverse('profile', kwargs={'user_id': id}))


@login_required
def followees(request):
    context = {}
    profile = Profile.objects.get(account=request.user)
    followees = profile.followee.all()
    followee_profiles = Profile.objects.filter(account__in=followees)
    posts = Post.objects.filter(owner__in=followee_profiles).order_by('-post_date')
    context['posts'] = posts
    context['profile'] = profile
    return render(request, 'follower.html', context)


@login_required
@transaction.atomic
def add_post(request):
    context = {}
    form = AddPostForm(request.POST)
    # we handle the check in front-end
    if form.is_valid():
        user_profile = Profile.objects.get(account=request.user)
        content = request.POST['content']
        post = Post(owner=user_profile, content=content)
        post.save()
    return redirect(reverse('home'))


@login_required
def get_avatar(request, id):
    profile = get_object_or_404(Profile, id=id)
    if not profile.avatar:
        return Http404
    return HttpResponse(profile.avatar)


@login_required
def get_post_after(request):
    date = request.GET['date']
    response_text = ""
    if date:
        date = datetime.fromtimestamp(float(date) / 1000)
        posts = Post.objects.filter(post_date__gt=date).order_by('post_date')
        list = []
        for i in range(len(posts)):
            data = {}
            data['content'] = posts[i].content
            data['owner_id'] = posts[i].owner_id
            data['date'] = posts[i].post_date.strftime("%b-%d-%Y %H:%M:%S")
            data['first_name'] = posts[i].owner.first_name
            data['last_name'] = posts[i].owner.last_name
            if posts[i].owner.avatar:
                data['image'] = reverse('getAvatar', kwargs={'id': data['owner_id']})
            else:
                data['image'] = '/static/img/default-avatar.png'
            list.append(data)
        response_text = json.dumps(list)
    return HttpResponse(response_text, content_type='application/json')


@login_required
@transaction.atomic
def add_reply(request):
    form = AddReplyForm(request.POST)
    response_text = ""
    # we handle the check in front-end
    if form.is_valid():
        post = Post.objects.get(id=form.cleaned_data['post_id'])
        content = form.cleaned_data['content']
        user_profile = Profile.objects.get(account=request.user)
        reply = PostReply(owner=user_profile, content=content, post=post)
        reply.save()
        reply_list = PostReply.objects.filter(post=post)
        list = []
        for reply in reply_list:
            data = {}
            data['content'] = reply.content
            data['owner_id'] = reply.owner_id
            data['date'] = reply.reply_date.strftime("%b-%d-%Y %H:%M:%S")
            data['first_name'] = reply.owner.first_name
            data['last_name'] = reply.owner.last_name
            if reply.owner.picture_url:
                data['image'] = reply.owner.picture_url
            else:
                data['image'] = '/static/img/default-avatar.png'
            list.append(data)
        response_text = json.dumps(list)
    return HttpResponse(response_text, content_type='application/json')

@transaction.atomic
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'confirmed.html', {})