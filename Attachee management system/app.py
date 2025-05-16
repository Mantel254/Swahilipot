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
    "Engineering": [Attachee("Elizabeth Ng'ang'a", "Engineering"), Attachee("Avril Diamond Wavinya", "Engineering")],
    "Tech Programs": [Attachee("Rinnah Achieng Oyugi", "Tech Programs")],
    "Radio Support": [Attachee("Dorice Adhiambo Obonyo", "Radio Support")],
    "Hub Support": [Attachee("Mwamuye Joseph", "Hub Support")]
}

# === Routes ===
@app.route('/index')
def index():
    return render_template('index.html', attachees=attachees)

@app.route('/', methods=['GET', 'POST'])
def add_attachee():
    divisions = attachees.keys()

    if request.method == 'POST':
        name = request.form['name'].strip()
        division = request.form['division']

        # Check if attachee already exists
        existing_attachee = next(
            (a for a in attachees[division] if a.name.lower() == name.lower()), None)

        if existing_attachee:
            # Redirect to their portal if they exist
            return redirect(url_for('attachee_portal', division=division, name=name))
        else:
            # Add new attachee and redirect to portal
            new_attachee = Attachee(name, division)
            attachees[division].append(new_attachee)
            return redirect(url_for('attachee_portal', division=division, name=name))

    return render_template('attachee.html', divisions=divisions)


@app.route('/attachee/<division>/<name>')
def attachee_detail(division, name):
    attachee = next((a for a in attachees[division] if a.name == name), None)
    return render_template('attachee_list.html', attachee=attachee)

@app.route('/attachee_portal/<division>/<name>', methods=['GET', 'POST'])
def attachee_portal(division, name):
    attachee = next((a for a in attachees[division] if a.name.lower() == name.lower()), None)
    message = None

    if not attachee:
        return f"Attachee '{name}' not found in {division}", 404

    if request.method == 'POST':
        task_index = int(request.form['task_index'])
        feedback = request.form['feedback']
        attachee.tasks[task_index].feedback = feedback
        message = "Feedback submitted successfully."

    return render_template('attachee_portal.html', attachee=attachee, message=message)


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
