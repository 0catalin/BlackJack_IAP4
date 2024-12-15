import pygame, sys, time
from button import Button
from game_logic import Card, Deck, Hand
from utils import get_font, draw_balance_box, place_chip, crt_h, crt_w

SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280

pygame.mixer.init()
quit_sound = pygame.mixer.Sound("sounds/quit_game.mp3")
button_click_sound = pygame.mixer.Sound("sounds/button.mp3")
default_rect = pygame.image.load("assets/Options Rect.png")
chip_drop_sound = pygame.mixer.Sound("sounds/chip.mp3")
all_in_sound = pygame.mixer.Sound("sounds/all_in.mp3")
flip_card = pygame.mixer.Sound("sounds/flip_card.mp3")

class Gameplay():
    def __init__(self, screen, background, deck_number, initial_balance):
        self.background = background
        self.screen = screen
        self.deck_number = deck_number
        self.initial_balance = initial_balance
        self.deck = Deck(self.deck_number)
        self.player = Hand(self.initial_balance)
        self.dealer = Hand(0)


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
            screen_info = pygame.display.Info()
            current_width = screen_info.current_w
            current_height = screen_info.current_h
            self.screen.fill((255, 255, 255))
            self.screen.blit(pygame.transform.scale(self.background, (current_width, current_height)), (0, 0))

            # Do not show hands to player yet
            self.show_hidden_hand(crt_w() / 2.4, crt_h() / 1.4)
            self.show_hidden_hand(crt_w() / 2.4, crt_h() / 16)

            draw_balance_box(self.screen, self.player.sum)

            BET_TEXT = get_font(int(current_width / 60)).render("CHOOSE YOUR BET:", True, (255,215,0))
            self.screen.blit(BET_TEXT, (crt_w() / 128, crt_h() / 2.9))

            FIRST_BET = Button(image=pygame.transform.scale(default_rect, (int(current_width * 0.15), int(current_height * 0.05))),
                         pos=(crt_w() / 8.5, crt_h() / 2.4), text_input = str(int(self.initial_balance / 10)), font=get_font(int(current_width / 60)),
                         base_color = (255, 215, 0), hovering_color = (255, 140, 0))
            SECOND_BET = Button(image=pygame.transform.scale(default_rect, (int(current_width * 0.15), int(current_height * 0.05))),
                         pos=(crt_w() / 8.5, crt_h() / 2.4 + int(current_width * 0.045)), text_input = str(int(self.initial_balance / 100)), font=get_font(int(current_width / 60)),
                         base_color = (255, 215, 0), hovering_color = (255, 140, 0))
            THIRD_BET = Button(image=pygame.transform.scale(default_rect, (int(current_width * 0.15), int(current_height * 0.05))),
                         pos=(crt_w() / 8.5, crt_h() / 2.4 + int(current_width * 0.090)), text_input = str(int(self.initial_balance / 1000)), font=get_font(int(current_width / 60)),
                         base_color = (255, 215, 0), hovering_color = (255, 140, 0))
            FOURTH_BET = Button(image=pygame.transform.scale(default_rect, (int(current_width * 0.15), int(current_height * 0.05))),
                         pos=(crt_w() / 8.5, crt_h() / 2.4 + int(current_width * 0.135)), text_input = "ALL IN", font=get_font(int(current_width / 60)),
                         base_color = (255, 215, 0), hovering_color = (255, 140, 0))
            BACK_BUTTON = Button(image=pygame.transform.scale(default_rect, (int(current_width * 0.1), int(current_height * 0.05))),
                             pos=(75, 25), text_input="BACK", font=get_font(int(current_width / 60)),
                             base_color=(0, 0, 0), hovering_color=(25, 51, 0))

            BET_ERROR = get_font(int(current_width / 80)).render(error, True, (255, 0, 0))
            self.screen.blit(BET_ERROR, (crt_w() / 128, crt_h() / 2.4 + crt_w() * 0.16))

            MOUSE_POS = pygame.mouse.get_pos()
            for button in [FIRST_BET, SECOND_BET, THIRD_BET, FOURTH_BET, BACK_BUTTON]:
                button.changeColor(MOUSE_POS)
                button.update(self.screen)

            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
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
                        from game import main
                        main()
                elif event.type == pygame.QUIT:
                    quit_sound.play()
                    time.sleep(0.7)
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    from game import main
                    main()

            

    def loop(self):
        print("time to work")
        player = self.player
        dealer = self.dealer
        player.clear_hand()
        dealer.clear_hand()

        screen_info = pygame.display.Info()
        current_width = screen_info.current_w
        current_height = screen_info.current_h
        self.screen.fill((255, 255, 255))
        self.screen.blit(pygame.transform.scale(self.background, (current_width, current_height)), (0, 0))
        pygame.display.update() # added those 5 lines to ensure that a background exists after the self.deck.deal sounds are played

        player.add_card(self.deck.deal())
        player.add_card(self.deck.deal())
        dealer.add_card(self.deck.deal())
        dealer.add_card(self.deck.deal())
        self.choose_bet()
        double_error = ""

        place_chip_once_sound = True
        flip_cards = True
        while(True):
            if len(self.deck.cards) < 15:
                print("running out...")
                self.deck = Deck(self.deck_number)
            screen_info = pygame.display.Info()
            current_width = screen_info.current_w
            current_height = screen_info.current_h
            self.screen.fill((255, 255, 255))
            self.screen.blit(pygame.transform.scale(self.background, (current_width, current_height)), (0, 0))

            self.show_hand(self.player, crt_w() / 2.4, crt_h() / 1.4)
            self.show_dealer_hand(self.dealer, crt_w() / 2.4, crt_h() / 16)

            draw_balance_box(self.screen, self.player.sum)
            place_chip(self.screen, self.player.bet)

            # ensures that the sound is only played once and that the right sound is played
            if place_chip_once_sound and self.player.sum != 0:
                chip_drop_sound.play()
                place_chip_once_sound = False
            elif place_chip_once_sound: 
                all_in_sound.play()
                place_chip_once_sound = False

            if flip_cards:
                flip_card.play()
                time.sleep(0.2)
                flip_card.play()
                time.sleep(0.2)
                flip_card.play()
                time.sleep(0.2)
                flip_cards = False


            BACK_BUTTON = Button(image=pygame.transform.scale(default_rect, (int(current_width * 0.1), int(current_height * 0.05))),
                             pos=(75, 25), text_input="BACK", font=get_font(int(current_width / 60)),
                             base_color=(0, 0, 0), hovering_color=(25, 51, 0))

            HIT_BUTTON = Button(image=pygame.transform.scale(default_rect, (crt_w() / 8.5, crt_h() / 7.5)),
                             pos=(crt_w() / 1.1, crt_h() / 1.6), text_input="HIT", font=get_font(int(current_width / 50)),
                             base_color=(0, 0, 0), hovering_color=(255, 215, 0))

            STAND_BUTTON = Button(image=pygame.transform.scale(default_rect, (crt_w() / 8.5, crt_h() / 7.5)),
                             pos=(crt_w() / 1.1, crt_h() / 1.2), text_input="STAND", font=get_font(int(current_width / 50)),
                             base_color=(0, 0, 0), hovering_color=(255, 69, 0))

            DOUBLE_BUTTON = Button(image=pygame.transform.scale(default_rect, (crt_w() / 8.5, crt_h() / 7.5)),
                             pos=(crt_w() / 1.1, crt_h() * 0.41), text_input="DOUBLE", font=get_font(int(current_width / 50)),
                             base_color=(0, 0, 0), hovering_color=(0,0,205))

            DOUBLE_ERROR = get_font(int(current_width / 80)).render(double_error, True, (255, 0, 0))
            self.screen.blit(DOUBLE_ERROR, (crt_w() / 1.25, crt_h() / 2))
            
            MOUSE_POS = pygame.mouse.get_pos()

            for button in [HIT_BUTTON, STAND_BUTTON, BACK_BUTTON, DOUBLE_BUTTON]:
                button.changeColor(MOUSE_POS)
                button.update(self.screen)
            
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_BUTTON.checkForInput(MOUSE_POS):
                        from game import main
                        main()
                    elif HIT_BUTTON.checkForInput(MOUSE_POS):
                        button_click_sound.play()
                        time.sleep(0.3)
                        button_click_sound.stop()
                        player.add_card(self.deck.deal())
                    elif STAND_BUTTON.checkForInput(MOUSE_POS):
                        button_click_sound.play()
                        time.sleep(0.3)
                        button_click_sound.stop()
                        self.dealer_turn()
                    elif DOUBLE_BUTTON.checkForInput(MOUSE_POS):
                        button_click_sound.play()
                        time.sleep(0.3)
                        button_click_sound.stop()
                        if player.sum < player.bet:
                            double_error = "Cannot double!"
                            continue
                        player.add_card(self.deck.deal())
                        player.sum -= player.bet
                        player.bet *= 2

                        # sound for double case when you end up spending all after a double
                        if player.sum != 0:
                            chip_drop_sound.play()
                        else: 
                            all_in_sound.play()

                        self.check_score()
                        self.dealer_turn()
                elif event.type == pygame.QUIT:
                    quit_sound.play()
                    time.sleep(0.7)
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    from game import main
                    main()
            self.check_score()


    def game_end(self, text):
        break_time = True
        while(True):

            screen_info = pygame.display.Info()
            current_width = screen_info.current_w
            current_height = screen_info.current_h

            # Keep background and cards on table
            self.screen.blit(pygame.transform.scale(self.background, (current_width, current_height)), (0, 0))
            self.show_hand(self.player, crt_w() / 2.4, crt_h() / 1.4)
            self.show_hand(self.dealer, crt_w() / 2.4, crt_h() / 16)
            draw_balance_box(self.screen, self.player.sum)
            place_chip(self.screen, self.player.bet)
            # Before showing the result, sleep the table once so
            # that the window doesn't appear instantly
            if (break_time):
                pygame.display.flip()
                time.sleep(0.7)
                break_time = False

            # Round over window
            pygame.draw.rect(self.screen, (0, 0, 0), (crt_w() / 4.5, crt_h() / 4.5, crt_w() / 1.8, crt_h() / 1.8))
            OVER_TEXT = get_font(int(current_width / 34)).render("ROUND OVER", True, "#FB773C")
            self.screen.blit(OVER_TEXT, (crt_w() / 2.7, crt_h() / 4))
            RESULT_TEXT = get_font(int(current_width / 34)).render(text, True, "#FB773C")
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
            NEXT_ROUND_BUTTON = Button(image=pygame.transform.scale(default_rect, (int(current_width * 0.2), int(current_height * 0.1))),
                             pos=(crt_w() / 2, crt_h() / 2), text_input="NEXT_ROUND", font=get_font(int(current_width / 60)),
                             base_color=(255, 215, 0), hovering_color=(255, 140, 0))
            EXIT_BUTTON = Button(image=pygame.transform.scale(default_rect, (int(current_width * 0.2), int(current_height * 0.1))),
                             pos=(crt_w() / 2, crt_h() / 1.6), text_input="EXIT", font=get_font(int(current_width / 60)),
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
                        match text:
                            case "BLACKJACK!":
                                self.player.sum += 2.5 * self.player.bet
                            case "DRAW!":
                                self.player.sum += self.player.bet
                            case "PLAYER WON!":
                                self.player.sum += 2 * self.player.bet
                        self.loop()
                    elif EXIT_BUTTON.checkForInput(MOUSE_POS):
                        from game import main
                        main()
                elif event.type == pygame.QUIT:
                    quit_sound.play()
                    time.sleep(0.7)
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    from game import main
                    main()

            
    def dealer_turn(self):
        flip_card.play()
        time.sleep(0.2)
        while(self.dealer.value <= 16 and not (self.player.value == 21 and len(self.player.cards) == 2)):
            screen_info = pygame.display.Info()
            current_width = screen_info.current_w
            current_height = screen_info.current_h
            self.screen.blit(pygame.transform.scale(self.background, (current_width, current_height)), (0, 0))

            self.show_hand(self.player, crt_w() / 2.4, crt_h() / 1.4)
            self.show_hand(self.dealer, crt_w() / 2.4, crt_h() / 16)
            
            draw_balance_box(self.screen, self.player.sum)
            place_chip(self.screen, self.player.bet)
            MOUSE_POS = pygame.mouse.get_pos()

            pygame.display.flip()
            time.sleep(1)
            self.dealer.add_card(self.deck.deal())
        if (self.dealer.value > self.player.value and self.dealer.value <= 21):
            self.game_end("DEALER WON!")
        elif (self.dealer.value < self.player.value or self.dealer.value > 21):
            if (self.player.value == 21 and len(self.player.cards) == 2):
                self.game_end("BLACKJACK!")
            else:
                self.game_end("PLAYER WON!")
        elif (self.dealer.value == self.player.value):
            self.game_end("DRAW!")
        

