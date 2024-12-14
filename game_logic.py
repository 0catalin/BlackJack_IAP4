import random, pygame, sys

class Card:
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value
        self.image_path = "assets/card_assets/" + self.rank + "_of_" + self.suit
        if self.rank in ['jack', 'queen', 'king']:
            self.image_path = self.image_path + '2'
        self.image_path = self.image_path + ".png"

    def load_card_image(self):
        return pygame.image.load(self.image_path)

    def load_hidden_card(self):
        return pygame.image.load("assets/card_assets/back_of_card.png")

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self, pack_number):
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
                  'jack': 10, 'queen': 10, 'king': 10, 'ace': 11}
        single_deck = [Card(suit, rank, values[rank]) for suit in suits for rank in ranks]
        self.cards = single_deck * pack_number
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()


class Hand:
    def __init__(self, initial_sum):
        self.cards = []
        self.sum = initial_sum
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.value
        if card.rank == 'ace':
            self.aces += 1
        self.adjust_for_ace()

    def adjust_for_ace(self):
        while self.value > 21 and self.aces != 0:
            self.value -= 10
            self.aces -= 1

    def clear_hand(self):
        self.cards = []
        self.value = 0
        self.aces = 0
