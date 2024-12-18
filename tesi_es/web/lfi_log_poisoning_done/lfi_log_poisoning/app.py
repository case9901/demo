from flask import Flask, request, render_template
import os
import random
import string

app = Flask(__name__)

# Generate a random log file name
log_filename = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16)) + '.log'
log_filepath = os.path.join('logs', log_filename)

# Open the log file and keep it open
log_file = open(log_filepath, 'a')
log_fd = log_file.fileno()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/include', methods=['GET'])
def include():
    file = request.args.get('file')
    cmd = request.args.get('cmd')
    if not file:
        return "File parameter is required"

    # Log the request details
    user_agent = request.headers.get('User-Agent')
    log_file.write(f"User-Agent: {user_agent}\n")
    log_file.flush()
    print(f"Logged User-Agent: {user_agent}")

    # Attempt to include the requested file
    try:
        print(f"Trying to open file: {file}")
        with open(file, 'r') as f:
            content = f.read()
        if cmd:
            content += f"\n<!-- Executing Command: {cmd} -->\n"
            content += os.popen(cmd).read()
        return f"<pre>{content}</pre>"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    os.makedirs('logs', exist_ok=True)
    os.makedirs('flags', exist_ok=True)
    with open('flags/flag.txt', 'w') as f:
        f.write('CTF{congratulations_you_found_the_flag}\n')

    print(f"Log file path: {log_filepath}")
    print(f"File descriptor for the log file: {log_fd}")

    app.run(host='0.0.0.0', port=5000)
