from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Track(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)

#We're Using the tracks app to make the Like model, and hence will use the tracks app's schema for the likes query & mutations
class Like(models.Model):
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    # related_name here created a field 'likes' on Track model, beside the Like model having a field called track. Its an inverse relationship 
    track = models.ForeignKey('tracks.Track', related_name='likes', on_delete=models.CASCADE)