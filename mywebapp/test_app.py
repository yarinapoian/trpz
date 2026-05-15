import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch
from app import app, create_html_response, get_accept_type
from models import Task


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


@pytest.fixture
def mock_task_service():
    with patch('app.task_service') as mock:
        yield mock


def test_create_html_response():
    result = create_html_response("<p>Test</p>", "TestTitle")
    assert "TestTitle" in result
    assert "<p>Test</p>" in result
    assert "<!DOCTYPE html>" in result


def test_get_accept_type_html():
    with app.test_request_context(headers={'Accept': 'text/html'}):
        assert get_accept_type() == 'html'


def test_get_accept_type_json():
    with app.test_request_context(headers={'Accept': 'application/json'}):
        assert get_accept_type() == 'json'


def test_get_accept_type_default():
    with app.test_request_context():
        assert get_accept_type() == 'json'


def test_get_tasks_empty_json(client, mock_task_service):
    mock_task_service.get_all_tasks.return_value = []
    response = client.get('/tasks', headers={'Accept': 'application/json'})
    assert response.status_code == 200
    assert response.json == []


def test_get_tasks_empty_html(client, mock_task_service):
    mock_task_service.get_all_tasks.return_value = []
    response = client.get('/tasks', headers={'Accept': 'text/html'})
    assert response.status_code == 200
    assert b'No tasks found' in response.data


def test_get_tasks_with_data_json(client, mock_task_service):
    task = Task(1, "Test Task", "todo", datetime(2024, 1, 1, 12, 0, 0))
    mock_task_service.get_all_tasks.return_value = [task]
    response = client.get('/tasks', headers={'Accept': 'application/json'})
    assert response.status_code == 200
    data = response.json
    assert len(data) == 1
    assert data[0]['title'] == "Test Task"


def test_get_tasks_with_data_html(client, mock_task_service):
    task = Task(1, "Test Task", "todo", datetime(2024, 1, 1, 12, 0, 0))
    mock_task_service.get_all_tasks.return_value = [task]
    response = client.get('/tasks', headers={'Accept': 'text/html'})
    assert response.status_code == 200
    assert b'<h1>Tasks</h1>' in response.data
    assert b'Test Task' in response.data


def test_create_task_json(client, mock_task_service):
    new_task = Task(1, "New Task", "todo", datetime(2024, 1, 1, 12, 0, 0))
    mock_task_service.create_task.return_value = new_task
    response = client.post('/tasks',
                           json={'title': 'New Task'},
                           headers={'Accept': 'application/json'})
    assert response.status_code == 201
    assert response.json['title'] == "New Task"


def test_create_task_html(client, mock_task_service):
    new_task = Task(1, "New Task", "todo", datetime(2024, 1, 1, 12, 0, 0))
    mock_task_service.create_task.return_value = new_task
    response = client.post('/tasks',
                           json={'title': 'New Task'},
                           headers={'Accept': 'text/html'})
    assert response.status_code == 201
    assert b'Task created successfully' in response.data


def test_create_task_missing_title(client, mock_task_service):
    response = client.post('/tasks',
                           json={},
                           headers={'Accept': 'application/json'})
    assert response.status_code == 400
    assert 'Title is required' in response.json['error']


def test_create_task_invalid_json(client, mock_task_service):
    response = client.post('/tasks',
                           data='invalid',
                           headers={'Content-Type': 'application/json',
                                    'Accept': 'application/json'})
    assert response.status_code == 400


def test_get_task_by_id_json(client, mock_task_service):
    task = Task(1, "Test Task", "todo", datetime(2024, 1, 1, 12, 0, 0))
    mock_task_service.get_task_by_id.return_value = task
    response = client.get('/tasks/1', headers={'Accept': 'application/json'})
    assert response.status_code == 200
    assert response.json['title'] == "Test Task"


def test_get_task_by_id_html(client, mock_task_service):
    task = Task(1, "Test Task", "todo", datetime(2024, 1, 1, 12, 0, 0))
    mock_task_service.get_task_by_id.return_value = task
    response = client.get('/tasks/1', headers={'Accept': 'text/html'})
    assert response.status_code == 200
    assert b'Task #1' in response.data


def test_get_task_not_found(client, mock_task_service):
    mock_task_service.get_task_by_id.return_value = None
    response = client.get('/tasks/999', headers={'Accept': 'application/json'})
    assert response.status_code == 404
    assert 'Task not found' in response.json['error']


def test_mark_task_done_json(client, mock_task_service):
    original_task = Task(1, "Test Task", "todo", datetime(2024, 1, 1, 12, 0, 0))
    done_task = Task(1, "Test Task", "done", datetime(2024, 1, 1, 12, 0, 0))
    mock_task_service.get_task_by_id.side_effect = [original_task, done_task]
    mock_task_service.mark_task_done.return_value = True
    response = client.post('/tasks/1/done', headers={'Accept': 'application/json'})
    assert response.status_code == 200
    assert response.json['status'] == "done"


def test_mark_task_done_html(client, mock_task_service):
    original_task = Task(1, "Test Task", "todo", datetime(2024, 1, 1, 12, 0, 0))
    done_task = Task(1, "Test Task", "done", datetime(2024, 1, 1, 12, 0, 0))
    mock_task_service.get_task_by_id.side_effect = [original_task, done_task]
    mock_task_service.mark_task_done.return_value = True
    response = client.post('/tasks/1/done', headers={'Accept': 'text/html'})
    assert response.status_code == 200
    assert b'Task marked as done' in response.data


def test_mark_task_done_not_found(client, mock_task_service):
    mock_task_service.get_task_by_id.return_value = None
    response = client.post('/tasks/999/done', headers={'Accept': 'application/json'})
    assert response.status_code == 404


def test_health_alive(client):
    response = client.get('/health/alive')
    assert response.status_code == 200
    assert response.data == b'OK'


def test_health_ready_connected(client, mock_task_service):
    mock_connection = MagicMock()
    mock_connection.is_connected.return_value = True
    mock_task_service.connection = mock_connection
    response = client.get('/health/ready')
    assert response.status_code == 200
    assert response.data == b'OK'


def test_health_ready_disconnected(client, mock_task_service):
    mock_connection = MagicMock()
    mock_connection.is_connected.return_value = False
    mock_task_service.connection = mock_connection
    response = client.get('/health/ready')
    assert response.status_code == 500


def test_models_task_to_dict():
    task = Task(1, "Test", "todo", datetime(2024, 1, 1, 12, 0, 0))
    d = task.to_dict()
    assert d['id'] == 1
    assert d['title'] == "Test"
    assert d['status'] == "todo"


def test_models_task_to_dict_compact():
    task = Task(1, "Test", "todo", datetime(2024, 1, 1, 12, 0, 0))
    d = task.to_dict_compact()
    assert d['id'] == 1
    assert d['title'] == "Test"


def test_models_task_default_status():
    task = Task(1, "Test")
    assert task.status == "todo"


def test_models_task_default_datetime():
    task = Task(1, "Test")
    assert isinstance(task.created_at, datetime)
