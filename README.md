# Project Management Tool

## Setup Instructions

### Backend (Python Flask + MySQL)
1. Create MySQL DB using the schema below.
2. Update `app.py` with your MySQL credentials.
3. Install Python packages:
    ```
    pip install flask flask-cors mysql-connector-python
    ```
4. Run the backend:
    ```
    python app.py
    ```

### Frontend
Open `index.html` in a browser.

## MySQL Schema

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