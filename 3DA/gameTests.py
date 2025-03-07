import unittest
from unittest.mock import patch, MagicMock
from game.Cards import GoldCard, SilverCard
from game.Card import *
from game.Player import Player

class TestGoldCard(unittest.TestCase):
    def setUp(self):
        self.game = MagicMock()  # Mock game object
        self.player = Player(10)
        self.player.flight.goods = 3
        self.player.cardCount = 0
        self.ai_player = MagicMock()
        self.ai_player.flight.goods = 2
        self.ai_player.cards = []

    @patch("builtins.input", side_effect=["Gold 5", "Silver 3", "Blue 7"])  # Mock user input
    def test_gold_card_power(self, mock_input):
        card = GoldCard(Value(5))
        card.power(self.player, self.game)
        
        # Check player received correct cards
        self.assertEqual(self.player.cardCount, 3)

        card.power(self.ai_player, self.game)
        self.assertEqual(len(self.ai_player.cards), 2)

class TestSilverCard(unittest.TestCase):
    def setUp(self):
        self.game = MagicMock()
        self.game.players = [MagicMock(), MagicMock()]
        self.game.players[0].flight.goods = 2
        self.game.players[0].cardCount = 0
        self.game.players[1].flight.goods = 0
        self.game.players[1].cardCount = 0
        self.game.AIPlayer = MagicMock()
        self.game.AIPlayer.flight.goods = 1
        self.game.AIPlayer.cards = []

    @patch("builtins.input", return_value="Gold 10")
    def test_silver_card_power(self, mock_input):
        card = SilverCard(Value(3))
        card.power(self.game.players[0], self.game)

        # Check each player got their extra card if they had goods
        self.assertEqual(self.game.players[0].cardCount, 1)
        self.assertEqual(self.game.players[1].cardCount, 0)

        # Check AIPlayer receives a card
        self.assertEqual(isinstance(self.game.AIPlayer.cards[0], GoldCard), True)

if __name__ == "__main__":
    unittest.main()
