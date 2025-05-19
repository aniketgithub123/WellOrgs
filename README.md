# 🛠️ Project Management Tool

A simple web-based project management tool built with **Flask**, **MySQL**, and **Vanilla JS (HTML/CSS/JS)**.

---

## 📦 Project Deliverables

- ✅ **GitHub Repository** with clean and well-documented code.
- ✅ `README.md` with setup and deployment instructions.
- ✅ **Working Demo** (see below).
- ✅ **Documentation** of API endpoints and testing steps.

---

## 🚀 Working Demo

🌐 **Live App:** [https://your-live-link.com](https://wellorgs-flask-app.onrender.com)  
*(Replace with your deployed link)*

---

## 🖥️ Setup Instructions

### 📌 Backend (Python Flask + MySQL)

1. **Create MySQL database and tables** using the schema below.
2. **Update** `app.py` with your MySQL credentials.
3. **Install Python packages**:
   ```bash
   pip install flask flask-cors mysql-connector-python
   ```
4. **Run the Flask server**:
   ```bash
   python app.py
   ```

### 📌 Frontend

Just open the `index.html` file in your browser.

---

## 🗃️ MySQL Schema

```sql
CREATE DATABASE project_management;

USE project_management;

CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT,
    title VARCHAR(255) NOT NULL,
    status ENUM('todo', 'inprogress', 'done') DEFAULT 'todo',
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);
```

---

## 🌐 API Endpoints

### 📁 Projects

| Method | Endpoint                   | Description              |
|--------|----------------------------|--------------------------|
| GET    | `/projects`                | Get all projects         |
| POST   | `/projects`                | Create a new project     |
| PUT    | `/projects/<project_id>`   | Update a project         |
| DELETE | `/projects/<project_id>`   | Delete a project         |

**Request Body for POST/PUT:**
```json
{
  "name": "Project Alpha",
  "description": "Alpha description"
}
```

---

### ✅ Tasks

| Method | Endpoint                                 | Description                     |
|--------|------------------------------------------|---------------------------------|
| GET    | `/projects/<project_id>/tasks`           | Get all tasks for a project     |
| POST   | `/projects/<project_id>/tasks`           | Create a task in a project      |
| PUT    | `/tasks/<task_id>`                       | Update a task                   |
| DELETE | `/tasks/<task_id>`                       | Delete a task                   |

**Request Body for POST/PUT:**
```json
{
  "title": "Fix bug",
  "status": "inprogress"
}
```

---

## 🧪 How to Test the App

### ✅ Manual Testing
- Use [Postman](https://www.postman.com/) or [Insomnia](https://insomnia.rest/) to test API endpoints.
- Or, test via browser for `GET` endpoints (e.g., [http://localhost:5000/projects](http://localhost:5000/projects)).

### ✅ Frontend Testing
- Open `index.html` in a browser.
- Add, update, and delete projects/tasks.
- Observe live API integration via browser developer tools.

---

## 📁 Folder Structure

```
wellorgs/
│
├── app.py              # Flask backend
├── index.html          # Frontend HTML UI
├── script.js           # JavaScript logic
├── style.css           # CSS styling
├── readme.md           # This file
└── venv/               # Python virtual environment (ignored in Git)
```

---

## 🔗 License

MIT License — free to use, modify, and share.

---

> 👨‍💻 Built with ❤️ by [Aniket Kadam]. Replace this section with your details if needed.
