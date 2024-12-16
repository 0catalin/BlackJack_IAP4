import pygame, sys, time
from button import Button
from game_logic import Card, Deck, Hand
from utils import get_font, draw_balance_box, place_chip, crt_h, crt_w
from statistics import Statistics

SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280

pygame.mixer.init()
quit_sound = pygame.mixer.Sound("sounds/quit_game.mp3")
button_click_sound = pygame.mixer.Sound("sounds/button.mp3")
default_rect = pygame.image.load("assets/Options Rect.png")
chip_drop_sound = pygame.mixer.Sound("sounds/chip.mp3")
all_in_sound = pygame.mixer.Sound("sounds/all_in.mp3")
flip_card = pygame.mixer.Sound("sounds/flip_card.mp3")
shuffle_cards = pygame.mixer.Sound("sounds/shuffle_cards.mp3")

class Gameplay():
    def __init__(self, screen, background, deck_number, initial_balance):
        self.background = background
        self.screen = screen
        self.deck_number = deck_number
        self.initial_balance = initial_balance
        self.deck = Deck(self.deck_number)
        self.player = Hand(self.initial_balance)
        self.dealer = Hand(0)
        # Variable for running the gameplay loop
        self.running = True
        # Variable for running a round
        self.round_running = True


    # Shows the given card face up.
    def show_card(self, card, position):
        card_image = card.load_card_image()
        card_image = pygame.transform.scale(card_image, (crt_w() / 10.2, crt_h() / 3.9))
        self.screen.blit(card_image, position)


    # Shows a face down card.
    def show_hidden_card(self, position):
        hidden_image = pygame.image.load("assets/card_assets/back_of_card.png")
        hidden_image = pygame.transform.scale(hidden_image, (crt_w() / 10.2, crt_h() / 3.9))
        self.screen.blit(hidden_image, position)


    # Shows hand normally.
    def show_hand(self, hand, start_x, start_y):
        x = start_x
        y = start_y
        for card in hand.cards:
            self.show_card(card, (x, y))
            x = x + crt_w() / 20.4


    # Shows hand with one card face down.
    def show_dealer_hand(self, hand, start_x, start_y):
        x = start_x
        y = start_y
        self.show_card(hand.cards[0], (x, y))
        self.show_hidden_card((x + crt_w() / 20.4, y))

    # Shows hand with all cards face down
    def show_hidden_hand(self, start_x, start_y):
        x = start_x
        y = start_y
        self.show_hidden_card((x, y))
        self.show_hidden_card((x + crt_w() / 20.4, y))

    # Checks score after a hit
    def check_score(self):
        if self.player.value > 21:
            self.game_end("BUST!")
        elif self.player.value == 21:
            self.dealer_turn()

    # Betting state
    def choose_bet(self):
        error = ""
        
        while(True):
            # Background
            self.screen.fill((255, 255, 255))
            self.screen.blit(pygame.transform.scale(self.background, (crt_w(), crt_h())), (0, 0))

            # Do not show hands to player yet
            self.show_hidden_hand(crt_w() / 2.4, crt_h() / 1.4)
            self.show_hidden_hand(crt_w() / 2.4, crt_h() / 16)

            # Show balance
            draw_balance_box(self.screen, self.player.sum)

            # Bet choice text
            BET_TEXT = get_font(int(crt_w() / 60)).render("CHOOSE YOUR BET:", True, (255,215,0))
            self.screen.blit(BET_TEXT, (crt_w() / 128, crt_h() / 2.9))

            # Betting options
            FIRST_BET = Button(image=pygame.transform.scale(default_rect, (int(crt_w() * 0.15), int(crt_h() * 0.05))),
                         pos=(crt_w() / 8.5, crt_h() / 2.4), text_input = str(int(self.initial_balance / 10)), font=get_font(int(crt_w() / 60)),
                         base_color = (255, 215, 0), hovering_color = (255, 140, 0))
            SECOND_BET = Button(image=pygame.transform.scale(default_rect, (int(crt_w() * 0.15), int(crt_h() * 0.05))),
                         pos=(crt_w() / 8.5, crt_h() / 2.4 + int(crt_w() * 0.045)), text_input = str(int(self.initial_balance / 100)), font=get_font(int(crt_w() / 60)),
                         base_color = (255, 215, 0), hovering_color = (255, 140, 0))
            THIRD_BET = Button(image=pygame.transform.scale(default_rect, (int(crt_w() * 0.15), int(crt_h() * 0.05))),
                         pos=(crt_w() / 8.5, crt_h() / 2.4 + int(crt_w() * 0.090)), text_input = str(int(self.initial_balance / 1000)), font=get_font(int(crt_w() / 60)),
                         base_color = (255, 215, 0), hovering_color = (255, 140, 0))
            FOURTH_BET = Button(image=pygame.transform.scale(default_rect, (int(crt_w() * 0.15), int(crt_h() * 0.05))),
                         pos=(crt_w() / 8.5, crt_h() / 2.4 + int(crt_w() * 0.135)), text_input = "ALL IN", font=get_font(int(crt_w() / 60)),
                         base_color = (255, 215, 0), hovering_color = (255, 140, 0))
            
            # Back button
            BACK_BUTTON = Button(image=pygame.transform.scale(default_rect, (int(crt_w() * 0.1), int(crt_h() * 0.05))),
                             pos=(75, 25), text_input="BACK", font=get_font(int(crt_w() / 60)),
                             base_color=(0, 0, 0), hovering_color=(25, 51, 0))

            # Betting error
            BET_ERROR = get_font(int(crt_w() / 80)).render(error, True, (255, 0, 0))
            self.screen.blit(BET_ERROR, (crt_w() / 128, crt_h() / 2.4 + crt_w() * 0.16))
            MOUSE_POS = pygame.mouse.get_pos()
            for button in [FIRST_BET, SECOND_BET, THIRD_BET, FOURTH_BET, BACK_BUTTON]:
                button.changeColor(MOUSE_POS)
                button.update(self.screen)

            # Update screen
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Manage the chosen bet
                    if FIRST_BET.checkForInput(MOUSE_POS):
                        button_click_sound.play()
                        time.sleep(0.3)
                        button_click_sound.stop()
                        if self.player.sum < self.initial_balance / 10:
                            error = "Not enough funds!"
                            continue
                        self.player.bet = self.initial_balance / 10
                        self.player.sum -= self.player.bet
                        return
                    elif SECOND_BET.checkForInput(MOUSE_POS):
                        button_click_sound.play()
                        time.sleep(0.3)
                        button_click_sound.stop()
                        if self.player.sum < self.initial_balance / 100:
                            error = "Not enough funds!"
                            continue
                        self.player.bet = self.initial_balance / 100
                        self.player.sum -= self.player.bet
                        return
                    elif THIRD_BET.checkForInput(MOUSE_POS):
                        button_click_sound.play()
                        time.sleep(0.3)
                        button_click_sound.stop()
                        if self.player.sum < self.initial_balance / 1000:
                            error = "Not enough funds!"
                            continue
                        self.player.bet = self.initial_balance / 1000
                        self.player.sum -= self.player.bet
                        return
                    elif FOURTH_BET.checkForInput(MOUSE_POS):
                        button_click_sound.play()
                        time.sleep(0.3)
                        button_click_sound.stop()
                        if self.player.sum == 0:
                            error = "Not enough funds!"
                            continue
                        self.player.bet = self.player.sum
                        self.player.sum = 0
                        return
                    elif BACK_BUTTON.checkForInput(MOUSE_POS):
                        # Update profit when exiting
                        statistics = Statistics()
                        statistics.profit += int(self.player.sum - self.initial_balance)
                        statistics.encryptMessageAndInsertIntoFile()
                        # Exit gameplay loop
                        self.round_running = False
                        self.running = False
                        return
                elif event.type == pygame.QUIT:
                    statistics = Statistics()
                    statistics.profit += int(self.player.sum - self.initial_balance)
                    statistics.encryptMessageAndInsertIntoFile()
                    quit_sound.play()
                    time.sleep(0.7)
                    pygame.quit()
                    sys.exit()

            
    # Primary gameplay loop
    def loop(self):
        # Runs only if running is true (this variable is set to false when exiting)
        while(self.running):
            # Clear hands
            self.player.clear_hand()
            self.dealer.clear_hand()

            self.screen.fill((255, 255, 255))
            self.screen.blit(pygame.transform.scale(self.background, (crt_w(), crt_h())), (0, 0))
            pygame.display.update()
            # Deal cards
            self.player.add_card(self.deck.deal())
            self.player.add_card(self.deck.deal())
            self.dealer.add_card(self.deck.deal())
            self.dealer.add_card(self.deck.deal())
            self.round_running = True
            # Betting state
            self.choose_bet()
            double_error = ""
            empty_error = "Running out! Reshuffling..."
            place_chip_once_sound = True
            flip_cards = True
            while(self.round_running):
                double_check = True
                # Reshuffle if deck is running out
                if len(self.deck.cards) < 15:
                    self.deck = Deck(self.deck_number)
                    shuffle_cards.play()
                    EMPTY_TEXT = get_font(int(crt_w() / 70)).render(empty_error, True, (255, 0, 0))
                    self.screen.blit(EMPTY_TEXT, (crt_w() / 1.6, crt_h() / 40))
                    pygame.display.flip()
                    time.sleep(1)
                    shuffle_cards.stop()
                    time.sleep(0.2)

                self.screen.fill((255, 255, 255))
                self.screen.blit(pygame.transform.scale(self.background, (crt_w(), crt_h())), (0, 0))
                # Show hands
                self.show_hand(self.player, crt_w() / 2.4, crt_h() / 1.4)
                self.show_dealer_hand(self.dealer, crt_w() / 2.4, crt_h() / 16)

                draw_balance_box(self.screen, self.player.sum)
                place_chip(self.screen, self.player.bet)
                # Show current scores of hands
                SCORE_TEXT = get_font(int(crt_w() / 70)).render("PLAYER: " + str(self.player.value), True, (255, 215, 0))
                self.screen.blit(SCORE_TEXT, (crt_w() / 4, crt_h() / 1.1))
                SCORE_TEXT = get_font(int(crt_w() / 70)).render("DEALER: " + str(self.dealer.cards[0].value), True, (255, 0, 0))
                self.screen.blit(SCORE_TEXT, (crt_w() / 4, crt_h() / 17))

                # Ensures that the sound is only played once and that the right sound is played
                if place_chip_once_sound and self.player.sum != 0:
                    chip_drop_sound.play()
                    place_chip_once_sound = False
                elif place_chip_once_sound: 
                    all_in_sound.play()
                    place_chip_once_sound = False
                # PLay flipping sounds once
                if flip_cards:
                    flip_card.play()
                    time.sleep(0.2)
                    flip_card.play()
                    time.sleep(0.2)
                    flip_card.play()
                    time.sleep(0.2)
                    flip_cards = False

                # Options 
                BACK_BUTTON = Button(image=pygame.transform.scale(default_rect, (int(crt_w() * 0.1), int(crt_h() * 0.05))),
                                pos=(75, 25), text_input="BACK", font=get_font(int(crt_w() / 60)),
                                base_color=(0, 0, 0), hovering_color=(25, 51, 0))

                HIT_BUTTON = Button(image=pygame.transform.scale(default_rect, (crt_w() / 8.5, crt_h() / 7.5)),
                                pos=(crt_w() / 1.1, crt_h() / 1.6), text_input="HIT", font=get_font(int(crt_w() / 50)),
                                base_color=(0, 0, 0), hovering_color=(255, 215, 0))

                STAND_BUTTON = Button(image=pygame.transform.scale(default_rect, (crt_w() / 8.5, crt_h() / 7.5)),
                                pos=(crt_w() / 1.1, crt_h() / 1.2), text_input="STAND", font=get_font(int(crt_w() / 50)),
                                base_color=(0, 0, 0), hovering_color=(255, 69, 0))

                DOUBLE_BUTTON = Button(image=pygame.transform.scale(default_rect, (crt_w() / 8.5, crt_h() / 7.5)),
                                pos=(crt_w() / 1.1, crt_h() * 0.41), text_input="DOUBLE", font=get_font(int(crt_w() / 50)),
                                base_color=(0, 0, 0), hovering_color=(0,0,205))

                DOUBLE_ERROR = get_font(int(crt_w() / 80)).render(double_error, True, (255, 0, 0))
                self.screen.blit(DOUBLE_ERROR, (crt_w() / 1.25, crt_h() / 2))
                MOUSE_POS = pygame.mouse.get_pos()
                for button in [HIT_BUTTON, STAND_BUTTON, BACK_BUTTON, DOUBLE_BUTTON]:
                    button.changeColor(MOUSE_POS)
                    button.update(self.screen)
                
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if BACK_BUTTON.checkForInput(MOUSE_POS):
                            # Update profit and exit
                            statistics = Statistics()
                            statistics.profit += int(self.player.sum - self.initial_balance)
                            statistics.encryptMessageAndInsertIntoFile()
                            self.round_running = False
                            self.running = False
                            return
                        elif HIT_BUTTON.checkForInput(MOUSE_POS):
                            button_click_sound.play()
                            time.sleep(0.3)
                            button_click_sound.stop()
                            # Add card on hit
                            self.player.add_card(self.deck.deal())
                            double_error = ""
                        elif STAND_BUTTON.checkForInput(MOUSE_POS):
                            button_click_sound.play()
                            time.sleep(0.3)
                            button_click_sound.stop()

                            double_error = ""
                            # Skip to dealer turn
                            self.dealer_turn()
                            break
                        elif DOUBLE_BUTTON.checkForInput(MOUSE_POS):
                            button_click_sound.play()
                            time.sleep(0.3)
                            button_click_sound.stop()
                            # Check for double error
                            if self.player.sum < self.player.bet:
                                double_error = "Cannot double!"
                                continue
                            # Add card and double bet
                            self.player.add_card(self.deck.deal())
                            self.player.sum -= self.player.bet
                            self.player.bet *= 2
                            # Sound for double case when you end up spending all after a double
                            if self.player.sum != 0:
                                chip_drop_sound.play()
                            else: 
                                all_in_sound.play()
                            # Check cases for double
                            if self.player.value > 21:
                                self.game_end("BUST!")
                            else:
                                self.dealer_turn()
                            double_check = False
                            break
                    elif event.type == pygame.QUIT:
                        # Update profit
                        statistics = Statistics()
                        statistics.profit += int(self.player.sum - self.initial_balance)
                        statistics.encryptMessageAndInsertIntoFile()
                        quit_sound.play()
                        time.sleep(0.7)
                        pygame.quit()
                        sys.exit()
                # Do not perform check twice for double, only performed for hit
                if (double_check):
                    self.check_score()
                else:
                    double_check = True
                    
                
            

    # Game over window
    def game_end(self, text):
        break_time = True
        # Update statistics
        statistics = Statistics()
        statistics.total_games += 1
        match text:
            case "BUST!":
                statistics.total_losses += 1
            case "BLACKJACK!":
                statistics.total_blackjacks += 1
                statistics.total_wins += 1 
            case "PLAYER WON!":
                statistics.total_wins += 1
            case "DEALER WON!":
                statistics.total_losses += 1
        statistics.encryptMessageAndInsertIntoFile()
                    
        while(True):
            # Keep background and cards on table
            self.screen.blit(pygame.transform.scale(self.background, (crt_w(), crt_h())), (0, 0))
            self.show_hand(self.player, crt_w() / 2.4, crt_h() / 1.4)
            self.show_hand(self.dealer, crt_w() / 2.4, crt_h() / 16)

            draw_balance_box(self.screen, self.player.sum)
            place_chip(self.screen, self.player.bet)

            SCORE_TEXT = get_font(int(crt_w() / 70)).render("PLAYER: " + str(self.player.value), True, (255, 215, 0))
            self.screen.blit(SCORE_TEXT, (crt_w() / 4, crt_h() / 1.1))
            SCORE_TEXT = get_font(int(crt_w() / 70)).render("DEALER: " + str(self.dealer.value), True, (255, 0, 0))
            self.screen.blit(SCORE_TEXT, (crt_w() / 4, crt_h() / 17))
            # Before showing the result, sleep the table once so
            # that the window doesn't appear instantly
            if (break_time):
                pygame.display.flip()
                time.sleep(0.7)
                break_time = False

            # Round over window
            pygame.draw.rect(self.screen, (0, 0, 0), (crt_w() / 4.5, crt_h() / 4.5, crt_w() / 1.8, crt_h() / 1.8))
            OVER_TEXT = get_font(int(crt_w() / 34)).render("ROUND OVER", True, "#FB773C")
            self.screen.blit(OVER_TEXT, (crt_w() / 2.7, crt_h() / 4))
            RESULT_TEXT = get_font(int(crt_w() / 34)).render(text, True, "#FB773C")
            result_position = (0, 0)

            # Decide result of round
            match text:
                case "BUST!":
                    result_position = (crt_w() / 2.3, crt_h() / 3.2)
                case "BLACKJACK!":
                    result_position = (crt_w() / 2.6, crt_h() / 3.2)
                case "PLAYER WON!":
                    result_position = (crt_w() / 2.8, crt_h() / 3.2)
                case "DEALER WON!":
                    result_position = (crt_w() / 2.7, crt_h() / 3.2)
                case "DRAW!":
                    result_position = (crt_w() / 2.3, crt_h() / 3.2)

            self.screen.blit(RESULT_TEXT, result_position)
                
            # Option buttons
            NEXT_ROUND_BUTTON = Button(image=pygame.transform.scale(default_rect, (int(crt_w() * 0.2), int(crt_h() * 0.1))),
                             pos=(crt_w() / 2, crt_h() / 2), text_input="NEXT_ROUND", font=get_font(int(crt_w() / 60)),
                             base_color=(255, 215, 0), hovering_color=(255, 140, 0))
            EXIT_BUTTON = Button(image=pygame.transform.scale(default_rect, (int(crt_w() * 0.2), int(crt_h() * 0.1))),
                             pos=(crt_w() / 2, crt_h() / 1.6), text_input="EXIT", font=get_font(int(crt_w() / 60)),
                             base_color=(255, 215, 0), hovering_color=(255, 140, 0))
            MOUSE_POS = pygame.mouse.get_pos()
            for button in [NEXT_ROUND_BUTTON, EXIT_BUTTON]:
                button.changeColor(MOUSE_POS)
                button.update(self.screen)

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if NEXT_ROUND_BUTTON.checkForInput(MOUSE_POS):
                        button_click_sound.play()
                        time.sleep(0.3)
                        button_click_sound.stop()
                        # Update balance for each outcome
                        match text:
                            case "BLACKJACK!":
                                self.player.sum += 2.5 * self.player.bet
                            case "DRAW!":
                                self.player.sum += self.player.bet
                            case "PLAYER WON!":
                                self.player.sum += 2 * self.player.bet
                        # Only exit the current round loop, stay in the gameplay loop
                        self.round_running = False
                        return
                    elif EXIT_BUTTON.checkForInput(MOUSE_POS):
                        match text:
                            case "BLACKJACK!":
                                self.player.sum += 2.5 * self.player.bet
                            case "DRAW!":
                                self.player.sum += self.player.bet
                            case "PLAYER WON!":
                                self.player.sum += 2 * self.player.bet
                        statistics = Statistics()
                        statistics.profit += int(self.player.sum - self.initial_balance)
                        statistics.encryptMessageAndInsertIntoFile()
                        # Exit gameplay loop
                        self.round_running = False
                        self.running = False
                        return
                elif event.type == pygame.QUIT:
                    statistics = Statistics()
                    statistics.profit += int(self.player.sum - self.initial_balance)
                    statistics.encryptMessageAndInsertIntoFile()
                    quit_sound.play()
                    time.sleep(0.7)
                    pygame.quit()
                    sys.exit()

    # Dealer's turn
    def dealer_turn(self):
        flip_card.play()
        time.sleep(0.2)
        # Slowly draw cards until 17 is reached
        while(self.dealer.value <= 16 and not (self.player.value == 21 and len(self.player.cards) == 2)):
            self.screen.blit(pygame.transform.scale(self.background, (crt_w(), crt_h())), (0, 0))

            self.show_hand(self.player, crt_w() / 2.4, crt_h() / 1.4)
            self.show_hand(self.dealer, crt_w() / 2.4, crt_h() / 16)
            
            draw_balance_box(self.screen, self.player.sum)
            place_chip(self.screen, self.player.bet)

            SCORE_TEXT = get_font(int(crt_w() / 70)).render("PLAYER: " + str(self.player.value), True, (255, 215, 0))
            self.screen.blit(SCORE_TEXT, (crt_w() / 4, crt_h() / 1.1))
            SCORE_TEXT = get_font(int(crt_w() / 70)).render("DEALER: " + str(self.dealer.value), True, (255, 0, 0))
            self.screen.blit(SCORE_TEXT, (crt_w() / 4, crt_h() / 17))

            pygame.display.flip()
            time.sleep(1)
            self.dealer.add_card(self.deck.deal())
        
        # Call the game_end function with the proper outcome    
        if (self.dealer.value > self.player.value and self.dealer.value <= 21):
            self.game_end("DEALER WON!")
        elif (self.dealer.value < self.player.value or self.dealer.value > 21):
            if (self.player.value == 21 and len(self.player.cards) == 2):
                self.game_end("BLACKJACK!")
            else:
                self.game_end("PLAYER WON!")
        elif (self.dealer.value == self.player.value):
            if (self.player.value == 21 and len(self.player.cards) == 2 and len(self.dealer.cards) > 2):
                self.game_end("BLACKJACK!")
            elif (self.player.value == 21 and len(self.dealer.cards) == 2 and len(self.player.cards) > 2):
                self.game_end("DEALER WON!")
            else:
                self.game_end("DRAW!")
        return
        

