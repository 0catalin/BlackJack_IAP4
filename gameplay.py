from button import Button
from game_logic import Card, Deck, Hand


class Gameplay():
    def __init__(self, screen, background, deck_number, initial_balance):
        self.background = background
        self.screen = screen
        self.deck_number = deck_number
        self.initial_balance = initial_balance
    def loop(self):
        print("petre rocks")