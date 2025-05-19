# 🛠️ Project Management Tool

A simple full-stack web app for managing projects, tasks, and users using **Flask**, **MySQL**, and basic HTML frontend.

---

## 🚀 Deliverables

- ✅ **GitHub Repository**: Clean and well-documented code.
- ✅ **README.md** with:
  - Local setup instructions
  - Deployment guide
  - API documentation
- ✅ **Working Demo**: [Public demo link here]([https://your-demo-url.com](https://wellorgs-flask-app.onrender.com))

---

## 📦 Features

- Add, edit, delete **projects**
- Create and manage **tasks** per project
- Assign tasks to **users**
- RESTful API for frontend/backend integration

---

## 🏗️ Setup Instructions

### 🔧 Backend (Python Flask + MySQL)

1. ✅ **Create MySQL database** using the schema below.
2. 🔑 Update MySQL credentials in `app.py` under `DB_CONFIG`.
3. 📦 Install required Python packages:
    ```bash
    pip install flask flask-cors mysql-connector-python
    ```
4. ▶️ **Run the Flask server**:
    ```bash
    python app.py
    ```

> Default runs on `http://127.0.0.1:5000/`

---

### 🎨 Frontend

Just open `index.html` in your browser manually or use any static file server to host it.

---

## 🗃️ MySQL Schema

```sql
CREATE DATABASE project_management;

USE project_management;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT,
    title VARCHAR(255) NOT NULL,
    status ENUM('todo', 'inprogress', 'done') DEFAULT 'todo',
    assigned_user_id INT,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_user_id) REFERENCES users(id) ON DELETE SET NULL
);
