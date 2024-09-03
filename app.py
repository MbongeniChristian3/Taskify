import os
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ubt6qkl3u8huhp:pe5a1737aac7b96de6d02c3651c5ac36d7a53a6b14524d23efcfccc02fa37aaa4@c97r84s7psuajm.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/de07heu1vc4ufh'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Task model
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_title = request.form.get('content')
        if task_title:
            try:
                new_task = MyTask(title=task_title)
                db.session.add(new_task)
                db.session.commit()
            except Exception as e:
                print(f"Error adding task: {e}")
            return redirect(url_for('index'))
    
    tasks = MyTask.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/edit/<int:id>', methods=['POST'])
def edit_task(id):
    task = MyTask.query.get_or_404(id)
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'Request must be JSON'}), 400

    task_title = request.json.get('title')
    if task_title:
        try:
            task.title = task_title
            db.session.commit()
            return jsonify({'status': 'success'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    return jsonify({'status': 'error', 'message': 'Invalid title'})

@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
    except Exception as e:
        print(f"Error deleting task: {e}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
