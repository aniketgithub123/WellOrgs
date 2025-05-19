document.addEventListener("DOMContentLoaded", () => {
    loadUsers();
    loadProjects();

    // Add Project
    document.getElementById("addProjectBtn").addEventListener("click", () => {
        const name = document.getElementById("projectName").value.trim();
        const description = document.getElementById("projectDescription").value.trim();
        const errorDiv = document.getElementById("projectError");
        errorDiv.textContent = "";

        if (!name) {
            errorDiv.textContent = "Project name is required.";
            return;
        }

        fetch("/projects", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, description })
        })
        .then(response => response.json().then(data => ({ status: response.status, body: data })))
        .then(({ status, body }) => {
            if (status === 201) {
                alert("✅ Project added!");
                document.getElementById("projectName").value = "";
                document.getElementById("projectDescription").value = "";
                loadProjects();
            } else {
                errorDiv.textContent = body.error || "❌ Failed to add project.";
            }
        });
    });

    // Add User
    document.getElementById("addUserBtn").addEventListener("click", () => {
        const username = document.getElementById("username").value.trim();
        const errorDiv = document.getElementById("userError");
        errorDiv.textContent = "";

        if (!username) {
            errorDiv.textContent = "Username is required.";
            return;
        }

        fetch("/users", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username })
        })
        .then(response => response.json().then(data => ({ status: response.status, body: data })))
        .then(({ status, body }) => {
            if (status === 201) {
                alert("✅ User added!");
                document.getElementById("username").value = "";
                loadUsers();
            } else {
                errorDiv.textContent = body.error || "❌ Failed to add user.";
            }
        });
    });

    // Add Task
    document.getElementById("addTaskBtn").addEventListener("click", () => {
        const projectId = document.getElementById("projectDropdown").value;
        const title = document.getElementById("taskTitle").value.trim();
        const status = document.getElementById("taskStatus").value;
        const assignedUserId = document.getElementById("userDropdown").value;
        const errorDiv = document.getElementById("taskError");
        errorDiv.textContent = "";

        if (!projectId) {
            errorDiv.textContent = "Please select a project.";
            return;
        }
        if (!title) {
            errorDiv.textContent = "Task title is required.";
            return;
        }

        fetch(`/projects/${projectId}/tasks`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, status, assigned_user_id: assignedUserId || null })
        })
        .then(response => response.json().then(data => ({ status: response.status, body: data })))
        .then(({ status, body }) => {
            if (status === 201) {
                alert("✅ Task added!");
                document.getElementById("taskTitle").value = "";
                loadTasks(projectId);
            } else {
                errorDiv.textContent = body.error || "❌ Failed to add task.";
            }
        });
    });

    // Change Project - Load Tasks
    document.getElementById("projectDropdown").addEventListener("change", function () {
        const projectId = this.value;
        loadTasks(projectId);
    });
});

// Load Users
function loadUsers() {
    fetch("/users")
        .then(response => response.json())
        .then(users => {
            const userDropdown = document.getElementById("userDropdown");
            userDropdown.innerHTML = '<option value="">Unassigned</option>';
            users.forEach(user => {
                const option = document.createElement("option");
                option.value = user.id;
                option.textContent = user.username;
                userDropdown.appendChild(option);
            });

            const userList = document.getElementById("userList");
            if (userList) {
                userList.innerHTML = '';
                users.forEach(user => {
                    const li = document.createElement("li");
                    li.textContent = user.username;
                    userList.appendChild(li);
                });
            }
        });
}

// Load Projects
function loadProjects() {
    fetch("/projects")
        .then(response => response.json())
        .then(projects => {
            const projectDropdown = document.getElementById("projectDropdown");
            projectDropdown.innerHTML = '<option value="">Select a project</option>';
            projects.forEach(project => {
                const option = document.createElement("option");
                option.value = project.id;
                option.textContent = project.name;
                projectDropdown.appendChild(option);
            });
            if (projects.length > 0) {
                loadTasks(projects[0].id);
            }
        });
}

// Load Tasks for Selected Project
function loadTasks(projectId) {
    if (!projectId) return;
    fetch(`/projects/${projectId}/tasks`)
        .then(response => response.json())
        .then(tasks => {
            renderKanban(tasks);
        });
}

// Render Kanban Board
function renderKanban(tasks) {
    let kanbanContainer = document.getElementById("kanban");
    if (!kanbanContainer) {
        kanbanContainer = document.createElement("div");
        kanbanContainer.id = "kanban";
        kanbanContainer.className = "kanban";
        document.body.appendChild(kanbanContainer);
    }
    kanbanContainer.innerHTML = "";

    const columns = {
        todo: createColumn("To Do"),
        inprogress: createColumn("In Progress"),
        done: createColumn("Done")
    };

    tasks.forEach(task => {
        const taskDiv = document.createElement("div");
        taskDiv.className = "task";
        taskDiv.draggable = true;
        taskDiv.dataset.taskId = task.id;
        taskDiv.dataset.title = task.title;
        taskDiv.textContent = `${task.title} ${task.assigned_user ? `(${task.assigned_user.username})` : ''}`;

        taskDiv.addEventListener("dragstart", dragStart);
        taskDiv.addEventListener("dragend", dragEnd);

        columns[task.status]?.appendChild(taskDiv);
    });

    Object.values(columns).forEach(col => {
        col.addEventListener("dragover", dragOver);
        col.addEventListener("drop", drop);
        kanbanContainer.appendChild(col);
    });
}

function createColumn(title) {
    const col = document.createElement("div");
    col.className = "column";
    col.innerHTML = `<h3>${title}</h3>`;
    return col;
}

// Drag and Drop handlers
let draggedTask = null;

function dragStart(e) {
    draggedTask = this;
    e.dataTransfer.effectAllowed = "move";
    e.dataTransfer.setData("text/plain", this.dataset.taskId);
    this.style.opacity = "0.5";
}

function dragEnd(e) {
    this.style.opacity = "1";
    draggedTask = null;
}

function dragOver(e) {
    e.preventDefault();
}

function drop(e) {
    e.preventDefault();
    const newStatus = this.querySelector("h3").textContent.toLowerCase().replace(/\s/g, '');
    const taskId = e.dataTransfer.getData("text/plain");
    const taskTitle = draggedTask?.dataset?.title || "";

    fetch(`/tasks/${taskId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: newStatus, title: taskTitle })
    })
    .then(response => {
        if (response.ok) {
            loadTasks(document.getElementById("projectDropdown").value);
        } else {
            alert("❌ Failed to update task status.");
        }
    });
}
