from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.urls import reverse

class Author(models.Model):
    name=models.CharField(max_length=256)
    born_date=models.CharField(max_length=256)
    born_location=models.CharField(max_length=256)

    def __str__(self):
        return self.name

class Article(models.Model):
    author=models.ForeignKey(Author,on_delete=models.CASCADE,null=True)
    user=models.ManyToManyField(User,blank=True)
    body=models.TextField()
    title=models.CharField(max_length=256)
    tags=models.ManyToManyField('Tag',blank=True)

    def get_absolute_url(self):
        return reverse('spiders:detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

class Tag(models.Model):
    name=models.CharField(max_length=256)

    def __str__(self):
        return self.name

class Comment(models.Model):
    user=models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    article=models.ForeignKey(Article,null=True,on_delete=models.CASCADE)
    content=models.TextField()
    pub_date=models.DateTimeField(auto_now_add=True,editable=True)

    def __str__(self):
        return self.content