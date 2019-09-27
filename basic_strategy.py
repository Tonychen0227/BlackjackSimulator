from deck_stuff import Card
from enums import Action


class BasicStrategy:
    @staticmethod
    def get_action(player_cards, player_aces, dealer_card: Card):
        dealer_value = dealer_card.print_value()

        # Split?
        if len(player_cards) == 2 and player_cards[0].value == player_cards[1].value:
            value = player_cards[0].print_value()
            if value == 5 or value == 10:
                pass
            if value == 1:
                return Action.SPLIT
            elif value == 2 or value == 3:
                if 2 <= dealer_value <= 7:
                    return Action.SPLIT
                else:
                    return Action.HIT
            elif value == 4:
                if 2 <= dealer_value <= 4:
                    return Action.HIT
                elif 5 <= dealer_value <= 6:
                    return Action.SPLIT
                else:
                    return Action.HIT
            elif value == 6:
                if 2 <= dealer_value <= 6:
                    return Action.SPLIT
                else:
                    return Action.HIT
            elif value == 7:
                if 2 <= dealer_value <= 7:
                    return Action.SPLIT
                else:
                    return Action.HIT
            elif value == 8:
                if 2 <= dealer_value <= 10:
                    return Action.SPLIT
                else:
                    return Action.SURRENDER
            elif value == 9:
                if 2 <= dealer_value <= 6:
                    return Action.SPLIT
                elif 8 <= dealer_value <= 9:
                    return Action.SPLIT
                else:
                    return Action.STAND

        # Soft?
        player_base_sum = 0
        player_number_cards = len(player_cards)
        for card in player_cards:
            player_base_sum += card.print_value()

        if player_aces >= 1 and player_base_sum <= 11:
            if 3 <= player_base_sum <= 4:
                if 5 <= dealer_value <= 6:
                    if player_number_cards == 2:
                        return Action.DOUBLE
                    else:
                        return Action.HIT
                else:
                    return Action.HIT
            elif 5 <= player_base_sum <= 6:
                if 4 <= dealer_value <= 6:
                    if player_number_cards == 2:
                        return Action.DOUBLE
                    else:
                        return Action.HIT
                else:
                    return Action.HIT
            elif player_base_sum == 7:
                if 3 <= dealer_value <= 6:
                    if player_number_cards == 2:
                        return Action.DOUBLE
                    else:
                        return Action.HIT
                else:
                    return Action.HIT
            elif player_base_sum == 8:
                if 2 <= dealer_value <= 6:
                    if player_number_cards == 2:
                        return Action.DOUBLE
                    else:
                        return Action.STAND
                elif 7 <= dealer_value <= 8:
                    return Action.STAND
                else:
                    return Action.HIT
            elif player_base_sum == 9:
                if dealer_value == 6:
                    if player_number_cards == 2:
                        return Action.DOUBLE
                    else:
                        return Action.STAND
                else:
                    return Action.STAND
            else:
                return Action.STAND

        if player_base_sum <= 11 and player_aces >= 1:
            player_base_sum += 10

        if player_base_sum <= 8:
            return Action.HIT
        elif player_base_sum == 9:
            if 3 <= dealer_value <= 6:
                if player_number_cards == 2:
                    return Action.DOUBLE
                else:
                    return Action.HIT
            else:
                return Action.HIT
        elif player_base_sum == 10:
            if 2 <= dealer_value <= 9:
                if player_number_cards == 2:
                    return Action.DOUBLE
                else:
                    return Action.HIT
            else:
                return Action.HIT
        elif player_base_sum == 11:
            if player_number_cards == 2:
                return Action.DOUBLE
            else:
                return Action.HIT
        elif player_base_sum == 12:
            if 4 <= dealer_value <= 6:
                return Action.STAND
            else:
                return Action.HIT
        elif 13 <= player_base_sum <= 14:
            if 2 <= dealer_value <= 6:
                return Action.STAND
            else:
                return Action.HIT
        elif player_base_sum == 15:
            if 2 <= dealer_value <= 6:
                return Action.STAND
            elif dealer_value == 10:
                return Action.SURRENDER
            else:
                return Action.HIT
        elif player_base_sum == 16:
            if 2 <= dealer_value <= 6:
                return Action.STAND
            elif dealer_value >= 9 or dealer_value == 1:
                return Action.SURRENDER
            else:
                return Action.HIT
        else:
            return Action.STAND
