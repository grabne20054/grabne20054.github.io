from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
DATABASE = 'database.sqlite'

def connect_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def new_user(username, password):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE username = '{username}'")
    if cur.fetchone() == None:
        return 1
    cur.execute("INSERT INTO users(username, password) VALUES('{0}', '{1}');".format(username, password))
    conn.commit()

def get_user(username):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cur.fetchone()
    conn.close()
    return user

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user(username)

        if user is not None and user['password'] == password:
            return redirect(url_for('dashboard'))
        else:
            error = 'Incorrect username or password.'

    return render_template('login.html', error=error)

@app.route('/signin.html' , methods=['GET', 'POST'])
def signin():
    error = None
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        new = new_user(username, password)
        if new == 1:
            error = "jo passt du depp"
        else:
            return redirect(url_for('login'))
    return render_template("signin.html", error=error)

@app.route('/dashboard.html')
def dashboard():
    return render_template("dashboard.html")

@app.route('/about_us.html')
def about_us():
    return render_template("about_us.html")

if __name__ == '__main__':
    app.run(debug=True)
