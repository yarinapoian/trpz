import argparse
from flask import Flask, request, jsonify
from service import TaskService

app = Flask(__name__)
task_service = None


def create_html_response(content: str, title: str = "Task Tracker") -> str:
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <meta charset="UTF-8">
    </head>
    <body>
        {content}
    </body>
    </html>
    """


def get_accept_type() -> str:
    accept1 = request.headers.get('Accept', 'application/json')
    if 'text/html' in accept1:
        return 'html'
    return 'json'


@app.route('/tasks', methods=['GET'])
def get_tasks():
    accept_type = get_accept_type()
    tasks = task_service.get_all_tasks()

    if accept_type == 'html':
        if not tasks:
            content = "<h1>Tasks</h1><p>No tasks found.</p>"
        else:
            rows = "".join([
                f"<tr><td>{t.id}</td><td>{t.title}</td><td>{t.status}</td><td>{t.created_at}</td></tr>"
                for t in tasks
            ])
            content = f"""
            <h1>Tasks</h1>
            <table border="1">
                <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Status</th>
                    <th>Created At</th>
                </tr>
                {rows}
            </table>
            """
        return create_html_response(content), 200
    else:
        return jsonify([t.to_dict_compact() for t in tasks]), 200


@app.route('/tasks', methods=['POST'])
def create_task():
    accept_type = get_accept_type()

    try:
        data = request.get_json()
        title = data.get('title')

        if not title:
            error_msg = "Title is required"
            if accept_type == 'html':
                return create_html_response(f"<h1>Error</h1><p>{error_msg}</p>"), 400
            else:
                return jsonify({"error": error_msg}), 400

        task = task_service.create_task(title)

        if accept_type == 'html':
            content = f"""
            <h1>Task Created</h1>
            <p>Task created successfully.</p>
            <p><strong>ID:</strong> {task.id}</p>
            <p><strong>Title:</strong> {task.title}</p>
            <p><strong>Status:</strong> {task.status}</p>
            <p><strong>Created At:</strong> {task.created_at}</p>
            """
            return create_html_response(content), 201
        return jsonify(task.to_dict()), 201
    except Exception as e:
        error_msg = f"Invalid request: {str(e)}"
        if accept_type == 'html':
            return create_html_response(f"<h1>Error</h1><p>{error_msg}</p>"), 400
        return jsonify({"error": error_msg}), 400


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    accept_type = get_accept_type()
    task = task_service.get_task_by_id(task_id)

    if task is None:
        error_msg = "Task not found"
        if accept_type == 'html':
            return create_html_response(f"<h1>Error</h1><p>{error_msg}</p>"), 404
        return jsonify({"error": error_msg}), 404

    if accept_type == 'html':
        content = f"""
        <h1>Task #{task.id}</h1>
        <p><strong>Title:</strong> {task.title}</p>
        <p><strong>Status:</strong> {task.status}</p>
        <p><strong>Created At:</strong> {task.created_at}</p>
        """
        return create_html_response(content), 200
    return jsonify(task.to_dict()), 200


@app.route('/tasks/<int:task_id>/done', methods=['POST'])
def mark_task_done(task_id):
    accept_type = get_accept_type()

    task = task_service.get_task_by_id(task_id)
    if task is None:
        error_msg = "Task not found"
        if accept_type == 'html':
            return create_html_response(f"<h1>Error</h1><p>{error_msg}</p>"), 404
        return jsonify({"error": error_msg}), 404

    task_service.mark_task_done(task_id)

    updated_task = task_service.get_task_by_id(task_id)

    if accept_type == 'html':
        content = f"""
        <h1>Task Updated</h1>
        <p>Task marked as done.</p>
        <p><strong>ID:</strong> {updated_task.id}</p>
        <p><strong>Title:</strong> {updated_task.title}</p>
        <p><strong>Status:</strong> {updated_task.status}</p>
        <p><strong>Created At:</strong> {updated_task.created_at}</p>
        """
        return create_html_response(content), 200
    return jsonify(updated_task.to_dict()), 200


@app.route('/health/alive', methods=['GET'])
def health_alive():
    return 'OK', 200


@app.route('/health/ready', methods=['GET'])
def health_ready():
    if task_service.connection and task_service.connection.is_connected():
        return 'OK', 200
    return 'Database connection not established', 500


def main():
    global task_service

    parser = argparse.ArgumentParser(description='Task Tracker Web Application')
    parser.add_argument('--host', type=str, default='127.0.0.1')
    parser.add_argument('--port', type=int, default=3000)
    parser.add_argument('--db-host', type=str, default='127.0.0.1')
    parser.add_argument('--db-user', type=str, default='app')
    parser.add_argument('--db-password', type=str, default='app')
    parser.add_argument('--db-name', type=str, default='task_tracker')

    args = parser.parse_args()

    db_config = {
        'host': args.db_host,
        'user': args.db_user,
        'password': args.db_password,
        'database': args.db_name
    }

    task_service = TaskService(db_config)

    try:
        app.run(host=args.host, port=args.port, debug=False)
    finally:
        task_service.disconnect()


if __name__ == '__main__':
    main()
