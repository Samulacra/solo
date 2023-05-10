import unittest
import random

from utils.deck import playing_cards, Deck, PlayingCard, Rank, Suit

class TestDeck(unittest.TestCase):

    def test_draw_cards(self):
        deck = Deck([1, 2, 3, 4])

        top_card = deck.pop()
        self.assertEqual(top_card, 4)

        bottom_card = deck.pop(0)
        self.assertEqual(bottom_card, 1)

    def test_shuffle_cards(self):
        deck = Deck([1, 2, 3, 4])
        r = random.Random(int("deadbeef13", 16))
        deck.shuffle(r)
        self.assertEqual(deck, [2, 3, 1, 4])

class TestPlayingCards(unittest.TestCase):

    def test_playing_cards(self):
        deck = playing_cards()

        # Has 52 cards
        self.assertEqual(len(deck), 52)

        # Has 13 each of Clubs, Diamonds, Hearts, Spades
        self._validate_suit(deck, Suit.CLUBS)
        self._validate_suit(deck, Suit.DIAMONDS)
        self._validate_suit(deck, Suit.HEARTS)
        self._validate_suit(deck, Suit.SPADES)

    def _validate_suit(self, deck: Deck[PlayingCard], suit: Suit):
        _ranks = [rank for rank in Rank]
        _cards = list(filter(lambda card: card.suit == suit, deck))
        for idx in range(13):
            self.assertEqual(_cards[idx].rank, _ranks[idx])

