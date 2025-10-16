

DataBridge:

A Flask-based web application that allows you to convert JSON files to databases (SQLite/PostgreSQL) and export databases back to JSON. The project provides a clean, responsive UI and professional dashboard experience.

---

Features:
Upload a JSON file and store it in SQLite or PostgreSQL.
Export a database table (SQLite/PostgreSQL) back to a JSON file.
Dynamic table creation based on JSON keys.
Download the generated SQLite `.db` or JSON file.
Responsive design, works on all devices.
Professional and modern dashboard interface.

---

Technologies Used:

 Backend: Python, Flask, SQLite, psycopg2 (PostgreSQL)
 Frontend: HTML, CSS, JavaScript
 Libraries: Flask, werkzeug (for secure file uploads)

---

Project Structure:

```
json-db-dashboard/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
│   ├── home.html
│   ├── json_to_db.html
│   ├── db_to_json.html
│   ├── result.html
├── static/                # CSS, JS, images
│   └── style.css
├── uploads/               # Temporary uploaded files
└── outputs/               # Generated DB/JSON files
```

---

Installation:

1. Clone the repository:

```bash
git clone https://github.com/yourusername/json-db-dashboard.git
cd json-db-dashboard
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the Flask app:

```bash
python app.py
```

5. Open your browser at:

```
http://127.0.0.1:5000
```

---

 Usage:

1. Home Page:

   * Choose either JSON → DB or DB → JSON option.

2. JSON → DB:

   * Upload a JSON file.
   * Enter database name and choose SQLite or PostgreSQL.
   * Click Convert.
   * Download the SQLite `.db` file (if selected) or use PostgreSQL.

3. DB → JSON:

   * Upload a SQLite `.db` file.
   * Enter the table name to export.
   * Click Convert.
   * Download the JSON file.

---

Notes:

* JSON must be a list of objects. Example:

```json
[
  { "name": "France", "capital": "Paris", "population": 67364357 },
  { "name": "Germany", "capital": "Berlin", "population": 83240525 }
]
```

* PostgreSQL option requires a running PostgreSQL instance and valid credentials.

---

## **License**

MIT License © 2025


