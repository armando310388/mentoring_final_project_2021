from django.db import models

# Create your models here.

class News(models.Model):
    source_web = models.CharField(max_length=100)
    title = models.CharField(max_length=300)
    creation_time = models.DateTimeField()
    url = models.CharField(max_length=400)
    clicks_counter = models.IntegerField(default=0)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.source_web + '_' + str(self.creation_time)

    def update_counter(self):
        self.clicks_counter += 1
        self.save()