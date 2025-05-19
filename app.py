from flask import Flask, request, jsonify, send_from_directory, g
import mysql.connector
from flask_cors import CORS
import sys

app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)

# --- Database config ---
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "aniket123",
    "database": "project_management",
    "port": 3306
}

# --- Helper to get DB connection and cursor per request ---
def get_db():
    if 'db_conn' not in g:
        try:
            g.db_conn = mysql.connector.connect(**DB_CONFIG)
            g.db_cursor = g.db_conn.cursor(dictionary=True)
            print("✅ Connected to MySQL database.")
        except mysql.connector.Error as err:
            print(f"❌ Failed to connect to MySQL: {err}")
            sys.exit(1)
    return g.db_conn, g.db_cursor

@app.teardown_appcontext
def close_db(error):
    db_cursor = g.pop('db_cursor', None)
    db_conn = g.pop('db_conn', None)
    if db_cursor is not None:
        db_cursor.close()
    if db_conn is not None and db_conn.is_connected():
        db_conn.close()
        print("❎ MySQL connection closed.")

# --- Helper Functions ---

def project_exists(name):
    conn, cursor = get_db()
    cursor.execute("SELECT id FROM projects WHERE name = %s", (name,))
    return cursor.fetchone() is not None

def user_exists(user_id):
    conn, cursor = get_db()
    cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
    return cursor.fetchone() is not None

def task_exists(task_id):
    conn, cursor = get_db()
    cursor.execute("SELECT id FROM tasks WHERE id = %s", (task_id,))
    return cursor.fetchone() is not None

# --- Routes ---

@app.route("/")
def home():
    return send_from_directory('.', 'index.html')

# --- Users ---

@app.route("/users", methods=["GET", "POST"])
def users():
    conn, cursor = get_db()
    if request.method == "GET":
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return jsonify(users)
    else:
        data = request.json
        username = data.get("username")
        if not username:
            return jsonify({"error": "Username is required"}), 400
        try:
            cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
            conn.commit()
            return jsonify({"message": "User created"}), 201
        except mysql.connector.IntegrityError:
            # Instead of returning error, add silently (if you want) or ignore duplicate errors:
            return jsonify({"message": "User already exists"}), 200

# --- Projects ---

@app.route("/projects", methods=["GET", "POST"])
def projects():
    conn, cursor = get_db()
    if request.method == "GET":
        cursor.execute("SELECT * FROM projects")
        projects = cursor.fetchall()
        return jsonify(projects)
    else:
        data = request.json
        name = data.get("name")
        description = data.get("description", "")
        if not name:
            return jsonify({"error": "Project name is required"}), 400
        # Ignore duplicate error: just insert anyway or ignore on conflict (MySQL doesn't have native 'ON CONFLICT DO NOTHING')
        # So, do a try-except:
        try:
            cursor.execute("INSERT INTO projects (name, description) VALUES (%s, %s)", (name, description))
            conn.commit()
            return jsonify({"message": "Project created"}), 201
        except mysql.connector.IntegrityError:
            return jsonify({"message": "Project already exists"}), 200

@app.route("/projects/<int:project_id>", methods=["PUT", "DELETE"])
def modify_project(project_id):
    conn, cursor = get_db()
    if request.method == "PUT":
        data = request.json
        name = data.get("name")
        description = data.get("description", "")
        if not name:
            return jsonify({"error": "Project name is required"}), 400
        cursor.execute("SELECT id FROM projects WHERE name = %s AND id != %s", (name, project_id))
        if cursor.fetchone():
            return jsonify({"error": "Project name already exists"}), 409
        cursor.execute("UPDATE projects SET name=%s, description=%s WHERE id=%s", (name, description, project_id))
        conn.commit()
        return jsonify({"message": "Project updated"})
    else:
        cursor.execute("DELETE FROM projects WHERE id=%s", (project_id,))
        conn.commit()
        return jsonify({"message": "Project deleted"})

# --- Tasks ---

@app.route("/projects/<int:project_id>/tasks", methods=["GET", "POST"])
def project_tasks(project_id):
    conn, cursor = get_db()
    if request.method == "GET":
        cursor.execute("""
            SELECT t.*, u.username as assigned_user 
            FROM tasks t 
            LEFT JOIN users u ON t.assigned_user_id = u.id 
            WHERE t.project_id=%s
        """, (project_id,))
        tasks = cursor.fetchall()
        return jsonify(tasks)
    else:
        data = request.json
        title = data.get("title")
        status = data.get("status", "todo")
        assigned_user_id = data.get("assigned_user_id")

        if not title:
            return jsonify({"error": "Task title is required"}), 400
        if status not in ['todo', 'inprogress', 'done']:
            return jsonify({"error": "Invalid status"}), 400
        if assigned_user_id is not None and not user_exists(assigned_user_id):
            return jsonify({"error": "Assigned user does not exist"}), 400

        cursor.execute("""
            INSERT INTO tasks (project_id, title, status, assigned_user_id) 
            VALUES (%s, %s, %s, %s)
        """, (project_id, title, status, assigned_user_id))
        conn.commit()
        return jsonify({"message": "Task created"}), 201

@app.route("/tasks/<int:task_id>", methods=["PUT", "DELETE"])
def task_operations(task_id):
    conn, cursor = get_db()
    if not task_exists(task_id):
        return jsonify({"error": "Task not found"}), 404

    if request.method == "PUT":
        data = request.json
        title = data.get("title")
        status = data.get("status")
        assigned_user_id = data.get("assigned_user_id")

        if not title or not status:
            return jsonify({"error": "Title and status are required"}), 400
        if status not in ['todo', 'inprogress', 'done']:
            return jsonify({"error": "Invalid status"}), 400
        if assigned_user_id is not None and not user_exists(assigned_user_id):
            return jsonify({"error": "Assigned user does not exist"}), 400

        cursor.execute("""
            UPDATE tasks SET title=%s, status=%s, assigned_user_id=%s WHERE id=%s
        """, (title, status, assigned_user_id, task_id))
        conn.commit()
        return jsonify({"message": "Task updated"})
    else:
        cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
        conn.commit()
        return jsonify({"message": "Task deleted"})

if __name__ == "__main__":
    app.run(debug=True)
