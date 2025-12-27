# path_planner.py
import heapq
from config import MAP_WIDTH, MAP_HEIGHT, STATIC_OBSTACLES

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def build_obstacle_map(other_cars):
    obstacles = set(STATIC_OBSTACLES)
    for c in other_cars:
        obstacles.add((c["x"], c["y"]))
    return obstacles

def a_star(start, goal, obstacles):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g = {start: 0}

    while open_list:
        _, current = heapq.heappop(open_list)
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return list(reversed(path))

        cx, cy = current
        for nx, ny in [(cx+1,cy), (cx-1,cy), (cx,cy+1), (cx,cy-1)]:
            if not (0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT):
                continue
            if (nx, ny) in obstacles:
                continue

            ng = g[current] + 1
            if (nx, ny) not in g or ng < g[(nx, ny)]:
                g[(nx, ny)] = ng
                heapq.heappush(
                    open_list,
                    (ng + heuristic((nx, ny), goal), (nx, ny))
                )
                came_from[(nx, ny)] = current
    return None

def should_yield(my_id, my_pos, other_cars):
    mx, my = my_pos
    for c in other_cars:
        if c["id"] < my_id:
            if abs(mx - c["x"]) <= 1 and abs(my - c["y"]) <= 1:
                return True
    return False
