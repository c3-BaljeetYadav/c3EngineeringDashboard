from django.contrib import admin
from .models import JiraStatistics, GithubPullRequestSize, GithubPullRequestNotification


admin.site.register(JiraStatistics)
admin.site.register(GithubPullRequestSize)
admin.site.register(GithubPullRequestNotification)
