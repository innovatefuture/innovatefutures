# pyre-strict

from django.db import models
from userauth.models import CustomUser # pyre-ignore[21]
from urllib.parse import quote
from hashlib import shake_256

class Idea(models.Model):
    slug = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    proposed = models.ForeignKey('userauth.CustomUser', null=True, on_delete=models.SET_NULL) # null=true means nullable
    def save(self, *args, **kwargs):
        if (self.slug == ''):
            self.slug = quote(self.name)[:86] + shake_256(str(self.id).encode()).hexdigest(8)
        super().save(*args, **kwargs)

class IdeaSupport(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    user = models.ForeignKey('userauth.CustomUser', on_delete=models.CASCADE)

# ---

class Project(models.Model):
    slug = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    def save(self, *args, **kwargs):
        if (self.slug == ''): # shouldn't happen because created from ideas with existing slugs, but just in case
            self.slug = quote(self.name)[:86] + shake_256(str(self.id).encode()).hexdigest(8)
        super().save(*args, **kwargs)

class ProjectMembership(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey('userauth.CustomUser', on_delete=models.CASCADE)
    owner = models.BooleanField(default = False)
    champion = models.BooleanField(default = False)
