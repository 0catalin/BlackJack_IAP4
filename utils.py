import pygame

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def draw_balance_box(screen, balance, width):
    pygame.draw.rect(screen, (0, 0, 0), (25, 595, 200, 100))
    BALANCE_TEXT = get_font(int(width / 60)).render("BALANCE:", True, (255,215,0))
    screen.blit(BALANCE_TEXT, (40, 610))
    AMOUNT_TEXT = get_font(int(width / 60)).render(str(balance) + "$", True, (255,215,0))
    screen.blit(AMOUNT_TEXT, (40, 650))
