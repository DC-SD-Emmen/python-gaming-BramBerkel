import pygame
import random

pygame.init()

window_size = (750, 750)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("My Pygame Window")

GRID_SIZE = 70
GRID_WIDTH = window_size[0] // GRID_SIZE
GRID_HEIGHT = window_size[1] // GRID_SIZE


def drawgrid(grid):
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            color = (255, 255, 255) if not grid[row][col] else (0, 255, 0)
            pygame.draw.rect(window, color, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(window, (0, 0, 0), (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)


def main():
    grid = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:  # Left mouse button clicked
                    x, y = pygame.mouse.get_pos()
                    row = y // GRID_SIZE
                    col = x // GRID_SIZE
                    grid[row][col] = not grid[row][col]

        # Draw shapes
        window.fill((255, 255, 255))
        drawgrid(grid)

        # Update display
        pygame.display.flip()


if __name__ == "__main__":
    main()