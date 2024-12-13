import pygame, sys
from button import Button

pygame.init()
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))     # change if they are too big, just a reminder to change here
pygame.display.set_caption("BlackJack for everyone")
BG = pygame.image.load("assets/Background.png")

second_image = pygame.image.load("assets/Options Rect.png")


def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="Red")
        STATISTICS_BUTTON = Button(image=pygame.transform.scale(second_image, (820, second_image.get_height())), pos=(640, 400), 
                            text_input="STATISTICS", font=get_font(75), base_color="#d7fcd4", hovering_color="Red")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="Red")

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
    error_message_1 = ""                                   #   more than 100 decks! / input not a number!
    error_message_2 = ""                                   #   initial balance too big! / low! / input not a number!
    
    while True:

   
        SCREEN.blit(BG, (0, 0))

        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("white")

        PLAY_TEXT = get_font(50).render("CHOOSE GAME SETTINGS", True, "#b68f40")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 100))


        text_surface = get_font(10).render("number of decks of cards:  total initial balance:", True, (0, 0, 0))  # Text, anti-aliasing, color
        text_position = (425, 225)
        SCREEN.blit(text_surface, text_position)

        text_surface = get_font(10).render(error_message_1, True, (255, 0, 0))
        text_position = (450, 310)
        SCREEN.blit(text_surface, text_position)

        text_surface = get_font(10).render(error_message_2, True, (255, 0, 0))
        text_position = (700, 310)
        SCREEN.blit(text_surface, text_position)

        

        
        input_box1 = pygame.Rect(450, 250, 200, 50)
        input_box2 = pygame.Rect(700, 250, 200, 50)
        if error_message_1 == "":
            pygame.draw.rect(SCREEN, (0, 0, 0), input_box1, 2)
        else:
            pygame.draw.rect(SCREEN, (255, 0, 0), input_box1, 2)
        if error_message_2 == "":
            pygame.draw.rect(SCREEN, (0, 0, 0), input_box2, 2)
        else:
            pygame.draw.rect(SCREEN, (255, 0, 0), input_box2, 2)

            

        input_text_surface = get_font(15).render(input_text1, True, (0, 0, 0))
        SCREEN.blit(input_text_surface, (input_box1.x + 5, input_box1.y + 5))
        input_text_surface = get_font(15).render(input_text2, True, (0, 0, 0))
        SCREEN.blit(input_text_surface, (input_box2.x + 5, input_box2.y + 5))





        BACK_BUTTON = Button(image=pygame.transform.scale(second_image, (100, 50)), pos=(50, 25), 
                            text_input="back", font=get_font(20), base_color="#d7fcd4", hovering_color="Red")
        


        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        for button in [BACK_BUTTON]:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:


                #(good_input, error_message_1, error_message_2) = custom_validation(input_text1, input_text2)
                #if good_input:
                #    gameplay(int(input_text1), int(input_text2))
                (good_input1, error_message_1) = custom_validation1(input_text1)
                (good_input2, error_message_2) = custom_validation2(input_text2)
                if good_input1 and good_input2:
                    gameplay(int(input_text1), int(input_text2))
                if not good_input1:
                    input_text1 = ""
                if not good_input2:
                    input_text2 = ""

            elif event.type == pygame.KEYDOWN and input_box1.collidepoint(PLAY_MOUSE_POS):
                if event.key == pygame.K_BACKSPACE:
                    input_text1 = input_text1[:-1]
                else:
                    input_text1 += event.unicode  # Add character to the input text
            elif event.type == pygame.KEYDOWN and input_box2.collidepoint(PLAY_MOUSE_POS):

                if event.key == pygame.K_BACKSPACE:
                    input_text2 = input_text2[:-1]
                else:
                    input_text2 += event.unicode






            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    main_menu()



        pygame.display.update()


def statistics():
    i = 0

def gameplay(input_text1, input_text2):
    print("petre can start")

def custom_validation1(input1):
    try:
        input1 = int(input1)
    except ValueError:
        return False, "input not a number!"
    if input1 < 1:
        return False, "less than 1 deck!"
    if input1 > 100:
        return False, "more than 100 decks!"
    return True, ""
    
def custom_validation2(input2):
    try:
        input2 = int(input2)
    except ValueError:
        return False, "input not a number!"
    if input2 > 1000000:
        return False, "initial balance too big!"
    if input2 < 100:
        return False, "initial balance too low!"
    return True, ""
    


main_menu()