from django.db import models

from utils.models import CommonModel

class ProjectTags(CommonModel):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "project_tags"

class Project(CommonModel):
    client = models.ForeignKey('users.ClientProfile', on_delete=models.CASCADE, related_name='projects')
    team_members = models.ManyToManyField('users.EmployeeProfile', related_name='projects')
    team_leaders = models.ManyToManyField('users.EmployeeProfile', related_name='leader_projects')
    project_managers = models.ManyToManyField('users.EmployeeProfile', related_name='manager_projects')
    tags = models.ManyToManyField(ProjectTags, related_name='projects')

    STATUSES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    PRIORITIES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUSES, default='active')
    start_date = models.DateField()
    end_date = models.DateField()
    priority = models.CharField(max_length=20, choices=PRIORITIES, default='medium')
    project_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class ProjectDocument(CommonModel):
    maker = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='created_documents') 
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='project_documents/')

    class Meta:
        db_table = "project_documents"


# Project Tasks

# Title
# Due Date
# Project Select
# Team Members
#  Tag 
 
# Status 

# Priority 
# Who Can See this Task?
# Public, Private, Admin Only

# Description

# Upload Attachment(s)


class ProjectTask(CommonModel):
    STATUSES = (
        ('todo', 'To Do'),
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('on_review', 'On Review'),
    )
    VISIBILITY_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
        ('admin_only', 'Admin Only'),
    )

    title = models.CharField(max_length=255)
    due_date = models.DateTimeField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    members = models.ManyToManyField('users.EmployeeProfile', related_name='tasks')
    tags = models.ManyToManyField(ProjectTags, related_name='tasks')
    
    status = models.CharField(max_length=20, choices=STATUSES, default='todo')
    priority = models.CharField(max_length=20, choices=Project.PRIORITIES, default='low')
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='private')
    description = models.TextField(blank=True, null=True)


    class Meta:
        db_table = "project_tasks"

class TaskAttachment(CommonModel):
    task = models.ForeignKey(ProjectTask, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='task_attachments/')

    class Meta:
        db_table = "task_attachments"
