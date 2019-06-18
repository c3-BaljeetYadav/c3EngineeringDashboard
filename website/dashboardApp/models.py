from django.db import models


class JiraStatistics(models.Model):
    class Meta:
        unique_together = (('User', 'SprintNum',))
    
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
    # class Meta:
    #     unique_together = (('User', 'Repo',))

    # User = models.CharField(max_length=100)
    # Repo = models.CharField(max_length=100)
    Repo = models.CharField(max_length=100, primary_key=True)
    Number = models.IntegerField()
    Additions = models.IntegerField()
    Deletions = models.IntegerField()


class GithubPullRequestNotification(models.Model):
    # class Meta:
    #     unique_together = (('User', 'Number',))

    # User = models.CharField(max_length=100)
    # Number = models.IntegerField()
    Number = models.IntegerField(primary_key=True)
    Title = models.CharField(max_length=150)
    Url = models.CharField(max_length=300)
