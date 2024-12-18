from flask import Flask, request, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ping', methods=['POST'])
def ping():
    hostname = request.form.get('hostname')
    if not hostname:
        return "Hostname is required"

    # Input sanitization
    forbidden_patterns = [' ', 'cat', 'flag', '|', '&', '`', '>', '<', '&&', '||']
    for pattern in forbidden_patterns:
        if pattern in hostname:
            print("Invalid pattern found:"+pattern)
            return "Invalid input"

    # Execute command
    try:
        command = f"ping -c 1 {hostname}"
        result = os.popen(command).read()
        return f"<pre>{result}</pre>"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
