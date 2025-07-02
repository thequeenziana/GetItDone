from django.contrib import admin
from .models import Notice
from .models import Task
from .models import Project
from .models import Theme
# Register your models here.
admin.site.register(Notice)
admin.site.register(Task)
admin.site.register(Project)
admin.site.register(Theme)