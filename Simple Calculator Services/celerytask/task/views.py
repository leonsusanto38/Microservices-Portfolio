import json
from django.shortcuts import redirect

from .task import get_prime, get_prime_palindrom

from django.http import HttpResponse

# Create your views here.

def create_response(result):
    response_data = {
        'result': result
    }
    return json.dumps(response_data)

def prime(request, n):
    prime = get_prime(n = n)
    response = create_response(prime)
    return HttpResponse(response, content_type="application/json")

def palindrome(request, n):
    palindrome = get_prime_palindrom(n = n)
    response = create_response(palindrome)
    return HttpResponse(response, content_type="application/json")