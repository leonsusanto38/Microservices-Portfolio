import requests
from nameko.web.handlers import http
from werkzeug.wrappers import Response
from nameko.rpc import RpcProxy
from session import SessionProvider

class GatewayService:
    name = "gateway"

    session_provider = SessionProvider()
    services = RpcProxy('research_paper_storage_service')

    @http('POST', '/register')
    def register(self, request):
        data = format(request.get_data(as_text=True))
        array = data.split("&")

        nrp = ""
        name = ""
        email = ""
        password = ""

        for index in array:
            node = index.split("=")
            if (node[0] == "nrp"):
                nrp = node[1]
            elif (node[0] == "name"):
                name = node[1]
            elif (node[0] == "email"):
                email = node[1]
            elif (node[0] == "password"):
                password = node[1]
        nrp = requests.utils.unquote(nrp)
        name = requests.utils.unquote(name)
        email = requests.utils.unquote(email)
        password = requests.utils.unquote(password)
        
        result = self.services.register(nrp, name, email, password)

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
            responses['message'] = "Username already taken!"

        return Response(str(responses))

    @http('POST', '/login')
    def login(self, request):
        responses = {
            'status': None,
            'message': None,
            'data': None,
        }

        cookies = request.cookies
        if cookies:
            responses['status'] = "Error"
            responses['message'] = "You already login!"
            return Response(str(responses))
        else:
            data = format(request.get_data(as_text=True))
            array = data.split("&")

            email = ""
            password = ""

            for index in array:
                node = index.split("=")
                if (node[0] == "email"):
                    email = node[1]
                elif (node[0] == "password"):
                    password = node[1]
            email = requests.utils.unquote(email)
            password = requests.utils.unquote(password)
            
            result = self.services.login(email, password)

            if result != None:
                responses['status'] = "Success"
                responses['message'] = "Login success!"
                responses['data'] = result
                
                response = Response(str(responses))
                session_id = self.session_provider.set_session(responses)
                response.set_cookie('SESS_ID', session_id)
                
                return response
            else:
                responses['status'] = "Error"
                responses['message'] = "Wrong username & password!"
                return Response(str(responses))

    @http('GET', '/logout')
    def logout(self, request):
        cookies = request.cookies
        
        responses = {
            'status': None,
            'message': None,
            'data': None,
        }

        if cookies:
            responses['status'] = "Success"
            responses['message'] = "Logout success!"

            response = Response(str(responses))
            response.delete_cookie('SESS_ID')
            
            return response
        else:
            responses['status'] = "Error"
            responses['message'] = "You not logged in!"

            return Response(str(responses))