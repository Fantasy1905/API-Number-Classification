# Deploying a Number-Classification Flask_CORS API Using Lambda Function

## Summing-Up
##### __Number Classification API is just a simple HTTP API gateway that allows number classification based on mathematical properties provided. This API can be publicly accessible using AWS Lambda or other Cloud plateform with a well configured API Gateway. Lambda Function and API Gateway is serverless that is scalable and cost-efficient to deploy a simple module.__ 

>## Technology Stack:
*  CORS is enabled for public accessibility.
*  JSONIFY based reponse.
*  Logic that determines if a number is prime, even, and odd.
*  Accept multiple number classification in a single request.
  
>## Resourcess Used
* AWS Lambda
* API Gateway 
* Python 
* GitHub

>## Set Up Instructions
## Create and Activate Virtual Environment
```python
python -m venv venv
Source venv\Scripts\activate
``` 
## Install depenencies
~~~python
pip install flask flask-cors
~~~
~~~python
Downloading Flask_Cors-5.0.0-py2.py3-none-any.whl.metadata (5.5 kB)
Requirement already satisfied: Flask>=0.9 in c:\users\hp\appdata\local\programs\python\python313\lib\site-packages (from flask-cors) (3.1.0)
Requirement already satisfied: Werkzeug>=3.1 in c:\users\hp\appdata\local\programs\python\python313\lib\site-packages (from Flask>=0.9->flask-cors) (3.1.3)
Requirement already satisfied: Jinja2>=3.1.2 in c:\users\hp\appdata\local\programs\python\python313\lib\site-packages (from Flask>=0.9->flask-cors) (3.1.5)
Requirement already satisfied: itsdangerous>=2.2 in c:\users\hp\appdata\local\programs\python\python313\lib\site-packages (from Flask>=0.9->flask-cors) (2.2.0)
Requirement already satisfied: click>=8.1.3 in c:\users\hp\appdata\local\programs\python\python313\lib\site-packages (from Flask>=0.9->flask-cors) (8.1.8)
Requirement already satisfied: blinker>=1.9 in c:\users\hp\appdata\local\programs\python\python313\lib\site-packages (from Flask>=0.9->flask-cors) (1.9.0)
Requirement already satisfied: colorama in c:\users\hp\appdata\local\programs\python\python313\lib\site-packages (from click>=8.1.3->Flask>=0.9->flask-cors) (0.4.6)
Requirement already satisfied: MarkupSafe>=2.0 in c:\users\hp\appdata\local\programs\python\python313\lib\site-packages (from Jinja2>=3.1.2->Flask>=0.9->flask-cors) (3.0.2)
Downloading Flask_Cors-5.0.0-py2.py3-none-any.whl (14 kB)
Installing collected packages: flask-cors
Successfully installed flask-cors-5.0.0
~~~
## Creating the Flask App
~~~python
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
~~~
## API Deployed Locally 
~~~python
cuments/Devops/HNG Project/stage 1/API/main.py"
 * Serving Flask app 'main'
 * Debug mode: on
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.        
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.        
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 934-514-253
127.0.0.1 - - [05/Feb/2025 01:40:38] "GET /api/classify-number?number=153 HTTP/1.1" 200 -
127.0.0.1 - - [05/Feb/2025 01:41:30] "GET /api/classify-number?number=153 HTTP/1.1" 200 -
127.0.0.1 - - [05/Feb/2025 08:25:31] "GET /api/classify-number?number=153 HTTP/1.1" 200 
~~~
## Test API Locally:
~~~python
http://127.0.0.1:5000/api/classify-number?number=153
~~~
## JSON Response
~~~python
{
  "digit_sum": 9,
  "fun_fact": "153 is an Armstrong number because 1^3+5^3+3^3 = 153.",
  "is_perfect": false,
  "is_prime": false,
  "number": 153,
  "properties": [
    "odd",
    "armstrong"
  ]
}
~~~
## Deploy API on Lambda Enironment
~~~python
import json

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    if n <= 0:
        return False  # Fix: 0 should not be a perfect number
    return n == sum(i for i in range(1, n) if n % i == 0)

def is_armstrong(n):
    digits = [int(d) for d in str(abs(n))]  # Use absolute value to avoid issues
    power = len(digits)
    return n == sum(d**power for d in digits)

def get_fun_fact(n):
    if is_armstrong(n):
        return f"{n} is an Armstrong number because {' + '.join([f'{d}^{len(str(abs(n)))}' for d in str(abs(n))])} = {n}"
    elif is_prime(n):
        return f"{n} is a prime number because it has only two divisors: 1 and itself."
    elif is_perfect(n):
        return f"{n} is a perfect number because the sum of its proper divisors equals the number."
    else:
        return f"{n} is just an interesting number!"

def lambda_handler(event, context):
    try:
        query_params = event.get("queryStringParameters", {})
        num_str = query_params.get("number", "")

        # Validate input: number must be a valid integer or float
        try:
            num = float(num_str) if "." in num_str else int(num_str)
        except ValueError:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"number": num_str, "error": True})
            }

        # Construct response data
        response = {
            "number": num,
            "is_prime": is_prime(int(num)),  # Convert to int for prime check
            "is_perfect": is_perfect(int(num)),  # Convert to int for perfect check
            "properties": ["odd" if int(num) % 2 else "even"],
            "digit_sum": sum(int(d) for d in str(abs(int(num)))),
            "fun_fact": get_fun_fact(int(num))
        }

        if is_armstrong(int(num)):
            response["properties"].append("armstrong")

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(response)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }
~~~
## Create an API Gateway
* Choose HTTP API.
* Add Integration - Choose Lambda Function.
* Select your Lambda function (Number_Classification).
* Enter /api/classify-number as the route.
* Choose GET as the method.
* Then Deploy

## API Test
Copy the invoke URL and past on the brower
~~~python
https://x71n6tgymk.execute-api.us-east-1.amazonaws.com/test/api/classify-number?number=371
~~~
Output
~~~python
 "digit_sum": 9,
  "fun_fact": "153 is an Armstrong number because 1^3+5^3+3^3 = 153.",
  "is_perfect": false,
  "is_prime": false,
  "number": 153,
  "properties": [
    "odd",
    "armstrong"
  ]
  ~~~

## Enabling CORS in API Gateway

## Skills Achieved 
* Deploy Lambda Function using HTTP API.
* Configure CORS for public API access.
* Handling API requests and responses in JSON format.
* Write Logic that determines if a number is prime, even, and odd with python 
