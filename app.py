from flask import Flask, request, render_template, send_file
import sqlite3, psycopg2, json, os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)


# ------------------ HOME ------------------
# Home Page
@app.route('/')
def home():
    return render_template('home.html')  # Shows both options

# Serve JSON → DB page
@app.route('/json_to_db_page')
def json_to_db_page():
    return render_template('json_to_db.html')

# Serve DB → JSON page
@app.route('/db_to_json_page')
def db_to_json_page():
    return render_template('db_to_json.html')



# ------------------ JSON → DB ------------------
@app.route('/json_to_db', methods=['POST'])
def json_to_db():
    try:
        db_type = request.form.get('db_type')
        db_name = request.form.get('db_name')
        db_user = request.form.get('db_user')
        db_password = request.form.get('db_password')
        file = request.files.get('json_file')

        if not file or not db_name or not db_type:
            return "❌ Please provide all required fields."

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, list) or not data:
            return "❌ JSON must be a non-empty list of objects."

        columns = list(data[0].keys())
        table_name = os.path.splitext(filename)[0].replace('-', '_')

        # --- SQLite ---
        if db_type == "sqlite":
            db_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{db_name}.db")
            conn = sqlite3.connect(db_path)
            c = conn.cursor()

            c.execute(f"DROP TABLE IF EXISTS {table_name}")
            create_stmt = f"CREATE TABLE {table_name} ({', '.join([f'\"{col}\" TEXT' for col in columns])})"
            c.execute(create_stmt)

            for row in data:
                values = [str(row.get(col, '')) for col in columns]
                c.execute(f"INSERT INTO {table_name} VALUES ({', '.join(['?'] * len(values))})", values)

            conn.commit()
            conn.close()

            return render_template('result.html',
                                   message=f"✅ JSON stored in SQLite DB: {db_name}.db",
                                   download_link=f"/download/{db_name}.db")

        # --- PostgreSQL ---
        elif db_type == "postgres":
            import psycopg2
            import subprocess

            conn = psycopg2.connect(
                host="localhost",
                database=db_name,
                user=db_user,
                password=db_password
            )
            cur = conn.cursor()

            cur.execute(f"DROP TABLE IF EXISTS {table_name}")
            create_stmt = f"CREATE TABLE {table_name} ({', '.join([f'\"{col}\" TEXT' for col in columns])})"
            cur.execute(create_stmt)

            for row in data:
                values = [str(row.get(col, '')) for col in columns]
                cur.execute(f"INSERT INTO {table_name} VALUES ({', '.join(['%s'] * len(values))})", values)

            conn.commit()
            conn.close()

            # --- Export PostgreSQL table to SQL file for download ---
            sql_file_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{db_name}_{table_name}.sql")
            dump_cmd = f'pg_dump -h localhost -U {db_user} -t {table_name} {db_name} > "{sql_file_path}"'
            subprocess.run(dump_cmd, shell=True, check=True, env={**os.environ, "PGPASSWORD": db_password})

            return render_template('result.html',
                                   message=f"✅ JSON stored in PostgreSQL ({db_name})",
                                   download_link=f"/download/{db_name}_{table_name}.sql")
        else:
            return "❌ Invalid database type."

    except Exception as e:
        print("⚠️ Error:", e)
        return f"Error: {e}"


# ------------------ DB → JSON (Step 1: Upload DB) ------------------
@app.route('/db_to_json', methods=['POST'])
def db_to_json():
    file = request.files.get('db_file')
    if not file:
        return render_template('result.html', message="❌ No DB file uploaded!", download_link="#")

    filename = secure_filename(file.filename)
    db_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(db_path)

    # SQLite: fetch table names
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    try:
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in c.fetchall()]
    except Exception as e:
        conn.close()
        return render_template('result.html', message=f"❌ Error reading DB: {e}", download_link="#")
    conn.close()

    if not tables:
        return render_template('result.html', message="❌ No tables found in DB!", download_link="#")

    return render_template('select_table.html', tables=tables, db_filename=filename)


# ------------------ DB → JSON (Step 2: Export selected table) ------------------
@app.route('/export_json', methods=['POST'])
def export_json():
    db_filename = request.form.get('db_filename')
    table_name = request.form.get('table_name')
    if not db_filename or not table_name:
        return render_template('result.html', message="❌ DB file or table name missing!", download_link="#")

    db_path = os.path.join(app.config['UPLOAD_FOLDER'], db_filename)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    try:
        rows = c.execute(f"SELECT * FROM {table_name}").fetchall()
        data = [dict(row) for row in rows]
    except Exception as e:
        conn.close()
        return render_template('result.html', message=f"❌ Error fetching table: {e}", download_link="#")
    conn.close()

    json_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{table_name}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    return render_template('result.html', message=f"✅ Table '{table_name}' exported to JSON!", download_link=f"/download/{table_name}.json")


# ------------------ DOWNLOAD ------------------
@app.route('/download/<filename>')
def download(filename):
    path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    if not os.path.exists(path):
        return f"❌ File '{filename}' not found!"
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
