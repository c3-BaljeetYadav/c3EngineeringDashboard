from django.contrib import admin
from .models import UserProfile, JiraStatistics, GithubPullRequestSize, GithubPullRequestNotification


admin.site.register(UserProfile)
admin.site.register(JiraStatistics)
admin.site.register(GithubPullRequestSize)
admin.site.register(GithubPullRequestNotification)
