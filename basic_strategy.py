from abstractions import Action

class BasicStrategy:
    @staticmethod
    def get_action(self, playerSums, playerAces, dealerCard):
        return Action.DOUBLE
