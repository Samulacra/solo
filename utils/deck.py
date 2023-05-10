import random
from collections import UserList
from enum import Enum
from typing import TypeVar

TCard = TypeVar('TCard')

class Deck(UserList[TCard]):
        
    def shuffle(self, rng: random.Random | None = None) -> None:
        (rng or random).shuffle(self)

class Suit(Enum):
    CLUBS = '♣'
    DIAMONDS = '♦'
    HEARTS = '♥'
    SPADES = '♠'

class Rank(Enum):
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"

class PlayingCard():

    def __init__(self, rank: Rank, suit: Suit) -> None:
        self._rank = rank
        self._suit = suit

    @property
    def value(self) -> str:
        return self.rank.value + self.suit.value

    @property
    def rank(self) -> Rank:
        return self._rank

    @property
    def suit(self) -> Suit:
        return self._suit
 
def playing_cards():
    ranks = [e for e in Rank]
    suits = [e for e in Suit]
    return Deck([PlayingCard(rank, suit) for rank in ranks for suit in suits])