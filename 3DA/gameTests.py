import unittest
from unittest.mock import patch, MagicMock
from game.Cards import *
from game.Card import *
from game.Player import Player
from game.Ante import Ante

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

class TestCopperCard(unittest.TestCase):
    def setUp(self):
        self.game = MagicMock()
        self.player = Player(10)
        self.player.flight.goods = 1
        self.player.flight.cards = [MagicMock(), MagicMock()]
        self.player.cardCount = 2
        self.ai_player = MagicMock()

    @patch("builtins.input", return_value="Gold 5")
    def test_copper_card_power(self, mock_input):
        card = CopperCard(Value(3))
        card.power(self.player, self.game)

        # Check if the card power was called correctly
        self.assertTrue(mock_input.called)
        self.assertEqual(self.player.cardCount, 4)

class TestBronzeCard(unittest.TestCase):
    def setUp(self):
        self.game = MagicMock()
        self.player = Player(10)
        self.player.cardCount = 2
        self.game.ante = Ante([GoldCard(Value(4)), RedCard(Value(3)), BlueCard(Value(2))])
        self.game.ante.cards[0].value = Value(4)
        self.game.ante.cards[1].value = Value(3)
        self.game.ante.cards[2].value = Value(2)

    def test_bronze_card_power(self):
        card = BronzeCard(Value(3))
        card.power(self.player, self.game)

        # Check if the player received the correct number of cards
        self.assertEqual(self.player.cardCount, 4)
        self.assertEqual(len(self.game.ante.cards), 1)
        self.assertEqual(self.game.ante.cards[0].value, Value(4))

class TestBrassCard(unittest.TestCase):
    def setUp(self):
        self.game = MagicMock()
        self.player = Player(10)
        self.player.cardCount = 2
        self.game.AIPlayer = AIPlayer(10, [GreenCard(Value(7)), BronzeCard(Value(5)), RedCard(Value(1))])

    def test_brass_card_power_to_AI(self):
        self.game.players = [self.player, MagicMock()]
        card = BrassCard(Value(3))
        card.power(self.player, self.game)

        # Check if the player received the correct number of cards
        self.assertEqual(self.player.cardCount, 3)
        self.assertEqual(len(self.game.AIPlayer.cards), 2)
        self.assertFalse(any(isinstance(card, BronzeCard) and card.value == Value(5) for card in self.game.AIPlayer.cards))
    
    @patch("builtins.input", return_value="Y")
    def test_brass_card_power_to_player(self, mock_input):
        self.game.players = [MagicMock(), self.player]
        self.game.players[0].cardCount = 4
        card = BrassCard(Value(3))
        card.power(self.player, self.game)

        # Check if the player received the correct number of cards
        self.assertTrue(mock_input.called)
        self.assertEqual(self.player.cardCount, 3)
        self.assertEqual(self.game.players[0].cardCount, 3)
    
    @patch("builtins.input", side_effect=["Y", "Red 7"])
    def test_brass_card_power_from_AI(self, mock_input):
        self.game.players = [MagicMock(), self.player]
        card = BrassCard(Value(3))
        card.power(self.game.AIPlayer, self.game)

        # Check if the player received the correct number of cards
        self.assertTrue(mock_input.called)
        self.assertEqual(self.player.cardCount, 1)
        self.assertEqual(len(self.game.AIPlayer.cards), 4)
        self.assertTrue(any(isinstance(card, RedCard) and card.value == Value(7) for card in self.game.AIPlayer.cards))

# class TestRedCard(unittest.TestCase):
#     def setUp(self):
#         self.game = MagicMock()
#         self.player = Player(10)
#         self.game.players = [MagicMock(), MagicMock()]
#         self.game.players[0].flight.total = 5
#         self.game.players[1].flight.total = 3
#         self.game.AIPlayer = MagicMock()
#         self.game.AIPlayer.flight.total = 4

#     @patch("builtins.input", side_effect=["0", "Gold 5"])
#     def test_red_card_power(self, mock_input):
#         card = RedCard(Value(3))
#         card.power(self.player, self.game)

#         # Check if the player received the correct number of cards
#         self.assertTrue(mock_input.called)

# class TestBlackCard(unittest.TestCase):
#     def setUp(self):
#         self.game = MagicMock()
#         self.player = Player(10)
#         self.game.ante.value = 5

#     def test_black_card_power(self):
#         card = BlackCard(Value(3))
#         card.power(self.player, self.game)

#         # Check if the player received the correct amount of gold
#         self.assertEqual(self.player.gold, 13)

# class TestGreenCard(unittest.TestCase):
#     def setUp(self):
#         self.game = MagicMock()
#         self.player = Player(10)
#         self.game.players = [MagicMock(), MagicMock()]
#         self.game.players[0].flight.total = 5
#         self.game.players[1].flight.total = 3
#         self.game.AIPlayer = MagicMock()
#         self.game.AIPlayer.flight.total = 4

#     @patch("builtins.input", return_value="Gold 5")
#     def test_green_card_power(self, mock_input):
#         card = GreenCard(Value(3))
#         card.power(self.player, self.game)

#         # Check if the player received the correct number of cards
#         self.assertTrue(mock_input.called)

# class TestWhiteCard(unittest.TestCase):
#     def setUp(self):
#         self.game = MagicMock()
#         self.player = Player(10)
#         self.game.players = [MagicMock(), MagicMock()]
#         self.game.players[0].flight.total = 2
#         self.game.players[1].flight.total = 3
#         self.game.AIPlayer = MagicMock()
#         self.game.AIPlayer.flight.total = 1

#     @patch("builtins.input", return_value="0")
#     def test_white_card_power(self, mock_input):
#         card = WhiteCard(Value(3))
#         card.power(self.player, self.game)

#         # Check if the player received the correct amount of gold
#         self.assertEqual(self.player.gold, 12)

# class TestBlueCard(unittest.TestCase):
#     def setUp(self):
#         self.game = MagicMock()
#         self.player = Player(10)
#         self.game.players = [MagicMock(), MagicMock()]
#         self.game.players[0].gold = 10
#         self.game.players[1].gold = 10
#         self.game.AIPlayer = MagicMock()
#         self.game.AIPlayer.gold = 10

#     @patch("builtins.input", return_value="Y")
#     def test_blue_card_power(self, mock_input):
#         card = BlueCard(Value(3))
#         card.power(self.player, self.game)

#         # Check if the player received the correct amount of gold
#         self.assertTrue(mock_input.called)

if __name__ == "__main__":
    unittest.main()
