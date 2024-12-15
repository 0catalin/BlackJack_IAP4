import pygame

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

# Shows player balance
def draw_balance_box(screen, balance):
    BALANCE_TEXT = get_font(int(crt_w() / 60)).render("BALANCE:", True, (255,215,0))
    screen.blit(BALANCE_TEXT, (crt_w() / 32, crt_h() / 1.2))
    AMOUNT_TEXT = get_font(int(crt_w() / 60)).render(str(balance) + "$", True, (255,215,0))
    screen.blit(AMOUNT_TEXT, (crt_w() / 32, crt_h() / 1.1))

# Places chip on table
def place_chip(screen, bet):
    AMOUNT_TEXT = get_font(int(crt_w() / 97)).render(str(int(bet)), True, (255,215,0))
    chip = pygame.image.load("assets/bet_chip.png")
    chip = pygame.transform.scale(chip, (crt_w() / 6.4 , crt_h() / 3.6))
    screen.blit(chip, (crt_w() / 2.5, crt_h() / 2.6))
    chip_rect = chip.get_rect()
    text_rect = AMOUNT_TEXT.get_rect()
    text_rect.center= chip_rect.center
    screen.blit(AMOUNT_TEXT, (crt_w() / 2.5 + text_rect.x, crt_h() / 2.6 + text_rect.y))

# Returns current width of the screen
def crt_w():
    return pygame.display.Info().current_w

# Returns current height of the screen
def crt_h():
    return pygame.display.Info().current_h
