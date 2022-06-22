import json
import string
import requests as req
from unittest import result
from xml.etree.ElementTree import tostring

from nameko.rpc import RpcProxy
from nameko.web.handlers import http
from werkzeug.wrappers import Response
from session import SessionProvider

class GatewayService:
    name = 'gateway'

    database = RpcProxy('user_service')
    session_provider = SessionProvider()
    
    @http('POST', '/regis')
    def regis(self, request):
        data = format(request.get_data(as_text=True))
        arr  =  data.split("&")

        username = "" 
        password = "" 

        for separator in arr:
            node = separator.split("=")
            if node[0] == "username":
                username = node[1]
            if node[0] == "password":
                password = node[1]
        data_regis = self.database.regis(username, password)
        return json.dumps(data_regis)
    
    @http('GET', '/login')
    def login(self, request):
        data = format(request.get_data(as_text=True))
        arr  =  data.split("&")

        username = "" 
        password = "" 

        for separator in arr:
            node = separator.split("=")
            if node[0] == "username":
                username = node[1]
            if node[0] == "password":
                password = node[1]
        flags = self.database.login(username, password)
        
        if(flags == 1):
            user_data = {
                'username': username,
                'password': password
            }
            session_id = self.session_provider.set_session(user_data)
            response = Response(str(user_data))
            response.set_cookie('SESSID', session_id)
            return response
        else:
            result = []
            result.append("Username / password incorrect")
            return json.dumps(result)
    
    @http('GET', '/check')
    def check(self, request):
        cookies = request.cookies
        return Response(cookies['SESSID'])
    
    @http('POST', '/logout')
    def logout(self, request):
        cookies = request.cookies
        if cookies:
            confirm = self.session_provider.delete_session(cookies['SESSID'])
            if (confirm):
                response = Response('Logout successful')
                response.delete_cookie('SESSID')
            else:
                response = Response("Logout failed")
            return response
        else:
            response = Response('Required login')
            return response
        
    @http('GET', '/all_news')
    def get_all_news(self, request):
        news = self.database.get_all_news()
        return json.dumps(news)
    
    @http('GET', '/all_news/<int:id>')
    def get_news(self, request, id):
        news = self.database.get_news(id)
        return json.dumps(news)
    
    @http('POST', '/post_news')
    def post_news(self, request):
        cookies = request.cookies
        if cookies:
            data = format(request.get_data(as_text=True))
            arr  =  data.split("&")

            username = "" 
            news = "" 

            for separator in arr:
                node = separator.split("=")
                if node[0] == "username":
                    username = node[1]
                if node[0] == "news":
                    news = node[1]
            news = req.utils.unquote(news)
            data = self.database.post_news(username, news)
            return json.dumps(data)
        else:
            result = []
            result.append("Login Required")
            return json.dumps(result)
        
    @http('POST', '/update_news/<int:id>')
    def edit_news(self, request, id):
        cookies = request.cookies
        if cookies:
            data = format(request.get_data(as_text=True))
            arr  =  data.split("&")

            username = "" 
            news = "" 

            for separator in arr:
                node = separator.split("=")
                if node[0] == "username":
                    username = node[1]
                if node[0] == "news":
                    news = node[1]
            username = req.utils.unquote(username)
            news = req.utils.unquote(news)
            data = self.database.edit_news(id, username, news)
            return json.dumps(data)
        else:
            result = []
            result.append("Login Required")
            return json.dumps(result)
        
    @http('DELETE', '/delete_news/<int:id>')
    def delete_news(self, request, id):
        cookies = request.cookies
        if cookies:
            news = self.database.delete_news(id)
            return json.dumps(news)
        else:
            result = []
            result.append("Login Required")
            return json.dumps(result)