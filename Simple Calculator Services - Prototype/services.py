from nameko.rpc import rpc
import dependencies

class ResearchPaperStorageService:
    name = "simple_calculator_service"

    database = dependencies.Database()

    @rpc
    def get_prime(self, n):
        return self.database.get_prime(n)

    @rpc
    def get_prime_palindrome(self, n):
        return self.database.get_prime_palindrome(n)