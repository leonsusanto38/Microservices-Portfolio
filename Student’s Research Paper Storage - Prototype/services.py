from nameko.rpc import rpc
import dependencies

class ResearchPaperStorageService:
    name = "research_paper_storage_service"

    database = dependencies.Database()

    @rpc
    def register(self, nrp, name, email, password):
        return self.database.register(nrp, name, email, password)

    @rpc
    def login(self, email, password):
        return self.database.login(email, password)