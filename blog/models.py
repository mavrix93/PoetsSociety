from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.


@python_2_unicode_compatible
class PoetsGroup(models.Model):
    PUBLIC_SITE = "PUB"
    PRIVATE_SITE = "PRIV"
    VISIBILITY_CHOICES = [ (PUBLIC_SITE, "Public Site"), (PRIVATE_SITE, "Private Site")]

    name = models.CharField(max_length=200)
    visibility = models.CharField(
        choices=VISIBILITY_CHOICES,
        default=PUBLIC_SITE,
        max_length=4
    )


    #def isMember(self,user):

    def __str__(self):
        return self.name.encode('utf8')


@python_2_unicode_compatible
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    poet_group = models.ManyToManyField(PoetsGroup)

    def __str__(self):
        return (self.user.username).encode('utf8')


@python_2_unicode_compatible
class Poem(models.Model):
    PUBLIC_STATE = "PUB"
    DRAFT_STATE = "DRAFT"
    STATE_CHOICES = [ (PUBLIC_STATE, "Visible for other users"), (DRAFT_STATE, "Visible just for me (in the draft view)")]

    from_user = models.ForeignKey('auth.User', unique=False)
    poets_group = models.ForeignKey( PoetsGroup, unique=False)
    poet =  models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    visibility = models.CharField(
        choices=STATE_CHOICES,
        default=PUBLIC_STATE,
        max_length=5)


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title.encode('utf8')
