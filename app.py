import os
import psycopg2
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS calculations (
            id SERIAL PRIMARY KEY,
            num1 FLOAT,
            num2 FLOAT,
            operation TEXT,
            result FLOAT
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

# Initialize DB when app starts
with app.app_context():
    init_db()

@app.route('/', methods=['GET', 'POST'])
def calculator():
    conn = get_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        operation = request.form['operation']

        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            result = num1 / num2 if num2 != 0 else 0

        cur.execute(
            "INSERT INTO calculations (num1, num2, operation, result) VALUES (%s, %s, %s, %s)",
            (num1, num2, operation, result)
        )
        conn.commit()

    cur.execute("SELECT * FROM calculations ORDER BY id DESC")
    data = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('index.html', data=data)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM calculations WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    new_result = request.form['result']
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE calculations SET result = %s WHERE id = %s",
        (new_result, id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')