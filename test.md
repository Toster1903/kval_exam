# ШПАРГАЛКА — DJANGO ЭКЗАМЕН
> **3 файла менять → 5 команд запустить → сдать**

---

## ПЛАН НА ЭКЗАМЕН (порядок действий)

| № | Что делать | Где |
|---|---|---|
| 1 | Запусти шаблон через Claude Code | Вставь промпт → жди файлы |
| 2 | Найди таблицу полей в билете | Раздел «Создайте таблицу ...» |
| 3 | Поправь `models.py` | Вписать поля из таблицы |
| 4 | Поправь `forms.py` | Вписать валидацию из раздела «Валидация» |
| 5 | Поправь `index.html` | Поменять названия колонок |
| 6 | `makemigrations` + `migrate` | Терминал VS Code (Ctrl+`) |
| 7 | `python manage.py test` | Должно быть: **OK** |
| 8 | `runserver` → показать комиссии | http://127.0.0.1:8000 |

---

## ФАЙЛ 1: `myapp/models.py`

> Смотришь таблицу в билете → каждая строка = одно поле в модели

### Шаблон (меняешь поля под свой вариант)

```python
from django.db import models
from datetime import date

class Item(models.Model):                       # имя класса не трогай
    name = models.CharField(max_length=200)     # ← МЕНЯЙ ЭТИ СТРОКИ
    description = models.TextField(blank=True)
    number_field = models.IntegerField(default=0)
    date_field = models.DateField(default=date.today)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  # НЕ ТРОГАЙ

    def __str__(self):
        return str(self.name)   # ← поменяй name на главное поле варианта
```

---

### Справочник типов полей

| Тип в билете | Django поле |
|---|---|
| `VARCHAR(200)` | `models.CharField(max_length=200)` |
| `VARCHAR(50)` уникальный | `models.CharField(max_length=50, unique=True)` |
| `TEXT` | `models.TextField()` |
| `INTEGER` | `models.IntegerField(default=0)` |
| `DECIMAL(10,2)` | `models.DecimalField(max_digits=10, decimal_places=2)` |
| `DATE` | `models.DateField(default=date.today)` |
| `TIMESTAMP` | `models.DateTimeField()` |
| `TIMESTAMP` автоматически | `models.DateTimeField(auto_now_add=True)` |
| `BOOLEAN` | `models.BooleanField(default=False)` |

### Модификаторы

| Условие в билете | Что добавить |
|---|---|
| не пустое | убери `blank=True` (просто `CharField(max_length=200)`) |
| по умолчанию 0 | `default=0` |
| по умолчанию сегодня | `default=date.today` (без скобок!) |
| уникальный | `unique=True` |
| может быть пустым | `blank=True, null=True` |
| создаётся автоматически | `auto_now_add=True` |

---

### Готовые примеры под популярные варианты

**Посты в блоге (posts)**
```python
title = models.CharField(max_length=200)
content = models.TextField()
published_at = models.DateField(default=date.today)
views = models.IntegerField(default=0)
is_published = models.BooleanField(default=False)
created_at = models.DateTimeField(auto_now_add=True)
```

**Товары (products)**
```python
name = models.CharField(max_length=150)
category = models.CharField(max_length=100, blank=True)
price = models.DecimalField(max_digits=10, decimal_places=2)
sku = models.CharField(max_length=50, unique=True)
created_at = models.DateTimeField(auto_now_add=True)
```

**Мероприятия (events)**
```python
title = models.CharField(max_length=200)
location = models.CharField(max_length=150, blank=True)
event_date = models.DateTimeField()
max_guests = models.IntegerField()
created_at = models.DateTimeField(auto_now_add=True)
```

**Клиенты (clients)**
```python
full_name = models.CharField(max_length=200)
email = models.EmailField(unique=True)
phone = models.CharField(max_length=20, blank=True)
birth_date = models.DateField(null=True, blank=True)
created_at = models.DateTimeField(auto_now_add=True)
```

**Задачи (tasks)**
```python
title = models.CharField(max_length=200)
description = models.TextField(blank=True)
due_date = models.DateField()
priority = models.IntegerField(default=1)
is_done = models.BooleanField(default=False)
created_at = models.DateTimeField(auto_now_add=True)
```

---

## ФАЙЛ 2: `myapp/forms.py`

> Смотришь раздел «Валидация» в билете → каждый пункт = одна проверка в `clean()`

### Полный шаблон со всеми типами проверок

```python
from django import forms
from datetime import date, datetime
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['id', 'created_at']   # эту строку не трогай

    def clean(self):
        cleaned_data = super().clean()

        # ── ПРОВЕРКА: поле не пустое ──────────────────────────────────────
        title = cleaned_data.get('title')
        if not title:
            self.add_error('title', 'Заголовок не может быть пустым')

        # ── ПРОВЕРКА: число больше нуля ───────────────────────────────────
        price = cleaned_data.get('price')
        if price is not None and price <= 0:
            self.add_error('price', 'Цена должна быть больше 0')

        # ── ПРОВЕРКА: число не отрицательное ─────────────────────────────
        views = cleaned_data.get('views')
        if views is not None and views < 0:
            self.add_error('views', 'Не может быть отрицательным')

        # ── ПРОВЕРКА: дата НЕ в будущем (поле DATE) ──────────────────────
        published_at = cleaned_data.get('published_at')
        if published_at and published_at > date.today():
            self.add_error('published_at', 'Дата не может быть в будущем')

        # ── ПРОВЕРКА: дата ДОЛЖНА быть в будущем (поле DATETIME) ─────────
        event_date = cleaned_data.get('event_date')
        if event_date and event_date <= datetime.now():
            self.add_error('event_date', 'Дата должна быть в будущем')

        return cleaned_data
```

### Шпаргалка по валидации

| Условие в билете | Код проверки |
|---|---|
| не может быть пустым | `if not field:` |
| больше 0 | `if field is not None and field <= 0:` |
| не отрицательное (≥ 0) | `if field is not None and field < 0:` |
| не в будущем (DATE) | `if field and field > date.today():` |
| только в будущем (DATETIME) | `if field and field <= datetime.now():` |
| уникальность | Django сам проверит если `unique=True` в модели |

> **Важно:** название переменной (`title`, `price` и т.д.) должно совпадать с именем поля в `models.py`

---

## ФАЙЛ 3: `myapp/templates/myapp/index.html`

> Меняешь только `<th>` заголовки и `{{ obj.??? }}` поля

### Что менять

```html
<!-- БЫЛО (шаблон): -->
<th>ID</th>
<th>Name</th>
<th>Date</th>
<th>Actions</th>

<td>{{ obj.id }}</td>
<td>{{ obj.name }}</td>
<td>{{ obj.date_field }}</td>

<!-- СТАЛО (пример для постов): -->
<th>ID</th>
<th>Заголовок</th>
<th>Дата публикации</th>
<th>Просмотры</th>
<th>Опубликован</th>
<th>Действия</th>

<td>{{ obj.id }}</td>
<td>{{ obj.title }}</td>
<td>{{ obj.published_at }}</td>
<td>{{ obj.views }}</td>
<td>{{ obj.is_published }}</td>
```

> **Правило:** `obj.???` — название после точки = точно такое же как поле в `models.py`

---

## 5 ОБЯЗАТЕЛЬНЫХ КОМАНД

```bash
# 1. Создать файл миграции из models.py
python manage.py makemigrations

# 2. Применить миграцию — создать таблицу в БД
python manage.py migrate

# 3. Собрать CSS/JS для DEBUG=False
python manage.py collectstatic --noinput

# 4. Запустить тест — должно быть OK
python manage.py test

# 5. Запустить сервер
python manage.py runserver
```

> **После любого изменения models.py** — обязательно повторить команды 1 и 2

---

## ЧТО НЕ ТРОГАТЬ

| Файл | Почему |
|---|---|
| `manage.py` | Точка входа Django |
| `myproject/settings.py` | Уже настроен (dotenv, whitenoise, middleware) |
| `myproject/urls.py` | Маршруты уже подключены |
| `myproject/wsgi.py` / `asgi.py` | Нужны серверу |
| `myapp/views.py` | Логика уже написана |
| `myapp/urls.py` | Маршруты уже прописаны |
| `myapp/middleware.py` | Метрики уже работают |
| `myapp/tests.py` | Тест уже написан |
| `myapp/admin.py` | Модель уже зарегистрирована |
| `base.html` / `form.html` / `confirm_delete.html` | Универсальные шаблоны |
| `.env` | Только если нужно поменять `SECRET_KEY` |

---

## ФИНАЛЬНЫЙ ЧЕКЛИСТ ПЕРЕД СДАЧЕЙ

```
☐  models.py — поля совпадают с таблицей в билете
☐  forms.py — все пункты из «Валидация» реализованы
☐  index.html — колонки соответствуют модели
☐  makemigrations — выполнен без ошибок
☐  migrate — выполнен без ошибок
☐  python manage.py test → OK (не FAIL)
☐  http://127.0.0.1:8000 — список записей открывается
☐  Создать запись через форму — работает
☐  Пустая форма — показывает ошибку валидации
☐  http://127.0.0.1:8000/admin/ — открывается со стилями
☐  http://127.0.0.1:8000/ping/ — возвращает OK
☐  metrics.log — создался в папке проекта
```

---

> **Итого: меняешь 3 файла → запускаешь 5 команд → сдаёшь**