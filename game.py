import pygame, sys
from button import Button
from gameplay import Gameplay
from cryptography.fernet import Fernet
import os, stat
from statistics import Statistics
import time
from utils import get_font, draw_balance_box, place_chip, crt_h, crt_w

# initialize pygame, mixer for sound effects and clock
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# create sound objects
button_click_sound = pygame.mixer.Sound("sounds/button.mp3")
quit_sound = pygame.mixer.Sound("sounds/quit_game.mp3")
rect_sound = pygame.mixer.Sound("sounds/click.mp3")
wrong_input_sound = pygame.mixer.Sound("sounds/wrong_input.mp3")

# set up constants and caption
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("BlackJack for everyone")

# loading and scaling background images
BG = pygame.image.load("assets/main_menu_background.jpg")
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

table_bg = pygame.image.load("assets/table_bg.jpg")
table_bg = pygame.transform.scale(table_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

second_image = pygame.image.load("assets/Options Rect.png")

# counter variable to prevent the button sound being played when the game is opened
counter = False


def main():
    # plays the main music infinitely
    pygame.mixer.music.load("sounds/background2.mp3")
    pygame.mixer.music.play(loops=-1)

     # prevents it from getting written accidentally, the key is unique
    os.chmod("secret.key", stat.S_IREAD)

    # to not play the sound when the game starts
    global counter
    if counter:
        button_click_sound.play()
        time.sleep(0.3)
        button_click_sound.stop()
    else:
        counter = True

    # get current height and width of screen
    initial_width = crt_w()
    initial_height = crt_h()

    # scale the bg to the height and width which are initially chosen for the game and load images
    BG_SCALED = pygame.transform.scale(BG, (initial_width, initial_height))
    play_button_image = pygame.image.load("assets/Play Rect.png")
    quit_button_image = pygame.image.load("assets/Quit Rect.png")

    # loop to always check elements
    while True:

        # get current width and height
        current_width = crt_w()
        current_height = crt_h()

        # blit the background to the previously calculated width and height
        SCREEN.blit(pygame.transform.scale(BG, (current_width, current_height)), (0, 0))

        # get mouse position
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # create rectangle object and draw box for the menu text
        box = pygame.Rect(current_width * 0.137, current_height * 0.05, current_width * 0.725, current_height * 0.15)
        pygame.draw.rect(SCREEN, (0, 0, 0), box, 0)

        # create menu text and blit it in the box
        MENU_TEXT = get_font(int(current_width / 12.8)).render("MAIN MENU", True, "#FB773C")
        MENU_RECT = MENU_TEXT.get_rect(center=(current_width / 2, current_height * 0.14))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # create buttons
        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(current_width / 2, current_height * 0.35),
                             text_input="PLAY", font=get_font(int(current_width / 22)), base_color="#d7fcd4", hovering_color=(25, 51, 0))
        STATISTICS_BUTTON = Button(image=pygame.transform.scale(second_image, (int(current_width * 0.64), second_image.get_height())),
                                   pos=(current_width / 2, current_height * 0.55),
                                   text_input="STATISTICS", font=get_font(int(current_width / 22)), base_color="#d7fcd4", hovering_color=(25, 51, 0))
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(current_width / 2, current_height * 0.75),
                             text_input="QUIT", font=get_font(int(current_width / 22)), base_color="#d7fcd4", hovering_color=(25, 51, 0))


        # update buttons color depending on where the cursor is
        for button in [PLAY_BUTTON, STATISTICS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        # for each event
        for event in pygame.event.get():
            # if Esc or X are pressed quit app
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit_sound.play()
                time.sleep(0.7)
                pygame.quit()
                sys.exit()
            # if there are clicks on buttons redirects to other loops
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if STATISTICS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    statistics()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    quit_sound.play()
                    time.sleep(0.7)
                    pygame.quit()
                    sys.exit()
                
        # update screen and set frame rate to 60
        pygame.display.update()
        clock.tick(60)



def play():


    # play the clicking sound
    button_click_sound.play()
    time.sleep(0.3)
    button_click_sound.stop()

    # texts to store the inputs and their correspondent error messahes, plus some boolean conditions
    input_text1 = ""  # This will store the user input
    input_text2 = ""
    error_message_1 = ""
    error_message_2 = ""
    inputbox1_status = False
    inputbox2_status = False
    good_input = True

    # loop to always check elements
    while True:

        # get current height and width of screen
        current_width = crt_w()
        current_height = crt_h()

        # cover with white and transform background to current width and height
        SCREEN.fill("white")
        SCREEN.blit(pygame.transform.scale(BG, (current_width, current_height)), (0, 0))

        # get mouse position
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        # draws box for game settings text
        box = pygame.Rect(current_width * 0.1, current_height * 0.05, current_width * 0.8, current_height * 0.15)
        pygame.draw.rect(SCREEN, (0, 0, 0), box, 0)

        # places game settings text on screen in the box
        PLAY_TEXT = get_font(int(current_width / 25)).render("CHOOSE GAME SETTINGS", True, "#FB773C")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(current_width / 2, current_height * 0.13))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        # placing the texts on the screen
        PLAY_TEXT = get_font(int(current_width / 60)).render("Press ENTER when you are ready", True, (0, 0, 0))
        PLAY_RECT = PLAY_TEXT.get_rect(center=(current_width / 2, current_height * 0.65))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        text_surface = get_font(int(current_width / 60)).render("Number of decks of cards:", True, (255, 255, 255))
        text_position = (5, current_height * 0.35)
        SCREEN.blit(text_surface, text_position)

        text_surface = get_font(int(current_width / 60)).render("Total initial balance:", True, (255, 255, 255))
        text_position = (5, current_height * 0.5)
        SCREEN.blit(text_surface, text_position)

        # placing the text errors on the screen
        text_surface = get_font(int(current_width / 100)).render(error_message_1, True, (255, 0, 0))
        text_position = (current_width * 0.43, current_height * 0.4)
        SCREEN.blit(text_surface, text_position)

        text_surface = get_font(int(current_width / 100)).render(error_message_2, True, (255, 0, 0))
        text_position = (current_width * 0.43, current_height * 0.54)
        SCREEN.blit(text_surface, text_position)

        # creating input box rects
        input_box1 = pygame.Rect(current_width * 0.43, current_height * 0.33, current_width * 0.4, current_height * 0.07)
        input_box2 = pygame.Rect(current_width * 0.43, current_height * 0.47, current_width * 0.4, current_height * 0.07)
        
        # drawing input boxes with colour depending on state 
        pygame.draw.rect(SCREEN, 
                 (255, 255, 255) if inputbox1_status else (255, 0, 0) if error_message_1 else (0, 0, 0), 
                 input_box1,
                 5)
        pygame.draw.rect(SCREEN, 
                 (255, 255, 255) if inputbox2_status else (255, 0, 0) if error_message_2 else (0, 0, 0), 
                 input_box2,
                 5)

        # places the input text on the screen in the input boxes
        input_text_surface = get_font(int(current_width / 60)).render(input_text1, True, (0, 0, 0))
        SCREEN.blit(input_text_surface, (input_box1.x + 5, input_box1.y + 15))
        
        input_text_surface = get_font(int(current_width / 60)).render(input_text2, True, (0, 0, 0))
        SCREEN.blit(input_text_surface, (input_box2.x + 5, input_box2.y + 15))


        # drawing back button
        BACK_BUTTON = Button(image=pygame.transform.scale(second_image, (int(current_width * 0.1), int(current_height * 0.05))),
                             pos=(75, 25), text_input="BACK", font=get_font(int(current_width / 60)),
                             base_color=(0, 0, 0), hovering_color=(25, 51, 0))


        # update buttons color depending on where the cursor is
        for button in [BACK_BUTTON]:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(SCREEN)

        # for each event
        for event in pygame.event.get():
            # if X is pressed then exit game
            if event.type == pygame.QUIT:
                quit_sound.play()
                time.sleep(0.7)
                pygame.quit()
                sys.exit()

            # if enter is pressed then it submits input and validates
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                (good_input1, error_message_1) = custom_validation1(input_text1)
                (good_input2, error_message_2) = custom_validation2(input_text2)
                if good_input1 and good_input2:
                    gameplay(int(input_text1), int(input_text2))
                if not good_input1:
                    input_text1 = ""
                if not good_input2:
                    input_text2 = ""
                wrong_input_sound.play()
                inputbox1_status = False
                inputbox2_status = False
            
            # if a button besides escape is pressed it adds to the input text or removes if backspace is the pressed button
            elif event.type == pygame.KEYDOWN and event.key != pygame.K_ESCAPE:
                if inputbox1_status:
                    if event.key == pygame.K_BACKSPACE:
                        input_text1 = input_text1[:-1]
                    else:
                        input_text1 += event.unicode
                elif inputbox2_status:
                    if event.key == pygame.K_BACKSPACE:
                        input_text2 = input_text2[:-1]
                    else:
                        input_text2 += event.unicode
                else:
                    pass

            # if escape is pressed it goes back to main
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                main()

            # if first box is clicked change status to change color at the beginning of loop
            elif event.type == pygame.MOUSEBUTTONDOWN and input_box1.collidepoint(PLAY_MOUSE_POS):
                rect_sound.play()
                inputbox1_status = True
                inputbox2_status = False

            # if second box is clicked change status to change color at the beginning of loop
            elif event.type == pygame.MOUSEBUTTONDOWN and input_box2.collidepoint(PLAY_MOUSE_POS):
                rect_sound.play()
                inputbox1_status = False
                inputbox2_status = True

            # if back button is clicked go back to main loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    main()
            
        # update screen and set frame rate to 60
        pygame.display.update()
        clock.tick(60)


def statistics():

    # play the clicking sound
    button_click_sound.play()
    time.sleep(0.3)
    button_click_sound.stop()

    # create a statistics instance which takes the data from the database file
    statistics = Statistics()
    while True:

        # get current height and width of screen
        current_width = crt_w()
        current_height = crt_h()

        # cover with white and transform background to current width and height
        SCREEN.fill("white")
        SCREEN.blit(pygame.transform.scale(BG, (current_width, current_height)), (0, 0))

        # get mouse position
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        # resize button image, get upper left corner and blit it there
        resized_image = pygame.transform.scale(second_image, (current_width * 0.8 , current_height * 0.8))
        image_width, image_height = resized_image.get_size()
        x = (current_width - image_width) / 2
        y = (current_height - image_height) / 2
        SCREEN.blit(resized_image, (x, y))

        # draws box for statistics text
        box = pygame.Rect(current_width * 0.3, current_height * 0.13, current_width * 0.4, current_height * 0.08)
        pygame.draw.rect(SCREEN, (0, 0, 0), box, 0)

        # place text in the box
        STATISTICS_TEXT = get_font(int(current_width / 25)).render("STATISTICS", True, "#FB773C")
        STATISTICS_RECT = STATISTICS_TEXT.get_rect(center=(current_width / 2, current_height * 0.17))
        SCREEN.blit(STATISTICS_TEXT, STATISTICS_RECT)

        # place the statistics in the resized transparent image
        STATISTICS_TEXT = get_font(int(current_width / 60)).render("Total Games Played:" + " " * 5 + str(statistics.total_games), True, (255, 255, 255))
        STATISTICS_RECT = STATISTICS_TEXT.get_rect(center=(current_width / 3, current_height * 0.35))
        SCREEN.blit(STATISTICS_TEXT, STATISTICS_RECT)

        STATISTICS_TEXT = get_font(int(current_width / 60)).render("Total Wins:" + " " * 5 + str(statistics.total_wins), True, (255, 255, 255))
        STATISTICS_RECT = STATISTICS_TEXT.get_rect(center=(current_width / 3, current_height * 0.45))
        SCREEN.blit(STATISTICS_TEXT, STATISTICS_RECT)

        STATISTICS_TEXT = get_font(int(current_width / 60)).render("Total Losses:" + " " * 5 + str(statistics.total_losses), True, (255, 255, 255))
        STATISTICS_RECT = STATISTICS_TEXT.get_rect(center=(current_width / 3, current_height * 0.55))
        SCREEN.blit(STATISTICS_TEXT, STATISTICS_RECT)

        STATISTICS_TEXT = get_font(int(current_width / 60)).render("Total Blackjacks:" + " " * 5 + str(statistics.total_blackjacks), True, (255, 255, 255))
        STATISTICS_RECT = STATISTICS_TEXT.get_rect(center=(current_width / 3, current_height * 0.65))
        SCREEN.blit(STATISTICS_TEXT, STATISTICS_RECT)

        STATISTICS_TEXT = get_font(int(current_width / 60)).render("Total Profit:" + " " * 5 + str(statistics.profit) , True, (255, 255, 255))
        STATISTICS_RECT = STATISTICS_TEXT.get_rect(center=(current_width / 3, current_height * 0.75))
        SCREEN.blit(STATISTICS_TEXT, STATISTICS_RECT)


        
        # create back button
        BACK_BUTTON = Button(image=pygame.transform.scale(second_image, (int(current_width * 0.1), int(current_height * 0.05))),
                             pos=(75, 25), text_input="BACK", font=get_font(int(current_width / 60)),
                             base_color=(0, 0, 0), hovering_color=(25, 51, 0))

        # # update button color depending on where the cursor is
        for button in [BACK_BUTTON]:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(SCREEN)

        # for each event
        for event in pygame.event.get():
            # if X is pressed quit game
            if event.type == pygame.QUIT:
                quit_sound.play()
                time.sleep(0.7)
                pygame.quit()
                sys.exit()
            # if back is clicked run main loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    main()
            # if esc is pressed run main loop, go back
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                main()

        # update screen and set frame rate to 60
        pygame.display.update()
        clock.tick(60)


def gameplay(deck_number, initial_balance):
    # fade music for 2 seconds
    pygame.mixer.music.fadeout(2000)

    # play 2nd music
    pygame.mixer.music.load("sounds/guitar_background.mp3")
    pygame.mixer.music.play(loops=-1)

    # play click sound
    button_click_sound.play()
    time.sleep(0.3)
    button_click_sound.stop()
    
    # create gameplay instance and run the loop function
    gameplay = Gameplay(SCREEN, table_bg, deck_number, initial_balance)
    gameplay.loop()



    # function for validating first box input
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
    


    # function fot validating second box input
def custom_validation2(input2):
    try:
        input2 = int(input2)
    except ValueError:
        return False, "input must be a number!"
    if input2 > 1000000:
        return False, "initial balance too big!"
    if input2 < 1000:
        return False, "initial balance too low!"
    if input2 % 1000 != 0:
        return False, "balance must be multiple of 1000!"
    return True, ""
    


if __name__ == "__main__":
    main()