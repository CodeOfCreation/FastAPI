from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Flask Calculator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f4f4;
            display: flex;
            justify-content: center;
            margin-top: 50px;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
            width: 320px;
        }
        input, select, button {
            width: 100%;
            padding: 10px;
            margin: 8px 0;
            font-size: 16px;
        }
        h2 {
            text-align: center;
        }
        .result {
            margin-top: 15px;
            font-weight: bold;
            text-align: center;
            color: green;
        }
        .error {
            margin-top: 15px;
            font-weight: bold;
            text-align: center;
            color: red;
        }
    </style>
</head>
<body>
<div class="container">
    <h2>Calculator</h2>
    <form method="POST">
        <input type="number" step="any" name="num1" placeholder="First Number" required>

        <select name="operation">
            <option value="+">Addition (+)</option>
            <option value="-">Subtraction (-)</option>
            <option value="*">Multiplication (*)</option>
            <option value="/">Division (/)</option>
        </select>

        <input type="number" step="any" name="num2" placeholder="Second Number" required>

        <button type="submit">Calculate</button>
    </form>

    {% if result is not none %}
        <div class="result">Result: {{ result }}</div>
    {% endif %}

    {% if error %}
        <div class="error">{{ error }}</div>
    {% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def calculator():
    result = None
    error = ""

    if request.method == "POST":
        try:
            num1 = float(request.form["num1"])
            num2 = float(request.form["num2"])
            operation = request.form["operation"]

            if operation == "+":
                result = num1 + num2
            elif operation == "-":
                result = num1 - num2
            elif operation == "*":
                result = num1 * num2
            elif operation == "/":
                if num2 == 0:
                    error = "Cannot divide by zero."
                else:
                    result = num1 / num2

        except ValueError:
            error = "Please enter valid numbers."

    return render_template_string(HTML, result=result, error=error)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)