from django.contrib.auth.models import User
from django.db import models

class MemeTemplate(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.URLField()
    default_top_text = models.CharField(max_length=100, blank=True)
    default_bottom_text = models.CharField(max_length=100, blank=True)

class Meme(models.Model):
    template = models.ForeignKey(MemeTemplate, on_delete=models.CASCADE)
    top_text = models.CharField(max_length=100)
    bottom_text = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('meme', 'user')

class FunnyTemplatePhrases(models.Model):
    template = models.ForeignKey(MemeTemplate, on_delete=models.CASCADE, related_name='phrases')
    top_phrase = models.CharField(max_length=200)
    bottom_phrase = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.template.name} - {self.top_phrase[:20]}... | {self.bottom_phrase[:20]}..."
