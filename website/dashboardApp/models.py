from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(AbstractUser):
    GithubUser = models.CharField(max_length=50)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['GithubUser', 'password']

    def __str__(self):
        return self.username


class JiraStatistics(models.Model):
    class Meta:
        unique_together = ('User', 'SprintNum')

    id = models.CharField(max_length=150, primary_key=True)
    User = models.CharField(max_length=100)
    SprintNum = models.IntegerField()
    P0Completed = models.IntegerField()
    P0Assigned = models.IntegerField()
    P1Completed = models.IntegerField()
    P1Assigned = models.IntegerField()
    SprintCompleted = models.IntegerField()
    SprintAssigned = models.IntegerField()
    RcaCompleted = models.IntegerField()
    RcaTotal = models.IntegerField()
    UnderestimatedTicketRates = models.DecimalField(max_digits=5, decimal_places=2)


class GithubPullRequestSize(models.Model):
    class Meta:
        unique_together = ('User', 'Repo', 'Number')

    id = models.CharField(max_length=200, primary_key=True)
    User = models.CharField(max_length=100)
    Repo = models.CharField(max_length=100)
    Number = models.IntegerField()
    Additions = models.IntegerField()
    Deletions = models.IntegerField()


class GithubPullRequestNotification(models.Model):
    class Meta:
        unique_together = ('User', 'Number')

    id = models.CharField(max_length=150, primary_key=True)
    User = models.CharField(max_length=100)
    Number = models.IntegerField()
    Title = models.CharField(max_length=150)
    Url = models.CharField(max_length=300)
