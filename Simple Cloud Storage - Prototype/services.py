from nameko.rpc import rpc
import dependencies

class ResearchPaperStorageService:
    name = "cloud_storage_service"

    database = dependencies.Database()

    @rpc
    def register(self, username, password):
        return self.database.register(username, password)

    @rpc
    def login(self, username, password):
        return self.database.login(username, password)