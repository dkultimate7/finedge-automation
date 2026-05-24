from flask import Flask
import threading
import main

app = Flask(__name__)

@app.route('/')
def home():
    return "Finedge Automation is running!"

@app.route('/run')
def run_script():
    # Run the script logic in a separate thread so it doesn't block the web server
    thread = threading.Thread(target=main.main)
    thread.start()
    return "Automation script started in the background!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
