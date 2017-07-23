from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE, default=1)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    content = models.CharField(max_length=1000, blank=True, default='')

    @staticmethod
    def get_absolute_url(self):
        return reverse("posts:post_detail")

    class Meta:
        ordering = ('created',)


