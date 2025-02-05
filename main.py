from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(_name_)
CORS(app)  # Enable CORS

def is_prime(n):
    """Check if integer n is a prime"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    """Check if integer n is a perfect number"""
    if n < 2:
        return False
    total = 1
    for i in range(2, n):
        if n % i == 0:
            total += i
            if total > n:
                return False
        if total == n:
            return True
    return False

def is_armstrong(n):
    """Check if integer n is an Armstrong number"""
    digits = [int(d) for d in str(n)]
    return n==sum(d ** len(digits) for d in digits)

def get_fun_fact(n):
    """Get fun fact about integer n"""
    if is_prime(n):
        return f"{n} is a prime number because it has only two division: 1 and itself."
    if is_perfect(n):
        return f"{n} is a prime number because the sum of its proper diisors equals the number."
    if is_armstrong(n):
        return f"{n} is an Armstrong number because {'+'.join([f'{d}^{len(str(n))}' for d in str(n)])} = {n}."
    else:
        return f"{n} is just an interesting number!"
    

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    num = request.args.get('number')

    if not num or not num.isdigit():
        return jsonify({"number": num, "error": True}), 400

    num = int(num)
    
    response = {
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": ["odd" if num % 2 else "even"],
        "digit_sum": sum(int(d) for d in str(num)),
        "fun_fact": get_fun_fact(num)
    }

    if is_armstrong(num):
        response["properties"].append("armstrong")

    return jsonify(response)

if _name_ == '_main_':
    app.run(debug=True)
