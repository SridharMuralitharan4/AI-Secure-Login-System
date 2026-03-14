import subprocess
from flask import Flask, render_template_string
import os

app = Flask(__name__)

html_page = """
<!DOCTYPE html>
<html>
<head>
<title>AI Secure Login</title>
</head>

<body style="text-align:center;font-family:Arial">

<h1>AI Secure Login System</h1>
<h3>Face Recognition Authentication</h3>

<p>Click the button to start face login</p>

<form action="/login">
<button style="padding:10px 20px;font-size:18px;">
Start Face Login
</button>
</form>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html_page)

@app.route("/login")
def login():
    subprocess.Popen(
        ["cmd", "/c", "start", "python", "core\\face_recognition_system.py"],
        shell=True
    )
    return "<h2>Face recognition started. Check camera.</h2>"
if __name__ == "__main__":
    app.run(debug=True)