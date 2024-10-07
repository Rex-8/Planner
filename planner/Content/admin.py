from django.contrib import admin
from .models import Notes,ToDoList,Content,Task

# Register your models here.
admin.site.register(Notes)
admin.site.register(ToDoList)
admin.site.register(Task)