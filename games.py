from dataclasses import dataclass
from abc import ABC
from typing import Union

@dataclass
class Card:
    game_value: int
    human_value: Union[int, str]
    suit: str


class Deck:

    deck = []
    human_values = [x for x in range(2, 11)]
    human_values_pics = ['j', 'q', 'k', 'a']
    human_values.extend(human_values_pics)
    suits = ['♤', '♡', '♧', '♢']

    for suit in suits:
        for human_value in human_values:
            if isinstance(human_value, int):
                game_value = human_value
            elif human_value in ['j', 'q', 'k']:
                game_value = 10
            else:
                game_value = 11
            card = Card(game_value, human_value, suit)
            deck.append(card)
