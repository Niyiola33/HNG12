from django.http import JsonResponse
import requests
import math

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    if n < 2:
        return False
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n

def is_armstrong(n):
    digits = [int(d) for d in str(abs(n))]  # Handle negative numbers
    num_digits = len(digits)
    return sum(d**num_digits for d in digits) == abs(n)

def digit_sum(n):
    return sum(int(d) for d in str(abs(n)))  # Handle negative numbers

def classify_number(request):
    number = request.GET.get('number')
    
    # Validate input
    try:
        number = float(number)  # Accept decimal numbers
    except (TypeError, ValueError):
        return JsonResponse({
            "number": number,
            "error": True,
            "message": "Invalid input. Please provide a valid number."
        }, status=400)
    
    # Prepare response
    response = {
        "number": number,
        "is_prime": is_prime(int(number)) if number.is_integer() else False,  # Only integers can be prime
        "is_perfect": is_perfect(int(number)) if number.is_integer() else False,  # Only integers can be perfect
        "properties": [],
        "digit_sum": digit_sum(int(number)) if number.is_integer() else None,  # Only integers have digit sums
        "fun_fact": None
    }
    
    # Add properties
    if number.is_integer():
        if is_armstrong(int(number)):
            response["properties"].append("armstrong")
        if number % 2 == 0:
            response["properties"].append("even")
        else:
            response["properties"].append("odd")
    else:
        response["properties"].append("decimal")
    
    # Fetch fun fact from Numbers API (only for integers)
    if number.is_integer():
        fun_fact_response = requests.get(f'http://numbersapi.com/{int(number)}')
        response["fun_fact"] = fun_fact_response.text if fun_fact_response.status_code == 200 else "No fun fact available."
    else:
        response["fun_fact"] = "Fun facts are only available for integers."
    
    return JsonResponse(response)