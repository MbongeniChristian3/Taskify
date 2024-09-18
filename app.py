import os
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

"""create a Flask application instance"""
app = Flask(__name__)

"""configure the SQLAlchemy database URI, using an environment variable for the database URL if available, 
otherwise using a default PostgreSQL URL"""
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://taskify_itvz_user:OE3JJaiIS7MrFTibWD5eTo2twtqq7czj@dpg-cra5rvaj1k6c73bs5qag-a.oregon-postgres.render.com/taskify_itvz')

""" disable SQLAlchemy modification tracking to save resources"""
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

"""Initialize SQLAlchemy with the Flask app"""
db = SQLAlchemy(app)

"""define the Task model, representing a task entity in the database"""
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Task ID, the primary key
    title = db.Column(db.String(100), nullable=False)  # Task title, must not be empty

"""defines the main route for the app, which handles both GET and POST requests"""
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # If the request method is POST (form submission)
        task_title = request.form.get('content')  # Get the task content from the form
        if task_title:  # If the task title is not empty
            try:
                new_task = MyTask(title=task_title)  # Create a new task object
                db.session.add(new_task)  # Add the new task to the database session
                db.session.commit()  # Commit the session to save the task to the database
            except Exception as e:
                print(f"Error adding task: {e}")  # Handle any errors during task creation
            return redirect(url_for('index'))  # Redirect back to the index page after adding task
    
    # If the request method is GET, fetch all tasks from the database and render them in the template
    tasks = MyTask.query.all()  # Retrieve all tasks
    return render_template('index.html', tasks=tasks)  # Render the template with the list of tasks

""" define the route for editing a task, which accepts a task ID and expects a JSON body with a new title"""
@app.route('/edit/<int:id>', methods=['POST'])
def edit_task(id):
    task = MyTask.query.get_or_404(id)  # Fetch the task by ID, or return 404 if not found
    if not request.is_json:  # Check if the request content type is JSON
        return jsonify({'status': 'error', 'message': 'Request must be JSON'}), 400  # Return an error if not JSON
    task_title = request.json.get('title')  # Get the new title from the JSON body
    if task_title:  # If the title is not empty
        try:
            task.title = task_title  # Update the task's title
            db.session.commit()  # Commit the changes to the database
            return jsonify({'status': 'success'})  # Return a success response
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})  # Return an error message if something goes wrong
    return jsonify({'status': 'error', 'message': 'Invalid title'})  # Return an error if the title is invalid

"""defines the route for deleting a task, which accepts a task ID and removes the task from the database"""
@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    task = MyTask.query.get_or_404(id)  # Fetch the task by ID, or return 404 if not found
    try:
        db.session.delete(task)  # Delete the task from the session
        db.session.commit()  # Commit the deletion to the database
    except Exception as e:
        print(f"Error deleting task: {e}")  # Handle any errors during task deletion
    return redirect(url_for('index'))  # Redirect back to the index page after deletion

""" the entry point of the Flask application"""
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create all database tables if they don't exist yet
 