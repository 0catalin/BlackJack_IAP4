# Blackjack in Python - IA4 Project

The aim of this project is to implement a functional version of the popular card 
game `Blackjack` in a manner as close to the real-life version as possible. Although
a simple counterpart to the original, our game includes the most important features
and more:
- Ability to choose the number of decks and the initial balance
- Supports card counting! (The player is warned when the deck is running out and will be reshuffled)
- Multiple betting options
- Visuals for the current hands' scores
- Options to hit, stand and double down
- Custom statistics section
- Immersive sound effects and ambience

## Build details and instructions

The main modules that were used are **pygame** and **cryptography** (eventual
ceva detalieri aici). To start the game, simply run the `game.py` file in a 
***Windows*** system.

## Contribution

### Nicolescu Petre - 324CD

Implemented the gameplay section (most of what happens after the start of a new game).
Source files:
- gameplay.py: contains all the states of the game (rounds, betting state, game over screen)
- utils.py: some auxiliary functions used in the implementation
- game_logic.py: classes for cards, deck and players (hands)

### Oprea Andrei Catalin - 324CD

Implemented the main menu section, the personalized input and the statistics Class with its methods.
Source files:
- game.py: contains the main menu of the game
- button.py: contains the Button class with its logic and methods
- statistics.py : the methods for storing statistics cryptographically and the cases where something wrong happens

Difficulties:

- the adjustment of the screen's size while keeping the same proportions
- understanding while loops and how to place the elements on the screen
- the cryptographic encoding and decoding for the statistics
- searching for the right sound effects (and timing the sounds to the backend commands), backgrounds and overall design



