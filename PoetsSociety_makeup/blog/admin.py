from django.contrib import admin
from .models import Poem, UserProfile, PoetsGroup

admin.site.register(Poem)
admin.site.register(PoetsGroup)
admin.site.register(UserProfile)
