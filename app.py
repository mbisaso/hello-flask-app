import os
import psycopg2
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def get_connection():
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set!")
    return psycopg2.connect(url)

def init_db():
    try:
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
    except Exception as e:
        print(f"DB init failed: {e}")

@app.route('/', methods=['GET', 'POST'])
def calculator():
    result = None  # <-- track result to show on page
    try:
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
                # Fix: use float division, handle zero
                result = num1 / num2 if num2 != 0 else "Error: division by zero"

            cur.execute(
                "INSERT INTO calculations (num1, num2, operation, result) VALUES (%s, %s, %s, %s)",
                (num1, num2, operation, result if isinstance(result, float) else 0)
            )
            conn.commit()

        cur.execute("SELECT * FROM calculations ORDER BY id DESC")
        data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('index.html', data=data, result=result)

    except Exception as e:
        return f"<h2>Database Error: {e}</h2>", 500

@app.route('/delete/<int:id>')
def delete(id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM calculations WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        return f"<h2>Error: {e}</h2>", 500
    return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    try:
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
    except Exception as e:
        return f"<h2>Error: {e}</h2>", 500
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))