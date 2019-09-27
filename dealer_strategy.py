from typing import List

from deck_stuff import Card
from enums import Action


class DealerStrategy:
    @staticmethod
    def get_action(player_cards: List[Card], player_aces) -> Action:
        sum_so_far = 0
        for card in player_cards:
            sum_so_far += card.print_value()

        if sum_so_far >= 17:
            return Action.STAND

        if player_aces >= 1 and 8 <= sum_so_far <= 11:
            sum_so_far += 10

        if sum_so_far >= 17:
            return Action.STAND

        return Action.HIT
