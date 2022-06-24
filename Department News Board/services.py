from nameko.rpc import rpc
import dependencies

class NewsService:
    name = "news_service"

    database = dependencies.Database()

    @rpc
    def register(self, username, password):
        return self.database.register(username, password)

    @rpc
    def login(self, username, password):
        return self.database.login(username, password)

    @rpc
    def get_all_news(self):
        return self.database.get_all_news()
    
    @rpc
    def get_news_by_id(self, news_id):
        return self.database.get_news_by_id(news_id)
    
    @rpc
    def add_news(self, writer, news):
        return self.database.add_news(writer, news)

    @rpc
    def edit_news(self, news_id, writer, news):
        return self.database.edit_news(news_id, writer, news)
    
    @rpc
    def delete_news(self, news_id):
        return self.database.delete_news(news_id)