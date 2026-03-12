from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>AI Secure Login System</h1><p>Face Authentication Loading...</p>"

app.run(debug=True)