from django.db import models

from users.models import MyUser

class Product(models.Model):
    owner = models.CharField(max_length=100,)

class Lesson(models.Model):
    related_product = models.ManyToManyField(to=Product, related_name='lessons')
    title = models.CharField(max_length=100)
    video_url = models.URLField()
    video_duration = models.IntegerField(blank=False)

class AllowedProducts(models.Model):
    user = models.ForeignKey(to=MyUser, on_delete=models.CASCADE, related_name='allowed_products')
    products = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='allowed_to')

class WatchedLessons(models.Model):
    lesson = models.ForeignKey(to=Lesson, on_delete=models.CASCADE, related_name='users_watched')
    watcher = models.ForeignKey(to=MyUser, on_delete=models.CASCADE, related_name='watched_lessons')
    time_watched = models.IntegerField()
    last_watch_date = models.DateField(auto_now=True, null=True, blank=True)

    def is_completed(self):
        if self.time_watched / self.lesson.video_duration >= 0.8:
            return True
        else:
            return False

    class Meta:
        unique_together = ('lesson', 'watcher')