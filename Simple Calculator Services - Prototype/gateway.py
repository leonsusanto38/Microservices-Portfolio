import requests
from nameko.web.handlers import http
from werkzeug.wrappers import Response
from nameko.rpc import RpcProxy
from session import SessionProvider

class GatewayService:
    name = "gateway"

    session_provider = SessionProvider()
    services = RpcProxy('simple_calculator_service')

    @http('GET', '/api/prime/<int:n>')
    def register(self, request, n):
        result = self.services.get_prime(n)

        responses = {
            'status': None,
            'message': None,
            'data': None,
        }

        if result != None:
            responses['status'] = "Success"
            responses['message'] = "Register success!"
            responses['data'] = result
        else:
            responses['status'] = "Error"
            responses['message'] = "Email already taken!"

        return Response(str(responses))

    @http('GET', '/api/prime/palindrome/<int:n>')
    def login(self, request, n):
        result = self.services.get_prime_palindrome(n)

        responses = {
            'status': None,
            'message': None,
            'data': None,
        }
        
        if result != None:
            responses['status'] = "Success"
            responses['message'] = "Register success!"
            responses['data'] = result
        else:
            responses['status'] = "Error"
            responses['message'] = "Email already taken!"

        return Response(str(responses))