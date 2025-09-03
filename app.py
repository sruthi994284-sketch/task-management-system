let tasks = [];

// Function to render tasks to the UI
function renderTasks() {
    const taskListContainer = document.getElementById('taskListContainer');
    taskListContainer.innerHTML = ''; // Clear current tasks

    // If tasks are present in the array, display them
    tasks.forEach((task, index) => {
        const taskElement = document.createElement('div');
        taskElement.classList.add('task-item');

        // Ensure that task title is properly rendered
        taskElement.innerHTML = `
      <p><strong>${task.title}</strong></p> <!-- Display task title here -->
      <p>${task.description}</p>
      <p class="task-status">Status: ${task.status}</p>
      <button onclick="deleteTask(${index})">Delete</button>
    `;

        taskListContainer.appendChild(taskElement);
    });
}

// Function to add a new task
function addTask() {
    const title = document.getElementById('taskTitle').value;
    const description = document.getElementById('taskDescription').value;
    const status = document.getElementById('taskStatus').value;

    // Ensure that title is not empty
    if (title.trim() === "") {
        alert("Please provide a task title!");
        return;
    }

    // Create a new task object
    const newTask = {
        title,
        description,
        status
    };

    // Add the new task to the tasks array
    tasks.push(newTask);

    // Log the tasks array to check if the task was properly added
    console.log("Tasks after adding new task:", tasks);

    // Clear input fields and re-render tasks
    document.getElementById('taskTitle').value = '';
    document.getElementById('taskDescription').value = '';
    document.getElementById('taskStatus').value = 'Pending';
    renderTasks();
}

// Function to delete a task
function deleteTask(index) {
    tasks.splice(index, 1); // Remove the task from the array
    renderTasks(); // Re-render the task list
}

// Call renderTasks on page load to display tasks if any exist
document.addEventListener('DOMContentLoaded', renderTasks);
