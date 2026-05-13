from flask import Flask, render_template, request, session
import sqlite3

app = Flask(__name__)

app.secret_key = "taskmanager"



@app.route('/')
def home():
    return render_template('home.html')



@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password)
        )

        conn.commit()
        conn.close()

        return '''
        <script>
            alert("Registration Successful");
            window.location.href="/login";
        </script>
        '''

    return render_template('home.html')



@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            session['username'] = user[1]

            return '''
            <script>
                alert("Login Successful");
                window.location.href="/create-task";
            </script>
            '''

        else:

            return '''
            <script>
                alert("Invalid Email or Password");
                window.location.href="/login";
            </script>
            '''

    return render_template('login.html')



@app.route('/create-task', methods=['GET', 'POST'])
def create_task():

    if request.method == 'POST':

        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        assigned_to = request.form['assigned_to']

        assigned_by = session['username']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            '''
            INSERT INTO tasks
            (title, description, priority, status, assigned_to, assigned_by)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (
                title,
                description,
                priority,
                'Pending',
                assigned_to,
                assigned_by
            )
        )

        conn.commit()
        conn.close()

        return '''
        <script>
            alert("Task Created Successfully");
            window.location.href="/dashboard";
        </script>
        '''

    return render_template('create_task.html')



@app.route('/dashboard')
def dashboard():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")

    tasks = cursor.fetchall()

    conn.close()

    return render_template('dashboard.html', tasks=tasks)


@app.route('/update-status/<int:id>', methods=['POST'])
def update_status(id):

    status = request.form['status']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET status=? WHERE id=?",
        (status, id)
    )

    conn.commit()
    conn.close()

    return '''
    <script>
        alert("Task Status Updated Successfully");
        window.location.href="/dashboard";
    </script>
    '''



@app.route('/delete-task/<int:id>', methods=['POST'])
def delete_task(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return '''
    <script>
        alert("Task Deleted Successfully");
        window.location.href="/dashboard";
    </script>
    '''


if __name__ == '__main__':
    app.run(debug=True)