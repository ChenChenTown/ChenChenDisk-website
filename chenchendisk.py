from flask import Flask, request, send_file, render_template
import sqlite3
import os

app = Flask(__name__)

# Function to initialize the database
def initialize_database():
    conn = sqlite3.connect('chenchendisk.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS files
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  filename TEXT)''')
    conn.commit()
    conn.close()

# Function to save file details to the database
def save_to_database(filename):
    conn = sqlite3.connect('chenchendisk.db')
    c = conn.cursor()
    c.execute("INSERT INTO files (filename) VALUES (?)", (filename,))
    conn.commit()
    conn.close()

# Function to get file details from the database
def get_files_from_database():
    conn = sqlite3.connect('chenchendisk.db')
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

# Route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filename = file.filename
        file.save(os.path.join('uploads', filename))
        save_to_database(filename)
    return "File uploaded successfully!"

# Route to handle file downloads
@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join('uploads', filename), as_attachment=True)

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
