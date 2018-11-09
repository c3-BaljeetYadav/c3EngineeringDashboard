from django.db import models

class Fruit(models.Model):
    name = models.CharField(max_length=255)
    amt = models.IntegerField()

    def __str__(self):
        return self.name


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class JiraLogSprintCompletion(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    key = models.CharField(max_length=255)
    assignee = models.CharField(max_length=255)
    sprint = models.CharField(max_length=255)
    date = models.DateField('%Y-%m-%d')
    timeSpent = models.CharField(max_length=255)



class JiraLogs(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    issueType = models.CharField(max_length=255)
    priority = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    assignee = models.CharField(max_length=255)
    sprint = models.CharField(max_length=255)
    originalEstimate = models.CharField(max_length=255)
    timeSpent = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    rca = models.CharField(max_length=512)


class GithubLogs (models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    mergeNumber = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    committer = models.CharField(max_length=255)
    file = models.CharField(max_length=512)
    additions = models.CharField(max_length=16)
    deletions = models.CharField(max_length=16)
    modifications = models.CharField(max_length=16)
    sprint = models.CharField(max_length=255)
