// Wait for the DOM to be fully loaded before executing any code
document.addEventListener('DOMContentLoaded', () => {
    // Initialize event listeners for task manager functionalities
    initTaskManager();
});

// Function to initialize all task manager-related functionalities
function initTaskManager() {
    setupEditButtons();  // Set up the functionality for task edit buttons
    setupCheckboxes();   // Set up the functionality for task checkboxes
}

// Function to set up event listeners on all edit buttons
function setupEditButtons() {
    // For each edit button found, attach a click event listener
    document.querySelectorAll('.edit-button').forEach(button => {
        button.addEventListener('click', handleEditButtonClick);  // Handle edit button clicks
    });
}

// Function to handle the event when the edit button is clicked
function handleEditButtonClick(event) {
    // Get the list item (task) that the clicked edit button belongs to
    const li = event.target.closest('li');
    // Find the elements for the task title and input field for editing the task
    const taskTitle = li.querySelector('.task-title');
    const editInput = li.querySelector('.edit-task-input');
    const taskId = li.dataset.taskId;  // Retrieve the task ID from the dataset

    // Toggle the visibility of the task title and edit input
    toggleEditMode(taskTitle, editInput);
    // Set up the functionality for editing the task in the input field
    setupEditInput(editInput, taskTitle, taskId);
}
// Function to set up event listeners on all task checkboxes
function setupCheckboxes() {
    // For each checkbox found, attach a change event listener
    document.querySelectorAll('.task-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', handleCheckboxChange);  // Handle checkbox changes
    });
}

// Function to handle the event when a checkbox's state is changed
function handleCheckboxChange(event) {
    const checkbox = event.target;
    // Toggle the "completed" class for the task label based on checkbox state
    checkbox.nextElementSibling.classList.toggle('completed', checkbox.checked);
}

// Function to toggle the visibility between task title and edit input
function toggleEditMode(taskTitle, editInput) {
    taskTitle.style.display = 'none';  // Hide the task title
    editInput.style.display = 'inline';  // Show the input field for editing
    editInput.focus();  // Automatically focus the input field for editing
}

// Function to toggle the display of elements back after editing
function toggleDisplay(taskTitle, editInput) {
    taskTitle.style.display = 'inline';  // Show the task title
    editInput.style.display = 'none';    // Hide the input field
}

// Function to set up the input field for editing tasks, listening for 'Enter' key
function setupEditInput(editInput, taskTitle, taskId) {
    // Listen for the 'keydown' event in the input field
    editInput.addEventListener('keydown', async function(event) {
        if (event.key === 'Enter') {  // If the 'Enter' key is pressed
            console.log("You clicked enter...........");
            // Update the task title by sending the new title to the server
            await updateTaskTitle(taskId, editInput.value, taskTitle);
            // Toggle the display of task title and edit input back after updating
            toggleDisplay(taskTitle, editInput);
            // Optionally remove the event listener after use (to avoid memory leaks)
            editInput.removeEventListener('keydown', this);
        }
    });
}

// Function to update the task title in the database via an AJAX request
async function updateTaskTitle(taskId, newTitle, taskTitle) {
    // Send a POST request to update the task title on the server
    const response = await sendRequest(`/edit/${taskId}`, 'POST', { title: newTitle });
    
    // If the request is successful, update the task title in the UI
    if (response.status === 'success') {
        taskTitle.textContent = newTitle;
    } else {
        alert(`Error: ${response.message}`);  // Alert the user if there's an error
    }
}

// Generic function to handle AJAX requests
async function sendRequest(url, method, data) {
    try {
        // Make an AJAX request using the Fetch API
        const response = await fetch(url, {
            method,  // HTTP method (GET, POST, etc.)
            headers: { 'Content-Type': 'application/json' },  // Set content type to JSON
            body: JSON.stringify(data)  // Send the data as a JSON string
        });

        // Check if the response status is OK (status code 200-299)
        if (!response.ok) {
            const errorText = await response.text();  // Read the error message
            console.error('Error response:', errorText);
            return { status: 'error', message: `Server returned an error: ${response.status}` };
        }

        // Return the JSON response if the request is successful
        return await response.json();
    } catch (error) {
        console.error('Request failed', error);  // Log any network errors
        return { status: 'error', message: 'Request failed' };
    }
}


