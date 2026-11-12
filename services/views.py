
from urllib.parse import quote

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.db.models import F, Q
from django.contrib.auth.models import User
from django.urls import reverse

from .models import ShortLink
from .forms import ShortLinkForm


@login_required
def home(request):
    if request.method == 'POST':
        form = ShortLinkForm(request.POST)

        if form.is_valid():
            link = form.save(commit=False)
            link.user = request.user
            link.save()

            messages.success(request, 'Ссылка успешно создана!')
            return redirect('home')
    else:
        form = ShortLinkForm()

    links = ShortLink.objects.filter(
        user=request.user
    )

    # Поиск
    search_query = request.GET.get('q', '').strip()

    if search_query:
        links = links.filter(
            Q(title__icontains=search_query) |
            Q(original_url__icontains=search_query) |
            Q(short_code__icontains=search_query)
        )

    # Сортировка
    sort = request.GET.get('sort', 'newest')

    sort_options = {
        'newest': '-created_at',
        'oldest': 'created_at',
        'popular': '-clicks',
        'least_popular': 'clicks',
    }

    order_by = sort_options.get(sort, '-created_at')
    links = links.order_by(order_by)

    # Короткие ссылки и QR-коды
    for link in links:
        short_path = reverse(
            'short_redirect',
            args=[link.short_code]
        )

        link.short_url = request.build_absolute_uri(short_path)

        encoded_url = quote(link.short_url, safe='')

        link.qr_url = (
            'https://api.qrserver.com/v1/create-qr-code/'
            f'?size=200x200&data={encoded_url}'
        )

    return render(request, 'home.html', {
        'form': form,
        'links': links,
        'search_query': search_query,
        'current_sort': sort,
    })


@login_required
def edit_link(request, link_id):
    link = get_object_or_404(
        ShortLink,
        id=link_id,
        user=request.user
    )

    if request.method == 'POST':
        form = ShortLinkForm(request.POST, instance=link)

        if form.is_valid():
            form.save()

            messages.success(request, 'Ссылка успешно обновлена!')
            return redirect('home')
    else:
        form = ShortLinkForm(instance=link)

    return render(request, 'edit_link.html', {
        'form': form,
        'link': link,
    })


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

    ShortLink.objects.filter(
        pk=link.pk
    ).update(
        clicks=F('clicks') + 1
    )

    return redirect(link.original_url)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'login.html', {
        'form': form,
        'register': True,
    })
