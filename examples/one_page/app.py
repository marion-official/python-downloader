from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        expression = request.form['expression']
        result = eval(expression)  # Note: Using eval() can be dangerous in production
        return jsonify(result=str(result))
    except Exception as e:
        return jsonify(result='error')


if __name__ == '__main__':
    app.run(debug=True)

