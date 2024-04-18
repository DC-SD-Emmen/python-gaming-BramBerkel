import pygame
import random

pygame.init()

window_size = (750, 750)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("My Pygame Window")

GRID_SIZE = 75
GRID_WIDTH = window_size[0] // GRID_SIZE
GRID_HEIGHT = window_size[1] // GRID_SIZE

font = pygame.font.Font(None, 32)
titlefont = pygame.font.Font(None, 128)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

default = 0
hiddenArray = [[default for i in range(10)] for j in range(10)]


def arraygrid():

    carrier = 5
    battler = 4
    cruiser = 3
    submarine = 3
    destroyer = 2

    hiddenArray = [[False for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]

    ships = [carrier, battler, cruiser, submarine, destroyer]

    for ship in ships:
        orientation = random.randint(0, 1)
        if orientation == 0:  # horitzontal
            while True:
                ship_row = random.randint(0, GRID_WIDTH-1)
                ship_col = random.randint(0, GRID_HEIGHT-ship)
                if not any(hiddenArray[ship_row][c] for c in range(ship_col, ship_col+ship)):
                    for c in range(ship_col, ship_col+ship):
                        hiddenArray[ship_row][c] = True
                    break
        else:
            while True:
                ship_row = random.randint(0, GRID_WIDTH-ship)
                ship_col = random.randint(0, GRID_HEIGHT-1)
                if not any(hiddenArray[r][ship_col] for r in range(ship_row, ship_row+ship)):
                    for r in range(ship_row, ship_row+ship):
                        hiddenArray[r][ship_col] = True
                    break
    return hiddenArray

    # for row in range(GRID_HEIGHT):
    #     for col in range(GRID_WIDTH):
    #         accuracy = random.randint(0, 1)
    #         if accuracy == 0:
    #             hiddenArray[row][col] = 0
    #         if accuracy == 1:
    #             shippicking = 1
    #             while shippicking == 1:
    #                 shiptype = random.randint(1, 5)
    #                 if shiptype == 1:
    #                     if carrier == 0:
    #                         direction = random.randint(0, 1)
    #                         if direction == 0 and GRID_WIDTH > 5:
    #                             hiddenArray[row][col] = 1
    #                             # herhaal voor 5 keer
    #                             carrier = 1
    #                             shippicking = 0
    #                         elif direction == 1 and GRID_HEIGHT > 5:
    #                             hiddenArray[row][col] = 1
    #                             # herhaal 5 keer, maar verticaal
    #                             carrier = 1
    #                             shippicking = 0
    #                     else:
    #                         continue


buttons = []
def resetGrid():
    global buttons, hiddenArray
    buttons = []
    hiddenArray = arraygrid()

def drawgrid(grid):
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            color = (255, 255, 255) # if not grid[row][col] else (0, 255, 0)
            button = pygame.draw.rect(window, color, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(window, (0, 0, 0), (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
            buttons.append(button)
    pygame.display.update()

def main(screen):
    global current_screen

    if screen == "main":
        current_screen = "main"
        mainmenu()
    elif screen == "play":
        current_screen = "play"
        play()

def mainmenu():
    # while current_screen == "main":
    window.fill(WHITE)

    titlebox = pygame.Rect(0, 50, 750, 200)
    pygame.draw.rect(window, BLUE, titlebox)
    titletext = titlefont.render("Battleship", True, RED)
    titlerect = titletext.get_rect(center=(titlebox.center))
    window.blit(titletext, titlerect)

    playbutton = pygame.Rect(275, 350, 200, 50)
    pygame.draw.rect(window, BLACK, playbutton)
    playtext = font.render("Play", True, WHITE)
    playtextrect = playtext.get_rect(center=playbutton.center)
    window.blit(playtext, playtextrect)

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    mousepos = event.pos
                    if playbutton.collidepoint(mousepos):
                        main("play")
                        return

        pygame.display.update()


def play():
    resetGrid()
    grid = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    # Draw shapes
    window.fill(WHITE)
    drawgrid(grid)
    hiddenArray = arraygrid()
    clickcount = 0
    correctcount = 0
    showingscore = 0

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:  # Left mouse button clicked
                    # de hiddenArray bevat de 0 en 1
                    # controleren of de positie van de muis overeenkomt met grid
                    # als de positie van de muis overeenkomt met de grid, dan heb je op de grid geklikt,
                    # dan wil je de positie van de grid checken met de hiddenArray
                    # als de hiddenArray een 0 is op die plek, dan kan je de rectangle blauw maken
                    # as de hiddenArray een 1 is op die plek, dan kan je de rectangle (bijvoorbeeld) rood maken
                    if correctcount < 17:
                        mousepos = pygame.mouse.get_pos()
                        for i, button in enumerate(buttons):
                            if button.collidepoint(mousepos):
                                row = i // GRID_WIDTH
                                col = i % GRID_WIDTH
                                if hiddenArray[row][col]:
                                    pygame.draw.rect(window, RED, button)
                                    pygame.draw.rect(window, BLACK, button, 1)
                                    clickcount += 1
                                    correctcount += 1
                                else:
                                    pygame.draw.rect(window, BLUE, button)
                                    pygame.draw.rect(window, BLACK, button, 1)
                                    clickcount += 1
                                grid[row][col] = not grid[row][col]
                    elif correctcount == 17 and showingscore == 0:
                        scoredisplay = pygame.Rect(0, 200, 750, 350)
                        pygame.draw.rect(window, BLACK, scoredisplay)
                        gentext = "Turn count: " + str(clickcount)
                        scoretext = font.render(gentext, True, WHITE)
                        scorerect = scoretext.get_rect(center=scoredisplay.center)
                        window.blit(scoretext, scorerect)
                        showingscore = 1

                        # playbutton = pygame.Rect(300, 250, 175, 50)
                        # pygame.draw.rect(window, BLACK, playbutton)
                        # playtext = font.render("Play", True, WHITE)
                        # playtextrect = playtext.get_rect(center=playbutton.center)
                        # window.blit(playtext, playtextrect)

                    else:
                        main("main")
                        return

        # Update display
        pygame.display.flip()


if __name__ == "__main__":
    main("main")
