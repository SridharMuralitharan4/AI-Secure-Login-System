from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>AI Secure Login System</h1>

    <a href="/login">
        <button>Start Face Login</button>
    </a>

    <br><br>

    <form action="/register" method="post">
        <input type="text" name="username" placeholder="Enter Name" required>
        <button type="submit">Register New User</button>
    </form>

    <br><br>

    <a href="/logs">
        <button>View Logs</button>
    </a>
    """

@app.route("/login")
def login():
    subprocess.Popen(
        ["venv\\Scripts\\python", "core\\final_login_system.py"],
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    return """
    <h2 style="color:green;">AI Secure Login Started</h2>
    <p>⏳ Initializing AI system...</p>
    <p>Please look at the camera and follow instructions.</p>
    """

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]

    subprocess.Popen(
        ["venv\\Scripts\\python", "core\\register_user.py", username],
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    return f"""
    <h2>Registering {username}</h2>
    <p>📷 Camera will open. Please look at the camera.</p>
    """

@app.route("/logs")
def logs():
    try:
        with open("logs.txt", "r") as f:
            data = f.read()
    except:
        data = "No logs yet"

    return f"<h2>Login Logs</h2><pre>{data}</pre>"

if __name__ == "__main__":
    app.run(debug=True)