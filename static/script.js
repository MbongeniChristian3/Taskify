document.addEventListener('DOMContentLoaded', () => {
    // Initialize event listeners
    initTaskManager();
});

// Initialize task manager functionalities
function initTaskManager() {
    setupEditButtons();
    setupCheckboxes();
}

// Setup edit button functionality for each task
function setupEditButtons() {
    document.querySelectorAll('.edit-button').forEach(button => {
        button.addEventListener('click', handleEditButtonClick);
    });
}

// Handle edit button click event
function handleEditButtonClick(event) {
    const li = event.target.closest('li');
    const taskTitle = li.querySelector('.task-title');
    const editInput = li.querySelector('.edit-task-input');
    const taskId = li.dataset.taskId;
    toggleEditMode(taskTitle, editInput);
    setupEditInput(editInput, taskTitle, taskId);
}

// Setup checkbox functionality for each task
function setupCheckboxes() {
    document.querySelectorAll('.task-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', handleCheckboxChange);
    });
}

// Handle checkbox change event
function handleCheckboxChange(event) {
    const checkbox = event.target;
    checkbox.nextElementSibling.classList.toggle('completed', checkbox.checked);
}

// Toggle edit mode visibility
function toggleEditMode(taskTitle, editInput) {
    taskTitle.style.display = 'none';
    editInput.style.display = 'inline';
    editInput.focus();
}

// Toggle the display of elements
function toggleDisplay(taskTitle, editInput) {
    taskTitle.style.display = 'inline';
    editInput.style.display = 'none';
}

// Setup the input field for editing tasks
function setupEditInput(editInput, taskTitle, taskId) {

    editInput.addEventListener('keydown', async function(event) {
        if (event.key === 'Enter') {
          console.log("You clicked enter...........");
          await updateTaskTitle(taskId, editInput.value, taskTitle);
          toggleDisplay(taskTitle, editInput); 
          // Optionally, remove the event listener after use
          editInput.removeEventListener('keydown', this);
        }
      });
}

// Update task title in Database 
async function updateTaskTitle(taskId, newTitle, taskTitle) {
    const response = await sendRequest(`/edit/${taskId}`, 'POST', { title: newTitle });
    
    if (response.status === 'success') {
        taskTitle.textContent = newTitle;
    } else {
        alert(`Error: ${response.message}`);
    }
}

// Generic function to handle AJAX requests
async function sendRequest(url, method, data) {
    try {
        const response = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        // Check if the response is OK (status code 200-299)
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Error response:', errorText);
            return { status: 'error', message: `Server returned an error: ${response.status}` };
        }

        return await response.json();
    } catch (error) {
        console.error('Request failed', error);
        return { status: 'error', message: 'Request failed' };
    }
}
