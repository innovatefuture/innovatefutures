# pyre-strict

from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.db import models
from uuid import uuid4

from userauth.models import CustomUser # pyre-ignore[21]

from typing import List, Dict

def validate_poll_options(value: List[str]) -> bool:
    if type(value) == list and all(map(lambda x: type(x) == str, value)):
        return True
    else:
        raise ValidationError('poll options must be a list of strings (got ' + repr(value) + ')')

class BasePoll(models.Model):
    uuid: models.UUIDField = models.UUIDField(default = uuid4)
    question: models.CharField = models.CharField(max_length = 100)
    options: models.JSONField = models.JSONField(validators = [validate_poll_options])
    expires: models.DateTimeField = models.DateTimeField()
    closed: models.BooleanField = models.BooleanField(default = False)
    vote_kind: models.Model = BaseVote
    # initialise the votes relevant to this poll. needed so we know who's allowed to vote on it. should be called after creating any poll
    def make_votes(self, project) -> None: # pyre-ignore[2] can't import Project for this, see next line
        from project.models import ProjectMembership # pyre-ignore[21] this is considered bad form, but as far as i can tell necessary to avoid a circular import
        for voter in ProjectMembership.objects.filter(project = project):
            self.vote_kind.objects.create(user = voter.user, poll = self, choice = None)
    @property
    def current_results(self) -> Dict[str,List[CustomUser]]: # pyre-ignore[11]
        votes = Vote.objects.filter(poll = self, choice__isnull = False)
        results = {self.options[n-1] if n != 0 else 'poll is wrong':[] for n in range(len(self.options) + 1)}
        for vote in votes:
            results[self.options[vote.choice - 1] if vote.choice != 0 else 'poll is wrong'].append(vote.user)
        return results
    def check_closed(self) -> bool:
        if self.closed:
            return True
        elif self.expires < timezone.now():
            self.closed = True
            self.save()
            return True
        else:
            if vote_nums[0] > vote_nums[1] + len(Vote.objects.filter(poll = self, choice__isnull = True)):
                # if all remaining votes went to the current second-place option it still wouldn't equal the top option
                self.closed = True
                self.save()
                return True
            else:
                return False

class SingleChoicePoll(BasePoll):
    vote_kind = SingleVote

class MultipleChoicePoll(BasePoll):
    vote_kind = MultipleVote

class BaseVote(models.Model):
    user: models.ForeignKey = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    poll: models.ForeignKey = models.ForeignKey(Poll, on_delete = models.CASCADE)

class SingleVote(BaseVote):
    choice: models.IntegerField = models.IntegerField(null = True, default = None)
    def clean(self) -> None:
        cleaned_data = super().clean()
        # 0 indicates the always-present unask-the-question option
        if self.choice < 0 or self.choice > len(self.poll.options):
            raise ValidationError('not a valid choice for that poll (got ' + str(self.choice) + ', expected an integer in 0 - ' + str(len(self.poll.options)) + ')')
        else:
            return cleaned_data

class MultipleVote(BaseVote):
    choice: ArrayField = ArrayField(models.IntegerField)
