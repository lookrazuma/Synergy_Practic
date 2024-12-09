# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from .models import Task, Comment
from .forms import TaskForm, CommentForm
from django.core.paginator import Paginator
from django.http import HttpResponse
import random

# Отображение списка задач
def task_list(request):
    task_list = Task.objects.all()  # Получаем все задачи
    paginator = Paginator(task_list, 5)  # Показывать 5 задач на странице
    page_number = request.GET.get('page')  # Получаем номер страницы из GET-запроса
    tasks = paginator.get_page(page_number)  # Получаем задачи для текущей страницы
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

# Создание новой задачи
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')  # Перенаправляем на список задач
        else:
            return render(request, 'tasks/task_form.html', {'form': form})  # Показываем ошибку
    else:
        form = TaskForm()
    
    return render(request, 'tasks/task_form.html', {'form': form})

# Редактирование задачи
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')  # Перенаправляем на список задач
        else:
            return render(request, 'tasks/task_form.html', {'form': form})  # Показываем ошибку
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'tasks/task_form.html', {'form': form})

# Удаление задачи
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('task_list')  # После удаления перенаправляем на страницу списка задач

# Обновление статуса задачи
def task_update_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    # Обновляем статус задачи
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Task.STATUS_CHOICES):
            task.status = new_status
            task.save()
    
    return redirect('task_list')

# Просмотр подробной информации о задаче
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    comments = task.comments.all()  # Получаем все комментарии к задаче
    comment_form = CommentForm()  # Форма для добавления нового комментария

    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'comments': comments,
        'comment_form': comment_form,
    })
    
def test_tasks(request):
    result_1 = None
    result_2 = None
    steps_1 = []  # Список для промежуточных шагов задачи 1
    steps_2 = []  # Список для промежуточных шагов задачи 2

    # Обрабатываем форму для задачи 1
    if request.method == 'POST':
        if 'task_1' in request.POST:
            result_1, steps_1 = task_1_solution(request)  # Возвращаем результат и шаги задачи 1
        elif 'task_2' in request.POST:
            result_2, steps_2 = task_2_solution()  # Возвращаем результат и шаги задачи 2

    # Отправляем результаты и шаги для отображения на странице
    return render(request, 'tasks/test_tasks.html', {
        'result_1': result_1,
        'result_2': result_2,
        'steps_1': steps_1,
        'steps_2': steps_2,
    })

# Задача 1: Сумма отрицательных чисел между максимальным и минимальным элементами массива
def task_1_solution(request):
    result_1 = None
    steps_1 = []  # Список шагов для отображения
    array_input = request.POST.get('array_input')

    if array_input:  # Проверка, что строка не пустая
        try:
            steps_1.append(f"Ввод массива: {array_input}")
            
            # Преобразуем строку в список чисел
            array = list(map(int, array_input.split(',')))
            steps_1.append(f"Преобразованный список: {array}")

            # Находим индексы максимального и минимального значения
            max_index = array.index(max(array))
            min_index = array.index(min(array))
            steps_1.append(f"Максимальное значение: {max(array)} на индексе {max_index}")
            steps_1.append(f"Минимальное значение: {min(array)} на индексе {min_index}")

            # Если максимальное значение идет раньше минимального, меняем их местами
            if max_index > min_index:
                max_index, min_index = min_index, max_index
                steps_1.append(f"Индексы максимального и минимального значения поменялись: max_index={max_index}, min_index={min_index}")

            # Суммируем отрицательные числа между ними
            negative_sum = sum(x for x in array[max_index+1:min_index] if x < 0)
            steps_1.append(f"Сумма отрицательных чисел между индексами: {negative_sum}")

            result_1 = negative_sum
        except ValueError:
            result_1 = "Ошибка: введены некорректные данные (не числовые значения или пустые)."
            steps_1.append(f"Ошибка: {result_1}")
    else:
        result_1 = "Ошибка: поле ввода пустое."
        steps_1.append("Ошибка: поле ввода пустое.")

    return result_1, steps_1

# Задача 2: Демонстрация работы методов базового и производного классов
def task_2_solution():
    steps_2 = []  # Список шагов для отображения
    result_2 = ""

    # Базовый класс
    class BaseClass:
        def greet(self):
            return "Бу, испугался? Это я, Базовый класс!"

    # Производный класс
    class DerivedClass(BaseClass):
        def greet(self):
            return "О нет! Я производный класс и мне очень страшно!"

    # Создание экземпляров классов
    base_instance = BaseClass()
    derived_instance = DerivedClass()

    # Демонстрация работы методов
    steps_2.append(f"Создали экземпляр базового класса: {base_instance}")
    steps_2.append(f"Создали экземпляр производного класса: {derived_instance}")
    
    base_greeting = base_instance.greet()
    derived_greeting = derived_instance.greet()

    steps_2.append(f"Результат работы метода базового класса: {base_greeting}")
    steps_2.append(f"Результат работы метода производного класса: {derived_greeting}")

    result_2 = f"{base_greeting} {derived_greeting}"

    return result_2, steps_2