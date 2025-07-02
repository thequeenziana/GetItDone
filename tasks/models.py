from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)  
    project_name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)
    collaborators = models.ManyToManyField(User, related_name='collaborating_projects', blank=True)
    
    def __str__(self):
        return self.project_name

class Task(models.Model):
    task_id = models.AutoField(primary_key=True) 
    task_name = models.CharField(max_length=100)
    parent_project = models.ForeignKey(Project, on_delete=models.CASCADE)
    completion = models.BooleanField(default=False)  
    description = models.TextField(default="")  # Providing a default value
    time = models.IntegerField(default=0)
    PRIORITY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ) 
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Low')
    deadline = models.DateTimeField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks')
    STATUS_CHOICES = (
        ('Did Not Start', 'Did Not Start'),
        ('InProgress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Need Help','Need Help')
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    def save(self, *args, **kwargs):
        if not self.assigned_to_id:  # Check if assigned_to is not already set
            self.assigned_to = self.parent_project.created_by
        super().save(*args, **kwargs)

    def __str__(self):
        return self.task_name
    
    def mark_as_complete(self):
        self.completion = True
        self.save()




class Notice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    notice = models.TextField(default="End", null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE,default=None, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=None, null=True, blank=True)  # Allow NULL values
    

    
def __str__(self):
    return f"Task: {self.task.task_name} - Notice: {self.notice}"
    

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.content
    
class Message(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    related_project = models.ForeignKey(Project, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return f"From: {self.from_user.username} | To: {self.to_user.username} | Project: {self.related_project.project_name}"


class Theme(models.Model):
    name = models.CharField(max_length=200)
    video = models.FileField(upload_to='themes/')

    def __str__(self):
        return self.name