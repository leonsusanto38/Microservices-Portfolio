from django.shortcuts import redirect

from .task import get_prime, get_prime_palindrom

from django.http import HttpResponse

# Create your views here.

def prime(request, n):
    prime = get_prime(n = n)
    html = '<html><h1> Prime %s. </h1></html>'  %prime
    return HttpResponse(html)

def palindrome(request, n):
    palindrome = get_prime_palindrom(n = n)
    html = '<html><h1> Prime and Palindrome %s. </h1></html>' %palindrome
    return HttpResponse(html)