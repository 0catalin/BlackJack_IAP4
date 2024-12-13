import pygame, sys
from button import Button
from gameplay import Gameplay
pygame.init()


SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)  # Make window resizable
pygame.display.set_caption("BlackJack for everyone")


BG = pygame.image.load("assets/main_menu_background.jpg")
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
second_image = pygame.image.load("assets/Options Rect.png")

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def main():
    while True:

        screen_info = pygame.display.Info()
        current_width = screen_info.current_w
        current_height = screen_info.current_h

        SCREEN.blit(pygame.transform.scale(BG, (current_width, current_height)), (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()


        input_box = pygame.Rect(current_width * 0.137, current_height * 0.05, current_width * 0.725, current_height * 0.15)
        pygame.draw.rect(SCREEN, (0, 0, 0), input_box, 0)

        MENU_TEXT = get_font(int(current_width / 12.8)).render("MAIN MENU", True, "#FB773C")
        MENU_RECT = MENU_TEXT.get_rect(center=(current_width / 2, current_height * 0.14))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(current_width / 2, current_height * 0.35),
                             text_input="PLAY", font=get_font(int(current_width / 22)), base_color="#d7fcd4", hovering_color=(25, 51, 0))
        STATISTICS_BUTTON = Button(image=pygame.transform.scale(second_image, (int(current_width * 0.64), second_image.get_height())),
                                   pos=(current_width / 2, current_height * 0.55),
                                   text_input="STATISTICS", font=get_font(int(current_width / 22)), base_color="#d7fcd4", hovering_color=(25, 51, 0))
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(current_width / 2, current_height * 0.75),
                             text_input="QUIT", font=get_font(int(current_width / 22)), base_color="#d7fcd4", hovering_color=(25, 51, 0))

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, STATISTICS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if STATISTICS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    statistics()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()







def play():
    good_input = True

    input_text1 = ""  # This will store the user input
    input_text2 = ""
    error_message_1 = ""  # more than 100 decks! / input not a number!
    error_message_2 = ""  # initial balance too big! / low! / input not a number!

    while True:
        screen_info = pygame.display.Info()
        current_width = screen_info.current_w
        current_height = screen_info.current_h


        SCREEN.fill("white")
        SCREEN.blit(pygame.transform.scale(BG, (current_width, current_height)), (0, 0))

        PLAY_MOUSE_POS = pygame.mouse.get_pos()


        input_box = pygame.Rect(current_width * 0.1, current_height * 0.05, current_width * 0.8, current_height * 0.15)
        pygame.draw.rect(SCREEN, (0, 0, 0), input_box, 0)


        PLAY_TEXT = get_font(int(current_width / 25)).render("CHOOSE GAME SETTINGS", True, "#FB773C")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(current_width / 2, current_height * 0.14))


        text_surface = get_font(int(current_width / 60)).render("Number of decks of cards:", True, (255, 255, 255))
        text_position = (5, current_height * 0.35)
        SCREEN.blit(text_surface, text_position)

        text_surface = get_font(int(current_width / 60)).render("Total initial balance:", True, (255, 255, 255))
        text_position = (5, current_height * 0.5)
        SCREEN.blit(text_surface, text_position)


        text_surface = get_font(int(current_width / 100)).render(error_message_1, True, (255, 0, 0))
        text_position = (current_width * 0.43, current_height * 0.4)
        SCREEN.blit(text_surface, text_position)

        text_surface = get_font(int(current_width / 100)).render(error_message_2, True, (255, 0, 0))
        text_position = (current_width * 0.43, current_height * 0.54)
        SCREEN.blit(text_surface, text_position)


        input_box1 = pygame.Rect(current_width * 0.43, current_height * 0.33, current_width * 0.4, current_height * 0.07)
        input_box2 = pygame.Rect(current_width * 0.43, current_height * 0.47, current_width * 0.4, current_height * 0.07)
        

        pygame.draw.rect(SCREEN, (255, 0, 0) if error_message_1 else (0, 0, 0), input_box1, 2)
        pygame.draw.rect(SCREEN, (255, 0, 0) if error_message_2 else (0, 0, 0), input_box2, 2)


        input_text_surface = get_font(int(current_width / 60)).render(input_text1, True, (0, 0, 0))
        SCREEN.blit(input_text_surface, (input_box1.x + 5, input_box1.y + 5))
        
        input_text_surface = get_font(int(current_width / 60)).render(input_text2, True, (0, 0, 0))
        SCREEN.blit(input_text_surface, (input_box2.x + 5, input_box2.y + 5))


        BACK_BUTTON = Button(image=pygame.transform.scale(second_image, (int(current_width * 0.1), int(current_height * 0.05))),
                             pos=(75, 25), text_input="BACK", font=get_font(int(current_width / 60)),
                             base_color=(0, 0, 0), hovering_color=(25, 51, 0))


        SCREEN.blit(PLAY_TEXT, PLAY_RECT)


        for button in [BACK_BUTTON]:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                (good_input1, error_message_1) = custom_validation1(input_text1)
                (good_input2, error_message_2) = custom_validation2(input_text2)
                if good_input1 and good_input2:
                    gameplay(int(input_text1), int(input_text2))
                if not good_input1:
                    input_text1 = ""
                if not good_input2:
                    input_text2 = ""

            elif event.type == pygame.KEYDOWN:
                if input_box1.collidepoint(PLAY_MOUSE_POS):
                    if event.key == pygame.K_BACKSPACE:
                        input_text1 = input_text1[:-1]
                    else:
                        input_text1 += event.unicode
                elif input_box2.collidepoint(PLAY_MOUSE_POS):
                    if event.key == pygame.K_BACKSPACE:
                        input_text2 = input_text2[:-1]
                    else:
                        input_text2 += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    main()

        pygame.display.update()

## Esc, ALT + F4, maybe F11 for fullscreen

def statistics():
    i = 0

def gameplay(deck_number, initial_balance):
    gameplay = Gameplay(SCREEN, BG, deck_number, initial_balance)
    gameplay.loop()

def custom_validation1(input1):
    try:
        input1 = int(input1)
    except ValueError:
        return False, "input must be a number!"
    if input1 < 1:
        return False, "the deck number must be higher than 0!"
    if input1 > 100:
        return False, "the deck number must be less than 100!"
    return True, ""
    
def custom_validation2(input2):
    try:
        input2 = int(input2)
    except ValueError:
        return False, "input must be a number!"
    if input2 > 1000000:
        return False, "initial balance too big!"
    if input2 < 100:
        return False, "initial balance too low!"
    return True, ""
    

if __name__ == "__main__":
    main()