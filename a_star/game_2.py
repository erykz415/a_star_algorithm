import pygame
import math

# Pygame initialization
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
GRID_SIZE = 20
CELL_SIZE = WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
START_COLOR = (0, 255, 255)
GOAL_COLOR = (255, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Pathfinding Visualization")

# Heuristic function
def heuristic(poz_x, poz_y, cel_x, cel_y):
    return math.sqrt((poz_x - cel_x) ** 2 + (poz_y - cel_y) ** 2)

# A* algorithm
def a_star(mapa, start, goal):
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    open_list = [start]
    closed_list = set()
    g_costs = {start: 0}
    f_costs = {start: heuristic(start[0], start[1], goal[0], goal[1])}
    parent = {}

    while open_list:
        current = min(open_list, key=lambda x: f_costs[x])
        open_list.remove(current)
        closed_list.add(current)

        if current == goal:
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(start)
            path.reverse()
            return path

        for dx, dy in directions:
            neighbour = (current[0] + dx, current[1] + dy)
            if 0 <= neighbour[0] < len(mapa) and 0 <= neighbour[1] < len(mapa[0]) and mapa[neighbour[0]][neighbour[1]] != 5:
                if neighbour not in closed_list:
                    g = g_costs[current] + 1
                    if neighbour not in g_costs or g < g_costs[neighbour]:
                        g_costs[neighbour] = g
                        f_costs[neighbour] = g + heuristic(neighbour[0], neighbour[1], goal[0], goal[1])
                        parent[neighbour] = current
                        if neighbour not in open_list:
                            open_list.append(neighbour)

    return None

# Draw grid
def draw_grid(grid, path=None):
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            rect = pygame.Rect(y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = WHITE
            if grid[x][y] == 5:
                color = BLACK
            elif (x, y) == start:
                color = START_COLOR
            elif (x, y) == goal:
                color = GOAL_COLOR
            if path and (x, y) in path:
                color = BLUE
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

# Main function
def main():
    global start, goal
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    start, goal = (0, 0), (GRID_SIZE - 1, GRID_SIZE - 1)

    running = True
    setting_obstacles = False

    while running:
        screen.fill(WHITE)
        draw_grid(grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif pygame.mouse.get_pressed()[0]:  # Left mouse button
                pos = pygame.mouse.get_pos()
                x, y = pos[1] // CELL_SIZE, pos[0] // CELL_SIZE
                if (x, y) != start and (x, y) != goal:
                    grid[x][y] = 5
            elif pygame.mouse.get_pressed()[2]:  # Right mouse button
                pos = pygame.mouse.get_pos()
                x, y = pos[1] // CELL_SIZE, pos[0] // CELL_SIZE
                if grid[x][y] == 5:
                    grid[x][y] = 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Start the pathfinding
                    path = a_star(grid, start, goal)
                    if path:
                        draw_grid(grid, path)
                        pygame.display.update()
                        pygame.time.wait(5000)
                    else:
                        print("No path found!")

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
