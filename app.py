import os
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ue8omuqg30a8su:p7358bafbae3ac44ba0a38e54fb318ed2978b09d990bc472d4910a82f8212684b@c9mq4861d16jlm.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d9i6kftff8b69o'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#postgresql://taskify_itvz_user:OE3JJaiIS7MrFTibWD5eTo2twtqq7czj@dpg-cra5rvaj1k6c73bs5qag-a.oregon-postgres.render.com/taskify_itvz
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
