
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.db.models import F
from django.contrib.auth.models import User

from .models import ShortLink
from .forms import ShortLinkForm


def home(request):
    links = []

    if request.user.is_authenticated:
        links = ShortLink.objects.filter(
            user=request.user
        ).order_by('-created_at')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        form = ShortLinkForm(request.POST)

        if form.is_valid():
            link = form.save(commit=False)
            link.user = request.user
            link.save()

            messages.success(request, 'Ссылка успешно создана!')
            return redirect('home')
    else:
        form = ShortLinkForm()

    return render(request, 'home.html', {
        'form': form,
        'links': links,
    })

def profile(request, username):
    profile_user = get_object_or_404(
        User,
        username=username
    )

    links = ShortLink.objects.filter(
        user=profile_user
    ).order_by('-created_at')

    return render(request, 'profile.html', {
        'profile_user': profile_user,
        'links': links,
    })


def short_redirect(request, code):
    link = get_object_or_404(
        ShortLink,
        short_code=code
    )

    ShortLink.objects.filter(pk=link.pk).update(
        clicks=F('clicks') + 1
    )

    return redirect(link.original_url)


@login_required
def delete_link(request, link_id):
    if request.method != 'POST':
        return HttpResponseBadRequest('POST required')

    link = get_object_or_404(
        ShortLink,
        id=link_id,
        user=request.user
    )

    link.delete()

    messages.success(request, 'Ссылка удалена!')
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'login.html',  {
        'form': form,
        'register': True,
    })
