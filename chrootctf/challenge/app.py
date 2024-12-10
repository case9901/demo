from flask import Flask, request, render_template
import os
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
    #forbidden_patterns = [' ', 'cat', 'flag', '|', '&', '`', '>', '<', '&&', '||']
    #for pattern in forbidden_patterns:
        #if pattern in hostname:
            #print("Invalid pattern found:" + pattern)
            #return "Invalid input"

    # Execute command inside chroot
    try:
        command = f"ping -c 1 {hostname}"
        chroot_command = f" chroot /chroot/home/user/chroot /bin/bash -c '{command}'"  # Aggiunto sudo per ottenere i permessi di root
        result = subprocess.check_output(chroot_command, shell=True, stderr=subprocess.STDOUT)
        return f"<pre>{result.decode()}</pre>"
    except subprocess.CalledProcessError as e:
        return f"Error: {str(e.output.decode())}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

