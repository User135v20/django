Для начала работы перейдите в django1
```cd django1```

и примените миграцию
```python manage.py migrate```

запуск сервера
```python manage.py runserver```

админка
 ```http://127.0.0.1:8000/admin```
 
создание админа для админки
```python manage.py createsuperuser```
 
 показать все миграции
 ```python manage.py showmigrations```
 
откатить все миграции
```python manage.py migrate main zero```

откатить миграцию до нйжной
```python manage.py migrate main 0004```

создание миграций
```python manage.py makemigrations```
 
 