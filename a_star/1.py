import math

def heuristic(poz_x, poz_y, cel_x, cel_y):
    return math.sqrt((poz_x - cel_x) ** 2 + (poz_y - cel_y) ** 2)

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

        if current == goal:
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(start)
            path.reverse()
            return path

    return None

def draw_path(grid, path):
    for x, y in path:
        grid[x][y] = 3
    return grid

def draw_grid(grid):
    for line in grid:
        print(" ".join(str(x) for x in line))

grid = []
with open('grid.txt', 'r') as file:
    for line in file:
        grid.append([int(x) for x in line.split()])

start = (0, 19)
goal = (19, 0)

path = a_star(grid, start, goal)
if path:
    print("Path found:", path)
    grid = draw_path(grid, path)
    draw_grid(grid)
else:
    print("Path could not be found.")

