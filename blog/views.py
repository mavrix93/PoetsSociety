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
    poems = Poem.objects.filter(poets_group = poets_groups).exclude(visibility="DRAFT")

    poems_preview = []
    for poem in poems:
        poem.text = helpers.get_first_verse( poem.text )
        poems_preview.append( poem )
    return render( request, 'blog/poem_list.html', {'poems': poems_preview, 'group_name':group_name} )

@login_required
def draft_poem_list(request):
    GROUP_NAME = "My Drafts"
    poems = Poem.objects.filter(visibility="DRAFT")

    poems_preview = []
    for poem in poems:
        poem.text = helpers.get_first_verse( poem.text )
        poems_preview.append( poem )
    return render( request, 'blog/poem_list.html', {'poems': poems_preview, 'group_name':GROUP_NAME} )

@login_required
def my_poem_list(request):
    GROUP_NAME = "My Poems"
    poems = Poem.objects.filter(from_user=request.user)

    poems_preview = []
    for poem in poems:
        poem.text = helpers.get_first_verse( poem.text )
        poems_preview.append( poem )
    return render( request, 'blog/poem_list.html', {'poems': poems_preview, 'group_name':GROUP_NAME} )


@login_required
def poem_list(request):
    GROUP_NAME = "PoetSociety"
    this_user = request.user
    #available_groups = PoetsGroup.objects.filter(userprofile__user= this_user)

    poems = Poem.objects.exclude(visibility="Draft").order_by('published_date').reverse()
    #poems = Poem.objects.filter(poets_group = this_user.userprofile_set.first().poet_group.all())
    #my_poems = Poem.objects.filter(from_user = this_user ).order_by('published_date').reverse()

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
    return render(request, 'blog/poem_edit.html', {'form': form})


@login_required
def poem_new(request):
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
    return render(request, 'blog/poem_edit.html', {'form': form})

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
    GROUP_NAME = "PoetSociety"
    poets_groups = PoetsGroup.objects.all()


    return render(request, 'blog/poets_groups.html', {'poets_groups':poets_groups})
