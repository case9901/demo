from flask import Flask, request, redirect, url_for, render_template_string, session, jsonify
import pymysql
import pyotp

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # You should set this to a random value

# Database configuration
db = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='san_magnolia',
    unix_socket='/var/run/mysqld/mysqld.sock'
)

@app.route('/')
def home():
    return '''
        <h1>Welcome to San Magnolia Military Portal</h1>
        <p>Bloody Regina needs to bypass the authentication to authorize missiles for the Undertaker's mission. Can you help?</p>
        <p>Hint: Use SQL injection to bypass the login and then use the secret for OTP.</p>
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
            session['secret'] = user[3]    # Store secret in session
            return redirect(url_for('otp'))
        else:
            return "Login failed"
    return render_template_string('''
        <h1>Login to San Magnolia Military Portal</h1>
        <form method="post">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username"><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
        <a href="/">Back to Home</a>
    ''')

@app.route('/get_secret')
def get_secret():
    if 'username' in session:
        secret = session.get('secret')
        return jsonify({'secret': secret})
    else:
        return jsonify({'error': 'Unauthorized'}), 401

@app.route('/otp', methods=['GET', 'POST'])
def otp():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        otp_token = request.form['otp_token']
        secret = session['secret']
        totp = pyotp.TOTP(secret)
        if totp.verify(otp_token):
            return redirect(url_for('flag'))
        else:
            return "Invalid OTP"

    return render_template_string('''
        <h1>2FA Authentication</h1>
        <p>Use your authenticator app to generate the OTP and authenticate.</p>
        <form method="post">
            <label for="otp_token">OTP Token:</label>
            <input type="text" id="otp_token" name="otp_token"><br>
            <input type="submit" value="Verify OTP">
        </form>
        <a href="/">Back to Home</a>

        <!-- Hidden field to store the secret -->
        <input type="hidden" id="hidden_secret">
        
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script>
            $(document).ready(function() {
                $.get("/get_secret", function(data) {
                    // Store the secret in a hidden input field
                    $('#hidden_secret').val(data.secret); 
                });
            });
        </script>
    ''')

@app.route('/flag')
def flag():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template_string('''
        <h1>Congratulations!</h1>
        <p>Here is your flag: CTF{bloody_regina_otp_success}</p>
        <a href="/">Back to Home</a>
    ''')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('secret', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)


