from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# === OOP Class Definitions ===
class Attachee:
    def __init__(self, name, division):
        self.name = name
        self.division = division
        self.tasks = []

    def assign_task(self, task):
        self.tasks.append(task)

class Task:
    def __init__(self, title, feedback="", score=None):
        self.title = title
        self.feedback = feedback
        self.score = score

# === "Database" ===
attachees = {
    "ICT": [Attachee("Alice", "ICT"), Attachee("Bob", "ICT")],
    "HR": [Attachee("Eve", "HR")],
    "Finance": [Attachee("John", "Finance")]
}

# === Routes ===
@app.route('/')
def index():
    return render_template('index.html', attachees=attachees)

@app.route('/attachee/<division>/<name>')
def attachee_detail(division, name):
    attachee = next((a for a in attachees[division] if a.name == name), None)
    return render_template('attachee_list.html', attachee=attachee)

@app.route('/assign/<division>/<name>', methods=['GET', 'POST'])
def assign_task(division, name):
    attachee = next((a for a in attachees[division] if a.name == name), None)
    if request.method == 'POST':
        title = request.form['title']
        feedback = request.form['feedback']
        score = request.form['score']
        task = Task(title, feedback, int(score))
        attachee.assign_task(task)
        return redirect(url_for('attachee_detail', division=division, name=name))
    return render_template('assign_task.html', attachee=attachee)

if __name__ == '__main__':
    app.run(debug=True)
