from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.utils import timezone
from .models import Poem, PoetsGroup
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse

from .forms import PoemForm
from utils import helpers

# Create your views here.

#TODO create generic views
@login_required
def group_poem_list(request, group_name):
    poets_groups = PoetsGroup.objects.filter(name = group_name)
    poems = Poem.objects.filter(poets_group = poets_groups).exclude(visibility="DRAFT").order_by('published_date').reverse()

    poems_preview = []
    for poem in poems:
        poem.text = helpers.get_first_verse( poem.text )
        poems_preview.append( poem )
    return render( request, 'blog/poem_list.html', {'poems': poems_preview, 'group_name':group_name} )

@login_required
def draft_poem_list(request):
    GROUP_NAME = "My Drafts"
    poems = Poem.objects.filter(visibility="DRAFT", from_user=request.user).order_by('created_date').reverse()

    poems_preview = []
    for poem in poems:
        poem.text = helpers.get_first_verse( poem.text )
        poems_preview.append( poem )
    return render( request, 'blog/poem_list.html', {'poems': poems_preview, 'group_name':GROUP_NAME} )

@login_required
def my_poem_list(request):
    GROUP_NAME = "My Poems"
    poems = Poem.objects.filter(from_user=request.user).exclude(visibility="DRAFT").order_by('published_date').reverse()

    poems_preview = []
    for poem in poems:
        poem.text = helpers.get_first_verse( poem.text )
        poems_preview.append( poem )
    return render( request, 'blog/poem_list.html', {'poems': poems_preview, 'group_name':GROUP_NAME} )


@login_required
def poem_list(request):
    GROUP_NAME = "Poet Society"
    this_user = request.user

    poems = Poem.objects.filter(poets_group = this_user.userprofile_set.first().poet_group.all()).exclude(visibility="DRAFT").order_by('published_date').reverse()


    poems_preview = []
    for poem in poems:
        poem.text = helpers.get_first_verse(poem.text)
        poems_preview.append(poem)
    return render(request, 'blog/poem_list.html', {'poems': poems_preview, 'group_name': GROUP_NAME})

@login_required
def poem_detail(request, pk):
    poem = get_object_or_404(Poem, pk=pk)

    return render(request, 'blog/poem_detail.html', {'poem': poem, 'group_name': poem.poets_group})


@login_required
def poem_edit(request, pk):
    poem = get_object_or_404(Poem, pk=pk)

    if not poem.from_user == request.user:
        return HttpResponse( "<h1>It is not yours poem!</h1>" )

    if request.method == "POST":
        form = PoemForm(request.POST, instance=poem)
        if form.is_valid():
            poem = form.save(commit=False)
            poem.from_user = request.user
            poem.save()
            return redirect('poem_detail', pk=poem.pk)
    else:
        form = PoemForm(instance=poem)
    return render(request, 'blog/poem_edit.html', {'form': form, 'group_name': poem.poets_group})


@login_required
def poem_new(request):
    GROUP_NAME = "Poets Society"
    if request.method == "POST":
        form = PoemForm(request.POST)
        if form.is_valid():
            poem = form.save(commit=False)
            poem.from_user = request.user
            poem.published_date = timezone.now( )
            poem.save( )
            return redirect('poem_detail', pk=poem.pk)
    else:
        form = PoemForm()
    return render(request, 'blog/poem_edit.html', {'form': form, 'group_name': GROUP_NAME})

@login_required
def poem_remove(request, pk):
    poem = get_object_or_404(Poem, pk=pk)
    if poem.from_user == request.user:
        poem.delete()
        return redirect('poem_list')
    else:
        return HttpResponse("<h1>It is not yours poem!</h1>")


@login_required
def groups_list(request):
    GROUP_NAME = "Public groups"
    poets_groups = PoetsGroup.objects.filter(visibility="PUB")


    return render(request, 'blog/poets_groups.html', {'poets_groups':poets_groups, 'group_name': GROUP_NAME})


@login_required
def follow_group(request, group_name):
    this_user = request.user
    group = get_object_or_404(PoetsGroup, name = group_name)

    this_user.userprofile_set.first().poet_group.add(group)

    return redirect('my_profile')

@login_required
def leave_group(request, group_name):
    this_user = request.user
    this_user.userprofile_set.first().poet_group.remove(*PoetsGroup.objects.filter(name=group_name))
    return redirect('my_profile')

@login_required
def my_profile(request):
    GROUP_NAME = "My profile"
    this_user = request.user
    groups = this_user.userprofile_set.first().poet_group.all()
    poems = this_user.poem_set.all()

    poems_preview = []
    for poem in poems:
        poem.text = helpers.get_first_verse( poem.text )
        poems_preview.append( poem )

    drafts = this_user.poem_set.filter(visibility="DRAFT")
    poets_num = len(poems)
    return render( request, 'blog/my_profile.html',
                   {'groups': groups,
                    'group_name':GROUP_NAME,
                    'poets_num': poets_num,
                    'poems': poems_preview,
                    'drafts_num' : len(drafts)
                    } )