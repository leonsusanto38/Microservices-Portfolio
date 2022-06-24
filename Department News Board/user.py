from nameko.rpc import rpc

import dependencies

class UserService:

    name = 'user_service'

    database = dependencies.Database()

    @rpc
    def regis(self, username, password):
        user = self.database.regis(username, password)
        return user
    
    @rpc
    def login(self, username, password):
        user = self.database.login(username, password)
        return user
    
    @rpc
    def get_all_news(self):
        news = self.database.get_all_news()
        return news

    @rpc
    def get_news(self, newsid):
        news = self.database.get_news(newsid)
        return news
    
    @rpc
    def post_news(self, username, desc):
        news = self.database.post_news(username, desc)
        return news
    
    @rpc
    def edit_news(self, id, username, news):
        news = self.database.edit_news(id, username, news)
        return news
    
    @rpc
    def delete_news(self, id):
        news = self.database.delete_news(id)
        return news