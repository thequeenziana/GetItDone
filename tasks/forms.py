from django import forms
from .models import Task
from .models import Comment


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'description', 'priority', 'time']


class TimerForm(forms.Form):
    # Define fields for your timer form, if needed
    # For example, you might want to have fields for hours, minutes, and seconds
    hours = forms.IntegerField(label='Hours', min_value=0)
    minutes = forms.IntegerField(label='Minutes', min_value=0, max_value=59)
    seconds = forms.IntegerField(label='Seconds', min_value=0, max_value=59)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


from django import forms
from django.contrib.auth.models import User

class AssignTaskForm(forms.Form):
    assigned_to = forms.ModelChoiceField(queryset=User.objects.all())

