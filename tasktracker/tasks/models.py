from django.db import models

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершено'),
        ('on_hold', 'На паузе'),
    ]
    
    title = models.CharField('Заголовок задачи', max_length=200)
    description = models.TextField('Описание задачи')
    priority = models.CharField('Приоритет', max_length=10, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateField('Дата выполнения', null=True, blank=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_to = models.CharField('Ответственный', max_length=100, blank=True, null=True)
    completed = models.BooleanField('Завершена', default=False)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    user = models.CharField('Пользователь', max_length=100)
    content = models.TextField('Комментарий')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.user} к задаче {self.task.title}"
    
class TaskHistory(models.Model):
    array_input = models.CharField(max_length=255)  # Введенный массив как строка
    result = models.IntegerField()  # Результат решения задачи
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время решения задачи

    def __str__(self):
        return f"Решение от {self.created_at}"