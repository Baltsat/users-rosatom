from django.db import models

# Create your models here.

class QAItem(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    sentiment = models.CharField(max_length=50)
    j = models.IntegerField()
    cluster_id = models.IntegerField()
    topic_name = models.CharField(max_length=100)

    def __str__(self):
        return self.question
