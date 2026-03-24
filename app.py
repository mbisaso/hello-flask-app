#from flask import Flask

#app = Flask(__name__)

#@app.route('/')
#def home():
 #   return "Hello, Coolify! My Flask app is working!!"

#if __name__ == '__main__':
 #   app.run(host='0.0.0.0', port=8080)
 
from flask import Flask, request

app = Flask(__name__)

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
                result = num1 / num2

        except:
            result = "Error: Invalid input"

    return f"""
    <h2>Simple Flask Calculator</h2>
    <form method="post">
        <input type="text" name="num1" placeholder="First number" required><br><br>
        <input type="text" name="num2" placeholder="Second number" required><br><br>

        <select name="operation">
            <option value="add">Add</option>
            <option value="subtract">Subtract</option>
            <option value="multiply">Multiply</option>
            <option value="divide">Divide</option>
        </select><br><br>

        <button type="submit">Calculate</button>
    </form>

    <h3>Result: {result}</h3>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)