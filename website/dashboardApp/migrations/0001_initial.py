from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JiraStatistics',
            fields=[
                ('SprintNum', models.IntegerField(primary_key=True)),
                ('P0Completed', models.IntegerField()),
                ('P0Assigned', models.IntegerField()),
                ('P1Completed', models.IntegerField()),
                ('P1Assigned', models.IntegerField()),
                ('SprintCompleted', models.IntegerField()),
                ('SprintAssigned', models.IntegerField()),
                ('NumberOfCompletedRcas', models.IntegerField()),
                ('UnderestimatedTicketRates', models.DecimalField(max_digits=5, decimal_places=2))
            ]
        ),
        migrations.CreateModel(
            name='GithubPullRequestSize',
            fields=[
                ('Repo', models.CharField(max_length=100, primary_key=True)),
                ('Number', models.IntegerField()),
                ('Additions', models.IntegerField()),
                ('Deletions', models.IntegerField())
            ]
        ),
        migrations.CreateModel(
            name='GithubPullRequestNotification',
            fields=[
                ('Number', models.IntegerField(primary_key=True)),
                ('Title', models.CharField(max_length=150)),
                ('Url', models.CharField(max_length=300))
            ]
        )
    ]
