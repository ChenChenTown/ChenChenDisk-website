from flask import Flask, request, send_file, render_template
import sqlite3
import os

app = Flask(__name__)

# Function to initialize the database
def initialize_database():
    conn = sqlite3.connect('ChenChenDisk.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS files
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  filename TEXT,
                  is_folder INTEGER)''')
    conn.commit()
    conn.close()

# Function to save file or folder details to the database
def save_to_database(name, is_folder):
    conn = sqlite3.connect('ChenChenDisk.db')
    c = conn.cursor()
    c.execute("INSERT INTO files (filename, is_folder) VALUES (?, ?)", (name, is_folder))
    conn.commit()
    conn.close()

# Function to get files and folders from the database
def get_files_from_database():
    conn = sqlite3.connect('ChenChenDisk.db')
    c = conn.cursor()
    c.execute("SELECT * FROM files")
    files = c.fetchall()
    conn.close()
    return files

# Route for the home page
@app.route('/')
def index():
    files = get_files_from_database()
    return render_template('index.html', files=files)

# Route to handle file/folder creation
@app.route('/create', methods=['POST'])
def create():
    name = request.form['name']
    is_folder = int(request.form['is_folder'])
    if name:
        if is_folder:
            os.makedirs(os.path.join('uploads', name), exist_ok=True)
        save_to_database(name, is_folder)
    return "File or folder created successfully!"

# Route to handle file downloads
@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(os.path.join('uploads', filename), as_attachment=True)

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
