from celery import shared_task

@shared_task
def is_prime(n):
    for i in range(2,n):
        if (n%i) == 0:
            return False
    return True

@shared_task
def get_prime(n):
    counter = 0
    x = 0
    while(n != counter):
        x += 1
        if (is_prime(x) == True):
            counter += 1
            
    return x

@shared_task
def get_prime_palindrom(n):
    counter = 0
    x = 0
    while(n != counter):
        x += 1
        if(is_prime(x) == True):
            if(str(x) == str(x)[::-1]):
                counter += 1
                
    return x