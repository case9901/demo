from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)

# Percorso del file di log
LOG_FILE = '/tmp/access.log'
FLAG_FILE = 'flag.txt'

@app.route('/')
def index():
    file = request.args.get('file')
    if file:
        try:
            # Per evitare LFI, limitiamo il file alla directory corrente
            if not os.path.basename(file) in ['log.txt', FLAG_FILE]:
                return "Accesso non autorizzato.", 403
            
            with open(file, 'r') as f:
                content = f.read()
            
            return f"<pre>{content}</pre>"
        except FileNotFoundError:
            return "File non trovato.", 404
    return "Nessun file specificato."

@app.route('/log')
def log():
    cmd = request.args.get('cmd')
    if cmd:
        # Scrivi il comando nel file di log
        with open(LOG_FILE, 'a') as f:
            f.write(cmd + "\n")
        return f"Comando inserito nel log: {cmd}"
    return "Nessun comando specificato."

@app.route('/flag')
def flag():
    return send_from_directory(directory='.', filename=FLAG_FILE)

if __name__ == "__main__":
    app.run(debug=True)
