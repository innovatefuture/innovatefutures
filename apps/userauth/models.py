# pyre-strict

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse

from typing import List, Optional


class CustomUser(AbstractUser):
    first_name: None = None  # pyre-ignore[15] (pyre thinks this field can't be None in the parent class)
    last_name: None = None  # pyre-ignore[15]
    display_name: models.CharField = models.CharField(verbose_name=_("Display name"),
                                                      max_length=30, help_text=_("Will be shown alongside entries"),
                                                      null=True)
    year_of_birth: models.PositiveIntegerField = models.PositiveIntegerField(verbose_name=_("Year of birth"),
                                                                             validators=[MinValueValidator(1900),
                                                                                         MaxValueValidator(2021)],
                                                                             null=True, blank=True)
    post_code: models.CharField = models.CharField(verbose_name=_("Post code"), max_length=8, null=True, blank=True)

    class Meta:
        ordering: List[str] = ['display_name']

    # to redirect to account profile page
    def get_absolute_url(self) -> str:
        return reverse('profile_view')

    def __str__(self) -> str:
        return f"{self.display_name}"

class UserRequest(models.Model):
    kind: models.CharField = models.CharField(max_length=15) # one of the following, we can't put better type constraints on the db:
    # make_moderator, change_postcode, change_dob, other
    reason: models.CharField = models.CharField(max_length=1000)
    date: models.DateTimeField = models.DateTimeField('date/time request made')
    user: models.ForeignKey = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
