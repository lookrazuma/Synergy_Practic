from django import forms
from .models import Task, Comment

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'due_date', 'status', 'assigned_to']
        labels = {
            'title': 'Заголовок задачи',
            'description': 'Описание задачи',
            'priority': 'Приоритет',
            'due_date': 'Дата выполнения',
            'status': 'Статус',
            'assigned_to': 'Ответственный',
        }
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'content']