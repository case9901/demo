from flask import Flask, request, redirect, url_for, render_template_string, session
import pymysql

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # You should set this to a random value

# Database configuration
db = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='assassination_classroom',
    unix_socket='/var/run/mysqld/mysqld.sock'
)

@app.route('/')
def home():
    return '''
        <h1>Welcome to KoroSensei's Gradebook System</h1>
        <p>The students of Class 3-E are trying to sneak into KoroSensei's secret page. Can you help them?</p>
        <p>Hint: Sometimes, you need to think like a hacker to get what you want...</p>
        <a href="/login">Login</a>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = db.cursor()
        # Simulate SQL injection vulnerability
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        if user:
            session['username'] = user[1]  # Store username in session
            if user[1] == 'koroSensei':
                return redirect(url_for('secret'))
            else:
                return "Login successful, but you don't have access to the secret page!"
        else:
            return "Login failed"
    return render_template_string('''
        <h1>Login to KoroSensei's Gradebook System</h1>
        <form method="post">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username"><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
        <a href="/">Back to Home</a>
    ''')

@app.route('/secret')
def secret():
    if 'username' in session and session['username'] == 'koroSensei':
        return render_template_string('''
            <h1>Welcome, KoroSensei!</h1>
            <p>Here is your flag: CTF{korosensei_secret_flag}</p>
            <a href="/">Back to Home</a>
        ''')
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

