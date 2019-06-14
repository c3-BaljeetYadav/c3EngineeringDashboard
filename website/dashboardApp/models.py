from django.db import models


class JiraStatistics(models.Model):
    SprintNum = models.IntegerField(primary_key=True, unique=True)
    P0Completed = models.IntegerField()
    P0Assigned = models.IntegerField()
    P1Completed = models.IntegerField()
    P1Assigned = models.IntegerField()
    SprintCompleted = models.IntegerField()
    SprintAssigned = models.IntegerField()
    NumberOfCompletedRcas = models.IntegerField()
    UnderestimatedTicketRates = models.DecimalField(max_digits=5, decimal_places=2)


class GithubPullRequestSize(models.Model):
    Repo = models.CharField(max_length=100, primary_key=True)
    Number = models.IntegerField()
    Additions = models.IntegerField()
    Deletions = models.IntegerField()


class GithubPullRequestNotification(models.Model):
    Number = models.IntegerField(primary_key=True)
    Title = models.CharField(max_length=150)
    Url = models.CharField(max_length=300)
