import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (169, 169, 169)
YELLOW = (255, 255, 0)  # Open list color
PURPLE = (128, 0, 128)  # Closed list color

# Screen dimensions
WIDTH, HEIGHT = 800, 800
GRID_SIZE = 20  # Size of the grid cells
COLS = WIDTH // GRID_SIZE
ROWS = HEIGHT // GRID_SIZE

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Pathfinding Visualization")


# Heuristic function (Euclidean distance)
def heuristic(poz_x, poz_y, cel_x, cel_y):
    return math.sqrt((poz_x - cel_x) ** 2 + (poz_y - cel_y) ** 2)


# A* Algorithm
def a_star(mapa, start, goal):
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    open_list = [start]
    closed_list = set()
    g_costs = {start: 0}
    f_costs = {start: heuristic(start[0], start[1], goal[0], goal[1])}
    parent = {}
    steps = []

    while open_list:
        current = min(open_list, key=lambda x: f_costs[x])
        open_list.remove(current)
        closed_list.add(current)

        steps.append((current, "closed"))

        if current == goal:
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(start)
            path.reverse()
            return path, steps

        for dx, dy in directions:
            neighbour = (current[0] + dx, current[1] + dy)
            if 0 <= neighbour[0] < len(mapa) and 0 <= neighbour[1] < len(mapa[0]) and mapa[neighbour[0]][
                neighbour[1]] != 5:
                if neighbour not in closed_list:
                    g = g_costs[current] + 1
                    if neighbour not in g_costs or g < g_costs[neighbour]:
                        g_costs[neighbour] = g
                        f_costs[neighbour] = g + heuristic(neighbour[0], neighbour[1], goal[0], goal[1])
                        parent[neighbour] = current
                        if neighbour not in open_list:
                            open_list.append(neighbour)
                            steps.append((neighbour, "open"))

    return None, steps


# Draw grid
def draw_grid(mapa):
    for y in range(ROWS):
        for x in range(COLS):
            color = WHITE
            if mapa[y][x] == 1:  # Obstacle
                color = BLACK
            elif mapa[y][x] == 2:  # Start point
                color = GREEN
            elif mapa[y][x] == 3:  # Path
                color = BLUE
            elif mapa[y][x] == 4:  # Open list
                color = YELLOW
            elif mapa[y][x] == 5:  # Closed list
                color = PURPLE
            pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, GRAY, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)


# Main function to run the visualization
def main():
    # Create an empty grid (0 = empty space, 1 = obstacle)
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    # Default start and goal positions
    start = (0, 19)
    goal = (19, 0)

    grid[start[1]][start[0]] = 2  # Mark the start point
    grid[goal[1]][goal[0]] = 2  # Mark the goal point

    path = []
    is_running = True
    is_paused = False
    step_idx = 0
    steps = []

    while is_running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                grid_x, grid_y = mouse_x // GRID_SIZE, mouse_y // GRID_SIZE

                if event.button == 1:  # Left-click for start point
                    if grid[grid_y][grid_x] != 1:
                        grid[start[1]][start[0]] = 0  # Remove old start
                        start = (grid_x, grid_y)
                        grid[start[1]][start[0]] = 2  # Set new start point
                        path = []
                        steps = []
                elif event.button == 3:  # Right-click for obstacles
                    if grid[grid_y][grid_x] != 2:  # Prevent placing obstacles on start/goal
                        grid[grid_y][grid_x] = 1  # Place obstacle
                        path = []
                        steps = []
                elif event.button == 2:  # Middle-click for goal point
                    if grid[grid_y][grid_x] != 1:
                        grid[goal[1]][goal[0]] = 0  # Remove old goal
                        goal = (grid_x, grid_y)
                        grid[goal[1]][goal[0]] = 2  # Set new goal point
                        path = []
                        steps = []

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Space to start the algorithm
                    path, steps = a_star(grid, start, goal)
                    step_idx = 0
                    is_paused = True
                if event.key == pygame.K_c:  # Clear grid with 'C' key
                    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
                    grid[start[1]][start[0]] = 2
                    grid[goal[1]][goal[0]] = 2
                    path = []
                    steps = []
                    is_paused = False
                    step_idx = 0

        # Step-by-step visualization
        if path and is_paused:
            if step_idx < len(steps):
                # Mark the open and closed lists on the grid
                current_step, state = steps[step_idx]
                if state == "open":
                    grid[current_step[1]][current_step[0]] = 4  # Open list
                elif state == "closed":
                    grid[current_step[1]][current_step[0]] = 5  # Closed list
                step_idx += 1
            elif step_idx == len(steps):
                # Once done, mark the path
                for (x, y) in path:
                    grid[y][x] = 3  # Path

        draw_grid(grid)

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


"""Instructions:
Left-click to set the start point.
Right-click to place obstacles.
Middle-click to set the goal point.
Spacebar to run the algorithm step-by-step.
C to clear the grid and reset everything."""