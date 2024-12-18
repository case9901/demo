from flask import Flask, send_from_directory, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <h1>Welcome to SERN's Database</h1>
        <p>SERN has hidden sensitive data somewhere on this website. Can you find it?</p>
        <p>Hint: Sometimes, secrets are hidden in plain sight...</p>
        <ul>
            <li><a href="/about">About SERN</a></li>
            <li><a href="/contact">Contact Us</a></li>
            <li><a href="/secret">Secret Research</a></li>
        </ul>
    '''

@app.route('/about')
def about():
    return '''
        <h1>About SERN</h1>
        <p>SERN is a powerful organization known for its clandestine research in time travel.</p>
        <p><!-- False Flag: CTF{steins_gate_fake_flag_1} --></p>
        <a href="/">Back to Home</a>
    '''

@app.route('/contact')
def contact():
    return '''
        <h1>Contact Us</h1>
        <p>If you have any information about the time travel research, please contact us immediately.</p>
        <p><!-- Note: The real flag is definitely not here! --></p>
        <a href="/">Back to Home</a>
    '''

@app.route('/secret')
def secret():
    return '''
        <h1>Secret Research</h1>
        <p>Access to these documents is restricted to authorized personnel only.</p>
        <p><!-- Another False Flag: CTF{steins_gate_fake_flag_2} --></p>
        <p><!-- Hint: try to search for some static file --></p>

        <a href="/">Back to Home</a>
    '''

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

@app.route('/flag.txt')
def falseflag():
    return send_from_directory('static', 'flag.txt')

if __name__ == '__main__':
    app.run(debug=True)

