# Трекер задач

## Розрахунок завдання згідно з варіантом

Мій номер у списку групи студентів N = 22:
- V2 = (22 % 2) + 1 = 1
- V3 = (22 % 3) + 1 = 2
- V5 = (22 % 5) + 1 = 3

Завдання згідно з N:
- Застосунок: **Task Tracker**
- БД: **MariaDB**
- Порт: **3000**
- Спосіб конфігурації: **Command-line arguments**

## Опис проєкту

Трекер задач дозволяє користувачам створювати нові задачі, переглядати список усіх задач, отримувати деталі конкретної задачі та змінювати статус задачі на виконано. Застосунок підтримує як JSON, так і HTML відповіді залежно від заголовка `Accept` у запиті.

### Налаштування середовища для розробки

1. Скопіюйте репозиторій:
```bash
git clone https://github.com/yarinapoian/trpz.git
cd mywebapp
```

2. Створіть venv:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Встановіть залежності:
```bash
pip install -r requirements.txt
```

4. Налаштуйте базу даних (MariaDB):
```bash
mysql -u root -p < setup.sql
```

5. Запустіть міграцію бази даних:
```bash
python3 migrate.py --host=127.0.0.1 --user=app --password=app --database=task_tracker
```

## Запуск застосунку

```bash
python3 app.py --host=0.0.0.0 --port=3000 --db-host=127.0.0.1 --db-user=app --db-password=app --db-name=task_tracker
```

## API ендпоінти

### Health Check

#### GET `/health/alive`

**Response (200 OK):**
```
OK
```

#### GET `/health/ready`
Повертає HTTP 200 з вмістом OK якщо сервіс успішно підключився до БД і готовий обробляти запити.

**Response (200 OK):**
```
OK
```

**Response (500 Internal Server Error):**
```
Database connection not established
```

#### GET `/tasks`

Повертає список усіх задач.

**Response (200 OK - JSON):**
```json
[
  {
    "id": 1,
    "title": "Complete project",
    "status": "todo",
    "created_at": "2024-05-13T10:30:00.000000"
  },
  {
    "id": 2,
    "title": "Review code",
    "status": "done",
    "created_at": "2024-05-13T09:15:00.000000"
  }
]
```

**Response (200 OK - HTML):**
```html
<h1>Tasks</h1>
<table>
  <tr>
    <th>ID</th>
    <th>Title</th>
    <th>Status</th>
    <th>Created At</th>
  </tr>
  <tr>
    <td>1</td>
    <td>Complete project</td>
    <td>todo</td>
    <td>2024-05-13 10:30:00</td>
  </tr>
</table>
```

#### POST `/tasks`
Створює нову задачу.

**Request Body (JSON):**
```json
{
  "title": "Complete project"
}
```

**Response (201 Created - JSON):**
```json
{
  "id": 1,
  "title": "Complete project",
  "status": "todo",
  "created_at": "2024-05-13T10:30:00.000000"
}
```

**Response (400 Bad Request - JSON):**
```json
{
  "error": "Title is required"
}
```

#### GET `/tasks/<id>`
Повертає деталі конкретної задачі.

**Parameters:**
- `id` (required): Task ID

**Response (200 OK - JSON):**
```json
{
  "id": 1,
  "title": "Complete project",
  "status": "todo",
  "created_at": "2024-05-13T10:30:00.000000"
}
```

**Response (404 Not Found - JSON):**
```json
{
  "error": "Task not found"
}
```

#### POST `/tasks/<id>/done`
Позначає задачу як виконану.

**Parameters:**
- `id` (required): Task ID

**Response (200 OK - JSON):**
```json
{
  "id": 1,
  "title": "Complete project",
  "status": "done",
  "created_at": "2024-05-13T10:30:00.000000"
}
```

**Response (404 Not Found - JSON):**
```json
{
  "error": "Task not found"
}
```

# Розгортання

### Вимоги до середовища

- Ubuntu 20.04 LTS. Взяти можна: https://ubuntu.com/download/server
- Root-доступ
- 2GB RAM
- 10GB вільних дискового простору

### Автоматичне розгортання за допомогою скрипту

Для автоматичного розгортання треба спочатку скопіювати репозиторій на сервер, а потім виконати наступну команду:

```bash
cd deploy
sudo bash deploy.sh
```

### Як увійти на ВМ
Після розгортання можна увійти на ВМ за допомогою SSH:

```bash
ssh student@<vm_ip_address>
```