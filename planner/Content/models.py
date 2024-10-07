from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Content(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now=True)
    favourite = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user = User.objects.get(id=1)
            
        if isinstance(self, Notes):
            self.slug = f'n{self.id}'
        elif isinstance(self, ToDoList):
            self.slug = f't{self.id}'
            
        super().save(*args, **kwargs)

class Notes(Content):
    body = models.TextField()
    def get_content_type(self):
        return self.__class__.__name__

class ToDoList(Content):
    def __str__(self):
        return self.title

    def get_content_type(self):
        return self.__class__.__name__
    
class Task(models.Model):
    body = models.TextField(max_length=200)
    to_do_list = models.ForeignKey(ToDoList, related_name='tasks', on_delete=models.CASCADE)
    completion = models.BooleanField(default=False)
