from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Task, Notice, Message, Comment
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from .forms import TimerForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import AssignTaskForm
from authentication.models import UserProfile
from .forms import CommentForm
@login_required
def create_project(request):
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        if project_name:
            project = Project.objects.create(project_name=project_name, created_by=request.user)
            return redirect('dashboard')  
    return render(request, 'authentication/dashboard.html')

@login_required
def project_page(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
        project_tasks = Task.objects.filter(parent_project_id=project_id)
    except Project.DoesNotExist:
        raise Http404("Project does not exist")

    return render(request, 'project_page.html', {'project': project, 'project_tasks': project_tasks})

@login_required
def create_task(request, project_id):
    project = Project.objects.get(pk=project_id)

    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        if task_name:
            task = Task.objects.create(task_name=task_name, parent_project=project)
            return redirect('project_page', project_id=project_id)
    
    return render(request, 'create_task.html', {'project': project})

@login_required
def delete_project(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        raise Http404("Project does not exist")

    if request.method == 'POST':
        project.delete()
    return redirect('dashboard')

@login_required
def delete_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    if request.method == 'POST':
        task.delete()
    return redirect('project_page', project_id=task.parent_project_id)

@login_required
def task_page(request, project_id, user_id, task_id):
    task = get_object_or_404(Task, pk=task_id)
    
    form = TimerForm()
    context = {'task': task, 'form': form, 'project_id': project_id, 'user_id': user_id, 'task_id': task_id}
    return render(request, 'task_page.html', context)

@login_required
def start_timer(request, task_id):
    # Start timer logic
    return redirect('task_page')

@login_required
def stop_timer(request, task_id):
    # Stop timer logic
    return redirect('task_page')

@login_required
def reset_timer(request, task_id):
    
    return redirect('task_page')

@login_required
def pause_timer(request, task_id):
    # Pause timer logic
    return redirect('task_page')

@login_required
def back_to_dashboard(request):
    return redirect('dashboard')

@login_required
def dashboard(request):
    fname = request.user.first_name
    user_projects = Project.objects.filter(created_by=request.user)
    return render(request, 'authentication/dashboard.html', {'user_projects': user_projects,'fname': fname})

@login_required
def add_collaborator(request, project_id, username):
    project = get_object_or_404(Project, project_id=project_id)
    collaborator = get_object_or_404(User, username=username)
    project.collaborators.add(collaborator)

    messages.success(request, f"{collaborator.username} added as a collaborator to the project.")
    return redirect('project_page', project_id=project_id)

@login_required
def remove_collaborator(request, project_id, username):
    project = get_object_or_404(Project, id=project_id)
    collaborator = get_object_or_404(User, username=username)
    project.collaborators.remove(collaborator)
    return redirect('dashboard')

@login_required
def set_deadline(request, project_id, task_id, user_name):
    if request.method == 'POST':
        deadline = request.POST.get('deadline')
        
        if deadline is None or not deadline.strip():
            return HttpResponse('Invalid deadline')

        # Fetch the Task, User, and Project objects or return a 404 error
        task = get_object_or_404(Task, task_id=task_id)
        user = get_object_or_404(User, username=user_name)
        project = get_object_or_404(Project, project_id=project_id)
        
        # Check if a notice for this task and user already exists and delete it if found
        existing_notice = Notice.objects.filter(task=task, project=project)
        if existing_notice:
            existing_notice.delete()

        # Update the task deadline
        task.deadline = deadline
        task.save()

        # Create a new notice for the updated deadline
        notice_message = f"The deadline for '{task.task_name}' in '{project.project_name}' has been updated to '{deadline}' for user '{task.assigned_to.username}'.        "
        messages.success(request, f'Task deadline Updated successfully')
        notice = Notice.objects.create(user=task.assigned_to, task=task, project=project, notice=notice_message)

        return redirect('project_page', project_id=project_id)




def assign_task(request, task_id, username):
    task = get_object_or_404(Task, pk=task_id)
    assigned_to = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = AssignTaskForm(request.POST)
        if form.is_valid():
            assigned_to = form.cleaned_data['assigned_to']
            task.assigned_to = assigned_to()
            task.save()
            messages.success(request, f"Task is assigned to: {assigned_to.username} successfully")
            return redirect('project_page', task_id=task_id)
    else:
        form = AssignTaskForm()
    return render(request, 'assign_task.html', {'form': form})

@login_required
def add_additional_details(request, project_id, task_id, user_name):
    if request.method == 'POST':
        # Get form data
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        status = request.POST.get('status')
        assigned_to_username = request.POST.get('assigned_to')  # Assuming username is passed
        
        # Retrieve project and task objects
        project = get_object_or_404(Project, pk=project_id)
        task = get_object_or_404(Task, pk=task_id)
        user_object=get_object_or_404(User,username=assigned_to_username)
        # Update task with additional details
        task.description = description
        task.priority = priority
        task.status = status
        
        # Check if task deadline exists
        if task.deadline:
            # Update username and notice in notifications
            notices = Notice.objects.filter(task_id=task_id).exclude(user=user_object.id)

            for notice in notices:
                notice.user = user_object
                notice.notice = f"Task {task.task_name} assigned to {assigned_to_username}"
                notice.save()
        
        
        assigned_to_user = User.objects.get(username=assigned_to_username)
        task.assigned_to = assigned_to_user
        
        task.save()
        messages.success(request, f'Task details added successfully!')
        return redirect('project_page', project_id=project_id)
    else:
        return HttpResponse('Invalid request method')

@login_required
def notifications(request, user_id):
    user = get_object_or_404(User, id=user_id)
    notifications = Notice.objects.filter(user=user)
    return render(request, 'notifications.html', {'notifications': notifications})
@login_required
def mssgs(request, user_id):
    user = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(to_user_id=user.id)
    # Render the notifications.html template with the notifications data
    return render(request, 'mssgs.html', {'messages': messages})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.mark_as_complete()
    messages.success(request, f'Task marked as complete!')
    return redirect('project_page', project_id=task.parent_project_id)


@login_required
def add_comment(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.created_by = request.user
            comment.project = project
            comment.save()
            return redirect('project_page', project_id=project_id)
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.created_by:
        comment.delete()
    return redirect('project_page', project_id=comment.project.project_id)


def send_message(request):
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        project_id = request.POST.get('project_id')
        user_id = request.POST.get('user_id')
        message_text = request.POST.get('message')
        
        try:
            sender = User.objects.get(id=user_id)
            recipient = User.objects.get(id=recipient_id)
            project = Project.objects.get(project_id=project_id)  # Assuming project_id is the primary key of the Project model
            
            message = Message.objects.create(
                from_user=sender,
                to_user=recipient,
                related_project=project,
                message=message_text
            )
            
            
            messages.success(request, f'Message sent!')
            
            
            return redirect('project_page', project_id=project_id)
        except Exception as e:
            # Use Django's messages framework to display an error message
            messages.error(request, f'An error occurred: {e}')
            return redirect('project_page',project_id=project_id)  # Redirect to an error page or handle the error accordingly


from .models import Theme

def immersion_mode(request,project_id):
    themes = Theme.objects.all()
    # project = Project.objects.get(created_by=request.user)# Get the current user's project
    project = Project.objects.get(project_id=project_id)
    tasks = Task.objects.filter(parent_project=project)  # Get the tasks for the current user's project
    return render(request, 'immersion_mode.html', {'themes': themes, 'tasks': tasks})

