import pygame
import math
from queue import PriorityQueue
import math

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('A* Path Finding Algorithm')

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neigbors = []
        self.width = width
        self.total_rows = total_rows
        
    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE
    
    def reset(self):
        self.color = WHITE
        

    def make_closed(self):
        self.color = RED
    
    def make_open(self):
        self.color = GREEN
    
    def make_barrier(self):
        self.color = BLACK
    
    def make_start(self):
        self.color = ORANGE
        
    def make_path(self):
        self.color = PURPLE
    
    def make_end(self):
        self.color = TURQUOISE
        
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        
    def update_neighbours(self, grid):
        self.neigbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neigbors.append((grid[self.row + 1][self.col], 1))
            
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neigbors.append((grid[self.row - 1][self.col], 1))
            
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neigbors.append((grid[self.row][self.col + 1], 1))
            
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neigbors.append((grid[self.row][self.col - 1], 1))
        
        if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col - 1].is_barrier(): # TOP LEFT
            self.neigbors.append((grid[self.row - 1][self.col - 1], math.sqrt(2)))
            
        if self.col < self.total_rows - 1 and self.row < self.total_rows - 1 and not grid[self.row + 1][self.col + 1].is_barrier(): # LOWER RIGHT
            self.neigbors.append((grid[self.row + 1][self.col + 1], math.sqrt(2)))
        
        if self.row > 0 and self.col < self.total_rows - 1 and not grid[self.row - 1][self.col + 1].is_barrier(): # TOP RIGHT
            self.neigbors.append((grid[self.row - 1][self.col + 1], math.sqrt(2)))
            
        if self.col > 0 and self.row < self.total_rows - 1 and not grid[self.row + 1][self.col - 1].is_barrier(): # LOWER LEFT
            self.neigbors.append((grid[self.row + 1][self.col - 1], math.sqrt(2)))
            
        # if self.col < self.total_rows - 1 and self.row < self.total_rows - 2 and not grid[self.row + 2][self.col + 1].is_barrier(): # L
        #     self.neigbors.append((grid[self.row + 2][self.col + 1], math.sqrt(5)))
            
        # if self.col > 0 and self.row < self.total_rows - 2 and not grid[self.row + 2][self.col - 1].is_barrier(): # REVERSED L
        #     self.neigbors.append((grid[self.row + 2][self.col - 1], math.sqrt(5)))
        
        # if self.row < self.total_rows - 1 and self.col > 1 and not grid[self.row + 1][self.col - 2].is_barrier(): # 90D L
        #     self.neigbors.append((grid[self.row + 1][self.col - 2], math.sqrt(5)))
            
        # if self.row > 0 and self.col > 1 and not grid[self.row - 1][self.col - 2].is_barrier(): # 90D REVERSED L
        #     self.neigbors.append((grid[self.row - 1][self.col - 2], math.sqrt(5)))
            
        # if self.row > 1 and self.col > 0 and not grid[self.row - 2][self.col - 1].is_barrier(): # 180D L
        #     self.neigbors.append((grid[self.row - 2][self.col - 1], math.sqrt(5)))
            
        # if self.row > 1 and self.col < self.total_rows - 1 and not grid[self.row - 2][self.col + 1].is_barrier(): # 180D REVERSED L
        #     self.neigbors.append((grid[self.row - 2][self.col + 1], math.sqrt(5)))
            
        # if self.row > 0 and self.col < self.total_rows - 2 and not grid[self.row - 1][self.col + 2].is_barrier(): # -90D L
        #     self.neigbors.append((grid[self.row - 1][self.col + 2], math.sqrt(5)))
            
        # if self.col < self.total_rows - 2 and self.row < self.total_rows - 1 and not grid[self.row + 1][self.col + 2].is_barrier(): # -90D REVERSED L
        #     self.neigbors.append((grid[self.row + 1][self.col + 2], math.sqrt(5)))
            
    def __lt__(self, other):
        return False
    
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        # for neigbor, distance in current.neigbors:
        #     if distance < math.sqrt(5):
        #         neigbor.make_path()
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot:float('inf') for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot:float('inf') for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    
    open_set_hash = {start}
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        if current == end:
            reconstruct_path(came_from, end, draw) # make path
            end.make_end()
            return True
        
        for neigbor, distance in current.neigbors:
            temp_g_score = g_score[current] + float(distance)
            
            if temp_g_score < g_score[neigbor]:
                came_from[neigbor] = current
                g_score[neigbor] = temp_g_score
                f_score[neigbor] = temp_g_score + h(neigbor.get_pos(), end.get_pos())
                if neigbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neigbor], count, neigbor))
                    open_set_hash.add(neigbor)
                    neigbor.make_open()
        draw()
        
        if current != start:
            current.make_closed()
    
    return False
                
    
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
            
    return grid

def draw_grid(win, rows, width):
    GAP = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * GAP), (width, i * GAP))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * GAP, 0), (j * GAP, width))
    
def draw(win, grid, rows, width):
    win.fill(WHITE)
    
    for row in grid:
        for spot in row:
            spot.draw(win)
            
    draw_grid(win, rows, width)
    pygame.display.update()
    
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    
    row = y // gap
    col = x // gap
    
    return row, col

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)
    
    start = None
    end = None
    
    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if pygame.mouse.get_pressed()[0]: #LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                    
                elif spot != end and spot != start:
                    spot.make_barrier()
                
            elif pygame.mouse.get_pressed()[2]: #RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                spot = grid[row][col]
                spot.reset()
                
                if spot == end:
                    start = None
                    
                if spot == start:
                    end = None
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)
                            
                    algorithm(lambda: draw(win, grid, ROWS, WIDTH), grid, start, end)
                    
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
    pygame.quit()
main(WIN, WIDTH)