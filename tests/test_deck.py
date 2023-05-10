import unittest
from itertools import groupby
import random

from utils.deck import playing_cards, Deck, Rank, Suit

class TestDeck(unittest.TestCase):

    def test_playing_cards(self):
        deck = playing_cards()

        # Has 52 cards
        self.assertEqual(len(deck), 52)

        # Has 13 each of Clubs, Diamonds, Hearts, Spades
        ranks = [rank for rank in Rank]
        clubs = list(filter((lambda card: card.suit == Suit.CLUBS), deck))
        diamonds = list(filter((lambda card: card.suit == Suit.DIAMONDS), deck))
        hearts = list(filter((lambda card: card.suit == Suit.HEARTS), deck))
        spades = list(filter((lambda card: card.suit == Suit.SPADES), deck))
        for idx in range(13):
            self.assertEqual(clubs[idx].rank, ranks[idx])
            self.assertEqual(diamonds[idx].rank, ranks[idx])
            self.assertEqual(hearts[idx].rank, ranks[idx])
            self.assertEqual(spades[idx].rank, ranks[idx])

class TestPlayingCards(unittest.TestCase):

    def test_draw_cards(self):
        deck = Deck([1, 2, 3, 4])

        top_card = deck.pop()
        self.assertEqual(top_card, 4)

        bottom_card = deck.pop(0)
        self.assertEqual(bottom_card, 1)