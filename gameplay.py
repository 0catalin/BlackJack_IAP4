import pygame, sys, time
from button import Button
from game_logic import Card, Deck, Hand
from utils import get_font

SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280
PLAYER_X = 525
PLAYER_Y = 500
DEALER_X = 525
DEALER_Y = 75

default_rect = pygame.image.load("assets/Options Rect.png")

class Gameplay():
    def __init__(self, screen, background, deck_number, initial_balance):
        self.background = background
        self.screen = screen
        self.deck_number = deck_number
        self.initial_balance = initial_balance
        self.deck = Deck(self.deck_number)
        self.player = Hand(self.initial_balance)
        self.dealer = Hand(0)

    def show_card(self, card, position):
        card_image = card.load_card_image()
        card_image = pygame.transform.scale(card_image, (125, 181))
        self.screen.blit(card_image, position)

    def show_hidden_card(self, position):
        hidden_image = pygame.image.load("assets/card_assets/back_of_card.png")
        hidden_image = pygame.transform.scale(hidden_image, (125, 181))
        self.screen.blit(hidden_image, position)

    def show_hand(self, hand, start_x, start_y):
        x = start_x
        y = start_y
        for card in hand.cards:
            self.show_card(card, (x, y))
            x = x + 50

    def show_dealer_hand(self, hand, start_x, start_y):
        x = start_x
        y = start_y
        self.show_card(hand.cards[0], (x, y))
        self.show_hidden_card((x + 50, y))

    def check_score(self):
        if self.player.value > 21:
            self.game_end("BUST!")
        elif self.player.value == 21:
            self.game_end("BLACKJACK!")

    def loop(self):
        print("time to work")
        deck = self.deck
        player = self.player
        dealer = self.dealer
        player.clear_hand()
        dealer.clear_hand()
        player.add_card(deck.deal())
        player.add_card(deck.deal())
        dealer.add_card(deck.deal())
        dealer.add_card(deck.deal())

        while(True):
            screen_info = pygame.display.Info()
            current_width = screen_info.current_w
            current_height = screen_info.current_h
            self.screen.fill((255, 255, 255))
            self.screen.blit(pygame.transform.scale(self.background, (current_width, current_height)), (0, 0))

            self.show_hand(player, PLAYER_X, PLAYER_Y)
            self.show_dealer_hand(dealer, DEALER_X, DEALER_Y)
        
            PAUSE_BUTTON = Button(image=pygame.transform.scale(default_rect, (int(current_width * 0.1), int(current_height * 0.05))),
                             pos=(75, 25), text_input="RETURN", font=get_font(int(current_width / 60)),
                             base_color=(0, 0, 0), hovering_color=(25, 51, 0))

            HIT_BUTTON = Button(image=pygame.transform.scale(default_rect, (150, 100)),
                             pos=(1100, 450), text_input="HIT", font=get_font(int(current_width / 50)),
                             base_color=(0, 0, 0), hovering_color=(255, 215, 0))

            STAND_BUTTON = Button(image=pygame.transform.scale(default_rect, (150, 100)),
                             pos=(1100, 575), text_input="STAND", font=get_font(int(current_width / 50)),
                             base_color=(0, 0, 0), hovering_color=(255, 69, 0))

            
            MOUSE_POS = pygame.mouse.get_pos()
            PAUSE_BUTTON.changeColor(MOUSE_POS)
            PAUSE_BUTTON.update(self.screen)

            for button in [HIT_BUTTON, STAND_BUTTON]:
                button.changeColor(MOUSE_POS)
                button.update(self.screen)
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PAUSE_BUTTON.checkForInput(MOUSE_POS):
                        from game import main
                        main()
                    elif HIT_BUTTON.checkForInput(MOUSE_POS):
                        player.add_card(deck.deal())
                    elif STAND_BUTTON.checkForInput(MOUSE_POS):
                        self.dealer_turn()
            self.check_score()


    def game_end(self, text):
        break_time = True
        while(True):

            screen_info = pygame.display.Info()
            current_width = screen_info.current_w
            current_height = screen_info.current_h

            # Keep background and cards on table
            self.screen.blit(pygame.transform.scale(self.background, (current_width, current_height)), (0, 0))
            self.show_hand(self.player, PLAYER_X, PLAYER_Y)
            self.show_hand(self.dealer, DEALER_X, DEALER_Y)

            # Before showing the result, sleep the table once so
            # that the window doesn't appear instantly
            if (break_time):
                pygame.display.flip()
                time.sleep(1)
                break_time = False

            # Round over window
            pygame.draw.rect(self.screen, (0, 0, 0), (290, 160, 700, 400))
            OVER_TEXT = get_font(int(current_width / 34)).render("ROUND OVER", True, "#FB773C")
            self.screen.blit(OVER_TEXT, (460, 180))
            RESULT_TEXT = get_font(int(current_width / 34)).render(text, True, "#FB773C")
            result_position = (0, 0)

            # Decide result of round
            match text:
                case "BUST!":
                    result_position = (550, 225)
                case "BLACKJACK!":
                    result_position = (475, 225)
                case "PLAYER WON!":
                    result_position = (450, 225)
                case "DEALER WON!":
                    result_position = (450, 225)

            self.screen.blit(RESULT_TEXT, result_position)
                
            # Option buttons
            NEXT_ROUND_BUTTON = Button(image=pygame.transform.scale(default_rect, (int(current_width * 0.2), int(current_height * 0.1))),
                             pos=(640, 350), text_input="NEXT_ROUND", font=get_font(int(current_width / 60)),
                             base_color=(255, 215, 0), hovering_color=(255, 140, 0))
            QUIT_BUTTON = Button(image=pygame.transform.scale(default_rect, (int(current_width * 0.2), int(current_height * 0.1))),
                             pos=(640, 450), text_input="QUIT", font=get_font(int(current_width / 60)),
                             base_color=(255, 215, 0), hovering_color=(255, 140, 0))

            MOUSE_POS = pygame.mouse.get_pos()
            for button in [NEXT_ROUND_BUTTON, QUIT_BUTTON]:
                button.changeColor(MOUSE_POS)
                button.update(self.screen)

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if NEXT_ROUND_BUTTON.checkForInput(MOUSE_POS):
                        self.loop()
                    elif QUIT_BUTTON.checkForInput(MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            
    def dealer_turn(self):
        while(self.dealer.value <= 16):
            screen_info = pygame.display.Info()
            current_width = screen_info.current_w
            current_height = screen_info.current_h
            self.screen.blit(pygame.transform.scale(self.background, (current_width, current_height)), (0, 0))

            self.show_hand(self.player, PLAYER_X, PLAYER_Y)
            self.show_hand(self.dealer, DEALER_X, DEALER_Y)
            
            MOUSE_POS = pygame.mouse.get_pos()

            pygame.display.flip()
            time.sleep(1)
            self.dealer.add_card(self.deck.deal())
        if (self.dealer.value >= self.player.value and self.dealer.value <= 21):
            self.game_end("DEALER WON!")
        else:
            self.game_end("PLAYER WON!")
        

