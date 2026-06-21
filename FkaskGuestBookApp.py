from flask import Flask, request
import sqlite3

app = Flask(__name__)
DB = "guestbook.db"

def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS guests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_guests():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT name, message FROM guests ORDER BY id DESC")
    guests = cursor.fetchall()
    conn.close()
    return guests

def add_guest(name, message):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO guests (name, message) VALUES (?, ?)",
    (name, message))
    conn.commit()
    conn.close()

def build_page(status=""):
    guests = get_guests()
    entries = ""
    if len(guests) == 0:
        entries = "<p style='color:#aaa'>No entries yet. Be the first!</p>"
    else:
        for guest in guests:
            entries += """
            <div style='background:#f0f0f0;padding:15px;
            border-radius:8px;margin-top:10px;text-align:left'>
            <b style='color:#2980b9'>""" + guest[0] + """</b>
            <p style='color:#555;margin:5px 0'>""" + guest[1] + """</p>
            </div>
            """
    return """
<!DOCTYPE html>
<html>
<head>
<title>Guest Book</title>
<style>
body {
background-color: #2c3e50;
font-family: Arial;
display: flex;
justify-content: center;
padding: 40px 20px;
}
.card {
background-color: #ffffff;
max-width: 450px;
width: 100%;
padding: 30px;
border-radius: 15px;
}
h1 { color: #2c3e50; text-align:center; }
h2 { color: #2980b9; }
input, textarea {
padding: 12px;
font-size: 16px;
border: 2px solid #2980b9;
border-radius: 8px;
width: 90%;
margin-top: 10px;
}
.button {
background-color: #2980b9;
color: white;
border: none;
padding: 12px;
font-size: 16px;
border-radius: 8px;
width: 95%;
margin-top: 15px;
cursor: pointer;
}
.status { color: green; font-size: 16px; text-align:center; }
</style>
</head>
<body>
<div class="card">
<h1>Guest Book</h1>
<p style='text-align:center;color:#555'>Leave a message!</p>
<hr>
<h2>Sign the Book</h2>
<form method="POST" action="/sign">
<input type="text" name="name"
placeholder="Your name" required>
<textarea name="message"
placeholder="Your message..."
rows="3"
style="resize:none;"></textarea>
<button class="button"
type="submit">Sign Guest Book</button>
</form>
<p class="status">""" + status + """</p>
<hr>
<h2>All Entries</h2>
""" + entries + """
</div>
</body>
</html>
"""

@app.route("/")
def home():
    return build_page()

@app.route("/sign", methods=["POST"])
def sign():
    name = request.form["name"]
    message = request.form["message"]
    if name and message:
        add_guest(name, message)
        return build_page("Entry added successfully!")
    return build_page("Please fill in both fields!")

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)