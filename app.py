#from flask import Flask

#app = Flask(__name__)

#@app.route('/')
#def home():
 #   return "Hello, Coolify! My Flask app is working!!"

#if __name__ == '__main__':
 #   app.run(host='0.0.0.0', port=8080)
 
import os
import psycopg2
from flask import Flask, request

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

conn = None
cur = None

if DATABASE_URL:
    conn = psycopg2.connect(DATABASE_URL)
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

@app.route('/', methods=['GET', 'POST'])
def calculator():
    result = ""

    if request.method == 'POST':
        num1 = request.form.get('num1')
        num2 = request.form.get('num2')
        operation = request.form.get('operation')

        try:
            num1 = float(num1)
            num2 = float(num2)

            if operation == 'add':
                result = num1 + num2
            elif operation == 'subtract':
                result = num1 - num2
            elif operation == 'multiply':
                result = num1 * num2
            elif operation == 'divide':
                if num2 == 0:
                    result = "Error: Division by zero"
                else:
                    result = num1 / num2
            else:
                result = "Invalid operation"

            # Save ONLY valid numeric results to DB
            if isinstance(result, (int, float)):
                if cur and conn:
                    try:
                        cur.execute(
                            "INSERT INTO calculations (num1, num2, operation, result) VALUES (%s, %s, %s, %s)",
                            (num1, num2, operation, result)
                        )
                        conn.commit()
                    except Exception as e:
                        print("Database error:", e)

        except Exception as e:
            result = "Error: Invalid input"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Calculator</title>
        <style>
            body {{
                font-family: Arial;
                background: #f4f6f8;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}

            .container {{
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
                text-align: center;
            }}

            input {{
                padding: 10px;
                margin: 10px;
                width: 200px;
            }}

            button {{
                padding: 10px 15px;
                margin: 5px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }}

            .add {{ background: #4CAF50; color: white; }}
            .sub {{ background: #f44336; color: white; }}
            .mul {{ background: #2196F3; color: white; }}
            .div {{ background: #ff9800; color: white; }}

            h2 {{
                margin-bottom: 20px;
            }}
        </style>
    </head>

    <body>
        <div class="container">
            <h2>Flask Calculator</h2>

            <form method="post">
                <input type="text" name="num1" placeholder="First number" required><br>
                <input type="text" name="num2" placeholder="Second number" required><br>

                <button class="add" name="operation" value="add">+</button>
                <button class="sub" name="operation" value="subtract">-</button>
                <button class="mul" name="operation" value="multiply">*</button>
                <button class="div" name="operation" value="divide">/</button>
            </form>

            <h3>Result: {result}</h3>
        </div>
    </body>
        </html>
        """
    
    if __name__ == '__main__':
        port = int(os.environ.get("PORT", 8080))
        app.run(host='0.0.0.0', port=port)