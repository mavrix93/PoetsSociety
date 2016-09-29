from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.utils import timezone
from .models import Poem, PoetsGroup
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from operator import __or__ as OR
from django.db.models import Q

from .forms import PoemForm
from utils import helpers, site_conf

# Create your views here.

#TODO create generic views
@login_required
def group_poem_list(request, group_name):
    poets_group = get_object_or_404( PoetsGroup, name = group_name )
    if poets_group.visibility == "PRIV" and poets_group != request.user.userprofile_set.first().poet_group.all():
        message = "This group is private and you have no permission to see it."
        return render( request, 'blog/error_page.html', {'message': message, 'group_name': site_conf.ERROR_HEADER} )

    poems = Poem.objects.filter(poets_group = poets_group).exclude(visibility="DRAFT").order_by('published_date').reverse()

    poems_preview = helpers.get_first_verses(poems)
    return render( request, 'blog/poem_list.html', {'poems': poems_preview, 'group_name':group_name} )

@login_required
def draft_poem_list(request):
    GROUP_NAME = "My Drafts"
    poems = Poem.objects.filter(visibility="DRAFT", from_user=request.user).order_by('created_date').reverse()

    poems_preview = helpers.get_first_verses(poems)
    return render( request, 'blog/poem_list.html', {'poems': poems_preview, 'group_name':GROUP_NAME} )

@login_required
def my_poem_list(request):
    GROUP_NAME = "My Poems"
    poems = Poem.objects.filter(from_user=request.user).exclude(visibility="DRAFT").order_by('published_date').reverse()

    poems_preview = helpers.get_first_verses( poems )

    return render( request, 'blog/poem_list.html', {'poems': poems_preview, 'group_name':GROUP_NAME} )


@login_required
def poem_list(request):
    GROUP_NAME = "Poet Society"
    this_user = request.user
    follow_groups = this_user.userprofile_set.first().poet_group.all()

    follow_groups_list = list( follow_groups )

    try:
        lst = []
        for group in follow_groups:
            lst.append( Q( poets_group=PoetsGroup.objects.get( name=group.name ) ) )

        poems = Poem.objects.filter( reduce( OR, lst ) ).order_by( 'published_date' ).exclude(
            visibility="DRAFT" ).reverse( )


        #Get text of following groups
        follow_txt = "You are following"
        follow_groups_txt = ""
        if len(follow_groups) > 1:
            for group in follow_groups_list[:-1]:
                follow_groups_txt += group.name + ", "
            follow_groups_txt = follow_groups_txt[:-2] + " and " + follow_groups_list[-1].name + "."
        else:
            follow_groups_txt = follow_groups_list[0].name
        poems_preview = helpers.get_first_verses( poems )

    except (IndexError, TypeError):
        follow_groups_txt = ""
        poems_preview = []
        follow_txt = 'You are not following any group. Go to "Groups" in order to specify groups which will be followed'


    return render(request, 'blog/poem_list.html', {'follow_txt': follow_txt, 'followed_groups': follow_groups_txt,'poems': poems_preview, 'group_name': GROUP_NAME})

@login_required
def poem_detail(request, pk):
    poem = get_object_or_404(Poem, pk=pk)

    if poem.visibility == "DRAFT" and poem.from_user != request.user:
        message = "This poem is in draft and it is not yours. So I will not show you this one..."
        return render( request, 'blog/error_page.html', {'message': message, 'group_name': site_conf.ERROR_HEADER} )

    return render(request, 'blog/poem_detail.html', {'poem': poem, 'group_name': poem.poets_group})


@login_required
def poem_edit(request, pk):
    poem = get_object_or_404(Poem, pk=pk)

    if not poem.from_user == request.user:
        message = "This poem is not yours, so you cannot edit it."
        return render( request, 'blog/error_page.html', {'message': message, 'group_name':site_conf.ERROR_HEADER} )

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
        message = "This poem is not yours, so you cannot delete it."
        return render( request, 'blog/error_page.html', {'message': message, 'group_name':site_conf.ERROR_HEADER} )


@login_required
def groups_list(request):
    poets_groups = PoetsGroup.objects.filter(visibility="PUB")
    followed_groups = request.user.userprofile_set.first().poet_group.all()
    private_groups = PoetsGroup.objects.filter( visibility="PRIV" )

    following = []
    not_following = []
    for group in poets_groups:
        if group in followed_groups:
            following.append(group)
        else:
            not_following.append(group)

    return render(request, 'blog/poets_groups.html', {'following': following,
                                                      'not_following':not_following,
                                                      'private_groups': private_groups,
                                                      'group_name': site_conf.MAIN_HEADER})


@login_required
def follow_group(request, group_name):
    this_user = request.user
    group = get_object_or_404(PoetsGroup, name = group_name)

    this_user.userprofile_set.first().poet_group.add(group)

    return redirect('groups_list')

@login_required
def leave_group(request, group_name):
    this_user = request.user
    this_user.userprofile_set.first().poet_group.remove(*PoetsGroup.objects.filter(name=group_name))
    return redirect('groups_list')

@login_required
def my_profile(request):
    GROUP_NAME = "My profile"
    this_user = request.user
    groups = this_user.userprofile_set.first().poet_group.all()
    poems = this_user.poem_set.exclude(visibility="DRAFT")

    poems_preview = helpers.get_first_verses(poems)

    drafts = this_user.poem_set.filter(visibility="DRAFT")
    poets_num = len(poems)
    return render( request, 'blog/my_profile.html',
                   {'groups': groups,
                    'group_name':GROUP_NAME,
                    'poets_num': poets_num,
                    'poems': poems_preview,
                    'drafts_num' : len(drafts)
                    } )