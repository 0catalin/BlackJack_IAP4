# Blackjack in Python - IA4 Project
[GitHub Repo Link](https://github.com/0catalin/BlackJack_IAP4)

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

The main modules that were used are **pygame** and **cryptography**. To start the game, simply run:
```
pip install -r requirements.txt
python3 game.py
```
***Important!*** Do not run this command on **WSL**! Also be sure to have all required modules installed.

## Contribution

### Nicolescu Petre - 324CD

Implemented the gameplay section (most of what happens after the start of a new game).
Source files:
- gameplay.py: contains all the states of the game (rounds, betting state, game over screen)
- utils.py: some auxiliary functions used in the implementation
- game_logic.py: classes for cards, deck and players (hands)

Difficulties:

- failure to implement **Split** functionality during gameplay (too complex)
- properly spacing out objects and positioning text
- implementing return logic for the gameplay loops (to avoid stack overflow)
- treating all Blackjack outcomes correctly


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


## Credits
- Sounds provided by [Pixabay](https://pixabay.com)
- Playing card png's provided by [Google Code archive](https://code.google.com/archive/p/vector-playing-cards/wikis)



